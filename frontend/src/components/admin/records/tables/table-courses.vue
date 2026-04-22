<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4">Pages / Courses</div>
      <div class="per-page-container">
        <!-- Upload & Add -->
        <div
          @click="isUploadModal = true"
          class="flex items-center gap-2 px-3 py-2 border bg-blue-700 text-white border-blue-700 rounded-xl hover:bg-white hover:text-blue-700 hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-blue-500 bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon name="uploads" />
          </div>
          <span class="font-medium text-sm">Upload Course</span>
        </div>

        <div
          @click="toggleAdd"
          class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon name="circle-add" />
          </div>

          <span class="font-medium text-sm">Add Course</span>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-container">
      <!-- Top Controls -->
      <div class="table-controls">
        <!-- Items per page -->
        <div class="per-page-container">
          <div class="select-wrapper">
            <select v-model="itemsPerPage" class="select-input" @change="changePage(1)">
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
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
          <span class="text-sm font-medium text-gray-600">Per page</span>
        </div>

        <div class="flex gap-2">
          <!-- Admin filters -->
          <template v-if="user?.role === 'Admin'">
            <!-- Institute -->
            <div class="relative">
              <div
                class="absolute inset-y-0 left-3 flex items-center text-green-700 pointer-events-none"
              >
                <icon name="building" />
              </div>

              <select
                v-model="selectedInstitute"
                @change="handleInstituteChange"
                class="select-filter-input pr-8"
              >
                <option value="">All Institutes</option>
                <option
                  v-for="inst in uniqueInstitutes"
                  :key="inst.institute_id"
                  :value="inst.institute_id"
                >
                  {{ inst.institute_code || inst.institute_name }}
                </option>
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

            <!-- Program -->
            <div class="relative">
              <div
                class="absolute inset-y-0 left-3 flex items-center text-green-700 pointer-events-none"
              >
                <icon name="layers" />
              </div>

              <select
                v-model="selectedProgram"
                @change="handleProgramChange"
                class="select-filter-input pr-8"
              >
                <option value="">All Programs</option>
                <option
                  v-for="prog in filteredPrograms"
                  :key="prog.program_id"
                  :value="prog.program_id"
                >
                  {{ prog.program_code || prog.program_name }}
                </option>
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

            <!-- Curriculum -->
            <div class="relative">
              <div
                class="absolute inset-y-0 left-3 flex items-center text-green-700 pointer-events-none"
              >
                <icon name="book" />
              </div>

              <select
                v-model="selectedCurriculum"
                @change="currentPage = 1"
                class="select-filter-input pr-8"
              >
                <option value="">All Curriculums</option>
                <option
                  v-for="curr in filteredCurriculums"
                  :key="curr.curriculum_id"
                  :value="curr.curriculum_id"
                >
                  {{
                    `${curr.program_code || curr.program_name || "Program"} (${
                      curr.curriculum_start_year || "-"
                    } - ${curr.curriculum_end_year || "-"})`
                  }}
                </option>
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
          </template>

          <!-- Search input -->
          <div class="search-wrapper">
            <input
              v-model="searchQuery"
              @input="currentPage = 1"
              type="text"
              placeholder="Search courses..."
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
      </div>

      <!-- Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[69vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide">
              <tr>
                <th class="text-left w-[8%]">Course Code</th>
                <th class="text-left">Course Title</th>
                <th class="text-center">Semester</th>
                <th class="text-center">Year Level</th>
                <th class="text-center">Lecture</th>
                <th class="text-center">Lab</th>
                <th class="text-center">Units</th>
                <th class="text-center">Pre-requisite</th>
                <th class="text-center rounded-tr-lg w-[10%]">Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="c in paginatedData"
                :key="c.curriculum_course_id"
                class="hover:bg-green-50 border-t transition-all"
              >
                <td>{{ c.course?.course_code || "-" }}</td>
                <td>{{ c.course?.course_title || "-" }}</td>
                <td class="text-center">{{ c.course?.course_semester || "-" }}</td>
                <td class="text-center">{{ c.course?.course_level || "-" }}</td>
                <td class="text-center">{{ c.course?.course_lec ?? 0 }}</td>
                <td class="text-center">{{ c.course?.course_lab ?? 0 }}</td>
                <td class="text-center">
                  {{ (c.course?.course_lec ?? 0) + (c.course?.course_lab ?? 0) }}
                </td>
                <td class="text-center">{{ c.course?.course_requisite || "-" }}</td>
                <td class="flex justify-center">
                  <div class="flex gap-2">
                    <button class="btn-edit" @click="toggleEdit(c)">
                      <icon name="edit" /> Edit
                    </button>
                    <button class="btn-delete" @click="toggleDelete(c)">
                      <icon name="delete" /> Delete
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="paginatedData.length === 0">
                <td colspan="9" class="text-center py-8 text-gray-400">
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
          {{ filteredCourses.length }} entries
        </div>

        <div class="flex items-center gap-1 text-sm">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 rounded-l-md hover:bg-gray-400"
          >
            &lt;
          </button>

          <button
            v-for="page in pageNumbers"
            :key="'page-' + page"
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
            class="px-3 py-1 bg-gray-300 rounded-r-md hover:bg-gray-400"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>
  </div>

  <div v-if="showDeleteModal" class="delete-container">
    <div class="delete-box">
      <div class="delete-icon">
        <icon name="question" class="text-red-600" />
      </div>

      <h1 class="delete-title">Delete Confirmation</h1>

      <p class="delete-text">
        Are you sure you want to delete
        <b>
          {{ recordToDelete?.course?.course_code }} -
          {{ recordToDelete?.course?.course_title }}
        </b>
        ? This action cannot be undone.
      </p>

      <div class="delete-actions">
        <button class="btn-cancel" @click="showDeleteModal = false">No, Cancel</button>
        <button class="btn-cancel-confirm" @click="confirmDelete">Yes, Delete</button>
      </div>
    </div>
  </div>

  <!-- Add/Edit/Upload Modals -->
  <addCourses
    v-if="(showEditModal && selectedCourse) || isAddCourses"
    :courseData="selectedCourse?.course || selectedCourse"
    @close="closeModal"
    @refresh="loadCourses"
  />

  <uploadCourses
    v-if="isUploadModal"
    @close="isUploadModal = false"
    @refresh="loadCourses"
  />
</template>

<script>
import icon from "@/assets/icon.vue";
import addCourses from "../modals/add-courses.vue";
import uploadCourses from "../modals/upload-course.vue";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TableCourses",
  components: { icon, addCourses, uploadCourses },

  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",

      // ADMIN FILTERS
      selectedInstitute: "",
      selectedProgram: "",
      selectedCurriculum: "",

      isAddCourses: false,
      isTable: true,
      isUploadModal: false,
      showEditModal: false,
      selectedCourse: null,
      user: null,
      showDeleteModal: false,
      recordToDelete: null,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["curriculum_courses"]),

    uniqueInstitutes() {
      const map = new Map();

      (this.curriculum_courses || []).forEach((c) => {
        const institute =
          c.curriculum?.program?.institute ||
          (c.curriculum?.institute_id
            ? {
                institute_id: c.curriculum.institute_id,
                institute_name: `Institute ${c.curriculum.institute_id}`,
                institute_code: "",
              }
            : null);

        if (institute?.institute_id && !map.has(institute.institute_id)) {
          map.set(institute.institute_id, institute);
        }
      });

      return Array.from(map.values());
    },
    filteredPrograms() {
      const map = new Map();

      (this.curriculum_courses || []).forEach((c) => {
        const curriculum = c.curriculum;
        const program = c.curriculum?.program;

        const programId = curriculum?.program_id;
        const instituteId = curriculum?.institute_id;

        if (!programId) return;

        if (
          this.selectedInstitute &&
          String(instituteId) !== String(this.selectedInstitute)
        ) {
          return;
        }

        if (!map.has(programId)) {
          map.set(programId, {
            program_id: programId,
            institute_id: instituteId,
            program_code: program?.program_code || `Program ${programId}`,
            program_name: program?.program_name || `Program ${programId}`,
          });
        }
      });

      return Array.from(map.values());
    },

    filteredCurriculums() {
      const map = new Map();

      (this.curriculum_courses || []).forEach((c) => {
        const curriculum = c.curriculum;
        const program = c.curriculum?.program;

        if (!curriculum?.curriculum_id) return;

        if (
          this.selectedInstitute &&
          String(curriculum.institute_id) !== String(this.selectedInstitute)
        ) {
          return;
        }

        if (
          this.selectedProgram &&
          String(curriculum.program_id) !== String(this.selectedProgram)
        ) {
          return;
        }

        if (!map.has(curriculum.curriculum_id)) {
          map.set(curriculum.curriculum_id, {
            curriculum_id: curriculum.curriculum_id,
            curriculum_start_year: curriculum.curriculum_start_year,
            curriculum_end_year: curriculum.curriculum_end_year,
            institute_id: curriculum.institute_id,
            program_id: curriculum.program_id,
            program_code: program?.program_code || "",
            program_name: program?.program_name || "",
          });
        }
      });

      return Array.from(map.values());
    },

    filteredCourses() {
      let result = this.curriculum_courses || [];

      // Program Chair filter
      if (this.user?.role === "Program Chairperson") {
        result = result.filter((c) => {
          const instituteId =
            c.curriculum?.program?.institute?.institute_id || c.curriculum?.institute_id;

          const programId = c.curriculum?.program?.program_id || c.curriculum?.program_id;

          return (
            String(instituteId) === String(this.user.institute_id) &&
            String(programId) === String(this.user.program_id)
          );
        });
      }

      // Admin filters
      if (this.user?.role === "Admin") {
        if (this.selectedInstitute) {
          result = result.filter(
            (c) => String(c.curriculum?.institute_id) === String(this.selectedInstitute)
          );
        }

        if (this.selectedProgram) {
          result = result.filter(
            (c) => String(c.curriculum?.program_id) === String(this.selectedProgram)
          );
        }

        if (this.selectedCurriculum) {
          result = result.filter(
            (c) => String(c.curriculum?.curriculum_id) === String(this.selectedCurriculum)
          );
        }
      }

      // Search filter
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();

        result = result.filter((c) => {
          const courseCode = c.course?.course_code?.toLowerCase() || "";
          const courseTitle = c.course?.course_title?.toLowerCase() || "";
          const requisite = c.course?.course_requisite?.toLowerCase() || "";
          const programText =
            c.curriculum?.program?.program_code?.toLowerCase() ||
            c.curriculum?.program?.program_name?.toLowerCase() ||
            "";
          const instituteText =
            c.curriculum?.program?.institute?.institute_code?.toLowerCase() ||
            c.curriculum?.program?.institute?.institute_name?.toLowerCase() ||
            "";

          return (
            courseCode.includes(q) ||
            courseTitle.includes(q) ||
            requisite.includes(q) ||
            programText.includes(q) ||
            instituteText.includes(q)
          );
        });
      }

      return result;
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredCourses.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredCourses.length / this.itemsPerPage) || 1;
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
      return this.filteredCourses.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(this.currentPage * this.itemsPerPage, this.filteredCourses.length);
    },
  },

  methods: {
    async fetchUser() {
      try {
        const res = await axios.get(`${process.env.VUE_APP_API_BASE_URL}/auth/me`, {
          withCredentials: true,
        });
        this.user = res.data || null;
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },

    async loadCourses() {
      const store = useFetchDataStore();
      await store.fetchCurriculumCourses();
    },

    handleInstituteChange() {
      this.selectedProgram = "";
      this.selectedCurriculum = "";
      this.currentPage = 1;
    },

    handleProgramChange() {
      this.selectedCurriculum = "";
      this.currentPage = 1;
    },

    toggleAdd() {
      this.selectedCourse = null;
      this.showEditModal = false;
      this.isAddCourses = true;
    },

    toggleEdit(course) {
      this.isAddCourses = false;
      this.selectedCourse = course;
      this.showEditModal = true;
    },

    toggleDelete(course) {
      this.recordToDelete = course;
      this.showDeleteModal = true;
    },

    async confirmDelete() {
      try {
        const courseId = this.recordToDelete?.course?.course_id;

        if (!courseId) return;

        await axios.delete(
          `${process.env.VUE_APP_API_BASE_URL}/courses/delete-id/${courseId}`,
          { withCredentials: true }
        );

        await this.loadCourses();

        this.showDeleteModal = false;
        this.recordToDelete = null;
      } catch (error) {
        console.error("Delete failed:", error);
        alert("Failed to delete course");
      }
    },

    closeModal() {
      this.isAddCourses = false;
      this.showEditModal = false;
      this.selectedCourse = null;
    },

    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
  },

  async mounted() {
    await this.fetchUser();
    await this.loadCourses();
  },
};
</script>
