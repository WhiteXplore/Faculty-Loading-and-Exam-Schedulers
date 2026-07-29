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
            <div class="absolute left-3 text-defaultGreen">
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
          <div
            class="absolute inset-y-0 left-3 flex items-center text-defaultGreen pointer-events-none"
          >
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
</template>

<script>
import { useFetchDataStore } from "@/store/fetch-data-store";
import axios from "axios";
import { eventBus } from "@/bus/event-bus";
export default {
  name: "UnscheduledMeetingTable",

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
    };
  },

  computed: {
    store() {
      return useFetchDataStore();
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
    await this.store.fetchUnscheduledMeetings();

    // Get the current active school year immediately
    this.activeSchoolYear = eventBus.data || null;

    // Listen for changes
    this.stopEventBus = eventBus.on((newYear) => {
      if (!newYear) return;

      console.log("NEW ACTIVE YEAR:", newYear);

      this.activeSchoolYear = { ...newYear };
      this.currentPage = 1;
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
