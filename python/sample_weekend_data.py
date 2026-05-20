"""
Sample Input Data — Weekend Scheduler (Masteral & Special Program / DNLI)

Designed to test faculty_loading_for_materal_and_dnli.py without a DB connection.

Usage in the main script:
    from sample_weekend_data import (
        SAMPLE_MASTERAL_CLASSES,
        SAMPLE_MASTERAL_FACULTY,
        SAMPLE_SPECIAL_CLASSES,
        SAMPLE_SPECIAL_FACULTY,
        SAMPLE_WEEKEND_ROOMS,
        SAMPLE_BRANCH_MAP,
    )

Expected scheduling outcomes
─────────────────────────────────────────────────────────────────────────────
MASTERAL MODE  (Saturday only)
  Dr. Ana Reyes      → 2 classes assigned  → 1 scheduled (Sat), 1 UNSCHEDULED
  Dr. Ben Santos     → 2 classes assigned  → 1 scheduled (Sat), 1 UNSCHEDULED
  Prof. Carlo Dela Cruz → 2 classes assigned → 1 scheduled (Sat), 1 UNSCHEDULED
  Total: 3 scheduled · 3 unscheduled
  Demonstrates: one-class-per-Saturday rule

SPECIAL PROGRAM MODE  (Saturday or Sunday)
  Dr. Elena Reyes   → 2 classes → Sat + Sun  (BOTH scheduled)
  Dr. Felix Santos  → 3 classes → Sat + Sun + FAIL (1 unscheduled)
  Dr. Gloria Mendoza→ 2 classes → Sat + Sun  (BOTH scheduled)
  Prof. Hector Cruz → 1 class  → Sat         (scheduled)
  Total: 7 scheduled · 1 unscheduled
  Demonstrates: Sat-first then Sun fallback, and both-days-full failure
─────────────────────────────────────────────────────────────────────────────
"""


# ============================================================================
# BRANCH MAP
# ============================================================================

SAMPLE_BRANCH_MAP = {
    1: "Main Campus",
}


# ============================================================================
# ROOMS  (shared by both masteral and special program modes)
# ============================================================================
# • All rooms are at Main Campus (branch_id=1), Graduate School Building.
# • Lecture rooms only — weekend classes are face-to-face full-day blocks.
# • building_name and time_travel are required by check_travel_time_compatible().
# • Capacities cover class sizes up to 30 (MAX_CAPACITY_EXCESS=5 allows +5 over).

SAMPLE_WEEKEND_ROOMS = [
    {
        "room_id": 1,
        "room_name": "GSB-LR101",
        "room_type": "Lecture",
        "room_capacity": 30,
        "institute_id": 1,
        "branch_id": 1,
        "building_name": "Graduate School Building",
        "time_travel": 0,
    },
    {
        "room_id": 2,
        "room_name": "GSB-LR102",
        "room_type": "Lecture",
        "room_capacity": 30,
        "institute_id": 1,
        "branch_id": 1,
        "building_name": "Graduate School Building",
        "time_travel": 0,
    },
    {
        "room_id": 3,
        "room_name": "GSB-LR103",
        "room_type": "Lecture",
        "room_capacity": 35,
        "institute_id": 1,
        "branch_id": 1,
        "building_name": "Graduate School Building",
        "time_travel": 0,
    },
    {
        "room_id": 4,
        "room_name": "GSB-LR201",
        "room_type": "Lecture",
        "room_capacity": 25,
        "institute_id": 1,
        "branch_id": 1,
        "building_name": "Graduate School Building",
        "time_travel": 0,
    },
    {
        "room_id": 5,
        "room_name": "GSB-LR202",
        "room_type": "Lecture",
        "room_capacity": 25,
        "institute_id": 1,
        "branch_id": 1,
        "building_name": "Graduate School Building",
        "time_travel": 0,
    },
]


# ============================================================================
# MASTERAL SAMPLE DATA
# ============================================================================
# Programs
#   101 → MBM  (Master in Business Management)
#   102 → MPA  (Master in Public Administration)
#
# All masteral courses:
#   • Lecture-only (course_lab=0)
#   • 3 lecture units each  →  3.0 teacher units via compute_load()
#   • Graduate level, small class sizes (12–20 students)
#   • Main Campus (branch_id=1)
#   • Fields pre-enriched so no DB lookup is needed:
#     program_code, program_name, class_size all embedded in each dict

SAMPLE_MASTERAL_CLASSES = [

    # ── MBM Program ───────────────────────────────────────────────────────────
    {
        "class_id": 201, "course_code": "MBA501", "set_name": "MBA501-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Graduate",
        "program_id": 101, "program_code": "MBM",
        "program_name": "Master in Business Management",
        "institute_id": 1, "class_size": 15, "branch_id": 1, "course_id": 501,
    },
    {
        "class_id": 202, "course_code": "MBA502", "set_name": "MBA502-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Graduate",
        "program_id": 101, "program_code": "MBM",
        "program_name": "Master in Business Management",
        "institute_id": 1, "class_size": 18, "branch_id": 1, "course_id": 502,
    },
    {
        "class_id": 203, "course_code": "MBA503", "set_name": "MBA503-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Graduate",
        "program_id": 101, "program_code": "MBM",
        "program_name": "Master in Business Management",
        "institute_id": 1, "class_size": 12, "branch_id": 1, "course_id": 503,
    },
    {
        "class_id": 204, "course_code": "MBA504", "set_name": "MBA504-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Graduate",
        "program_id": 101, "program_code": "MBM",
        "program_name": "Master in Business Management",
        "institute_id": 1, "class_size": 20, "branch_id": 1, "course_id": 504,
    },

    # ── MPA Program ───────────────────────────────────────────────────────────
    {
        "class_id": 205, "course_code": "MPA501", "set_name": "MPA501-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Graduate",
        "program_id": 102, "program_code": "MPA",
        "program_name": "Master in Public Administration",
        "institute_id": 1, "class_size": 14, "branch_id": 1, "course_id": 505,
    },
    {
        "class_id": 206, "course_code": "MPA502", "set_name": "MPA502-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Graduate",
        "program_id": 102, "program_code": "MPA",
        "program_name": "Master in Public Administration",
        "institute_id": 1, "class_size": 16, "branch_id": 1, "course_id": 506,
    },
]


# --- Masteral Faculty ---
# load_unit=6 → each faculty can take at most 2 masteral courses (3 units each).
# Each faculty is intentionally assigned 2 classes to trigger the
# one-class-per-Saturday constraint: the second class will be UNSCHEDULED.
#
# Faculty 101  Dr. Ana Reyes       →  MBA501 + MBA502  (both MBM)
# Faculty 102  Dr. Ben Santos      →  MBA503 + MBA504  (both MBM)
# Faculty 103  Prof. Carlo Dela Cruz → MPA501 + MPA502 (both MPA)

SAMPLE_MASTERAL_FACULTY = [

    # Dr. Ana Reyes — teaches MBA501 and MBA502 (MBM)
    {
        "faculty_id": 101, "faculty_name": "Dr. Ana Reyes",
        "course_code": "MBA501", "program_id": 101,
        "employment_type": "full time", "load_unit": 6,
        "preffered_time": None, "branches": None,
    },
    {
        "faculty_id": 101, "faculty_name": "Dr. Ana Reyes",
        "course_code": "MBA502", "program_id": 101,
        "employment_type": "full time", "load_unit": 6,
        "preffered_time": None, "branches": None,
    },

    # Dr. Ben Santos — teaches MBA503 and MBA504 (MBM)
    {
        "faculty_id": 102, "faculty_name": "Dr. Ben Santos",
        "course_code": "MBA503", "program_id": 101,
        "employment_type": "full time", "load_unit": 6,
        "preffered_time": None, "branches": None,
    },
    {
        "faculty_id": 102, "faculty_name": "Dr. Ben Santos",
        "course_code": "MBA504", "program_id": 101,
        "employment_type": "full time", "load_unit": 6,
        "preffered_time": None, "branches": None,
    },

    # Prof. Carlo Dela Cruz — teaches MPA501 and MPA502 (MPA)
    {
        "faculty_id": 103, "faculty_name": "Prof. Carlo Dela Cruz",
        "course_code": "MPA501", "program_id": 102,
        "employment_type": "full time", "load_unit": 6,
        "preffered_time": None, "branches": None,
    },
    {
        "faculty_id": 103, "faculty_name": "Prof. Carlo Dela Cruz",
        "course_code": "MPA502", "program_id": 102,
        "employment_type": "full time", "load_unit": 6,
        "preffered_time": None, "branches": None,
    },
]


# ============================================================================
# SPECIAL PROGRAM (DNLI) SAMPLE DATA
# ============================================================================
# Programs
#   201 → BSBA-SP  (BS Business Administration Special Program)
#   202 → BSIT-SP  (BS Information Technology Special Program)
#
# All special courses:
#   • Lecture-only (course_lab=0)
#   • 3 lecture units each → 3.0 teacher units
#   • Undergraduate year levels (First/Second/Third Year)
#   • Main Campus (branch_id=1)
#   • class sizes 18–28 (within room capacity + MAX_CAPACITY_EXCESS=5 tolerance)

SAMPLE_SPECIAL_CLASSES = [

    # ── BSBA-SP Program ───────────────────────────────────────────────────────
    {
        "class_id": 301, "course_code": "ACCT101", "set_name": "ACCT101-A",
        "course_lec": 3, "course_lab": 0, "course_level": "First Year",
        "program_id": 201, "program_code": "BSBA-SP",
        "program_name": "BS Business Administration Special Program",
        "institute_id": 1, "class_size": 25, "branch_id": 1, "course_id": 601,
    },
    {
        "class_id": 302, "course_code": "BCOM101", "set_name": "BCOM101-A",
        "course_lec": 3, "course_lab": 0, "course_level": "First Year",
        "program_id": 201, "program_code": "BSBA-SP",
        "program_name": "BS Business Administration Special Program",
        "institute_id": 1, "class_size": 28, "branch_id": 1, "course_id": 602,
    },
    {
        "class_id": 303, "course_code": "MGMT101", "set_name": "MGMT101-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Second Year",
        "program_id": 201, "program_code": "BSBA-SP",
        "program_name": "BS Business Administration Special Program",
        "institute_id": 1, "class_size": 22, "branch_id": 1, "course_id": 603,
    },
    {
        "class_id": 304, "course_code": "MKTG101", "set_name": "MKTG101-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Second Year",
        "program_id": 201, "program_code": "BSBA-SP",
        "program_name": "BS Business Administration Special Program",
        "institute_id": 1, "class_size": 20, "branch_id": 1, "course_id": 604,
    },
    {
        "class_id": 305, "course_code": "ENTR101", "set_name": "ENTR101-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Third Year",
        "program_id": 201, "program_code": "BSBA-SP",
        "program_name": "BS Business Administration Special Program",
        "institute_id": 1, "class_size": 18, "branch_id": 1, "course_id": 605,
    },

    # ── BSIT-SP Program ───────────────────────────────────────────────────────
    {
        "class_id": 306, "course_code": "PROG101", "set_name": "PROG101-A",
        "course_lec": 3, "course_lab": 0, "course_level": "First Year",
        "program_id": 202, "program_code": "BSIT-SP",
        "program_name": "BS Information Technology Special Program",
        "institute_id": 1, "class_size": 24, "branch_id": 1, "course_id": 606,
    },
    {
        "class_id": 307, "course_code": "DBASE101", "set_name": "DBASE101-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Second Year",
        "program_id": 202, "program_code": "BSIT-SP",
        "program_name": "BS Information Technology Special Program",
        "institute_id": 1, "class_size": 22, "branch_id": 1, "course_id": 607,
    },
    {
        "class_id": 308, "course_code": "NETW101", "set_name": "NETW101-A",
        "course_lec": 3, "course_lab": 0, "course_level": "Second Year",
        "program_id": 202, "program_code": "BSIT-SP",
        "program_name": "BS Information Technology Special Program",
        "institute_id": 1, "class_size": 26, "branch_id": 1, "course_id": 608,
    },
]


# --- Special Program Faculty ---
# Scenario breakdown:
#
#   Faculty 201  Dr. Elena Reyes    (load=6, 2 classes)
#     ACCT101-A → Saturday ✓
#     BCOM101-A → Sunday  ✓  (Sat already taken → falls back to Sunday)
#     Expected: BOTH scheduled
#
#   Faculty 202  Dr. Felix Santos   (load=9, 3 classes)
#     MGMT101-A → Saturday ✓
#     MKTG101-A → Sunday  ✓
#     ENTR101-A → UNSCHEDULED  (Sat+Sun both taken for this faculty)
#     Expected: 2 scheduled, 1 unscheduled
#
#   Faculty 203  Dr. Gloria Mendoza (load=6, 2 classes)
#     PROG101-A  → Saturday ✓
#     DBASE101-A → Sunday  ✓
#     Expected: BOTH scheduled
#
#   Faculty 204  Prof. Hector Cruz  (load=3, 1 class)
#     NETW101-A  → Saturday ✓
#     Expected: scheduled

SAMPLE_SPECIAL_FACULTY = [

    # Dr. Elena Reyes — BSBA-SP (Sat+Sun scenario)
    {
        "faculty_id": 201, "faculty_name": "Dr. Elena Reyes",
        "course_code": "ACCT101", "program_id": 201,
        "employment_type": "full time", "load_unit": 6,
        "preffered_time": None, "branches": None,
    },
    {
        "faculty_id": 201, "faculty_name": "Dr. Elena Reyes",
        "course_code": "BCOM101", "program_id": 201,
        "employment_type": "full time", "load_unit": 6,
        "preffered_time": None, "branches": None,
    },

    # Dr. Felix Santos — BSBA-SP (Sat+Sun+fail scenario)
    {
        "faculty_id": 202, "faculty_name": "Dr. Felix Santos",
        "course_code": "MGMT101", "program_id": 201,
        "employment_type": "full time", "load_unit": 9,
        "preffered_time": None, "branches": None,
    },
    {
        "faculty_id": 202, "faculty_name": "Dr. Felix Santos",
        "course_code": "MKTG101", "program_id": 201,
        "employment_type": "full time", "load_unit": 9,
        "preffered_time": None, "branches": None,
    },
    {
        "faculty_id": 202, "faculty_name": "Dr. Felix Santos",
        "course_code": "ENTR101", "program_id": 201,
        "employment_type": "full time", "load_unit": 9,
        "preffered_time": None, "branches": None,
    },

    # Dr. Gloria Mendoza — BSIT-SP (Sat+Sun scenario)
    {
        "faculty_id": 203, "faculty_name": "Dr. Gloria Mendoza",
        "course_code": "PROG101", "program_id": 202,
        "employment_type": "full time", "load_unit": 6,
        "preffered_time": None, "branches": None,
    },
    {
        "faculty_id": 203, "faculty_name": "Dr. Gloria Mendoza",
        "course_code": "DBASE101", "program_id": 202,
        "employment_type": "full time", "load_unit": 6,
        "preffered_time": None, "branches": None,
    },

    # Prof. Hector Cruz — BSIT-SP (single class scenario)
    {
        "faculty_id": 204, "faculty_name": "Prof. Hector Cruz",
        "course_code": "NETW101", "program_id": 202,
        "employment_type": "full time", "load_unit": 3,
        "preffered_time": None, "branches": None,
    },
]


# ============================================================================
# DATA SUMMARY
# ============================================================================
"""
ROOMS (shared)
  5 Lecture rooms in Graduate School Building, Main Campus
  Capacities: 25, 25, 30, 30, 35
  (All cover masteral class sizes of 12–20 and special class sizes of 18–28)

MASTERAL DATA
  Programs  : MBM (101), MPA (102)
  Classes   : 6 total — MBA501-A, MBA502-A, MBA503-A, MBA504-A, MPA501-A, MPA502-A
  Faculty   : 3 — each assigned 2 classes (load_unit=6)
  Rule tested: One class per faculty per Saturday
  Expected  : 3 scheduled (one per faculty), 3 unscheduled

SPECIAL PROGRAM (DNLI) DATA
  Programs  : BSBA-SP (201), BSIT-SP (202)
  Classes   : 8 total — ACCT101-A, BCOM101-A, MGMT101-A, MKTG101-A, ENTR101-A,
                         PROG101-A, DBASE101-A, NETW101-A
  Faculty   : 4
    Faculty 201 (load=6, 2 classes)  → Sat+Sun  → 2 scheduled
    Faculty 202 (load=9, 3 classes)  → Sat+Sun+fail → 2 scheduled, 1 unscheduled
    Faculty 203 (load=6, 2 classes)  → Sat+Sun  → 2 scheduled
    Faculty 204 (load=3, 1 class)    → Sat      → 1 scheduled
  Expected  : 7 scheduled, 1 unscheduled
"""
