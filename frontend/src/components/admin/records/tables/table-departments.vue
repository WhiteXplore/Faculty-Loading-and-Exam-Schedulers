<template>
  <div v-if="isTable">
    <div class="table-container">
      <!-- Top Controls -->
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

            <div class="select-arrow">
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

          <span class="per-page-label">Per page</span>
        </div>

        <div class="flex gap-2">
          <!-- Search -->
          <div class="search-wrapper">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search departments..."
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

          <!-- Add Department -->
          <div @click="toggleAdd" class="btn-add">
            <div class="btn-add-icon">
              <icon name="add-account1.1" />
            </div>
            <span class="btn-add-text">Add Department</span>
          </div>
        </div>
      </div>

      <!-- Departments Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[73vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead
              class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
            >
              <tr>
                <th class="px-4 py-3 text-left font-normal">Department Name</th>

                <th class="px-4 py-3 text-left font-normal">Institute Name</th>

                <th
                  class="px-4 py-3 text-center rounded-tr-lg font-normal w-[15%]"
                >
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="department in paginatedData"
                :key="department.department_id"
                class="hover:bg-green-50 transition-all border-t"
              >
                <!-- Department Name -->
                <td class="px-4 py-3 border-t border-gray-200">
                  {{ department.department_name }}
                </td>

                <!-- Institute Name -->
                <td class="px-4 py-3 border-t border-gray-200">
                  <span
                    v-if="department.institute"
                    class="inline-flex items-center px-2.5 py-1 rounded-md bg-green-50 text-green-800 text-xs font-medium"
                  >
                    {{ department.institute.institute_name }}
                  </span>

                  <span v-else class="text-gray-400 italic">
                    No institute assigned
                  </span>
                </td>

                <!-- Actions -->
                <td class="px-4 py-3 border-t border-gray-200">
                  <div class="flex gap-2 justify-center">
                    <button class="btn-edit" @click="toggleEdit(department)">
                      <icon name="edit" />
                      Edit
                    </button>

                    <button
                      class="btn-delete"
                      @click="toggleDelete(department)"
                    >
                      <icon name="delete" />
                      Delete
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="paginatedData.length === 0">
                <td
                  colspan="3"
                  class="text-center py-8 text-gray-400 border-t border-gray-200"
                >
                  {{
                    isLoading
                      ? "Loading departments..."
                      : "No departments found"
                  }}
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
          {{ filteredData.length }} entries
        </div>

        <div class="flex items-center gap-1 text-sm">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            &lt;
          </button>

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

          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Add / Edit Department Modal -->
  <addDepartment
    v-if="isAdd || editData"
    :editData="editData"
    @close="closeModal"
    @refresh="loadDepartments"
  />

  <!-- Delete Confirmation Modal -->
  <div v-if="showDeleteModal" class="delete-container">
    <div class="delete-box">
      <div class="delete-icon">
        <icon name="question" class="text-red-600" />
      </div>

      <h1 class="delete-title">Delete Confirmation</h1>

      <p class="delete-text">
        Are you sure you want to delete
        <b>{{ recordToDelete?.department_name }}</b
        >? This action cannot be undone.
      </p>

      <div class="delete-actions">
        <button
          class="btn-cancel"
          @click="showDeleteModal = false"
          :disabled="isDeleting"
        >
          No, Cancel
        </button>

        <button
          class="btn-cancel-confirm"
          @click="confirmDelete"
          :disabled="isDeleting"
        >
          {{ isDeleting ? "Deleting..." : "Yes, Delete" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import addDepartment from "../modals/add-departments.vue";
import { toast } from "vue3-toastify";
import axios from "axios";
import { useFetchDataStore } from "@/store/fetch-data-store";
export default {
  name: "TableDepartments",

  components: {
    icon,
    addDepartment,
  },

  data() {
    return {
      fetchDataStore: useFetchDataStore(),
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAdd: false,
      editData: null,
      isTable: true,
      showDeleteModal: false,
      recordToDelete: null,
      isLoading: false,
      isDeleting: false,
    };
  },

  computed: {
    departments() {
      return this.fetchDataStore.departments || [];
    },

    filteredData() {
      const query = this.searchQuery.trim().toLowerCase();

      return this.departments.filter((department) => {
        const departmentName = (department.department_name || "").toLowerCase();

        const instituteName = (
          department.institute?.institute_name || ""
        ).toLowerCase();

        return departmentName.includes(query) || instituteName.includes(query);
      });
    },

    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;

      return this.filteredData.slice(start, start + this.itemsPerPage);
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
  },

  methods: {
    async loadDepartments() {
      this.isLoading = true;

      try {
        await this.fetchDataStore.fetchDepartments();

        if (this.fetchDataStore.error) {
          throw new Error(this.fetchDataStore.error);
        }

        this.changePage(this.currentPage);
      } catch (error) {
        console.error("Failed to load departments:", error);
        toast.error("Failed to load departments.");
      } finally {
        this.isLoading = false;
      }
    },

    toggleAdd() {
      this.editData = null;
      this.isAdd = true;
    },

    toggleEdit(department) {
      this.editData = { ...department };
      this.isAdd = true;
    },

    toggleDelete(department) {
      this.recordToDelete = department;
      this.showDeleteModal = true;
    },

    async confirmDelete() {
      if (
        !this.recordToDelete ||
        !Number.isInteger(Number(this.recordToDelete.department_id))
      ) {
        toast.error("Invalid department ID.");
        return;
      }

      if (this.isDeleting) return;

      this.isDeleting = true;

      try {
        await axios.delete(
          `${process.env.VUE_APP_API_BASE_URL}/departments/${this.recordToDelete.department_id}`,
        );

        this.showDeleteModal = false;
        this.recordToDelete = null;

        toast.success("Department deleted successfully.");

        await this.loadDepartments();
      } catch (error) {
        console.error("Department deletion failed:", error);

        toast.error(
          error.response?.data?.message || "Failed to delete department.",
        );
      } finally {
        this.isDeleting = false;
      }
    },

    changePage(page) {
      const targetPage = Number(page) || 1;

      this.currentPage = Math.max(1, Math.min(targetPage, this.totalPages));
    },

    closeModal() {
      this.isAdd = false;
      this.editData = null;
    },
  },

  mounted() {
    this.loadDepartments();
  },
};
</script>
