import random
import json
import os
import math
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from copy import deepcopy
from sqlalchemy import create_engine, Table, MetaData, select
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
# =========================
# MySQL Connection (adjust creds/host/db as needed)
# =========================
DB_USER = "root"
DB_PASS = "root"
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "dnsc_class_scheduler_ga_qa"

engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_pre_ping=True,
    echo=False,
)
metadata = MetaData()



# ===========================================================   =
# START CODE FOR SCHEDULING FUNCTIONS
# ============================================================

# ============================================================
# SCHEDULING FUNCTIONS
# ============================================================

# Time slot configuration
# Day patterns for weekly scheduling — add, remove, or reorder entries to change scheduling behavior
DAY_PATTERNS = {
    "TTH": ["Tuesday", "Thursday"],
    "MF": ["Monday", "Friday"],
    "WF": ["Wednesday", "Friday"],
    "MWF": ["Monday", "Wednesday", "Friday"],
}
# Standalone fallback day used when no pattern can accommodate the class
FALLBACK_DAY = "Wednesday"
# All schedulable days — derived automatically from patterns + fallback
DAYS = sorted(
    {day for days in DAY_PATTERNS.values() for day in days} | {FALLBACK_DAY},
    key=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index
)
START_HOUR = 7  # 7 AM
END_HOUR = 21   # 9 PM
PART_TIME_START_HOUR = 17  # 5 PM - Part-time faculty can only teach from 5 PM onwards
# 10 PM - Extended end time for part-time faculty to accommodate evening classes
PART_TIME_END_HOUR = 22
LUNCH_START = 12
LUNCH_END = 13
# AM/PM boundary for balanced scheduling
AFTERNOON_START = 13  # 1 PM — classes at or after this hour count as "afternoon"
MAX_CAPACITY_EXCESS = 5  # Allow up to 5 students over capacity
FULL_TIME_WEEKLY_HOURS = 40  # Full-time faculty weekly presence at school
MAX_DAILY_SPAN_HOURS = 9   # Max hours from first class start to last class end per day
MIN_DAILY_SPAN_HOURS = 6   # Min hours from first class start to last class end per day

# Unit to hour conversion constants (for scheduling contact hours)
LECTURE_UNIT_TO_HOUR = 1.0  # 1 student unit = 1 contact hour
LAB_UNIT_TO_HOUR = 3.0  # 1 student unit = 3 contact hours

# Faculty load calculation constants
# 1 student lec unit = 1 teacher unit
LECTURE_STUDENT_UNIT_TO_TEACHER_UNIT = 1.0
# 1 student lab unit = 3 hours × 0.75 = 2.25 teacher units
LAB_STUDENT_UNIT_TO_TEACHER_UNIT = 2.25

# Target percentage of total lecture HOURS that should be face-to-face
# Laboratory is always face-to-face and does NOT count toward this ratio
TARGET_FACE_TO_FACE_PERCENTAGE = 0.70  # 70% face-to-face

# Percentage of lab+lecture classes that may use different rooms on different pattern days
# (the rest require the same room on every day in the pattern)
DIFFERENT_ROOM_PERCENTAGE = 0.30  # 30% allowed different rooms per day

# Maximum round-trip travel time (in minutes) that still allows mixed-branch scheduling in a day.
# If 2 × time_travel > this threshold, the ENTIRE day must be spent at that branch.
# e.g., 480 min = 8 hours → branches with one-way travel >= 240 min (4h) force a full-day assignment.
FAR_BRANCH_ROUND_TRIP_LIMIT = 480  # minutes

# Main branch ID — faculty can teach at Main + at most 1 other branch across the week
MAIN_BRANCH_ID = 1

# Branch-specific IDs for special scheduling rules
SAMAL_BRANCH_ID = 5       # Samal: full-day f2f, vacant time filled with online Main classes
DAPECOL_BRANCH_ID = 6     # DAPECOL: whole-day f2f, no online, compressed curriculum

# IAAS institute ID — lab and lecture rooms are interchangeable for this institute
IAAS_INSTITUTE_ID = 63


def get_balanced_patterns(day_pattern_tracker, weekly_hours):
    """
    Return day patterns sorted by usage (least used first) with randomization for ties.
    Only includes patterns where weekly_hours / len(pattern_days) >= 1 hour per meeting.
    This ensures fair distribution across TTH, MF, and MWF.

    Args:
        day_pattern_tracker: dict mapping pattern name to usage count, e.g. {"TTH": 3, "MF": 2, "MWF": 1}
        weekly_hours: total weekly contact hours for the class being scheduled

    Returns:
        List of tuples: (pattern_name, pattern_days_list), sorted by least-used first, ties randomized.
    """
    # Filter to valid patterns only (each meeting must be at least 1 hour)
    # 2-hour courses must strictly use 2-day pairs (not MWF or any 3+ day pattern)
    valid_patterns = []
    for pattern_name, pattern_days in DAY_PATTERNS.items():
        hours_per_meeting = weekly_hours / len(pattern_days)
        if hours_per_meeting >= 1.0:
            # 2-hour weekly courses: only allow 2-day pairs
            if weekly_hours == 2.0 and len(pattern_days) > 2:
                continue
            valid_patterns.append((pattern_name, pattern_days))

    # Build count groups for sorting
    patterns_with_counts = [
        (pattern_name, pattern_days, day_pattern_tracker.get(pattern_name, 0))
        for pattern_name, pattern_days in valid_patterns
    ]

    count_groups = {}
    for pattern_name, pattern_days, count in patterns_with_counts:
        if count not in count_groups:
            count_groups[count] = []
        count_groups[count].append((pattern_name, pattern_days))

    # Shuffle within each count group and build result
    result = []
    for count in sorted(count_groups.keys()):
        group = count_groups[count]
        random.shuffle(group)
        result.extend(group)

    return result


def get_randomized_time_slots(available_slots):
    """
    Return time slots in randomized order to spread schedules across different times.
    """
    slots_copy = list(available_slots)
    random.shuffle(slots_copy)
    return slots_copy


def generate_time_slots():
    """
    Generate all available time slots (excluding lunch break 12-1pm).
    Returns list of time slots as tuples (start_hour, end_hour).
    """
    slots = []
    for hour in range(START_HOUR, END_HOUR):
        # Skip lunch hour
        if hour >= LUNCH_START and hour < LUNCH_END:
            continue
        slots.append((hour, hour + 1))
    return slots


def time_to_string(hour):
    """Convert hour (24-hour format) to readable string."""
    if hour == 0:
        return "12:00 AM"
    elif hour < 12:
        return f"{hour}:00 AM"
    elif hour == 12:
        return "12:00 PM"
    else:
        return f"{hour - 12}:00 PM"


def format_time_slot(start_hour, duration):
    """Format time slot as string. Handles fractional hours."""
    end_hour = start_hour + duration

    def time_to_str(hour):
        """Convert hour (can be fractional) to readable string."""
        hour_int = int(hour)
        minutes = int((hour - hour_int) * 60)

        if hour_int == 0:
            time_str = "12"
            am_pm = "AM"
        elif hour_int < 12:
            time_str = str(hour_int)
            am_pm = "AM"
        elif hour_int == 12:
            time_str = "12"
            am_pm = "PM"
        else:
            time_str = str(hour_int - 12)
            am_pm = "PM"

        if minutes > 0:
            time_str += f":{minutes:02d}"
        else:
            time_str += ":00"

        return f"{time_str} {am_pm}"

    return f"{time_to_str(start_hour)} - {time_to_str(end_hour)}"


def check_time_overlap(time1_start, time1_duration, time2_start, time2_duration):
    """Check if two time blocks overlap."""
    time1_end = time1_start + time1_duration
    time2_end = time2_start + time2_duration

    return not (time1_end <= time2_start or time2_end <= time1_start)


def check_lunch_conflict(start_hour, duration):
    """Check if a time block conflicts with lunch break."""
    end_hour = start_hour + duration

    # Check if any part of the block overlaps with lunch (12-1pm)
    if start_hour < LUNCH_END and end_hour > LUNCH_START:
        return True
    return False


def is_valid_time_block(start_hour, duration):
    """Check if a time block is valid (within hours and doesn't cross lunch)."""
    end_hour = start_hour + duration

    # Check if within operating hours
    if start_hour < START_HOUR or end_hour > END_HOUR:
        return False

    # Check if crosses lunch break
    if check_lunch_conflict(start_hour, duration):
        return False

    return True


def find_available_slots(start_hour, end_hour, duration, exclude_lunch=True):
    """
    Find all possible starting times for a block of given duration.
    Returns list of valid start hours.
    """
    valid_slots = []

    for hour in range(start_hour, end_hour):
        if is_valid_time_block(hour, duration):
            valid_slots.append(hour)

    return valid_slots


def is_room_available(room, day, start_hour, duration, schedule_tracker):
    """
    Check if a room is available for the given day and time block.
    """
    room_id = room["room_id"]  # Changed from room["id"]

    if room_id not in schedule_tracker:
        return True

    if day not in schedule_tracker[room_id]:
        return True

    # Check all existing schedules for this room on this day
    for scheduled_block in schedule_tracker[room_id][day]:
        if check_time_overlap(start_hour, duration,
                              scheduled_block["start_hour"],
                              scheduled_block["duration"]):
            return False

    return True


def is_faculty_available(faculty_id, day, start_hour, duration, faculty_schedule_tracker):
    """
    Check if a faculty member is available for the given day and time block.
    """
    if faculty_id not in faculty_schedule_tracker:
        return True

    if day not in faculty_schedule_tracker[faculty_id]:
        return True

    # Check all existing schedules for this faculty on this day
    for scheduled_block in faculty_schedule_tracker[faculty_id][day]:
        if check_time_overlap(start_hour, duration,
                              scheduled_block["start_hour"],
                              scheduled_block["duration"]):
            return False

    return True


def get_faculty_daily_hours(faculty_id, day, faculty_schedule_tracker):
    """
    Calculate total hours already scheduled for a faculty member on a specific day.
    """
    if faculty_id not in faculty_schedule_tracker:
        return 0

    if day not in faculty_schedule_tracker[faculty_id]:
        return 0

    total_hours = 0
    for scheduled_block in faculty_schedule_tracker[faculty_id][day]:
        total_hours += scheduled_block["duration"]

    return total_hours


def get_faculty_daily_span(faculty_id, day, faculty_schedule_tracker):
    """
    Calculate the span (earliest start to latest end) for a faculty on a day.
    Returns (earliest_start, latest_end, span_hours) or (None, None, 0) if no classes.
    """
    if faculty_id not in faculty_schedule_tracker:
        return None, None, 0
    if day not in faculty_schedule_tracker[faculty_id]:
        return None, None, 0
    slots = faculty_schedule_tracker[faculty_id][day]
    if not slots:
        return None, None, 0
    earliest = min(s["start_hour"] for s in slots)
    latest = max(s["start_hour"] + s["duration"] for s in slots)
    return earliest, latest, latest - earliest


def check_daily_span_ok(faculty_id, day, new_start, new_duration, faculty_schedule_tracker):
    """
    Check if adding a new class at (new_start, new_duration) on this day would
    keep the faculty's daily span within MAX_DAILY_SPAN_HOURS.
    """
    earliest, latest, _ = get_faculty_daily_span(faculty_id, day, faculty_schedule_tracker)
    new_end = new_start + new_duration

    if earliest is None:
        # No existing classes — the new class alone can't exceed max span
        return new_duration <= MAX_DAILY_SPAN_HOURS

    # Compute what the span would be with the new class
    combined_earliest = min(earliest, new_start)
    combined_latest = max(latest, new_end)
    combined_span = combined_latest - combined_earliest

    return combined_span <= MAX_DAILY_SPAN_HOURS


def get_faculty_next_start_hour(faculty_id, day, faculty_schedule_tracker, default_start):
    """
    Returns the consecutive next start hour for a faculty on a given day.
    This is the end time of their last scheduled class, or default_start if no classes yet.
    Ensures back-to-back (no gap) scheduling within the day.
    """
    if faculty_id not in faculty_schedule_tracker:
        return default_start
    if day not in faculty_schedule_tracker[faculty_id]:
        return default_start
    slots = faculty_schedule_tracker[faculty_id][day]
    if not slots:
        return default_start
    return math.ceil(max(s["start_hour"] + s["duration"] for s in slots))


def get_faculty_am_pm_hours(faculty_id, days, faculty_schedule_tracker):
    """
    Calculate total AM and PM hours for a faculty across the given days.
    AM = hours where start_hour < AFTERNOON_START (before 1 PM)
    PM = hours where start_hour >= AFTERNOON_START (1 PM or later)
    Returns (am_hours, pm_hours).
    """
    am_hours = 0.0
    pm_hours = 0.0
    if faculty_id not in faculty_schedule_tracker:
        return am_hours, pm_hours
    for day in days:
        if day not in faculty_schedule_tracker[faculty_id]:
            continue
        for block in faculty_schedule_tracker[faculty_id][day]:
            start = block["start_hour"]
            duration = block["duration"]
            if start < AFTERNOON_START:
                # Part or all in AM
                am_part = min(duration, AFTERNOON_START - start)
                pm_part = duration - am_part
                am_hours += am_part
                pm_hours += pm_part
            else:
                pm_hours += duration
    return am_hours, pm_hours


def get_balanced_slots(faculty_id, days, duration, scheduling_start_hour, scheduling_end_hour,
                       faculty_schedule_tracker):
    """
    Return available time slots ordered to balance AM and PM scheduling.
    If the faculty already has more AM hours, prefer PM slots first (and vice versa).
    Within the preferred period, slots are consecutive (back-to-back after last class).
    """
    am_hours, pm_hours = get_faculty_am_pm_hours(faculty_id, days, faculty_schedule_tracker)

    # Determine AM and PM slot ranges
    am_slots = find_available_slots(scheduling_start_hour, LUNCH_START, duration)
    pm_slots = find_available_slots(AFTERNOON_START, scheduling_end_hour, duration)

    # Filter each to only slots that are back-to-back (consecutive) with existing classes
    # For AM: find next available after existing AM classes
    # For PM: find next available after existing PM classes
    def get_consecutive_slots(slots, period_start):
        """Filter slots to start from consecutive point in this period."""
        next_starts = []
        for day in days:
            ns = get_faculty_next_start_hour(faculty_id, day, faculty_schedule_tracker, period_start)
            next_starts.append(ns)
        min_start = max(next_starts)
        return [s for s in slots if s >= min_start]

    am_consecutive = get_consecutive_slots(am_slots, scheduling_start_hour)
    pm_consecutive = get_consecutive_slots(pm_slots, AFTERNOON_START)

    # If no consecutive slots exist in a period, use all available slots in that period
    if not am_consecutive:
        am_consecutive = am_slots
    if not pm_consecutive:
        pm_consecutive = pm_slots

    # Order: prefer the period with fewer hours for balance
    if am_hours <= pm_hours:
        # Prefer AM first, then PM
        return am_consecutive + pm_consecutive
    else:
        # Prefer PM first, then AM
        return pm_consecutive + am_consecutive


def is_class_available(class_id, day, start_hour, duration, class_schedule_tracker):
    """
    Check if a class section is available (not already scheduled) for the given day and time block.
    Prevents the same class_id from being scheduled at overlapping times.
    """
    if class_id not in class_schedule_tracker:
        return True

    if day not in class_schedule_tracker[class_id]:
        return True

    # Check all existing schedules for this class on this day
    for scheduled_block in class_schedule_tracker[class_id][day]:
        if check_time_overlap(start_hour, duration,
                              scheduled_block["start_hour"],
                              scheduled_block["duration"]):
            return False

    return True


def is_branch_available(faculty_id, day, branch_id, faculty_branch_tracker, far_branch_set=None):
    """
    Check if a faculty member can be scheduled at the given branch on a given day.

    Rules:
    1. Multi-branch per day is ALLOWED — a faculty can teach at multiple branches
       on the same day as long as the travel time gap between classes is respected
       (enforced separately by check_travel_time_compatible).
    2. Max 1 non-Main branch per week — across the entire week, a faculty may teach at
       Main (MAIN_BRANCH_ID) plus at most ONE other branch.
    3. Far branches (round-trip > FAR_BRANCH_ROUND_TRIP_LIMIT) force a full-day
       assignment — no mixing with other branches on that day.

    Returns True if the assignment is allowed, False otherwise.
    """
    if branch_id is None:
        return True
    if faculty_id not in faculty_branch_tracker:
        return True
    if far_branch_set is None:
        far_branch_set = set()

    tracker = faculty_branch_tracker[faculty_id]

    # Rule 3: Far branch — entire day must be at that branch only
    # Exception: Samal allows online Main classes on the same day (handled at scheduling level)
    if day in tracker:
        existing_branches = tracker[day]
        # If the new class is at a far branch, check if mixing is allowed
        if branch_id in far_branch_set:
            rules = get_branch_schedule_rules(branch_id)
            for eb in existing_branches:
                if eb != branch_id:
                    # Samal allows Main on same day (online fill)
                    if rules["allow_online_main_fill"] and eb == MAIN_BRANCH_ID:
                        continue
                    return False
        # If the day already has a far branch, only that branch (+ allowed fills) is allowed
        for eb in existing_branches:
            if eb in far_branch_set and eb != branch_id:
                rules = get_branch_schedule_rules(eb)
                if rules["allow_online_main_fill"] and branch_id == MAIN_BRANCH_ID:
                    continue
                return False

    # Rule 2: Max 1 non-Main branch per week
    if branch_id != MAIN_BRANCH_ID:
        for d, assigned_branches in tracker.items():
            for ab in assigned_branches:
                if ab != MAIN_BRANCH_ID and ab != branch_id:
                    # Faculty already has a DIFFERENT non-Main branch
                    return False

    return True


def is_far_branch(rooms, branch_id):
    """
    Check if a branch is a 'far branch' — one where round-trip travel time
    exceeds FAR_BRANCH_ROUND_TRIP_LIMIT, meaning the entire day must be
    dedicated to that branch (no mixing with other branches on the same day).
    """
    if branch_id is None or branch_id == MAIN_BRANCH_ID:
        return False
    for room in rooms:
        if room.get("branch_id") == branch_id:
            travel = room.get("time_travel", 0) or 0
            if travel * 2 > FAR_BRANCH_ROUND_TRIP_LIMIT:
                return True
    return False


def get_branch_travel_time(rooms, branch_id):
    """
    Get the representative travel time (in minutes) for a branch.
    Returns the max time_travel value among rooms in that branch.
    Returns 0 for Main branch or unknown branches.
    """
    if branch_id is None or branch_id == MAIN_BRANCH_ID:
        return 0
    max_travel = 0
    for room in rooms:
        if room.get("branch_id") == branch_id:
            t = room.get("time_travel", 0) or 0
            if t > max_travel:
                max_travel = t
    return max_travel


def update_branch_tracker(faculty_id, days, branch_id, faculty_branch_tracker):
    """
    Record the branch a faculty is assigned to for the given days.
    Each day stores a SET of branches (since multi-branch per day is allowed).
    Skips if branch_id is None.
    """
    if branch_id is None:
        return
    if faculty_id not in faculty_branch_tracker:
        faculty_branch_tracker[faculty_id] = {}
    for day in days:
        if day not in faculty_branch_tracker[faculty_id]:
            faculty_branch_tracker[faculty_id][day] = set()
        faculty_branch_tracker[faculty_id][day].add(branch_id)


def get_branch_schedule_rules(branch_id):
    """
    Return branch-specific scheduling rules as a dict.

    Rules:
    - force_f2f: If True, ALL meetings at this branch must be face-to-face (no online)
    - allow_online_main_fill: If True, online classes from Main can fill vacant slots
      on the same day (used for Samal — faculty stays on-site but can teach Main online)
    - full_day_branch: If True, the faculty stays the whole day at this branch
    """
    if branch_id == SAMAL_BRANCH_ID:
        return {
            "force_f2f": True,
            "allow_online_main_fill": True,
            "full_day_branch": True,
        }
    elif branch_id == DAPECOL_BRANCH_ID:
        # DAPECOL f2f/online is handled by Phase 1 compressed scheduling
        # (2-day pair: 1 day f2f + 1 day online). If a DAPECOL class somehow
        # reaches the normal scheduling path, treat it as standard.
        return {
            "force_f2f": False,
            "allow_online_main_fill": False,
            "full_day_branch": False,
        }
    else:
        return {
            "force_f2f": False,
            "allow_online_main_fill": False,
            "full_day_branch": False,
        }


def get_travel_gap_minutes(building1, travel1, building2, travel2):
    """
    Calculate the travel gap in minutes between two rooms.
    If rooms are in the same building, no travel gap needed.
    Otherwise, the gap = max(travel_time_room1, travel_time_room2).
    """
    if building1 is None or building2 is None:
        return 0
    if building1 == building2:
        return 0
    t1 = travel1 if travel1 else 0
    t2 = travel2 if travel2 else 0
    return max(t1, t2)


def check_travel_time_compatible(faculty_id, day, start_hour, duration,
                                  new_building, new_travel_time,
                                  faculty_schedule_tracker):
    """
    Check if scheduling a new class at (day, start_hour, duration) with
    the given building/travel_time is compatible with the faculty's existing
    schedule on that day, considering travel gaps between buildings.

    Returns True if compatible, False if there is a travel time conflict.
    """
    if faculty_id not in faculty_schedule_tracker:
        return True
    if day not in faculty_schedule_tracker[faculty_id]:
        return True

    new_end = start_hour + duration

    for block in faculty_schedule_tracker[faculty_id][day]:
        existing_start = block["start_hour"]
        existing_end = existing_start + block["duration"]
        existing_building = block.get("building_name")
        existing_travel = block.get("travel_time", 0)

        gap_minutes = get_travel_gap_minutes(
            existing_building, existing_travel,
            new_building, new_travel_time if new_travel_time else 0)

        if gap_minutes == 0:
            continue

        gap_hours = gap_minutes / 60.0

        # Check if the new block is right after the existing block
        # Need gap_hours between existing_end and new start
        if existing_end <= start_hour:
            if start_hour - existing_end < gap_hours:
                return False

        # Check if the new block is right before the existing block
        # Need gap_hours between new end and existing start
        if new_end <= existing_start:
            if existing_start - new_end < gap_hours:
                return False

    return True


def parse_time_to_hour(time_str):
    """
    Convert a time string like '8:00AM' or '1:00PM' to an integer hour.
    Returns None if parsing fails.
    """
    try:
        time_str = time_str.strip().upper()
        if 'AM' in time_str:
            time_str = time_str.replace('AM', '').strip()
            hour = int(time_str.split(':')[0])
            if hour == 12:
                hour = 0
        elif 'PM' in time_str:
            time_str = time_str.replace('PM', '').strip()
            hour = int(time_str.split(':')[0])
            if hour != 12:
                hour += 12
        else:
            hour = int(time_str.split(':')[0])
        return hour
    except Exception:
        return None


def parse_preferred_time(time_str):
    """
    Parse preferred time string into a list of (start_hour, end_hour) tuples.
    Example: "8:00AM - 12:00PM, 1:00PM - 5:00PM" -> [(8, 12), (13, 17)]
    Returns empty list if no preferred time or parsing fails.
    """
    if not time_str:
        return []
    windows = []
    for segment in time_str.split(','):
        segment = segment.strip()
        if ' - ' not in segment:
            continue
        parts = segment.split(' - ')
        if len(parts) != 2:
            continue
        start = parse_time_to_hour(parts[0].strip())
        end = parse_time_to_hour(parts[1].strip())
        if start is not None and end is not None:
            windows.append((start, end))
    return windows


def filter_slots_by_preferred_time(slots, preferred_windows, duration):
    """
    Filter time slots to only include those that fit entirely within
    at least one preferred time window.
    If no preferred windows are defined, all slots are returned unchanged.
    """
    if not preferred_windows:
        return slots
    filtered = []
    for slot in slots:
        for (win_start, win_end) in preferred_windows:
            if slot >= win_start and slot + duration <= win_end:
                filtered.append(slot)
                break
    return filtered


def filter_rooms_by_type_and_institute(rooms, course_type, institute_id, branch_id=None):
    """
    Filter rooms by type (Lecture/Laboratory), institute, and branch.
    - Lecture rooms: available to ALL institutes (no institute filter)
    - Laboratory rooms: strictly filtered by institute ownership
    - IAAS (institute_id=IAAS_INSTITUTE_ID): Lab and Lecture rooms are interchangeable
    - All rooms: must belong to the same college branch as the class
    """
    is_iaas = (institute_id == IAAS_INSTITUTE_ID)
    filtered = []
    for room in rooms:
        room_type = room.get("room_type", "").strip()
        room_institute = room.get("institute_id")
        room_branch = room.get("branch_id")

        # IAAS: lab and lecture rooms are interchangeable — skip type filter
        # For all other institutes: room type must match course type
        if not is_iaas:
            if room_type.lower() != course_type.lower():
                continue

        # All rooms must match the class's college branch
        if branch_id is not None:
            if room_branch is None or room_branch != branch_id:
                continue

        # Laboratory rooms are strictly owned by their institute
        # Lecture rooms are open to all institutes
        # IAAS: all rooms owned by IAAS are available (both types)
        if is_iaas:
            if room_institute is not None and room_institute != institute_id:
                # For IAAS, also allow lecture rooms (open to all) even from other institutes
                if room_type.lower() == "laboratory":
                    continue
        else:
            if course_type.lower() == "laboratory":
                if institute_id is not None and room_institute is not None:
                    if room_institute != institute_id:
                        continue

        filtered.append(room)

    return filtered


def find_suitable_room(rooms, course_type, institute_id, class_size, day, start_hour,
                       duration, schedule_tracker, branch_id=None):
    """
    Find a suitable room that matches all requirements.
    """
    # Filter rooms by type, institute, and branch
    candidate_rooms = filter_rooms_by_type_and_institute(
        rooms, course_type, institute_id, branch_id)

    # Sort by capacity (prefer rooms closer to class size)
    candidate_rooms.sort(key=lambda r: r.get(
        "room_capacity", 0))  # Changed from "capacity"

    for room in candidate_rooms:
        room_capacity = room.get("room_capacity", 0)  # Changed from "capacity"

        # Check capacity (allow up to MAX_CAPACITY_EXCESS over)
        if room_capacity < class_size:
            if class_size - room_capacity > MAX_CAPACITY_EXCESS:
                continue

        # Check if room is available
        if is_room_available(room, day, start_hour, duration, schedule_tracker):
            return room

    return None


def schedule_class_with_lab(cls, rooms, faculty_id, employment_type,
                            schedule_tracker, faculty_schedule_tracker,
                            unscheduled_meetings, class_schedule_tracker,
                            day_pattern_tracker, preferred_time=None, faculty_branch_tracker=None,
                            far_branch_set=None):
    """
    Schedule a class that has both lecture and lab components.
    They must be scheduled consecutively (lecture first, then lab) on the same day.
    Classes meet on a day pattern (TTH, MF, or MWF) with hours split equally.

    Part-time faculty can only be scheduled from 5:00 PM onwards.

    IMPORTANT: Classes with lab MUST be face-to-face (require physical rooms).

    Returns list of scheduled meetings if successful, None otherwise.
    """
    institute_id = cls.get("institute_id")
    class_size = cls.get("class_size", 30)
    class_branch_id = cls.get("branch_id")

    # Classes with lab MUST be face-to-face
    schedule_type = "face to face"

    lecture_units = cls.get("course_lec", 0)
    lab_units = cls.get("course_lab", 0)

    # Convert units to contact hours (total per week)
    lecture_hours_per_week = lecture_units * LECTURE_UNIT_TO_HOUR
    lab_hours_per_week = lab_units * LAB_UNIT_TO_HOUR
    total_hours_per_week = lecture_hours_per_week + lab_hours_per_week

    # Determine start and end hours based on employment type
    if employment_type.lower() == "part time":
        scheduling_start_hour = PART_TIME_START_HOUR
        scheduling_end_hour = PART_TIME_END_HOUR
    else:
        scheduling_start_hour = START_HOUR
        scheduling_end_hour = END_HOUR

    # Track the most recent failure reason for specific error reporting
    fail_reason = "No available time slots"

    # Try each day pattern (TTH, MF, MWF) - balanced for fairness
    balanced_patterns = get_balanced_patterns(day_pattern_tracker, total_hours_per_week)
    for pattern_name, pattern_days in balanced_patterns:
        num_meetings = len(pattern_days)
        lecture_hours = lecture_hours_per_week / num_meetings
        lab_hours = lab_hours_per_week / num_meetings
        total_duration = lecture_hours + lab_hours

        # Each component (lecture, lab) must be at least 1 hour per meeting
        if lecture_hours_per_week > 0 and lecture_hours < 1.0:
            continue
        if lab_hours_per_week > 0 and lab_hours < 1.0:
            continue

        # Get AM/PM-balanced slots for fair distribution across morning and afternoon
        available_slots = get_balanced_slots(
            faculty_id, pattern_days, total_duration,
            scheduling_start_hour, scheduling_end_hour,
            faculty_schedule_tracker)
        # Restrict to preferred time windows if the faculty has one
        available_slots = filter_slots_by_preferred_time(
            available_slots, preferred_time, total_duration)

        # Try each time slot — balanced between AM and PM
        for start_hour in available_slots:
            # Check faculty availability on ALL days
            if not all(is_faculty_available(faculty_id, day, start_hour, total_duration,
                                           faculty_schedule_tracker)
                       for day in pattern_days):
                fail_reason = "Faculty time conflict"
                continue

            # Constraint: Check faculty daily workload limit (max 8 hours per day)
            if not all(get_faculty_daily_hours(faculty_id, day, faculty_schedule_tracker) + total_duration <= 8
                       for day in pattern_days):
                fail_reason = "Faculty daily workload limit exceeded (max 8 hours)"
                continue

            # Constraint: Check faculty daily span (max MAX_DAILY_SPAN_HOURS from first to last class)
            if not all(check_daily_span_ok(faculty_id, day, start_hour, total_duration, faculty_schedule_tracker)
                       for day in pattern_days):
                fail_reason = f"Faculty daily span would exceed {MAX_DAILY_SPAN_HOURS} hours"
                continue

            # Constraint: Check class section availability on ALL days
            class_id = cls["class_id"]
            if not all(is_class_available(class_id, day, start_hour, total_duration, class_schedule_tracker)
                       for day in pattern_days):
                fail_reason = "Class section time conflict"
                continue

            # Decide whether this class uses same room or different rooms per day
            lab_start_hour = start_hour + lecture_hours
            allow_different_rooms = random.random() < DIFFERENT_ROOM_PERCENTAGE

            if allow_different_rooms:
                # --- Per-day independent room finding (each day can have a different room) ---
                day_lecture_rooms = {}
                day_lab_rooms = {}
                rooms_found = True
                for day in pattern_days:
                    lec_room = find_suitable_room(rooms, "Lecture", institute_id, class_size,
                                                  day, start_hour, lecture_hours, schedule_tracker, class_branch_id)
                    if not lec_room:
                        fail_reason = "No available lecture room"
                        rooms_found = False
                        break
                    lab_room = find_suitable_room(rooms, "Laboratory", institute_id, class_size,
                                                  day, lab_start_hour, lab_hours, schedule_tracker, class_branch_id)
                    if not lab_room:
                        fail_reason = "No available laboratory room"
                        rooms_found = False
                        break
                    day_lecture_rooms[day] = lec_room
                    day_lab_rooms[day] = lab_room
                if not rooms_found:
                    continue
            else:
                # --- Same room on all pattern days (original behavior) ---
                lecture_room = find_suitable_room(rooms, "Lecture", institute_id, class_size,
                                                  pattern_days[0], start_hour, lecture_hours, schedule_tracker, class_branch_id)
                if not lecture_room:
                    fail_reason = "No available lecture room"
                    continue
                if not all(is_room_available(lecture_room, day, start_hour, lecture_hours, schedule_tracker)
                           for day in pattern_days[1:]):
                    fail_reason = "No available lecture room on all pattern days"
                    continue
                lab_room = find_suitable_room(rooms, "Laboratory", institute_id, class_size,
                                              pattern_days[0], lab_start_hour, lab_hours, schedule_tracker, class_branch_id)
                if not lab_room:
                    fail_reason = "No available laboratory room"
                    continue
                if not all(is_room_available(lab_room, day, lab_start_hour, lab_hours, schedule_tracker)
                           for day in pattern_days[1:]):
                    fail_reason = "No available laboratory room on all pattern days"
                    continue
                # Use same room for every day
                day_lecture_rooms = {day: lecture_room for day in pattern_days}
                day_lab_rooms = {day: lab_room for day in pattern_days}

            # Constraint: Check faculty branch consistency on ALL days
            branch_id = cls.get("branch_id")
            if not all(is_branch_available(faculty_id, day, branch_id,
                                           faculty_branch_tracker if faculty_branch_tracker is not None else {},
                                           far_branch_set)
                       for day in pattern_days):
                fail_reason = "Faculty branch conflict"
                continue

            # Constraint: Check travel time compatibility on ALL days (using each day's lecture room)
            travel_ok = True
            for day in pattern_days:
                day_lec = day_lecture_rooms[day]
                lec_building = day_lec.get("building_name")
                lec_travel = day_lec.get("time_travel", 0)
                if not check_travel_time_compatible(
                        faculty_id, day, start_hour, total_duration,
                        lec_building, lec_travel, faculty_schedule_tracker):
                    travel_ok = False
                    break
            if not travel_ok:
                fail_reason = "Travel time conflict between buildings"
                continue

            # All checks passed! Schedule on ALL days of the pattern
            scheduled_meetings = []

            for day in pattern_days:
                day_lec_room = day_lecture_rooms[day]
                day_lab_room = day_lab_rooms[day]
                day_lec_room_id = day_lec_room["room_id"]
                day_lab_room_id = day_lab_room["room_id"]

                # Schedule lecture room
                if day_lec_room_id not in schedule_tracker:
                    schedule_tracker[day_lec_room_id] = {}
                if day not in schedule_tracker[day_lec_room_id]:
                    schedule_tracker[day_lec_room_id][day] = []

                schedule_tracker[day_lec_room_id][day].append({
                    "start_hour": start_hour,
                    "duration": lecture_hours,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"]
                })

                # Schedule lab room
                if day_lab_room_id not in schedule_tracker:
                    schedule_tracker[day_lab_room_id] = {}
                if day not in schedule_tracker[day_lab_room_id]:
                    schedule_tracker[day_lab_room_id][day] = []

                schedule_tracker[day_lab_room_id][day].append({
                    "start_hour": lab_start_hour,
                    "duration": lab_hours,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"]
                })

                # Add to faculty schedule tracker
                if faculty_id not in faculty_schedule_tracker:
                    faculty_schedule_tracker[faculty_id] = {}
                if day not in faculty_schedule_tracker[faculty_id]:
                    faculty_schedule_tracker[faculty_id][day] = []

                faculty_schedule_tracker[faculty_id][day].append({
                    "start_hour": start_hour,
                    "duration": total_duration,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"],
                    "building_name": day_lec_room.get("building_name"),
                    "travel_time": day_lec_room.get("time_travel", 0)
                })

                # Add to class schedule tracker
                if class_id not in class_schedule_tracker:
                    class_schedule_tracker[class_id] = {}
                if day not in class_schedule_tracker[class_id]:
                    class_schedule_tracker[class_id][day] = []

                class_schedule_tracker[class_id][day].append({
                    "start_hour": start_hour,
                    "duration": total_duration,
                    "faculty_id": faculty_id,
                    "course_code": cls["course_code"]
                })

                # Create lecture meeting entry
                scheduled_meetings.append({
                    "class_id": cls["class_id"],
                    "set_name": cls["set_name"],
                    "course_level": cls["course_level"],
                    "course_code": cls["course_code"],
                    "program_id": cls["program_id"],
                    "program_name": cls.get("program_name", "Unknown"),
                    "program_code": cls.get("program_code", "Unknown"),
                    "institute_id": institute_id,
                    "type": "Lecture",
                    "day": day,
                    "start_hour": start_hour,
                    "duration": lecture_hours,
                    "time_slot": format_time_slot(start_hour, lecture_hours),
                    "room_id": day_lec_room_id,
                    "room_name": day_lec_room.get("room_name", "Unknown"),
                    "room_type": day_lec_room.get("room_type", "Unknown"),
                    "room_capacity": day_lec_room.get("room_capacity", 0),
                    "class_size": class_size,
                    "schedule_type": schedule_type
                })

                # Create lab meeting entry
                scheduled_meetings.append({
                    "class_id": cls["class_id"],
                    "set_name": cls["set_name"],
                    "course_level": cls["course_level"],
                    "course_code": cls["course_code"],
                    "program_id": cls["program_id"],
                    "program_name": cls.get("program_name", "Unknown"),
                    "program_code": cls.get("program_code", "Unknown"),
                    "institute_id": institute_id,
                    "type": "Laboratory",
                    "day": day,
                    "start_hour": lab_start_hour,
                    "duration": lab_hours,
                    "time_slot": format_time_slot(lab_start_hour, lab_hours),
                    "room_id": day_lab_room_id,
                    "room_name": day_lab_room.get("room_name", "Unknown"),
                    "room_type": day_lab_room.get("room_type", "Unknown"),
                    "room_capacity": day_lab_room.get("room_capacity", 0),
                    "class_size": class_size,
                    "schedule_type": schedule_type
                })

            # Update day pattern tracker for fairness
            day_pattern_tracker[pattern_name] = day_pattern_tracker.get(pattern_name, 0) + 1

            # Update faculty branch tracker for all days
            update_branch_tracker(faculty_id, pattern_days, branch_id, faculty_branch_tracker if faculty_branch_tracker is not None else {})

            return scheduled_meetings

    # Fallback: Try Wednesday with full hours (not split)
    wednesday = FALLBACK_DAY
    wed_lecture_hours = lecture_hours_per_week
    wed_lab_hours = lab_hours_per_week
    wed_total_duration = wed_lecture_hours + wed_lab_hours

    # Get AM/PM-balanced slots on Wednesday
    available_slots = get_balanced_slots(
        faculty_id, [wednesday], wed_total_duration,
        scheduling_start_hour, scheduling_end_hour,
        faculty_schedule_tracker)
    available_slots = filter_slots_by_preferred_time(
        available_slots, preferred_time, wed_total_duration)

    for start_hour in available_slots:
        if not is_faculty_available(faculty_id, wednesday, start_hour, wed_total_duration,
                                    faculty_schedule_tracker):
            fail_reason = "Faculty time conflict"
            continue

        faculty_hours_wed = get_faculty_daily_hours(faculty_id, wednesday, faculty_schedule_tracker)
        if faculty_hours_wed + wed_total_duration > 8:
            fail_reason = "Faculty daily workload limit exceeded (max 8 hours)"
            continue

        if not check_daily_span_ok(faculty_id, wednesday, start_hour, wed_total_duration, faculty_schedule_tracker):
            fail_reason = f"Faculty daily span would exceed {MAX_DAILY_SPAN_HOURS} hours"
            continue

        class_id = cls["class_id"]
        if not is_class_available(class_id, wednesday, start_hour, wed_total_duration, class_schedule_tracker):
            fail_reason = "Class section time conflict"
            continue

        branch_id = cls.get("branch_id")
        if not is_branch_available(faculty_id, wednesday, branch_id,
                                   faculty_branch_tracker if faculty_branch_tracker is not None else {},
                                   far_branch_set):
            fail_reason = "Faculty branch conflict"
            continue

        lecture_room = find_suitable_room(rooms, "Lecture", institute_id, class_size,
                                          wednesday, start_hour, wed_lecture_hours, schedule_tracker, class_branch_id)
        if not lecture_room:
            fail_reason = "No available lecture room"
            continue

        wed_lab_start_hour = start_hour + wed_lecture_hours
        lab_room = find_suitable_room(rooms, "Laboratory", institute_id, class_size,
                                      wednesday, wed_lab_start_hour, wed_lab_hours, schedule_tracker, class_branch_id)
        if not lab_room:
            fail_reason = "No available laboratory room"
            continue

        # Constraint: Check travel time compatibility on Wednesday
        wed_lec_building = lecture_room.get("building_name")
        wed_lec_travel = lecture_room.get("time_travel", 0)
        if not check_travel_time_compatible(
                faculty_id, wednesday, start_hour, wed_total_duration,
                wed_lec_building, wed_lec_travel, faculty_schedule_tracker):
            fail_reason = "Travel time conflict between buildings"
            continue

        # All checks passed! Schedule on Wednesday only
        scheduled_meetings = []

        lecture_room_id = lecture_room["room_id"]
        if lecture_room_id not in schedule_tracker:
            schedule_tracker[lecture_room_id] = {}
        if wednesday not in schedule_tracker[lecture_room_id]:
            schedule_tracker[lecture_room_id][wednesday] = []
        schedule_tracker[lecture_room_id][wednesday].append({
            "start_hour": start_hour,
            "duration": wed_lecture_hours,
            "class_id": cls["class_id"],
            "course_code": cls["course_code"]
        })

        lab_room_id = lab_room["room_id"]
        if lab_room_id not in schedule_tracker:
            schedule_tracker[lab_room_id] = {}
        if wednesday not in schedule_tracker[lab_room_id]:
            schedule_tracker[lab_room_id][wednesday] = []
        schedule_tracker[lab_room_id][wednesday].append({
            "start_hour": wed_lab_start_hour,
            "duration": wed_lab_hours,
            "class_id": cls["class_id"],
            "course_code": cls["course_code"]
        })

        if faculty_id not in faculty_schedule_tracker:
            faculty_schedule_tracker[faculty_id] = {}
        if wednesday not in faculty_schedule_tracker[faculty_id]:
            faculty_schedule_tracker[faculty_id][wednesday] = []
        faculty_schedule_tracker[faculty_id][wednesday].append({
            "start_hour": start_hour,
            "duration": wed_total_duration,
            "class_id": cls["class_id"],
            "course_code": cls["course_code"],
            "building_name": lecture_room.get("building_name"),
            "travel_time": lecture_room.get("time_travel", 0)
        })

        if class_id not in class_schedule_tracker:
            class_schedule_tracker[class_id] = {}
        if wednesday not in class_schedule_tracker[class_id]:
            class_schedule_tracker[class_id][wednesday] = []
        class_schedule_tracker[class_id][wednesday].append({
            "start_hour": start_hour,
            "duration": wed_total_duration,
            "faculty_id": faculty_id,
            "course_code": cls["course_code"]
        })

        scheduled_meetings.append({
            "class_id": cls["class_id"],
            "set_name": cls["set_name"],
            "course_level": cls["course_level"],
            "course_code": cls["course_code"],
            "program_id": cls["program_id"],
            "program_name": cls.get("program_name", "Unknown"),
            "program_code": cls.get("program_code", "Unknown"),
            "institute_id": institute_id,
            "type": "Lecture",
            "day": wednesday,
            "start_hour": start_hour,
            "duration": wed_lecture_hours,
            "time_slot": format_time_slot(start_hour, wed_lecture_hours),
            "room_id": lecture_room_id,
            "room_name": lecture_room.get("room_name", "Unknown"),
            "room_type": lecture_room.get("room_type", "Unknown"),
            "room_capacity": lecture_room.get("room_capacity", 0),
            "class_size": class_size,
            "schedule_type": schedule_type
        })

        scheduled_meetings.append({
            "class_id": cls["class_id"],
            "set_name": cls["set_name"],
            "course_level": cls["course_level"],
            "course_code": cls["course_code"],
            "program_id": cls["program_id"],
            "program_name": cls.get("program_name", "Unknown"),
            "program_code": cls.get("program_code", "Unknown"),
            "institute_id": institute_id,
            "type": "Laboratory",
            "day": wednesday,
            "start_hour": wed_lab_start_hour,
            "duration": wed_lab_hours,
            "time_slot": format_time_slot(wed_lab_start_hour, wed_lab_hours),
            "room_id": lab_room_id,
            "room_name": lab_room.get("room_name", "Unknown"),
            "room_type": lab_room.get("room_type", "Unknown"),
            "room_capacity": lab_room.get("room_capacity", 0),
            "class_size": class_size,
            "schedule_type": schedule_type
        })

        update_branch_tracker(faculty_id, [wednesday], branch_id, faculty_branch_tracker if faculty_branch_tracker is not None else {})

        return scheduled_meetings

    # Could not schedule
    unscheduled_meetings.append({
        "class_id": cls["class_id"],
        "course_code": cls["course_code"],
        "course_id": cls.get("course_id"),
        "institute_id": cls.get("institute_id"),
        "class_size": cls.get("class_size", 30),
        "faculty_name": cls.get("faculty_name", "Unknown"),
        "program_id": cls["program_id"],
        "program_name": cls.get("program_name", "Unknown"),
        "program_code": cls.get("program_code", "Unknown"),
        "type": "Lecture+Lab",
        "hours": f"{lecture_hours_per_week}h lec + {lab_hours_per_week}h lab per week",
        "reason": fail_reason
    })

    return None


def schedule_lecture_only(cls, rooms, faculty_id, employment_type,
                          schedule_tracker, faculty_schedule_tracker,
                          unscheduled_meetings, class_schedule_tracker,
                          lecture_type_tracker, day_pattern_tracker, preferred_time=None, faculty_branch_tracker=None,
                          day_f2f_tracker=None, far_branch_set=None, faculty_lecture_type_tracker=None):
    """
    Schedule a class that has only lecture (no lab).
    Classes meet on a day pattern (TTH, MF, or MWF) with hours split equally per meeting.

    Part-time faculty can only be scheduled from 5:00 PM onwards.

    Strategy:
    - Each meeting day in the pattern gets its OWN face-to-face or online assignment
    - num_f2f_days = int(len(pattern_days) * TARGET_FACE_TO_FACE_PERCENTAGE + 0.5)
      e.g. 30% on MF (2 days) -> 1 f2f + 1 online;  30% on MWF (3 days) -> 1 f2f + 2 online
    - Fairness: days with fewer f2f assignments (day_f2f_tracker) get f2f priority,
      ties are broken randomly so no single day always wins
    - One room is found for ALL f2f days together; if unavailable, those days fall back to online
    - Day patterns are balanced for fair distribution (day_pattern_tracker)
    - Patterns are filtered by minimum 1-hour-per-meeting rule

    Returns list of scheduled meetings if successful, None otherwise.
    """
    if day_f2f_tracker is None:
        day_f2f_tracker = {}

    institute_id = cls.get("institute_id")
    class_size = cls.get("class_size", 30)
    class_branch_id = cls.get("branch_id")

    lecture_units = cls.get("course_lec", 0)
    lecture_hours_per_week = lecture_units * LECTURE_UNIT_TO_HOUR

    # Determine start and end hours based on employment type
    if employment_type.lower() == "part time":
        scheduling_start_hour = PART_TIME_START_HOUR
        scheduling_end_hour = PART_TIME_END_HOUR
    else:
        scheduling_start_hour = START_HOUR
        scheduling_end_hour = END_HOUR

    # Track the most recent failure reason for specific error reporting
    fail_reason = "No available time slots"

    # Try each day pattern - balanced for fairness
    balanced_patterns = get_balanced_patterns(day_pattern_tracker, lecture_hours_per_week)
    for pattern_name, pattern_days in balanced_patterns:
        num_meetings = len(pattern_days)

        # Compute per-day hours (uneven split if hours don't divide evenly)
        # e.g. 3h on 2 days = [2, 1] instead of [1.5, 1.5]
        short_h = int(lecture_hours_per_week // num_meetings)
        remainder = int(lecture_hours_per_week - short_h * num_meetings)
        if remainder > 0:
            long_h = short_h + 1
            hours_list = [long_h] * remainder + [short_h] * (num_meetings - remainder)
            random.shuffle(hours_list)  # fairness: randomize which day gets the longer block
        else:
            hours_list = [int(lecture_hours_per_week // num_meetings)] * num_meetings
        max_duration = max(hours_list)

        # Get AM/PM-balanced slots for fair distribution across morning and afternoon
        available_slots = get_balanced_slots(
            faculty_id, pattern_days, max_duration,
            scheduling_start_hour, scheduling_end_hour,
            faculty_schedule_tracker)
        # Restrict to preferred time windows if the faculty has one
        available_slots = filter_slots_by_preferred_time(
            available_slots, preferred_time, max_duration)

        # Try each time slot — balanced between AM and PM
        for start_hour in available_slots:
            # Check faculty availability on ALL days (per-day duration)
            if not all(is_faculty_available(faculty_id, day, start_hour, hours_list[i],
                                           faculty_schedule_tracker)
                       for i, day in enumerate(pattern_days)):
                fail_reason = "Faculty time conflict"
                continue

            # Constraint: Check faculty daily workload limit (max 8 hours per day)
            if not all(get_faculty_daily_hours(faculty_id, day, faculty_schedule_tracker) + hours_list[i] <= 8
                       for i, day in enumerate(pattern_days)):
                fail_reason = "Faculty daily workload limit exceeded (max 8 hours)"
                continue

            # Constraint: Check faculty daily span (max MAX_DAILY_SPAN_HOURS from first to last class)
            if not all(check_daily_span_ok(faculty_id, day, start_hour, hours_list[i], faculty_schedule_tracker)
                       for i, day in enumerate(pattern_days)):
                fail_reason = f"Faculty daily span would exceed {MAX_DAILY_SPAN_HOURS} hours"
                continue

            # Constraint: Check class section availability on ALL days (per-day duration)
            class_id = cls["class_id"]
            if not all(is_class_available(class_id, day, start_hour, hours_list[i], class_schedule_tracker)
                       for i, day in enumerate(pattern_days)):
                fail_reason = "Class section time conflict"
                continue

            # Constraint: Check faculty branch consistency on ALL days
            branch_id = cls.get("branch_id")
            if not all(is_branch_available(faculty_id, day, branch_id,
                                           faculty_branch_tracker if faculty_branch_tracker is not None else {},
                                           far_branch_set)
                       for day in pattern_days):
                fail_reason = "Faculty branch conflict"
                continue

            # --- Per-day face-to-face / online assignment ---
            # Branch-specific rules override the default f2f/online logic
            branch_rules = get_branch_schedule_rules(class_branch_id)

            if branch_rules["force_f2f"]:
                # Samal / DAPECOL: ALL days must be face-to-face
                num_f2f = n = len(pattern_days)
                f2f_day_set = set(pattern_days)
            else:
                # Standard f2f/online split — use per-faculty tracker for accurate ratio
                n = len(pattern_days)
                if faculty_lecture_type_tracker is not None and faculty_id in faculty_lecture_type_tracker:
                    fac_f2f = faculty_lecture_type_tracker[faculty_id]["f2f"]
                    fac_total = faculty_lecture_type_tracker[faculty_id]["total"]
                    hours_per_day = lecture_hours_per_week / n
                    target_f2f_total = (fac_total + lecture_hours_per_week) * TARGET_FACE_TO_FACE_PERCENTAGE
                    f2f_still_needed = max(0.0, target_f2f_total - fac_f2f)
                    num_f2f = min(n, max(0, round(f2f_still_needed / hours_per_day)))
                else:
                    num_f2f = int(n * TARGET_FACE_TO_FACE_PERCENTAGE + 0.5)
                num_f2f = max(0, min(n, num_f2f))

                # When hours are uneven, assign longer-hour days to f2f
                has_uneven_hours = len(set(hours_list)) > 1
                if has_uneven_hours and num_f2f < n:
                    day_hour_pairs = list(zip(pattern_days, hours_list))
                    day_hour_pairs.sort(key=lambda dh: (-dh[1], day_f2f_tracker.get(dh[0], 0), random.random()))
                    f2f_day_set = set(d for d, _ in day_hour_pairs[:num_f2f])
                else:
                    days_sorted = sorted(pattern_days,
                                         key=lambda d: (day_f2f_tracker.get(d, 0), random.random()))
                    f2f_day_set = set(days_sorted[:num_f2f])

            day_types = {d: ("face to face" if d in f2f_day_set else "online")
                         for d in pattern_days}

            # Find room for each f2f day independently (different days can have different rooms)
            day_rooms = {}
            rooms_ok = True
            for i, day in enumerate(pattern_days):
                if day_types[day] == "face to face":
                    room = find_suitable_room(rooms, "Lecture", institute_id, class_size,
                                              day, start_hour, hours_list[i], schedule_tracker, class_branch_id)
                    if room:
                        day_rooms[day] = room
                    else:
                        # For force_f2f branches (Samal/DAPECOL), no room = cannot schedule
                        if branch_rules["force_f2f"]:
                            fail_reason = "No available room for mandatory f2f branch"
                            rooms_ok = False
                            break
                        day_types[day] = "online"  # fallback this specific day only
            if not rooms_ok:
                continue

            # Constraint: Check travel time compatibility on each day with its room
            # For online classes at non-Main branches, use the branch's travel time
            travel_conflict = False
            for i, day in enumerate(pattern_days):
                day_room = day_rooms.get(day)
                if day_room:
                    room_building = day_room.get("building_name")
                    room_travel = day_room.get("time_travel", 0)
                else:
                    branch_travel = get_branch_travel_time(rooms, class_branch_id)
                    room_building = f"__branch_{class_branch_id}" if branch_travel > 0 else None
                    room_travel = branch_travel
                if not check_travel_time_compatible(
                        faculty_id, day, start_hour, hours_list[i],
                        room_building, room_travel, faculty_schedule_tracker):
                    travel_conflict = True
                    break
            if travel_conflict:
                fail_reason = "Travel time conflict between buildings"
                continue

            # Schedule each day with its own schedule_type and per-day hours
            scheduled_meetings = []
            for i, day in enumerate(pattern_days):
                day_hours = hours_list[i]
                schedule_type = day_types[day]
                day_is_f2f = (schedule_type == "face to face")
                day_room = day_rooms.get(day)

                # Room tracker (only for f2f days)
                if day_is_f2f and day_room:
                    day_room_id = day_room["room_id"]
                    if day_room_id not in schedule_tracker:
                        schedule_tracker[day_room_id] = {}
                    if day not in schedule_tracker[day_room_id]:
                        schedule_tracker[day_room_id][day] = []
                    schedule_tracker[day_room_id][day].append({
                        "start_hour": start_hour,
                        "duration": day_hours,
                        "class_id": cls["class_id"],
                        "course_code": cls["course_code"]
                    })

                # Faculty schedule tracker (all days)
                # For online classes at non-Main branches, use the branch's travel time
                # so inter-branch travel gaps are still enforced
                if faculty_id not in faculty_schedule_tracker:
                    faculty_schedule_tracker[faculty_id] = {}
                if day not in faculty_schedule_tracker[faculty_id]:
                    faculty_schedule_tracker[faculty_id][day] = []
                day_room = day_rooms.get(day)
                if day_room:
                    sched_building = day_room.get("building_name")
                    sched_travel = day_room.get("time_travel", 0)
                else:
                    # Online class — use branch travel time for inter-branch gap enforcement
                    branch_travel = get_branch_travel_time(rooms, class_branch_id)
                    sched_building = f"__branch_{class_branch_id}" if branch_travel > 0 else None
                    sched_travel = branch_travel
                faculty_schedule_tracker[faculty_id][day].append({
                    "start_hour": start_hour,
                    "duration": day_hours,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"],
                    "building_name": sched_building,
                    "travel_time": sched_travel
                })

                # Class schedule tracker (all days)
                if class_id not in class_schedule_tracker:
                    class_schedule_tracker[class_id] = {}
                if day not in class_schedule_tracker[class_id]:
                    class_schedule_tracker[class_id][day] = []
                class_schedule_tracker[class_id][day].append({
                    "start_hour": start_hour,
                    "duration": day_hours,
                    "faculty_id": faculty_id,
                    "course_code": cls["course_code"]
                })

                # Build meeting entry with per-day schedule_type and per-day hours
                meeting_entry = {
                    "class_id": cls["class_id"],
                    "set_name": cls["set_name"],
                    "course_level": cls["course_level"],
                    "course_code": cls["course_code"],
                    "program_id": cls["program_id"],
                    "program_name": cls.get("program_name", "Unknown"),
                    "program_code": cls.get("program_code", "Unknown"),
                    "institute_id": institute_id,
                    "type": "Lecture",
                    "day": day,
                    "start_hour": start_hour,
                    "duration": day_hours,
                    "time_slot": format_time_slot(start_hour, day_hours),
                    "class_size": class_size,
                    "schedule_type": schedule_type
                }

                if day_is_f2f and day_room:
                    meeting_entry["room_id"] = day_room["room_id"]
                    meeting_entry["room_name"] = day_room.get("room_name", "Unknown")
                    meeting_entry["room_type"] = day_room.get("room_type", "Unknown")
                    meeting_entry["room_capacity"] = day_room.get("room_capacity", 0)
                else:
                    meeting_entry["room_id"] = None
                    meeting_entry["room_name"] = "Online"
                    meeting_entry["room_type"] = "Online"
                    meeting_entry["room_capacity"] = 0

                scheduled_meetings.append(meeting_entry)

            # Update lecture_type_tracker with actual per-day hours
            for i, day in enumerate(pattern_days):
                if day_types[day] == "face to face":
                    lecture_type_tracker["face_to_face_hours"] += hours_list[i]
                else:
                    lecture_type_tracker["online_hours"] += hours_list[i]
            lecture_type_tracker["total_lecture_hours"] += lecture_hours_per_week

            # Update day_f2f_tracker for fairness across future classes
            for day in pattern_days:
                if day_types[day] == "face to face":
                    day_f2f_tracker[day] = day_f2f_tracker.get(day, 0) + 1

            # Update day pattern tracker for fairness
            day_pattern_tracker[pattern_name] = day_pattern_tracker.get(pattern_name, 0) + 1

            # Update per-faculty f2f/online tracker
            if faculty_lecture_type_tracker is not None:
                if faculty_id not in faculty_lecture_type_tracker:
                    faculty_lecture_type_tracker[faculty_id] = {"f2f": 0.0, "online": 0.0, "total": 0.0}
                faculty_lecture_type_tracker[faculty_id]["total"] += lecture_hours_per_week
                for i, day in enumerate(pattern_days):
                    if day_types[day] == "face to face":
                        faculty_lecture_type_tracker[faculty_id]["f2f"] += hours_list[i]
                    else:
                        faculty_lecture_type_tracker[faculty_id]["online"] += hours_list[i]

            # Update faculty branch tracker for all days
            update_branch_tracker(faculty_id, pattern_days, branch_id, faculty_branch_tracker if faculty_branch_tracker is not None else {})

            return scheduled_meetings

    # Fallback: Try Wednesday with full hours (not split)
    wednesday = FALLBACK_DAY
    wed_lecture_hours = lecture_hours_per_week  # Full hours for single day

    # Get AM/PM-balanced slots on Wednesday
    available_slots = get_balanced_slots(
        faculty_id, [wednesday], wed_lecture_hours,
        scheduling_start_hour, scheduling_end_hour,
        faculty_schedule_tracker)
    available_slots = filter_slots_by_preferred_time(
        available_slots, preferred_time, wed_lecture_hours)

    for start_hour in available_slots:
        if not is_faculty_available(faculty_id, wednesday, start_hour, wed_lecture_hours,
                                    faculty_schedule_tracker):
            fail_reason = "Faculty time conflict"
            continue

        faculty_hours_wed = get_faculty_daily_hours(faculty_id, wednesday, faculty_schedule_tracker)
        if faculty_hours_wed + wed_lecture_hours > 8:
            fail_reason = "Faculty daily workload limit exceeded (max 8 hours)"
            continue

        if not check_daily_span_ok(faculty_id, wednesday, start_hour, wed_lecture_hours, faculty_schedule_tracker):
            fail_reason = f"Faculty daily span would exceed {MAX_DAILY_SPAN_HOURS} hours"
            continue

        class_id = cls["class_id"]
        if not is_class_available(class_id, wednesday, start_hour, wed_lecture_hours, class_schedule_tracker):
            fail_reason = "Class section time conflict"
            continue

        branch_id = cls.get("branch_id")
        if not is_branch_available(faculty_id, wednesday, branch_id,
                                   faculty_branch_tracker if faculty_branch_tracker is not None else {},
                                   far_branch_set):
            fail_reason = "Faculty branch conflict"
            continue

        # Per-day f2f/online for Wednesday — branch rules override
        wed_branch_rules = get_branch_schedule_rules(class_branch_id)
        if wed_branch_rules["force_f2f"]:
            wed_schedule_type = "face to face"
        else:
            if faculty_lecture_type_tracker is not None and faculty_id in faculty_lecture_type_tracker:
                fac_f2f = faculty_lecture_type_tracker[faculty_id]["f2f"]
                fac_total = faculty_lecture_type_tracker[faculty_id]["total"]
                target_f2f_total = (fac_total + wed_lecture_hours) * TARGET_FACE_TO_FACE_PERCENTAGE
                f2f_still_needed = max(0.0, target_f2f_total - fac_f2f)
                wed_schedule_type = "face to face" if f2f_still_needed >= wed_lecture_hours * 0.5 else "online"
            else:
                wed_num_f2f = int(1 * TARGET_FACE_TO_FACE_PERCENTAGE + 0.5)
                wed_schedule_type = "face to face" if wed_num_f2f == 1 else "online"

        lecture_room = None
        schedule_type = wed_schedule_type

        if wed_schedule_type == "face to face":
            lecture_room = find_suitable_room(rooms, "Lecture", institute_id, class_size,
                                              wednesday, start_hour, wed_lecture_hours, schedule_tracker, class_branch_id)
            if not lecture_room:
                if wed_branch_rules["force_f2f"]:
                    fail_reason = "No available room for mandatory f2f branch"
                    continue
                schedule_type = "online"

        # Constraint: Check travel time compatibility on Wednesday
        if lecture_room:
            wed_room_building = lecture_room.get("building_name")
            wed_room_travel = lecture_room.get("time_travel", 0)
        else:
            wed_bt = get_branch_travel_time(rooms, class_branch_id)
            wed_room_building = f"__branch_{class_branch_id}" if wed_bt > 0 else None
            wed_room_travel = wed_bt
        if not check_travel_time_compatible(
                faculty_id, wednesday, start_hour, wed_lecture_hours,
                wed_room_building, wed_room_travel, faculty_schedule_tracker):
            fail_reason = "Travel time conflict between buildings"
            continue

        # Schedule on Wednesday only
        scheduled_meetings = []
        lecture_room_id = lecture_room["room_id"] if lecture_room else None

        # Add to room schedule tracker (only if face-to-face)
        if lecture_room:
            if lecture_room_id not in schedule_tracker:
                schedule_tracker[lecture_room_id] = {}
            if wednesday not in schedule_tracker[lecture_room_id]:
                schedule_tracker[lecture_room_id][wednesday] = []
            schedule_tracker[lecture_room_id][wednesday].append({
                "start_hour": start_hour,
                "duration": wed_lecture_hours,
                "class_id": cls["class_id"],
                "course_code": cls["course_code"]
            })

        if faculty_id not in faculty_schedule_tracker:
            faculty_schedule_tracker[faculty_id] = {}
        if wednesday not in faculty_schedule_tracker[faculty_id]:
            faculty_schedule_tracker[faculty_id][wednesday] = []
        if lecture_room:
            wed_sched_building = lecture_room.get("building_name")
            wed_sched_travel = lecture_room.get("time_travel", 0)
        else:
            wed_branch_travel = get_branch_travel_time(rooms, class_branch_id)
            wed_sched_building = f"__branch_{class_branch_id}" if wed_branch_travel > 0 else None
            wed_sched_travel = wed_branch_travel
        faculty_schedule_tracker[faculty_id][wednesday].append({
            "start_hour": start_hour,
            "duration": wed_lecture_hours,
            "class_id": cls["class_id"],
            "course_code": cls["course_code"],
            "building_name": wed_sched_building,
            "travel_time": wed_sched_travel
        })

        if class_id not in class_schedule_tracker:
            class_schedule_tracker[class_id] = {}
        if wednesday not in class_schedule_tracker[class_id]:
            class_schedule_tracker[class_id][wednesday] = []
        class_schedule_tracker[class_id][wednesday].append({
            "start_hour": start_hour,
            "duration": wed_lecture_hours,
            "faculty_id": faculty_id,
            "course_code": cls["course_code"]
        })

        # Create meeting entry (Wednesday - full hours)
        meeting_entry = {
            "class_id": cls["class_id"],
            "set_name": cls["set_name"],
            "course_level": cls["course_level"],
            "course_code": cls["course_code"],
            "program_id": cls["program_id"],
            "program_name": cls.get("program_name", "Unknown"),
            "program_code": cls.get("program_code", "Unknown"),
            "institute_id": institute_id,
            "type": "Lecture",
            "day": wednesday,
            "start_hour": start_hour,
            "duration": wed_lecture_hours,
            "time_slot": format_time_slot(start_hour, wed_lecture_hours),
            "class_size": class_size,
            "schedule_type": schedule_type
        }

        if lecture_room:
            meeting_entry["room_id"] = lecture_room_id
            meeting_entry["room_name"] = lecture_room.get("room_name", "Unknown")
            meeting_entry["room_type"] = lecture_room.get("room_type", "Unknown")
            meeting_entry["room_capacity"] = lecture_room.get("room_capacity", 0)
        else:
            meeting_entry["room_id"] = None
            meeting_entry["room_name"] = "Online"
            meeting_entry["room_type"] = "Online"
            meeting_entry["room_capacity"] = 0

        scheduled_meetings.append(meeting_entry)

        # Update lecture type tracker with Wednesday hours
        if schedule_type == "online":
            lecture_type_tracker["online_hours"] += wed_lecture_hours
        else:
            lecture_type_tracker["face_to_face_hours"] += wed_lecture_hours
            day_f2f_tracker[wednesday] = day_f2f_tracker.get(wednesday, 0) + 1
        lecture_type_tracker["total_lecture_hours"] += wed_lecture_hours

        # Update per-faculty f2f/online tracker
        if faculty_lecture_type_tracker is not None:
            if faculty_id not in faculty_lecture_type_tracker:
                faculty_lecture_type_tracker[faculty_id] = {"f2f": 0.0, "online": 0.0, "total": 0.0}
            faculty_lecture_type_tracker[faculty_id]["total"] += wed_lecture_hours
            if schedule_type == "online":
                faculty_lecture_type_tracker[faculty_id]["online"] += wed_lecture_hours
            else:
                faculty_lecture_type_tracker[faculty_id]["f2f"] += wed_lecture_hours

        # Update faculty branch tracker for Wednesday
        update_branch_tracker(faculty_id, [wednesday], branch_id, faculty_branch_tracker if faculty_branch_tracker is not None else {})

        return scheduled_meetings

    # Could not schedule on any day pattern or Wednesday
    unscheduled_meetings.append({
        "class_id": cls["class_id"],
        "course_code": cls["course_code"],
        "course_id": cls.get("course_id"),
        "institute_id": cls.get("institute_id"),
        "class_size": cls.get("class_size", 30),
        "faculty_name": cls.get("faculty_name", "Unknown"),
        "program_id": cls["program_id"],
        "program_name": cls.get("program_name", "Unknown"),
        "program_code": cls.get("program_code", "Unknown"),
        "type": "Lecture",
        "hours": f"{lecture_hours_per_week}h per week",
        "reason": fail_reason
    })

    return None


def schedule_class_meeting(cls, course_type, hours, rooms, faculty_id,
                           schedule_tracker, faculty_schedule_tracker,
                           unscheduled_meetings):
    """
    DEPRECATED: This function is kept for backward compatibility but not used in new logic.
    Try to schedule a single meeting (lecture or laboratory).
    Returns scheduled meeting dict if successful, None otherwise.
    """
    institute_id = cls.get("institute_id")
    class_size = cls.get("class_size", 30)  # Default to 30 if not specified
    class_branch_id = cls.get("branch_id")

    # Track the most recent failure reason for specific error reporting
    fail_reason = "No available time slots"

    # Try each day
    for day in DAYS:
        # Find available time slots for this duration
        available_slots = find_available_slots(START_HOUR, END_HOUR, hours)

        # Try each time slot
        for start_hour in available_slots:
            # Check faculty availability
            if not is_faculty_available(faculty_id, day, start_hour, hours,
                                        faculty_schedule_tracker):
                fail_reason = "Faculty time conflict"
                continue

            # Find suitable room
            room = find_suitable_room(rooms, course_type, institute_id, class_size,
                                      day, start_hour, hours, schedule_tracker, class_branch_id)

            if not room:
                fail_reason = f"No available {course_type.lower()} room"

            if room:
                # Schedule this meeting
                room_id = room["room_id"]

                # Add to room schedule tracker
                if room_id not in schedule_tracker:
                    schedule_tracker[room_id] = {}
                if day not in schedule_tracker[room_id]:
                    schedule_tracker[room_id][day] = []

                schedule_tracker[room_id][day].append({
                    "start_hour": start_hour,
                    "duration": hours,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"]
                })

                # Add to faculty schedule tracker
                if faculty_id not in faculty_schedule_tracker:
                    faculty_schedule_tracker[faculty_id] = {}
                if day not in faculty_schedule_tracker[faculty_id]:
                    faculty_schedule_tracker[faculty_id][day] = []

                faculty_schedule_tracker[faculty_id][day].append({
                    "start_hour": start_hour,
                    "duration": hours,
                    "class_id": cls["class_id"],
                    "course_code": cls["course_code"],
                    "building_name": room.get("building_name"),
                    "travel_time": room.get("time_travel", 0)
                })

                return {
                    "class_id": cls["class_id"],
                    "set_name": cls["set_name"],
                    "course_level": cls["course_level"],
                    "course_code": cls["course_code"],
                    "program_id": cls["program_id"],
                    "institute_id": institute_id,
                    "type": course_type,
                    "day": day,
                    "start_hour": start_hour,
                    "duration": hours,
                    "time_slot": format_time_slot(start_hour, hours),
                    "room_id": room_id,
                    "room_name": room.get("room_name", "Unknown"),
                    "room_type": room.get("room_type", "Unknown"),
                    # Changed from "capacity"
                    "room_capacity": room.get("room_capacity", 0),
                    "class_size": class_size
                }

    # Could not schedule
    unscheduled_meetings.append({
        "class_id": cls["class_id"],
        "course_code": cls["course_code"],
        "course_id": cls.get("course_id"),
        "institute_id": cls.get("institute_id"),
        "class_size": cls.get("class_size", 30),
        "faculty_name": cls.get("faculty_name", "Unknown"),
        "type": course_type,
        "hours": hours,
        "reason": fail_reason
    })

    return None


def generate_faculty_core_time(complete_schedule):
    """
    Generate faculty core time schedule (time-in / time-out per day).
    Full-time faculty must be present at school for FULL_TIME_WEEKLY_HOURS (40) hours/week.
    Daily hours can vary (7, 8, 9, etc.) as long as the weekly total is met.
    Time-in is at or before the earliest class, time-out is at or after the latest class end.

    Returns a list of dicts: one entry per faculty with their daily time_in/time_out.
    """
    # Build per-faculty, per-day class windows from the schedule
    faculty_days = {}
    for meeting in complete_schedule:
        fid = meeting.get("faculty_id")
        fname = meeting.get("faculty_name", "Unknown")
        emp_type = meeting.get("employment_type", "full time")
        day = meeting.get("day")
        start = meeting.get("start_hour", 0)
        duration = meeting.get("duration", 0)
        end = start + duration

        if fid not in faculty_days:
            faculty_days[fid] = {
                "faculty_name": fname,
                "employment_type": emp_type,
                "days": {}
            }

        if day not in faculty_days[fid]["days"]:
            faculty_days[fid]["days"][day] = {"earliest_start": start, "latest_end": end}
        else:
            entry = faculty_days[fid]["days"][day]
            if start < entry["earliest_start"]:
                entry["earliest_start"] = start
            if end > entry["latest_end"]:
                entry["latest_end"] = end

    def hour_to_time_str(hour):
        """Convert decimal hour to readable time string (e.g., 7 -> '7:00 AM')."""
        h = int(hour)
        m = int((hour - h) * 60)
        if h == 0:
            return f"12:{m:02d} AM"
        elif h < 12:
            return f"{h}:{m:02d} AM"
        elif h == 12:
            return f"12:{m:02d} PM"
        else:
            return f"{h - 12}:{m:02d} PM"

    result = []

    for fid, info in faculty_days.items():
        fname = info["faculty_name"]
        emp_type = info["employment_type"]
        days_data = info["days"]
        teaching_days = [d for d in DAYS if d in days_data]

        if not teaching_days:
            continue

        if emp_type.lower() == "full time":
            # Full-time: distribute FULL_TIME_WEEKLY_HOURS across all weekdays
            # time_in = first class (or padded earlier), time_out = last class (or padded later)
            all_weekdays = list(DAYS)
            target_weekly = FULL_TIME_WEEKLY_HOURS

            # Compute minimum hours locked by class spans (can't go below these)
            day_class_span = {}
            for d in all_weekdays:
                if d in days_data:
                    day_class_span[d] = days_data[d]["latest_end"] - days_data[d]["earliest_start"]
                else:
                    day_class_span[d] = 0

            locked_hours = sum(max(s, 0) for s in day_class_span.values())
            remaining_to_distribute = max(target_weekly - locked_hours, 0)

            # Start each day at its class span minimum
            daily_targets = {d: max(day_class_span[d], 0) for d in all_weekdays}

            # Distribute remaining hours 1 at a time to days with fewest hours (balanced)
            while remaining_to_distribute > 0:
                min_hrs = min(daily_targets[d] for d in all_weekdays)
                candidates = [d for d in all_weekdays if daily_targets[d] == min_hrs]
                random.shuffle(candidates)
                for d in candidates:
                    if remaining_to_distribute <= 0:
                        break
                    daily_targets[d] += 1
                    remaining_to_distribute -= 1

            faculty_entry = {
                "faculty_id": fid,
                "faculty_name": fname,
                "employment_type": emp_type,
                "weekly_hours": target_weekly,
                "schedule": []
            }

            for day in all_weekdays:
                target_hrs = daily_targets[day]

                if day in days_data:
                    earliest = days_data[day]["earliest_start"]
                    latest = days_data[day]["latest_end"]
                    class_span = latest - earliest

                    if class_span >= target_hrs:
                        time_in = earliest
                        time_out = latest
                    else:
                        # Expand around class window to reach target
                        extra = target_hrs - class_span
                        add_before = min(extra, max(earliest - START_HOUR, 0))
                        add_after = extra - add_before
                        time_in = earliest - add_before
                        time_out = latest + add_after
                        if time_out > END_HOUR:
                            overflow = time_out - END_HOUR
                            time_out = END_HOUR
                            time_in = max(START_HOUR, time_in - overflow)
                else:
                    # No classes this day — assign a default block
                    time_in = START_HOUR
                    time_out = START_HOUR + target_hrs
                    if time_out > END_HOUR:
                        time_out = END_HOUR

                actual_hours = time_out - time_in

                faculty_entry["schedule"].append({
                    "day": day,
                    "time_in": hour_to_time_str(time_in),
                    "time_out": hour_to_time_str(time_out),
                    "hours": actual_hours,
                    "has_classes": day in days_data
                })

            result.append(faculty_entry)

        else:
            # Part-time: time_in = first class, time_out = last class (no padding)
            faculty_entry = {
                "faculty_id": fid,
                "faculty_name": fname,
                "employment_type": emp_type,
                "weekly_hours": sum(
                    days_data[d]["latest_end"] - days_data[d]["earliest_start"]
                    for d in teaching_days
                ),
                "schedule": []
            }

            for day in DAYS:
                if day not in days_data:
                    continue
                time_in = days_data[day]["earliest_start"]
                time_out = days_data[day]["latest_end"]
                faculty_entry["schedule"].append({
                    "day": day,
                    "time_in": hour_to_time_str(time_in),
                    "time_out": hour_to_time_str(time_out),
                    "hours": time_out - time_in,
                    "has_classes": True
                })

            result.append(faculty_entry)

    # Sort by faculty name
    result.sort(key=lambda x: x["faculty_name"])
    return result


def build_faculty_with_multiple_branches(complete_schedule, branch_map):
    """
    Identify faculty members who teach at more than one branch.
    Returns a dict keyed by faculty_name, each value containing branch details.
    """
    if not branch_map:
        branch_map = {}

    # Collect per-faculty: which branches they teach at, and which days/courses per branch
    faculty_branches = {}
    for meeting in complete_schedule:
        fid = meeting.get("faculty_id")
        fname = meeting.get("faculty_name", "Unknown")
        branch_id = meeting.get("college_branch_id")
        if branch_id is None:
            continue

        branch_name = branch_map.get(branch_id, f"Branch {branch_id}")

        if fid not in faculty_branches:
            faculty_branches[fid] = {"faculty_name": fname, "branches": {}}

        if branch_name not in faculty_branches[fid]["branches"]:
            faculty_branches[fid]["branches"][branch_name] = {
                "branch_id": branch_id,
                "days": set(),
                "courses": set(),
                "total_meetings": 0
            }

        faculty_branches[fid]["branches"][branch_name]["days"].add(meeting.get("day"))
        faculty_branches[fid]["branches"][branch_name]["courses"].add(meeting.get("course_code"))
        faculty_branches[fid]["branches"][branch_name]["total_meetings"] += 1

    # Filter to only faculty with multiple branches
    result = {}
    for fid, data in faculty_branches.items():
        if len(data["branches"]) > 1:
            fname = data["faculty_name"]
            result[fname] = {}
            for branch_name, info in data["branches"].items():
                result[fname][branch_name] = {
                    "branch_id": info["branch_id"],
                    "days": sorted(list(info["days"]),
                                   key=lambda d: ["Monday", "Tuesday", "Wednesday",
                                                   "Thursday", "Friday", "Saturday", "Sunday"].index(d)
                                   if d in ["Monday", "Tuesday", "Wednesday",
                                            "Thursday", "Friday", "Saturday", "Sunday"] else 99),
                    "courses": sorted(list(info["courses"])),
                    "total_meetings": info["total_meetings"]
                }

    return result


def save_faculty_core_time_to_json(core_time_data, filename, complete_schedule=None, branch_map=None):
    """
    Save faculty core time schedule to a JSON file.
    Includes faculty_with_multiple_branches if schedule data is provided.
    """
    output = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_faculty": len(core_time_data),
            "full_time_weekly_target": FULL_TIME_WEEKLY_HOURS
        },
        "faculty_schedules": core_time_data
    }

    # Add faculty with multiple branches if schedule data is available
    if complete_schedule is not None:
        multi_branch = build_faculty_with_multiple_branches(complete_schedule, branch_map or {})
        output["faculty_with_multiple_branches"] = multi_branch
        output["metadata"]["faculty_with_multiple_branches_count"] = len(multi_branch)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False, default=str)

    print(f"[INFO] Faculty core time schedule saved to: {filename}")
    if complete_schedule is not None and multi_branch:
        print(f"[INFO] Faculty with multiple branches: {len(multi_branch)}")
        for fname, branches in multi_branch.items():
            branch_names = list(branches.keys())
            print(f"  - {fname}: {', '.join(branch_names)}")


def create_schedule(faculty_loads, rooms, branch_map=None):
    """
    Create a complete schedule for all faculty loads.
    Scheduling rules:
    - Lecture: 1 student unit = 1 contact hour = 1 teacher unit
    - Laboratory: 1 student unit = 3 contact hours = 2.25 teacher units (3 × 0.75)
    - Classes meet on day patterns (TTH, MF, or MWF) with hours split equally
    - Pattern chosen dynamically: must have >= 1h per meeting, least-used first
    - Lecture and lab are scheduled consecutively (lecture first, then lab)
    - Wednesday standalone is fallback only (full hours, not split)

    Returns scheduled classes and unscheduled meetings.
    """
    schedule_tracker = {}  # Track room schedules
    faculty_schedule_tracker = {}  # Track faculty schedules
    class_schedule_tracker = {}  # Track class section schedules to prevent self-conflicts
    # Track lecture hours for f2f/online percentage distribution
    lecture_type_tracker = {"face_to_face_hours": 0.0, "online_hours": 0.0, "total_lecture_hours": 0.0}
    # Track day pattern usage for fair distribution
    day_pattern_tracker = {name: 0 for name in DAY_PATTERNS}
    # Track per-day f2f assignment count so no single day always gets f2f
    day_f2f_tracker = {}
    faculty_lecture_type_tracker = {}  # per-faculty f2f/online hour tracking
    faculty_branch_tracker = {}
    # Pre-compute which branches are "far" (round-trip travel > FAR_BRANCH_ROUND_TRIP_LIMIT)
    far_branch_set = set()
    seen_branches = set()
    for room in rooms:
        bid = room.get("branch_id")
        if bid and bid not in seen_branches:
            seen_branches.add(bid)
            if is_far_branch(rooms, bid):
                far_branch_set.add(bid)
    if far_branch_set:
        far_names = [branch_map.get(b, f"Branch {b}") if branch_map else f"Branch {b}" for b in far_branch_set]
        print(f"[INFO] Far branches (full-day only): {', '.join(far_names)}")
    complete_schedule = []
    unscheduled_meetings = []

    # ----------------------------------------------------------
    # DAPECOL scheduling: assign a 2-day pair per program
    # One day = face-to-face at DAPECOL (all faculty same day)
    # Other day = online (faculty stays at Main/home)
    # Only 2-day patterns allowed (MW, TTH, MF, WF — not MWF)
    # ----------------------------------------------------------
    # Available 2-day patterns for DAPECOL (exclude MWF and any 3+ day patterns)
    DAPECOL_PATTERNS = {k: v for k, v in DAY_PATTERNS.items() if len(v) == 2}
    dapecol_program_pattern = {}  # program_id → {"pattern_days": [...], "f2f_day": ..., "online_day": ...}
    dapecol_programs_seen = {}  # program_id → list of (fid, finfo, cls)
    for fid, finfo in faculty_loads.items():
        for cls in finfo.get("assigned_classes", []):
            if cls.get("branch_id") == DAPECOL_BRANCH_ID:
                pid = cls.get("program_id")
                if pid not in dapecol_programs_seen:
                    dapecol_programs_seen[pid] = []
                dapecol_programs_seen[pid].append((fid, finfo, cls))

    if dapecol_programs_seen:
        # ALL DAPECOL programs share the SAME single day pair
        pattern_names = list(DAPECOL_PATTERNS.keys())
        chosen_pattern = pattern_names[0]  # Use first 2-day pattern for all DAPECOL
        pdays = DAPECOL_PATTERNS[chosen_pattern]
        f2f_day = pdays[0]     # first day = face-to-face at DAPECOL
        online_day = pdays[1]  # second day = online
        print(f"[INFO] DAPECOL day pair: {chosen_pattern} (f2f={f2f_day}, online={online_day})")

        for pid in sorted(dapecol_programs_seen.keys()):
            dapecol_program_pattern[pid] = {
                "pattern_name": chosen_pattern,
                "pattern_days": pdays,
                "f2f_day": f2f_day,
                "online_day": online_day,
            }
            entries = dapecol_programs_seen[pid]
            pcode = entries[0][2].get("program_code", "?")
            level = entries[0][2].get("course_level", "?")
            print(f"  DAPECOL {pcode}-{level}: {len(entries)} courses")

    print("\n" + "="*80)
    print(" " * 25 + "STARTING SCHEDULING PROCESS")
    print("="*80)
    print("Scheduling Rules:")
    print("  - Lecture: 1 student unit = 1 contact hour per week")
    print("  - Laboratory: 1 student unit = 3 contact hours per week")
    print("  - Teacher Units: Lecture 1:1, Lab 1:2.25")
    print("  - Primary: Classes meet on day patterns (TTH, MF, WF, or MWF)")
    print("  - Pattern valid only if weekly_hours / num_meetings >= 1h per meeting")
    print("  - Hours SPLIT equally between meetings of the chosen pattern")
    print("  - Fallback: Wednesday scheduling with FULL hours (not split)")
    print("  - Lecture and lab scheduled consecutively in each meeting")
    print("  - Faculty daily workload limit: Max 8 hours per day")
    print("  - Part-time faculty: Scheduled from 5:00 PM to 10:00 PM only")
    print("  - Full-time faculty: Scheduled anytime (7:00 AM to 9:00 PM)")
    print("  - Laboratory classes MUST be face-to-face")
    print("  - DAPECOL: 2-day pair, 1 day f2f + 1 day online (all faculty same f2f day)")
    print(f"  - Lecture f2f target: {int(TARGET_FACE_TO_FACE_PERCENTAGE * 100)}% per meeting day "
          f"(e.g. MF: 1 day f2f + 1 online; MWF: 1 day f2f + 2 online at 30%)")
    print("  - Day patterns and time slots are RANDOMIZED for fair distribution")
    print("="*80)

    # Shuffle faculty order for fair distribution
    faculty_items = list(faculty_loads.items())
    random.shuffle(faculty_items)

    # ==========================================================
    # PHASE 1: Schedule DAPECOL classes (2-day pair: 1 f2f + 1 online)
    # All faculty for the same program go to DAPECOL on the SAME
    # f2f day. The other day in the pair is online.
    # ==========================================================
    dapecol_scheduled_keys = set()  # track (faculty_id, class_id, course_code) to skip in Phase 2

    if dapecol_program_pattern:
        print("\n--- DAPECOL 2-Day Pair Scheduling ---")
        for pid, pat_info in dapecol_program_pattern.items():
            f2f_day = pat_info["f2f_day"]
            online_day = pat_info["online_day"]
            pattern_days = pat_info["pattern_days"]
            entries = dapecol_programs_seen.get(pid, [])

            if not entries:
                continue

            pcode = entries[0][2].get("program_code", "?")
            level = entries[0][2].get("course_level", "?")
            print(f"  DAPECOL {pcode}-{level}: f2f={f2f_day}, online={online_day} ({len(entries)} courses)")

            for faculty_id, faculty_info, cls in entries:
                faculty_name = faculty_info["faculty_name"]
                employment_type = faculty_info.get("employment_type", "full time")
                institute_id = cls.get("institute_id")
                class_size = cls.get("class_size", 30)
                class_branch_id = cls.get("branch_id")
                class_id = cls["class_id"]

                lecture_units = cls.get("course_lec", 0)
                lab_units = cls.get("course_lab", 0)
                total_weekly_hours = lecture_units * LECTURE_UNIT_TO_HOUR + lab_units * LAB_UNIT_TO_HOUR

                if total_weekly_hours <= 0:
                    continue

                # Split hours across 2 days (may be uneven)
                hours_per_day = total_weekly_hours / 2
                short_h = int(hours_per_day)
                if short_h < hours_per_day:
                    # Uneven: give f2f day more hours
                    f2f_hours = short_h + 1
                    online_hours = int(total_weekly_hours - f2f_hours)
                else:
                    f2f_hours = short_h
                    online_hours = short_h

                # Determine start/end hours
                if employment_type.lower() == "part time":
                    sched_start = PART_TIME_START_HOUR
                    sched_end = PART_TIME_END_HOUR
                else:
                    sched_start = START_HOUR
                    sched_end = END_HOUR

                # --- Schedule FACE-TO-FACE day at DAPECOL ---
                f2f_next_start = get_faculty_next_start_hour(
                    faculty_id, f2f_day, faculty_schedule_tracker, sched_start)
                f2f_slots = find_available_slots(f2f_next_start, sched_end, f2f_hours)

                f2f_scheduled = False
                fail_reason = "No available time slots on DAPECOL f2f day"

                for start_hour in f2f_slots:
                    if not is_faculty_available(faculty_id, f2f_day, start_hour,
                                               f2f_hours, faculty_schedule_tracker):
                        fail_reason = "Faculty time conflict on DAPECOL f2f day"
                        continue
                    if get_faculty_daily_hours(faculty_id, f2f_day, faculty_schedule_tracker) + f2f_hours > 8:
                        fail_reason = "Faculty daily workload limit exceeded"
                        continue
                    if not check_daily_span_ok(faculty_id, f2f_day, start_hour, f2f_hours, faculty_schedule_tracker):
                        fail_reason = f"Faculty daily span would exceed {MAX_DAILY_SPAN_HOURS} hours"
                        continue
                    if not is_class_available(class_id, f2f_day, start_hour,
                                             f2f_hours, class_schedule_tracker):
                        fail_reason = "Class section time conflict on f2f day"
                        continue

                    # Find room at DAPECOL
                    lec_room = find_suitable_room(rooms, "Lecture", institute_id, class_size,
                                                   f2f_day, start_hour, f2f_hours,
                                                   schedule_tracker, class_branch_id)
                    if not lec_room:
                        fail_reason = "No available room at DAPECOL"
                        continue

                    # F2F day booked — record it
                    lec_room_id = lec_room["room_id"]
                    if lec_room_id not in schedule_tracker:
                        schedule_tracker[lec_room_id] = {}
                    if f2f_day not in schedule_tracker[lec_room_id]:
                        schedule_tracker[lec_room_id][f2f_day] = []
                    schedule_tracker[lec_room_id][f2f_day].append({
                        "start_hour": start_hour, "duration": f2f_hours,
                        "class_id": class_id, "course_code": cls["course_code"]
                    })

                    if faculty_id not in faculty_schedule_tracker:
                        faculty_schedule_tracker[faculty_id] = {}
                    if f2f_day not in faculty_schedule_tracker[faculty_id]:
                        faculty_schedule_tracker[faculty_id][f2f_day] = []
                    faculty_schedule_tracker[faculty_id][f2f_day].append({
                        "start_hour": start_hour, "duration": f2f_hours,
                        "class_id": class_id, "course_code": cls["course_code"],
                        "building_name": lec_room.get("building_name"),
                        "travel_time": lec_room.get("time_travel", 0)
                    })

                    if class_id not in class_schedule_tracker:
                        class_schedule_tracker[class_id] = {}
                    if f2f_day not in class_schedule_tracker[class_id]:
                        class_schedule_tracker[class_id][f2f_day] = []
                    class_schedule_tracker[class_id][f2f_day].append({
                        "start_hour": start_hour, "duration": f2f_hours,
                        "faculty_id": faculty_id, "course_code": cls["course_code"]
                    })

                    update_branch_tracker(faculty_id, [f2f_day], DAPECOL_BRANCH_ID, faculty_branch_tracker)

                    complete_schedule.append({
                        "class_id": class_id, "set_name": cls["set_name"],
                        "course_level": cls["course_level"], "course_code": cls["course_code"],
                        "program_id": cls["program_id"],
                        "program_name": cls.get("program_name", "Unknown"),
                        "program_code": cls.get("program_code", "Unknown"),
                        "institute_id": institute_id, "type": "Lecture",
                        "day": f2f_day, "start_hour": start_hour,
                        "duration": f2f_hours,
                        "time_slot": format_time_slot(start_hour, f2f_hours),
                        "room_id": lec_room_id, "room_name": lec_room.get("room_name", "Unknown"),
                        "room_type": lec_room.get("room_type", "Unknown"),
                        "room_capacity": lec_room.get("room_capacity", 0),
                        "class_size": class_size, "schedule_type": "face to face",
                        "faculty_id": faculty_id, "faculty_name": faculty_name,
                        "employment_type": employment_type,
                        "college_branch_id": DAPECOL_BRANCH_ID
                    })

                    lecture_type_tracker["face_to_face_hours"] += f2f_hours
                    lecture_type_tracker["total_lecture_hours"] += f2f_hours

                    print(f"    {cls['course_code']} -> {faculty_name} f2f {f2f_day} @ {format_time_slot(start_hour, f2f_hours)} [OK]")
                    f2f_scheduled = True
                    break

                if not f2f_scheduled:
                    print(f"    {cls['course_code']} -> {faculty_name} [FAILED f2f: {fail_reason}]")
                    unscheduled_meetings.append({
                        "class_id": class_id, "course_code": cls["course_code"],
                        "course_id": cls.get("course_id"), "institute_id": institute_id,
                        "class_size": class_size, "faculty_name": faculty_name,
                        "program_id": cls["program_id"],
                        "program_name": cls.get("program_name", "Unknown"),
                        "program_code": cls.get("program_code", "Unknown"),
                        "type": "Lecture", "hours": f"{total_weekly_hours}h (DAPECOL)",
                        "reason": fail_reason
                    })
                    dapecol_scheduled_keys.add((faculty_id, class_id, cls["course_code"]))
                    continue

                # --- Schedule ONLINE day ---
                online_next_start = get_faculty_next_start_hour(
                    faculty_id, online_day, faculty_schedule_tracker, sched_start)
                online_slots = find_available_slots(online_next_start, sched_end, online_hours)

                online_scheduled = False
                for ostart in online_slots:
                    if not is_faculty_available(faculty_id, online_day, ostart,
                                               online_hours, faculty_schedule_tracker):
                        continue
                    if get_faculty_daily_hours(faculty_id, online_day, faculty_schedule_tracker) + online_hours > 8:
                        continue
                    if not is_class_available(class_id, online_day, ostart,
                                             online_hours, class_schedule_tracker):
                        continue

                    # Online — no room needed
                    if faculty_id not in faculty_schedule_tracker:
                        faculty_schedule_tracker[faculty_id] = {}
                    if online_day not in faculty_schedule_tracker[faculty_id]:
                        faculty_schedule_tracker[faculty_id][online_day] = []
                    faculty_schedule_tracker[faculty_id][online_day].append({
                        "start_hour": ostart, "duration": online_hours,
                        "class_id": class_id, "course_code": cls["course_code"],
                        "building_name": None, "travel_time": 0
                    })

                    if online_day not in class_schedule_tracker.get(class_id, {}):
                        if class_id not in class_schedule_tracker:
                            class_schedule_tracker[class_id] = {}
                        class_schedule_tracker[class_id][online_day] = []
                    class_schedule_tracker[class_id][online_day].append({
                        "start_hour": ostart, "duration": online_hours,
                        "faculty_id": faculty_id, "course_code": cls["course_code"]
                    })

                    complete_schedule.append({
                        "class_id": class_id, "set_name": cls["set_name"],
                        "course_level": cls["course_level"], "course_code": cls["course_code"],
                        "program_id": cls["program_id"],
                        "program_name": cls.get("program_name", "Unknown"),
                        "program_code": cls.get("program_code", "Unknown"),
                        "institute_id": institute_id, "type": "Lecture",
                        "day": online_day, "start_hour": ostart,
                        "duration": online_hours,
                        "time_slot": format_time_slot(ostart, online_hours),
                        "room_id": None, "room_name": "Online",
                        "room_type": "Online", "room_capacity": 0,
                        "class_size": class_size, "schedule_type": "online",
                        "faculty_id": faculty_id, "faculty_name": faculty_name,
                        "employment_type": employment_type,
                        "college_branch_id": DAPECOL_BRANCH_ID
                    })

                    lecture_type_tracker["online_hours"] += online_hours
                    lecture_type_tracker["total_lecture_hours"] += online_hours

                    print(f"    {cls['course_code']} -> {faculty_name} online {online_day} @ {format_time_slot(ostart, online_hours)} [OK]")
                    online_scheduled = True
                    break

                if not online_scheduled:
                    print(f"    {cls['course_code']} -> {faculty_name} online day [FAILED]")

                # Mark as handled so Phase 2 skips it
                dapecol_scheduled_keys.add((faculty_id, class_id, cls["course_code"]))

        print("--- End DAPECOL Scheduling ---\n")

    # ==========================================================
    # PHASE 2: Schedule all other classes (normal pattern-based)
    # ==========================================================
    # Process each faculty's assigned classes
    for faculty_id, faculty_info in faculty_items:
        faculty_name = faculty_info["faculty_name"]
        employment_type = faculty_info.get("employment_type", "full time")
        preferred_time = faculty_info.get("preferred_time", [])

        if len(faculty_info["assigned_classes"]) == 0:
            continue

        # Filter out DAPECOL classes already scheduled in Phase 1
        classes_to_schedule = [
            cls for cls in faculty_info["assigned_classes"]
            if (faculty_id, cls["class_id"], cls["course_code"]) not in dapecol_scheduled_keys
        ]

        if not classes_to_schedule:
            continue

        print(
            f"\nScheduling classes for: {faculty_name} (ID: {faculty_id}) [{employment_type.title()}]")

        # Shuffle classes for fair distribution
        random.shuffle(classes_to_schedule)

        for cls in classes_to_schedule:
            lecture_units = cls.get("course_lec", 0)
            lab_units = cls.get("course_lab", 0)

            # Convert to contact hours per week
            lecture_hours_per_week = lecture_units * LECTURE_UNIT_TO_HOUR
            lab_hours_per_week = lab_units * LAB_UNIT_TO_HOUR

            # Determine scheduling strategy
            if lecture_units > 0 and lab_units > 0:
                # Course has both lecture and lab
                print(
                    f"  Scheduling {cls['course_code']} (Lec: {lecture_units}u={lecture_hours_per_week}h/wk + Lab: {lab_units}u={lab_hours_per_week}h/wk)...", end=" ")
                scheduled_meetings = schedule_class_with_lab(
                    cls, rooms, faculty_id, employment_type,
                    schedule_tracker, faculty_schedule_tracker, unscheduled_meetings, class_schedule_tracker,
                    day_pattern_tracker, preferred_time, faculty_branch_tracker,
                    far_branch_set
                )

                if scheduled_meetings:
                    for meeting in scheduled_meetings:
                        meeting["faculty_id"] = faculty_id
                        meeting["faculty_name"] = faculty_name
                        meeting["employment_type"] = employment_type
                        meeting["college_branch_id"] = cls.get("branch_id")
                        complete_schedule.append(meeting)
                    print("[OK] Scheduled")
                else:
                    print("[FAILED]")

            elif lecture_units > 0:
                # Course has only lecture
                print(
                    f"  Scheduling {cls['course_code']} (Lecture only: {lecture_units}u={lecture_hours_per_week}h/wk)...", end=" ")
                scheduled_meetings = schedule_lecture_only(
                    cls, rooms, faculty_id, employment_type,
                    schedule_tracker, faculty_schedule_tracker, unscheduled_meetings, class_schedule_tracker,
                    lecture_type_tracker, day_pattern_tracker, preferred_time, faculty_branch_tracker,
                    day_f2f_tracker, far_branch_set, faculty_lecture_type_tracker
                )

                if scheduled_meetings:
                    for meeting in scheduled_meetings:
                        meeting["faculty_id"] = faculty_id
                        meeting["faculty_name"] = faculty_name
                        meeting["employment_type"] = employment_type
                        meeting["college_branch_id"] = cls.get("branch_id")
                        complete_schedule.append(meeting)
                    print("[OK] Scheduled")
                else:
                    print("[FAILED]")

            elif lab_units > 0:
                # Course has only lab (unusual, but handle it)
                print(
                    f"  Scheduling {cls['course_code']} (Lab only: {lab_units}u={lab_hours_per_week}h/wk)...", end=" ")
                # Treat lab-only as lecture for scheduling purposes
                scheduled_meetings = schedule_lecture_only(
                    cls, rooms, faculty_id, employment_type,
                    schedule_tracker, faculty_schedule_tracker, unscheduled_meetings, class_schedule_tracker,
                    lecture_type_tracker, day_pattern_tracker, preferred_time, faculty_branch_tracker,
                    day_f2f_tracker, far_branch_set, faculty_lecture_type_tracker
                )

                if scheduled_meetings:
                    # Change type to Laboratory
                    for meeting in scheduled_meetings:
                        meeting["type"] = "Laboratory"
                        meeting["faculty_id"] = faculty_id
                        meeting["faculty_name"] = faculty_name
                        meeting["employment_type"] = employment_type
                        meeting["college_branch_id"] = cls.get("branch_id")
                        complete_schedule.append(meeting)
                    print("[OK] Scheduled")
                else:
                    print("[FAILED]")

    print("\n" + "="*80)
    print(f"Scheduling Complete: {len(complete_schedule)} meetings scheduled, "
          f"{len(unscheduled_meetings)} unscheduled")
    print("-"*80)
    total_lecture_hours = lecture_type_tracker["total_lecture_hours"]
    if total_lecture_hours > 0:
        f2f_hours = lecture_type_tracker["face_to_face_hours"]
        online_hours = lecture_type_tracker["online_hours"]
        f2f_pct = (f2f_hours / total_lecture_hours) * 100
        online_pct = (online_hours / total_lecture_hours) * 100
        print(f"Lecture Distribution: {f2f_hours:.1f}h face-to-face ({f2f_pct:.1f}%), "
              f"{online_hours:.1f}h online ({online_pct:.1f}%) "
              f"[Target: {int(TARGET_FACE_TO_FACE_PERCENTAGE * 100)}% f2f]")
    print("-"*80)
    # Show day pattern distribution
    pattern_counts = {name: day_pattern_tracker.get(name, 0) for name in DAY_PATTERNS}
    # Count fallback-only schedules from complete_schedule
    fallback_only_classes = set()
    for m in complete_schedule:
        if m["day"] == FALLBACK_DAY:
            fallback_only_classes.add(m["class_id"])
    # Remove classes that also appear on other days (those are multi-day patterns, not fallback-only)
    for m in complete_schedule:
        if m["day"] != FALLBACK_DAY:
            fallback_only_classes.discard(m["class_id"])
    fallback_count = len(fallback_only_classes)
    total_patterns = sum(pattern_counts.values()) + fallback_count
    if total_patterns > 0:
        dist_parts = [f"{name}: {count}" for name, count in pattern_counts.items()]
        dist_parts.append(f"{FALLBACK_DAY[:3]}-only: {fallback_count}")
        print(f"Day Distribution: {', '.join(dist_parts)}")
    # Show per-day f2f assignment counts (fairness audit)
    if day_f2f_tracker:
        f2f_summary = ", ".join(
            f"{d[:3]}: {day_f2f_tracker[d]}"
            for d in DAYS if d in day_f2f_tracker and day_f2f_tracker[d] > 0
        )
        if f2f_summary:
            print(f"  F2F meetings per day: {f2f_summary}")

    # Validate schedule for conflicts
    print("-"*80)
    print("Validating schedule for conflicts...")
    conflicts = validate_schedule(complete_schedule)
    if conflicts:
        print(f"WARNING: Found {len(conflicts)} conflicts:")
        for conflict in conflicts[:10]:  # Show first 10 conflicts
            print(f"  - {conflict}")
        if len(conflicts) > 10:
            print(f"  ... and {len(conflicts) - 10} more conflicts")
    else:
        print("No conflicts detected!")
    print("="*80)

    # Build schedule_by_room: group schedule entries by room name, sorted chronologically
    schedule_by_room = {}
    day_order = {d: i for i, d in enumerate(DAYS)}
    for entry in complete_schedule:
        room_name = entry.get("room_name", "Online")
        if room_name not in schedule_by_room:
            schedule_by_room[room_name] = []
        schedule_by_room[room_name].append({
            "day_time": f"{entry['day']} {entry['time_slot']}",
            "faculty_name": entry.get("faculty_name", "Unknown"),
            "class_name": entry.get("set_name", "Unknown"),
            "course_code": entry.get("course_code", "Unknown"),
            "program_code": entry.get("program_code", "Unknown"),
            "_sort_day": day_order.get(entry["day"], 99),
            "_sort_hour": entry.get("start_hour", 0)
        })
    # Sort each room's entries by day then start hour, and remove sort keys
    for room_name in schedule_by_room:
        schedule_by_room[room_name].sort(key=lambda x: (x["_sort_day"], x["_sort_hour"]))
        for item in schedule_by_room[room_name]:
            del item["_sort_day"]
            del item["_sort_hour"]

    # Build schedule_by_branch: group schedule entries by branch name, sorted chronologically
    if branch_map is None:
        branch_map = {}
    schedule_by_branch = {}
    for entry in complete_schedule:
        branch_id = entry.get("college_branch_id")
        branch_name = branch_map.get(branch_id, f"Branch {branch_id}") if branch_id else "Unassigned"
        if branch_name not in schedule_by_branch:
            schedule_by_branch[branch_name] = []
        schedule_by_branch[branch_name].append({
            "class_id": entry.get("class_id"),
            "set_name": entry.get("set_name", "Unknown"),
            "course_code": entry.get("course_code", "Unknown"),
            "program_code": entry.get("program_code", "Unknown"),
            "faculty_name": entry.get("faculty_name", "Unknown"),
            "type": entry.get("type", "Unknown"),
            "day": entry.get("day"),
            "start_hour": entry.get("start_hour", 0),
            "duration": entry.get("duration", 0),
            "time_slot": entry.get("time_slot", "Unknown"),
            "room_name": entry.get("room_name", "Online"),
            "schedule_type": entry.get("schedule_type", "Unknown"),
            "_sort_day": day_order.get(entry.get("day", ""), 99),
            "_sort_hour": entry.get("start_hour", 0)
        })
    # Sort each branch's entries by day then start hour, and remove sort keys
    for branch_name in schedule_by_branch:
        schedule_by_branch[branch_name].sort(key=lambda x: (x["_sort_day"], x["_sort_hour"]))
        for item in schedule_by_branch[branch_name]:
            del item["_sort_day"]
            del item["_sort_hour"]

    return complete_schedule, unscheduled_meetings, schedule_by_room, schedule_by_branch


def validate_schedule(schedule):
    """
    Validate the schedule for conflicts:
    - Same class_id at same day/time
    - Same room at same day/time (excluding online)
    - Same faculty at same day/time
    Returns list of conflict descriptions.
    """
    conflicts = []

    # Group by day
    for day in DAYS:
        day_schedule = [m for m in schedule if m["day"] == day]

        # Check for class conflicts (same class_id at overlapping times)
        class_groups = {}
        for meeting in day_schedule:
            class_id = meeting["class_id"]
            if class_id not in class_groups:
                class_groups[class_id] = []
            class_groups[class_id].append(meeting)

        for class_id, meetings in class_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append(
                                f"Class conflict: {m1['course_code']} (class_id={class_id}) "
                                f"on {day} at {m1['time_slot']} and {m2['time_slot']}"
                            )

        # Check for room conflicts (same room at overlapping times, excluding online)
        room_groups = {}
        for meeting in day_schedule:
            room_id = meeting.get("room_id")
            if room_id is None:  # Skip online classes
                continue
            if room_id not in room_groups:
                room_groups[room_id] = []
            room_groups[room_id].append(meeting)

        for room_id, meetings in room_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append(
                                f"Room conflict: {m1['room_name']} (room_id={room_id}) "
                                f"on {day} at {m1['time_slot']} ({m1['course_code']}) "
                                f"and {m2['time_slot']} ({m2['course_code']})"
                            )

        # Check for faculty conflicts (same faculty at overlapping times)
        faculty_groups = {}
        for meeting in day_schedule:
            faculty_id = meeting.get("faculty_id")
            if faculty_id is None:
                continue
            if faculty_id not in faculty_groups:
                faculty_groups[faculty_id] = []
            faculty_groups[faculty_id].append(meeting)

        for faculty_id, meetings in faculty_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append(
                                f"Faculty conflict: {m1['faculty_name']} (faculty_id={faculty_id}) "
                                f"on {day} at {m1['time_slot']} ({m1['course_code']}) "
                                f"and {m2['time_slot']} ({m2['course_code']})"
                            )

    return conflicts


def validate_schedule_detailed(schedule):
    """
    Validate the schedule for conflicts and return detailed conflict data for Excel export.
    Returns list of conflict dictionaries with structured data.
    """
    conflicts = []

    # Group by day
    for day in DAYS:
        day_schedule = [m for m in schedule if m["day"] == day]

        # Check for class conflicts (same class_id at overlapping times)
        class_groups = {}
        for meeting in day_schedule:
            class_id = meeting["class_id"]
            if class_id not in class_groups:
                class_groups[class_id] = []
            class_groups[class_id].append(meeting)

        for class_id, meetings in class_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append({
                                "type": "Class Conflict",
                                "day": day,
                                "time_slot_1": m1["time_slot"],
                                "time_slot_2": m2["time_slot"],
                                "course_1": m1["course_code"],
                                "course_2": m2["course_code"],
                                "resource": f"Class Section",
                                "resource_id": class_id,
                                "details": f"Same class section scheduled at overlapping times"
                            })

        # Check for room conflicts (same room at overlapping times, excluding online)
        room_groups = {}
        for meeting in day_schedule:
            room_id = meeting.get("room_id")
            if room_id is None:  # Skip online classes
                continue
            if room_id not in room_groups:
                room_groups[room_id] = []
            room_groups[room_id].append(meeting)

        for room_id, meetings in room_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append({
                                "type": "Room Conflict",
                                "day": day,
                                "time_slot_1": m1["time_slot"],
                                "time_slot_2": m2["time_slot"],
                                "course_1": m1["course_code"],
                                "course_2": m2["course_code"],
                                "resource": m1.get("room_name", "Unknown"),
                                "resource_id": room_id,
                                "details": f"Same room double-booked at overlapping times"
                            })

        # Check for faculty conflicts (same faculty at overlapping times)
        faculty_groups = {}
        for meeting in day_schedule:
            faculty_id = meeting.get("faculty_id")
            if faculty_id is None:
                continue
            if faculty_id not in faculty_groups:
                faculty_groups[faculty_id] = []
            faculty_groups[faculty_id].append(meeting)

        for faculty_id, meetings in faculty_groups.items():
            if len(meetings) > 1:
                for i in range(len(meetings)):
                    for j in range(i + 1, len(meetings)):
                        m1, m2 = meetings[i], meetings[j]
                        if check_time_overlap(m1["start_hour"], m1["duration"],
                                              m2["start_hour"], m2["duration"]):
                            conflicts.append({
                                "type": "Faculty Conflict",
                                "day": day,
                                "time_slot_1": m1["time_slot"],
                                "time_slot_2": m2["time_slot"],
                                "course_1": m1["course_code"],
                                "course_2": m2["course_code"],
                                "resource": m1.get("faculty_name", "Unknown"),
                                "resource_id": faculty_id,
                                "details": f"Same faculty assigned to overlapping classes"
                            })

    return conflicts


def save_schedule_to_text(schedule, unscheduled, filename):
    """Save schedule to a readable text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("="*100 + "\n")
        f.write(" " * 35 + "CLASS SCHEDULE\n")
        f.write("="*100 + "\n")
        f.write(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total Scheduled Meetings: {len(schedule)}\n")
        f.write(f"Total Unscheduled Meetings: {len(unscheduled)}\n")
        f.write("="*100 + "\n\n")

        # Group by day
        for day in DAYS:
            day_schedule = [s for s in schedule if s["day"] == day]

            if not day_schedule:
                continue

            f.write("\n" + "="*100 + "\n")
            f.write(f" {day.upper()}\n")
            f.write("="*100 + "\n\n")

            # Sort by time
            day_schedule.sort(key=lambda x: x["start_hour"])

            for entry in day_schedule:
                f.write("-"*100 + "\n")
                f.write(f"Time        : {entry['time_slot']}\n")
                f.write(f"Course      : {entry['course_code']}\n")
                f.write(f"Type        : {entry['type']}\n")
                f.write(
                    f"Faculty     : {entry['faculty_name']} (ID: {entry['faculty_id']}) [{entry.get('employment_type', 'N/A')}]\n")
                f.write(
                    f"Room        : {entry['room_name']} (ID: {entry['room_id']})\n")
                f.write(f"Room Type   : {entry['room_type']}\n")
                f.write(
                    f"Capacity    : {entry['room_capacity']} (Class Size: {entry['class_size']})\n")
                f.write(f"Program ID  : {entry['program_id']}\n")
                f.write(f"Institute ID: {entry['institute_id']}\n")
                f.write(f"Class ID    : {entry['class_id']}\n")
                f.write("\n")

        # Unscheduled meetings
        if unscheduled:
            f.write("\n" + "="*100 + "\n")
            f.write(" UNSCHEDULED MEETINGS\n")
            f.write("="*100 + "\n\n")

            for entry in unscheduled:
                f.write(f"Course: {entry['course_code']} | Type: {entry['type']} | "
                        f"Hours: {entry['hours']} | Reason: {entry['reason']}\n")

    print(f"\n[INFO] Schedule saved to text file: {filename}")


def save_schedule_to_json(schedule, unscheduled, filename, schedule_by_room=None,
                          schedule_by_branch=None):
    """Save schedule to a JSON file."""
    # Count full time and part time faculty in schedule
    faculty_types = {}
    for entry in schedule:
        fid = entry.get("faculty_id")
        if fid not in faculty_types:
            faculty_types[fid] = entry.get("employment_type", "full time")

    full_time_count = sum(1 for et in faculty_types.values()
                          if et.lower() == "full time")
    part_time_count = sum(1 for et in faculty_types.values()
                          if et.lower() == "part time")

    output_data = {
        "metadata": {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "total_scheduled": len(schedule),
            "total_unscheduled": len(unscheduled),
            "full_time_faculty_scheduled": full_time_count,
            "part_time_faculty_scheduled": part_time_count,
            "days": DAYS,
            "start_hour": START_HOUR,
            "end_hour": END_HOUR
        },
        "scheduled_meetings": schedule,
        "unscheduled_meetings": unscheduled,
        "schedule_by_room": schedule_by_room or {},
        "schedule_by_branch": schedule_by_branch or {}
    }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)

    print(f"[INFO] Schedule saved to JSON file: {filename}")


def save_schedule_to_excel(schedule, unscheduled, faculty_loads, filename):
    """Save schedule to an Excel file with multiple sheets."""
    wb = Workbook()

    # Remove default sheet
    if "Sheet" in wb.sheetnames:
        wb.remove(wb["Sheet"])

    # Define styles
    header_fill = PatternFill(start_color="366092",
                              end_color="366092", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    subheader_fill = PatternFill(
        start_color="B4C7E7", end_color="B4C7E7", fill_type="solid")
    subheader_font = Font(bold=True, size=11)
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    center_aligned = Alignment(
        horizontal='center', vertical='center', wrap_text=True)

    # ============================================================
    # SHEET 1: Schedule by Day
    # ============================================================
    ws_by_day = wb.create_sheet("Schedule by Day")

    # Headers - added Employment Type and Schedule Type
    headers = ["Day", "Time", "Course Code", "Type", "Faculty", "Employment Type", "Schedule Type", "Room", "Room Type",
               "Capacity", "Class Size", "Program ID", "Institute ID", "Class ID", "Program Code"]
    ws_by_day.append(headers)

    # Style headers
    for col_num, header in enumerate(headers, 1):
        cell = ws_by_day.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = border

    # Sort schedule by day and time
    sorted_schedule = sorted(schedule, key=lambda x: (
        DAYS.index(x["day"]), x["start_hour"]))

    # Add data
    for entry in sorted_schedule:
        # Get employment type from faculty_loads
        faculty_id = entry["faculty_id"]
        employment_type = faculty_loads.get(
            faculty_id, {}).get("employment_type", "full time")

        ws_by_day.append([
            entry["day"],
            entry["time_slot"],
            entry["course_code"],
            entry["type"],
            entry["faculty_name"],
            employment_type.title(),  # Capitalize for display
            # Schedule Type
            entry.get("schedule_type", "face to face").title(),
            entry["room_name"],
            entry["room_type"],
            entry["room_capacity"],
            entry["class_size"],
            entry["program_id"],
            entry["institute_id"],
            entry["class_id"],
            entry.get("program_code", "")
        ])

    # Apply borders and auto-adjust column widths
    for row in ws_by_day.iter_rows(min_row=2, max_row=ws_by_day.max_row):
        for cell in row:
            cell.border = border
            # Numeric columns (shifted due to Schedule Type)
            if cell.column in [10, 11, 12, 13, 14]:
                cell.alignment = Alignment(horizontal='center')

        # Color code employment type
        emp_type_cell = row[5]  # Employment Type column
        if emp_type_cell.value == "Full Time":
            emp_type_cell.fill = PatternFill(
                start_color="4472C4", end_color="4472C4", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")
        else:  # Part Time
            emp_type_cell.fill = PatternFill(
                start_color="ED7D31", end_color="ED7D31", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")

        # Color code schedule type
        schedule_type_cell = row[6]  # Schedule Type column
        if schedule_type_cell.value == "Face To Face":
            schedule_type_cell.fill = PatternFill(
                start_color="70AD47", end_color="70AD47", fill_type="solid")
            schedule_type_cell.font = Font(bold=True, color="FFFFFF")
        elif schedule_type_cell.value == "Online":
            schedule_type_cell.fill = PatternFill(
                start_color="5B9BD5", end_color="5B9BD5", fill_type="solid")
            schedule_type_cell.font = Font(bold=True, color="FFFFFF")

    # Auto-adjust column widths
    for col in range(1, len(headers) + 1):
        ws_by_day.column_dimensions[get_column_letter(col)].width = 15
    ws_by_day.column_dimensions['B'].width = 20  # Time column
    ws_by_day.column_dimensions['E'].width = 25  # Faculty name
    ws_by_day.column_dimensions['F'].width = 18  # Employment Type
    ws_by_day.column_dimensions['G'].width = 16  # Schedule Type

    # ============================================================
    # SHEET 2: Schedule by Faculty
    # ============================================================
    ws_by_faculty = wb.create_sheet("Schedule by Faculty")

    # Headers - added Employment Type
    headers_faculty = ["Faculty Name", "Faculty ID", "Employment Type", "Day", "Time", "Course Code",
                       "Type", "Room", "Hours", "Class ID", "Program Code"]
    ws_by_faculty.append(headers_faculty)

    # Style headers
    for col_num, header in enumerate(headers_faculty, 1):
        cell = ws_by_faculty.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = border

    # Sort by faculty name
    sorted_by_faculty = sorted(schedule, key=lambda x: (
        x["faculty_name"], DAYS.index(x["day"]), x["start_hour"]))

    # Add data
    for entry in sorted_by_faculty:
        # Get employment type from faculty_loads
        faculty_id = entry["faculty_id"]
        employment_type = faculty_loads.get(
            faculty_id, {}).get("employment_type", "full time")

        ws_by_faculty.append([
            entry["faculty_name"],
            entry["faculty_id"],
            employment_type.title(),  # Capitalize for display
            entry["day"],
            entry["time_slot"],
            entry["course_code"],
            entry["type"],
            entry["room_name"],
            entry["duration"],
            entry["class_id"],
            entry.get("program_code", "")
        ])

    # Apply styling
    for row in ws_by_faculty.iter_rows(min_row=2, max_row=ws_by_faculty.max_row):
        for cell in row:
            cell.border = border

        # Color code employment type
        emp_type_cell = row[2]  # Employment Type column
        if emp_type_cell.value == "Full Time":
            emp_type_cell.fill = PatternFill(
                start_color="4472C4", end_color="4472C4", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")
        else:  # Part Time
            emp_type_cell.fill = PatternFill(
                start_color="ED7D31", end_color="ED7D31", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")

    # Auto-adjust column widths
    for col in range(1, len(headers_faculty) + 1):
        ws_by_faculty.column_dimensions[get_column_letter(col)].width = 15
    ws_by_faculty.column_dimensions['A'].width = 25  # Faculty name
    ws_by_faculty.column_dimensions['C'].width = 18  # Employment Type
    ws_by_faculty.column_dimensions['E'].width = 20  # Time

    # ============================================================
    # SHEET 3: Schedule by Room
    # ============================================================
    ws_by_room = wb.create_sheet("Schedule by Room")

    # Headers
    headers_room = ["Room Name", "Room ID", "Room Type", "Capacity", "Day",
                    "Time", "Course Code", "Faculty", "Class ID", "Program Code"]
    ws_by_room.append(headers_room)

    # Style headers
    for col_num, header in enumerate(headers_room, 1):
        cell = ws_by_room.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = border

    # Sort by room and day/time
    sorted_by_room = sorted(schedule, key=lambda x: (
        x["room_name"], DAYS.index(x["day"]), x["start_hour"]))

    # Add data
    for entry in sorted_by_room:
        ws_by_room.append([
            entry["room_name"],
            entry["room_id"],
            entry["room_type"],
            entry["room_capacity"],
            entry["day"],
            entry["time_slot"],
            entry["course_code"],
            entry["faculty_name"],
            entry["class_id"],
            entry.get("program_code", "")
        ])

    # Apply styling
    for row in ws_by_room.iter_rows(min_row=2, max_row=ws_by_room.max_row):
        for cell in row:
            cell.border = border

    # Auto-adjust column widths
    for col in range(1, len(headers_room) + 1):
        ws_by_room.column_dimensions[get_column_letter(col)].width = 15
    ws_by_room.column_dimensions['F'].width = 20  # Time
    ws_by_room.column_dimensions['H'].width = 25  # Faculty name

    # ============================================================
    # SHEET 4: Schedule by Day and Room
    # ============================================================
    ws_day_room = wb.create_sheet("Schedule by Day & Room")

    # Headers
    headers_day_room = ["Day", "Room Name", "Room Type", "Time", "Course Code",
                        "Type", "Faculty", "Class Size", "Class ID", "Program Code"]
    ws_day_room.append(headers_day_room)

    # Style headers
    for col_num, header in enumerate(headers_day_room, 1):
        cell = ws_day_room.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = border

    # Sort by day, room, and time
    sorted_by_day_room = sorted(schedule, key=lambda x: (
        DAYS.index(x["day"]), x["room_name"], x["start_hour"]))

    # Add data
    for entry in sorted_by_day_room:
        ws_day_room.append([
            entry["day"],
            entry["room_name"],
            entry["room_type"],
            entry["time_slot"],
            entry["course_code"],
            entry["type"],
            entry["faculty_name"],
            entry["class_size"],
            entry["class_id"],
            entry.get("program_code", "")
        ])

    # Apply styling
    for row in ws_day_room.iter_rows(min_row=2, max_row=ws_day_room.max_row):
        for cell in row:
            cell.border = border

    # Auto-adjust column widths
    for col in range(1, len(headers_day_room) + 1):
        ws_day_room.column_dimensions[get_column_letter(col)].width = 15
    ws_day_room.column_dimensions['B'].width = 20  # Room Name
    ws_day_room.column_dimensions['D'].width = 20  # Time
    ws_day_room.column_dimensions['G'].width = 25  # Faculty name

    # ============================================================
    # SHEET 5: Faculty Load Summary
    # ============================================================
    ws_summary = wb.create_sheet("Faculty Load Summary")

    # Headers - added Employment Type and Max Load
    headers_summary = ["Faculty Name", "Faculty ID", "Employment Type", "Max Load",
                       "Total Courses", "Total Units", "Lecture Hours", "Lab Hours", "Load Status"]
    ws_summary.append(headers_summary)

    # Style headers
    for col_num, header in enumerate(headers_summary, 1):
        cell = ws_summary.cell(1, col_num)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_aligned
        cell.border = border

    # Add faculty load data
    faculty_list = []
    for fid, info in faculty_loads.items():
        num_courses = len(info["assigned_classes"])
        total_units = info["total_units"]
        employment_type = info.get("employment_type", "full time")
        load_unit = info.get("load_unit", MAX_LOAD)
        load_status = "FULL" if total_units >= load_unit else "PARTIAL" if total_units > 0 else "NONE"

        faculty_list.append([
            info["faculty_name"],
            fid,
            employment_type.title(),  # Capitalize for display
            load_unit,
            num_courses,
            round(total_units, 2),
            info["total_lecture_hours"],
            info["total_lab_hours"],
            load_status
        ])

    # Sort by faculty name
    faculty_list.sort(key=lambda x: x[0])

    # Add data
    for row_data in faculty_list:
        ws_summary.append(row_data)

    # Apply styling and conditional formatting for load status
    for row in ws_summary.iter_rows(min_row=2, max_row=ws_summary.max_row):
        for cell in row:
            cell.border = border
            if cell.column in [4, 5, 6, 7, 8]:  # Numeric columns
                cell.alignment = Alignment(horizontal='center')

        # Color code employment type
        emp_type_cell = row[2]  # Employment Type column
        if emp_type_cell.value == "Full Time":
            emp_type_cell.fill = PatternFill(
                start_color="4472C4", end_color="4472C4", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")
        else:  # Part Time
            emp_type_cell.fill = PatternFill(
                start_color="ED7D31", end_color="ED7D31", fill_type="solid")
            emp_type_cell.font = Font(bold=True, color="FFFFFF")

        # Color code load status
        status_cell = row[8]  # Load Status column (now index 8)
        if status_cell.value == "FULL":
            status_cell.fill = PatternFill(
                start_color="00B050", end_color="00B050", fill_type="solid")
            status_cell.font = Font(bold=True, color="FFFFFF")
        elif status_cell.value == "PARTIAL":
            status_cell.fill = PatternFill(
                start_color="FFC000", end_color="FFC000", fill_type="solid")
            status_cell.font = Font(bold=True)
        else:
            status_cell.fill = PatternFill(
                start_color="FF0000", end_color="FF0000", fill_type="solid")
            status_cell.font = Font(bold=True, color="FFFFFF")

    # Auto-adjust column widths
    for col in range(1, len(headers_summary) + 1):
        ws_summary.column_dimensions[get_column_letter(col)].width = 16
    ws_summary.column_dimensions['A'].width = 25  # Faculty name
    ws_summary.column_dimensions['C'].width = 18  # Employment Type

    # ============================================================
    # SHEET 6: Unscheduled Classes
    # ============================================================
    if unscheduled:
        ws_unscheduled = wb.create_sheet("Unscheduled Classes")

        # Headers
        headers_unsch = ["Course Code", "Type", "Hours", "Class ID", "Reason"]
        ws_unscheduled.append(headers_unsch)

        # Style headers
        for col_num, header in enumerate(headers_unsch, 1):
            cell = ws_unscheduled.cell(1, col_num)
            cell.font = header_font
            cell.fill = PatternFill(
                start_color="C00000", end_color="C00000", fill_type="solid")
            cell.alignment = center_aligned
            cell.border = border

        # Add unscheduled data
        for entry in unscheduled:
            ws_unscheduled.append([
                entry["course_code"],
                entry["type"],
                entry["hours"],
                entry["class_id"],
                entry["reason"]
            ])

        # Apply styling
        for row in ws_unscheduled.iter_rows(min_row=2, max_row=ws_unscheduled.max_row):
            for cell in row:
                cell.border = border

        # Auto-adjust column widths
        ws_unscheduled.column_dimensions['A'].width = 15
        ws_unscheduled.column_dimensions['B'].width = 12
        ws_unscheduled.column_dimensions['C'].width = 10
        ws_unscheduled.column_dimensions['D'].width = 12
        ws_unscheduled.column_dimensions['E'].width = 40

    # ============================================================
    # SHEET 7: Schedule Conflicts
    # ============================================================
    # Detect conflicts using validate_schedule_detailed
    conflicts_data = validate_schedule_detailed(schedule)

    ws_conflicts = wb.create_sheet("Schedule Conflicts")

    # Headers
    headers_conflicts = ["Conflict Type", "Day", "Time Slot 1", "Time Slot 2", "Course 1", "Course 2",
                         "Resource", "Resource ID", "Details"]
    ws_conflicts.append(headers_conflicts)

    # Style headers
    conflict_header_fill = PatternFill(start_color="C00000", end_color="C00000", fill_type="solid")
    for col_num, header in enumerate(headers_conflicts, 1):
        cell = ws_conflicts.cell(1, col_num)
        cell.font = header_font
        cell.fill = conflict_header_fill
        cell.alignment = center_aligned
        cell.border = border

    if conflicts_data:
        # Add conflict data
        for conflict in conflicts_data:
            ws_conflicts.append([
                conflict["type"],
                conflict["day"],
                conflict["time_slot_1"],
                conflict["time_slot_2"],
                conflict["course_1"],
                conflict["course_2"],
                conflict["resource"],
                conflict["resource_id"],
                conflict["details"]
            ])

        # Apply styling
        for row in ws_conflicts.iter_rows(min_row=2, max_row=ws_conflicts.max_row):
            for cell in row:
                cell.border = border

            # Color code conflict type
            conflict_type_cell = row[0]
            if "Room" in str(conflict_type_cell.value):
                conflict_type_cell.fill = PatternFill(
                    start_color="FF6B6B", end_color="FF6B6B", fill_type="solid")
                conflict_type_cell.font = Font(bold=True)
            elif "Class" in str(conflict_type_cell.value):
                conflict_type_cell.fill = PatternFill(
                    start_color="FFB347", end_color="FFB347", fill_type="solid")
                conflict_type_cell.font = Font(bold=True)
            elif "Faculty" in str(conflict_type_cell.value):
                conflict_type_cell.fill = PatternFill(
                    start_color="77DD77", end_color="77DD77", fill_type="solid")
                conflict_type_cell.font = Font(bold=True)
    else:
        # No conflicts - add a message
        ws_conflicts.append(["No conflicts detected", "", "", "", "", "", "", "", "Schedule is conflict-free!"])
        cell = ws_conflicts.cell(2, 1)
        cell.fill = PatternFill(start_color="00B050", end_color="00B050", fill_type="solid")
        cell.font = Font(bold=True, color="FFFFFF")

    # Auto-adjust column widths
    ws_conflicts.column_dimensions['A'].width = 15  # Conflict Type
    ws_conflicts.column_dimensions['B'].width = 12  # Day
    ws_conflicts.column_dimensions['C'].width = 18  # Time Slot 1
    ws_conflicts.column_dimensions['D'].width = 18  # Time Slot 2
    ws_conflicts.column_dimensions['E'].width = 15  # Course 1
    ws_conflicts.column_dimensions['F'].width = 15  # Course 2
    ws_conflicts.column_dimensions['G'].width = 20  # Resource
    ws_conflicts.column_dimensions['H'].width = 12  # Resource ID
    ws_conflicts.column_dimensions['I'].width = 40  # Details

    # Save workbook
    wb.save(filename)
    print(f"[INFO] Schedule saved to Excel file: {filename}")


# ===========================================================   =
# START CODE FOR FACULTY aSSIGNING TO CLASSES
# ============================================================
def fetch_table_data(table: Table) -> List[Dict]:
    """
    Fetch all rows from a given SQLAlchemy Table and return as a list of dictionaries.
    """
    with engine.connect() as conn:
        result = conn.execute(select(table))
        rows = result.fetchall()
        return [dict(row._mapping) for row in rows]


# ============================================================
# FACULTY LOAD CALCULATION FUNCTIONS
# ============================================================

MAX_LOAD = 18  # maximum faculty load units


def compute_load(lec_units, lab_units):
    """
    Compute teacher load units from student lecture and lab units.
    Based on the formula:
    - Lecture: 1 student unit = 1 hour = 1 teacher unit
    - Laboratory: 1 student unit = 3 hours × 0.75/hour = 2.25 teacher units

    lec_units: student lecture units
    lab_units: student laboratory units
    Returns total teacher units for faculty loading
    """
    teacher_lec_units = lec_units * LECTURE_STUDENT_UNIT_TO_TEACHER_UNIT
    teacher_lab_units = lab_units * LAB_STUDENT_UNIT_TO_TEACHER_UNIT
    return teacher_lec_units + teacher_lab_units


def matches_expertise(course, faculty_course):
    """
    Check if faculty expertise matches a class.
    Must match: course_code AND program_id.
    """
    return (
        faculty_course["course_code"] == course["course_code"]
        and faculty_course["program_id"] == course["program_id"]
    )


def parse_faculty_branches(branches_value):
    """
    Parse the 'branches' field from faculty_expertise_courses.
    It's stored as a Python list repr string like "['1']" or "['2', '1']".
    Returns a set of integer branch IDs.
    """
    if not branches_value:
        return set()
    if isinstance(branches_value, list):
        return {int(b) for b in branches_value if str(b).strip()}
    if isinstance(branches_value, str):
        try:
            import ast
            parsed = ast.literal_eval(branches_value)
            if isinstance(parsed, list):
                return {int(b) for b in parsed if str(b).strip()}
        except (ValueError, SyntaxError):
            pass
    return set()


def assign_faculty(classes_courses, faculty_expertise_courses):
    """
    Assign classes to faculty based on matching expertise and load limit.
    Uses load_unit from faculty data (18 for full time, 9 for part time).

    Inter-branch priority: For classes at non-Main branches, faculty who have
    that branch in their 'branches' expertise field are tried first.
    """

    # Prepare load tracking structure
    faculty_loads = {}

    # Build faculty branches lookup (fid → set of branch IDs)
    faculty_branches_map = {}

    for f in faculty_expertise_courses:
        fid = f["faculty_id"]
        # Only set if not already set (avoid overwriting with duplicate entries)
        if fid not in faculty_loads:
            faculty_loads[fid] = {
                "faculty_name": f["faculty_name"],
                "employment_type": f.get("employment_type", "full time"),
                # Use faculty's load_unit or default to MAX_LOAD
                "load_unit": f.get("load_unit", MAX_LOAD),
                "preferred_time": parse_preferred_time(f.get("preffered_time", "")),
                "assigned_classes": [],
                "total_units": 0,
                "total_lecture_hours": 0,
                "total_lab_hours": 0,
            }
            faculty_branches_map[fid] = parse_faculty_branches(f.get("branches"))

    # Track unassigned non-Main branch courses for branch_expertise_needed output
    unassigned_branch_courses = []

    # ----------------------------------------------------------------
    # EXPERTISE-FIRST ASSIGNMENT  (Round-Robin Interleaved)
    #
    # Why round-robin instead of sequential processing:
    #   Sequential "most-constrained-first" causes STARVATION. Example:
    #   IT411 (1 qualified faculty: F1) gets processed first → all 4 sections
    #   consume F1's load. Then ITELEC2 (3 qualified: F1,F2,F3) arrives later
    #   and F1 has no capacity left.
    #
    # Round-robin fix: each iteration assigns exactly 1 section from each
    # expertise group before going back to assign a second section.
    # This prevents any group from monopolising shared faculty capacity.
    #
    # Process flow:
    #   1. Group classes by expertise key (course_code, program_id)
    #   2. Build expertise → qualified faculty map
    #   3. Each round: visit every expertise group once and assign 1 section
    #      to the least-loaded qualified faculty (load-balanced)
    #   4. Repeat rounds until all sections assigned or none can progress
    # ----------------------------------------------------------------

    # Build expertise → qualified faculty list map
    # key: (course_code, program_id) → [fid, fid, ...]
    expertise_to_fids = {}
    for f in faculty_expertise_courses:
        if f.get("course_code") is None:
            continue
        key = (f["course_code"], f["program_id"])
        if key not in expertise_to_fids:
            expertise_to_fids[key] = []
        fid = f["faculty_id"]
        if fid not in expertise_to_fids[key]:
            expertise_to_fids[key].append(fid)

    # Group classes by expertise key; shuffle within each group for fairness
    classes_by_expertise = {}
    for course in classes_courses:
        key = (course.get("course_code"), course.get("program_id"))
        if key not in classes_by_expertise:
            classes_by_expertise[key] = []
        classes_by_expertise[key].append(course)

    # Mutable per-group queues of sections still waiting to be assigned
    remaining_sections = {}
    for k, v in classes_by_expertise.items():
        sections = list(v)
        random.shuffle(sections)
        remaining_sections[k] = sections

    # Expertise groups with no qualified faculty at all — mark immediately
    for key, sections in remaining_sections.items():
        if not expertise_to_fids.get(key):
            for course in sections:
                print(f"[WARNING] No qualified faculty found for course: {course['course_code']}")
                course_branch_id = course.get("branch_id")
                if course_branch_id is not None and course_branch_id != MAIN_BRANCH_ID:
                    unassigned_branch_courses.append(course)
            remaining_sections[key] = []

    # ----------------------------------------------------------------
    # TIERED ASSIGNMENT: process expertise groups in ascending order of
    # units_per_section.  Smaller-unit courses (e.g. ITELEC2 @ 4.25 units)
    # are fully scheduled before larger-unit courses (e.g. IT111 @ 7.5 units).
    # This prevents large-unit monopoly courses from consuming shared faculty
    # capacity before smaller, higher-section-count courses can claim their share.
    #
    # Within each tier: load-balanced round-robin (1 section per expertise group
    # per pass) distributes sections across all qualified faculty fairly.
    # ----------------------------------------------------------------

    # Build tier map: units_per_section → [expertise_key, ...]
    unit_to_keys = {}
    for key in classes_by_expertise.keys():
        if not expertise_to_fids.get(key):
            continue  # No qualified faculty — already warned above
        if not remaining_sections.get(key):
            continue
        sample = remaining_sections[key][0]
        ups = compute_load(sample["course_lec"], sample["course_lab"])
        if ups not in unit_to_keys:
            unit_to_keys[ups] = []
        unit_to_keys[ups].append(key)

    # Process tiers from smallest to largest units_per_section
    for ups in sorted(unit_to_keys.keys()):
        tier_keys = unit_to_keys[ups]
        random.shuffle(tier_keys)  # Fair ordering within tier

        # Round-robin within tier: assign 1 section per group per pass
        made_progress = True
        while made_progress:
            made_progress = False
            for expertise_key in tier_keys:
                if not remaining_sections.get(expertise_key):
                    continue

                qualified_fids = expertise_to_fids[expertise_key]
                course = remaining_sections[expertise_key][0]
                course_branch_id = course.get("branch_id")

                # Sort: branch priority → load balance → random tiebreaker
                sorted_fids = sorted(
                    qualified_fids,
                    key=lambda fid: (
                        0 if (
                            course_branch_id is not None
                            and course_branch_id != MAIN_BRANCH_ID
                            and course_branch_id in faculty_branches_map.get(fid, set())
                        ) else 1,
                        faculty_loads[fid]["total_units"],
                        random.random(),
                    )
                )

                for fid in sorted_fids:
                    units = compute_load(course["course_lec"], course["course_lab"])
                    if faculty_loads[fid]["total_units"] + units <= faculty_loads[fid]["load_unit"]:
                        faculty_loads[fid]["assigned_classes"].append(course)
                        faculty_loads[fid]["total_units"] += units
                        faculty_loads[fid]["total_lecture_hours"] += course["course_lec"]
                        faculty_loads[fid]["total_lab_hours"] += course["course_lab"]
                        remaining_sections[expertise_key].pop(0)
                        made_progress = True
                        break

    # Any sections that couldn't be assigned after all tiers exhausted
    for expertise_key, courses in remaining_sections.items():
        for course in courses:
            print(f"[WARNING] No qualified faculty found for course: {course['course_code']}")
            course_branch_id = course.get("branch_id")
            if course_branch_id is not None and course_branch_id != MAIN_BRANCH_ID:
                unassigned_branch_courses.append(course)

    return faculty_loads, unassigned_branch_courses


def save_faculty_load_to_text(faculty_loads: Dict, filename: str):
    """
    Save faculty loading results to a plain text file in a readable format.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write(" " * 25 + "FACULTY LOAD ASSIGNMENTS\n")
        f.write("=" * 80 + "\n")
        f.write(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Full Time Max Load: 18 units | Part Time Max Load: 9 units\n")
        f.write("=" * 80 + "\n\n")

        # Faculty with assignments
        for fid, info in faculty_loads.items():
            if len(info["assigned_classes"]) == 0:
                continue

            employment_type = info.get("employment_type", "full time").title()
            load_unit = info.get("load_unit", MAX_LOAD)

            f.write("-" * 80 + "\n")
            f.write(f"Faculty: {info['faculty_name']} (ID: {fid})\n")
            f.write(
                f"Employment Type: {employment_type} | Max Load: {load_unit} units\n")
            f.write("-" * 80 + "\n")
            f.write(
                f"Total Units Load      : {info['total_units']:.2f} / {load_unit} units\n")
            f.write(
                f"Total Lecture Hours   : {info['total_lecture_hours']} hours\n")
            f.write(
                f"Total Laboratory Hours: {info['total_lab_hours']} hours\n")
            f.write(
                f"Number of Classes     : {len(info['assigned_classes'])}\n\n")
            f.write("Assigned Classes:\n")

            for idx, cls in enumerate(info["assigned_classes"], 1):
                units = compute_load(cls['course_lec'], cls['course_lab'])
                f.write(f"  {idx}. Course Code   : {cls['course_code']}\n")
                f.write(f"     Class ID      : {cls['class_id']}\n")
                f.write(f"     Program ID    : {cls['program_id']}\n")
                f.write(f"     Lecture Hours : {cls['course_lec']}\n")
                f.write(f"     Lab Hours     : {cls['course_lab']}\n")
                f.write(f"     Units Load    : {units:.2f}\n\n")

            f.write("\n")

        # Summary section
        f.write("\n" + "=" * 80 + "\n")
        f.write(" " * 30 + "SUMMARY REPORT\n")
        f.write("=" * 80 + "\n\n")

        total_faculty_with_loads = 0
        total_faculty_without_loads = 0
        total_full_time = 0
        total_part_time = 0

        for fid, info in faculty_loads.items():
            num_courses = len(info["assigned_classes"])
            total_units = info["total_units"]
            employment_type = info.get("employment_type", "full time")
            load_unit = info.get("load_unit", MAX_LOAD)

            if num_courses > 0:
                total_faculty_with_loads += 1
                if employment_type.lower() == "full time":
                    total_full_time += 1
                else:
                    total_part_time += 1
                load_status = "FULL" if total_units >= load_unit else "PARTIAL"
                emp_short = "FT" if employment_type.lower() == "full time" else "PT"
                f.write(
                    f"{info['faculty_name']:<35} | {emp_short} | {num_courses:>2} courses | {total_units:>5.2f}/{load_unit:>2} units | {load_status}\n")
            else:
                total_faculty_without_loads += 1

        f.write("\n" + "-" * 80 + "\n")
        f.write(
            f"Total Faculty with Assignments   : {total_faculty_with_loads}\n")
        f.write(f"  - Full Time Faculty            : {total_full_time}\n")
        f.write(f"  - Part Time Faculty            : {total_part_time}\n")
        f.write(
            f"Total Faculty without Assignments: {total_faculty_without_loads}\n")
        f.write("=" * 80 + "\n")

    print(f"\n[INFO] Faculty load saved to text file: {filename}")


def save_faculty_load_to_json(faculty_loads: Dict, filename: str):
    """
    Save faculty loading results to a JSON file.
    """
    # Prepare JSON-serializable data
    output_data = {
        "metadata": {
            "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "full_time_max_load": 18,
            "part_time_max_load": 9,
            "total_faculty": len(faculty_loads),
            "faculty_with_assignments": sum(1 for info in faculty_loads.values() if len(info["assigned_classes"]) > 0),
            "faculty_without_assignments": sum(1 for info in faculty_loads.values() if len(info["assigned_classes"]) == 0),
            "full_time_faculty": sum(1 for info in faculty_loads.values() if info.get("employment_type", "full time").lower() == "full time" and len(info["assigned_classes"]) > 0),
            "part_time_faculty": sum(1 for info in faculty_loads.values() if info.get("employment_type", "full time").lower() == "part time" and len(info["assigned_classes"]) > 0)
        },
        "faculty_loads": []
    }

    for fid, info in faculty_loads.items():
        employment_type = info.get("employment_type", "full time")
        load_unit = info.get("load_unit", MAX_LOAD)

        faculty_entry = {
            "faculty_id": fid,
            "faculty_name": info["faculty_name"],
            "employment_type": employment_type,
            "max_load_unit": load_unit,
            "total_units": round(info["total_units"], 2),
            "total_lecture_hours": info["total_lecture_hours"],
            "total_lab_hours": info["total_lab_hours"],
            "number_of_classes": len(info["assigned_classes"]),
            "load_status": "FULL" if info["total_units"] >= load_unit else "PARTIAL" if info["total_units"] > 0 else "NONE",
            "assigned_classes": []
        }

        for cls in info["assigned_classes"]:
            class_entry = {
                "class_id": cls["class_id"],
                "course_code": cls["course_code"],
                "program_id": cls["program_id"],
                "institute_id": cls.get("institute_id", None),
                "lecture_hours": cls["course_lec"],
                "lab_hours": cls["course_lab"],
                "units_load": round(compute_load(cls["course_lec"], cls["course_lab"]), 2)
            }
            faculty_entry["assigned_classes"].append(class_entry)

        output_data["faculty_loads"].append(faculty_entry)

    # Sort by faculty name
    output_data["faculty_loads"].sort(key=lambda x: x["faculty_name"])

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)

    print(f"[INFO] Faculty load saved to JSON file: {filename}")
# ============================================================
# MAIN SCRIPT
# ============================================================


if __name__ == "__main__":

    # ------------------------------------------
    # LOAD DATA FROM DATABASE
    # ------------------------------------------
    classes_course_table = Table(
        "classes_course", metadata, autoload_with=engine
    )
    faculty_expertise_courses_table = Table(
        "faculty_expertise_courses", metadata, autoload_with=engine
    )
    rooms_table = Table(
        "rooms_view", metadata, autoload_with=engine
    )
    programs_table = Table(
        "programs", metadata, autoload_with=engine
    )
    classes_table = Table(
        "classes", metadata, autoload_with=engine
    )
    college_branch_table = Table(
        "college_branch", metadata, autoload_with=engine
    )

    classes_course = fetch_table_data(classes_course_table)
    faculty_expertise_courses = fetch_table_data(
        faculty_expertise_courses_table
    )
    rooms = fetch_table_data(rooms_table)
    programs = fetch_table_data(programs_table)
    classes = fetch_table_data(classes_table)
    college_branches = fetch_table_data(college_branch_table)

    # Build program_id -> program_code lookup map
    program_map = {p["program_id"]: p["program_code"] for p in programs}

    # Build college_branch_id -> college_branch_name lookup map
    branch_map = {b["college_branch_id"]: b["college_branch_name"] for b in college_branches}

    # Build class_id -> class_size lookup map
    class_size_map = {c["class_id"]: c["class_size"] for c in classes}

    # Enrich classes_course with program_code and class_size
    for cls in classes_course:
        cls["program_code"] = program_map.get(cls.get("program_id"), "Unknown")
        cls["class_size"] = class_size_map.get(cls.get("class_id"), 0)

    # ------------------------------------------
    # APPLY FACULTY LOAD ASSIGNMENT
    # ------------------------------------------
    faculty_load_result, unassigned_branch_courses = assign_faculty(
        classes_course,
        faculty_expertise_courses
    )

    # ------------------------------------------
    # BUILD branch_expertise_needed
    # ------------------------------------------
    # Group unassigned non-Main branch courses by branch → program-year → courses
    branch_expertise_needed = {}
    for course in unassigned_branch_courses:
        bid = course.get("branch_id")
        bname = branch_map.get(bid, f"Branch {bid}")
        program_code = course.get("program_code", "Unknown")
        year_level = course.get("course_level", 0)
        program_key = f"{program_code}-{year_level}"
        course_code = course.get("course_code", "Unknown")

        if bname not in branch_expertise_needed:
            branch_expertise_needed[bname] = {}
        if program_key not in branch_expertise_needed[bname]:
            branch_expertise_needed[bname][program_key] = []
        if course_code not in branch_expertise_needed[bname][program_key]:
            branch_expertise_needed[bname][program_key].append(course_code)

    if branch_expertise_needed:
        print(f"\n[INFO] Branch expertise needed:")
        for bname, programs in branch_expertise_needed.items():
            print(f"  {bname}:")
            for prog_key, courses in programs.items():
                print(f"    {prog_key}: {', '.join(courses)}")

    # ------------------------------------------
    # CREATE ROOM AND TIME SCHEDULE
    # ------------------------------------------
    complete_schedule, unscheduled_meetings, schedule_by_room, schedule_by_branch = create_schedule(
        faculty_load_result,
        rooms,
        branch_map
    )

    # Append branch expertise needed courses to unscheduled_meetings
    for course in unassigned_branch_courses:
        bid = course.get("branch_id")
        bname = branch_map.get(bid, f"Branch {bid}")
        program_code = course.get("program_code", "Unknown")
        year_level = course.get("course_level", 0)
        unscheduled_meetings.append({
            "class_id": course.get("class_id"),
            "course_code": course.get("course_code", "Unknown"),
            "course_id": course.get("course_id"),
            "institute_id": course.get("institute_id"),
            "class_size": course.get("class_size", 0),
            "faculty_name": "Unassigned",
            "program_id": course.get("program_id"),
            "program_name": course.get("program_name", "Unknown"),
            "program_code": program_code,
            "type": "Lecture" if course.get("course_lab", 0) == 0 else "Lecture+Lab",
            "hours": f"{course.get('course_lec', 0)}h lec + {course.get('course_lab', 0)}h lab",
            "reason": f"No qualified faculty - branch expertise needed ({bname}, {program_code}-{year_level})"
        })

    # Generate timestamp for filenames
    # Create output directory if it doesn't exist
    output_dir = "faculty_loading_output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    schedule_excel_filename = os.path.join(
        output_dir, f"scheduleeeessseee_{timestamp}.xlsx")
    save_schedule_to_excel(complete_schedule, unscheduled_meetings,
                           faculty_load_result, schedule_excel_filename)

    # Save schedule to JSON file (always overwrites with same filename)
    json_output_dir = os.path.join("..", "backend", "src", "generated_scheduled", "json_output")
    os.makedirs(json_output_dir, exist_ok=True)
    json_filename = os.path.join(json_output_dir, "faculty_loading.json")
    save_schedule_to_json(complete_schedule, unscheduled_meetings, json_filename,
                          schedule_by_room, schedule_by_branch)

    # Generate faculty core time schedule (time-in / time-out)
    faculty_core_time = generate_faculty_core_time(complete_schedule)
    core_time_filename = os.path.join(json_output_dir, "faculty_core_time.json")
    save_faculty_core_time_to_json(faculty_core_time, core_time_filename, complete_schedule, branch_map)

    # ------------------------------------------
    # FINAL OUTPUT (FOR NESTJS)
    # ------------------------------------------
    output = {
        "scheduled_meetings": complete_schedule,
        "unscheduled_meetings": unscheduled_meetings,
        "schedule_by_branch": schedule_by_branch
    }

    # IMPORTANT: markers help NestJS safely parse stdout
    print("===JSON_START===")
    print(json.dumps(output, indent=2, default=str))
    print("===JSON_END===")
