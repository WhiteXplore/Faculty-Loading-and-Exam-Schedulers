<template>
  <div v-if="isTable">
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
        <div class="flex gap-2">
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

          <div class="flex gap-2">
            <!-- IMPORT DROPDOWN -->
            <div class="relative">
              <div @click="showImportSelector = true" class="btn-download">
                <div class="btn-add-icon">
                  <icon :name="'uploads'" class="w-4 h-4" />
                </div>
                <span class="btn-add-text">Import</span>
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
            <div @click="toggleAdd" class="btn-add">
              <div class="btn-add-icon">
                <icon :name="'add-account1.1'" class="w-4 h-4" />
              </div>
              <span class="btn-add-text">Add Accounts</span>
            </div>
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
                <th class="px-4 py-3 text-left font-normal w-[12%]">Name</th>
                <th class="px-4 py-3 text-left font-normal w-[14%]">Email</th>
                <th class="px-4 py-3 text-left font-normal w-[12%]">
                  Designation
                </th>
                <th class="px-4 py-3 text-left font-normal w-[7%]">
                  Faculty Load Unit
                </th>
                <th class="px-4 py-3 text-left font-normal w-[7%]">
                  Admin Load Unit
                </th>
                <th class="px-4 py-3 text-left font-normal w-[10%]">
                  Institute
                </th>
                <th class="px-4 py-3 text-left font-normal w-[10%]">Program</th>
                <th class="px-4 py-3 text-left font-normal w-[10%]">
                  Position
                </th>
                <th class="px-4 py-3 text-left font-normal w-[8%]">Status</th>

                <th
                  class="px-4 py-3 text-center rounded-tr-lg font-normal w-[10%]"
                >
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
                  {{ user.designation }}
                </td>
                <td class="px-4 py-3 text-left">
                  {{ user.unit_load }}
                </td>
                <td class="px-4 py-3 text-left">
                  {{ user.admin_unit_load || "-" }}
                </td>

                <td class="px-4 py-3 text-left">
                  {{ user.institute?.institute_code }}
                </td>
                <td class="px-4 py-3 text-left">
                  {{ user.program?.program_code }}
                </td>
                <td class="px-4 py-3 text-left">{{ user.role }}</td>
                <td class="px-4 py-3 text-left">
                  <span
                    :class="{
                      'border-emerald-200 bg-emerald-50 text-emerald-700':
                        user.is_active === true || user.is_active === 1,

                      'border-slate-200 bg-slate-100 text-slate-600':
                        user.is_active === false || user.is_active === 0,
                    }"
                    class="inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold shadow-sm"
                  >
                    {{
                      user.is_active === true || user.is_active === 1
                        ? "Active"
                        : "Inactive"
                    }}
                  </span>
                </td>
                <td class="px-4 py-3 items-center justify-center flex relative">
                  <div class="per-page-container">
                    <!-- Always visible -->
                    <button
                      class="btn-see-details"
                      @click="toggleViewExpertise(user)"
                    >
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
                      @click="toggleEdit(user)"
                    >
                      <icon
                        name="edit"
                        class="rounded-lg bg-defaultGreen text-white p-1"
                      />
                      Edit
                    </button>

                    <button
                      class="w-full flex gap-2 items-center text-left px-2 py-2 hover:bg-green-50 rounded-md text-xs"
                      @click="toggleDelete(user)"
                    >
                      <icon
                        name="delete"
                        class="rounded-lg bg-red-800 text-white p-1"
                      />
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="paginatedData.length === 0">
                <td colspan="7" class="text-center py-6 text-gray-400">
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
  <importUsers
    v-if="showImportModal"
    @close="closeImportModal"
    @refresh="loadUsers"
  />
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
  <div v-if="showDeleteModal" class="delete-container">
    <div class="delete-box">
      <div class="delete-icon">
        <icon name="question" class="text-red-600" />
      </div>

      <h1 class="delete-title">Delete Confirmation</h1>

      <p class="delete-text">
        Are you sure you want to delete
        <b>
          {{ recordToDelete?.first_name }} {{ recordToDelete?.last_name }}
        </b>
        ? This action cannot be undone.
      </p>

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

  <!-- Import Selection Modal -->
  <div
    v-if="showImportSelector"
    class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-50"
  >
    <div class="bg-white rounded-2xl shadow-xl w-[450px] animate-slideUp">
      <!-- Title -->
      <div class="modal-header">
        <div class="flex items-center gap-3">
          <!-- Icon -->
          <div class="glass-container">
            <icon name="circle-add2" class="text-white" />
          </div>

          <!-- Title -->
          <div>
            <h2 class="text-lg font-semibold text-white">Choose import</h2>

            <p class="text-xs text-green-100">
              View, add, and update user details
            </p>
          </div>
        </div>

        <icon
          :name="'circle-close3'"
          @click="showImportSelector = false"
          class="close-button-header"
        />
      </div>

      <!-- Cards -->
      <div class="grid grid-cols-2 gap-4 p-4">
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

          <span class="text-sm font-semibold text-gray-700">
            Import Users
          </span>

          <p class="text-xs text-gray-500 text-center mt-1">
            Upload user accounts CSV
          </p>
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

          <span class="text-sm font-semibold text-gray-700">
            Import Expertise
          </span>

          <p class="text-xs text-gray-500 text-center mt-1">
            Upload expertise data CSV
          </p>
        </div>
      </div>

      <!-- Cancel -->
      <div class="p-4 text-center flex justify-end">
        <button @click="showImportSelector = false" class="btn-cancel">
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
        `${user.first_name} ${user.last_name}
     ${user.role}
     ${user.email}
     ${user.is_active ? "Active" : "Inactive"}`
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
      if (!user || !user.id) {
        toast.error("Invalid user selected.");
        return;
      }

      this.selectedUser = { ...user };
      this.showEditModal = true;
      this.openActionMenuId = null;
    },

    toggleDelete(user) {
      if (!user || !user.id) {
        toast.error("Invalid user selected.");
        return;
      }

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
        await axios.delete(
          process.env.VUE_APP_API_BASE_URL + `/auth/remove/${userId}`,
        );
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
