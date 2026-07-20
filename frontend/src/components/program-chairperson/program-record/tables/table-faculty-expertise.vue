<template>
  <div>
    <!-- Header -->
    <div class="flex justify-between items-center mt-8">
      <div class="text-[13px] text-gray-700">
        Pages / Faculty Expertise Overview
        <span class="text-gray-400 mx-1">/</span>
        <span class="font-semibold text-defaultGreen">{{ activeTab }}</span>
      </div>
    </div>

    <!-- Main Content -->
    <!-- Tabs -->
    <div class="flex gap-2 mt-6">
      <button
        v-for="tab in tabs"
        :key="tab"
        @click="activeTab = tab"
        :class="[
          'px-4 py-2 rounded-t-lg font-normal text-sm transition-all',
          activeTab === tab
            ? 'bg-defaultGreen text-white shadow-md'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
        ]"
      >
        {{ tab }}
      </button>
    </div>
    <div class="overflow-x-auto border p-3 rounded-tr-xl bg-white">
      <!-- Controls -->
      <div class="table-controls">
        <!-- Items per page -->
        <div class="per-page-container">
          <div class="select-wrapper">
            <select
              v-model="itemsPerPage"
              class="select-input"
              @change="changePage(1)"
            >
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
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
        <div class="search-wrapper">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search faculty ..."
            class="search-input"
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

      <!-- Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[69vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead
              class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
            >
              <tr>
                <th class="px-4 py-3 text-left w-[3%] rounded-tl-lg">No.</th>
                <th class="px-4 py-3 text-left w-[20%]">
                  {{
                    activeTab !== "Not Selected Expertise"
                      ? "Faculty Name"
                      : "Course Code"
                  }}
                </th>
                <th class="px-4 py-3 text-left w-[35%]">Course Description</th>
                <th class="px-4 py-3 text-center w-[12%]">Course Level</th>
                <th class="px-4 py-3 text-center w-[12%]">Course Lecture</th>
                <th class="px-4 py-3 text-center w-[12%]">Course Laboratory</th>
                <th class="px-4 py-3 text-left w-[15%]">Program</th>
                <th
                  v-if="activeTab === 'Not Selected Expertise'"
                  class="px-4 py-3 text-center w-[15%]"
                >
                  Assign
                </th>
              </tr>
            </thead>

            <tbody>
              <!-- Expertise / Other Expertise -->
              <template v-if="activeTab !== 'Not Selected Expertise'">
                <tr
                  v-for="(user, index) in paginatedUsers"
                  :key="`${user.id}-${user.course_id}-${user.type}`"
                  class="hover:bg-green-50 transition-all border-t"
                >
                  <td class="px-4 py-4 text-gray-600 text-left">
                    {{ startIndex + index }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.first_name }} {{ user.last_name }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.course_code }} - {{ user.course_title }}
                  </td>
                  <td class="px-4 py-3 truncate text-center">
                    {{ user.course_level }}
                  </td>
                  <td class="px-4 py-3 truncate text-center">
                    {{ user.course_lec }}
                  </td>
                  <td class="px-4 py-3 truncate text-center">
                    {{ user.course_lab }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.program?.program_code || "-" }}
                  </td>
                </tr>
              </template>

              <!-- Not Selected Expertise -->
              <template v-else>
                <tr
                  v-for="(user, index) in paginatedUsers"
                  :key="`not-selected-${user.course_id}-${index}`"
                  class="hover:bg-green-50 transition-all border-t"
                >
                  <td class="px-4 py-4 text-gray-600 text-left">
                    {{ startIndex + index }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.course_code }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.course_title }}
                  </td>
                  <td class="px-4 py-3 truncate text-center">
                    {{ user.course_level }}
                  </td>
                  <td class="px-4 py-3 truncate text-center">
                    {{ user.course_lec }}
                  </td>
                  <td class="px-4 py-3 truncate text-center">
                    {{ user.course_lab }}
                  </td>
                  <td class="px-4 py-3 truncate">
                    {{ user.curriculum?.program?.program_code || "-" }}
                  </td>
                  <td class="px-4 py-3 flex justify-center">
                    <button
                      @click="openAssignModal(user)"
                      class="px-3 py-1.5 bg-defaultGreen text-white rounded-lg hover:bg-green-700 transition text-xs font-medium"
                    >
                      Assign
                    </button>
                  </td>
                </tr>
              </template>

              <!-- No Records -->
              <tr v-if="paginatedUsers.length === 0">
                <td colspan="4" class="text-center py-8 text-gray-400">
                  No records found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-gray-700 text-sm">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredUsers.length }} entries
        </div>
        <div class="flex items-center gap-1 text-sm">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400"
          >
            &lt;
          </button>
          <button
            v-for="page in pageNumbers"
            :key="page"
            @click="changePage(page)"
            :class="{
              'bg-defaultGreen text-white': currentPage === page,
              'bg-gray-200 text-gray-700': currentPage !== page,
            }"
            class="px-3 py-1 rounded-md hover:bg-green-300"
          >
            {{ page }}
          </button>
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400"
          >
            &gt;
          </button>
        </div>
      </div>

      <!-- Assign Instructor Modal -->
      <div v-if="assignDialog" class="modal-overlay">
        <div class="modal-wrapper">
          <div class="modal-container">
            <!-- Header -->
            <div class="modal-header">
              <div class="flex items-center gap-3">
                <div class="glass-container">
                  <icon name="circle-add2" class="text-white" />
                </div>

                <div>
                  <h2 class="text-lg font-semibold text-white">
                    Assign Instructor
                  </h2>

                  <p class="text-xs text-green-100">
                    Assign an instructor to the selected course.
                  </p>
                </div>
              </div>

              <icon
                name="circle-close3"
                @click="closeAssignModal"
                class="close-button-header"
              />
            </div>

            <!-- Body -->
            <div class="modal-body w-[28vw]">
              <!-- Selected Course -->
              <div
                class="rounded-xl border border-gray-100 p-4 bg-white shadow-sm mb-5"
              >
                <div class="text-xs text-gray-500 uppercase tracking-wide mb-1">
                  Selected Course
                </div>

                <div class="font-semibold text-defaultGreen text-base">
                  {{ selectedCourse.course_code }}
                </div>

                <div class="text-sm text-gray-600 mt-1">
                  {{ selectedCourse.course_title }}
                </div>

                <div class="text-xs text-gray-400 mt-2">
                  {{ selectedCourse.program?.program_code }}
                </div>
              </div>

              <!-- Assign -->
              <div class="rounded-xl border border-gray-100 p-4 bg-white">
                <div class="dropdown-container" ref="instructorDropdown">
                  <label class="dropdown-label"> Instructor: </label>

                  <div class="dropdown-wrapper">
                    <input
                      v-model="searchInstructorQuery"
                      type="text"
                      placeholder="Search instructor..."
                      class="dropdown-input"
                      @focus="showInstructorDropdown = true"
                      @input="showInstructorDropdown = true"
                    />

                    <div
                      v-if="showInstructorDropdown"
                      class="dropdown-menu"
                      @mouseleave="showInstructorDropdown = false"
                    >
                      <template v-if="filteredInstructors.length">
                        <div
                          v-for="instr in filteredInstructors"
                          :key="instr.faculty_id"
                          :class="[
                            'dropdown-item border-b',
                            instr.overloadPrep
                              ? 'opacity-50 cursor-not-allowed bg-gray-100'
                              : 'cursor-pointer hover:bg-green-50',
                          ]"
                          @mousedown.prevent="
                            !instr.overloadPrep && selectInstructor(instr)
                          "
                        >
                          <div class="flex justify-between items-center">
                            <div class="font-medium">
                              {{ instr.faculty_name }}
                            </div>
                            <span
                              v-if="instr.overloadPrep"
                              class="px-2 py-0.5 rounded-full bg-red-100 text-red-700 text-[10px] font-semibold"
                            >
                              MAX PREP
                            </span>

                            <span
                              v-else
                              class="px-2 py-0.5 rounded-full bg-green-100 text-green-700 text-[10px]"
                            >
                              {{ instr.prepCount }}/4 Prep
                            </span>
                          </div>

                          <div class="text-[11px] text-gray-500 mb-1">
                            {{ instr.program?.program_code }}
                          </div>

                          <div
                            v-for="course in instr.expertiseCourses"
                            :key="course.course_code"
                            class="text-[11px] text-gray-600 ml-2"
                          >
                            • {{ course.course_code }}
                          </div>
                        </div>
                      </template>

                      <div v-else class="dropdown-empty">
                        No instructor found
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Footer -->
              <div class="modal-footer mt-6">
                <button @click="closeAssignModal" class="btn-cancel">
                  Cancel
                </button>

                <button @click="confirmAssign" class="btn-save">
                  Assign Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
export default {
  name: "FacultyExpertiseOverview",
  components: {
    icon,
  },
  data() {
    return {
      searchQuery: "",
      itemsPerPage: 10,
      currentPage: 1,
      user: null,
      activeTab: "Expertise",
      tabs: [
        "Expertise",
        "Other Expertise",
        "Cross Expertise",
        "Not Selected Expertise",
        "Cross Institute Faculty",
      ],
      allCourses: [],
      assignDialog: false,
      selectedCourse: null,

      searchInstructorQuery: "",
      showInstructorDropdown: false,
      selectedInstructor: null,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["rawusers", "curriculum_courses"]),
    filteredInstructors() {
      let users = this.rawusers || [];

      users = users.filter((u) => u.role === "Faculty");

      if (this.user?.role === "Program Chairperson") {
        users = users.filter(
          (u) =>
            Number(u.institute?.institute_id) ===
              Number(this.user.institute_id) &&
            Number(u.program?.program_id) === Number(this.user.program_id),
        );
      }

      const keyword = this.searchInstructorQuery.toLowerCase();

      return users
        .filter((u) =>
          `${u.first_name} ${u.last_name}`.toLowerCase().includes(keyword),
        )
        .map((u) => {
          const expertiseCourses = (u.expertise || [])
            .filter((e) => e.course)
            .map((e) => ({
              course_code: e.course.course_code,
              course_title: e.course.course_title,
              status: e.status,
            }));

          return {
            ...u,
            faculty_id: u.id,
            faculty_name: `${u.first_name} ${u.last_name}`,

            expertiseCourses,
            prepCount: expertiseCourses.length,
            overloadPrep: expertiseCourses.length >= 4,
          };
        });
    },
    filteredUsers() {
      let users = this.rawusers || [];
      const query = this.searchQuery.trim().toLowerCase();

      // ===============================
      // Filter Faculty
      // ===============================
      users = users.filter(
        (u) => u.role === "Faculty" || u.role === "Program Chairperson",
      );

      // ===============================
      // Program Chairperson Filter
      // ===============================
      if (this.user?.role === "Program Chairperson") {
        users = users.filter(
          (u) =>
            u.role === "Faculty" &&
            Number(u.institute?.institute_id) ===
              Number(this.user.institute_id) &&
            Number(u.program?.program_id) === Number(this.user.program_id),
        );
      }

      let expanded = [];

      // ===============================
      // PRIMARY
      // ===============================
      if (this.activeTab === "Expertise") {
        users.forEach((faculty) => {
          (faculty.expertise || []).forEach((e) => {
            if (!e.course || e.status !== "PRIMARY") return;

            expanded.push({
              ...faculty,
              type: "PRIMARY",
              course_id: Number(e.course.course_id),
              course_code: e.course.course_code,
              course_title: e.course.course_title,
              course_level: e.course.course_level,
              course_lec: e.course.course_lec,
              course_lab: e.course.course_lab,
            });
          });
        });
      }

      // ===============================
      // OTHER
      // ===============================
      if (this.activeTab === "Other Expertise") {
        users.forEach((faculty) => {
          (faculty.expertise || []).forEach((e) => {
            if (!e.course || e.status !== "OTHER") return;

            expanded.push({
              ...faculty,
              type: "OTHER",
              course_id: Number(e.course.course_id),
              course_code: e.course.course_code,
              course_title: e.course.course_title,
              course_level: e.course.course_level,
              course_lec: e.course.course_lec,
              course_lab: e.course.course_lab,
            });
          });
        });
      }

      // ===============================
      // CROSS
      // ===============================
      if (this.activeTab === "Cross Expertise") {
        users.forEach((faculty) => {
          (faculty.expertise || []).forEach((e) => {
            if (!e.course || e.status !== "CROSS") return;
            expanded.push({
              ...faculty,
              type: "CROSS",
              course_id: Number(e.course.course_id),
              course_code: e.course.course_code,
              course_title: e.course.course_title,
              course_level: e.course.course_level,
              course_lec: e.course.course_lec,
              course_lab: e.course.course_lab,
            });
          });
        });
      } // ===============================
      // 🔹 Cross INSTITUTE FACULTY
      // ===============================
      if (this.activeTab === "Cross Institute Faculty") {
        expanded = [];

        const curriculumCourseIds = new Set(
          (this.curriculum_courses || [])
            .filter(
              (cc) =>
                Number(cc.curriculum?.program?.program_id) ===
                  Number(this.user.program_id) &&
                Number(cc.curriculum?.institute?.institute_id) ===
                  Number(this.user.institute_id),
            )
            .map((cc) => Number(cc.course.course_id)),
        );

        const allFaculty = (this.rawusers || []).filter(
          (u) => u.role === "Faculty",
        );

        allFaculty.forEach((faculty) => {
          const isCurrentProgram =
            Number(faculty.institute?.institute_id) ===
              Number(this.user.institute_id) &&
            Number(faculty.program?.program_id) ===
              Number(this.user.program_id);

          // Skip faculty from the current program
          if (isCurrentProgram) return;

          (faculty.expertise || []).forEach((e) => {
            if (!e.course) return;

            if (!curriculumCourseIds.has(Number(e.course.course_id))) return;

            expanded.push({
              ...faculty,
              course_id: Number(e.course.course_id),
              course_code: e.course.course_code,
              course_title: e.course.course_title,
              course_level: e.course.course_level,
              course_lec: e.course.course_lec,
              course_lab: e.course.course_lab,
              type: "Cross Institute Faculty",
            });
          });
        });
      }
      // ===============================
      // 🔹 NOT SELECTED EXPERTISE
      // ===============================
      if (this.activeTab === "Not Selected Expertise") {
        expanded = [];

        // Courses selected by faculty in the CURRENT institute/program
        const currentSelectedCourseIds = new Set();

        // Courses selected by faculty from OTHER institutes/programs
        const otherInstituteCourseIds = new Set();

        // Check every faculty
        (this.rawusers || [])
          .filter((u) => u.role === "Faculty")
          .forEach((faculty) => {
            const isCurrentProgram =
              Number(faculty.institute?.institute_id) ===
                Number(this.user.institute_id) &&
              Number(faculty.program?.program_id) ===
                Number(this.user.program_id);

            (faculty.expertise || []).forEach((e) => {
              if (!e.course?.course_id) return;

              const courseId = Number(e.course.course_id);

              if (isCurrentProgram) {
                currentSelectedCourseIds.add(courseId);
              } else {
                otherInstituteCourseIds.add(courseId);
              }
            });
          });

        // Curriculum of the logged-in Program Chairperson only
        const curriculumCourses = (this.curriculum_courses || [])
          .filter(
            (cc) =>
              Number(cc.curriculum?.program?.program_id) ===
                Number(this.user.program_id) &&
              Number(cc.curriculum?.institute?.institute_id) ===
                Number(this.user.institute_id),
          )
          .filter(
            (cc, index, self) =>
              index ===
              self.findIndex(
                (x) =>
                  Number(x.course.course_id) === Number(cc.course.course_id),
              ),
          );

        curriculumCourses.forEach((cc) => {
          const courseId = Number(cc.course.course_id);

          // Already selected by current faculty
          if (currentSelectedCourseIds.has(courseId)) return;

          // Selected by Cross institute/program
          if (otherInstituteCourseIds.has(courseId)) return;

          expanded.push({
            curriculum_course_id: cc.curriculum_course_id,
            course_id: courseId,
            course_code: cc.course.course_code,
            course_title: cc.course.course_title,
            course_level: cc.course.course_level,
            course_lec: cc.course.course_lec,
            course_lab: cc.course.course_lab,
            curriculum: cc.curriculum,
            program: cc.curriculum.program,
            institute: cc.curriculum.institute,
            type: "Not Selected Expertise",
          });
        });
      }
      // ===============================
      // GENERAL SEARCH
      // ===============================
      if (query) {
        expanded = expanded.filter((item) => {
          const searchable = [
            // Faculty
            item.first_name,
            item.last_name,
            `${item.first_name || ""} ${item.last_name || ""}`,
            item.email,
            item.role,

            // Course
            item.course_code,
            item.course_title,

            // Program
            item.program?.program_name,
            item.program?.program_code,
            item.curriculum?.program?.program_name,
            item.curriculum?.program?.program_code,

            // Institute
            item.institute?.institute_name,
            item.institute?.institute_code,
            item.curriculum?.institute?.institute_name,
            item.curriculum?.institute?.institute_code,

            // Expertise Type
            item.type,

            // Curriculum
            item.curriculum?.curriculum_name,
            item.curriculum?.curriculum_code,
          ]
            .filter(Boolean)
            .join(" ")
            .toLowerCase();

          return searchable.includes(query);
        });
      }

      return expanded;
    },

    paginatedUsers() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredUsers.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredUsers.length / this.itemsPerPage) || 1;
    },

    pageNumbers() {
      const total = this.totalPages;
      if (total <= 3) return Array.from({ length: total }, (_, i) => i + 1);

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
      return this.filteredUsers.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      const end = this.currentPage * this.itemsPerPage;
      return Math.min(end, this.filteredUsers.length);
    },
  },

  methods: {
    openAssignModal(course) {
      this.selectedCourse = course;
      this.assignDialog = true;

      this.searchInstructorQuery = "";
      this.selectedInstructor = null;
      this.showInstructorDropdown = false;
    },

    closeAssignModal() {
      this.assignDialog = false;
    },

    selectInstructor(instructor) {
      this.selectedInstructor = instructor;
      this.searchInstructorQuery = instructor.faculty_name;
      this.showInstructorDropdown = false;
    },

    async confirmAssign() {
      if (!this.selectedInstructor) {
        alert("Please select an instructor.");
        return;
      }

      try {
        await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/users/assign-expertise",
          {
            user_id: this.selectedInstructor.id,
            course_id: this.selectedCourse.course_id,
          },
          {
            withCredentials: true,
          },
        );

        await this.loadRawUsers(); // Refresh the expertise list
        toast.success("Assigning of expertise successfully!");
        this.closeAssignModal();
      } catch (err) {
        alert(err.response?.data?.message || "Failed to assign expertise.");
      }
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(Number(page), this.totalPages));
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

    async loadRawUsers() {
      const store = useFetchDataStore();
      await store.fetchRawUsers();
    },

    async loadCurriculumCourses() {
      const store = useFetchDataStore();
      await store.fetchCurriculumCourses();
    },
  },

  async mounted() {
    await this.fetchUser();
    await this.loadRawUsers();
    await this.loadCurriculumCourses();
  },
};
</script>
