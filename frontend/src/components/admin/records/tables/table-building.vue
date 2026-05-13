<template>
  <div v-if="isTable" class="">
    <div class="flex justify-between items-center px-1 text-sm">
      <!-- LEFT -->
      <div class="text-[13px] text-text font-regular">Pages / Buildings</div>

      <!-- RIGHT -->
      <div class="flex gap-2">
        <!-- Upload Building -->
        <!-- <div
          @click="isUploadModal = true"
          class="btn-gui"
        >
          <div
           class="btn-add-icon"
          >
            <icon name="uploads" />
          </div>

             <span class="btn-add-text">Upload Building</span>
        </div> -->

        <!-- Add Building -->
        <div
          @click="toggleAdd"
          class="btn-add"
        >
          <div
            class="btn-add-icon"
          >
            <icon name="add-account1.1" />
          </div>

             <span class="btn-add-text">Add Building</span>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-container">
      <!-- Controls -->
      <div class="table-controls">
        <!-- Per page -->
        <div class="per-page-container">
          <div class="select-wrapper">
            <select v-model="itemsPerPage" class="select-input" @change="changePage(1)">
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
            </select>
            <div
              class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-defaultGreen transition-colors"
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

        <!-- Search -->
        <div class="search-wrapper">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search..."
            class="search-input"
            @input="changePage(1)"
          />

          <div class="absolute inset-y-0 left-3 flex items-center text-defaultGreen">
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
        <div class="max-h-[65vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead class="bg-defaultGreen text-white sticky top-0">
              <tr>
                <th class="px-4 py-3 text-left font-normal w-[25%]">Building Name</th>
                <th class="px-4 py-3 text-left font-normal w-[25%]">College Branch</th>
                <th class="px-4 py-3 text-left font-normalw-[25%]">Area</th>
                <th class="px-4 py-3 text-center font-normal w-[1%]">Actions</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="building in paginatedData"
                :key="building.building_id"
                class="hover:bg-green-50 border-t"
              >
                <td class="px-4 py-3">
                  {{ building.building_name }}
                </td>

                <td class="px-4 py-3">
                  {{ building.buildingArea?.collegeBranch?.college_branch_name }}
                </td>

                <td class="px-4 py-3">
                  {{ building.buildingArea?.area_name }}
                </td>

                <td class="px-4 py-3 flex justify-center">
                  <div class="flex gap-2">
                    <button class="btn-edit" @click="toggleEdit(building)">
                      <icon name="edit" /> Edit
                    </button>

                    <button class="btn-delete" @click="toggleDelete(building)">
                      <icon name="delete" /> Delete
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="paginatedData.length === 0">
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
          Showing {{ startIndex }} to {{ endIndex }} of {{ filteredData.length }} entries
        </div>

        <div class="flex items-center gap-1 text-sm">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 rounded-l-md"
          >
            &lt;
          </button>

          <button
            v-for="page in pageNumbers"
            :key="page"
            @click="changePage(page)"
            :class="[
              'px-3 py-1 rounded-md',
              currentPage === page ? 'bg-defaultGreen text-white' : 'bg-gray-200',
            ]"
          >
            {{ page }}
          </button>

          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 bg-gray-300 rounded-r-md"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>

    <!-- ADD MODAL -->
    <addBuilding v-if="isAdd" @close="isAdd = false" @refresh="loadBuildings" />

    <!-- EDIT MODAL -->
    <addBuilding
      v-if="showEditModal"
      :buildingData="selectedBuilding"
      @close="closeModal"
      @refresh="loadBuildings"
    />
  </div>
  <!-- DELETE CONFIRMATION MODAL -->

  <div v-if="showDeleteModal" class="delete-container">
    <div class="delete-box">
      <div class="delete-icon">
        <icon name="question" class="text-red-600" />
      </div>

      <h1 class="delete-title">Delete Confirmation</h1>

      <p class="delete-text">
        Are you sure you want to delete
        <b>{{ recordToDelete?.building_name }}</b> ? This action cannot be undone.
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
import addBuilding from "../modals/add-building.vue";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";
import { toast } from "vue3-toastify";

export default {
  name: "TableBuilding",

  components: {
    icon,
    addBuilding,
  },

  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",

      isAdd: false,
      isTable: true,

      selectedBuilding: null,
      showEditModal: false,

      recordToDelete: null,
      showDeleteModal: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["buildings"]),

    filteredData() {
      const query = this.searchQuery.toLowerCase();

      const filtered = this.buildings.filter((item) =>
        [
          item.building_name,
          item.buildingArea?.collegeBranch?.college_branch_name,
          item.buildingArea?.area_name,
        ]
          .join(" ")
          .toLowerCase()
          .includes(query)
      );

      // Sort by Area number (Area 1 → Area 7)
      return filtered.sort((a, b) => {
        const areaA = parseInt(a.buildingArea?.area_name?.replace("Area ", "")) || 0;
        const areaB = parseInt(b.buildingArea?.area_name?.replace("Area ", "")) || 0;

        return areaA - areaB;
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
      const end = this.currentPage * this.itemsPerPage;
      return end > this.filteredData.length ? this.filteredData.length : end;
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
    async loadBuildings() {
      const store = useFetchDataStore();
      await store.fetchBuildings();
    },

    toggleAdd() {
      this.isAdd = true;
    },

    toggleEdit(item) {
      this.selectedBuilding = item;
      this.showEditModal = true;
    },
    toggleDelete(item) {
      this.recordToDelete = item;
      this.showDeleteModal = true;
    },

    async confirmDelete() {
      try {
        await axios.delete(
          `${process.env.VUE_APP_API_BASE_URL}/buildings/${this.recordToDelete.building_id}`
        );
        toast.success("Building area deleted successfully");

        this.showDeleteModal = false;
        this.recordToDelete = null;

        this.loadBuildings();
      } catch (error) {
        console.error(error);
        toast.error("Failed to delete building area");
      }
    },

    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },

    closeModal() {
      this.showEditModal = false;
      this.selectedBuilding = null;
    },
  },

  mounted() {
    this.loadBuildings();
  },
};
</script>
