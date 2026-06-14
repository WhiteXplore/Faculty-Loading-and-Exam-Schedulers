<template>
  <div>
    <!-- Header -->

    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages / Class & Assigned Courses
      </div>
      <span
        class="text-sm bg-defaultGreen text-white px-4 py-1 rounded-full flex text-center items-center"
      >
        {{ filteredClasses.length }} Classes
      </span>
    </div>

    <!-- Classes with Courses Section -->
    <div class="overflow-x-auto border p-3 mt-4 rounded-xl bg-white">
      <!-- Controls -->
      <div class="table-controls">
        <div class="flex justify-between items-center gap-4 w-full rounded-lg">
          <div class="per-page-container">
            <div class="select-wrapper">
              <select v-model="itemsPerPage" class="select-input" @change="changePage(1)">
                <option value="10">10</option>
                <option value="15">15</option>
                <option value="20">20</option>
              </select>
              <!-- Custom arrow -->
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
          <div class="search-wrapper">
            <input
              v-model="classSearch"
              type="text"
              placeholder="Search..."
              class="search-input"
              @input="changePage(1)"
            />
            <!-- Search icon -->
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

        <!-- Table -->
        <div class="w-full mt-1 rounded-xl border bg-white overflow-hidden">
          <div class="max-h-[69vh] overflow-y-auto">
            <table class="min-w-full text-sm text-gray-700 border-collapse">
              <thead class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide">
                <tr>
                  <!-- <th class="px-4 py-3 text-left    w-[2%]">ID</th> -->
                  <th class="px-4 py-3 text-left w-[5%]">Year & Section</th>
                  <th class="px-4 py-3 text-left w-[20%]">Program</th>
                  <th class="px-4 py-3 text-center w-[10%]">Class Size</th>
                  <th class="px-4 py-3 text-center w-[15%]">School Year</th>
                  <th class="px-4 py-3 text-center w-[5%]">Campus</th>
                  <th class="px-4 py-3 text-center w-[8%]">Action</th>
                </tr>
              </thead>

              <!-- Table Body -->
              <tbody>
                <tr
                  v-for="cls in paginatedClasses"
                  :key="cls.class_id"
                  class="hover:bg-green-50 transition-all border-t"
                >
                  <!-- <td class="px-4 py-3 text-gray-600">
                    {{ classStartIndex + index }}
                  </td> -->
                  <td class="text-left">
                    {{ cls.set_name }}
                  </td>
                  <td>
                    {{ cls.program?.program_name || "N/A" }}
                  </td>
                  <td class="text-center">
                    <span
                      class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full"
                    >
                      {{ cls.class_size }} students
                    </span>
                  </td>
                  <td class="text-center">
                    {{ cls.schoolYear?.school_year_name || "N/A" }}
                  </td>
                  <!-- ✅ Campus Column -->
                  <td class="text-center">
                    <span
                      class="border border-green-600 text-green-800 text-xs px-2 py-1 rounded-full"
                    >
                      {{ cls.colleges?.college_branch_name || "N/A" }}
                    </span>
                  </td>
                  <!-- ✅ Action Column -->

                  <td class="flex justify-center items-center gap-2">
                    <button @click="showClassCourses(cls)" class="btn-view">
                      See Details
                    </button>

                    <button
                      @click="showClassSchedules(cls)"
                      class="text-[12px] py-2 px-3 rounded-xl bg-defaultGreen text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transform transition-all duration-300 hover:scale-105;"
                    >
                      See Schedules
                    </button>
                  </td>
                </tr>

                <!-- Empty State -->
                <tr v-if="filteredClasses.length === 0">
                  <td colspan="6" class="px-4 py-8 text-center text-gray-500">
                    No classes found
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pagination -->
        <div class="flex justify-between items-center mt-4 w-full">
          <div class="text-gray-700 text-sm">
            Showing {{ classStartIndex }} to {{ classEndIndex }} of
            {{ filteredClasses.length }} entries
          </div>

          <div class="flex items-center gap-1">
            <button
              @click="changePage(classPage - 1)"
              :disabled="classPage === 1"
              class="px-3 py-1 bg-gray-300 rounded-l-md hover:bg-gray-400 disabled:opacity-50"
            >
              &lt;
            </button>

            <button
              v-for="page in pageNumbers"
              :key="'page-' + page"
              @click="changePage(page)"
              :class="{
                'bg-defaultGreen text-white': classPage === page,
                'bg-gray-200 text-gray-700': classPage !== page,
              }"
              class="px-3 py-1 rounded-md hover:bg-green-300"
            >
              {{ page }}
            </button>

            <button
              @click="changePage(classPage + 1)"
              :disabled="classPage === totalPages"
              class="px-3 py-1 bg-gray-300 rounded-r-md hover:bg-gray-400 disabled:opacity-50"
            >
              &gt;
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Course Details Modal -->
    <div
      v-if="showCoursesModal"
      class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center"
      @click.self="closeCoursesModal"
    >
      <div class="bg-white rounded-xl shadow-2xl w-[800px] max-h-[80vh] overflow-y-auto">
        <div
          class="bg-defaultGreen text-white px-6 py-4 flex justify-between items-center sticky top-0"
        >
          <h3 class="font-bold text-lg">Courses for {{ selectedClass?.set_name }}</h3>
          <button @click="closeCoursesModal" class="text-white hover:text-gray-200">
            <icon name="close" class="w-6 h-6" />
          </button>
        </div>

        <div class="p-6">
          <div v-if="classCourses.length > 0" class="space-y-3">
            <div
              v-for="(course, index) in classCourses"
              :key="course.id"
              class="p-4 border border-gray-200 rounded-lg hover:border-purple-400 transition-colors"
            >
              <div class="flex justify-between items-start">
                <div class="flex-1">
                  <p class="font-bold text-gray-800">
                    {{ index + 1 }}. {{ course.course?.course_code }}
                  </p>
                  <p class="text-sm text-gray-600 mt-1">
                    {{ course.course?.course_description }}
                  </p>
                  <div class="mt-2 flex gap-4 text-xs text-gray-500">
                    <span>Year Level: {{ getYearLevelLabel(course.year_level) }}</span>
                    <span>Lec: {{ course.course?.course_lec || 0 }} hrs</span>
                    <span>Lab: {{ course.course?.course_lab || 0 }} hrs</span>
                    <span>Units: {{ course.course?.course_credit || 0 }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-8 text-gray-500">
            <icon name="question" class="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p>No courses assigned to this class yet.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- Schedule Modal -->
  <div
    v-if="scheduleModal"
    class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center"
    @click.self="closeScheduleModal"
  >
    <div class="bg-white rounded-xl shadow-2xl w-[1000px] max-h-[80vh] overflow-y-auto">
      <div class="bg-defaultGreen text-white px-6 py-4 flex justify-between items-center">
        <h3 class="font-bold text-lg">
          {{ selectedClass?.program?.program_code }} -
          {{ selectedClass?.set_name }}
        </h3>

        <button @click="closeScheduleModal" class="text-white text-xl">✕</button>
      </div>

      <div class="p-2">
        <table v-if="selectedSchedules.length" class="min-w-full border text-sm">
          <thead class="bg-gray-100">
            <tr>
              <th class="border px-3 py-2 bg-gray-50 text-gray-400 text-left">Course</th>
              <th class="border px-3 py-2 bg-gray-50 text-gray-400 text-left">Day</th>
              <th class="border px-3 py-2 bg-gray-50 text-gray-400 text-left">Time</th>
              <th class="border px-3 py-2 bg-gray-50 text-gray-400 text-left">Faculty</th>
              <th class="border px-3 py-2 bg-gray-50 text-gray-400 text-left">Room</th>
              <th class="border px-3 py-2 bg-gray-50 text-gray-400 text-left">Type</th>
              <th class="border px-3 py-2 bg-gray-50 text-gray-400 text-left">Mode</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="schedule in selectedSchedules" :key="schedule.id">
              <td class="border px-3 py-2">
                {{ schedule.course_code }}
              </td>

              <td class="border px-3 py-2">
                {{ schedule.day }}
              </td>

              <td class="border px-3 py-2">
                {{ schedule.time_slot }}
              </td>

              <td class="border px-3 py-2">
                {{ schedule.faculty_name }}
              </td>

              <td class="border px-3 py-2">
                {{ schedule.room_name }}
              </td>

              <td class="border px-3 py-2">
                {{ schedule.type }}
              </td>

              <td class="border px-3 py-2">
                {{ schedule.mode }}
              </td>
            </tr>
          </tbody>
        </table>

        <div v-else class="text-center py-8 text-gray-500">
          No schedules found for this class.
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { eventBus } from "@/bus/event-bus";
export default {
  name: "TableClassAssignedCourses",
  components: { icon },
  data() {
    return {
      user: null,
      classes: [],
      classCourses: [],
      selectedClass: null,
      showCoursesModal: false,

      classSearch: "",
      selectedProgram: "",

      classPage: 1,
      itemsPerPage: 10,

      loading: true,
      scheduleModal: false,
      selectedSchedules: [],

      // ADD THIS
      activeSchoolYear: null,
      stopEventBus: null,
    };
  },
  computed: {
    filteredClasses() {
      let result = [...this.classes];

      // FILTER BY ACTIVE SCHOOL YEAR
      if (this.activeSchoolYear?.school_year_id) {
        result = result.filter(
          (c) => Number(c.school_year_id) === Number(this.activeSchoolYear.school_year_id)
        );
      }

      if (this.classSearch) {
        const query = this.classSearch.toLowerCase();

        result = result.filter((c) => {
          return (
            c.set_name?.toLowerCase().includes(query) ||
            c.program?.program_name?.toLowerCase().includes(query) ||
            c.schoolYear?.school_year_name?.toLowerCase().includes(query) ||
            c.colleges?.college_branch_name?.toLowerCase().includes(query)
          );
        });
      }

      if (this.selectedProgram) {
        result = result.filter((c) => c.program?.program_name === this.selectedProgram);
      }

      if (this.user?.role === "Program Chairperson" && this.user?.program_id) {
        result = result.filter((c) => c.program_id === this.user.program_id);
      }

      result.sort((a, b) => {
        const yearA = this.extractYearLevel(a.set_name) || 0;
        const yearB = this.extractYearLevel(b.set_name) || 0;

        if (yearA !== yearB) {
          return yearA - yearB;
        }

        const sectionA = a.set_name?.split("-").pop().trim() || "";
        const sectionB = b.set_name?.split("-").pop().trim() || "";

        return sectionA.localeCompare(sectionB);
      });

      return result;
    },
    paginatedClasses() {
      const start = (this.classPage - 1) * this.itemsPerPage;
      return this.filteredClasses.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.max(1, Math.ceil(this.filteredClasses.length / this.itemsPerPage));
    },
    pageNumbers() {
      const total = this.totalPages;

      if (total <= 3) {
        return Array.from({ length: total }, (_, i) => i + 1);
      }

      let start = this.classPage - 1;
      let end = this.classPage + 1;

      if (start < 1) start = 1;
      if (end > total) end = total;

      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    },
    classStartIndex() {
      return this.filteredClasses.length === 0
        ? 0
        : (this.classPage - 1) * this.itemsPerPage + 1;
    },

    classEndIndex() {
      return Math.min(this.classPage * this.itemsPerPage, this.filteredClasses.length);
    },

    uniquePrograms() {
      const programs = this.classes.map((c) => c.program?.program_name).filter(Boolean);
      return [...new Set(programs)];
    },
  },
  methods: {
    async showClassSchedules(cls) {
      try {
        const fetchDataStore = useFetchDataStore();

        await fetchDataStore.fetchFinalSchedules();

        console.log("ACTIVE SCHOOL YEAR:", this.activeSchoolYear);

        this.selectedSchedules = fetchDataStore.final_schedules.filter(
          (schedule) =>
            schedule.class_id === cls.class_id &&
            schedule.school_year === this.activeSchoolYear?.school_year_name &&
            Number(schedule.semester) === Number(this.activeSchoolYear?.semester)
        );

        console.log("FILTERED SCHEDULES:", this.selectedSchedules);

        this.selectedClass = cls;
        this.scheduleModal = true;
      } catch (error) {
        console.error(error);
        toast.error("Failed to load schedules");
      }
    },
    closeScheduleModal() {
      this.scheduleModal = false;
      this.selectedSchedules = [];
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.classPage = page;
    },
    async fetchUser() {
      try {
        const res = await axios.get(process.env.VUE_APP_API_BASE_URL + "/auth/me", {
          withCredentials: true,
        });
        this.user = res.data;
      } catch (err) {
        console.error("Failed to fetch user:", err);
      }
    },
    async loadClasses() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/class/get-classes"
        );

        this.classes = response.data;

        console.log("ACTIVE YEAR:", this.activeSchoolYear);
        console.log("CLASSES:", this.classes);
      } catch (error) {
        console.error(error);
      }
    },
    async showClassCourses(cls) {
      this.selectedClass = cls;
      this.showCoursesModal = true;

      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/program-year-courses/get-by-program-and-school-year",
          {
            params: {
              program_id: cls.program_id,
              school_year_id: cls.school_year_id,
            },
          }
        );

        const yearLevel = this.extractYearLevel(cls.set_name);
        this.classCourses = yearLevel
          ? response.data.filter((c) => c.year_level === yearLevel)
          : response.data;
      } catch (error) {
        console.error("Failed to load class courses:", error);
        this.classCourses = [];
      }
    },
    closeCoursesModal() {
      this.showCoursesModal = false;
      this.selectedClass = null;
      this.classCourses = [];
    },
    getYearLevelLabel(level) {
      const labels = {
        1: "1st Year",
        2: "2nd Year",
        3: "3rd Year",
        4: "4th Year",
      };
      return labels[level] || `Year ${level}`;
    },
    extractYearLevel(setName) {
      if (!setName) return null;
      const match = setName.match(/(\d+)(?:st|nd|rd|th)\s*year/i);
      return match ? parseInt(match[1]) : null;
    },
  },
  async mounted() {
    this.loading = true;
    await this.fetchUser();
    await this.loadClasses();
    this.loading = false;
    // Current active school year
    this.activeSchoolYear = eventBus.data ? { ...eventBus.data } : null;

    console.log("INITIAL ACTIVE YEAR:", this.activeSchoolYear);

    // Listen for active year changes
    this.stopEventBus = eventBus.on((newYear) => {
      console.log("NEW ACTIVE YEAR:", newYear);

      this.activeSchoolYear = { ...newYear };
    });
  },
};
</script>
