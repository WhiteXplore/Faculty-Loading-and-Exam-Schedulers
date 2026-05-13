<template>
  <div v-if="isTable">
    <!-- Header & Add Button -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4 font-regular">Pages / Institute</div>
      <div
        @click="toggleAdd"
        class="btn-add"
      >
        <div
          class="btn-add-icon"
        >
          <icon name="add-account1.1" />
        </div>

           <span class="btn-add-text">Add Institute</span>
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
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
            </select>

            <div class="select-arrow">
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

          <span class="per-page-label">Per page</span>
        </div>

        <!-- Search -->
        <div class="search-wrapper">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search..."
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
      </div>

      <!-- Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[69vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide">
              <tr>
                <th class="px-4 py-3 text-left font-normal">Institute Code</th>
                <th class="px-4 py-3 text-left font-normal">Institute Title</th>
                <th class="px-4 py-3 text-left font-normal">Program Code</th>
                <th class="px-4 py-3 text-left font-normal">Program Title</th>
                <th class="px-4 py-3 text-center rounded-tr-lg font-normal w-[10%]">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="program in paginatedData"
                :key="program.program_id"
                class="hover:bg-green-50 transition-all border-t"
              >
                <td class="px-4 py-3 border-t border-gray-200">
                  {{ program.institute?.institute_code }}
                </td>
                <td class="px-4 py-3 border-t border-gray-200">
                  {{ program.institute?.institute_name }}
                </td>
                <td class="px-4 py-3 border-t border-gray-200">
                  {{ program.program_code }}
                </td>
                <td class="px-4 py-3 border-t border-gray-200">
                  {{ program.program_name }}
                </td>
                <td class="px-4 py-3 flex justify-center">
                  <div class="flex gap-2">
                    <button class="btn-edit" @click="toggleEdit(program)">
                      <icon name="edit" /> Edit
                    </button>
                    <button class="btn-delete" @click="toggleDelete(program)">
                      <icon name="delete" /> Delete
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="paginatedData.length === 0">
                <td
                  colspan="6"
                  class="text-center py-8 text-gray-400 border-t border-gray-200"
                >
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
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Add / Edit Modal -->
  <addInstitute
    v-if="isAdd || editData"
    :editData="editData"
    :institutes="institutes"
    @close="closeModal"
    @refresh="loadPrograms"
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
        <b>
          {{ recordToDelete?.institute?.institute_code }} -
          {{ recordToDelete?.program_code }}
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
import addInstitute from "../modals/add-institutes.vue";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TablePrograms",
  components: { icon, addInstitute },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAdd: false,
      editData: null,
      isTable: true,
      showDeleteModal: false,
      recordToDelete: null,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["programs", "institutes"]),

    filteredData() {
      const query = this.searchQuery.toLowerCase();

      // Step 1: Filter programs by search query
      const filtered = this.programs.filter((item) =>
        `${item.institute?.institute_name} ${item.institute?.institute_code} ${item.program_code} ${item.program_name}`
          .toLowerCase()
          .includes(query)
      );

      // Step 2: Remove duplicates based on all 4 fields
      const unique = [];
      const seen = new Set();

      for (const item of filtered) {
        const key = `${item.institute?.institute_name || ""}|${
          item.institute?.institute_code || ""
        }|${item.program_code}|${item.program_name}`;
        if (!seen.has(key)) {
          seen.add(key);
          unique.push(item);
        }
      }

      return unique;
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
      const end = this.currentPage * this.itemsPerPage;
      return end > this.filteredData.length ? this.filteredData.length : end;
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
  },

  methods: {
    async loadPrograms() {
      const store = useFetchDataStore();
      await store.fetchPrograms();
      await store.fetchInstitutes(); // fetch institutes for dropdown
    },
    toggleAdd() {
      this.isAdd = true;
      this.editData = null;
    },
    toggleEdit(program) {
      this.editData = {
        ...program,
        institute: program.institute || null,
      };
      this.isAdd = true;
    },
    toggleDelete(program) {
      this.recordToDelete = program;
      this.showDeleteModal = true;
    },
    confirmDelete() {
      if (!this.recordToDelete || isNaN(this.recordToDelete.program_id)) {
        toast.error("Invalid program ID.");
        return;
      }
      axios
        .delete(
          process.env.VUE_APP_API_BASE_URL +
            `/programs/delete-id/${this.recordToDelete.program_id}`
        )
        .then(() => {
          this.recordToDelete = null;
          this.showDeleteModal = false;
          new Audio(require("@/assets/delete.mp3")).play();
          this.loadPrograms();
          toast.success("Record deleted successfully");
        })
        .catch((error) => {
          console.error("Delete failed:", error);
          toast.error("Failed to delete record.");
        });
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
    closeModal() {
      this.isAdd = false;
      this.editData = null;
    },
  },
  mounted() {
    this.loadPrograms();
  },
};
</script>
