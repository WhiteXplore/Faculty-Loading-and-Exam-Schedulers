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
                class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-defaultGreen hover:text-white"
                :class="
                  selectedProgram === 'all' ? 'bg-defaultGreen text-white' : ''
                "
              >
                <div>
                  <p class="text-sm">All Programs</p>
                </div>
              </button>

              <!-- Programs -->
              <button
                v-for="program in availablePrograms"
                :key="program.program_id"
                @click="selectProgram(program.program_id)"
                class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-defaultGreen hover:text-white"
                :class="
                  Number(selectedProgram) === Number(program.program_id)
                    ? 'bg-defaultGreen text-white'
                    : ''
                "
              >
                <p class="text-sm">
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
            <th class="px-4 py-3 text-left w-[6%]">Course</th>
            <th class="px-4 py-3 text-center">Section</th>
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
              {{ getSetName(item) }}
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
              <button @click="assignMeeting(item)" class="btn-save">
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
  <!-- Faculty Selection Modal -->
  <div
    v-if="showFacultySelectionModal"
    class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 px-4"
  >
    <div
      class="w-full max-w-3xl rounded-2xl bg-white shadow-2xl overflow-hidden"
    >
      <!-- Header -->
      <div class="flex items-center justify-between border-b px-6 py-4">
        <div>
          <h2 class="text-lg font-bold text-gray-800">Select Faculty</h2>

          <p class="mt-1 text-sm text-gray-500">
            Multiple possible faculty were found for this unscheduled meeting.
          </p>
        </div>

        <button
          type="button"
          @click="closeFacultySelectionModal"
          class="flex h-9 w-9 items-center justify-center rounded-full text-gray-400 hover:bg-gray-100 hover:text-gray-700"
        >
          ✕
        </button>
      </div>

      <!-- Information -->
      <div class="border-b bg-gray-50 px-6 py-4">
        <div class="grid grid-cols-1 gap-3 md:grid-cols-3">
          <div>
            <p class="text-xs font-semibold uppercase text-gray-400">Course</p>

            <p class="mt-1 font-semibold text-gray-700">
              {{ pendingUnscheduledMeeting?.course_code || "-" }}
            </p>
          </div>

          <div>
            <p class="text-xs font-semibold uppercase text-gray-400">Program</p>

            <p class="mt-1 font-semibold text-gray-700">
              {{ pendingUnscheduledMeeting?.program_code || "-" }}
            </p>
          </div>

          <div>
            <p class="text-xs font-semibold uppercase text-gray-400">Section</p>

            <p class="mt-1 font-semibold text-gray-700">
              {{ getSetName(pendingUnscheduledMeeting) }}
            </p>
          </div>
        </div>
      </div>

      <!-- Faculty List -->
      <div class="max-h-[55vh] overflow-y-auto p-6">
        <div
          v-for="candidate in possibleFacultyCandidates"
          :key="candidate.faculty_id"
          class="mb-3 flex items-center justify-between rounded-xl border border-gray-200 bg-white p-4 transition hover:border-defaultGreen hover:bg-green-50"
        >
          <div class="min-w-0">
            <div class="flex items-center gap-2">
              <h3 class="font-semibold text-gray-800">
                {{ candidate.full_name }}
              </h3>

              <!-- Priority badge -->
              <span
                v-if="candidate.isProgramChairMatch"
                class="rounded-full bg-green-100 px-2 py-1 text-[10px] font-bold text-green-700"
              >
                YOUR INSTITUTE / PROGRAM
              </span>
            </div>

            <div
              class="mt-2 grid grid-cols-1 gap-1 text-sm text-gray-500 md:grid-cols-2"
            >
              <div>
                <span class="font-medium text-gray-600"> Institute: </span>

                {{ candidate.institute_name || "-" }}
              </div>

              <div>
                <span class="font-medium text-gray-600"> Program: </span>

                {{ candidate.program_name || "-" }}
              </div>
            </div>
          </div>

          <button
            type="button"
            @click="selectFacultyCandidate(candidate)"
            class="ml-4 shrink-0 rounded-lg bg-defaultGreen px-4 py-2 text-sm font-semibold text-white transition hover:opacity-90"
          >
            Assign
          </button>
        </div>

        <div
          v-if="possibleFacultyCandidates.length === 0"
          class="py-10 text-center text-gray-400"
        >
          No matching faculty found.
        </div>
      </div>

      <!-- Footer -->
      <div class="flex justify-end border-t bg-gray-50 px-6 py-4">
        <button
          type="button"
          @click="closeFacultySelectionModal"
          class="rounded-lg border border-gray-300 bg-white px-5 py-2 text-sm font-semibold text-gray-600 hover:bg-gray-100"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
  <!-- Edit Schedule Modal -->
  <editUnschedule
    :show="showEditSchedule"
    :instructorData="selectedScheduleData"
    :unscheduledMeeting="selectedUnscheduledMeeting"
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

      // Faculty selection modal
      showFacultySelectionModal: false,
      possibleFacultyCandidates: [],
      selectedFacultyCandidate: null,
      pendingUnscheduledMeeting: null,
    };
  },
  computed: {
    store() {
      return useFetchDataStore();
    },
    // FETCH CLASS SECTION IN THE API
    classSections() {
      return this.store.sections || [];
    },

    getSetName() {
      return (item) => {
        const section = this.classSections.find(
          (cls) => Number(cls.class_id) === Number(item.class_id),
        );

        return section?.set_name || "-";
      };
    },
    getTrimmedReason(reason) {
      if (!reason) return "-";

      // Keep only the first part before the long explanation
      return reason.split(" — ")[0].trim();
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
    extractPossibleFaculty(reason) {
      if (reason === null || reason === undefined) {
        return [];
      }

      let reasonText = "";

      if (typeof reason === "string") {
        reasonText = reason;
      } else if (Array.isArray(reason)) {
        reasonText = reason.join(", ");
      } else if (typeof reason === "object") {
        reasonText =
          reason.reason ||
          reason.message ||
          reason.description ||
          reason.text ||
          "";
      } else {
        reasonText = String(reason);
      }

      reasonText = String(reasonText).replace(/\s+/g, " ").trim();

      if (!reasonText) {
        return [];
      }

      const marker = "possible faculty:";
      const lowerReason = reasonText.toLowerCase();
      const index = lowerReason.indexOf(marker);

      if (index === -1) {
        return [];
      }

      let facultyPart = reasonText.substring(index + marker.length).trim();

      // Remove anything after the possible-faculty list
      facultyPart = facultyPart.split(" — ")[0].split(" - ")[0].trim();

      if (!facultyPart) {
        return [];
      }

      return facultyPart
        .split(",")
        .map((name) => name.trim())
        .filter(Boolean);
    },

    getPossibleFaculty(item) {
      const names = this.extractPossibleFaculty(item?.reason);

      return names.map((name) => {
        const user = this.findFacultyUser(name);

        return {
          name,
          user_id: user?.user_id || user?.id || null,
          user,
        };
      });
    },

    getLoggedInProgramChairScope() {
      const user = this.user || {};

      return {
        instituteId:
          user.institute_id ??
          user.institute?.institute_id ??
          user.institute?.id ??
          null,

        instituteName:
          user.institute_name ??
          user.institute?.institute_name ??
          user.institute?.name ??
          "",

        programId:
          user.program_id ??
          user.program?.program_id ??
          user.program?.id ??
          user.program_id ??
          null,

        programName:
          user.program_name ??
          user.program?.program_name ??
          user.program?.name ??
          "",

        programCode: user.program_code ?? user.program?.program_code ?? "",
      };
    },
    getPossibleFacultyCandidates(item) {
      if (!item) return [];

      const names = this.extractPossibleFaculty(item.reason);

      if (!Array.isArray(names) || !names.length) {
        console.warn("[ASSIGN] No possible faculty names found:", item.reason);

        return [];
      }

      const rawUsers = this.store.rawusers || [];

      if (!rawUsers.length) {
        console.warn("[ASSIGN] rawusers is empty.");
        return [];
      }

      const scope = this.getLoggedInProgramChairScope();

      const normalize = (value) =>
        String(value ?? "")
          .replace(/\s+/g, " ")
          .trim()
          .toLowerCase();

      const getFullName = (user) => {
        return [
          user.first_name || user.firstname,
          user.middle_name || user.middlename,
          user.last_name || user.lastname,
          user.suffix,
        ]
          .filter(Boolean)
          .join(" ")
          .replace(/\s+/g, " ")
          .trim();
      };

      const getInstituteId = (user) =>
        user.institute_id ??
        user.institute?.institute_id ??
        user.institute?.id ??
        user.faculty_institute_id ??
        null;

      const getInstituteName = (user) =>
        user.institute_name ??
        user.institute?.institute_name ??
        user.institute?.name ??
        "";

      const getProgramId = (user) =>
        user.program_id ??
        user.program?.program_id ??
        user.program?.id ??
        user.faculty_program_id ??
        null;

      const getProgramName = (user) =>
        user.program_name ??
        user.program?.program_name ??
        user.program?.name ??
        "";

      const getProgramCode = (user) =>
        user.program_code ?? user.program?.program_code ?? "";

      const candidates = [];

      names.forEach((name) => {
        const searchedName = normalize(name);

        if (!searchedName) return;

        const matches = rawUsers.filter((user) => {
          const fullName = normalize(getFullName(user));

          return fullName === searchedName;
        });

        matches.forEach((user) => {
          const facultyId = user.faculty_id ?? user.user_id ?? user.id ?? null;

          if (!facultyId) return;

          const instituteId = getInstituteId(user);
          const programId = getProgramId(user);

          const sameInstitute =
            scope.instituteId != null &&
            instituteId != null &&
            Number(scope.instituteId) === Number(instituteId);

          const sameProgram =
            scope.programId != null &&
            programId != null &&
            Number(scope.programId) === Number(programId);

          candidates.push({
            faculty_id: facultyId,
            full_name: getFullName(user) || name,

            institute_id: instituteId,
            institute_name: getInstituteName(user),

            program_id: programId,
            program_name: getProgramName(user),
            program_code: getProgramCode(user),

            user,

            isProgramChairMatch: sameInstitute && sameProgram,

            isInstituteMatch: sameInstitute,

            isProgramMatch: sameProgram,
          });
        });
      });

      // Remove duplicate faculty
      const uniqueCandidates = candidates.filter(
        (candidate, index, self) =>
          index ===
          self.findIndex(
            (item) => Number(item.faculty_id) === Number(candidate.faculty_id),
          ),
      );

      // Priority:
      // 1. Same Institute + Program
      // 2. Same Institute
      // 3. Same Program
      // 4. Other faculty
      return uniqueCandidates.sort((a, b) => {
        const score = (candidate) => {
          if (candidate.isProgramChairMatch) return 3;
          if (candidate.isInstituteMatch) return 2;
          if (candidate.isProgramMatch) return 1;
          return 0;
        };

        return score(b) - score(a);
      });
    },
    openFacultySelectionModal(item, candidates) {
      this.pendingUnscheduledMeeting = structuredClone(item);

      this.possibleFacultyCandidates = candidates;

      this.selectedFacultyCandidate = null;

      this.showFacultySelectionModal = true;
    },
    closeFacultySelectionModal() {
      this.showFacultySelectionModal = false;
      this.possibleFacultyCandidates = [];
      this.selectedFacultyCandidate = null;
      this.pendingUnscheduledMeeting = null;
    },
    async selectFacultyCandidate(candidate) {
      if (!candidate) return;

      this.selectedFacultyCandidate = candidate;

      const item = this.pendingUnscheduledMeeting;

      this.closeFacultySelectionModal();

      if (!item) return;

      const assignedItem = {
        ...structuredClone(item),

        faculty_id: candidate.faculty_id,
        faculty_name: candidate.full_name,

        faculty_institute_id: candidate.institute_id,
        faculty_institute_name: candidate.institute_name,

        faculty_program_id: candidate.program_id,
        faculty_program_name: candidate.program_name,
        faculty_program_code: candidate.program_code,
      };

      console.log(
        "[ASSIGN] Faculty manually selected from modal:",
        assignedItem,
      );

      // Continue through the existing assignment process
      await this.assignMeeting(assignedItem);
    },
    findFacultyUser(facultyName) {
      if (!facultyName) return null;

      const normalize = (value) => {
        if (value === null || value === undefined) return "";

        if (typeof value === "object") {
          const name =
            value.faculty_name ||
            value.name ||
            value.full_name ||
            value.fullName ||
            [
              value.first_name || value.firstname,
              value.middle_name || value.middlename,
              value.last_name || value.lastname,
              value.suffix,
            ]
              .filter(Boolean)
              .join(" ");

          return String(name).replace(/\s+/g, " ").trim().toLowerCase();
        }

        return String(value).replace(/\s+/g, " ").trim().toLowerCase();
      };

      const searchedName = normalize(facultyName);

      if (!searchedName) {
        console.warn("[FACULTY] Empty faculty name");
        return null;
      }

      const rawUsers = this.store.rawusers || [];

      console.log("[FACULTY] Searching for:", searchedName);
      console.log("[FACULTY] Available users:", rawUsers);

      if (!rawUsers.length) {
        console.error("[FACULTY] rawusers is empty");
        return null;
      }

      const getUserName = (user) => {
        const first = normalize(user.first_name || user.firstname);
        const middle = normalize(user.middle_name || user.middlename);
        const last = normalize(user.last_name || user.lastname);
        const suffix = normalize(user.suffix);

        return {
          first,
          middle,
          last,
          suffix,
          full: [first, middle, last, suffix].filter(Boolean).join(" "),
        };
      };

      // ==========================================
      // 1. EXACT FULL NAME
      // ==========================================

      let matches = rawUsers.filter((user) => {
        return getUserName(user).full === searchedName;
      });

      console.log(
        "[FACULTY] Exact matches:",
        matches.map((u) => getUserName(u).full),
      );

      if (matches.length === 1) {
        return matches[0];
      }

      // ==========================================
      // 2. FIRST + LAST NAME
      // ==========================================

      const parts = searchedName.split(" ").filter(Boolean);

      if (parts.length >= 2) {
        const searchLast = parts[parts.length - 1];
        const searchFirst = parts.slice(0, -1).join(" ");

        matches = rawUsers.filter((user) => {
          const name = getUserName(user);

          const firstMatch =
            name.first === searchFirst ||
            name.first.startsWith(searchFirst) ||
            searchFirst.startsWith(name.first);

          const lastMatch = name.last === searchLast;

          return firstMatch && lastMatch;
        });

        console.log(
          "[FACULTY] First + last matches:",
          matches.map((u) => getUserName(u).full),
        );
      }

      if (matches.length === 1) {
        return matches[0];
      }

      // ==========================================
      // 3. CHECK MIDDLE NAME
      // ==========================================

      if (matches.length > 1) {
        const searchMiddle = parts.slice(1, -1).join(" ");

        if (searchMiddle) {
          const middleMatches = matches.filter((user) => {
            const name = getUserName(user);

            return (
              name.middle === searchMiddle || name.full.includes(searchMiddle)
            );
          });

          if (middleMatches.length === 1) {
            return middleMatches[0];
          }
        }

        console.error("[FACULTY] Ambiguous faculty:", facultyName);

        return null;
      }

      console.error("[FACULTY] Faculty not found:", facultyName);

      return null;
    },
    closeEditSchedule() {
      this.showEditSchedule = false;
    },
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

      // Immediately close modal
      this.showEditSchedule = false;

      // Use the already-saved data immediately
      if (Array.isArray(savedData) && savedData.length) {
        this.finalSchedules = savedData;
      }

      this.selectedScheduleData = [];

      // Refresh unscheduled list in background
      this.store.fetchUnscheduledMeetings().catch((error) => {
        console.error("Failed to refresh unscheduled meetings:", error);
      });
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
    resolveCollegeBranch(item, section = null) {
      if (!item && !section) {
        return {
          college_branch_id: null,
          college_branch_name: "",
        };
      }

      // =========================================
      // 1. GET BRANCH ID
      // =========================================
      const branchId =
        item?.college_branch_id ??
        item?.collegeBranchId ??
        item?.college_branch?.college_branch_id ??
        item?.collegeBranch?.college_branch_id ??
        section?.college_branch_id ??
        section?.collegeBranchId ??
        section?.college_branch?.college_branch_id ??
        section?.collegeBranch?.college_branch_id ??
        section?.classInfo?.college_branch_id ??
        section?.classInfo?.collegeBranch?.college_branch_id ??
        null;

      const normalizedBranchId =
        branchId !== null && branchId !== undefined && branchId !== ""
          ? Number(branchId)
          : null;

      // =========================================
      // 2. GET BRANCH NAME
      // =========================================
      const branchName =
        item?.college_branch_name ||
        item?.collegeBranchName ||
        item?.college_branch?.college_branch_name ||
        item?.collegeBranch?.college_branch_name ||
        section?.college_branch_name ||
        section?.collegeBranchName ||
        section?.college_branch?.college_branch_name ||
        section?.collegeBranch?.college_branch_name ||
        section?.classInfo?.college_branch_name ||
        section?.classInfo?.collegeBranch?.college_branch_name ||
        "";

      return {
        college_branch_id: normalizedBranchId,
        college_branch_name: branchName,
      };
    },
    async assignMeeting(item) {
      if (!item) return;

      // Make sure faculty data is available
      if (!this.store.rawusers?.length && this.store.fetchRawUsers) {
        await this.store.fetchRawUsers();
      }

      // =====================================================
      // 0. RESOLVE FACULTY
      // =====================================================
      let faculty = null;

      /*
       * FACULTY RESOLUTION PRIORITY
       *
       * 1. Existing faculty_id
       * 2. Existing faculty_name
       * 3. Possible faculty from reason
       *
       * This allows records such as:
       *
       * faculty_name: "Boyeth Pelone"
       * reason: "Unresolved after repair pass —
       *          no Laboratory room available..."
       *
       * to automatically use Boyeth Pelone.
       */

      // -----------------------------------------------------
      // 0.1 EXISTING FACULTY ID
      // -----------------------------------------------------
      if (
        item.faculty_id != null &&
        item.faculty_id !== "" &&
        item.faculty_name &&
        String(item.faculty_name).trim().toLowerCase() !== "unassigned"
      ) {
        faculty = {
          faculty_id: item.faculty_id,
          faculty_name: item.faculty_name,
        };

        console.log("[ASSIGN] Using existing faculty_id:", faculty);
      }

      // -----------------------------------------------------
      // 0.2 EXISTING FACULTY NAME
      // -----------------------------------------------------
      if (!faculty && item.faculty_name) {
        let facultyName = item.faculty_name;

        // Handle faculty_name if it is an object
        if (typeof facultyName === "object") {
          facultyName =
            facultyName.faculty_name ||
            facultyName.name ||
            facultyName.full_name ||
            facultyName.fullName ||
            [
              facultyName.first_name || facultyName.firstname,
              facultyName.middle_name || facultyName.middlename,
              facultyName.last_name || facultyName.lastname,
              facultyName.suffix,
            ]
              .filter(Boolean)
              .join(" ");
        }

        facultyName = String(facultyName || "").trim();

        if (
          facultyName &&
          facultyName.toLowerCase() !== "unassigned" &&
          facultyName !== "-"
        ) {
          console.log("[ASSIGN] Faculty name found:", facultyName);

          const matchedUser = this.findFacultyUser(facultyName);

          console.log("[ASSIGN] Matched faculty user:", matchedUser);

          if (matchedUser) {
            const matchedFacultyId =
              matchedUser.faculty_id ?? matchedUser.user_id ?? matchedUser.id;

            if (!matchedFacultyId) {
              console.error(
                "[ASSIGN] Faculty matched but NO faculty ID found:",
                matchedUser,
              );
              return;
            }

            const matchedFacultyName = [
              matchedUser.first_name || matchedUser.firstname,
              matchedUser.middle_name || matchedUser.middlename,
              matchedUser.last_name || matchedUser.lastname,
              matchedUser.suffix,
            ]
              .filter(Boolean)
              .join(" ");

            faculty = {
              faculty_id: matchedFacultyId,
              faculty_name: matchedFacultyName || facultyName,
              user: matchedUser,
            };

            console.log("[ASSIGN] FACULTY SUCCESSFULLY RESOLVED:", faculty);
          } else {
            console.error("[ASSIGN] Could not find faculty:", facultyName);

            return;
          }
        }
      }

      // -----------------------------------------------------
      // 0.3 POSSIBLE FACULTY FROM REASON
      // -----------------------------------------------------
      if (!faculty) {
        console.log(
          "[ASSIGN] No existing faculty resolved. Checking possible faculty...",
        );

        const candidates = this.getPossibleFacultyCandidates(item);

        console.log("[ASSIGN] Possible faculty candidates:", candidates);

        if (!candidates.length) {
          console.error("[ASSIGN] No possible faculty candidates found.");

          return;
        }

        // =====================================================
        // PROGRAM CHAIR PRIORITY
        // =====================================================

        const programChairCandidates = candidates.filter(
          (candidate) => candidate.isProgramChairMatch,
        );

        console.log(
          "[ASSIGN] Program Chair matching faculty:",
          programChairCandidates,
        );

        // -----------------------------------------------------
        // CASE 1:
        // Exactly ONE faculty belongs to the logged-in
        // Program Chair's institute + program
        // -----------------------------------------------------

        if (programChairCandidates.length === 1) {
          const candidate = programChairCandidates[0];

          faculty = {
            faculty_id: candidate.faculty_id,
            faculty_name: candidate.full_name,
            user: candidate.user,

            faculty_institute_id: candidate.institute_id,
            faculty_institute_name: candidate.institute_name,

            faculty_program_id: candidate.program_id,
            faculty_program_name: candidate.program_name,
            faculty_program_code: candidate.program_code,
          };

          console.log(
            "[ASSIGN] Automatically prioritized Program Chair faculty:",
            faculty,
          );
        }

        // -----------------------------------------------------
        // CASE 2:
        // More than ONE faculty belongs to the Program Chair
        // -----------------------------------------------------
        else if (programChairCandidates.length > 1) {
          console.log(
            "[ASSIGN] Multiple Program Chair faculty found. Opening selection modal.",
          );

          this.openFacultySelectionModal(item, programChairCandidates);

          return;
        }

        // -----------------------------------------------------
        // CASE 3:
        // No faculty belongs to Program Chair's institute/program
        //
        // Show ALL possible faculty so the Program Chair can
        // manually determine the correct faculty.
        // -----------------------------------------------------
        else if (candidates.length > 1) {
          console.log(
            "[ASSIGN] No Program Chair faculty match. Multiple possible faculty found.",
          );

          this.openFacultySelectionModal(item, candidates);

          return;
        }

        // -----------------------------------------------------
        // CASE 4:
        // Only one possible faculty exists
        // -----------------------------------------------------
        else if (candidates.length === 1) {
          const candidate = candidates[0];

          faculty = {
            faculty_id: candidate.faculty_id,
            faculty_name: candidate.full_name,
            user: candidate.user,

            faculty_institute_id: candidate.institute_id,
            faculty_institute_name: candidate.institute_name,

            faculty_program_id: candidate.program_id,
            faculty_program_name: candidate.program_name,
            faculty_program_code: candidate.program_code,
          };

          console.log("[ASSIGN] Only one possible faculty found:", faculty);
        }
      }
      // -----------------------------------------------------
      // 0.4 NO FACULTY
      // -----------------------------------------------------
      if (!faculty || !faculty.faculty_id) {
        console.error("[ASSIGN] Faculty could not be resolved:", item);

        return;
      }

      const facultyId = faculty.faculty_id;
      const facultyName = faculty.faculty_name;

      console.log("[ASSIGN] FINAL FACULTY:", {
        facultyId,
        facultyName,
      });

      // =====================================================
      // 1. EXISTING FACULTY SCHEDULES
      // =====================================================
      const instructorSchedules = (this.finalSchedules || [])
        .filter((schedule) => {
          return (
            Number(schedule.faculty_id) === Number(facultyId) &&
            String(schedule.school_year || "").trim() ===
              String(item.school_year || "").trim() &&
            Number(schedule.semester) === Number(item.semester)
          );
        })
        .map((schedule) => ({
          ...structuredClone(schedule),

          isUnscheduledMeeting: false,
          isUnscheduledAssignment: false,
        }));

      console.log("[ASSIGN] Existing schedules:", instructorSchedules);

      // =====================================================
      // 2. UNSCHEDULED ID
      // =====================================================
      const unscheduledId =
        item.unscheduled_id ??
        item.unscheduled_meeting_id ??
        item.id ??
        Date.now();

      // =====================================================
      // 3. GET ALL CLASS / SECTION DATA
      // =====================================================
      // Use class sections from Pinia
      if (!this.store.sections?.length) {
        await this.store.fetchClassSections();
      }

      const classSections = this.store.sections || [];

      console.log("[ASSIGN] CLASS SECTIONS FROM PINIA:", classSections);

      // =====================================================
      // 4. GET CLASS ID FROM UNSCHEDULED ITEM
      // =====================================================
      const classId = item.class_id ?? item.classId ?? item.classID ?? null;

      console.log("[ASSIGN] ITEM FROM UNSCHEDULED:", item);

      console.log("[ASSIGN] CLASS ID:", classId);

      // =====================================================
      // 5. FIND SECTION USING CLASS ID
      // =====================================================
      const section = classSections.find(
        (cls) => Number(cls.class_id) === Number(classId),
      );

      console.log("[ASSIGN] MATCHED SECTION:", section);

      // =====================================================
      // 6. RESOLVE SET NAME
      // =====================================================
      const resolvedSetName =
        item.set_name ||
        item.section ||
        item.class_section ||
        section?.set_name ||
        "";

      console.log("[ASSIGN] RESOLVED SET NAME:", resolvedSetName);

      // =====================================================
      // 7. RESOLVE PROGRAM
      // =====================================================
      const resolvedProgramId =
        item.program_id ??
        item.class_program_id ??
        section?.program_id ??
        section?.program?.program_id ??
        null;

      const resolvedProgramCode =
        item.program_code || section?.program?.program_code || "";

      const resolvedProgramName =
        item.program_name || section?.program?.program_name || "";

      // =====================================================
      // 8. RESOLVE CLASS SIZE
      // =====================================================
      const resolvedClassSize = item.class_size ?? section?.class_size ?? null;

      // =====================================================
      // 9. DEBUG EVERYTHING
      // =====================================================
      console.log("[ASSIGN] FINAL CLASS INFORMATION:", {
        classId,
        resolvedSetName,
        resolvedProgramId,
        resolvedProgramCode,
        resolvedProgramName,
        resolvedClassSize,
        section,
      });

      // =====================================================
      // 10. PARSE HOURS
      // =====================================================
      const hoursText = String(item.hours || "")
        .trim()
        .toLowerCase();

      let lectureHours = 0;
      let laboratoryHours = 0;

      // -----------------------------------------------------
      // Lecture
      // -----------------------------------------------------
      const lectureMatch = hoursText.match(
        /(\d+(?:\.\d+)?)\s*h?\s*(?:lec|lecture)/i,
      );

      if (lectureMatch) {
        lectureHours = Number(lectureMatch[1]);
      }

      // -----------------------------------------------------
      // Laboratory
      // -----------------------------------------------------
      const laboratoryMatch = hoursText.match(
        /(\d+(?:\.\d+)?)\s*h?\s*(?:lab|laboratory)/i,
      );

      if (laboratoryMatch) {
        laboratoryHours = Number(laboratoryMatch[1]);
      }

      console.log("[ASSIGN] Parsed hours:", {
        original: item.hours,
        lectureHours,
        laboratoryHours,
      });

      // =====================================================
      // 11. FALLBACK HOURS
      // =====================================================
      if (lectureHours === 0 && laboratoryHours === 0) {
        const type = String(item.type || "").toLowerCase();

        const duration = item.duration != null ? Number(item.duration) : 0;

        if (type === "lecture" || type === "lec") {
          lectureHours = duration;
        }

        if (type === "laboratory" || type === "lab") {
          laboratoryHours = duration;
        }
      }

      // =====================================================
      // 12. INITIAL CALENDAR POSITION
      // =====================================================
      const initialDay = "Monday";
      const initialStartHour = 7;

      // =====================================================
      // 13. TIME SLOT HELPER
      // =====================================================
      const makeTimeSlot = (startHour, duration) => {
        const start = Number(startHour);
        const dur = Number(duration);

        if (Number.isNaN(start) || Number.isNaN(dur) || dur <= 0) {
          return null;
        }

        const end = start + dur;

        const formatTime = (decimalHour) => {
          let hour = Math.floor(decimalHour);

          const minutes = Math.round((decimalHour - hour) * 60);

          const suffix = hour >= 12 ? "PM" : "AM";

          let displayHour = hour % 12;

          if (displayHour === 0) {
            displayHour = 12;
          }

          return `${displayHour}:${String(minutes).padStart(2, "0")} ${suffix}`;
        };

        return `${formatTime(start)} - ${formatTime(end)}`;
      };

      // =====================================================
      // 14. CREATE SPLIT RECORDS
      // =====================================================
      const splitRecords = [];

      // =====================================================
      // 15. LECTURE
      // =====================================================
      if (lectureHours > 0) {
        splitRecords.push({
          ...structuredClone(item),

          id: null,

          tempId: `temp-unscheduled-${unscheduledId}-lecture`,

          faculty_id: facultyId,
          faculty_name: facultyName,

          unscheduled_id: unscheduledId,
          unscheduled_meeting_id: unscheduledId,

          isNew: true,
          isUnscheduledMeeting: true,
          isUnscheduledAssignment: true,

          type: "Lecture",

          hours: `${lectureHours}h lec`,

          lec_hours: lectureHours,
          lab_hours: 0,

          duration: lectureHours,

          day: initialDay,
          start_hour: initialStartHour,

          time_slot: makeTimeSlot(initialStartHour, lectureHours),
        });
      }

      // =====================================================
      // 16. LABORATORY
      // =====================================================
      if (laboratoryHours > 0) {
        const laboratoryStartHour = initialStartHour + lectureHours;

        splitRecords.push({
          ...structuredClone(item),

          id: null,

          tempId: `temp-unscheduled-${unscheduledId}-laboratory`,

          faculty_id: facultyId,
          faculty_name: facultyName,

          unscheduled_id: unscheduledId,
          unscheduled_meeting_id: unscheduledId,

          isNew: true,
          isUnscheduledMeeting: true,
          isUnscheduledAssignment: true,

          type: "Laboratory",

          hours: `${laboratoryHours}h lab`,

          lec_hours: 0,
          lab_hours: laboratoryHours,

          duration: laboratoryHours,

          day: initialDay,
          start_hour: laboratoryStartHour,

          time_slot: makeTimeSlot(laboratoryStartHour, laboratoryHours),
        });
      }

      // =====================================================
      // 17. FALLBACK RECORD
      // =====================================================
      if (!splitRecords.length) {
        const duration = Number(item.duration) > 0 ? Number(item.duration) : 1;

        splitRecords.push({
          ...structuredClone(item),

          id: null,

          tempId: `temp-unscheduled-${unscheduledId}`,

          faculty_id: facultyId,
          faculty_name: facultyName,

          unscheduled_id: unscheduledId,
          unscheduled_meeting_id: unscheduledId,

          isNew: true,
          isUnscheduledMeeting: true,
          isUnscheduledAssignment: true,

          type: item.type || "Lecture",

          duration,

          day: initialDay,
          start_hour: initialStartHour,

          time_slot: makeTimeSlot(initialStartHour, duration),
        });
      }

      // =====================================================
      // 18. APPLY CLASS / SECTION INFORMATION
      // =====================================================
      // =====================================================
      // 18. RESOLVE CAMPUS / COLLEGE BRANCH
      // =====================================================
      const resolvedCollegeBranch = this.resolveCollegeBranch(item, section);

      console.log("[ASSIGN] RESOLVED COLLEGE BRANCH:", {
        item_branch_id: item?.college_branch_id,
        item_branch_name: item?.college_branch_name,

        section_branch_id: section?.college_branch_id,
        section_branch_name: section?.college_branch_name,

        resolved_branch_id: resolvedCollegeBranch.college_branch_id,
        resolved_branch_name: resolvedCollegeBranch.college_branch_name,
      });

      // =====================================================
      // 19. APPLY CLASS / SECTION INFORMATION
      // =====================================================
      splitRecords.forEach((record) => {
        // -------------------------------------------------
        // FACULTY
        // -------------------------------------------------
        record.faculty_id = facultyId;
        record.faculty_name = facultyName;

        // -------------------------------------------------
        // SCHOOL YEAR / SEMESTER
        // -------------------------------------------------
        record.school_year = item.school_year;
        record.semester = item.semester;

        // -------------------------------------------------
        // CLASS ID
        // -------------------------------------------------
        record.class_id = classId;

        // -------------------------------------------------
        // COURSE
        // -------------------------------------------------
        record.course_id = item.course_id ?? null;
        record.course_code = item.course_code ?? "";

        // -------------------------------------------------
        // PROGRAM
        // -------------------------------------------------
        record.program_id = resolvedProgramId;
        record.program_code = resolvedProgramCode;
        record.program_name = resolvedProgramName;

        // -------------------------------------------------
        // SECTION / SET NAME
        // -------------------------------------------------
        record.set_name = resolvedSetName;

        // -------------------------------------------------
        // CLASS SIZE
        // -------------------------------------------------
        record.class_size = resolvedClassSize;

        // -------------------------------------------------
        // CLASS OWNERSHIP
        // -------------------------------------------------
        record.class_program_id =
          item.class_program_id ??
          section?.program_id ??
          section?.program?.program_id ??
          item.program_id ??
          null;

        record.class_institute_id =
          item.class_institute_id ?? section?.program?.institute_id ?? null;

        // -------------------------------------------------
        // CAMPUS / COLLEGE BRANCH
        // -------------------------------------------------
        record.college_branch_id = resolvedCollegeBranch.college_branch_id;

        record.college_branch_name = resolvedCollegeBranch.college_branch_name;

        // IMPORTANT FOR CAMPUS INPUT DISPLAY
        record.searchCampusQuery =
          resolvedCollegeBranch.college_branch_name || "";

        record.showCampusDropdown = false;

        // -------------------------------------------------
        // ROOM
        // -------------------------------------------------
        record.room_id = item.room_id ?? null;
        record.room_name = item.room_name ?? null;

        record.searchRoomQuery = item.room_name || "";
        record.showRoomDropdown = false;
      });

      // =====================================================
      // 19. FINAL DEBUG
      // =====================================================
      console.log(
        "[ASSIGN] FINAL SPLIT RECORDS:",
        splitRecords.map((record) => ({
          class_id: record.class_id,

          set_name: record.set_name,

          program_code: record.program_code,

          course_code: record.course_code,

          class_size: record.class_size,

          faculty_id: record.faculty_id,

          faculty_name: record.faculty_name,

          type: record.type,

          day: record.day,

          time_slot: record.time_slot,
        })),
      );

      // =====================================================
      // 20. SEND TO EDIT SCHEDULE
      // =====================================================
      this.selectedScheduleData = [...instructorSchedules, ...splitRecords];

      console.log(
        "[ASSIGN] FINAL DATA SENT TO EDIT SCHEDULE:",
        this.selectedScheduleData,
      );

      // =====================================================
      // 21. SAVE SELECTED UNSCHEDULED MEETING
      // =====================================================
      this.selectedUnscheduledMeeting = {
        ...structuredClone(item),

        class_id: classId,
        set_name: resolvedSetName,
        program_id: resolvedProgramId,
        program_code: resolvedProgramCode,
        program_name: resolvedProgramName,
        class_size: resolvedClassSize,

        faculty_id: facultyId,
        faculty_name: facultyName,

        // CAMPUS
        college_branch_id: resolvedCollegeBranch.college_branch_id,
        college_branch_name: resolvedCollegeBranch.college_branch_name,
      };

      // =====================================================
      // 22. OPEN EDIT SCHEDULE
      // =====================================================
      this.showEditSchedule = false;

      await this.$nextTick();

      this.showEditSchedule = true;
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
