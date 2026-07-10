<template>
  <div class="space-y-2 text-[13px]">
    <!-- HEADER -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4">Pages / Year & Section</div>

      <button @click="openYearSectionModal" class="btn-add">
        <div class="btn-add-icon">
          <icon name="add-account1.1" />
        </div>
        <span class="font-medium">Add Year/Section</span>
      </button>
    </div>

    <!-- MAIN CONTENT -->
    <div v-if="user" class="space-y-6">
      <!-- Program Info (Program Chairperson only) -->
      <div v-if="user.role === 'Program Chairperson' && userProgram">
        <!-- <h2 class="text-lg font-bold text-gray-800">
          {{ userProgram.program_name }}
        </h2>
        <p class="text-sm text-gray-600 mb-2" v-if="userProgram.institute">
          Institute: {{ userProgram.institute.institute_name }}
        </p> -->

        <!-- SECTIONS TABLE -->
        <div>
          <div class="overflow-x-auto border p-3 rounded-xl bg-white">
            <!-- Controls -->
            <div class="table-controls">
              <!-- Items per page -->
              <div class="per-page-container">
                <div class="select-wrapper">
                  <select
                    v-model.number="itemsPerPage"
                    class="select-input"
                    @change="changePage(1)"
                  >
                    <option :value="10">10</option>
                    <option :value="15">15</option>
                    <option :value="20">20</option>
                  </select>
                  <div
                    class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-green-700"
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
                <span class="text-sm font-medium">Per page</span>
              </div>

              <!-- Search -->

              <div class="per-page-container">
                <!-- Campus Branch Filter -->
                <div class="relative">
                  <select
                    v-model="selectedCampus"
                    class="select-filter-input pr-8"
                    @change="changePage(1)"
                  >
                    <option value="all">All Campus</option>
                    <option
                      v-for="campus in campusBranches"
                      :key="campus"
                      :value="campus"
                    >
                      {{ campus }}
                    </option>
                  </select>

                  <div
                    class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-green-700"
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

                <!-- Search -->
                <div class="search-wrapper">
                  <input
                    v-model="searchQuery"
                    type="text"
                    placeholder="Search section ..."
                    class="search-input"
                    @input="changePage(1)"
                  />

                  <div
                    class="absolute inset-y-0 left-3 flex items-center text-green-700 pointer-events-none"
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
            <div class="w-full mt-2 rounded-xl border bg-white overflow-hidden">
              <div class="max-h-[70vh] overflow-y-auto">
                <table class="min-w-full text-sm text-gray-700 border-collapse">
                  <thead
                    class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
                  >
                    <tr>
                      <th
                        v-if="user.role === 'Admin'"
                        class="px-4 py-3 text-left w-[20%]"
                      >
                        Program
                      </th>
                      <th class="px-4 py-3 text-left w-[15%]">Campus Branch</th>
                      <th class="px-4 py-3 text-left w-[15%]">Program</th>
                      <th class="px-4 py-3 text-left w-[15%]">Section Name</th>
                      <th class="px-4 py-3 text-center w-[18%]">Class Size</th>
                      <th class="px-4 py-3 text-center w-[18%]">School Year</th>
                      <th class="px-4 py-3 text-center w-[18%]">Semester</th>
                      <th class="px-4 py-3 text-center w-[20%]">Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="cls in paginatedClasses"
                      :key="cls.class_id"
                      class="hover:bg-green-50 transition-all border-t"
                    >
                      <td
                        v-if="user.role === 'Admin'"
                        class="px-4 py-3 text-left"
                      >
                        {{ cls.program?.program_name }}
                      </td>

                      <td class="px-4 py-3 text-left">
                        {{ cls.colleges?.college_branch_name }}
                      </td>
                      <td class="px-4 py-3 text-left">
                        {{ cls.program?.program_code }}
                      </td>
                      <td class="px-4 py-3 font-medium text-left">
                        {{ cls.set_name }}
                      </td>
                      <td class="px-4 py-3 text-center">
                        {{ cls.class_size }}
                      </td>
                      <td class="px-4 py-3 text-center">
                        {{ cls.schoolYear?.school_year_name }}
                      </td>
                      <td class="px-4 py-3 text-center">
                        {{ formatSemester(cls.schoolYear?.semester) }}
                      </td>
                      <td class="px-4 py-3 flex justify-center gap-2">
                        <!-- Delete Button -->
                        <button
                          @click="promptDelete(cls.class_id)"
                          class="px-3 py-1 border border-red-300 hover:bg-red-200 text-red-800 rounded-lg flex items-center gap-1"
                        >
                          <icon name="delete" /> Delete
                        </button>
                      </td>
                    </tr>

                    <tr v-if="paginatedClasses.length === 0">
                      <td
                        :colspan="user.role === 'Admin' ? 8 : 7"
                        class="text-center py-10 text-gray-400"
                      >
                        No matching sections found
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Pagination -->
            <div class="flex justify-between items-center mt-4 text-gray-700">
              <div>
                Showing {{ startIndex }} to {{ endIndex }} of
                {{ filteredAndSearchedClasses.length }} entries
              </div>

              <div class="flex items-center gap-1 text-sm">
                <!-- Prev -->
                <button
                  @click="changePage(currentPage - 1)"
                  :disabled="currentPage === 1"
                  class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400 disabled:opacity-50"
                >
                  &lt;
                </button>

                <!-- Page Numbers -->
                <span v-for="page in paginatedNumbers" :key="'page-' + page">
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
                  class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400 disabled:opacity-50"
                >
                  &gt;
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <!-- Empty State -->
        <!-- Optional Empty State -->
        <div
          v-if="filteredClasses.length === 0"
          class="bg-white border p-8 rounded-xl text-center"
        >
          <p class="text-gray-600">
            No sections created for {{ activeSchoolYearName }} -
            {{ formatSemester(activeSemesterYear) }} yet.
          </p>
        </div>
      </div>
    </div>

    <!-- LOADING OR EMPTY STATES -->
    <div v-else-if="loading" class="bg-white border p-8 rounded-xl text-center">
      <p class="text-gray-500 animate-pulse">Loading program information...</p>
    </div>

    <div v-else class="bg-white border p-8 rounded-xl text-center">
      <p class="text-gray-600 font-medium">
        No program found for your account.
      </p>
      <p class="text-sm text-gray-400 mt-1">
        Please contact the administrator.
      </p>
    </div>
  </div>

  <!-- MODAL -->
  <addYearSection
    v-if="showYearSectionModal"
    :programData="userProgram || {}"
    @close="closeYearSectionModal"
    @refresh="refreshSections"
  />
  <div v-if="showDeleteModal" class="fixed inset-0 z-50">
    <div class="absolute inset-0 bg-gray-800 bg-opacity-40"></div>
    <div
      class="rounded-xl border w-[300px] md:w-[400px] bg-white py-6 px-4 flex flex-col items-center absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2"
    >
      <div
        class="rounded-full w-16 h-16 md:w-20 md:h-20 flex justify-center items-center bg-red-300 animate-pulse"
      >
        <icon
          name="question"
          class="w-8 h-8 md:w-10 md:h-10 text-white flex justify-center items-center"
        />
      </div>
      <h1 class="text-[14px] md:text-[16px] font-semibold mt-4">
        Delete Confirmation
      </h1>
      <p class="mt-2 text-[12px] md:text-[13px] text-center px-8">
        Are you sure you want to delete this record? This action cannot be
        undone.
      </p>
      <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>
      <div class="tracking-wide flex gap-2 mt-4">
        <button
          class="bg-red-400 p-2 px-3 text-[11px] md:text-[13px] rounded-md text-white hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md"
          @click="showDeleteModal = false"
        >
          No, Cancel
        </button>
        <button
          class="bg-green-400 p-2 px-3 text-[11px] md:text-[13px] rounded-md text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
          @click="confirmDelete"
        >
          Yes, Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import addYearSection from "@/components/program-chairperson/program-record/modals/add-year-section.vue";
import axios from "axios";
import { mapState, mapActions } from "pinia";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { eventBus } from "@/bus/event-bus";
export default {
  name: "YearSectionManagement",
  components: { icon, addYearSection },
  data() {
    return {
      selectedCampus: "all",
      showYearSectionModal: false,
      userProgram: null,
      user: null,
      searchQuery: "",
      currentPage: 1,
      itemsPerPage: 10,
      showDeleteModal: false,
      deleteTargetId: null,
      loading: true,

      stopEventBus: null,
      activeSchoolYear: null,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["activeYear", "programs", "sections"]),
    campusBranches() {
      const branches = this.sections
        .map((cls) => cls.colleges?.college_branch_name)
        .filter(Boolean);

      return [...new Set(branches)];
    },
    filteredClasses() {
      const active = this.activeSchoolYear || this.activeYear;
      if (!active?.school_year_id) return [];

      let result = this.sections.filter(
        (cls) => String(cls.school_year_id) === String(active.school_year_id),
      );

      if (this.user?.role === "Admin") return result;

      if (this.userProgram) {
        return result.filter(
          (cls) =>
            String(cls.program_id) === String(this.userProgram.program_id),
        );
      }

      return [];
    },

    activeSchoolYearId() {
      return (this.activeSchoolYear || this.activeYear)?.school_year_id || null;
    },

    activeSchoolYearName() {
      return (
        (this.activeSchoolYear || this.activeYear)?.school_year_name ||
        "Current School Year"
      );
    },
    activeSemesterYear() {
      return (
        (this.activeSchoolYear || this.activeYear)?.semester ||
        "Current semester Year"
      );
    },

    filteredAndSearchedClasses() {
      const filtered = this.filteredClasses.filter((cls) => {
        const matchesSearch = cls.set_name
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase());

        const matchesCampus =
          this.selectedCampus === "all" ||
          cls.colleges?.college_branch_name === this.selectedCampus;

        return matchesSearch && matchesCampus;
      });

      // Custom sort: year priority then section letter
      return filtered.sort((a, b) => {
        const yearA = this.getYearPriority(a.set_name);
        const yearB = this.getYearPriority(b.set_name);

        if (yearA !== yearB) return yearA - yearB;

        const sectionA = a.set_name.split("-")[1]?.trim() || "";
        const sectionB = b.set_name.split("-")[1]?.trim() || "";
        return sectionA.localeCompare(sectionB);
      });
    },

    totalPages() {
      return Math.max(
        1,
        Math.ceil(this.filteredAndSearchedClasses.length / this.itemsPerPage),
      );
    },
    startIndex() {
      return this.filteredAndSearchedClasses.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(
        this.startIndex + this.itemsPerPage - 1,
        this.filteredAndSearchedClasses.length,
      );
    },

    paginatedClasses() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredAndSearchedClasses.slice(
        start,
        start + this.itemsPerPage,
      );
    },

    paginatedNumbers() {
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
  },
  methods: {
    ...mapActions(useFetchDataStore, ["fetchPrograms", "fetchClassSections"]),
    async refreshSections() {
      await this.fetchClassSections();
      await this.loadUserProgram();
    },
    formatSemester(value) {
      if (value === 1 || value === "1") return "First Semester";
      if (value === 2 || value === "2") return "Second Semester";
      return value; // fallback if unexpected
    },
    getYearPriority(setName) {
      const match = setName.match(/^(\d+)(st|nd|rd|th) Year/i);
      if (match) return parseInt(match[1], 10);
      return 99;
    },

    async fetchUser() {
      const { data } = await axios.get(
        process.env.VUE_APP_API_BASE_URL + "/auth/me",
        {
          withCredentials: true,
        },
      );
      this.user = data;
    },

    async loadUserProgram() {
      if (this.user?.role === "Program Chairperson") {
        this.userProgram = this.programs.find(
          (p) => String(p.program_id) === String(this.user.program_id),
        );
      }
    },

    promptDelete(classId) {
      this.deleteTargetId = classId;
      this.showDeleteModal = true;
    },

    async confirmDelete() {
      if (!this.deleteTargetId) return;

      try {
        await axios.delete(
          process.env.VUE_APP_API_BASE_URL +
            `/class/delete-id/${this.deleteTargetId}`,
          { withCredentials: true },
        );
        await this.fetchClassSections();
        toast.success("Record deleted successfully");
        this.showDeleteModal = false;
        this.deleteTargetId = null;
      } catch (error) {
        console.error("Error deleting class:", error);
        toast.error("Failed to delete class");
      }
    },

    openYearSectionModal() {
      this.showYearSectionModal = true;
    },

    closeYearSectionModal() {
      this.showYearSectionModal = false;
    },

    changePage(page) {
      const maxPage = this.totalPages || 1;

      if (page < 1) {
        this.currentPage = 1;
        return;
      }

      if (page > maxPage) {
        this.currentPage = maxPage;
        return;
      }

      this.currentPage = page;
    },
  },

  async mounted() {
    await this.fetchUser();

    const store = useFetchDataStore();
    await store.fetchActiveYears();

    await this.fetchPrograms();
    await this.fetchClassSections();

    await this.loadUserProgram();

    this.loading = false;

    this.stopEventBus = eventBus.on(async (newYear) => {
      if (!newYear) return;

      this.activeSchoolYear = newYear;
      this.currentPage = 1;

      await this.$nextTick();

      await this.fetchClassSections();
    });
  },

  beforeUnmount() {
    this.stopEventBus?.();
  },
};
</script>
