<template>
  <div v-if="isTable">
    <!-- Header -->
    <!-- Header -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4 font-regular">Pages / User Accounts</div>

      <div class="flex gap-2">
        <!-- IMPORT DROPDOWN -->
        <div class="relative">
          <div
            @click="showImportSelector = true"
            class="flex items-center gap-2 px-3 py-2 border bg-blue-700 text-white border-blue-700 rounded-xl hover:bg-white hover:text-blue-700 hover:shadow-lg cursor-pointer transition duration-200"
          >
            <div
              class="p-1 bg-blue-500 bg-opacity-20 rounded-full flex items-center justify-center"
            >
              <icon :name="'uploads'" class="w-4 h-4" />
            </div>
            <span class="font-medium text-sm">Import</span>
          </div>

          <!-- DROPDOWN MENU -->
          <div
            v-if="showImportMenu"
            class="absolute right-0 mt-2 w-48 bg-white border rounded-xl shadow-lg overflow-hidden z-50"
          >
            <div
              @click="openImportUsers"
              class="px-4 py-2 hover:bg-blue-50 cursor-pointer text-sm flex items-center gap-2"
            >
              <icon name="uploads" class="w-4 h-4 text-blue-600" />
              Import Users
            </div>

            <div
              @click="openImportExpertise"
              class="px-4 py-2 hover:bg-purple-50 cursor-pointer text-sm flex items-center gap-2"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="w-4 h-4 text-purple-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                />
              </svg>
              Import Expertise
            </div>
          </div>
        </div>

        <!-- ADD ACCOUNT -->
        <div
          @click="toggleAdd"
          class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
        >
          <div
            class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
          >
            <icon :name="'add-account1.1'" class="w-4 h-4" />
          </div>
          <span class="font-medium text-sm">Add Accounts</span>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="table-container">
      <!-- Top controls -->
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

        <!-- Search -->
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search..."
            class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-[250px] transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
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

      <!-- Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <table class="min-w-full text-sm text-gray-700 border-collapse">
          <thead class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide">
            <tr>
              <th class="px-4 py-3 text-left font-normal w-[15%]">Name</th>
              <th class="px-4 py-3 text-left font-normal w-[25%]">Email</th>
              <th class="px-4 py-3 text-left font-normal">Institute</th>
              <th class="px-4 py-3 text-left font-normal">Program</th>
              <th class="px-4 py-3 text-left font-normal">Position</th>

              <th class="px-4 py-3 text-center rounded-tr-lg font-normal w-[10%]">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="user in paginatedData"
              :key="user.id"
              class="hover:bg-green-50 transition-all border-t"
            >
              <td class="px-4 py-3 text-left">
                {{ user.first_name }} {{ user.last_name }}
              </td>
              <td class="px-4 py-3 text-left">{{ user.email }}</td>
              <td class="px-4 py-3 text-left">
                {{ user.institute?.institute_code }}
              </td>
              <td class="px-4 py-3 text-left">
                {{ user.program?.program_code }}
              </td>
              <td class="px-4 py-3 text-left">{{ user.role }}</td>

              <td class="px-4 py-3 items-center justify-center flex relative">
           <div class="per-page-container">
                  <!-- Always visible -->
                  <button class="btn-view" @click="toggleViewExpertise(user)">
                    See Details
                  </button>

                  <!-- 3 dots button -->
                  <button
                    class="w-5.5 h-8 rounded-md border border-gray-300 flex items-center justify-center hover:bg-gray-100"
                    @click.stop="toggleActionMenu(user.id)"
                  >
                    <icon name="3dots" class="rotate-90" />
                  </button>
                </div>

                <!-- Dropdown actions -->
                <div
                  v-if="openActionMenuId === user.id"
                  @mouseleave="openActionMenuId = false"
                  class="absolute right-0 top-12 z-50 w-40 bg-white border rounded-lg shadow-lg p-2 space-y-0.5"
                >
                  <button
                    class="w-full flex gap-2 items-center text-left px-2 py-2 hover:bg-green-50 rounded-md text-xs"
                    @click="toggleEdit('edit', user)"
                  >
                    <icon name="edit" class="rounded-lg bg-defaultGreen text-white p-1" />
                    Edit
                  </button>

                  <button
                    class="w-full flex gap-2 items-center text-left px-2 py-2 hover:bg-green-50 rounded-md text-xs"
                    @click="toggleDelete('delete', user)"
                  >
                    <icon name="delete" class="rounded-lg bg-red-800 text-white p-1" />
                    Delete
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="paginatedData.length === 0">
              <td colspan="7" class="text-center py-6 text-gray-400">No records found</td>
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

  <!-- Modals -->
  <addUsers v-if="isAdd" @close="closeView" @refresh="loadUsers" />
  <addUsers
    v-if="showEditModal && selectedUser"
    :userData="selectedUser"
    @close="closeModal"
    @refresh="loadUsers"
  />
  <importUsers v-if="showImportModal" @close="closeImportModal" @refresh="loadUsers" />
  <importExpertise
    v-if="showImportExpertiseModal"
    @close="closeImportExpertiseModal"
    @refresh="loadUsers"
  />
  <viewUserExpertise
    v-if="showViewExpertiseModal && selectedUserExpertise"
    :userData="selectedUserExpertise"
    @close="closeViewExpertiseModal"
  />

  <!-- Delete Confirmation Modal -->
  <div
    v-if="showDeleteModal"
    <div class="modal-overlay">
  ></div>
  <div
    v-if="showDeleteModal"
    class="rounded-xl shadow-lg w-[300px] md:w-[400px] bg-white py-6 px-4 flex flex-col items-center fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 animate-slideUp"
  >
    <div
      class="rounded-full w-16 h-16 md:w-20 md:h-20 flex justify-center items-center bg-red-300 animate-pulse"
    >
      <icon
        name="question"
        class="w-8 h-8 md:w-10 md:h-10 text-white flex justify-center items-center"
      />
    </div>

    <h1 class="text-[14px] md:text-[16px] font-semibold mt-4">Delete Confirmation</h1>
    <p class="mt-2 text-[12px] md:text-[13px] text-center px-8">
      Are you sure you want to delete this record? This action cannot be undone.
    </p>

    <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

    <div class="tracking-wide flex gap-2 mt-4">
      <button
        class="bg-red-400 p-2 px-3 text-[11px] md:text-[13px] rounded-md text-white hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md"
        @click="showDeleteModal = false"
      >
        No, Cancel
      </button>
      <button
        class="bg-green-400 p-2 px-3 text-[11px] md:text-[13px] rounded-md text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
        @click="confirmDelete"
      >
        Yes, Delete
      </button>
    </div>
  </div>
  <!-- Import Selection Modal -->
  <div
    v-if="showImportSelector"
    class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50"
  >
    <div class="bg-white rounded-2xl shadow-xl w-[450px] p-0.5 animate-slideUp">
      <!-- Title -->
      <div
        class="w-full p-5 py-3 bg-defaultGreen text-white rounded-t-[14px] flex justify-between items-center border-b shadow"
      >
        <div class="flex gap-1 items-center">
          <icon :name="'add-students'" />
          <h1 class="font-bold tracking-wide text-lg">Choose Import</h1>
        </div>
        <icon
          :name="'circle-close3'"
          @click="showImportSelector = false"
          class="cursor-pointer"
        />
      </div>

      <!-- Cards -->
      <div class="grid grid-cols-2 gap-4 p-2">
        <!-- Import Users -->
        <div
          @click="openImportUsers"
          class="border rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:bg-blue-50 hover:border-blue-500 transition"
        >
          <div class="bg-blue-100 p-3 rounded-full mb-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-6 h-6 text-blue-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          </div>

          <span class="text-sm font-semibold text-gray-700"> Import Users </span>

          <p class="text-xs text-gray-500 text-center mt-1">Upload user accounts CSV</p>
        </div>

        <!-- Import Expertise -->
        <div
          @click="openImportExpertise"
          class="border rounded-xl p-4 flex flex-col items-center justify-center cursor-pointer hover:bg-purple-50 hover:border-purple-500 transition"
        >
          <div class="bg-purple-100 p-3 rounded-full mb-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-6 h-6 text-purple-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
              />
            </svg>
          </div>

          <span class="text-sm font-semibold text-gray-700"> Import Expertise </span>

          <p class="text-xs text-gray-500 text-center mt-1">Upload expertise data CSV</p>
        </div>
      </div>

      <!-- Cancel -->
      <div class="p-1.5 text-center flex justify-end">
        <button
          @click="showImportSelector = false"
          class="text-sm px-4 py-2 border rounded-lg hover:bg-gray-100"
        >
          Cancel
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import addUsers from "../modals/add-users.vue";
import importUsers from "../modals/import-users.vue";
import importExpertise from "../modals/import-expertise.vue";
import viewUserExpertise from "../modals/view-user-expertise.vue";

import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";

export default {
  name: "TableUsers",
  components: {
    icon,
    addUsers,
    importUsers,
    importExpertise,
    viewUserExpertise,
  },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isAdd: false,
      isTable: true,

      showImportSelector: false,
      showImportMenu: false,
      showImportModal: false,
      showImportExpertiseModal: false,

      showDeleteModal: false,
      showViewExpertiseModal: false,
      showEditModal: false,

      openActionMenuId: null,

      recordToDelete: null,
      selectedUser: null,
      selectedUserExpertise: null,
      isDeleting: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["users", "programs"]),
    filteredData() {
      const query = this.searchQuery.toLowerCase();
      return this.users.filter((user) =>
        `${user.first_name} ${user.last_name} ${user.role} ${user.email}`
          .toLowerCase()
          .includes(query)
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
    toggleActionMenu(userId) {
      this.openActionMenuId = this.openActionMenuId === userId ? null : userId;
    },

    openImportUsers() {
      this.showImportSelector = false;
      this.showImportModal = true;
    },

    openImportExpertise() {
      this.showImportSelector = false;
      this.showImportExpertiseModal = true;
    },

    toggleImportMenu() {
      this.showImportMenu = !this.showImportMenu;
    },

    async loadUsers() {
      const store = useFetchDataStore();
      await store.fetchUsers();
      await store.fetchPrograms();
    },

    toggleAdd() {
      this.isAdd = true;
      this.isTable = true;
    },

    toggleImport() {
      this.showImportModal = true;
    },

    toggleImportExpertise() {
      this.showImportExpertiseModal = true;
    },

    toggleViewExpertise(user) {
      this.selectedUserExpertise = user;
      this.showViewExpertiseModal = true;
      this.openActionMenuId = null;
    },

    toggleEdit(user) {
      this.selectedUser = user;
      this.showEditModal = true;
      this.openActionMenuId = null;
    },

    toggleDelete(user) {
      this.recordToDelete = user;
      this.showDeleteModal = true;
      this.openActionMenuId = null;
    },

    async confirmDelete() {
      if (!this.recordToDelete || isNaN(this.recordToDelete.id)) {
        toast.error("Invalid user ID.");
        return;
      }

      const userId = this.recordToDelete.id;
      this.isDeleting = true;

      try {
        await axios.delete(process.env.VUE_APP_API_BASE_URL + `/auth/remove/${userId}`);
        this.recordToDelete = null;
        this.showDeleteModal = false;

        const audio = new Audio(require("@/assets/delete.mp3"));
        audio.play();

        const store = useFetchDataStore();
        await store.fetchUsers();

        toast.success("Record deleted successfully");
      } catch (error) {
        console.error("Delete failed:", error);
        toast.error("Failed to delete record.");
      } finally {
        this.isDeleting = false;
      }
    },

    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },

    closeView() {
      this.isAdd = false;
    },

    closeModal() {
      this.showEditModal = false;
      this.selectedUser = null;
    },

    closeImportModal() {
      this.showImportModal = false;
    },

    closeImportExpertiseModal() {
      this.showImportExpertiseModal = false;
    },

    closeViewExpertiseModal() {
      this.showViewExpertiseModal = false;
      this.selectedUserExpertise = null;
    },
  },
  mounted() {
    this.loadUsers();
  },
};
</script>
