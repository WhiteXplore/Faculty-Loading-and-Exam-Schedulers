<template>
  <div v-if="isTable">
    <!-- Header -->
    <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages /
        <span class="font-semibold text-green-900">
          {{
            user && user.role === "Program Chairperson"
              ? "Faculty Under My Program"
              : "Faculty List"
          }}
        </span>
      </div>
    </div>

    <!-- Table Container -->
    <div class="table-container">
      <div class="table-controls">
        <!-- Items per page -->
        <div class="per-page-container">
          <div class="select-wrapper">
            <select v-model="itemsPerPage" class="select-input" @change="changePage(1)">
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
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

        <!-- Search -->
        <div class="search-wrapper">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search faculty..."
            class="search-input"
            @input="changePage(1)"
          />
          <div
            class="absolute inset-y-0 left-3 flex items-center text-defaultGreen pointer-events-none"
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

      <!-- Faculty Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[69vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide">
              <tr>
                <th class="px-4 py-3 text-left font-normal w-[15%]">Faculty Name</th>
                <!-- <th class="px-4 py-3 text-center font-normal w-[5%]">
                  Institute
                </th>
                <th class="px-4 py-3 text-left font-normal w-[30%]">Program</th> -->
                <th class="px-4 py-3 text-center font-normal w-[15%]">Designation</th>
                <th class="px-4 py-3 text-center font-normal w-[15%]">
                  Employment Status
                </th>

                <th class="px-4 py-3 text-center font-normal w-[20%]">Preferred Time</th>
                <th class="px-4 py-3 text-center font-normal w-[16%]">Inter-branch</th>
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
                <td class="px-4 py-3">{{ user.first_name }} {{ user.last_name }}</td>
                <!-- <td class="px-4 py-3 text-center">
                  {{ user.institute?.institute_code || "-" }}
                </td>
                <td class="px-4 py-3">
                  {{ user.program?.program_code || "-" }}
                </td> -->
                <td class="px-4 py-3 text-center">
                  {{ user.designation || "-" }}
                </td>
                <td class="px-4 py-3 text-center">
                  <span
                    :class="{
                      'border border-green-600 text-green-800':
                        user.employment_type === 'Full Time',
                      ' border border-orange-600 text-orange-800':
                        user.employment_type === 'Part Time',
                      'text-gray-400 ': !user.employment_type,
                    }"
                    class="border border-green-600 text-green-800 text-xs px-2 py-1 rounded-full"
                  >
                    {{ user.employment_type || "-" }}
                  </span>
                </td>

                <td class="px-4 py-3 text-center">
                  {{ user.preffered_time || "-" }}
                </td>

                <td class="px-4 py-3 text-center">
                  <div
                    v-if="facultyBranchesByUser[user.id]?.length"
                    class="flex flex-wrap gap-1 justify-center"
                  >
                    <span
                      v-for="(branchName, idx) in facultyBranchesByUser[user.id]"
                      :key="idx"
                      class="border border-green-600 text-green-800 text-xs px-2 py-1 rounded-full"
                    >
                      {{ branchName }}
                    </span>
                  </div>
                  <span v-else class="text-gray-400">-</span>
                </td>

                <td class="px-4 py-3 items-center justify-center flex relative">
                  <div class="per-page-container">
                    <!-- Always visible -->
                    <button class="btn-view" @click="toggleView(user)">
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
                      @click="handleAction('update', user)"
                    >
                      <icon
                        name="edit"
                        class="rounded-lg bg-defaultGreen text-white p-1"
                      />
                      Update
                    </button>

                    <button
                      class="w-full flex gap-2 items-center text-left px-2 py-2 hover:bg-green-50 rounded-md text-xs"
                      @click="handleAction('assign', user)"
                    >
                      <icon
                        name="edit"
                        class="rounded-lg bg-defaultGreen text-white p-1"
                      />
                      Assign
                    </button>

                    <button
                      class="w-full flex gap-2 items-center text-left px-2 py-2 hover:bg-green-50 rounded-md text-xs"
                      @click="handleAction('cross', user)"
                    >
                      <icon
                        name="edit"
                        class="rounded-lg bg-defaultGreen text-white p-1"
                      />
                      Cross Assign
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="paginatedData.length === 0">
                <td colspan="6" class="text-center py-8 text-gray-400">
                  No faculty found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-gray-700 text-sm">
          Showing {{ startIndex }} to {{ endIndex }} of {{ filteredData.length }} faculty
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

  <!-- Add Modal -->
  <div
    v-if="showAddModal"
    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
  >
    <div class="rounded-[16px] shadow-lg animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-[30vw] bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
      >
        <!-- Header -->
        <div
          class="w-full px-4 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center"
        >
          <h1 class="font-bold tracking-wide text-lg">Update Faculty</h1>

          <button type="button" @click="showAddModal = false" class="text-white text-lg">
            ✕
          </button>
        </div>

        <!-- Body -->
        <div class="px-4 py-3 space-y-4 text-sm">
          <!-- Faculty Info -->
          <div class="bg-gray-50 rounded-lg space-y-1.5">
            <p>
              <span class="font-semibold">Faculty:</span>
              {{ selectedFaculty?.first_name }} {{ selectedFaculty?.last_name }}
            </p>

            <p>
              <span class="font-semibold">Institute:</span>
              {{ selectedFaculty?.institute?.institute_name || "N/A" }}
            </p>

            <p>
              <span class="font-semibold">Program:</span>
              {{ selectedFaculty?.program?.program_name || "N/A" }}
            </p>
          </div>

          <!-- Update Mode Selection -->
          <div class="space-y-2 text-[13px] text-gray-600y">
            <label class="font-normal block mb-1">Select Update Type</label>

            <select
              v-model="updateMode"
              class="w-full border px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-600 cursor-pointer font-normal"
            >
              <option disabled value="">-- Select Option --</option>
              <option value="preffered_time">Preferred Time</option>
              <option value="interbranch">Inter-branch</option>
              <option value="all">All (Preferred Time + Inter-branch)</option>
            </select>
          </div>

          <!-- ===================== -->
          <!-- PREFFERED TIME SECTION -->
          <!-- ===================== -->
          <div
            v-if="updateMode === 'preffered_time' || updateMode === 'all'"
            class="space-y-3"
          >
            <!-- Selected Slot Display -->
            <div
              v-if="formattedSlot"
              class="bg-green-50 p-3 rounded-lg border border-green-200 space-y-2"
            >
              <p class="font-semibold">Selected Time Slot:</p>
              <p>{{ formattedSlot }}</p>
              <p>Total Hours: {{ totalHours }} hrs</p>
            </div>

            <!-- MORNING -->
            <div class="rounded-lg space-y-3">
              <h3 class="font-normal text-green-800 text-sm">Morning Schedule</h3>

              <div class="flex gap-4">
                <div class="flex-1">
                  <label class="font-normal block mb-1">Start</label>
                  <input
                    type="time"
                    v-model="form.morningStart"
                    class="w-full border px-3 py-2 rounded-md"
                  />
                </div>

                <div class="flex-1">
                  <label class="font-normal block mb-1">End</label>
                  <input
                    type="time"
                    v-model="form.morningEnd"
                    class="w-full border px-3 py-2 rounded-md"
                  />
                </div>
              </div>
            </div>

            <!-- AFTERNOON -->
            <div class="rounded-lg space-y-3">
              <h3 class="font-nromal text-green-800 text-sm">Afternoon Schedule</h3>

              <div class="flex gap-4">
                <div class="flex-1">
                  <label class="font-normal block mb-1">Start</label>
                  <input
                    type="time"
                    v-model="form.afternoonStart"
                    class="w-full border px-3 py-2 rounded-md"
                  />
                </div>

                <div class="flex-1">
                  <label class="font-normal block mb-1">End</label>
                  <input
                    type="time"
                    v-model="form.afternoonEnd"
                    class="w-full border px-3 py-2 rounded-md"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- ===================== -->
          <!-- INTERBRANCH SECTION -->
          <!-- ===================== -->
          <div
            v-if="updateMode === 'interbranch' || updateMode === 'all'"
            class="space-y-3 text-[13px]"
          >
            <label class="font-normal block mb-1">Select Inter-branch Campus</label>

            <!-- Dropdown Trigger -->
            <div class="relative">
              <button
                type="button"
                @click="showBranchDropdown = !showBranchDropdown"
                class="w-full border px-3 py-2 rounded-md bg-white text-left flex justify-between items-center font-normal"
              >
                <span v-if="form.interbranchCampus.length">
                  {{ form.interbranchCampus.length }} campus(es) selected
                </span>
                <span v-else class="text-gray-400">Select campuses</span>
                <span>▾</span>
              </button>

              <!-- Dropdown List -->
              <div
                v-if="showBranchDropdown"
                @mouseleave="showBranchDropdown = false"
                class="absolute z-50 mt-1 w-full bg-white border rounded-md shadow-lg max-h-60 overflow-y-auto"
              >
                <label
                  v-for="branch in college_branch"
                  :key="branch.college_branch_id"
                  class="flex items-center gap-2 px-3 py-2 hover:bg-gray-100 cursor-pointer"
                >
                  <input
                    type="checkbox"
                    :value="branch.college_branch_id"
                    :checked="form.interbranchCampus.includes(branch.college_branch_id)"
                    @change="toggleBranch(branch.college_branch_id)"
                  />
                  {{ branch.college_branch_name }}
                </label>
              </div>
            </div>

            <p class="text-gray-500">You can select multiple campuses.</p>

            <!-- Selected Tags -->
            <div v-if="form.interbranchCampus.length" class="flex flex-wrap gap-2 mt-2">
              <div
                v-for="id in form.interbranchCampus"
                :key="id"
                class="flex items-center gap-2 bg-defaultGreen text-white px-3 py-1 rounded-md text-[13px] font-normal"
              >
                {{
                  college_branch.find((b) => b.college_branch_id === id)
                    ?.college_branch_name
                }}

                <button
                  type="button"
                  @click="removeBranch(id)"
                  class="text-white hover:text-red-600"
                >
                  <icon name="delete" />
                </button>
              </div>
            </div>
          </div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2 pt-3">
            <button type="button" @click="showAddModal = false" class="btn-cancel">
              Cancel
            </button>

            <button type="submit" class="btn-save">Save Changes</button>
          </div>
        </div>
      </form>
    </div>
  </div>

  <!-- View Modal -->
  <div
    v-if="showViewModal"
    class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50"
  >
    <div
      class="bg-white w-full max-w-2xl rounded-2xl shadow-2xl p-6 relative animate-slideUp"
    >
      <!-- Header -->
      <div class="flex justify-between items-center border-b pb-3 mb-4">
        <h2 class="text-xl font-semibold text-gray-900 flex items-center gap-2">
          <svg
            class="w-6 h-6 text-defaultGreen"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 11c0 1.657-1.343 3-3 3S6 12.657 6 11s1.343-3 3-3 3 1.343 3 3zm0 0v10m0-10c0 1.657 1.343 3 3 3s3-1.343 3-3-1.343-3-3-3-3 1.343-3 3z"
            />
          </svg>
          Faculty Informations
        </h2>
        <button
          @click="showViewModal = false"
          class="text-gray-400 hover:text-gray-600 transition"
        >
          ✕
        </button>
      </div>

      <!-- Content -->
      <div class="space-y-6" v-if="selectedFaculty">
        <!-- Basic Info -->
        <div class="grid gap-2 text-sm">
          <p class="flex space-x-4">
            <span class="font-semibold text-gray-700">Name:</span>
            <span class="text-gray-900">
              {{ selectedFaculty.first_name }} {{ selectedFaculty.last_name }}
            </span>
          </p>
          <p class="flex space-x-4">
            <span class="font-semibold text-gray-700">Institute:</span>
            <span class="text-gray-900">
              {{ selectedFaculty.institute?.institute_name || "N/A" }}
            </span>
          </p>
          <p class="flex space-x-4">
            <span class="font-semibold text-gray-700">Program:</span>
            <span class="text-gray-900">
              {{ selectedFaculty.program?.program_name || "N/A" }}
            </span>
          </p>
        </div>

        <!-- Expertise & Other Expertise -->
        <div class="flex justify-between gap-6 border-t py-3 text-sm">
          <!-- Expertise -->
          <div class="flex-1">
            <h3 class="font-semibold text-gray-800 mb-2">Expertise</h3>

            <div v-if="filteredExpertise.primary.length" class="space-y-3">
              <div
                v-for="(group, key) in groupByYearSemester(filteredExpertise.primary)"
                :key="key"
              >
                <div class="mb-2">
                  <span class="text-green-800 text-xs font-semibold">
                    {{ key }}
                  </span>
                </div>

                <ul class="list-disc list-inside ml-2 text-gray-700 space-y-1">
                  <li v-for="(exp, i) in group" :key="i">
                    {{ exp.course?.course_code }} -
                    {{ exp.course?.course_title }}
                  </li>
                </ul>
              </div>
            </div>

            <p v-else class="text-gray-500 italic">No expertise added</p>
          </div>

          <!-- Other Expertise -->
          <div class="flex-1">
            <h3 class="font-semibold text-gray-800 mb-2">Other Expertise</h3>

            <div v-if="filteredExpertise.other.length" class="space-y-3">
              <div
                v-for="(group, key) in groupByYearSemester(filteredExpertise.other)"
                :key="key"
              >
                <div class="mb-2">
                  <span class="text-orange-700 text-xs font-semibold">
                    {{ key }}
                  </span>
                </div>

                <ul class="list-disc list-inside ml-2 text-gray-700 space-y-1">
                  <li v-for="(exp, i) in group" :key="i">
                    <span class="text-defaultGreen font-extrabold">
                      {{ getProgramCode(exp.course?.program_id) }}
                    </span>
                    -
                    {{ exp.course?.course_code }} -
                    {{ exp.course?.course_title }}
                  </li>
                  s
                </ul>
              </div>
            </div>

            <p v-else class="text-gray-500 italic">None other expertise added</p>
          </div>

          <div class="flex-1">
            <h3 class="font-semibold text-gray-800 mb-2">Cross Expertise</h3>

            <div v-if="filteredExpertise.cross.length" class="space-y-3">
              <div
                v-for="(group, key) in groupByYearSemester(filteredExpertise.cross)"
                :key="key"
              >
                <div class="mb-2">
                  <span class="text-blue-700 text-xs font-semibold">
                    {{ key }}
                  </span>
                </div>

                <ul class="list-disc list-inside ml-2 text-gray-700 space-y-1">
                  <li v-for="(exp, i) in group" :key="i">
                    <span class="text-defaultGreen font-extrabold">
                      {{ getProgramCode(exp.course?.program_id) }}
                    </span>
                    {{ exp.course?.course_code }} -
                    {{ exp.course?.course_title }}
                  </li>
                </ul>
              </div>
            </div>

            <p v-else class="text-gray-500 italic">No cross expertise assigned</p>
          </div>
        </div>

        <!-- Preferred Time -->
        <div class="pt-3 border-t text-sm">
          <h3 class="font-semibold text-gray-800 mb-2">Preferred Time</h3>
          <p class="text-gray-700" v-if="selectedFaculty.preffered_time">
            {{ selectedFaculty.preffered_time }}
          </p>
          <p class="text-gray-500 italic" v-else>No preferred time set</p>
        </div>

        <!-- Inter-branch Campuses -->
        <div class="pt-3 border-t text-sm">
          <h3 class="font-semibold text-gray-800 mb-2">Inter-branch Campuses</h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="(branchName, i) in selectedFaculty.faculty_branches || []"
              :key="i"
              class="bg-defaultGreen text-white text-xs px-2 py-1 rounded-full"
            >
              {{ branchName }}
            </span>
            <span
              v-if="
                !selectedFaculty.faculty_branches ||
                selectedFaculty.faculty_branches.length === 0
              "
              class="text-gray-500 italic"
            >
              No inter-branch campuses
            </span>
          </div>
        </div>
      </div>

      <!-- Close Button -->
      <div class="flex justify-end mt-6">
        <button type="button" @click="showViewModal = false" class="btn-cancel">
          Close
        </button>
      </div>
    </div>
  </div>

  <addExpertise
    v-if="showExpertiseModal"
    :userData="selectedFaculty"
    :mode="modalMode"
    @close="showExpertiseModal = false"
    @updated="loadUsers"
  />
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";
import addExpertise from "../modals/add-expertise.vue";

export default {
  name: "TableFaculty",
  components: { icon, addExpertise },
  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isTable: true,
      selectedFaculty: null,
      showViewModal: false,
      showAddModal: false,
      user: null,
      openActionMenuId: null,
      modalMode: "",

      form: {
        morningStart: "",
        morningEnd: "",
        afternoonStart: "",
        afternoonEnd: "",
        interbranchCampus: [],
      },

      selectedOption: "",
      updateMode: "",
      showBranchDropdown: false,
      showExpertiseModal: false,
      selectedFacultyForExpertise: null,
      showCrossAssignModal: false,
      selectedFacultyForCross: null,
      facultyBranches: [],
    };
  },

  computed: {
    ...mapState(useFetchDataStore, [
      "rawusers",
      "college_branch",
      "faculty_branch",
      "programs",
    ]),

    filteredExpertise() {
      const list = this.selectedFaculty?.expertise || [];

      return {
        primary: list.filter((e) => e.status === "PRIMARY"),
        other: list.filter((e) => e.status === "OTHER"),
        cross: list.filter((e) => e.status === "CROSS"),
      };
    },
    filteredSlots() {
      if (this.form.period === "morning") {
        return this.morningSlots;
      }
      if (this.form.period === "afternoon") {
        return this.afternoonSlots;
      }
      return [];
    },
    facultyBranchesByUser() {
      const map = {};
      (this.faculty_branch || []).forEach((fb) => {
        const uid = fb.user.id;
        if (!map[uid]) map[uid] = [];
        map[uid].push(fb.collegeBranch.college_branch_name);
      });
      return map;
    },

    totalHours() {
      let total = 0;

      const calc = (start, end) => {
        if (!start || !end) return 0;

        const s = new Date(`1970-01-01T${start}`);
        const e = new Date(`1970-01-01T${end}`);

        return isNaN(s) || isNaN(e) ? 0 : (e - s) / (1000 * 60 * 60);
      };

      total += calc(this.form.morningStart, this.form.morningEnd);
      total += calc(this.form.afternoonStart, this.form.afternoonEnd);

      return total;
    },
    formattedSlot() {
      let parts = [];

      if (this.form.morningStart && this.form.morningEnd) {
        parts.push(
          `${this.formatTo12(this.form.morningStart)} - ${this.formatTo12(
            this.form.morningEnd
          )}`
        );
      }

      if (this.form.afternoonStart && this.form.afternoonEnd) {
        parts.push(
          `${this.formatTo12(this.form.afternoonStart)} - ${this.formatTo12(
            this.form.afternoonEnd
          )}`
        );
      }

      return parts.join(" , ");
    },
    filteredData() {
      const query = this.searchQuery.toLowerCase();
      const currentUser = this.user;

      if (!this.rawusers || !currentUser) return [];

      let list = [];

      // Admin → All faculty and PC
      if (currentUser.role === "Admin") {
        list = this.rawusers.filter(
          (u) => u.role === "Program Chairperson" || u.role === "Faculty"
        );
      }
      // Program Chairperson → Faculty only in same institute + program
      else if (currentUser.role === "Program Chairperson") {
        list = this.rawusers.filter(
          (u) =>
            u.role === "Faculty" &&
            u.institute?.institute_id === currentUser.institute_id &&
            u.program?.program_id === currentUser.program_id
        );
      }

      // Search filter
      return list.filter((u) =>
        [
          `${u.first_name} ${u.last_name}`,
          u.institute?.institute_name || "",
          u.program?.program_name || "",
          u.role || "",
        ]
          .join(" ")
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

    handleAction(action, user) {
      this.openActionMenuId = null;

      if (action === "update") {
        this.openAddModal(user);
      } else if (action === "assign") {
        this.openAssignModal(user);
      } else if (action === "cross") {
        this.openCrossAssignModal(user);
      }
    },
    getProgramCode(programId) {
      const program = (this.programs || []).find((p) => p.program_id === programId);
      return program?.program_code || "-";
    },
    groupByYearSemester(list) {
      const grouped = {};

      const formatYear = (year) => {
        if (!year) return "N/A Year";

        const suffix =
          year == 1 ? "1st" : year == 2 ? "2nd" : year == 3 ? "3rd" : `${year}th`;

        return `${suffix} Year`;
      };

      const formatSem = (sem) => {
        if (!sem) return "N/A Semester";

        const suffix =
          sem == 1 ? "1st" : sem == 2 ? "2nd" : sem == 3 ? "3rd" : `${sem}th`;

        return `${suffix} Semester`;
      };

      (list || []).forEach((item) => {
        const year = item.course?.course_level;
        const sem = item.course?.course_semester;

        const key = `${formatYear(year)} • ${formatSem(sem)}`;

        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(item);
      });

      return grouped;
    },
    convertTo24(time12) {
      if (!time12) return "";

      const clean = time12.replace(/\s+/g, "").toUpperCase();

      const match = clean.match(/(\d{1,2}):(\d{2})(AM|PM)/);
      if (!match) return "";

      let hours = parseInt(match[1]); // ✅ FIXED
      let minutes = match[2];
      const modifier = match[3];

      if (modifier === "PM" && hours !== 12) hours += 12;
      if (modifier === "AM" && hours === 12) hours = 0;

      return `${hours.toString().padStart(2, "0")}:${minutes}`;
    },

    toggleBranch(id) {
      const index = this.form.interbranchCampus.indexOf(id);

      if (index > -1) {
        this.form.interbranchCampus.splice(index, 1);
      } else {
        this.form.interbranchCampus.push(id);
      }
    },
    removeBranch(id) {
      this.form.interbranchCampus = this.form.interbranchCampus.filter((b) => b !== id);
    },

    handleClickOutside(event) {
      if (!this.$el.contains(event.target)) {
        this.showBranchDropdown = false;
        this.openActionMenuId = null;
      }
    },
    async loadUsers() {
      const store = useFetchDataStore();
      await store.fetchRawUsers();
      await store.fetchFacultyBranch();
    },
    formatTo12(time) {
      if (!time) return "";

      const [hour, minute] = time.split(":");
      let h = parseInt(hour);

      const ampm = h >= 12 ? "PM" : "AM";
      h = h % 12 || 12;

      return `${h}:${minute.padStart(2, "0")} ${ampm}`; // ✅ FIX
    },
    openAssignModal(user) {
      this.selectedFaculty = user;
      this.modalMode = "assign";
      this.showExpertiseModal = true;
    },

    openCrossAssignModal(user) {
      this.selectedFaculty = user;
      this.modalMode = "cross";
      this.showExpertiseModal = true;
    },
    openAddModal(user) {
      this.selectedFaculty = user;

      // Reset form first
      this.form = {
        morningStart: "",
        morningEnd: "",
        afternoonStart: "",
        afternoonEnd: "",
        interbranchCampus: [],
      };

      // =========================
      // ✅ 1. POPULATE PREFERRED TIME
      // =========================
      if (user.preffered_time) {
        const parts = user.preffered_time.split(",");

        parts.forEach((slot, index) => {
          const [rawStart, rawEnd] = slot.trim().split(" - ");

          const start24 = this.convertTo24(rawStart.trim());
          const end24 = this.convertTo24(rawEnd.trim());

          if (index === 0) {
            this.form.morningStart = start24;
            this.form.morningEnd = end24;
          } else if (index === 1) {
            this.form.afternoonStart = start24;
            this.form.afternoonEnd = end24;
          }
        });
      }
      // =========================
      // ✅ 2. POPULATE INTER-BRANCH (FIXED)
      // =========================
      this.form.interbranchCampus = (this.faculty_branch || [])
        .filter((fb) => fb.user.id === user.id)
        .map((fb) => fb.collegeBranch.college_branch_id);

      // =========================
      // ✅ 3. AUTO SELECT MODE (OPTIONAL BUT BETTER)
      // =========================
      if (user.preffered_time && this.form.interbranchCampus.length) {
        this.updateMode = "all";
      } else if (user.preffered_time) {
        this.updateMode = "preffered_time";
      } else if (this.form.interbranchCampus.length) {
        this.updateMode = "interbranch";
      } else {
        this.updateMode = "";
      }

      // =========================
      // ✅ 4. OPEN MODAL
      // =========================
      this.showAddModal = true;
    },
    toggleView(user) {
      // Access computed property WITHOUT parentheses
      this.selectedFaculty = {
        ...user,
        faculty_branches: this.facultyBranchesByUser[user.id] || [],
      };
      this.showViewModal = true;
    },
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },
    async fetchUser() {
      try {
        const response = await axios.get(process.env.VUE_APP_API_BASE_URL + "/auth/me", {
          withCredentials: true,
        });
        if (response.data) {
          this.user = response.data;
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },
    async submitData() {
      try {
        if (!this.updateMode) {
          alert("Please select update type.");
          return;
        }

        // Prepare variables
        const userId = this.selectedFaculty.id;

        // ----- 1️⃣ Only Preferred Time -----
        if (this.updateMode === "preffered_time") {
          if (this.totalHours !== 8) {
            alert("Total time must equal exactly 8 hours.");
            return;
          }

          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/users/${userId}`,
            { preffered_time: this.formattedSlot },
            { withCredentials: true }
          );

          toast.success("Preferred time updated successfully!");
          this.showAddModal = false;
          await this.loadUsers();
        }

        // ----- 2️⃣ Only Inter-branch -----
        else if (this.updateMode === "interbranch") {
          if (!this.form.interbranchCampus.length) {
            alert("Please select at least one inter-branch campus.");
            return;
          }

          // Delete existing faculty branch records for this user
          const existingBranches = (this.faculty_branch || []).filter(
            (fb) => fb.user.id === userId
          );

          for (const fb of existingBranches) {
            await axios.delete(
              `${process.env.VUE_APP_API_BASE_URL}/faculty-branch/${fb.faculty_branch_id}`,
              { withCredentials: true }
            );
          }

          // Add new faculty branch records
          for (const branchId of this.form.interbranchCampus) {
            await axios.post(
              `${process.env.VUE_APP_API_BASE_URL}/faculty-branch`,
              { user_id: userId, college_branch_id: branchId },
              { withCredentials: true }
            );
          }

          toast.success("Inter branch updated successfully!");
          this.showAddModal = false;
          await this.loadUsers();
        }

        // ----- 3️⃣ Both Preferred Time and Inter-branch -----
        else if (this.updateMode === "all") {
          if (this.totalHours !== 8) {
            alert("Total time must equal exactly 8 hours.");
            return;
          }

          // ✅ Update preferred time
          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/users/${userId}`,
            { preffered_time: this.formattedSlot },
            { withCredentials: true }
          );

          // ✅ DELETE existing (FIXED)
          const existingBranches = (this.faculty_branch || []).filter(
            (fb) => fb.user.id === userId
          );

          for (const fb of existingBranches) {
            await axios.delete(
              `${process.env.VUE_APP_API_BASE_URL}/faculty-branch/${fb.faculty_branch_id}`,
              { withCredentials: true }
            );
          }

          // ✅ INSERT new
          for (const branchId of this.form.interbranchCampus) {
            await axios.post(
              `${process.env.VUE_APP_API_BASE_URL}/faculty-branch`,
              { user_id: userId, college_branch_id: branchId },
              { withCredentials: true }
            );
          }

          toast.success("Preferred time and Inter Branch updated successfully!");
          this.showAddModal = false;
          await this.loadUsers();
        }

        // Reload users after update
        this.showAddModal = false;
        await this.loadUsers();
      } catch (error) {
        console.error(error);
        alert("Failed to update data. Check console for details.");
      }
    },
  },

  async mounted() {
    await this.fetchUser();
    await this.loadUsers();

    const store = useFetchDataStore();
    await store.fetchCollegeBranch();
    await store.fetchFacultyBranch();
  },
};
</script>
