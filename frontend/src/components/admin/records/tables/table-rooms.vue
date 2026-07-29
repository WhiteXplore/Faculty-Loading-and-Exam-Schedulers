<template>
  <div v-if="isTable" class=" ">
    <!-- <div class="flex justify-between items-center px-1 text-sm">
  
      <div class="text-[13px] text-text font-regular">
        Pages / Rooms Availability
      </div>

    </div> -->

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
        <div class="flex gap-2">
          <!-- button for filters  -->
          <button
            @click="showFilters = !showFilters"
            class="flex items-center gap-2 rounded-xl border border-gray-200 bg-white px-3 py-2 shadow-sm transition hover:border-defaultGreen hover:bg-green-50"
          >
            <icon name="academic-cap" />
            <span class="text-sm font-medium">Filter</span>
          </button>
          <div
            class="relative w-56"
            ref="instituteDropdownRef"
            v-if="showFilters"
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
                    d="M3 21h18M5 21V7l7-4 7 4v14"
                  />
                </svg>
              </div>

              <!-- Selected -->
              <button
                type="button"
                @click="showInstituteDropdown = !showInstituteDropdown"
                class="w-full rounded-xl py-3 pl-10 pr-10 text-left text-sm font-semibold text-gray-700"
              >
                <span v-if="selectedInstitute !== 'all'">
                  {{
                    availableInstitutes.find(
                      (i) =>
                        Number(i.institute_id) === Number(selectedInstitute),
                    )?.institute_code
                  }}
                </span>

                <span v-else class="text-gray-600 font-light">
                  Select All Institutes
                </span>
              </button>

              <button
                type="button"
                @click="showInstituteDropdown = !showInstituteDropdown"
                class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 hover:text-defaultGreen"
              >
                <svg
                  class="h-4 w-4 transition-transform duration-200"
                  :class="{ 'rotate-180': showInstituteDropdown }"
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

            <div
              v-if="showInstituteDropdown"
              class="absolute z-[9999] mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
            >
              <div class="border-b border-gray-100 px-4 py-3">
                <p
                  class="text-xs font-semibold uppercase tracking-wide text-gray-400"
                >
                  Institutes
                </p>
              </div>

              <div class="max-h-[260px] overflow-y-auto p-1.5">
                <button
                  @click="selectInstitute('all')"
                  class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                  :class="selectedInstitute === 'all' ? 'bg-green-50' : ''"
                >
                  <p class="text-sm text-gray-800">All Institutes</p>
                </button>

                <button
                  v-for="institute in availableInstitutes"
                  :key="institute.institute_id"
                  @click="selectInstitute(institute.institute_id)"
                  class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                  :class="
                    Number(selectedInstitute) === Number(institute.institute_id)
                      ? 'bg-green-50'
                      : ''
                  "
                >
                  <p class="text-sm text-gray-800">
                    {{ institute.institute_code }}
                  </p>

                  <svg
                    v-if="
                      Number(selectedInstitute) ===
                      Number(institute.institute_id)
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
          <div
            v-if="showFilters"
            class="relative w-56"
            ref="roomTypeDropdownRef"
          >
            <div
              class="relative flex items-center rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 focus-within:border-defaultGreen focus-within:ring-4 focus-within:ring-green-100"
            >
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
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              </div>

              <button
                type="button"
                @click="showRoomTypeDropdown = !showRoomTypeDropdown"
                class="w-full rounded-xl py-3 pl-10 pr-10 text-left text-sm font-semibold text-gray-700"
              >
                <span v-if="selectedRoomType !== 'all'">
                  {{ selectedRoomType }}
                </span>

                <span v-else class="text-gray-600 font-light">
                  Select Room Type
                </span>
              </button>

              <button
                type="button"
                @click="showRoomTypeDropdown = !showRoomTypeDropdown"
                class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 hover:text-defaultGreen"
              >
                <svg
                  class="h-4 w-4 transition-transform duration-200"
                  :class="{ 'rotate-180': showRoomTypeDropdown }"
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

            <div
              v-if="showRoomTypeDropdown"
              class="absolute z-[9999] mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
            >
              <div class="border-b border-gray-100 px-4 py-3">
                <p class="text-xs uppercase tracking-wide text-gray-400">
                  Room Types
                </p>
              </div>

              <div class="max-h-[260px] overflow-y-auto p-1.5">
                <button
                  @click="selectRoomType('all')"
                  class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                  :class="selectedRoomType === 'all' ? 'bg-green-50' : ''"
                >
                  <p class="text-sm text-gray-800">All Room Types</p>
                </button>

                <button
                  v-for="type in availableRoomTypes"
                  :key="type"
                  @click="selectRoomType(type)"
                  class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                  :class="selectedRoomType === type ? 'bg-green-50' : ''"
                >
                  <p class="text-sm text-gray-800">
                    {{ type }}
                  </p>

                  <svg
                    v-if="selectedRoomType === type"
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
          <!-- RIGHT (Buttons) -->
          <div class="flex gap-2">
            <!-- Upload Room -->
            <div @click="isUploadModal = true" class="btn-download">
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
      showFilters: false,
      showRoomTypeDropdown: false,
      selectedRoomType: "all",
      showInstituteDropdown: false,
      selectedInstitute: "all",
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rooms", "institutes"]),
    availableInstitutes() {
      return [
        ...new Map(
          this.rooms
            .filter((room) => room.institute)
            .map((room) => [room.institute.institute_id, room.institute]),
        ).values(),
      ].sort((a, b) => a.institute_name.localeCompare(b.institute_name));
    },
    availableRoomTypes() {
      return [
        ...new Set(
          this.rooms
            .map((room) => room.room_type)
            .filter((type) => type && type.trim() !== ""),
        ),
      ].sort();
    },

    filteredData() {
      const query = this.searchQuery.toLowerCase();

      return this.rooms.filter((item) => {
        const matchesSearch = [
          item.room_name,
          item.room_type,
          item.room_capacity,
          item.institute?.institute_name,
          item.building?.building_name,
          item.is_active ? "Active" : "Inactive",
        ]
          .join(" ")
          .toLowerCase()
          .includes(query);

        const matchesInstitute =
          this.selectedInstitute === "all" ||
          Number(item.institute?.institute_id) ===
            Number(this.selectedInstitute);

        const matchesRoomType =
          this.selectedRoomType === "all" ||
          item.room_type === this.selectedRoomType;

        return matchesSearch && matchesInstitute && matchesRoomType;
      });
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredData.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;
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
    selectInstitute(id) {
      this.selectedInstitute = id;
      this.showInstituteDropdown = false;
      this.changePage(1);
    },
    selectRoomType(type) {
      this.selectedRoomType = type;
      this.showRoomTypeDropdown = false;
      this.changePage(1);
    },
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
