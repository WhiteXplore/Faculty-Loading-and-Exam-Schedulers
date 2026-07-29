<template>
  <div>
    <!-- Header -->
    <!-- <div class="flex justify-between items-center mt-6 mb-2">
      <div class="text-[13px] text-gray-700">
        Pages / Year & Section Overview
      </div>
      <span class="text-sm bg-defaultGreen text-white px-3 py-1 rounded-full">
        {{ filteredClasses.length }} Classes
      </span>
    </div> -->

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
          <div class="flex gap-2">
            <div
              class="relative w-56"
              ref="programDropdownRef"
              v-if="user?.role === 'Admin'"
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
                class="absolute z-[9999] mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
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
                      <p class="text-sm text-gray-800">All Programs</p>
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
                    <p class="text-sm text-gray-800">
                      {{ program.program_code }}
                    </p>

                    <svg
                      v-if="
                        Number(selectedProgram) === Number(program.program_id)
                      "
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
        </div>

        <!-- Table -->
        <div class="w-full mt-1 rounded-xl border bg-white overflow-hidden">
          <div class="max-h-[69vh] overflow-y-auto">
            <table class="min-w-full text-sm border-collapse">
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
                  <th class="px-4 py-3 text-center font-semibold w-[10%]">
                    Campus
                  </th>
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
                  <td class="px-4 py-3 t text-left">
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
                    <button
                      @click="showClassCourses(cls)"
                      class="btn-see-details"
                    >
                      See Details
                    </button>

                    <button
                      @click="showClassSchedules(cls)"
                      class="btn-see-details1"
                    >
                      Schedules
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
        class="bg-white rounded-2xl shadow-2xl w-[70vw] max-h-[90vh] overflow-hidden"
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
        <!-- Body -->
        <div class="bg-slate-50 p-5 max-h-[75vh] overflow-y-auto">
          <div
            class="rounded-md border border-gray-200 bg-white overflow-hidden"
          >
            <table
              v-if="classCourses.length"
              class="min-w-full border-collapse text-sm"
            >
              <thead class="sticky top-0 bg-defaultGreen text-white z-10">
                <tr>
                  <th class="schedule-th text-center w-12">#</th>
                  <th class="schedule-th">Course Code</th>
                  <th class="schedule-th">Course Title</th>
                  <th class="schedule-th text-center">Year Level</th>
                  <th class="schedule-th text-center">Semester</th>
                  <th class="schedule-th text-center">Lecture</th>
                  <th class="schedule-th text-center">Laboratory</th>
                  <th class="schedule-th text-center">Units</th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="(course, index) in classCourses"
                  :key="course.course_id"
                  class="border-b hover:bg-green-50 transition"
                >
                  <td class="schedule-td text-center">
                    {{ index + 1 }}
                  </td>

                  <td class="schedule-td font-semibold text-defaultGreen">
                    {{ course.course_code }}
                  </td>

                  <td class="schedule-td">
                    {{ course.course_title }}
                  </td>

                  <td class="schedule-td text-center">
                    <span
                      class="px-2 py-1 rounded-full bg-green-100 text-defaultGreen text-xs"
                    >
                      {{ getYearLevelLabel(course.course_level) }}
                    </span>
                  </td>

                  <td class="schedule-td text-center">
                    {{ course.course_semester }}
                  </td>

                  <td class="schedule-td text-center">
                    {{ course.course_lec }}
                  </td>

                  <td class="schedule-td text-center">
                    {{ course.course_lab }}
                  </td>

                  <td class="schedule-td text-center font-semibold">
                    {{ Number(course.course_lec) + Number(course.course_lab) }}
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Empty State -->
            <div
              v-else
              class="flex items-center justify-center h-40 text-gray-500"
            >
              No courses assigned to this class.
            </div>
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
        <div class="rounded-md border border-gray-200 bg-white overflow-hidden">
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

      // Pagination
      classPage: 1,
      itemsPerPage: 10,

      loading: true,
      scheduleModal: false,
      activeSchoolYear: null,
      stopEventBus: null,
      selectedProgram: "all",
      showProgramDropdown: false,
    };
  },
  computed: {
    availablePrograms() {
      return [
        ...new Map(
          this.classes
            .filter((c) => c.program)
            .map((c) => [c.program.program_id, c.program]),
        ).values(),
      ].sort((a, b) => a.program_code.localeCompare(b.program_code));
    },
    filteredClasses() {
      let result = [...this.classes];

      // Filter using the latest active school year
      if (this.activeSchoolYear) {
        const { school_year_name, semester } = this.activeSchoolYear;

        result = result.filter((c) => {
          return (
            c.schoolYear &&
            c.schoolYear.school_year_name === school_year_name &&
            Number(c.schoolYear.semester) === Number(semester)
          );
        });
      }

      // Search
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

      // Program filter
      if (this.selectedProgram && this.selectedProgram !== "all") {
        result = result.filter(
          (c) => Number(c.program_id) === Number(this.selectedProgram),
        );
      }

      // Role-based filtering
      switch (this.user?.role) {
        case "Admin":
          // Admin can view all classes
          break;

        case "Program Chairperson":
          if (this.user?.program_id) {
            result = result.filter(
              (c) => Number(c.program_id) === Number(this.user.program_id),
            );
          }
          break;

        default:
          // Other roles can view all classes
          break;
      }

      // Sort by year level then section
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
    selectProgram(programId) {
      this.selectedProgram = programId;
      this.showProgramDropdown = false;
      this.changePage(1);
    },
    async loadActiveSchoolYear() {
      const fetchDataStore = useFetchDataStore();

      await fetchDataStore.fetchSchoolYears();

      // Get the latest active school year
      const latestActive = fetchDataStore.school_years
        .filter((sy) => sy.is_active)
        .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))[0];

      this.activeSchoolYear = latestActive || null;

      console.log("Resolved Active School Year:", this.activeSchoolYear);
    },
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
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/class/get-classes-course",
        );

        this.classCourses = data
          .filter((item) => Number(item.class_id) === Number(cls.class_id))
          .sort((a, b) =>
            (a.course_code || "").localeCompare(b.course_code || ""),
          );

        console.log("Selected Class:", cls);
        console.log("Courses:", this.classCourses);
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

      // Get the first number in the set name
      const match = setName.trim().match(/^(\d+)/);

      return match ? Number(match[1]) : null;
    },
  },
  async mounted() {
    this.loading = true;

    await this.fetchUser();

    // Always load the latest active school year from the database
    await this.loadActiveSchoolYear();

    await this.loadClasses();

    this.loading = false;

    // Listen for changes
    this.stopEventBus = eventBus.on(async () => {
      // Always resolve the latest active school year
      await this.loadActiveSchoolYear();

      // Optional: reload classes if needed
      await this.loadClasses();
    });
  },
  beforeUnmount() {
    if (this.stopEventBus) {
      this.stopEventBus();
    }
  },
};
</script>
