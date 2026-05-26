<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4">Pages / Courses</div>

      <div class="per-page-container">
        <!-- Upload -->
        <div @click="isUploadModal = true" class="btn-gui">
          <div class="btn-add-icon">
            <icon name="uploads" />
          </div>
          <span class="btn-add-text">Upload Course</span>
        </div>

        <!-- Add -->
        <div @click="toggleAdd" class="btn-add">
          <div class="btn-add-icon">
            <icon name="add-account1.1" />
          </div>

          <span class="btn-add-text">Add Course</span>
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

          <span class="text-sm font-medium text-gray-600"> Per page </span>
        </div>

        <!-- Search -->
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
                :key="c.course_id"
                class="hover:bg-green-50 border-t transition-all"
              >
                <td>{{ c.course_code || "-" }}</td>
                <td>{{ c.course_title || "-" }}</td>
                <td class="text-center">{{ c.course_semester || "-" }}</td>
                <td class="text-center">{{ c.course_level || "-" }}</td>
                <td class="text-center">{{ c.course_lec ?? 0 }}</td>
                <td class="text-center">{{ c.course_lab ?? 0 }}</td>

                <td class="text-center">
                  {{ (c.course_lec ?? 0) + (c.course_lab ?? 0) }}
                </td>

                <td class="text-center">
                  {{ c.course_requisite || "-" }}
                </td>

                <td class="flex justify-center">
                  <div class="flex gap-2">
                    <button class="btn-edit" @click="toggleEdit(c)">
                      <icon name="edit" />
                      Edit
                    </button>

                    <button class="btn-delete" @click="toggleDelete(c)">
                      <icon name="delete" />
                      Delete
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

  <!-- DELETE MODAL -->
  <div v-if="showDeleteModal" class="delete-container">
    <div class="delete-box">
      <div class="delete-icon">
        <icon name="question" class="text-red-600" />
      </div>

      <h1 class="delete-title">Delete Confirmation</h1>

      <p class="delete-text">
        Are you sure you want to delete
        <b>
          {{ recordToDelete?.course_code }} -
          {{ recordToDelete?.course_title }}
        </b>
        ? This action cannot be undone.
      </p>

      <div class="delete-actions">
        <button class="btn-cancel" @click="showDeleteModal = false">No, Cancel</button>

        <button class="btn-cancel-confirm" @click="confirmDelete">Yes, Delete</button>
      </div>
    </div>
  </div>

  <!-- MODALS -->
  <addCourses
    v-if="(showEditModal && selectedCourse) || isAddCourses"
    :courseData="selectedCourse"
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
import { toast } from "vue3-toastify";

export default {
  name: "TableCourses",

  components: {
    icon,
    addCourses,
    uploadCourses,
  },

  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",

      isAddCourses: false,
      isTable: true,
      isUploadModal: false,

      showEditModal: false,
      selectedCourse: null,

      showDeleteModal: false,
      recordToDelete: null,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["courses"]),

    filteredCourses() {
      let result = this.courses || [];

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();

        result = result.filter((c) => {
          const code = c.course_code?.toLowerCase() || "";
          const title = c.course_title?.toLowerCase() || "";
          const requisite = c.course_requisite?.toLowerCase() || "";

          return code.includes(q) || title.includes(q) || requisite.includes(q);
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
      return this.filteredCourses.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(this.currentPage * this.itemsPerPage, this.filteredCourses.length);
    },
  },

  methods: {
    async loadCourses() {
      const store = useFetchDataStore();

      await store.fetchCourses();
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
        const courseId = this.recordToDelete?.course_id;

        if (!courseId) return;

        await axios.delete(
          `${process.env.VUE_APP_API_BASE_URL}/courses/delete-id/${courseId}`,
          {
            withCredentials: true,
          }
        );

        await this.loadCourses();

        toast.success("Course deleted successfully");

        this.showDeleteModal = false;
        this.recordToDelete = null;
      } catch (error) {
        console.error("Delete failed:", error);

        toast.error("Failed to delete course");
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
    await this.loadCourses();
  },
};
</script>
