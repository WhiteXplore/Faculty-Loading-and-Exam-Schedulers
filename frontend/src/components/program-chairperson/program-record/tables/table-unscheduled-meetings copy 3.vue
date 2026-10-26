<template>
  <!-- Controls -->
  <div class="table-container">
    <div class="table-controls">
      <!-- Per Page -->
      <div class="per-page-container">
        <div class="select-wrapper">
          <select
            v-model.number="itemsPerPage"
            @change="changePage(1)"
            class="select-input"
          >
            <option :value="10">10</option>
            <option :value="15">15</option>
            <option :value="20">20</option>
          </select>
          <div
            class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-defaultGreen"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M19 9l-7 7-7-7"
              />
            </svg>
          </div>
        </div>
        <span class="text-sm">Per page</span>
      </div>
      <div class="flex gap-2">
        <!-- Admin Program Filter -->
        <div
          v-if="user.role === 'Admin'"
          class="relative w-56"
          ref="programDropdownRef"
        >
          <div
            class="relative flex items-center rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 focus-within:border-defaultGreen focus-within:ring-4 focus-within:ring-green-100"
          >
            <!-- Icon -->
            <div class="absolute left-3 text-gray-400">
              <svg
                class="h-4 w-4"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M4 7h16M4 12h16M4 17h16"
                />
              </svg>
            </div>

            <!-- Selected -->
            <button
              type="button"
              @click="showProgramDropdown = !showProgramDropdown"
              class="w-full rounded-xl py-3 pl-10 pr-10 text-left text-sm font-semibold text-gray-700"
            >
              <span v-if="selectedProgram !== 'all'">
                {{
                  availablePrograms.find(
                    (p) => Number(p.program_id) === Number(selectedProgram),
                  )?.program_code
                }}
              </span>

              <span v-else class="text-gray-600 font-light">
                Select All Programs
              </span>
            </button>

            <!-- Arrow -->
            <button
              type="button"
              @click="showProgramDropdown = !showProgramDropdown"
              class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 hover:text-defaultGreen"
            >
              <svg
                class="h-4 w-4 transition-transform duration-200"
                :class="{ 'rotate-180': showProgramDropdown }"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </button>
          </div>

          <!-- Dropdown -->
          <div
            v-if="showProgramDropdown"
            class="absolute z-50 mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
          >
            <div class="border-b border-gray-100 px-4 py-3">
              <p
                class="text-xs font-semibold uppercase tracking-wide text-gray-400"
              >
                Programs
              </p>
            </div>

            <div class="max-h-[260px] overflow-y-auto p-1.5">
              <!-- All -->
              <button
                @click="selectProgram('all')"
                class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                :class="selectedProgram === 'all' ? 'bg-green-50' : ''"
              >
                <div>
                  <p class="text-sm font-semibold text-gray-800">
                    All Programs
                  </p>
                </div>
              </button>

              <!-- Programs -->
              <button
                v-for="program in availablePrograms"
                :key="program.program_id"
                @click="selectProgram(program.program_id)"
                class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                :class="
                  Number(selectedProgram) === Number(program.program_id)
                    ? 'bg-green-50'
                    : ''
                "
              >
                <p class="text-sm font-semibold text-gray-800">
                  {{ program.program_code }}
                </p>

                <svg
                  v-if="Number(selectedProgram) === Number(program.program_id)"
                  class="h-5 w-5 text-defaultGreen"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
        <!-- Search -->
        <div class="search-wrapper">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search course, program, SY..."
            class="search-input"
            @input="changePage(1)"
          />
          <div class="search-icon">
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <circle cx="11" cy="11" r="8" />
              <path d="M21 21l-4.35-4.35" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div
      class="w-full mt-3 rounded-xl border bg-white overflow-y-auto max-h-[69vh]"
    >
      <table class="min-w-full text-sm text-gray-700">
        <thead class="bg-defaultGreen text-white">
          <tr>
            <!-- <th class="px-4 py-3 text-left">Campus</th> -->
            <th class="px-4 py-3 text-left">Course</th>
            <th class="px-4 py-3 text-center">Program</th>
            <th class="px-4 py-3 text-center">Type</th>
            <th class="px-4 py-3 text-center">School Year</th>
            <th class="px-4 py-3 text-center">Semester</th>
            <th class="px-4 py-3 text-center w-[14%]">Hours</th>
            <th class="px-4 py-3 text-center">Reason</th>
            <th class="px-4 py-3 text-center">Possible Faculty</th>
            <th class="px-4 py-3 text-center">Action</th>
            <!-- <th class="px-4 py-3 text-center">Created</th> -->
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="item in paginatedData"
            :key="item.id"
            class="border-t hover:bg-green-50"
          >
            <!-- <td class="px-4 py-3 font-semibold">
              {{ item.inter_branch || "-" }}
            </td> -->
            <td class="px-4 py-3 font-semibold">
              {{ item.course_code }}
            </td>

            <td class="px-4 py-3 text-center">
              {{ item.program_code }}
            </td>

            <td class="px-4 py-3 text-center">
              {{ item.type }}
            </td>

            <td class="px-4 py-3 text-center">
              {{ item.school_year }}
            </td>

            <td class="px-4 py-3 text-center">
              {{ semesterLabel(item.semester) }}
            </td>
            <td class="px-4 py-3 text-left">
              {{ item.hours }}
            </td>

            <td class="px-4 py-3 text-xs text-red-600 max-w-xs">
              {{ item.reason }}
            </td>

            <td class="px-4 py-3 text-xs text-center text-red-600 max-w-xs">
              {{ item.faculty_name === "Unassigned" ? "-" : item.faculty_name }}
            </td>
            <td class="px-4 py-3 text-xs text-red-600 max-w-xs">
              <button
                @click="assignMeeting(item)"
                class="px-3 py-1 text-xs bg-defaultGreen text-white rounded-md"
              >
                Assign
              </button>
            </td>
            <!-- <td class="px-4 py-3 text-center text-xs text-gray-500">
              {{ formatDate(item.created_at) }}
            </td> -->
          </tr>

          <tr v-if="paginatedData.length === 0">
            <td colspan="7" class="text-center py-8 text-gray-400">
              No unscheduled meetings found
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="flex justify-between items-center mt-4">
      <div class="text-gray-700 text-sm">
        Showing {{ startIndex }} to {{ endIndex }} of
        {{ filteredData.length }} entries
      </div>

      <div class="flex items-center gap-1 text-sm">
        <!-- Prev -->
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400"
        >
          &lt;
        </button>

        <!-- Page Numbers -->
        <span v-for="page in pageNumbers" :key="'page-' + page">
          <button
            @click="changePage(page)"
            :class="{
              'bg-defaultGreen text-white': currentPage === page,
              'bg-gray-200 text-gray-700': currentPage !== page,
            }"
            class="px-3 py-1 rounded-md hover:bg-green-300"
          >
            {{ page }}
          </button>
        </span>

        <!-- Next -->
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400"
        >
          &gt;
        </button>
      </div>
    </div>
  </div>
  <!-- Edit Schedule Modal -->
  <editUnschedule
    :show="showEditSchedule"
    :instructorData="selectedScheduleData"
    :activeSchoolYear="activeSchoolYear"
    @close="closeEditSchedule"
    @saved="handleScheduleSaved"
  />
</template>

<script>
import { useFetchDataStore } from "@/store/fetch-data-store";
import axios from "axios";
import { eventBus } from "@/bus/event-bus";
import editUnschedule from "../modals/edit-unscheduled.vue";
export default {
  name: "UnscheduledMeetingTable",
  components: {
    editUnschedule,
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      user: {},
      selectedProgram: "all",

      stopEventBus: null,
      activeSchoolYear: null,

      showProgramDropdown: false,

      showEditSchedule: false,

      // Data sent to edit-unscheduled.vue
      // Data sent to edit-unscheduled.vue
      editInstructorData: [],
      selectedScheduleData: [],
      showEditModal: false,
      selectedUnscheduledMeeting: null,

      // =========================================
      // FINAL GENERATED SCHEDULE DATA
      // =========================================
      finalSchedules: [],
      groupedSchedule: {},

      loadingSchedules: false,
    };
  },
  computed: {
    store() {
      return useFetchDataStore();
    },

    getTrimmedReason(reason) {
      if (!reason) return "-";

      // Keep only the first part before the long explanation
      return reason.split(" — ")[0].trim();
    },

    extractPossibleFaculty(reason) {
      if (!reason) return [];

      const marker = "possible faculty:";
      const index = reason.toLowerCase().indexOf(marker);

      if (index === -1) return [];

      const facultyPart = reason.substring(index + marker.length).trim();

      return facultyPart
        .split(",")
        .map((name) => name.trim())
        .filter(Boolean);
    },

    findFacultyUser(facultyName) {
      if (!facultyName) return null;

      const normalize = (value) =>
        String(value || "")
          .replace(/\s+/g, " ")
          .trim()
          .toLowerCase();

      const searchedName = normalize(facultyName);

      const rawUsers = this.store.rawusers || [];

      console.log("[Faculty Match] Searching:", searchedName);

      console.log("[Faculty Match] Raw users:", rawUsers);

      if (!rawUsers.length) {
        console.error("[Faculty Match] rawusers is EMPTY!");
        return null;
      }

      // =========================================
      // BUILD USER NAME
      // =========================================

      const getName = (user) => {
        const first = normalize(user.first_name || user.firstname);

        const middle = normalize(user.middle_name || user.middlename);

        const last = normalize(user.last_name || user.lastname);

        return {
          first,
          middle,
          last,
          full: [first, middle, last].filter(Boolean).join(" "),
        };
      };

      // =========================================
      // STEP 1
      // EXACT FULL NAME
      // =========================================

      let matches = rawUsers.filter((user) => {
        const n = getName(user);

        return n.full === searchedName;
      });

      console.log("[Faculty Match] Exact full-name matches:", matches);

      if (matches.length === 1) {
        return matches[0];
      }

      // =========================================
      // STEP 2
      // GET SEARCH FIRST/LAST
      // =========================================

      const parts = searchedName.split(" ");

      const searchLast = parts[parts.length - 1];

      const searchFirst = parts.slice(0, -1).join(" ");

      // =========================================
      // STEP 3
      // FIRST + LAST
      // =========================================

      matches = rawUsers.filter((user) => {
        const n = getName(user);

        const firstMatch =
          n.first === searchFirst ||
          n.first.startsWith(searchFirst) ||
          searchFirst.startsWith(n.first);

        const lastMatch = n.last === searchLast;

        return firstMatch && lastMatch;
      });

      console.log("[Faculty Match] First + last matches:", matches);

      if (matches.length === 1) {
        return matches[0];
      }

      // =========================================
      // STEP 4
      // SAME FIRST NAME?
      // CHECK MORE CONTENT
      // =========================================

      if (matches.length > 1) {
        console.warn(
          "[Faculty Match] Multiple matches:",
          matches.map((u) => getName(u).full),
        );

        // Compare complete searched string
        const exact = matches.find((user) => {
          return getName(user).full === searchedName;
        });

        if (exact) {
          return exact;
        }

        // Compare middle-name portion
        const searchMiddle = parts.slice(1, -1).join(" ");

        if (searchMiddle) {
          const middleMatches = matches.filter((user) => {
            const n = getName(user);

            return n.middle === searchMiddle || n.full.includes(searchMiddle);
          });

          console.log("[Faculty Match] Middle-name matches:", middleMatches);

          if (middleMatches.length === 1) {
            return middleMatches[0];
          }
        }

        // DO NOT randomly select one
        console.error("[Faculty Match] AMBIGUOUS FACULTY:", searchedName);

        return null;
      }

      // =========================================
      // STEP 5
      // NO MATCH
      // =========================================

      console.error("[Faculty Match] FACULTY NOT FOUND:", searchedName);

      return null;
    },

    getPossibleFaculty(item) {
      const names = this.extractPossibleFaculty(item.reason);

      return names.map((name) => {
        const user = this.findFacultyUser(name);

        return {
          name,
          user_id: user?.user_id || user?.id || null,
          user,
        };
      });
    },
    availablePrograms() {
      const programs = this.store.unscheduled_meetings
        .map((item) => ({
          program_id: item.program_id,
          program_code: item.program_code,
        }))
        .filter(
          (value, index, self) =>
            index === self.findIndex((p) => p.program_id === value.program_id),
        )
        .sort((a, b) => a.program_code.localeCompare(b.program_code));

      return programs;
    },

    filteredData() {
      const query = this.searchQuery.trim().toLowerCase();

      return (
        this.store.unscheduled_meetings
          // Role Filter
          .filter((item) => {
            // Admin
            if (this.user.role === "Admin") {
              if (this.selectedProgram === "all") return true;

              return Number(item.program_id) === Number(this.selectedProgram);
            }

            // Everyone else
            return Number(item.program_id) === Number(this.user.program_id);
          })

          // Active School Year
          .filter((item) => {
            if (!this.activeSchoolYear) return true;

            return (
              String(item.school_year) ===
                String(this.activeSchoolYear.school_year_name) &&
              String(item.semester) === String(this.activeSchoolYear.semester)
            );
          })
          // Search
          .filter((item) => {
            if (!query) return true;

            return (
              item.course_code?.toLowerCase().includes(query) ||
              item.program_code?.toLowerCase().includes(query) ||
              item.school_year?.toLowerCase().includes(query) ||
              item.reason?.toLowerCase().includes(query) ||
              item.type?.toLowerCase().includes(query) ||
              item.faculty_name?.toLowerCase().includes(query)
            );
          })

          // Sort newest first
          .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      );
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredData.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;
    },

    pageNumbers() {
      const total = this.totalPages;

      if (total <= 3) {
        return Array.from({ length: total }, (_, i) => i + 1);
      }

      let start = this.currentPage - 1;
      let end = this.currentPage + 1;

      if (start < 1) {
        start = 1;
        end = 3;
      }

      if (end > total) {
        end = total;
        start = total - 2;
      }

      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    },

    startIndex() {
      return this.filteredData.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(
        this.currentPage * this.itemsPerPage,
        this.filteredData.length,
      );
    },
  },

  methods: {
    resolveFacultyForAssignment(item) {
      if (!item) return null;

      // =========================================
      // 1. GET POSSIBLE FACULTY FROM REASON
      // =========================================

      const reason = String(item.reason || "");

      const marker = "possible faculty:";
      const markerIndex = reason.toLowerCase().indexOf(marker);

      if (markerIndex === -1) {
        console.error("[ASSIGN] No possible faculty found in reason:", reason);

        return null;
      }

      const facultyName = reason
        .substring(markerIndex + marker.length)
        .split(" — ")[0]
        .split(" - ")[0]
        .split(",")[0]
        .trim();

      console.log("[ASSIGN] Possible faculty extracted:", facultyName);

      if (!facultyName) {
        return null;
      }

      // =========================================
      // 2. RAW USERS
      // =========================================

      const rawUsers = this.store.rawusers || [];

      if (!rawUsers.length) {
        console.error("[ASSIGN] rawusers is empty.");

        return null;
      }

      // =========================================
      // 3. NORMALIZE
      // =========================================

      const normalize = (value) =>
        String(value || "")
          .replace(/\s+/g, " ")
          .trim()
          .toLowerCase();

      const searchedName = normalize(facultyName);

      // =========================================
      // 4. BUILD USER NAME
      // =========================================

      const getUserName = (user) => {
        const firstName = normalize(user.first_name || user.firstname);

        const middleName = normalize(user.middle_name || user.middlename);

        const lastName = normalize(user.last_name || user.lastname);

        const suffix = normalize(user.suffix);

        return {
          firstName,
          middleName,
          lastName,
          suffix,

          fullName: [firstName, middleName, lastName, suffix]
            .filter(Boolean)
            .join(" "),
        };
      };

      // =========================================
      // 5. EXACT FULL NAME FIRST
      // =========================================

      let matches = rawUsers.filter((user) => {
        const name = getUserName(user);

        return name.fullName === searchedName;
      });

      console.log("[ASSIGN] Exact name matches:", matches);

      if (matches.length === 1) {
        const user = matches[0];

        return {
          faculty_id: user.user_id || user.id,
          faculty_name: getUserName(user).fullName || facultyName,
          user,
        };
      }

      // =========================================
      // 6. FIRST NAME + LAST NAME
      // =========================================

      const parts = searchedName.split(" ");

      const searchLastName = parts[parts.length - 1];

      const searchFirstName = parts.slice(0, -1).join(" ");

      matches = rawUsers.filter((user) => {
        const name = getUserName(user);

        const firstMatch =
          name.firstName === searchFirstName ||
          name.firstName.includes(searchFirstName) ||
          searchFirstName.includes(name.firstName);

        const lastMatch = name.lastName === searchLastName;

        return firstMatch && lastMatch;
      });

      console.log(
        "[ASSIGN] First + last matches:",
        matches.map((user) => getUserName(user).fullName),
      );

      if (matches.length === 1) {
        const user = matches[0];

        return {
          faculty_id: user.user_id || user.id,
          faculty_name: getUserName(user).fullName || facultyName,
          user,
        };
      }

      // =========================================
      // 7. MULTIPLE MATCHES
      // =========================================

      if (matches.length > 1) {
        console.warn(
          "[ASSIGN] Multiple faculty matches:",
          matches.map((user) => getUserName(user).fullName),
        );

        // Try exact full name again
        const exactMatch = matches.find((user) => {
          return getUserName(user).fullName === searchedName;
        });

        if (exactMatch) {
          return {
            faculty_id: exactMatch.user_id || exactMatch.id,

            faculty_name: getUserName(exactMatch).fullName,

            user: exactMatch,
          };
        }

        // Do NOT randomly choose matches[0]
        console.error("[ASSIGN] Ambiguous faculty:", facultyName);

        return null;
      }

      // =========================================
      // 8. NOT FOUND
      // =========================================

      console.error("[ASSIGN] Faculty not found:", facultyName);

      return null;
    },
    async handleScheduleSaved(savedData) {
      console.log("[Table Unscheduled] Schedule saved:", savedData);

      // Close modal
      this.showEditSchedule = false;

      // Refresh final-generated schedules
      await this.fetchFinalSchedules();

      // Refresh unscheduled meetings
      await this.store.fetchUnscheduledMeetings();

      // Reset selected data
      this.selectedScheduleData = [];
    },

    async fetchFinalSchedules() {
      this.loadingSchedules = true;

      try {
        // =========================================
        // 1. GET FINAL GENERATED SCHEDULES
        // =========================================
        const { data: schedulesData } = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/get-all-final-schedules`,
          {
            withCredentials: true,
          },
        );

        // =========================================
        // 2. GET CLASS SECTIONS
        // Needed for set_name / class information
        // =========================================
        const { data: classSections } = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/class/get-classes`,
          {
            withCredentials: true,
          },
        );

        // =========================================
        // 3. GET RAW USERS
        // Needed to reliably identify faculty
        // =========================================
        const store = useFetchDataStore();

        if (!store.rawusers?.length) {
          await store.fetchRawUsers();
        }

        const rawUsers = store.rawusers || [];

        let schedules = Array.isArray(schedulesData) ? schedulesData : [];

        // =========================================
        // 4. SAME SCHOOL YEAR / SEMESTER
        // =========================================
        if (this.activeSchoolYear) {
          schedules = schedules.filter(
            (schedule) =>
              String(schedule.school_year).trim() ===
                String(this.activeSchoolYear.school_year_name).trim() &&
              Number(schedule.semester) ===
                Number(this.activeSchoolYear.semester),
          );
        }

        // =========================================
        // 5. ATTACH CLASS INFORMATION
        // =========================================
        schedules = schedules.map((schedule) => {
          const classInfo = classSections.find(
            (cls) => Number(cls.class_id) === Number(schedule.class_id),
          );

          const faculty = rawUsers.find(
            (user) =>
              Number(user.id || user.user_id) === Number(schedule.faculty_id),
          );

          return {
            ...schedule,

            classInfo: classInfo || null,

            // Class ownership
            class_program_id:
              classInfo?.program_id || schedule.class_program_id || null,

            class_institute_id:
              classInfo?.program?.institute_id ||
              schedule.class_institute_id ||
              null,

            // Section
            set_name: classInfo?.set_name || schedule.set_name || "",

            class_size: classInfo?.class_size || schedule.class_size || null,

            // Faculty information
            faculty_name:
              schedule.faculty_name ||
              (faculty
                ? `${faculty.first_name || ""} ${
                    faculty.last_name || ""
                  }`.trim()
                : "Unknown Faculty"),

            faculty_id:
              schedule.faculty_id || faculty?.id || faculty?.user_id || null,

            faculty_program_id:
              faculty?.program?.program_id ||
              schedule.faculty_program_id ||
              null,

            faculty_institute_id:
              faculty?.institute?.institute_id ||
              schedule.faculty_institute_id ||
              null,
          };
        });

        // =========================================
        // 6. SAVE FINAL SCHEDULES
        // =========================================
        this.finalSchedules = schedules;

        // =========================================
        // 7. GROUP BY INSTRUCTOR
        // =========================================
        this.groupedSchedule = this.groupByInstructor(this.finalSchedules);

        console.log(
          "[Table Unscheduled] Final generated schedules:",
          this.finalSchedules.length,
        );

        console.log(
          "[Table Unscheduled] Grouped schedule:",
          this.groupedSchedule,
        );
      } catch (error) {
        console.error(
          "[Table Unscheduled] Failed to fetch final schedules:",
          error.response?.data || error,
        );

        this.finalSchedules = [];
        this.groupedSchedule = {};
      } finally {
        this.loadingSchedules = false;
      }
    },
    groupByInstructor(schedules) {
      return (schedules || []).reduce((groups, schedule) => {
        const instructor = schedule.faculty_name || "Unknown Faculty";

        if (!groups[instructor]) {
          groups[instructor] = [];
        }

        groups[instructor].push(schedule);

        return groups;
      }, {});
    },
    async assignMeeting(item) {
      if (!item) return;

      console.log("[ASSIGN] Selected item:", item);

      // =========================================================
      // 1. RESOLVE POSSIBLE FACULTY
      // =========================================================

      const faculty = this.resolveFacultyForAssignment(item);

      if (!faculty) {
        console.error("[ASSIGN] Cannot assign faculty.");
        return;
      }

      const facultyId = faculty.faculty_id;
      const facultyName = faculty.faculty_name;

      console.log("[ASSIGN] Resolved faculty:", faculty);

      // =========================================================
      // 2. GET EXISTING FACULTY SCHEDULES
      // =========================================================

      const instructorSchedules = (this.finalSchedules || [])
        .filter((schedule) => {
          return (
            Number(schedule.faculty_id) === Number(facultyId) &&
            String(schedule.school_year).trim() ===
              String(item.school_year).trim() &&
            Number(schedule.semester) === Number(item.semester)
          );
        })
        .map((schedule) => ({
          ...structuredClone(schedule),

          // IMPORTANT:
          // Existing schedules must NEVER be treated as unscheduled.
          isUnscheduledMeeting: false,
          isNew: false,

          unscheduled_id: null,
          unscheduled_meeting_id: null,
        }));

      // =========================================================
      // 3. FIND SECTION
      // =========================================================

      const store = useFetchDataStore();

      const sections = store.sections || [];

      const section = sections.find(
        (s) => Number(s.class_id) === Number(item.class_id),
      );

      console.log("[ASSIGN] Matched section:", section);

      // =========================================================
      // 4. GET REAL UNSCHEDULED ID
      // =========================================================

      const unscheduledId =
        item.unscheduled_id ?? item.unscheduled_meeting_id ?? item.id ?? null;

      if (!unscheduledId) {
        console.error("[ASSIGN] UNSCHEDULED MEETING HAS NO ID:", item);
        return;
      }

      // =========================================================
      // 5. CREATE SELECTED UNSCHEDULED RECORD
      // =========================================================

      const selectedMeeting = {
        ...structuredClone(item),

        // IMPORTANT IDENTIFIERS
        id: item.id ?? unscheduledId,

        unscheduled_id: unscheduledId,

        unscheduled_meeting_id:
          item.unscheduled_meeting_id ?? item.unscheduled_id ?? unscheduledId,

        // IMPORTANT FLAG
        isUnscheduledMeeting: true,
        isNew: true,

        // =======================================================
        // FACULTY
        // =======================================================

        faculty_id: facultyId,
        faculty_name: facultyName,

        // =======================================================
        // CLASS / SECTION
        // =======================================================

        class_id: item.class_id ?? section?.class_id ?? null,

        class_size: item.class_size ?? section?.class_size ?? 0,

        set_name: item.set_name ?? section?.set_name ?? "",

        // =======================================================
        // COURSE
        // =======================================================

        course_id: item.course_id ?? null,

        course_code: item.course_code ?? "",

        // =======================================================
        // PROGRAM
        // =======================================================

        program_id: item.program_id ?? section?.program_id ?? null,

        program_code: item.program_code ?? section?.program?.program_code ?? "",

        // =======================================================
        // SCHOOL YEAR / SEMESTER
        // =======================================================

        school_year:
          item.school_year ?? this.activeSchoolYear?.school_year_name ?? "",

        semester: item.semester ?? this.activeSchoolYear?.semester ?? "",

        // =======================================================
        // DO NOT INVENT SCHEDULE
        // =======================================================

        day: null,
        start_hour: null,
        duration: null,

        // =======================================================
        // FORM SEARCH VALUES
        // =======================================================

        searchSectionQuery: item.set_name ?? section?.set_name ?? "",

        searchCourseQuery: item.course_code ?? "",

        searchRoomQuery: item.room_name ?? "",

        searchCampusQuery: item.college_branch_name ?? "",

        showSectionDropdown: false,
        showCourseDropdown: false,
        showRoomDropdown: false,
        showCampusDropdown: false,
      };

      console.log("[ASSIGN] FINAL UNSCHEDULED RECORD:", selectedMeeting);

      // =========================================================
      // 6. IMPORTANT:
      // SEND EXISTING SCHEDULES + SELECTED UNSCHEDULED RECORD
      // =========================================================

      this.selectedScheduleData = [...instructorSchedules, selectedMeeting];

      // =========================================================
      // 7. VERIFY BEFORE OPENING MODAL
      // =========================================================

      const verifyUnscheduled = this.selectedScheduleData.find(
        (record) =>
          record.isUnscheduledMeeting === true &&
          (record.unscheduled_id != null ||
            record.unscheduled_meeting_id != null),
      );

      console.log("[ASSIGN] UNSCHEDULED RECORD BEING SENT:", verifyUnscheduled);

      if (!verifyUnscheduled) {
        console.error(
          "[ASSIGN] FAILED: No unscheduled record in selectedScheduleData",
          this.selectedScheduleData,
        );

        return;
      }

      // =========================================================
      // 8. OPEN EDIT SCHEDULE
      // =========================================================

      this.showEditSchedule = false;

      await this.$nextTick();

      this.showEditSchedule = true;

      console.log(
        "[ASSIGN] Edit Schedule opened with:",
        this.selectedScheduleData,
      );
    },
    selectProgram(programId) {
      this.selectedProgram = programId;
      this.showProgramDropdown = false;
      this.changePage(1);
    },

    handleClickOutside(event) {
      if (
        this.$refs.programDropdownRef &&
        !this.$refs.programDropdownRef.contains(event.target)
      ) {
        this.showProgramDropdown = false;
      }
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },

    semesterLabel(sem) {
      return sem === "1" ? "1st Semester" : sem === "2" ? "2nd Semester" : sem;
    },

    formatDate(date) {
      return new Date(date).toLocaleString();
    },

    async fetchUser() {
      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/auth/me`,
          {
            withCredentials: true,
          },
        );
        this.user = res.data || {};
      } catch {
        this.user = {};
      }
    },
  },
  async mounted() {
    await this.fetchUser();

    // Load unscheduled meetings
    await this.store.fetchUnscheduledMeetings();

    // Get active school year
    this.activeSchoolYear = eventBus.data || null;

    // IMPORTANT:
    // Load final generated schedules BEFORE Assign is clicked
    await this.fetchFinalSchedules();

    // Listen for school year changes
    this.stopEventBus = eventBus.on(async (newYear) => {
      if (!newYear) return;

      console.log("[Table Unscheduled] NEW ACTIVE YEAR:", newYear);

      this.activeSchoolYear = {
        ...newYear,
      };

      this.currentPage = 1;

      // Refresh final generated schedules
      await this.fetchFinalSchedules();

      // Refresh unscheduled meetings
      await this.store.fetchUnscheduledMeetings();
    });

    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
    if (this.stopEventBus) {
      this.stopEventBus();
    }
  },
};
</script>
