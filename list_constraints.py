"""
list_constraints.py — Generates Scheduling_Constraints.xlsx: a plain two-column
reference list of every scheduling constraint (Column A = constraint name,
Column B = its description/detail).

Same 32 constraints documented as CON-01..CON-32 in add_constraints.py (which
targets QA_TestCases_FacultyLoader.xlsx with full test-case steps/expected
results) — this is a lighter-weight, standalone reference version of the same
list, grouped by category, for quick reading instead of QA test authoring.

Run:  python list_constraints.py
"""

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

PATH = r"C:\Users\JiMkErR\Documents\DNSCSYSTEM\GA-faculty-scheduler\GA-Faculty-Loading-Final\Faculty-Loading-and-Exam-Schedulers\Scheduling_Constraints.xlsx"

thin = Side(style="thin", color="AAAAAA")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

HEADER_HEX = "722F37"
GROUP_HEX = "F2DCDB"
ROW_EVEN = "FDF2F0"
N = 2  # Column A: Constraint, Column B: Description/Detail


def fill(hex_color):
    return PatternFill("solid", fgColor=hex_color)


def header_row(ws):
    ws.append(["Constraint", "Description / Detail"])
    for c in ws[1]:
        c.font = Font(bold=True, name="Calibri", size=11, color="FFFFFF")
        c.fill = fill(HEADER_HEX)
        c.alignment = Alignment(horizontal="left", vertical="center")
        c.border = border
    ws.row_dimensions[1].height = 22


def group_row(ws, label):
    ws.append([label, ""])
    r = ws.max_row
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=N)
    c = ws.cell(r, 1)
    c.font = Font(bold=True, name="Calibri", size=10)
    c.fill = fill(GROUP_HEX)
    c.alignment = Alignment(horizontal="left", vertical="center")
    c.border = border
    ws.row_dimensions[r].height = 18


def data_row(ws, constraint_id, name, description, even):
    ws.append([f"{constraint_id}: {name}", description])
    r = ws.max_row
    bg = ROW_EVEN if even else "FFFFFF"
    for i in range(1, N + 1):
        c = ws.cell(r, i)
        c.fill = fill(bg)
        c.font = Font(name="Calibri", size=10)
        c.alignment = Alignment(vertical="top", wrap_text=True)
        c.border = border
    ws.row_dimensions[r].height = 45


# ---------------------------------------------------------------------------
# Same 32 constraints as add_constraints.py (CON-01..CON-32), reduced to just
# (id, name, description). "Description" here = what the rule actually
# requires (the constraint's own definition), not QA test steps.
# ---------------------------------------------------------------------------
data = [
    ("Hard Constraint - No Overlap", [
        ("CON-01", "No faculty schedule overlap",
         "A faculty member must never be teaching two classes at the same time on the same day."),
        ("CON-02", "No room double-booking",
         "A room must never host two classes at overlapping times on the same day."),
        ("CON-03", "No class section overlap",
         "A single class section must never have two courses running at the same time on the same day."),
    ]),
    ("Hard Constraint - Lunch Break", [
        ("CON-04", "No class scheduled during lunch break (12:00 PM - 1:00 PM)",
         "No class may start or overlap with the 12:00 PM-1:00 PM window; the scheduler skips this hour entirely."),
    ]),
    ("Hard Constraint - Part-Time Faculty Hours", [
        ("CON-05", "Part-time faculty cannot teach before 5:00 PM",
         "All classes assigned to a part-time faculty must start at 5:00 PM (17:00) or later."),
        ("CON-06", "Part-time faculty cannot teach beyond 10:00 PM",
         "No class assigned to a part-time faculty may extend past 10:00 PM (22:00)."),
    ]),
    ("Hard Constraint - Room Capacity", [
        ("CON-07", "Room capacity exceeded beyond 5-student tolerance is rejected",
         "A class may not be assigned to a room if the class size exceeds the room's capacity by more than 5 students."),
        ("CON-08", "Room capacity within 5-student tolerance is accepted",
         "A class may be assigned to a room if it exceeds capacity by 5 students or fewer."),
    ]),
    ("Hard Constraint - Faculty Expertise", [
        ("CON-09", "Faculty can only be assigned courses matching their expertise",
         "A course may only be assigned to a faculty member who has a matching expertise entry for it."),
        ("CON-10", "Unassigned course logged when no qualified faculty exists",
         "A course with no qualified faculty appears in the unscheduled-meetings output with that reason stated."),
    ]),
    ("Hard Constraint - Faculty Unit Load", [
        ("CON-11", "Faculty unit load must not be exceeded",
         "A faculty member may never be assigned courses totaling more than their declared load_unit ceiling."),
        ("CON-12", "Full-time faculty weekly hours capped at 40 hours",
         "A full-time faculty member's total scheduled hours across the week must not exceed 40 hours."),
    ]),
    ("Hard Constraint - Daily Span", [
        ("CON-13", "Faculty daily teaching span must not exceed 9 hours",
         "The gap from a faculty's first class start to their last class end on any day must not exceed 9 hours."),
        ("CON-14", "Faculty daily teaching span should meet minimum of 6 hours",
         "When multiple classes fall on the same day, the span from first to last class should be at least 6 hours."),
    ]),
    ("Hard Constraint - Branch Rules", [
        ("CON-15", "Faculty can teach at Main branch plus at most one other branch per week",
         "Across the whole week, a faculty may only be scheduled at Main plus one non-Main branch, never two or more non-Main branches."),
        ("CON-16", "Far branch forces full-day assignment with no branch mixing",
         "If a branch's one-way travel time exceeds 4 hours (round trip > 480 min), the faculty's entire day must stay at that branch — no mixing with other branches."),
        ("CON-17", "Samal branch: full-day face-to-face with online Main fill for vacant slots",
         "All Samal (branch ID 5) classes must be face-to-face; any vacant time that day may only be filled with online Main-branch classes."),
        ("CON-18", "DAPECOL branch: whole-day face-to-face with no online mode allowed",
         "All DAPECOL (branch ID 6) classes must be face-to-face; online mode is never used for DAPECOL."),
    ]),
    ("Soft Constraint - Preferred Time", [
        ("CON-19", "Faculty preferred teaching time should be respected",
         "Classes should be placed within a faculty's declared preferred time window whenever possible."),
        ("CON-20", "Faculty with no preferred time receives default scheduling",
         "A faculty with no preferred time set is scheduled using the default AM/PM-balanced logic without error."),
    ]),
    ("Soft Constraint - Face-to-Face Ratio", [
        ("CON-21", "At least 70% of lecture hours must be scheduled as face-to-face",
         "Across all scheduled lecture contact hours, at least 70% should be face-to-face; lab hours are always face-to-face and are excluded from this ratio."),
    ]),
    ("Soft Constraint - Back-to-Back Scheduling", [
        ("CON-22", "Classes within the same day should be consecutive with no large idle gaps",
         "A faculty's classes on the same day should be back-to-back or have minimal gaps, avoiding long idle periods."),
    ]),
    ("Soft Constraint - Travel Time Between Buildings", [
        ("CON-23", "Adequate travel time gap required between rooms in different buildings",
         "Between two consecutive classes in different buildings, the scheduler must leave a gap at least as long as the travel time between them."),
    ]),
    ("Special Rule - IAAS Institute", [
        ("CON-24", "IAAS institute lab and lecture rooms are interchangeable",
         "For IAAS (institute ID 63) courses, either a lecture room or a lab room may be assigned regardless of the course's declared type."),
    ]),
    ("Hard Constraint - Faculty Prep Limit", [
        ("CON-25", "Faculty capped at 4 distinct course preps (PREP_LIMIT)",
         "A faculty member may never be assigned more than 4 distinct course codes (preps) in total, even with spare load capacity remaining."),
    ]),
    ("Hard Constraint - Course Code Matching", [
        ("CON-26", "Duplicate/misspelled course codes are matched via normalization",
         "Course codes are normalized (whitespace stripped, uppercased) before matching expertise to classes, so spelling/whitespace variants of the same code (e.g. 'ENG 111' vs 'ENG111') are still recognized as a match."),
    ]),
    ("Special Rule - Cross-Program Assignment", [
        ("CON-27", "Cross-program overflow for shared GenEd-type course codes",
         "A section with no faculty registered under its own program_id may be assigned to a faculty registered for the same course_code under a DIFFERENT program, but only after native-program assignment and the exhaustion pass fail, and only within that faculty's load cap and prep limit."),
    ]),
    ("Special Rule - Saturation Assignment Order", [
        ("CON-28", "One faculty absorbs all sections of a course before overflow",
         "For a given course code, the least-loaded qualified faculty receives ALL its sections up to their load cap before any sections overflow to the next qualified faculty — sections are not split evenly by default."),
        ("CON-29", "Branch-expertise faculty get priority for non-Main branch courses",
         "For a non-Main-branch course, a faculty who has that branch listed in their own branch-expertise field is assigned before other qualified faculty, regardless of current load."),
    ]),
    ("Soft Constraint - Repair Pass (Relaxation Tiers)", [
        ("CON-30", "Unscheduled classes are retried under progressively relaxed SOFT constraints only",
         "Classes that fail initial scheduling are retried through tiers that relax preferred-time, then daily-span, then the daily-hour cap — in that order — while hard constraints (double-booking, capacity, etc.) are never relaxed."),
        ("CON-31", "Lecture+Lab decouples to independent days/times as a last resort",
         "If a Lecture+Lab class cannot fit as one consecutive block under any tier, the final repair tier may schedule the lecture and lab on different days/times (lecture may go online); this is rolled back entirely if the lecture still cannot be placed after the lab is booked."),
    ]),
    ("Special Rule - DAPECOL Branch", [
        ("CON-32", "All DAPECOL programs share the same fixed 2-day f2f/online pair",
         "Every DAPECOL class across every program uses the identical 2-day pattern (same face-to-face day, same paired online day) — the pair is fixed once per run for the whole branch, not chosen per program or per faculty."),
    ]),
]

wb = Workbook()
ws = wb.active
ws.title = "Constraints"
header_row(ws)

even = False
for grp, rows in data:
    group_row(ws, grp)
    for constraint_id, name, description in rows:
        data_row(ws, constraint_id, name, description, even)
        even = not even

ws.column_dimensions[get_column_letter(1)].width = 45
ws.column_dimensions[get_column_letter(2)].width = 90
ws.freeze_panes = "A2"

wb.save(PATH)
print("Saved:", PATH)
