"""
Weekend Scheduler — Masteral and Special Programs
Extension of faculty_ga_remar.py (shares all helper functions).

Masteral Mode  : Saturday only, 8:00 AM – 5:00 PM (9 hours per class)
Special Mode   : Saturday or Sunday, 8:00 AM – 5:00 PM (9 hours per class)

Core rules:
- One class = one whole day block (no splitting, no patterns)
- One class per faculty per day (no double-booking)
- Face-to-face only (no online)
- Fixed deterministic assignment — try Saturday [then Sunday for Special]
- All weekday helper functions reused unchanged (faculty/room/class/branch checks)

Usage:
    python faculty_loading_for_materal_and_dnli.py masteral
    python faculty_loading_for_materal_and_dnli.py special
"""

import json
import os
import random
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from sqlalchemy import Table, select
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------------------
# Reuse all shared helpers from the main scheduler.
# Importing faculty_ga_remar executes its module-level DB setup (safe — uses
# pool_pre_ping, and none of its auto-run code calls create_schedule()).
# ---------------------------------------------------------------------------
from faculty_ga_remar import (
    MAX_LOAD,
    MAIN_BRANCH_ID,
    assign_faculty,
    check_time_overlap,
    check_travel_time_compatible,
    compute_load,
    engine,
    fetch_table_data,
    find_suitable_room,
    is_branch_available,
    is_class_available,
    is_faculty_available,
    is_room_available,
    metadata,
    parse_preferred_time,
    update_branch_tracker,
)


# ==============================================================
# WEEKEND CONSTANTS
# ==============================================================

WEEKEND_START_HOUR = 8       # 8:00 AM
WEEKEND_END_HOUR = 17        # 5:00 PM
WEEKEND_FULL_DAY_DURATION = 9  # 8 AM–5 PM = 9 hours
WEEKEND_TIME_SLOT = "8:00 AM - 5:00 PM"

WEEKEND_DAYS_MASTERAL = ["Saturday"]
WEEKEND_DAYS_SPECIAL  = ["Saturday", "Sunday"]

# Day order used only for sorting Excel output
_WEEKEND_DAYS_ORDER = ["Saturday", "Sunday",
                       "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


# ==============================================================
# INTERNAL HELPERS  (not part of the public API)
# ==============================================================

def _try_day(
    day: str,
    cls: dict,
    rooms: list,
    faculty_id: int,
    schedule_tracker: dict,
    faculty_schedule_tracker: dict,
    class_schedule_tracker: dict,
    faculty_branch_tracker: dict,
    far_branch_set: set,
) -> Tuple[Optional[dict], Optional[str]]:
    """
    Try to book cls as a full 9-hour block on day.
    Returns (room_dict, None) on success, (None, fail_reason) on failure.
    """
    class_id  = cls["class_id"]
    branch_id = cls.get("branch_id")
    start     = WEEKEND_START_HOUR
    duration  = WEEKEND_FULL_DAY_DURATION

    if not is_faculty_available(faculty_id, day, start, duration, faculty_schedule_tracker):
        return None, f"Faculty already has a class on {day}"

    if not is_class_available(class_id, day, start, duration, class_schedule_tracker):
        return None, f"Class section already scheduled on {day}"

    if not is_branch_available(faculty_id, day, branch_id,
                                faculty_branch_tracker, far_branch_set):
        return None, f"Faculty branch conflict on {day}"

    room = find_suitable_room(
        rooms, "Lecture",
        cls.get("institute_id"), cls.get("class_size", 30),
        day, start, duration, schedule_tracker, branch_id,
    )
    if room is None:
        return None, f"No available lecture room on {day}"

    if not check_travel_time_compatible(
            faculty_id, day, start, duration,
            room.get("building_name"), room.get("time_travel", 0),
            faculty_schedule_tracker):
        return None, f"Travel time conflict on {day}"

    return room, None


def _commit(
    day: str,
    room: dict,
    cls: dict,
    faculty_id: int,
    schedule_tracker: dict,
    faculty_schedule_tracker: dict,
    class_schedule_tracker: dict,
    faculty_branch_tracker: dict,
) -> None:
    """Write the booked block into all four trackers (room, faculty, class, branch)."""
    room_id   = room["room_id"]
    class_id  = cls["class_id"]
    branch_id = cls.get("branch_id")
    start     = WEEKEND_START_HOUR
    duration  = WEEKEND_FULL_DAY_DURATION

    # Room tracker
    schedule_tracker.setdefault(room_id, {}).setdefault(day, []).append({
        "start_hour": start, "duration": duration,
        "class_id": class_id, "course_code": cls["course_code"],
    })

    # Faculty tracker
    faculty_schedule_tracker.setdefault(faculty_id, {}).setdefault(day, []).append({
        "start_hour":    start,
        "duration":      duration,
        "class_id":      class_id,
        "course_code":   cls["course_code"],
        "building_name": room.get("building_name"),
        "travel_time":   room.get("time_travel", 0),
    })

    # Class section tracker
    class_schedule_tracker.setdefault(class_id, {}).setdefault(day, []).append({
        "start_hour": start, "duration": duration,
        "faculty_id": faculty_id, "course_code": cls["course_code"],
    })

    # Branch tracker
    update_branch_tracker(faculty_id, [day], branch_id, faculty_branch_tracker)


def _meeting(cls: dict, day: str, room: dict) -> dict:
    """Build the standardised meeting dict returned by both schedulers."""
    return {
        "class_id":      cls["class_id"],
        "set_name":      cls["set_name"],
        "course_level":  cls["course_level"],
        "course_code":   cls["course_code"],
        "program_id":    cls["program_id"],
        "program_name":  cls.get("program_name", "Unknown"),
        "program_code":  cls.get("program_code", "Unknown"),
        "institute_id":  cls.get("institute_id"),
        "type":          "Lecture",
        "day":           day,
        "start_hour":    WEEKEND_START_HOUR,
        "duration":      WEEKEND_FULL_DAY_DURATION,
        "time_slot":     WEEKEND_TIME_SLOT,
        "room_id":       room["room_id"],
        "room_name":     room.get("room_name", "Unknown"),
        "room_type":     room.get("room_type", "Unknown"),
        "room_capacity": room.get("room_capacity", 0),
        "class_size":    cls.get("class_size", 30),
        "schedule_type": "face to face",
    }


def _unscheduled_entry(cls: dict, hours_label: str, reason: str) -> dict:
    """Build the standardised unscheduled-meetings dict used across the project."""
    return {
        "class_id":     cls["class_id"],
        "course_code":  cls["course_code"],
        "course_id":    cls.get("course_id"),
        "institute_id": cls.get("institute_id"),
        "class_size":   cls.get("class_size", 30),
        "faculty_name": cls.get("faculty_name", "Unknown"),
        "program_id":   cls["program_id"],
        "program_name": cls.get("program_name", "Unknown"),
        "program_code": cls.get("program_code", "Unknown"),
        "type":         "Lecture",
        "hours":        hours_label,
        "reason":       reason,
    }


# ==============================================================
# MASTERAL SCHEDULER
# ==============================================================

def schedule_masteral_class(
    cls: dict,
    rooms: list,
    faculty_id: int,
    employment_type: str,
    schedule_tracker: dict,
    faculty_schedule_tracker: dict,
    unscheduled_meetings: list,
    class_schedule_tracker: dict,
    faculty_branch_tracker: dict = None,
    far_branch_set: set = None,
) -> Optional[List[dict]]:
    """
    Schedule a Masteral class: Saturday only, 8:00 AM – 5:00 PM (9 hours).

    - Exactly one attempt: Saturday @ 8 AM, duration 9 h
    - No day patterns, no f2f/online split, no weekday fallback
    - Reuses is_faculty_available, is_class_available, is_branch_available,
      find_suitable_room, check_travel_time_compatible, update_branch_tracker

    Returns list with one meeting dict on success, or None (appending to
    unscheduled_meetings) on failure.
    """
    if faculty_branch_tracker is None:
        faculty_branch_tracker = {}
    if far_branch_set is None:
        far_branch_set = set()

    day = WEEKEND_DAYS_MASTERAL[0]  # "Saturday"

    room, reason = _try_day(
        day, cls, rooms, faculty_id,
        schedule_tracker, faculty_schedule_tracker,
        class_schedule_tracker, faculty_branch_tracker, far_branch_set,
    )

    if room is not None:
        _commit(day, room, cls, faculty_id,
                schedule_tracker, faculty_schedule_tracker,
                class_schedule_tracker, faculty_branch_tracker)
        return [_meeting(cls, day, room)]

    unscheduled_meetings.append(
        _unscheduled_entry(cls, "9h (Saturday full-day)", reason or "Cannot schedule on Saturday")
    )
    return None


# ==============================================================
# SPECIAL PROGRAM SCHEDULER
# ==============================================================

def schedule_special_program_class(
    cls: dict,
    rooms: list,
    faculty_id: int,
    employment_type: str,
    schedule_tracker: dict,
    faculty_schedule_tracker: dict,
    unscheduled_meetings: list,
    class_schedule_tracker: dict,
    faculty_branch_tracker: dict = None,
    far_branch_set: set = None,
) -> Optional[List[dict]]:
    """
    Schedule a Special Program class: Saturday or Sunday, 8:00 AM – 5:00 PM (9 hours).

    - Saturday is tried first; Sunday is the fallback.
    - If both days fail, the class is added to unscheduled_meetings.
    - No day patterns, no f2f/online split, no weekday fallback
    - Same conflict checks as schedule_masteral_class

    Returns list with one meeting dict on success, or None on failure.
    """
    if faculty_branch_tracker is None:
        faculty_branch_tracker = {}
    if far_branch_set is None:
        far_branch_set = set()

    last_reason = "Cannot schedule on Saturday or Sunday"

    for day in WEEKEND_DAYS_SPECIAL:  # ["Saturday", "Sunday"]
        room, reason = _try_day(
            day, cls, rooms, faculty_id,
            schedule_tracker, faculty_schedule_tracker,
            class_schedule_tracker, faculty_branch_tracker, far_branch_set,
        )
        if room is not None:
            _commit(day, room, cls, faculty_id,
                    schedule_tracker, faculty_schedule_tracker,
                    class_schedule_tracker, faculty_branch_tracker)
            return [_meeting(cls, day, room)]
        last_reason = reason

    unscheduled_meetings.append(
        _unscheduled_entry(cls, "9h (Sat/Sun full-day)", last_reason)
    )
    return None


# ==============================================================
# SCHEDULE VALIDATION
# ==============================================================

def validate_weekend_schedule(schedule: list) -> List[str]:
    """
    Check for faculty/room/class conflicts on Saturday and Sunday.
    Returns a list of human-readable conflict strings (empty = no conflicts).
    """
    conflicts: List[str] = []

    for day in ["Saturday", "Sunday"]:
        day_meetings = [m for m in schedule if m.get("day") == day]

        checks = [
            ("class_id",   "Class"),
            ("room_id",    "Room"),
            ("faculty_id", "Faculty"),
        ]
        for key, label in checks:
            groups: Dict[int, list] = {}
            for m in day_meetings:
                val = m.get(key)
                if val is None:
                    continue
                groups.setdefault(val, []).append(m)

            for val, meetings in groups.items():
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(
                                m1["start_hour"], m1["duration"],
                                m2["start_hour"], m2["duration"]):
                            conflicts.append(
                                f"{label} conflict (id={val}) on {day}: "
                                f"{m1['course_code']} vs {m2['course_code']}"
                            )
    return conflicts


# ==============================================================
# ORCHESTRATOR
# ==============================================================

def create_weekend_schedule(
    faculty_loads: dict,
    rooms: list,
    mode: str,
    branch_map: dict = None,
) -> Tuple[list, list]:
    """
    Create a complete weekend schedule for all faculty loads.

    Parameters
    ----------
    faculty_loads : dict
        Same structure as produced by assign_faculty() —
        {faculty_id: {faculty_name, employment_type, assigned_classes, ...}}
    rooms : list
        List of room dicts from rooms_view.
    mode : str
        "masteral" → Saturday only
        "special"  → Saturday or Sunday
    branch_map : dict, optional
        {college_branch_id: college_branch_name} for display/reporting.

    Returns
    -------
    (complete_schedule, unscheduled_meetings)
        complete_schedule     : list of meeting dicts (same format as create_schedule)
        unscheduled_meetings  : list of unscheduled dicts
    """
    if mode not in ("masteral", "special"):
        raise ValueError(f"Invalid mode '{mode}'. Use 'masteral' or 'special'.")

    # Fresh trackers per run — same structure as weekday scheduler
    schedule_tracker         = {}   # room_id -> {day -> [blocks]}
    faculty_schedule_tracker = {}   # faculty_id -> {day -> [blocks]}
    class_schedule_tracker   = {}   # class_id -> {day -> [blocks]}
    faculty_branch_tracker   = {}   # faculty_id -> {day -> {branch_ids}}
    far_branch_set           = set()

    complete_schedule    : list = []
    unscheduled_meetings : list = []

    mode_label = ("Masteral Program — Saturday only"
                  if mode == "masteral"
                  else "Special Program — Saturday or Sunday")

    print("\n" + "=" * 80)
    print(f"  WEEKEND SCHEDULING — {mode_label}")
    print("=" * 80)
    print("  Block  : 8:00 AM – 5:00 PM  (9 hours)")
    print("  Mode   : Face-to-face only  |  No patterns  |  No splitting")
    print("=" * 80)

    faculty_items = list(faculty_loads.items())
    random.shuffle(faculty_items)  # fair distribution across faculty

    for faculty_id, faculty_info in faculty_items:
        faculty_name    = faculty_info["faculty_name"]
        employment_type = faculty_info.get("employment_type", "full time")
        classes         = list(faculty_info.get("assigned_classes", []))

        if not classes:
            continue

        print(f"\n  Scheduling: {faculty_name} (ID: {faculty_id}) [{employment_type.title()}]"
              f" — {len(classes)} class(es)")

        random.shuffle(classes)

        for cls in classes:
            print(f"    {cls['course_code']}... ", end="", flush=True)

            if mode == "masteral":
                meetings = schedule_masteral_class(
                    cls, rooms, faculty_id, employment_type,
                    schedule_tracker, faculty_schedule_tracker,
                    unscheduled_meetings, class_schedule_tracker,
                    faculty_branch_tracker, far_branch_set,
                )
            else:
                meetings = schedule_special_program_class(
                    cls, rooms, faculty_id, employment_type,
                    schedule_tracker, faculty_schedule_tracker,
                    unscheduled_meetings, class_schedule_tracker,
                    faculty_branch_tracker, far_branch_set,
                )

            if meetings:
                for m in meetings:
                    m["faculty_id"]        = faculty_id
                    m["faculty_name"]      = faculty_name
                    m["employment_type"]   = employment_type
                    m["college_branch_id"] = cls.get("branch_id")
                    complete_schedule.append(m)
                assigned_day = meetings[0]["day"]
                print(f"[OK] → {assigned_day}  {WEEKEND_TIME_SLOT}")
            else:
                # fail_reason already appended inside the scheduler
                print("[FAILED]")

    # Summary
    print("\n" + "=" * 80)
    print(f"  Scheduling complete: {len(complete_schedule)} scheduled,"
          f" {len(unscheduled_meetings)} unscheduled")
    print("-" * 80)

    conflicts = validate_weekend_schedule(complete_schedule)
    if conflicts:
        print(f"  WARNING: {len(conflicts)} conflict(s) detected:")
        for c in conflicts[:10]:
            print(f"    - {c}")
        if len(conflicts) > 10:
            print(f"    ... and {len(conflicts) - 10} more")
    else:
        print("  No conflicts detected.")
    print("=" * 80)

    return complete_schedule, unscheduled_meetings


# ==============================================================
# EXCEL EXPORT
# ==============================================================

def save_weekend_schedule_to_excel(
    schedule: list,
    unscheduled: list,
    faculty_loads: dict,
    filename: str,
    mode: str,
) -> None:
    """
    Export weekend schedule to Excel.
    Matches the column structure and visual style of the main scheduler's export.

    Sheets:
        1. Schedule by Day
        2. Schedule by Faculty
        3. Faculty Load Summary
        4. Unscheduled Classes  (only if there are any)
    """
    wb = Workbook()
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    # ── Shared styles ──────────────────────────────────────────
    h_fill   = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    h_font   = Font(bold=True, color="FFFFFF", size=12)
    u_fill   = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
    border   = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin'),
    )
    c_align  = Alignment(horizontal='center', vertical='center', wrap_text=True)
    mode_tag = "Masteral" if mode == "masteral" else "Special Program"

    def _header(ws, cols):
        ws.append(cols)
        for col_idx, _ in enumerate(cols, 1):
            c = ws.cell(1, col_idx)
            c.font = h_font; c.fill = h_fill; c.alignment = c_align; c.border = border

    def _sort_day(day_str):
        try:
            return _WEEKEND_DAYS_ORDER.index(day_str)
        except ValueError:
            return 99

    def _apply_border_rows(ws):
        for row in ws.iter_rows(min_row=2, max_row=ws.max_row):
            for cell in row:
                cell.border = border

    # ── Sheet 1: Schedule by Day ───────────────────────────────
    ws1 = wb.create_sheet(f"{mode_tag} — By Day")
    cols1 = [
        "Day", "Time", "Course Code", "Type", "Faculty", "Employment Type",
        "Schedule Type", "Room", "Room Type", "Capacity", "Class Size",
        "Program Code", "Program ID", "Institute ID", "Class ID",
    ]
    _header(ws1, cols1)

    for entry in sorted(schedule, key=lambda x: (_sort_day(x["day"]), x["start_hour"])):
        fid = entry.get("faculty_id")
        emp = faculty_loads.get(fid, {}).get("employment_type", "full time")
        ws1.append([
            entry["day"], entry["time_slot"], entry["course_code"], entry["type"],
            entry["faculty_name"], emp.title(),
            entry.get("schedule_type", "face to face").title(),
            entry["room_name"], entry["room_type"],
            entry["room_capacity"], entry["class_size"],
            entry.get("program_code", ""), entry["program_id"],
            entry["institute_id"], entry["class_id"],
        ])

    _apply_border_rows(ws1)

    # Colour-code Schedule Type column (col 7)
    for row in ws1.iter_rows(min_row=2, max_row=ws1.max_row):
        stype_cell = row[6]
        if str(stype_cell.value).lower() == "face to face":
            stype_cell.fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")
            stype_cell.font = Font(bold=True, color="FFFFFF")

    # Colour-code Employment Type column (col 6)
    for row in ws1.iter_rows(min_row=2, max_row=ws1.max_row):
        emp_cell = row[5]
        if str(emp_cell.value).lower() == "full time":
            emp_cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            emp_cell.font = Font(bold=True, color="FFFFFF")
        else:
            emp_cell.fill = PatternFill(start_color="ED7D31", end_color="ED7D31", fill_type="solid")
            emp_cell.font = Font(bold=True, color="FFFFFF")

    for col in range(1, len(cols1) + 1):
        ws1.column_dimensions[get_column_letter(col)].width = 15
    ws1.column_dimensions['B'].width = 22  # Time
    ws1.column_dimensions['E'].width = 27  # Faculty
    ws1.column_dimensions['F'].width = 18  # Employment Type

    # ── Sheet 2: Schedule by Faculty ──────────────────────────
    ws2 = wb.create_sheet(f"{mode_tag} — By Faculty")
    cols2 = [
        "Faculty Name", "Faculty ID", "Employment Type", "Day", "Time",
        "Course Code", "Type", "Room", "Hours", "Class ID", "Program Code",
    ]
    _header(ws2, cols2)

    for entry in sorted(
            schedule,
            key=lambda x: (x["faculty_name"], _sort_day(x["day"]), x["start_hour"])):
        fid = entry.get("faculty_id")
        emp = faculty_loads.get(fid, {}).get("employment_type", "full time")
        ws2.append([
            entry["faculty_name"], fid, emp.title(),
            entry["day"], entry["time_slot"], entry["course_code"],
            entry["type"], entry["room_name"], entry["duration"],
            entry["class_id"], entry.get("program_code", ""),
        ])

    _apply_border_rows(ws2)
    for row in ws2.iter_rows(min_row=2, max_row=ws2.max_row):
        emp_cell = row[2]
        if str(emp_cell.value).lower() == "full time":
            emp_cell.fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            emp_cell.font = Font(bold=True, color="FFFFFF")
        else:
            emp_cell.fill = PatternFill(start_color="ED7D31", end_color="ED7D31", fill_type="solid")
            emp_cell.font = Font(bold=True, color="FFFFFF")

    ws2.column_dimensions['A'].width = 27
    ws2.column_dimensions['C'].width = 18
    ws2.column_dimensions['E'].width = 22

    # ── Sheet 3: Faculty Load Summary ─────────────────────────
    ws3 = wb.create_sheet("Faculty Load Summary")
    cols3 = [
        "Faculty Name", "Faculty ID", "Employment Type",
        "Max Load", "Total Courses", "Total Units", "Load Status",
    ]
    _header(ws3, cols3)

    for fid, info in sorted(faculty_loads.items(), key=lambda x: x[1]["faculty_name"]):
        emp        = info.get("employment_type", "full time")
        load_unit  = info.get("load_unit", MAX_LOAD)
        total_u    = info["total_units"]
        status     = "FULL" if total_u >= load_unit else ("PARTIAL" if total_u > 0 else "NONE")
        ws3.append([
            info["faculty_name"], fid, emp.title(),
            load_unit, len(info["assigned_classes"]), round(total_u, 2), status,
        ])

    _apply_border_rows(ws3)
    _STATUS_COLORS = {
        "FULL":    ("00B050", "FFFFFF"),
        "PARTIAL": ("FFC000", "000000"),
        "NONE":    ("FF0000", "FFFFFF"),
    }
    for row in ws3.iter_rows(min_row=2, max_row=ws3.max_row):
        sc = row[6]
        fg, fc = _STATUS_COLORS.get(str(sc.value), ("FFFFFF", "000000"))
        sc.fill = PatternFill(start_color=fg, end_color=fg, fill_type="solid")
        sc.font = Font(bold=True, color=fc)
        for cell in row:
            cell.border = border

    ws3.column_dimensions['A'].width = 27
    ws3.column_dimensions['C'].width = 18

    # ── Sheet 4: Unscheduled Classes ──────────────────────────
    if unscheduled:
        ws4 = wb.create_sheet("Unscheduled Classes")
        cols4 = [
            "Course Code", "Type", "Hours", "Class ID",
            "Faculty", "Program Code", "Reason",
        ]
        ws4.append(cols4)
        for col_idx, _ in enumerate(cols4, 1):
            c = ws4.cell(1, col_idx)
            c.font = h_font; c.fill = u_fill; c.alignment = c_align; c.border = border

        for entry in unscheduled:
            ws4.append([
                entry["course_code"], entry["type"], entry["hours"],
                entry["class_id"], entry.get("faculty_name", "Unknown"),
                entry.get("program_code", "Unknown"), entry["reason"],
            ])
        _apply_border_rows(ws4)
        ws4.column_dimensions['A'].width = 15
        ws4.column_dimensions['G'].width = 45

    wb.save(filename)
    print(f"[INFO] Excel saved to: {filename}")


# ==============================================================
# MAIN
# ==============================================================

if __name__ == "__main__":

    # Run mode: "masteral" (default) or "special"
    run_mode = sys.argv[1].lower() if len(sys.argv) > 1 else "masteral"
    if run_mode not in ("masteral", "special"):
        print(f"[ERROR] Unknown mode '{run_mode}'. Use:  masteral | special")
        sys.exit(1)

    print(f"[INFO] Weekend Scheduler starting — mode: {run_mode}")

    # ----------------------------------------------------------
    # LOAD DATA FROM SAMPLE FILE  (no DB connection needed)
    # ----------------------------------------------------------
    # Switch the imports below to the correct set for each mode.
    # When connected to a live DB, comment this whole block out and
    # uncomment the "LOAD DATA FROM DATABASE" block further below.

    # from sample_weekend_data import (
    #     SAMPLE_MASTERAL_CLASSES,
    #     SAMPLE_MASTERAL_FACULTY,
    #     SAMPLE_SPECIAL_CLASSES,
    #     SAMPLE_SPECIAL_FACULTY,
    #     SAMPLE_WEEKEND_ROOMS,
    #     SAMPLE_BRANCH_MAP,
    # )

    # if run_mode == "masteral":
    #     classes_course    = SAMPLE_MASTERAL_CLASSES
    #     faculty_expertise = SAMPLE_MASTERAL_FACULTY
    # else:
    #     classes_course    = SAMPLE_SPECIAL_CLASSES
    #     faculty_expertise = SAMPLE_SPECIAL_FACULTY

    # rooms      = SAMPLE_WEEKEND_ROOMS
    # branch_map = SAMPLE_BRANCH_MAP

    # Sample data already has program_code and class_size embedded in every
    # class dict, so no lookup enrichment step is needed here.

    # ----------------------------------------------------------
    # LOAD DATA FROM DATABASE  (uncomment when using a live DB)
    # ----------------------------------------------------------
    # Tables / views shared with the main scheduler
    classes_course_table    = Table("classes_course",           metadata, autoload_with=engine)
    rooms_table             = Table("rooms_view",               metadata, autoload_with=engine)
    programs_table          = Table("programs",                 metadata, autoload_with=engine)
    classes_table           = Table("classes",                  metadata, autoload_with=engine)
    college_branch_table    = Table("college_branch",           metadata, autoload_with=engine)
    
    Faculty expertise view — replace the table name to match your schema:
      "faculty_expertise_courses_masteral"  for Masteral
      "faculty_expertise_courses_special"   for Special Program
    faculty_expertise_table = Table("faculty_expertise_courses", metadata, autoload_with=engine)
    
    classes_course    = fetch_table_data(classes_course_table)
    faculty_expertise = fetch_table_data(faculty_expertise_table)
    rooms             = fetch_table_data(rooms_table)
    programs          = fetch_table_data(programs_table)
    classes           = fetch_table_data(classes_table)
    college_branches  = fetch_table_data(college_branch_table)
    
    # Build lookup maps
    program_map    = {p["program_id"]:        p["program_code"]        for p in programs}
    branch_map     = {b["college_branch_id"]: b["college_branch_name"] for b in college_branches}
    class_size_map = {c["class_id"]:          c["class_size"]          for c in classes}
    
    # Enrich classes_course with program_code and class_size
    for cls in classes_course:
        cls["program_code"] = program_map.get(cls.get("program_id"), "Unknown")
        cls["class_size"]   = class_size_map.get(cls.get("class_id"), 0)
    
    # Filter by program type — adjust to match your DB schema:
    # if run_mode == "masteral":
    #     classes_course = [c for c in classes_course if c.get("course_level", 0) >= 5]
    # elif run_mode == "special":
    #     classes_course = [c for c in classes_course
    #                       if str(c.get("program_name", "")).lower().startswith("special")]

    # ----------------------------------------------------------
    # ASSIGN FACULTY TO CLASSES
    # ----------------------------------------------------------
    faculty_loads, unassigned = assign_faculty(classes_course, faculty_expertise)

    if unassigned:
        print(f"[WARNING] {len(unassigned)} course(s) had no matching faculty.")

    # ----------------------------------------------------------
    # CREATE WEEKEND SCHEDULE
    # ----------------------------------------------------------
    complete_schedule, unscheduled_meetings = create_weekend_schedule(
        faculty_loads, rooms, mode=run_mode, branch_map=branch_map,
    )

    # Append unassigned courses to the unscheduled list
    for course in unassigned:
        bid   = course.get("branch_id")
        bname = branch_map.get(bid, f"Branch {bid}") if bid else "Main"
        unscheduled_meetings.append({
            "class_id":     course.get("class_id"),
            "course_code":  course.get("course_code", "Unknown"),
            "course_id":    course.get("course_id"),
            "institute_id": course.get("institute_id"),
            "class_size":   course.get("class_size", 0),
            "faculty_name": "Unassigned",
            "program_id":   course.get("program_id"),
            "program_name": course.get("program_name", "Unknown"),
            "program_code": course.get("program_code", "Unknown"),
            "type":         "Lecture",
            "hours":        f"{course.get('course_lec', 0)}h lec",
            "reason":       f"No qualified faculty — {bname}",
        })

    # ----------------------------------------------------------
    # SAVE OUTPUTS
    # ----------------------------------------------------------
    output_dir = "faculty_loading_output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    excel_file = os.path.join(
        output_dir, f"weekend_schedule_{run_mode}_{timestamp}.xlsx"
    )
    save_weekend_schedule_to_excel(
        complete_schedule, unscheduled_meetings,
        faculty_loads, excel_file, run_mode,
    )

    json_dir = os.path.join(
        "..", "backend", "src", "generated_scheduled", "json_output"
    )
    os.makedirs(json_dir, exist_ok=True)
    json_file = os.path.join(json_dir, f"weekend_schedule_{run_mode}.json")

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "metadata": {
                    "generated_at":      datetime.now().isoformat(),
                    "mode":              run_mode,
                    "total_scheduled":   len(complete_schedule),
                    "total_unscheduled": len(unscheduled_meetings),
                    "start_hour":        WEEKEND_START_HOUR,
                    "end_hour":          WEEKEND_END_HOUR,
                    "block_duration":    WEEKEND_FULL_DAY_DURATION,
                    "days":              WEEKEND_DAYS_MASTERAL if run_mode == "masteral"
                                         else WEEKEND_DAYS_SPECIAL,
                },
                "scheduled_meetings":   complete_schedule,
                "unscheduled_meetings": unscheduled_meetings,
            },
            f, indent=2, ensure_ascii=False, default=str,
        )
    print(f"[INFO] JSON saved to: {json_file}")

    # Final output for NestJS / API consumption
    print(json.dumps(
        {
            "scheduled_meetings":   complete_schedule,
            "unscheduled_meetings": unscheduled_meetings,
        },
        indent=2, default=str,
    ))
