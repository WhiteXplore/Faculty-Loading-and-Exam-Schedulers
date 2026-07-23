<template>
  <div v-if="isTable" class=" ">
    <div class="flex justify-between items-center px-1 text-sm">
      <!-- LEFT (Pages Title) -->
      <div class="text-[13px] text-text font-regular">
        Pages / Rooms Availability
      </div>

      <!-- RIGHT (Buttons) -->
      <div class="flex gap-2">
        <!-- Upload Room -->
        <div @click="isUploadModal = true" class="btn-gui">
          <div class="btn-add-icon">
            <icon name="uploads" />
          </div>

          <span class="btn-add-text">Upload Room</span>
        </div>

        <!-- Add Room -->
        <div @click="toggleAdd" class="btn-add">
          <div class="btn-add-icon">
            <icon name="add-account1.1" />
          </div>

          <span class="btn-add-text">Add Room</span>
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
              class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-defaultGreen transition-colors"
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
          <!-- Search icon -->
          <div
            class="absolute inset-y-0 left-3 flex items-center text-defaultGreen pointer-events-none transition-colors"
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
        <div class="max-h-[65vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead
              class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
            >
              <tr>
                <th class="px-4 py-3 text-left font-normal w-[4%]">
                  Room Name
                </th>
                <th class="px-4 py-3 text-center font-normal w-[4%]">
                  Room Type
                </th>
                <th class="px-4 py-3 text-center font-normal w-[4%]">
                  Room Capacity
                </th>
                <th class="px-4 py-3 text-center font-normal w-[4%]">
                  Institute
                </th>
                <th class="px-4 py-3 text-center font-normal w-[10%]">
                  Building Name
                </th>
                <th class="px-4 py-3 text-center font-normal w-[4%]">Status</th>

                <th
                  class="px-4 py-3 text-center rounded-tr-lg font-normal w-[1%]"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="rooms_data in paginatedData"
                :key="rooms_data.rooms_id"
                class="hover:bg-green-50 transition-all border-t"
              >
                <td class="px-4 py-3 text-left">
                  {{ rooms_data.room_name }}
                </td>

                <td class="px-4 py-3 text-center">
                  {{ rooms_data.room_type }}
                </td>
                <td class="px-4 py-3 text-center">
                  {{ rooms_data.room_capacity }}
                </td>
                <td class="px-4 py-3 text-center">
                  {{ rooms_data.institute?.institute_code || "-" }}
                </td>
                <td class="px-4 py-3 text-center">
                  {{ rooms_data.building?.building_name }}
                </td>

                <td class="px-4 py-3 text-center">
                  <span
                    :class="{
                      'border-emerald-200 bg-emerald-50 text-emerald-700':
                        rooms_data.is_active,

                      'border-slate-200 bg-slate-100 text-slate-600':
                        !rooms_data.is_active,
                    }"
                    class="inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold"
                  >
                    {{ rooms_data.is_active ? "Active" : "Inactive" }}
                  </span>
                </td>

                <td class="px-4 py-3 flex justify-center">
                  <div class="flex gap-2 justify-center">
                    <button class="btn-edit" @click="toggleEdit(rooms_data)">
                      <icon name="edit" /> Edit
                    </button>

                    <button
                      class="btn-delete"
                      @click="toggleDelete(rooms_data)"
                    >
                      <icon name="delete" /> Delete
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="paginatedData.length === 0">
                <td colspan="6" class="text-left py-6 text-gray-400">
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
          {{ filteredData.length }} entries
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
                ' bg-defaultGreen text-white': currentPage === page,
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

  <addRooms v-if="isAdd" @close="closeView" @refresh="loadRooms" />
  <addRooms
    v-if="showEditModal && selectedRoom"
    :roomData="selectedRoom"
    @close="closeModal"
    @refresh="loadRooms"
  />
  <uploadRooms
    v-if="isUploadModal"
    @close="isUploadModal = false"
    @refresh="loadRooms"
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
        <b>{{ recordToDelete?.room_name }}</b> ? This action cannot be undone.
      </p>

      <!-- <div class="delete-divider"></div> -->

      <div class="delete-actions">
        <button class="btn-cancel" @click="showDeleteModal = false">
          No, Cancel
        </button>
        <button class="btn-cancel-confirm" @click="confirmDelete">
          Yes, Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import addRooms from "../modals/add-rooms.vue";
import uploadRooms from "../modals/upload-rooms.vue";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TableRooms",
  components: {
    icon,
    addRooms,
    uploadRooms,
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAdd: false,
      isEdit: false,
      isTable: true,
      isUploadData: false,
      showDeleteModal: false,
      recordToDelete: null,
      selectedRoom: null,
      showEditModal: false,
      isUploadModal: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rooms"]),

    filteredData() {
      const query = this.searchQuery.toLowerCase();

      return this.rooms.filter((item) =>
        [
          item.room_name,
          item.room_type,
          item.room_capacity,
          item.institute?.institute_name,
          item.is_active ? "Active" : "Inactive",
        ]
          .join(" ")
          .toLowerCase()
          .includes(query),
      );
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
    async loadRooms() {
      const store = useFetchDataStore();
      await store.fetchRooms();
    },
    toggleUploadData() {
      this.isUploadData = true;
      this.isTable = true;
    },
    toggleAdd() {
      this.isAdd = true;
      this.isTable = true;
    },
    toggleEdit(item) {
      this.selectedRoom = item;
      this.showEditModal = true;
    },
    toggleDelete(item) {
      this.recordToDelete = item;
      this.showDeleteModal = true;
    },
    confirmDelete() {
      if (!this.recordToDelete || isNaN(this.recordToDelete.room_id)) {
        toast.error("Invalid room ID.");
        return;
      }

      const roomId = this.recordToDelete.room_id;

      axios
        .delete(process.env.VUE_APP_API_BASE_URL + `/rooms/delete-id/${roomId}`)
        .then(() => {
          this.recordToDelete = null;
          this.showDeleteModal = false;

          // Play sound after successful delete
          const audio = new Audio(require("@/assets/delete.mp3"));
          audio.play();

          this.loadRooms(); // refresh the list from backend
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
    closeView() {
      this.isAdd = false;
      this.isUploadData = false;
    },
    closeModal() {
      this.showEditModal = false;
      this.selectedRoom = null;
    },
    handleBackToTable() {
      this.isEdit = false;
      this.isAdd = false;
      this.isUploadData = false;
      this.isTable = true;
    },
  },
  mounted() {
    this.loadRooms();
  },
};
</script>
