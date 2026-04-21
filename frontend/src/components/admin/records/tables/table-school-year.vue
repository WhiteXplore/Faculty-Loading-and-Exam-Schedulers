<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4">Pages / School Years</div>

      <div
        @click="toggleAdd"
        class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
      >
        <div
          class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
        >
          <icon name="circle-add" />
        </div>

        <span class="font-medium text-sm">Add School Year</span>
      </div>
    </div>

    <!-- Controls -->
    <div class="table-container">
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
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
          <span class="text-sm font-medium">Per page</span>
        </div>

        <!-- Filters -->
        <div class="flex items-center gap-3 flex-wrap">
          <!-- Search -->
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search..."
              class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full sm:w-[280px] transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
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
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <table class="min-w-full text-sm text-gray-700 border-collapse">
          <thead class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide">
            <tr>
              <th class="px-4 py-3 text-left w-[10%]">School Year</th>
              <!-- <th class="px-4 py-3 text-center">Start Year</th>
              <th class="px-4 py-3 text-center">End Year</th> -->
              <th class="px-4 py-3 text-center">Semester</th>
              <th class="px-4 py-3 text-center">Status</th>
              <th class="px-4 py-3 text-center rounded-tr-lg w-[10%]">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="sy in paginatedData"
              :key="sy.school_year_id"
              class="hover:bg-green-50 transition-all border-t"
            >
              <td class="px-4 py-3">{{ sy.school_year_name }}</td>
              <!-- <td class="px-4 py-3 text-center">{{ sy.start_year }}</td>
              <td class="px-4 py-3 text-center">{{ sy.end_year }}</td> -->
              <td class="px-4 py-3 text-center">
                {{ getSemesterLabel(sy.semester) }}
              </td>
              <td class="px-4 py-3 text-center">
                <span
                  :class="
                    sy.is_active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  "
                  class="px-2 py-1 rounded-full text-xs font-semibold"
                >
                  {{ sy.is_active ? "Active" : "Inactive" }}
                </span>
              </td>
              <td class="px-4 py-3 flex justify-center">
                <div class="flex gap-2">
                  <button class="btn-edit" @click="toggleEdit(sy)">
                    <icon name="edit" /> Edit
                  </button>
                  <button class="btn-delete" @click="toggleDelete(sy)">
                    <icon name="delete" /> Delete
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="paginatedData.length === 0">
              <td colspan="7" class="text-center py-8 text-gray-400">No records found</td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-gray-700 text-sm">
          Showing {{ startIndex }} to {{ endIndex }} of {{ filteredData.length }} entries
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
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Add / Edit Modals -->
  <addSchoolYear v-if="isAddSchoolYear" @close="closeView" @refresh="loadSchoolYears" />
  <addSchoolYear
    v-if="showEditModal && selectedSchoolYear"
    :schoolYearData="selectedSchoolYear"
    @close="closeModal"
    @refresh="loadSchoolYears"
  />

  <!-- Delete Confirmation -->
  <div v-if="showDeleteModal" class="delete-container">
    <div class="delete-box">
      <div class="delete-icon">
        <icon name="question" class="text-red-600" />
      </div>

      <h1 class="delete-title">Delete Confirmation</h1>

      <p class="delete-text">
        Are you sure you want to delete
        <b>
          {{ getSemesterLabel(recordToDelete?.semester) }} -
          {{ recordToDelete?.start_year }} to
          {{ recordToDelete?.end_year }}
        </b>
        ? This action cannot be undone.
      </p>

      <!-- <div class="delete-divider"></div> -->

      <div class="delete-actions">
        <button class="btn-cancel" @click="showDeleteModal = false">No, Cancel</button>
        <button class="btn-cancel-confirm" @click="confirmDelete">Yes, Delete</button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import addSchoolYear from "../modals/add-school-year.vue";
import axios from "axios";

export default {
  name: "TableSchoolYear",
  components: { icon, addSchoolYear },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAddSchoolYear: false,
      isTable: true,
      showDeleteModal: false,
      recordToDelete: null,
      selectedSchoolYear: null,
      showEditModal: false,
      schoolYears: [],
    };
  },
  computed: {
    filteredData() {
      let result = this.schoolYears || [];

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        result = result.filter(
          (sy) =>
            sy.school_year_name?.toLowerCase().includes(query) ||
            String(sy.start_year).includes(query) ||
            String(sy.end_year).includes(query)
        );
      }

      return result;
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
      return this.filteredData.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },
    endIndex() {
      const end = this.currentPage * this.itemsPerPage;
      return Math.min(end, this.filteredData.length);
    },
  },
  methods: {
    async loadSchoolYears() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years"
        );
        this.schoolYears = response.data;
      } catch (error) {
        console.error("Failed to load school years:", error);
        toast.error("Failed to load school years");
      }
    },

    toggleAdd() {
      this.isAddSchoolYear = true;
      this.isTable = true;
    },
    toggleEdit(item) {
      this.selectedSchoolYear = item;
      this.showEditModal = true;
    },
    toggleDelete(item) {
      this.recordToDelete = item;
      this.showDeleteModal = true;
    },
    confirmDelete() {
      if (!this.recordToDelete || isNaN(this.recordToDelete.school_year_id)) {
        toast.error("Invalid school year ID.");
        return;
      }
      axios
        .delete(
          process.env.VUE_APP_API_BASE_URL +
            `/school-year/delete-id/${this.recordToDelete.school_year_id}`
        )
        .then(() => {
          this.showDeleteModal = false;
          this.recordToDelete = null;
          this.loadSchoolYears();
          toast.success("Record deleted successfully");
        })
        .catch((err) => {
          console.error("Delete failed:", err);
          toast.error("Failed to delete record.");
        });
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
    closeView() {
      this.isAddSchoolYear = false;
    },
    closeModal() {
      this.showEditModal = false;
      this.selectedSchoolYear = null;
    },
    getSemesterLabel(semester) {
      if (semester === 1) return "1st Semester";
      if (semester === 2) return "2nd Semester";
      return "N/A";
    },
  },
  async mounted() {
    await this.loadSchoolYears();
  },
};
</script>
