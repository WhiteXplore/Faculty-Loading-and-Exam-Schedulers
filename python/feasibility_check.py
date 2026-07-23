"""
feasibility_check.py  -  Scheduling pre-assessment (no GA run).

Reads the SAME input views the scheduler uses (classes_course,
faculty_expertise_courses, rooms_view, programs, classes) and evaluates whether a
COMPLETE, no-unscheduled term is achievable - purely from supply vs demand. Runs
in well under a second (no genetic algorithm).

It reuses the scheduler's own formulas (compute_load, normalize_course_code) so
the pre-assessment agrees with what a real run would produce.

Output: a human-readable console report, then a machine-readable JSON readiness
report between ===JSON_START=== / ===JSON_END=== markers (same convention the
NestJS backend already parses for the scheduler).

Model - feasibility is a set of independent "gates"; a complete schedule needs
EVERY gate to clear (supply >= demand). Passing all gates is a NECESSARY, strong
indicator of schedulability - not an absolute guarantee, because timetabling also
needs slots to align. So the result is a readiness score + binding constraints.
"""

import os
import json
import importlib.util

# --- reuse the scheduler's engine, formulas and constants -------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    "faculty_ga_remar", os.path.join(_HERE, "faculty_ga_remar.py"))
ga = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ga)  # safe: the pipeline is under a __main__ guard

from sqlalchemy import Table, MetaData  # noqa: E402

# Derived operating capacities (Mon-Fri, 7AM-9PM minus a 1h lunch)
DAYS_PER_WEEK = 5
HOURS_PER_DAY = (ga.END_HOUR - ga.START_HOUR) - (ga.LUNCH_END - ga.LUNCH_START)  # 13
SECTION_WEEK_HOURS = HOURS_PER_DAY * DAYS_PER_WEEK          # 65 - a student section's ceiling
ROOM_WEEK_HOURS = HOURS_PER_DAY * DAYS_PER_WEEK             # 65 - one room's weekly capacity
FAC_WEEK_HOURS = 8 * DAYS_PER_WEEK                          # 40 - one faculty (8h/day cap)
F2F_FRACTION = ga.TARGET_FACE_TO_FACE_PERCENTAGE           # ~0.70 of lecture hours need a room

norm = ga.normalize_course_code


def _fetch(name):
    md = MetaData()
    return ga.fetch_table_data(Table(name, md, autoload_with=ga.engine))


def _contact_hours(c):
    """Physical contact hours per week for one section-course (lec x1 + lab x3)."""
    lec = c.get("course_lec") or 0
    lab = c.get("course_lab") or 0
    return lec * ga.LECTURE_UNIT_TO_HOUR + lab * ga.LAB_UNIT_TO_HOUR


def _load_units(c):
    return ga.compute_load(c.get("course_lec", 0) or 0, c.get("course_lab", 0) or 0)


def _status(util_pct, has_hard_fail=False):
    if has_hard_fail or util_pct > 100:
        return "FAIL"
    if util_pct > 85:
        return "WARN"
    return "PASS"


def evaluate():
    cc = _fetch("classes_course")
    fec = _fetch("faculty_expertise_courses")
    rooms = _fetch("rooms_view")
    programs = _fetch("programs")
    prog_code = {p["program_id"]: p.get("program_code") for p in programs}
    for c in cc:
        c["program_code"] = prog_code.get(c.get("program_id"), "?")

    # institute id -> readable name (for room offenders)
    inst_name = {}
    for it in _fetch("institutes"):
        inst_name[it.get("institute_id")] = (
            it.get("institute_name") or it.get("name")
            or f"Institute {it.get('institute_id')}")

    total_sections = len(cc)
    at_risk = set()            # class-course rows (by index) at risk of not scheduling

    # unique active faculty (one record per faculty_id) + their load caps + names
    fac = {}
    fac_name = {}
    for f in fec:
        fid = f.get("faculty_id")
        if fid is not None:
            fac_name.setdefault(fid, f.get("faculty_name"))
            if fid not in fac:
                fac[fid] = float(f.get("load_unit") or 0)
    active_fac = {fid: lu for fid, lu in fac.items() if lu and lu > 0}

    # normalized course_code -> set of qualified faculty_ids
    code_experts = {}
    for f in fec:
        code = f.get("course_code")
        if code:
            code_experts.setdefault(norm(code), set()).add(f.get("faculty_id"))

    gates = []
    prescriptions = []

    # -------- GATE 1: Expertise coverage (does every course have a teacher?) --
    offered_codes = {}   # normalized code -> [section indices]
    for i, c in enumerate(cc):
        offered_codes.setdefault(norm(c.get("course_code")), []).append(i)
    uncovered = {code: idxs for code, idxs in offered_codes.items()
                 if not code_experts.get(code)}
    uncovered_sections = sum(len(idxs) for idxs in uncovered.values())
    for idxs in uncovered.values():
        at_risk.update(idxs)
    uncovered_rows = []
    for code, idxs in uncovered.items():
        rep = cc[idxs[0]]
        progs_aff = sorted({cc[i].get("program_code") for i in idxs if cc[i].get("program_code")})
        uncovered_rows.append({
            "course_code": rep.get("course_code"),
            "title": (rep.get("course_title") or "")[:40],
            "sections": len(idxs),
            "programs": ", ".join(progs_aff)[:50],
        })
    uncovered_rows.sort(key=lambda r: -r["sections"])
    gates.append({
        "id": "expertise", "label": "Expertise coverage",
        "status": "FAIL" if uncovered else "PASS",
        "supply": len(offered_codes) - len(uncovered), "demand": len(offered_codes),
        "unit": "courses with a qualified teacher",
        "utilization_pct": 100 if not uncovered else round(100 * len(offered_codes) /
                            max(1, len(offered_codes) - len(uncovered))),
        "detail": (f"{len(uncovered)} course(s) covering {uncovered_sections} section(s) "
                   f"have NO registered faculty." if uncovered else
                   "Every offered course has at least one qualified faculty."),
        "prescription": (f"Register expertise (or hire) for {len(uncovered)} course(s)."
                         if uncovered else None),
        "offender_columns": [
            {"key": "course_code", "label": "Course"}, {"key": "title", "label": "Title"},
            {"key": "sections", "label": "Sections"}, {"key": "programs", "label": "Programs"}],
        "offenders": uncovered_rows[:40],
        "offenders_total": len(uncovered_rows),
    })
    if uncovered:
        prescriptions.append(f"Register expertise / hire for {len(uncovered)} course(s) "
                             f"({uncovered_sections} sections).")

    # -------- GATE 2: Faculty load capacity (teacher-units) -------------------
    demand_units = sum(_load_units(c) for c in cc)
    supply_units = sum(active_fac.values())
    u2 = round(100 * demand_units / max(1, supply_units))
    avg_cap = (supply_units / len(active_fac)) if active_fac else 1
    # secondary physical-hours check
    demand_hours = sum(_contact_hours(c) for c in cc)
    supply_hours = len(active_fac) * FAC_WEEK_HOURS
    presc2 = None
    if demand_units > supply_units:
        need = demand_units - supply_units
        presc2 = f"+{need:.0f} teacher-units (~{max(1, round(need / max(1, avg_cap)))} more faculty)."
        prescriptions.append(presc2)
    gates.append({
        "id": "faculty_load", "label": "Faculty load capacity",
        "status": _status(u2),
        "supply": round(supply_units, 1), "demand": round(demand_units, 1),
        "unit": "teacher load-units / week", "utilization_pct": u2,
        "detail": (f"{demand_units:.0f} of {supply_units:.0f} teacher-units used "
                   f"({u2}%). Physical hours: {demand_hours:.0f} of {supply_hours:.0f} "
                   f"({round(100 * demand_hours / max(1, supply_hours))}%). "
                   f"{len(active_fac)} active faculty."),
        "prescription": presc2,
    })

    # -------- GATE 3: Per-course capacity (specialist bottlenecks) ------------
    short_pools = []
    for code, idxs in offered_codes.items():
        experts = code_experts.get(code)
        if not experts:
            continue  # already counted in gate 1
        pool_demand = sum(_load_units(cc[i]) for i in idxs)
        pool_supply = sum(fac.get(fid, 0) for fid in experts)   # generous upper bound
        if pool_demand > pool_supply:
            rep = cc[idxs[0]]
            short_pools.append({
                "course_code": rep.get("course_code"), "sections": len(idxs),
                "demand_units": round(pool_demand, 1),
                "their_total_cap": round(pool_supply, 1),
                "faculty": ", ".join(sorted(str(fac_name.get(fid) or fid) for fid in experts))[:70],
            })
            at_risk.update(idxs)
    short_pools.sort(key=lambda p: -(p["demand_units"] - p["their_total_cap"]))
    g3_status = "FAIL" if len(short_pools) > 5 else ("WARN" if short_pools else "PASS")
    gates.append({
        "id": "per_pool", "label": "Per-course capacity",
        "status": g3_status,
        "supply": len(offered_codes) - len(short_pools), "demand": len(offered_codes),
        "unit": "course pools within capacity",
        "utilization_pct": round(100 * len(offered_codes) /
                                 max(1, len(offered_codes) - len(short_pools))) if short_pools else 100,
        "detail": (f"{len(short_pools)} course pool(s) demand more load than their "
                   f"qualified faculty can hold (even if dedicated)." if short_pools else
                   "Every course pool has enough qualified-faculty capacity."),
        "prescription": (f"Add faculty / register more experts for {len(short_pools)} "
                         f"course pool(s), or reduce sections." if short_pools else None),
        "offender_columns": [
            {"key": "course_code", "label": "Course"}, {"key": "sections", "label": "Sections"},
            {"key": "demand_units", "label": "Demand (u)"}, {"key": "their_total_cap", "label": "Faculty cap (u)"},
            {"key": "faculty", "label": "Qualified faculty"}],
        "offenders": short_pools[:40],
        "offenders_total": len(short_pools),
    })
    if short_pools:
        prescriptions.append(f"Relieve {len(short_pools)} over-subscribed course pool(s) "
                             f"(e.g. {', '.join(p['course_code'] for p in short_pools[:3])}).")

    # -------- GATE 4: Room capacity ------------------------------------------
    # Lab rooms are owned per-institute; lecture rooms are shared but branch-scoped.
    lab_rooms_by_inst, lec_rooms_by_branch = {}, {}
    for r in rooms:
        t = str(r.get("room_type", "")).lower()
        if t == "laboratory":
            lab_rooms_by_inst[r.get("institute_id")] = lab_rooms_by_inst.get(r.get("institute_id"), 0) + 1
        elif t == "lecture":
            lec_rooms_by_branch[r.get("branch_id")] = lec_rooms_by_branch.get(r.get("branch_id"), 0) + 1

    lab_demand_by_inst, lec_demand_by_branch = {}, {}
    lab_idx_by_inst = {}
    for i, c in enumerate(cc):
        lab_h = (c.get("course_lab") or 0) * ga.LAB_UNIT_TO_HOUR
        lec_h = (c.get("course_lec") or 0) * ga.LECTURE_UNIT_TO_HOUR * F2F_FRACTION
        inst, br = c.get("institute_id"), c.get("branch_id")
        if lab_h:
            lab_demand_by_inst[inst] = lab_demand_by_inst.get(inst, 0) + lab_h
            lab_idx_by_inst.setdefault(inst, []).append(i)
        if lec_h:
            lec_demand_by_branch[br] = lec_demand_by_branch.get(br, 0) + lec_h

    lab_offenders = []
    for inst, dem in lab_demand_by_inst.items():
        n = lab_rooms_by_inst.get(inst, 0)
        sup = n * ROOM_WEEK_HOURS
        if dem > sup:
            need = -(-(dem - sup) // ROOM_WEEK_HOURS)  # ceil
            lab_offenders.append({"institute": inst_name.get(inst, f"Institute {inst}"),
                                  "lab_rooms": n,
                                  "demand_hours": round(dem), "supply_hours": sup,
                                  "rooms_needed": int(need)})
            at_risk.update(lab_idx_by_inst.get(inst, []))
    lab_offenders.sort(key=lambda x: -(x["demand_hours"] - x["supply_hours"]))
    tot_lab_dem = sum(lab_demand_by_inst.values())
    tot_lab_sup = sum(lab_rooms_by_inst.get(i, 0) for i in lab_demand_by_inst) * ROOM_WEEK_HOURS
    u4 = round(100 * tot_lab_dem / max(1, tot_lab_sup))
    hard_lab = any(o["lab_rooms"] == 0 for o in lab_offenders)
    gates.append({
        "id": "rooms_lab", "label": "Lab rooms (per institute)",
        "status": "FAIL" if lab_offenders else _status(u4),
        "supply": round(tot_lab_sup), "demand": round(tot_lab_dem),
        "unit": "lab room-hours / week", "utilization_pct": u4,
        "detail": (f"{len(lab_offenders)} institute(s) lack enough lab rooms"
                   + (" (some own ZERO)." if hard_lab else ".") if lab_offenders
                   else "Lab-room supply covers lab demand in every institute."),
        "prescription": (f"Add/borrow lab rooms for {len(lab_offenders)} institute(s)."
                         if lab_offenders else None),
        "offender_columns": [
            {"key": "institute", "label": "Institute"}, {"key": "lab_rooms", "label": "Lab rooms"},
            {"key": "demand_hours", "label": "Demand (h)"}, {"key": "supply_hours", "label": "Capacity (h)"},
            {"key": "rooms_needed", "label": "Rooms needed"}],
        "offenders": lab_offenders[:20],
        "offenders_total": len(lab_offenders),
    })
    if lab_offenders:
        total_needed = sum(o["rooms_needed"] for o in lab_offenders)
        prescriptions.append(f"+{total_needed} lab room(s) across "
                             f"{len(lab_offenders)} institute(s).")

    # lecture rooms — how much lecture can be face-to-face vs how much is FORCED online
    tot_lec_dem = sum(lec_demand_by_branch.values())              # demand at the 70% f2f target
    lec_full = tot_lec_dem / F2F_FRACTION if F2F_FRACTION else tot_lec_dem   # if 100% f2f
    tot_lec_sup = sum(lec_rooms_by_branch.values()) * ROOM_WEEK_HOURS
    u4b = round(100 * tot_lec_dem / max(1, tot_lec_sup))
    # with every lecture room filled: max % of lecture hours that fit face-to-face
    max_f2f_pct = 100 if lec_full <= tot_lec_sup else round(100 * tot_lec_sup / max(1, lec_full))
    required_online_pct = max(0, 100 - max_f2f_pct)              # the rest MUST be online
    target_online_pct = round((1 - F2F_FRACTION) * 100)         # policy target (~30%)
    if required_online_pct > 0:
        lec_detail = (f"{tot_lec_dem:.0f} of {tot_lec_sup:.0f} lecture room-hours used ({u4b}%). "
                      f"With every lecture room filled, only {max_f2f_pct}% of lecture hours fit "
                      f"face-to-face — at least {required_online_pct}% MUST be online "
                      f"(policy online target: {target_online_pct}%).")
    else:
        lec_detail = (f"{tot_lec_dem:.0f} of {tot_lec_sup:.0f} lecture room-hours used ({u4b}%). "
                      f"Rooms can seat up to 100% of lectures face-to-face — no room-forced online "
                      f"(the {target_online_pct}% online target is a policy choice, not a room limit).")
    gates.append({
        "id": "rooms_lecture", "label": "Lecture rooms (overall)",
        "status": _status(u4b),
        "supply": round(tot_lec_sup), "demand": round(tot_lec_dem),
        "unit": "lecture room-hours / week", "utilization_pct": u4b,
        "max_f2f_pct": max_f2f_pct,
        "required_online_pct": required_online_pct,
        "target_online_pct": target_online_pct,
        "detail": lec_detail,
        "prescription": (
            f"Rooms force {required_online_pct}% of lectures online (> {target_online_pct}% target); "
            f"add ~{-(-(lec_full - tot_lec_sup)//ROOM_WEEK_HOURS):.0f} lecture room(s) to hold the target."
            if required_online_pct > target_online_pct else None),
    })
    if required_online_pct > target_online_pct:
        prescriptions.append(f"Lecture rooms force {required_online_pct}% online (target {target_online_pct}%) — "
                             f"add ~{-(-(lec_full - tot_lec_sup)//ROOM_WEEK_HOURS):.0f} lecture room(s).")

    # -------- GATE 5: Section feasibility (fits in the operating week?) -------
    sec_hours, sec_idx = {}, {}
    for i, c in enumerate(cc):
        cid = c.get("class_id")
        sec_hours[cid] = sec_hours.get(cid, 0) + _contact_hours(c)
        sec_idx.setdefault(cid, []).append(i)
    overpacked = []
    for cid, h in sec_hours.items():
        if h > SECTION_WEEK_HOURS:
            reps = [cc[i] for i in sec_idx.get(cid, [])]
            r0 = reps[0] if reps else {}
            overpacked.append({
                "class_id": cid,
                "section": r0.get("set_name", "?"),
                "program": r0.get("program_code", "?"),
                "hours": round(h),
                "courses": ", ".join(sorted({r.get("course_code") for r in reps if r.get("course_code")}))[:60],
            })
    overpacked.sort(key=lambda o: -o["hours"])
    tight = [cid for cid, h in sec_hours.items() if SECTION_WEEK_HOURS >= h > SECTION_WEEK_HOURS * 0.85]
    for o in overpacked:
        at_risk.update(sec_idx.get(o["class_id"], []))
    gates.append({
        "id": "section_fit", "label": "Section feasibility",
        "status": "FAIL" if overpacked else ("WARN" if tight else "PASS"),
        "supply": SECTION_WEEK_HOURS, "demand": max([round(h) for h in sec_hours.values()] + [0]),
        "unit": "hours / week (65 max per section)",
        "utilization_pct": round(100 * max([h for h in sec_hours.values()] + [0]) / SECTION_WEEK_HOURS),
        "detail": (f"{len(overpacked)} section(s) exceed the {SECTION_WEEK_HOURS}h week and "
                   f"cannot fit; {len(tight)} are tight (>85%)." if overpacked else
                   (f"{len(tight)} section(s) are tight (>85% of the week)." if tight else
                    "Every student section fits within the operating week.")),
        "prescription": (f"Trim {len(overpacked)} over-packed section(s) (fewer/lighter courses)."
                         if overpacked else None),
        "offender_columns": [
            {"key": "section", "label": "Section"}, {"key": "program", "label": "Program"},
            {"key": "hours", "label": "Hours/wk"}, {"key": "courses", "label": "Courses"}],
        "offenders": overpacked[:20],
        "offenders_total": len(overpacked),
    })
    if overpacked:
        prescriptions.append(f"Trim {len(overpacked)} over-packed section(s) (> {SECTION_WEEK_HOURS}h).")

    # -------- overall verdict + estimate -------------------------------------
    statuses = [g["status"] for g in gates]
    if "FAIL" in statuses:
        verdict = "NOT_READY"
    elif "WARN" in statuses:
        verdict = "READY_WITH_GAPS"
    else:
        verdict = "READY"
    schedulable_pct = round(100 * (total_sections - len(at_risk)) / max(1, total_sections))

    # -------- structured recommendations (what to set up, grouped) -----------
    recommendations = []
    if uncovered_rows:
        recommendations.append({
            "key": "register_expertise", "icon": "expertise", "priority": "high",
            "title": "Register faculty expertise (or hire)",
            "summary": f"{len(uncovered_rows)} course(s) — {uncovered_sections} section(s) — "
                       f"have no qualified faculty.",
            "impact": f"Unlocks up to {uncovered_sections} sections.",
            "items": [{"label": r["course_code"],
                       "sub": f'{r["sections"]} sec · {r["title"]}'} for r in uncovered_rows[:40]],
            "items_total": len(uncovered_rows),
        })
    if demand_units > supply_units or short_pools:
        bits = []
        if demand_units > supply_units:
            need = demand_units - supply_units
            bits.append(f"~{max(1, round(need / max(1, avg_cap)))} more faculty (+{need:.0f} units)")
        if short_pools:
            bits.append(f"more experts for {len(short_pools)} over-subscribed course(s)")
        recommendations.append({
            "key": "add_faculty", "icon": "faculty",
            "priority": "high" if demand_units > supply_units else "medium",
            "title": "Add faculty capacity",
            "summary": "Need " + " and ".join(bits) + ".",
            "impact": f"Relieves the specialist squeeze on {len(short_pools)} course pool(s).",
            "items": [{"label": p["course_code"],
                       "sub": f'need +{max(0, round(p["demand_units"] - p["their_total_cap"]))}u · '
                              f'now: {p["faculty"]}'} for p in short_pools[:40]],
            "items_total": len(short_pools),
        })
    if lab_offenders:
        total_rooms = sum(o["rooms_needed"] for o in lab_offenders)
        recommendations.append({
            "key": "add_lab_rooms", "icon": "lab",
            "priority": "high" if any(o["lab_rooms"] == 0 for o in lab_offenders) else "medium",
            "title": "Add / borrow lab rooms",
            "summary": f"+{total_rooms} lab room(s) across {len(lab_offenders)} institute(s).",
            "impact": "Lets lab-bearing courses be timetabled.",
            "items": [{"label": o["institute"],
                       "sub": f'has {o["lab_rooms"]} lab(s) · need +{o["rooms_needed"]}'}
                      for o in lab_offenders],
            "items_total": len(lab_offenders),
        })
    if tot_lec_dem > tot_lec_sup:
        need_lec = int(-(-(tot_lec_dem - tot_lec_sup) // ROOM_WEEK_HOURS))
        recommendations.append({
            "key": "add_lecture_rooms", "icon": "room", "priority": "medium",
            "title": "Add lecture rooms",
            "summary": f"+{need_lec} lecture room(s).",
            "impact": "Adds face-to-face lecture capacity.",
            "items": [], "items_total": 0,
        })
    if overpacked:
        recommendations.append({
            "key": "trim_sections", "icon": "section", "priority": "medium",
            "title": "Lighten over-packed sections",
            "summary": f"{len(overpacked)} section(s) exceed the {SECTION_WEEK_HOURS}h operating week.",
            "impact": "These cannot fully fit until trimmed.",
            "items": [{"label": f'{o["program"]} {o["section"]}',
                       "sub": f'{o["hours"]}h · {o["courses"]}'} for o in overpacked],
            "items_total": len(overpacked),
        })

    return {
        "verdict": verdict,
        "schedulable_estimate_pct": schedulable_pct,
        "at_risk_sections": len(at_risk),
        "totals": {
            "sections": total_sections,
            "active_faculty": len(active_fac),
            "faculty_total_capacity_units": round(sum(active_fac.values()), 1),
            "rooms": len(rooms),
        },
        "gates": gates,
        "recommendations": recommendations,
        "prescriptions": prescriptions or ["No blocking gaps found - schedule looks feasible."],
        "assumptions": {
            "section_week_hours": SECTION_WEEK_HOURS,
            "faculty_week_hours": FAC_WEEK_HOURS,
            "room_week_hours": ROOM_WEEK_HOURS,
            "f2f_fraction": F2F_FRACTION,
            "note": ("Necessary-not-sufficient: passing all gates strongly indicates a "
                     "full schedule is achievable, but timetabling alignment can still "
                     "leave a few classes unplaced."),
        },
    }


def _print_console(rep):
    icon = {"READY": "OK", "READY_WITH_GAPS": "WARN", "NOT_READY": "FAIL"}
    print("=" * 74)
    print(f" SCHEDULING READINESS: {rep['verdict']}   "
          f"(est. ~{rep['schedulable_estimate_pct']}% schedulable)")
    print("=" * 74)
    t = rep["totals"]
    print(f" Sections: {t['sections']} | Active faculty: {t['active_faculty']} "
          f"(cap {t['faculty_total_capacity_units']} units) | Rooms: {t['rooms']}")
    print("-" * 74)
    for g in rep["gates"]:
        print(f" [{icon.get('READY') if g['status']=='PASS' else g['status']:<4}] "
              f"{g['label']:<28} {g['utilization_pct']:>4}%  {g['detail'][:90]}")
    print("-" * 74)
    print(" TO REACH 100%:")
    for p in rep["prescriptions"]:
        print(f"   - {p}")
    print("=" * 74)


def main():
    rep = evaluate()
    _print_console(rep)
    print("===JSON_START===")
    print(json.dumps(rep, indent=2, default=str))
    print("===JSON_END===")


if __name__ == "__main__":
    main()
