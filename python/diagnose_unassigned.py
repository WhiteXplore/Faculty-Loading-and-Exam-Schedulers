"""
diagnose_unassigned.py — READ-ONLY diagnostic for "no-faculty (assignment gap)"
unscheduled sections.

It reuses faculty_ga_remar.py's own data loading + assign_faculty() (no scheduling,
no changes to the scheduler, no touching of existing outputs). For every section that
assign_faculty could not place, it classifies WHY and computes supply-vs-demand per
course pool, so you can tell which gaps are fixable by an algorithm (rebalancing),
which need a policy knob (overload / prep-limit / GenEd matching), and which need
staffing/data changes (no algorithm can fix those).

Output: a printed one-page summary + an Excel workbook + a JSON file in
faculty_loading_output/.

Run:  python diagnose_unassigned.py
"""

import os
import json
import importlib.util
from datetime import datetime
from collections import defaultdict

from sqlalchemy import Table, MetaData
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

# ---------------------------------------------------------------------------
# Import the scheduler module WITHOUT running its pipeline (guarded by __main__)
# ---------------------------------------------------------------------------
_HERE = os.path.dirname(os.path.abspath(__file__))
_SPEC = importlib.util.spec_from_file_location(
    "faculty_ga_remar", os.path.join(_HERE, "faculty_ga_remar.py"))
ga = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ga)


# ---------------------------------------------------------------------------
# Verdict categories
# ---------------------------------------------------------------------------
HIRE = "HIRE / REGISTER EXPERTISE"          # no qualified faculty at all (even loosened)
GENED = "GENED-MATCH FIX"                    # strict fails but course_code-only matches
REBALANCE = "REBALANCE / PREP-LIMIT"         # qualified faculty have spare load (optimizer/prep relax)
OVERLOAD = "OVERLOAD / HIRE"                 # qualified faculty exist but ALL truly full

VERDICT_ORDER = [REBALANCE, GENED, OVERLOAD, HIRE]
VERDICT_HELP = {
    REBALANCE: "Qualified faculty still have spare load — blocked by greedy ordering or the "
               "4-prep limit. An optimal (min-cost-flow) assignment or a higher PREP_LIMIT recovers these.",
    GENED:     "No faculty is registered for this course UNDER THIS PROGRAM, but faculty ARE "
               "registered for the same course_code under another program. Loosening the "
               "program_id match for GenEd/shared courses recovers these.",
    OVERLOAD:  "Qualified faculty exist but every one is already at their load cap. Needs overload "
               "allowance (raise MAX_LOAD) or more staff — no reshuffle can place these.",
    HIRE:      "No qualified faculty exists at all (not even course_code-only). Requires registering "
               "expertise in faculty_expertise_courses or hiring — no algorithm can fix these.",
}


def load_data():
    """Load the exact same tables __main__ uses, and enrich classes_course."""
    metadata = MetaData()
    eng = ga.engine

    def fetch(name):
        return ga.fetch_table_data(Table(name, metadata, autoload_with=eng))

    classes_course = fetch("classes_course")
    faculty_expertise_courses = fetch("faculty_expertise_courses")
    programs = fetch("programs")
    classes = fetch("classes")

    program_map = {p["program_id"]: p["program_code"] for p in programs}
    class_size_map = {c["class_id"]: c["class_size"] for c in classes}
    for cls in classes_course:
        cls["program_code"] = program_map.get(cls.get("program_id"), "Unknown")
        cls["class_size"] = class_size_map.get(cls.get("class_id"), 0)

    return classes_course, faculty_expertise_courses


def build_faculty_maps(faculty_expertise_courses, faculty_loads):
    """
    Returns:
      fac_info: fid -> {name, load_unit, total_units, spare}
      strict_fids: (course_code, program_id) -> set(fid)   [course_code AND program_id]
      loose_fids:  course_code -> set(fid)                  [course_code only]
    """
    fac_info = {}
    for fid, info in faculty_loads.items():
        load_unit = info.get("load_unit", ga.MAX_LOAD)
        total = info.get("total_units", 0.0)
        fac_info[fid] = {
            "name": info.get("faculty_name", str(fid)),
            "load_unit": load_unit,
            "total_units": total,
            "spare": max(0.0, load_unit - total),
        }

    strict_fids = defaultdict(set)
    loose_fids = defaultdict(set)
    for f in faculty_expertise_courses:
        fid = f.get("faculty_id")
        cc = f.get("course_code")
        pid = f.get("program_id")
        if fid is None or cc is None:
            continue
        strict_fids[(cc, pid)].add(fid)
        loose_fids[cc].add(fid)

    return fac_info, strict_fids, loose_fids


def classify(course, fac_info, strict_fids, loose_fids):
    """Return (verdict, metrics dict) for one unassigned section."""
    cc = course.get("course_code")
    pid = course.get("program_id")
    units = ga.compute_load(course.get("course_lec", 0), course.get("course_lab", 0))

    strict_q = strict_fids.get((cc, pid), set())
    loose_q = loose_fids.get(cc, set())

    def spare(fids):
        return sum(fac_info[fid]["spare"] for fid in fids if fid in fac_info)

    strict_spare = spare(strict_q)
    loose_spare = spare(loose_q)

    if not loose_q:
        verdict = HIRE
    elif not strict_q:
        verdict = GENED
    elif strict_spare >= units:
        verdict = REBALANCE
    else:
        verdict = OVERLOAD

    return verdict, {
        "units": units,
        "strict_faculty": len(strict_q),
        "strict_spare": strict_spare,
        "loose_faculty": len(loose_q),
        "loose_spare": loose_spare,
    }


def main():
    print("Loading data + running assign_faculty (read-only)...")
    classes_course, fec = load_data()
    faculty_loads, unassigned = ga.assign_faculty(classes_course, fec)

    fac_info, strict_fids, loose_fids = build_faculty_maps(fec, faculty_loads)

    # Classify every unassigned section
    rows = []
    for course in unassigned:
        verdict, m = classify(course, fac_info, strict_fids, loose_fids)
        rows.append({
            "class_id": course.get("class_id"),
            "course_code": course.get("course_code"),
            "program_code": course.get("program_code", "Unknown"),
            "program_id": course.get("program_id"),
            "section": course.get("set_name", "?"),
            "institute_id": course.get("institute_id"),
            "type": "Lecture+Lab" if course.get("course_lab", 0) else "Lecture",
            "units": round(m["units"], 2),
            "strict_faculty": m["strict_faculty"],
            "strict_spare": round(m["strict_spare"], 2),
            "loose_faculty": m["loose_faculty"],
            "verdict": verdict,
        })

    # Category counts
    cat_counts = defaultdict(int)
    for r in rows:
        cat_counts[r["verdict"]] += 1

    # Per-course-pool supply/demand (grouped by course_code)
    pools = defaultdict(lambda: {"sections": 0, "demand": 0.0, "verdicts": defaultdict(int),
                                 "programs": set()})
    for r in rows:
        p = pools[r["course_code"]]
        p["sections"] += 1
        p["demand"] += r["units"]
        p["verdicts"][r["verdict"]] += 1
        p["programs"].add(r["program_code"])
    pool_rows = []
    for cc, p in pools.items():
        # a pool's headline verdict = the most severe among its sections
        headline = next((v for v in [HIRE, OVERLOAD, GENED, REBALANCE]
                         if p["verdicts"].get(v)), REBALANCE)
        loose_q = loose_fids.get(cc, set())
        loose_spare = sum(fac_info[fid]["spare"] for fid in loose_q if fid in fac_info)
        pool_rows.append({
            "course_code": cc,
            "sections": p["sections"],
            "unit_demand": round(p["demand"], 2),
            "qualified_faculty_any_program": len(loose_q),
            "their_total_spare_units": round(loose_spare, 2),
            "programs_affected": len(p["programs"]),
            "headline_verdict": headline,
        })
    pool_rows.sort(key=lambda x: (-x["sections"], x["course_code"]))

    # Bottleneck faculty: those at capacity who are named as possible_faculty a lot
    from collections import Counter
    named = Counter()
    for course in unassigned:
        for nm in course.get("possible_faculty", []):
            named[nm] += 1
    full_by_name = {info["name"]: info for info in fac_info.values()
                    if info["spare"] <= 0.001}
    bottleneck = []
    for nm, cnt in named.most_common():
        if nm in full_by_name:
            info = full_by_name[nm]
            bottleneck.append({
                "faculty": nm,
                "load": f"{round(info['total_units'],2)}/{info['load_unit']}",
                "times_needed_but_full": cnt,
            })

    # ---------------- PRINTED ONE-PAGE SUMMARY ----------------
    total = len(rows)
    print("\n" + "=" * 78)
    print(" UNASSIGNED-SECTION DIAGNOSTIC  (no-faculty / assignment gap)")
    print("=" * 78)
    print(f" Total sections with NO faculty assigned: {total}")
    print("-" * 78)
    print(" Split by root cause (most actionable first):")
    for v in VERDICT_ORDER:
        print(f"   {cat_counts.get(v,0):4d}  {v}")
    print("-" * 78)
    fixable = cat_counts.get(REBALANCE, 0) + cat_counts.get(GENED, 0)
    print(f" Algorithm/policy-fixable (REBALANCE + GENED): {fixable}")
    print(f" Needs staffing/data      (OVERLOAD + HIRE):   "
          f"{cat_counts.get(OVERLOAD,0) + cat_counts.get(HIRE,0)}")
    print("-" * 78)
    print(" Top course pools by unassigned sections:")
    print(f"   {'course':<16}{'secs':>5}{'demand':>8}{'qual.fac':>9}{'spare':>7}  verdict")
    for pr in pool_rows[:12]:
        print(f"   {pr['course_code'][:15]:<16}{pr['sections']:>5}{pr['unit_demand']:>8.1f}"
              f"{pr['qualified_faculty_any_program']:>9}{pr['their_total_spare_units']:>7.1f}"
              f"  {pr['headline_verdict']}")
    print("-" * 78)
    print(" Most-overloaded bottleneck faculty (qualified but full):")
    for b in bottleneck[:8]:
        print(f"   {b['faculty'][:34]:<35} load {b['load']:<9} blocked {b['times_needed_but_full']} section(s)")
    print("=" * 78)
    print(" Verdict legend:")
    for v in VERDICT_ORDER:
        print(f"  * {v}: {VERDICT_HELP[v]}")
    print("=" * 78)

    # ---------------- WRITE EXCEL + JSON ----------------
    out_dir = os.path.join(_HERE, "faculty_loading_output")
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    xlsx_path = os.path.join(out_dir, f"unassigned_diagnostic_{ts}.xlsx")
    json_path = os.path.join(out_dir, f"unassigned_diagnostic_{ts}.json")

    wb = Workbook()
    hdr_fill = PatternFill("solid", fgColor="305496")
    hdr_font = Font(bold=True, color="FFFFFF")

    def write_sheet(ws, headers, data_rows):
        ws.append(headers)
        for c in ws[1]:
            c.fill = hdr_fill
            c.font = hdr_font
            c.alignment = Alignment(horizontal="center")
        for r in data_rows:
            ws.append(r)
        for i, h in enumerate(headers, 1):
            ws.column_dimensions[chr(64 + i) if i <= 26 else "A"].width = max(12, len(str(h)) + 3)

    ws1 = wb.active
    ws1.title = "Summary"
    write_sheet(ws1, ["Metric", "Value"], [
        ["Total no-faculty sections", total],
        *[[v, cat_counts.get(v, 0)] for v in VERDICT_ORDER],
        ["Algorithm/policy-fixable (REBALANCE+GENED)", fixable],
        ["Needs staffing/data (OVERLOAD+HIRE)",
         cat_counts.get(OVERLOAD, 0) + cat_counts.get(HIRE, 0)],
    ])
    ws1.append([])
    ws1.append(["Verdict", "What it means"])
    for v in VERDICT_ORDER:
        ws1.append([v, VERDICT_HELP[v]])

    ws2 = wb.create_sheet("By Course Pool")
    write_sheet(ws2,
                ["course_code", "sections", "unit_demand", "qualified_faculty_any_program",
                 "their_total_spare_units", "programs_affected", "headline_verdict"],
                [[pr["course_code"], pr["sections"], pr["unit_demand"],
                  pr["qualified_faculty_any_program"], pr["their_total_spare_units"],
                  pr["programs_affected"], pr["headline_verdict"]] for pr in pool_rows])

    ws3 = wb.create_sheet("Unassigned Detail")
    write_sheet(ws3,
                ["class_id", "course_code", "program_code", "section", "type", "units",
                 "strict_faculty", "strict_spare", "loose_faculty", "verdict"],
                [[r["class_id"], r["course_code"], r["program_code"], r["section"], r["type"],
                  r["units"], r["strict_faculty"], r["strict_spare"], r["loose_faculty"],
                  r["verdict"]] for r in sorted(rows, key=lambda x: (x["verdict"], x["course_code"]))])

    ws4 = wb.create_sheet("Bottleneck Faculty")
    write_sheet(ws4, ["faculty", "load", "times_needed_but_full"],
                [[b["faculty"], b["load"], b["times_needed_but_full"]] for b in bottleneck])

    wb.save(xlsx_path)

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({
            "generated_at": ts,
            "total_no_faculty_sections": total,
            "category_counts": {v: cat_counts.get(v, 0) for v in VERDICT_ORDER},
            "algorithm_or_policy_fixable": fixable,
            "needs_staffing_or_data": cat_counts.get(OVERLOAD, 0) + cat_counts.get(HIRE, 0),
            "by_course_pool": pool_rows,
            "unassigned_detail": rows,
            "bottleneck_faculty": bottleneck,
            "verdict_legend": VERDICT_HELP,
        }, fh, indent=2, default=str)

    print(f"\n[OK] Excel written: {xlsx_path}")
    print(f"[OK] JSON  written: {json_path}")


if __name__ == "__main__":
    main()
