<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mt-6 mb-2">
      <div class="text-[13px] text-gray-700">
        Pages / Class & Assigned Courses Overview
      </div>
      <span class="text-sm bg-defaultGreen text-white px-3 py-1 rounded-full">
        {{ filteredClasses.length }} Classes
      </span>
    </div>

    <!-- Classes with Courses Section -->
    <div class="table-container">
      <div class="table-controls">
        <div class="flex justify-between items-center gap-4 w-full rounded-lg">
          <div class="per-page-container">
            <div class="select-wrapper">
              <select v-model="itemsPerPage" class="select-input">
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
              <thead
                class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
              >
                <tr>
                  <th class="px-4 py-3 text-left font-semibold w-[7%]">
                    Year & Section
                  </th>
                  <th class="px-4 py-3 text-left font-semibold w-[15%]">
                    Program
                  </th>
                  <th class="px-4 py-3 text-center font-semibold w-[10%]">
                    Class Size
                  </th>
                  <th class="px-4 py-3 text-center font-semibold w-[10%]">
                    School Year
                  </th>
                  <th class="px-4 py-3 text-center w-[10%]">Campus</th>
                  <th class="px-4 py-3 text-center font-semibold w-[6%]">
                    Assigned Courses
                  </th>
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
                  <td class="px-4 py-3 text-gray-800 text-left">
                    {{ cls.set_name }}
                  </td>
                  <td class="px-4 py-3">
                    {{ cls.program?.program_name || "N/A" }}
                  </td>
                  <td class="px-4 py-3 text-center">
                    <span
                      class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full"
                    >
                      {{ cls.class_size }} students
                    </span>
                  </td>
                  <td class="px-4 py-3 text-center">
                    {{ cls.schoolYear?.school_year_name || "N/A" }}
                  </td>
                  <td class="text-center">
                    <span
                      class="border border-green-600 text-green-800 text-xs px-2 py-1 rounded-full"
                    >
                      {{ cls.colleges?.college_branch_name || "N/A" }}
                    </span>
                  </td>
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

          <div class="flex items-center gap-1 text-sm">
            <!-- Prev -->
            <button
              @click="changePage(classPage - 1)"
              :disabled="classPage === 1"
              class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400 disabled:opacity-50"
            >
              &lt;
            </button>

            <!-- Page Numbers -->
            <span v-for="page in paginatedNumbers" :key="'page-' + page">
              <button
                @click="changePage(page)"
                :class="{
                  'bg-defaultGreen text-white': classPage === page,
                  'bg-gray-200 text-gray-700': classPage !== page,
                }"
                class="px-3 py-1 rounded-md hover:bg-green-300"
              >
                {{ page }}
              </button>
            </span>

            <!-- Next -->
            <button
              @click="changePage(classPage + 1)"
              :disabled="classPage === classTotalPages"
              class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400 disabled:opacity-50"
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
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click.self="closeCoursesModal"
    >
      <div
        class="bg-white rounded-2xl shadow-2xl w-[950px] max-h-[90vh] overflow-hidden"
      >
        <!-- Header -->
        <div class="modal-header">
          <div class="flex items-center gap-3">
            <div class="glass-container">
              <icon name="book-open" class="text-white" />
            </div>

            <div>
              <h2 class="text-lg font-semibold text-white">
                Courses for {{ selectedClass?.program?.program_code }} -
                {{ selectedClass?.set_name }}
              </h2>

              <p class="text-xs text-green-100">
                Assigned Program Year Courses
              </p>
            </div>
          </div>

          <icon
            name="circle-close3"
            @click="closeCoursesModal"
            class="close-button-header"
          />
        </div>

        <!-- Body -->
        <div class="bg-slate-50 p-5 max-h-[75vh] overflow-y-auto">
          <div v-if="classCourses.length" class="space-y-3">
            <div
              v-for="(course, index) in classCourses"
              :key="course.course_id"
              class="bg-white border border-slate-200 rounded-xl shadow-sm hover:border-defaultGreen transition-all"
            >
              <!-- Header -->
              <div class="flex items-center justify-between px-5 py-4">
                <div class="flex items-center gap-4">
                  <div
                    class="w-10 h-10 rounded-lg bg-defaultGreen/10 text-defaultGreen font-semibold flex items-center justify-center"
                  >
                    {{ index + 1 }}
                  </div>

                  <div>
                    <div class="flex items-center gap-2">
                      <h3 class="text-base font-semibold text-slate-800">
                        {{ course.course?.course_code }}
                      </h3>

                      <span
                        class="px-2.5 py-1 rounded-md bg-green-50 text-defaultGreen text-xs font-medium"
                      >
                        {{ getYearLevelLabel(course.year_level) }}
                      </span>
                    </div>

                    <p class="text-sm text-slate-500 mt-1">
                      {{ course.course?.course_title }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Divider -->
              <div class="border-t border-slate-100"></div>

              <!-- Information -->
              <div
                class="grid grid-cols-2 md:grid-cols-4 gap-x-8 gap-y-4 px-5 py-4 text-sm"
              >
                <div>
                  <p class="text-slate-400">Lecture</p>
                  <p class="font-semibold text-slate-800">
                    {{ course.course?.course_lec ?? 0 }} hrs
                  </p>
                </div>

                <div>
                  <p class="text-slate-400">Laboratory</p>
                  <p class="font-semibold text-slate-800">
                    {{ course.course?.course_lab ?? 0 }} hrs
                  </p>
                </div>

                <div>
                  <p class="text-slate-400">Credit Units</p>
                  <p class="font-semibold text-slate-800">
                    {{ course.course?.course_credit ?? 0 }}
                  </p>
                </div>

                <div>
                  <p class="text-slate-400">Semester</p>
                  <p class="font-semibold text-slate-800">
                    {{ selectedClass?.schoolYear?.semester }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div
            v-else
            class="bg-white rounded-2xl border border-dashed border-slate-300 py-20 text-center"
          >
            <div
              class="w-16 h-16 rounded-full bg-slate-100 flex items-center justify-center mx-auto mb-5"
            >
              <icon name="book-open" class="text-slate-400" />
            </div>

            <h3 class="text-lg font-semibold text-slate-700">
              No Courses Available
            </h3>

            <p class="text-slate-500 mt-2">
              There are currently no assigned courses for this class section.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    v-if="scheduleModal"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    @click.self="closeScheduleModal"
  >
    <div
      class="bg-white rounded-2xl shadow-2xl w-[950px] max-h-[90vh] overflow-hidden"
    >
      <!-- Header -->
      <div class="modal-header">
        <div class="flex items-center gap-3">
          <div class="glass-container">
            <icon name="circle-add2" class="text-white" />
          </div>

          <div>
            <h2 class="text-lg font-semibold text-white">
              Schedule for {{ selectedClass?.program?.program_code }} -
              {{ selectedClass?.set_name }}
            </h2>

            <p class="text-xs text-green-100">
              View and manage schedules assigned to this class section
            </p>
          </div>
        </div>

        <icon
          name="circle-close3"
          @click="closeScheduleModal"
          class="close-button-header"
        />
      </div>

      <!-- Body -->
      <div class="bg-slate-50 p-5 max-h-[75vh] overflow-y-auto">
        <div class="rounded-xl border border-gray-200 bg-white overflow-hidden">
          <table
            v-if="selectedSchedules.length"
            class="min-w-full border-collapse text-sm"
          >
            <thead class="sticky top-0 bg-defaultGreen text-white z-10">
              <tr>
                <th class="schedule-th">Course</th>
                <th class="schedule-th">Day</th>
                <th class="schedule-th">Time</th>
                <th class="schedule-th">Faculty</th>
                <th class="schedule-th">Room</th>
                <th class="schedule-th">Type</th>
                <th class="schedule-th">Mode</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="schedule in selectedSchedules"
                :key="schedule.id"
                class="border-b hover:bg-gray-50 transition"
              >
                <td class="schedule-td">{{ schedule.course_code }}</td>
                <td class="schedule-td">{{ schedule.day }}</td>
                <td class="schedule-td">{{ schedule.time_slot }}</td>
                <td class="schedule-td">{{ schedule.faculty_name }}</td>
                <td class="schedule-td">{{ schedule.room_name }}</td>
                <td class="schedule-td">{{ schedule.type }}</td>
                <td class="schedule-td">{{ schedule.mode }}</td>
              </tr>
            </tbody>
          </table>

          <div
            v-else
            class="flex items-center justify-center h-40 text-gray-500"
          >
            No schedules found for this class.
          </div>
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

      // Filters
      classSearch: "",
      selectedProgram: "",

      // Pagination
      classPage: 1,
      itemsPerPage: 10,

      loading: true,
      scheduleModal: false,
      activeSchoolYear: null,
      stopEventBus: null,
    };
  },
  computed: {
    filteredClasses() {
      let result = [...this.classes];

      // Filter by active school year
      if (this.activeSchoolYear) {
        const { school_year_name, semester } = this.activeSchoolYear;

        // Special case:
        // 2025-2026 Semester 1 -> show everything
        if (school_year_name === "2025-2026" && Number(semester) === 1) {
          // Do nothing (show all classes)
        } else {
          // Otherwise only show classes for the active school year and semester
          result = result.filter(
            (c) =>
              c.schoolYear?.school_year_name === school_year_name &&
              Number(c.schoolYear?.semester) === Number(semester),
          );
        }
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
        result = result.filter(
          (c) => c.program?.program_name === this.selectedProgram,
        );
      }

      if (this.user?.role === "Program Chairperson" && this.user?.program_id) {
        result = result.filter((c) => c.program_id === this.user.program_id);
      }

      // Sort
      result = result.sort((a, b) => {
        const yearA = this.extractYearLevel(a.set_name) || 0;
        const yearB = this.extractYearLevel(b.set_name) || 0;

        if (yearA !== yearB) return yearA - yearB;

        const sectionA = a.set_name?.split("-").pop().trim() || "";
        const sectionB = b.set_name?.split("-").pop().trim() || "";

        return sectionA.localeCompare(sectionB);
      });

      return result;
    },
    paginatedNumbers() {
      const total = this.classTotalPages;

      if (total <= 3) {
        return Array.from({ length: total }, (_, i) => i + 1);
      }
      let start = this.classPage - 1;
      let end = this.classPage + 1;

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

    paginatedClasses() {
      const start = (this.classPage - 1) * this.itemsPerPage;
      return this.filteredClasses.slice(start, start + this.itemsPerPage);
    },
    classTotalPages() {
      return Math.ceil(this.filteredClasses.length / this.itemsPerPage) || 1;
    },
    classStartIndex() {
      return this.filteredClasses.length === 0
        ? 0
        : (this.classPage - 1) * this.itemsPerPage + 1;
    },
    classEndIndex() {
      const end = this.classPage * this.itemsPerPage;
      return Math.min(end, this.filteredClasses.length);
    },
    uniquePrograms() {
      const programs = this.classes
        .map((c) => c.program?.program_name)
        .filter(Boolean);
      return [...new Set(programs)];
    },
  },
  methods: {
    closeScheduleModal() {
      this.scheduleModal = false;
      this.selectedSchedules = [];
    },
    async showClassSchedules(cls) {
      try {
        const fetchDataStore = useFetchDataStore();

        await fetchDataStore.fetchFinalSchedules();

        console.log("ACTIVE SCHOOL YEAR:", this.activeSchoolYear);

        const dayOrder = {
          Monday: 1,
          Tuesday: 2,
          Wednesday: 3,
          Thursday: 4,
          Friday: 5,
          Saturday: 6,
          Sunday: 7,
        };

        const parseTime = (timeSlot) => {
          const first = timeSlot.split("-")[0].trim(); // "7:30 AM"
          const date = new Date(`1970-01-01 ${first}`);
          return date.getHours() * 60 + date.getMinutes();
        };

        this.selectedSchedules = fetchDataStore.final_schedules
          .filter(
            (schedule) =>
              schedule.class_id === cls.class_id &&
              schedule.school_year ===
                this.activeSchoolYear?.school_year_name &&
              Number(schedule.semester) ===
                Number(this.activeSchoolYear?.semester),
          )
          .sort((a, b) => {
            const dayDiff = (dayOrder[a.day] || 99) - (dayOrder[b.day] || 99);

            if (dayDiff !== 0) return dayDiff;

            return parseTime(a.time_slot) - parseTime(b.time_slot);
          });

        console.log("FILTERED SCHEDULES:", this.selectedSchedules);

        this.selectedClass = cls;
        this.scheduleModal = true;
      } catch (error) {
        console.error(error);
        toast.error("Failed to load schedules");
      }
    },
    changePage(page) {
      if (page < 1 || page > this.classTotalPages) return;
      this.classPage = page;
    },
    async fetchUser() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          },
        );
        this.user = res.data;
      } catch (err) {
        console.error("Failed to fetch user:", err);
      }
    },
    async loadClasses() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/class/get-classes",
        );
        this.classes = response.data;
      } catch (error) {
        console.error("Failed to load classes:", error);
        toast.error("Failed to load classes data");
      }
    },
    async showClassCourses(cls) {
      this.selectedClass = cls;
      this.showCoursesModal = true;

      try {
        const fetchDataStore = useFetchDataStore();

        // Load all courses
        await fetchDataStore.fetchCourses();

        // Load program year courses
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/program-year-courses/view-all",
        );

        const yearLevel = this.extractYearLevel(cls.set_name);

        // Filter the matching program/year courses
        const filteredCourses = data.filter(
          (item) =>
            Number(item.program_id) === Number(cls.program_id) &&
            Number(item.school_year_id) === Number(cls.school_year_id) &&
            Number(item.year_level) === Number(yearLevel),
        );

        // Merge course details
        const mergedCourses = filteredCourses.map((item) => ({
          ...item,
          course: fetchDataStore.courses.find(
            (c) => Number(c.course_id) === Number(item.course_id),
          ),
        }));

        // Remove duplicates by course_id
        const uniqueCourses = new Map();

        mergedCourses.forEach((item) => {
          if (!uniqueCourses.has(item.course_id)) {
            uniqueCourses.set(item.course_id, item);
          }
        });

        this.classCourses = Array.from(uniqueCourses.values());

        // Optional: sort by course code
        this.classCourses.sort((a, b) =>
          (a.course?.course_code || "").localeCompare(
            b.course?.course_code || "",
          ),
        );

        console.log(this.classCourses);

        console.log(this.classCourses);
      } catch (err) {
        console.error(err);
        this.classCourses = [];
        toast.error("Failed to load class courses.");
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
