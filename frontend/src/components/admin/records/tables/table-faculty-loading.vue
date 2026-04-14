<template>
  <!-- TODO  Loading Overlay -->
  <div
    v-if="loading"
    class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50"
  >
    <div class="relative flex items-center justify-center">
      <div
        class="absolute w-52 h-44 bg-gradient-to-r from-green-400/30 to-emerald-500/30 rounded-3xl animate-ping"
      ></div>
      <div
        class="relative flex flex-col items-center justify-center bg-white/90 backdrop-blur-md p-8 rounded-3xl shadow-2xl border border-white/30"
      >
        <div class="relative mb-4">
          <div
            class="w-12 h-12 border-4 border-green-400 border-t-transparent rounded-full animate-spin"
          ></div>
          <div class="absolute inset-0 flex items-center justify-center">
            <span class="text-defaultGreen text-sm font-semibold"
              >{{ Math.floor(progress) }}%</span
            >
          </div>
        </div>
        <div class="text-gray-700 font-semibold text-[15px] tracking-wide">
          Generating Schedule...
        </div>
        <div class="text-xs text-gray-500 mt-1">
          Please wait while we finalize your data.
        </div>
      </div>
    </div>
  </div>

  <!-- TODO  Confirm Save Modal -->
  <div
    v-if="showConfirmSaved"
    class="fixed inset-0 flex items-center justify-center bg-black/30 z-50"
  >
    <div class="bg-white rounded-2xl shadow-2xl p-6 w-96">
      <!-- TODO  Header -->
      <div class="flex items-center justify-between border-b pb-3 mb-4">
        <!-- Left: Icon + Title -->
        <div class="flex items-center gap-2">
          <icon
            name="exclamation-circle"
            class="w-7 h-7 p-1 rounded-full bg-green-200 text-green-900 flex items-center justify-center"
          />
          <h3 class="text-lg font-semibold text-gray-800 leading-none">Confirm Save</h3>
        </div>
      </div>

      <!-- TODO  Message -->
      <p class="text-gray-600 mb-6">Are you sure you want to save this schedule?</p>

      <!-- TODO  Buttons -->
      <div class="flex justify-center gap-2 text-sm">
        <button
          @click="showConfirmSaved = false"
          class="bg-gray-200 p-2 px-3 rounded-lg text-gray-700 hover:bg-white border hover:border-gray-800 hover:text-gray-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
        >
          Cancel
        </button>
        <button
          @click="saveScheduledConfirmed"
          class="bg-defaultGreen p-2 px-3 rounded-lg text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md transform transition-all duration-300 hover:scale-105"
        >
          Yes, Save
        </button>
      </div>
    </div>
  </div>
  <div class="flex flex-col h-[calc(100vh-180px)] overflow-hidden">
    <!-- TODO  Top Controls -->
    <div class="flex flex-wrap items-center justify-between">
      <div class="flex flex-wrap items-center gap-2">
        <!-- Institute -->
        <div class="relative">
          <select
            v-model="selectedInstituteId"
            class="appearance-none rounded-xl border border-green-600 bg-white px-4 py-2 pr-8 text-green-900 text-sm shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 hover:shadow-md"
          >
            <option value="">All Institutes</option>
            <option
              v-for="institute in uniqueInstitutes"
              :key="institute.id"
              :value="institute.id"
            >
              {{ institute.name }}
            </option>
          </select>

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

        <!-- Program -->
        <div class="relative">
          <select
            v-model="selectedProgramId"
            :disabled="!selectedInstituteId"
            class="appearance-none rounded-xl border border-green-600 bg-white px-4 py-2 pr-8 text-green-900 text-sm shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 hover:shadow-md disabled:bg-gray-100 disabled:border-gray-300 disabled:text-gray-400 disabled:cursor-not-allowed"
          >
            <option value="">All Programs</option>
            <option
              v-for="program in filteredPrograms"
              :key="program.id"
              :value="program.id"
            >
              {{ program.name }}
            </option>
          </select>

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
      </div>

      <!-- RIGHT SIDE -->
      <div class="flex flex-wrap items-center gap-2">
        <!-- Filters -->

        <!-- LEFT : Faculty Search -->
        <div class="relative w-full sm:w-64 md:w-72 lg:w-80">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search faculty..."
            class="rounded-xl border border-green-600 bg-white px-4 py-2.5 pl-10 text-sm shadow-sm w-full transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md"
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
        <!-- Actions -->
        <div class="flex items-center gap-2">
          <!-- Generate -->
          <button
            @click="generateSchedule"
            class="flex items-center gap-2 px-3 py-2.5 border bg-blue-700 text-white border-blue-600 rounded-xl hover:bg-white hover:text-blue-700 hover:shadow-lg transition duration-200"
          >
            <div class="p-1 bg-blue-800/20 rounded-full flex items-center justify-center">
              <icon name="arrow-path" />
            </div>
            <span class="font-medium text-sm">Generate</span>
          </button>

          <!-- Save -->
          <button
            @click="showConfirmSaved = true"
            class="flex items-center gap-2 px-3 py-2.5 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg transition duration-200"
          >
            <div
              class="p-1 bg-defaultGreen/20 rounded-full flex items-center justify-center"
            >
              <icon name="circle-check" />
            </div>
            <span class="font-medium text-sm">Save Schedule</span>
          </button>
        </div>
      </div>
    </div>

    <!-- TODO  Scrollable Content -->
    <div class="flex-1 overflow-y-auto scrollbar-hide">
      <div>
        <!-- TODO  Faculty Cards -->
        <div
          v-if="Object.keys(filteredFacultyCards).length"
          :class="[
            'gap-2 grid  overflow-hidden mt-2',
            Object.keys(filteredFacultyCards).length === 1
              ? 'grid-cols-1'
              : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-2',
          ]"
        >
          <div
            v-for="(schedules, instructor) in filteredFacultyCards"
            :key="instructor"
            class="bg-white rounded-xl border flex flex-col relative"
          >
            <!-- TODO  Header -->
            <div
              class="flex justify-between items-center bg-defaultGreen text-white px-4 py-3 font-semibold text-sm rounded-t-xl"
            >
              <span class="text-lg font-bold">{{ instructor }}</span>
              <div v-if="facultyTotalUnits[instructor]">
                <p class="font-normal">
                  Total Units:
                  {{ facultyTotalUnits[instructor].totalUnits }}
                </p>
              </div>
            </div>

            <!-- TODO  Schedule Table -->
            <div class="flex-1">
              <table class="w-full text-left border-collapse text-[11px]">
                <!-- <thead class="sticky top-0 bg-gray-100 z-10"></thead> -->
                <thead class="top-0 bg-gray-100 z-10">
                  <tr class="text-gray-700">
                    <th class="px-4 py-2 border border-gray-200 w-24 text-center">
                      Time
                    </th>
                    <th
                      v-for="day in days"
                      :key="day"
                      class="px-4 py-2 border border-gray-200 text-center w-28"
                    >
                      {{ day }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="slot in timeSlots"
                    :key="slot.start + slot.end"
                    class="odd:bg-white even:bg-gray-50"
                  >
                    <td
                      class="px-3 border border-gray-200 font-medium text-center whitespace-nowrap"
                    >
                      {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                    </td>
                    <td
                      v-for="day in days"
                      :key="day"
                      class="relative border border-gray-200 text-left align-top h-[60px] p-0"
                    >
                      <template
                        v-for="item in getScheduleForCell(slot, day, instructor)"
                        :key="item.course_name + item.start_hour + item.room_name"
                      >
                        <div
                          v-if="isStartingSlot(item, slot)"
                          draggable="true"
                          @mouseenter="showScheduleTooltip($event, item)"
                          @mouseleave="hideScheduleTooltip"
                          @click="highlightRow(item)"
                          :class="[
                            'absolute inset-x-1 border rounded text-[11px] p-1 shadow-sm truncate cursor-pointer',
                            item.id?.toString().startsWith('temp-')
                              ? 'bg-purple-200 border-purple-400 text-purple-900'
                              : getTypeColor(item.type),
                            hasRoomConflict(item)
                              ? 'bg-red-300 border-red-500 text-red-900'
                              : '',
                          ]"
                          :style="{
                            top: getBlockTop(item, slot.start) + 'px',
                            height: getBlockHeight(item) + 'px',
                            width: 'calc(100% - 0.5rem)',
                            zIndex: 20,
                          }"
                        >
                          <!-- schedule_type BADGE -->
                          <span
                            v-if="item.schedule_type"
                            :class="[
                              'absolute top-1 right-1 w-auto h-4 px-1 rounded-full text-[10px] font-bold flex items-center justify-center text-white',
                              item.schedule_type === 'face to face'
                                ? 'bg-orange-500'
                                : '',
                              item.schedule_type === 'online' ? 'bg-purple-500' : '',
                            ]"
                          >
                            {{ item.schedule_type === "face to face" ? "F2F" : "OL" }}
                          </span>
                          <div class="leading-snug truncate">
                            <p class="font-semibold truncate">
                              {{ item.course_code }}
                            </p>
                            <p class="text-gray-600 truncate">
                              {{ item.room_name }}
                            </p>
                            <p class="text-gray-600 truncate">
                              {{ item.program_code }}-{{ item.set_name }}
                            </p>
                            <button
                              v-if="hasRoomConflict(item) && !isJoined"
                              @click.stop="openConflictModal(item)"
                              class="absolute bottom-1 right-1 flex items-center justify-center w-4 h-4 rounded-full bg-red-600 text-white text-[9px] font-bold shadow hover:bg-red-700"
                              title="View conflict"
                            >
                              !
                            </button>
                          </div>
                        </div>
                      </template>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- 🔍 Schedule Tooltip -->
            <div
              v-if="scheduleTooltipVisible && tooltipItem"
              class="fixed z-[9999] pointer-events-none"
              :style="{
                top: tooltipY + 'px',
                left: tooltipX + 'px',
                maxWidth: '260px',
              }"
            >
              <div class="bg-white border border-gray-300 rounded-xl p-3 scale-125">
                <div class="flex items-center justify-between gap-2 mb-2 w-full">
                  <!-- Course Code -->
                  <div class="text-sm font-bold text-defaultGreen leading-none">
                    {{ tooltipItem.course_code }}
                  </div>

                  <span
                    v-if="tooltipItem.schedule_type"
                    class="inline-flex items-center justify-center px-2 py-1 text-[8px] leading-none rounded-full text-white"
                    :class="
                      tooltipItem.schedule_type === 'face to face'
                        ? 'bg-orange-500'
                        : 'bg-purple-500'
                    "
                  >
                    {{
                      tooltipItem.schedule_type === "face to face"
                        ? "Face to Face"
                        : "Online"
                    }}
                  </span>
                </div>

                <div class="text-[10px] text-gray-700 space-y-0.5">
                  <p><strong>Faculty:</strong> {{ tooltipItem.faculty_name }}</p>
                  <p>
                    <strong>Year & Section:</strong>
                    {{ tooltipItem.program_code }}-{{ tooltipItem.set_name }}
                  </p>
                  <p><strong>Room:</strong> {{ tooltipItem.room_name }}</p>
                  <p><strong>Day:</strong> {{ tooltipItem.day }}</p>
                  <p>
                    <strong>Time:</strong>
                    {{ formatTime(tooltipItem.start_hour) }} –
                    {{
                      formatTime(tooltipItem.start_hour + Number(tooltipItem.duration))
                    }}
                  </p>
                  <p><strong>Type:</strong> {{ tooltipItem.type }}</p>
                  <p>
                    <strong>Campus Branch:</strong>
                    {{ getCollegeBranchName(tooltipItem.college_branch_id) }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- TODO  Fallback ONLY for Faculty Cards -->
        <div
          v-else
          class="flex flex-col items-center justify-center min-h-[400px] text-center text-gray-500"
        >
          <div class="text-center text-gray-500">
            <p class="text-lg font-semibold mb-2">No schedule data available</p>
            <p class="text-sm text-gray-400">
              Please click
              <span class="font-medium text-defaultGreen">"Generate"</span>
              to generate schedule data.
            </p>
          </div>
        </div>
        <div
          v-if="totalCardPages > 1"
          class="flex justify-center items-center gap-2 mt-4"
        >
          <button
            @click="cardPage--"
            :disabled="cardPage === 1"
            class="px-3 py-1 rounded-lg bg-gray-200 disabled:opacity-50"
          >
            &lt;
          </button>

          <span class="text-sm font-medium text-gray-600">
            Page {{ cardPage }} of {{ totalCardPages }}
          </span>

          <button
            @click="cardPage++"
            :disabled="cardPage === totalCardPages"
            class="px-3 py-1 rounded-lg bg-gray-200 disabled:opacity-50"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>

    <ConflictModal
      :visible="conflictModalVisible"
      :schedule="selectedSchedule"
      :conflicts="conflictRecords"
      @close="closeConflictModal"
      @cancel="closeConflictModal"
    />
  </div>
</template>

<script>
import axios from "axios";
import icon from "@/assets/icon.vue";
import { useFetchDataStore } from "@/store/fetch-data-store";
import ConflictModal from "@/components/program-chairperson/program-record/faculty-components/conflict-modal.vue";
import { toast } from "vue3-toastify";
// import sample_schedule from "./sample_schedule.json";
export default {
  name: "FacultySchedule",
  components: { icon, ConflictModal },

  data() {
    return {
      user: {},
      schedule: [],
      unscheduledMeetings: [],
      groupedSchedule: {},
      filteredGroupedSchedule: {},
      loading: false,
      error: null,
      showFacultyTable: false,
      selectedInstructor: null,
      scheduleGenerated: false,
      selectedInstituteId: "",
      selectedProgramId: "",
      showConfirmSaved: false,
      days: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ],

      timeSlots: Array.from({ length: 14 }, (_, i) => ({
        start: 7 + i, // 7, 8, 9 ... 20
        end: 8 + i, // 8, 9, 10 ... 21
      })),

      progress: 0,
      progressInterval: null,
      showConflictModal: false,
      selectedConflict: {},
      currentPage: 1,
      itemsPerPage: 10,
      timeSlotHeight: 60,

      schoolYears: [],

      conflictModalVisible: false,
      scheduleTooltipVisible: false,
      tooltipItem: null,
      tooltipX: 0,
      tooltipY: 0,
      cardPage: 1,
      cardsPerPage: 6,
      pageWindow: 3,
      searchQuery: "",
    };
  },

  computed: {
    filteredFacultyCards() {
      let entries = Object.entries(this.filteredGroupedSchedule);

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        entries = entries.filter(([faculty]) => faculty.toLowerCase().includes(q));
      }

      const start = (this.cardPage - 1) * this.cardsPerPage;
      const end = start + this.cardsPerPage;

      return Object.fromEntries(entries.slice(start, end));
    },
    totalCardPages() {
      const entries = Object.entries(this.filteredGroupedSchedule);

      const filtered = this.searchQuery
        ? entries.filter(([faculty]) =>
            faculty.toLowerCase().includes(this.searchQuery.toLowerCase())
          )
        : entries;

      return Math.ceil(filtered.length / this.cardsPerPage);
    },

    coursesList() {
      const store = useFetchDataStore();
      return store.courses || [];
    },
    collegeBranches() {
      const store = useFetchDataStore();
      return store.college_branch || [];
    },
    // Total units per faculty
    facultyTotalUnits() {
      const result = {};

      Object.entries(this.filteredGroupedSchedule).forEach(([faculty, schedules]) => {
        let totalLecture = 0;
        let totalLab = 0;

        schedules.forEach((sched) => {
          const course = this.coursesList.find(
            (c) => c.course_code === sched.course_code
          );
          if (!course) return;

          const duration = Number(sched.duration || 0);

          if (sched.type === "Lecture") {
            const unitsPerSlot = (duration / 3) * Number(course.course_lec || 0);
            totalLecture += unitsPerSlot;
          } else if (sched.type === "Laboratory") {
            const unitsPerSlot = (duration / 3) * Number(course.course_lab || 0);
            totalLab += unitsPerSlot;
          }
        });

        const lectureUnits = Number(totalLecture.toFixed(2));
        const labUnits = Number(totalLab.toFixed(2));
        const totalUnits = Number((lectureUnits + labUnits).toFixed(2));

        result[faculty] = {
          lectureUnits,
          labUnits,
          totalUnits,
        };
      });

      return result;
    },
    // Map institute IDs to their names
    uniqueInstitutes() {
      const store = useFetchDataStore();
      const institutes = store.institutes || [];

      const ids = [...new Set(this.schedule.map((s) => Number(s.institute_id)))];

      return ids.map((id) => {
        const inst = institutes.find((i) => Number(i.institute_id) === id);

        return {
          id,
          name: inst?.institute_code || `Institute ${id}`,
        };
      });
    },

    // Map program IDs to their names (filtered by selectedInstituteId if any)
    filteredPrograms() {
      const store = useFetchDataStore();
      const programs = store.programs || [];

      let ids;

      if (!this.selectedInstituteId) {
        ids = [...new Set(this.schedule.map((s) => Number(s.program_id)))];
      } else {
        ids = [
          ...new Set(
            this.schedule
              .filter((s) => Number(s.institute_id) === Number(this.selectedInstituteId))
              .map((s) => Number(s.program_id))
          ),
        ];
      }

      return ids.map((id) => {
        const prog = programs.find((p) => Number(p.program_id) === id);

        return {
          id,
          name: prog?.program_code || `Program ${id}`,
        };
      });
    },

    // Compute latest active school year dynamically
    latestActiveSchoolYear() {
      if (!this.schoolYears.length) return null;
      const activeYears = this.schoolYears.filter((y) => y.is_active);
      if (!activeYears.length) return null;
      return activeYears.reduce((latest, current) =>
        new Date(current.updated_at) > new Date(latest.updated_at) ? current : latest
      );
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(
        this.currentPage * this.itemsPerPage,
        Object.keys(this.filteredGroupedSchedule).length
      );
    },

    totalPages() {
      return Math.ceil(
        Object.keys(this.filteredGroupedSchedule).length / this.itemsPerPage
      );
    },

    // --------------------------
    // Updated pageNumbers for windowed pagination
    // --------------------------
    pageNumbers() {
      const halfWindow = Math.floor(this.pageWindow / 2);
      let start = Math.max(1, this.currentPage - halfWindow);
      let end = Math.min(this.totalPages, start + this.pageWindow - 1);

      start = Math.max(1, end - this.pageWindow + 1);

      const pages = [];
      for (let i = start; i <= end; i++) pages.push(i);
      return pages;
    },

    paginatedFaculty() {
      let entries = Object.entries(this.filteredGroupedSchedule);

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        entries = entries.filter(([faculty]) => faculty.toLowerCase().includes(q));
      }

      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return Object.fromEntries(entries.slice(start, end));
    },
  },

  watch: {
    selectedInstituteId() {
      this.filterSchedules();
      this.selectedProgramId = "";
      this.cardPage = 1;
    },

    selectedProgramId() {
      this.filterSchedules();
      this.cardPage = 1;
    },

    // ✅ FINAL FIX
    searchQuery() {
      this.currentPage = 1;
      this.cardPage = 1;
    },
  },

  methods: {
    async loadFetchData() {
      const store = useFetchDataStore();
      await store.fetchPrograms();
      await store.fetchInstitutes();
      await store.fetchCourses();
      await store.fetchCollegeBranch();
    },
    getCollegeBranchName(branchId) {
      const branch = this.collegeBranches.find(
        (b) => Number(b.college_branch_id) === Number(branchId)
      );

      return branch ? branch.college_branch_name : `Branch ${branchId}`;
    },
    showScheduleTooltip(event, item) {
      const rect = event.currentTarget.getBoundingClientRect();

      const tooltipWidth = 260;
      const tooltipHeight = 160;
      const padding = 10;

      let x = rect.right + padding;
      let y = rect.top;

      const screenWidth = window.innerWidth;
      const screenHeight = window.innerHeight;

      // Prevent overflow right
      if (x + tooltipWidth > screenWidth) {
        x = rect.left - tooltipWidth - padding;
      }

      // Prevent overflow bottom
      if (y + tooltipHeight > screenHeight) {
        y = screenHeight - tooltipHeight - padding;
      }

      this.tooltipX = x;
      this.tooltipY = y;
      this.tooltipItem = item;
      this.scheduleTooltipVisible = true;
    },

    hideScheduleTooltip() {
      this.scheduleTooltipVisible = false;
      this.tooltipItem = null;
    },

    backToFacultyTable() {
      this.filteredGroupedSchedule = this.groupedSchedule;
      this.showFacultyTable = true;
      this.currentPage = 1;
    },
    highlightRow(item) {
      this.highlightedRecordId = item.id || item.tempId;
      // optional: scroll to the row
      this.$nextTick(() => {
        const el = document.getElementById(`row-${this.highlightedRecordId}`);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    },

    // Normalize hour to 24h format
    normalizeHour(hour) {
      const h = Number(hour);
      if (Number.isNaN(h)) return null;
      return h; // ✅ already 24-hour based
    },

    // Get all conflicting records for a given schedule item
    getConflictingRecords(record) {
      const allSchedules = this.schedule || [];
      const recordStart = this.normalizeHour(record.start_hour);
      const recordEnd = recordStart + Number(record.duration);

      return allSchedules
        .map((r) => {
          const rId = r.id?.toString() || r.tempId;
          const recId = record.id?.toString() || record.tempId;

          // Skip the same record
          if (r.faculty_id === record.faculty_id && rId === recId) return null;

          // Must be on the same day
          if (r.day !== record.day) return null;

          // Check for time overlap
          const rStart = this.normalizeHour(r.start_hour);
          const rEnd = rStart + Number(r.duration);

          if (Math.max(rStart, recordStart) >= Math.min(rEnd, recordEnd)) return null;

          // Determine conflict reasons
          let reason = [];

          // SAME CLASS SECTION
          if (r.class_id && record.class_id && r.class_id === record.class_id) {
            reason.push("Same class section in the same Day and Time");
          }

          // SAME ROOM (Face to Face)
          if (
            (record.schedule_type || "").toLowerCase() === "face to face" &&
            (r.schedule_type || "").toLowerCase() === "face to face" &&
            r.room_id === record.room_id
          ) {
            reason.push("Same Room");
          }

          // SAME FACULTY
          if (
            r.faculty_id === record.faculty_id &&
            (r.schedule_type || "").toLowerCase() ===
              (record.schedule_type || "").toLowerCase()
          ) {
            reason.push("Same Faculty + Same schedule_type");
          }

          // ✅ ONLINE CONFLICT (same program + same section only)
          if (
            (record.room_name || "").toLowerCase() === "online" &&
            (r.room_name || "").toLowerCase() === "online" &&
            r.set_name === record.set_name &&
            r.program_id === record.program_id &&
            r.college_branch_id === record.college_branch_id &&
            r.college_branch_id === record.college_branch_id
          ) {
            reason.push(
              "ONLINE conflict: Same program section cannot attend two online classes at the same time."
            );
          }

          if (!reason.length) return null;

          return { ...r, reason: reason.join(", ") };
        })
        .filter(Boolean);
    },

    // Check if a record has any room/faculty conflicts
    hasRoomConflict(record) {
      return this.getConflictingRecords(record).length > 0;
    },

    // Open the conflict modal for a record
    openConflictModal(record) {
      const conflicts = this.getConflictingRecords(record);

      if (!conflicts.length) return;

      this.selectedSchedule = record; // 👈 LEFT SIDE
      this.conflictRecords = conflicts; // 👉 RIGHT SIDE
      this.conflictModalVisible = true;
    },

    closeConflictModal() {
      this.conflictModalVisible = false;
      this.conflictRecords = [];
      this.selectedSchedule = null;
    },

    isStartingSlot(item, slot) {
      return item.start_hour >= slot.start && item.start_hour < slot.end;
    },
    getBlockTop(item, slotStart) {
      if (!item || item.start_hour == null) return 0;

      const start = this.normalizeHour(Number(item.start_hour));
      return (start - slotStart) * this.timeSlotHeight;
    },

    getBlockHeight(item) {
      if (!item || !item.duration) return this.timeSlotHeight;

      return Number(item.duration) * this.timeSlotHeight - 1;
    },

    checkConflicts() {
      const conflicts = [];
      const allSchedules = this.schedule;

      for (let i = 0; i < allSchedules.length; i++) {
        for (let j = i + 1; j < allSchedules.length; j++) {
          const a = allSchedules[i];
          const b = allSchedules[j];

          const sameDay = a.day === b.day;
          const sameRoom = a.room_name === b.room_name;
          const sameCourse = a.course_code === b.course_code;

          const aStart = this.normalizeHour(a.start_hour);
          const aEnd = aStart + Number(a.duration);

          const bStart = this.normalizeHour(b.start_hour);
          const bEnd = bStart + Number(b.duration);

          const overlap = aEnd > bStart && aStart < bEnd;

          if (sameDay && sameRoom && sameCourse && overlap) {
            conflicts.push({ a, b });
          }
        }
      }
      return conflicts;
    },

    formatTime(h) {
      if (h == null) return "";
      const hour = Math.floor(h); // integer hour
      const minutes = Math.round((h - hour) * 60); // decimal -> minutes
      const period = hour >= 12 ? "PM" : "AM";
      const hour12 = hour % 12 || 12;
      const minutesStr = minutes.toString().padStart(2, "0");
      return `${hour12}:${minutesStr} ${period}`;
    },

    changePage(page) {
      if (page < 1) page = 1;
      if (page > this.totalPages) page = this.totalPages;
      this.currentPage = page;
    },

    filterSchedules() {
      let filtered = { ...this.groupedSchedule };

      if (this.selectedInstituteId)
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some((s) => s.institute_id == this.selectedInstituteId)
          )
        );

      if (this.selectedProgramId)
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some((s) => s.program_id == this.selectedProgramId)
          )
        );

      this.filteredGroupedSchedule = filtered;
      this.cardPage = 1;
      this.changePage(1);
    },
    getScheduleForCell(slot, day, instructor) {
      const schedules = this.filteredGroupedSchedule[instructor] || [];
      return schedules.filter((item) => {
        if (item.day !== day) return false;

        const start = this.normalizeHour(item.start_hour);
        const end = start + Number(item.duration);
        return end > slot.start && start < slot.end;
      });
    },

    getTypeColor(room_type) {
      if (!room_type) return "bg-green-100 border-green-400";
      const normalized = room_type.toLowerCase();
      if (normalized === "laboratory" || normalized === "lab") {
        return "bg-blue-200 border-blue-300";
      }
      return "bg-green-200 border-green-300";
    },

    viewFacultySchedule(instructor) {
      this.filteredGroupedSchedule = {
        [instructor]: this.groupedSchedule[instructor],
      };
      this.showFacultyTable = false;
    },

    async fetchUser() {
      try {
        const res = await axios.get(`${process.env.VUE_APP_API_BASE_URL}/auth/me`, {
          withCredentials: true,
        });
        this.user = res.data || {};
      } catch {
        this.user = {};
      }
    },

    async fetchSchedule() {
      this.loading = true;
      this.progress = 0;
      this.progressInterval = setInterval(() => {
        if (this.progress < 90) this.progress += Math.random() * 10;
      }, 200);

      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/generated-scheduled/load`
        );

        const data = res.data.data || {};

        const allSchedules = data.scheduled_meetings || [];
        this.unscheduledMeetings = data.unscheduled_meetings || []; // ✅ IMPORTANT

        this.schedule = allSchedules;
        this.groupedSchedule = this.groupByInstructor(this.schedule);
        this.filteredGroupedSchedule = this.groupedSchedule;
      } catch {
        this.error = "Failed to fetch schedule.";
      } finally {
        clearInterval(this.progressInterval);
        this.progress = 100;
        setTimeout(() => (this.loading = false), 400);
      }
    },

    //     async fetchSchedule() {
    //   this.loading = true;

    //   try {
    //     // JSON content is already available
    //     const allSchedules = sample_schedule.scheduled_meetings || [];

    //     this.schedule = allSchedules;
    //     this.groupedSchedule = this.groupByInstructor(this.schedule);
    //     this.filteredGroupedSchedule = this.groupedSchedule;
    //   } catch (err) {
    //     this.error = "Failed to load schedule.";
    //   } finally {
    //     this.loading = false;
    //   }
    // },

    groupByInstructor(schedules) {
      return schedules.reduce((acc, s) => {
        const instructor = s.faculty_name || "Unknown Faculty";
        if (!acc[instructor]) acc[instructor] = [];
        acc[instructor].push(s);
        return acc;
      }, {});
    },

    async generateSchedule() {
      const store = useFetchDataStore();

      try {
        this.loading = true;
        this.progress = 0;

        // simulate progress animation
        this.progressInterval = setInterval(() => {
          if (this.progress < 90) {
            this.progress += Math.random() * 10;
          }
        }, 200);

        // 1️⃣ Trigger scheduler (updates JSON)
        await store.runScheduler();

        // 2️⃣ Fetch generated schedule from JSON
        const data = await store.fetchGeneratedScheduled();

        this.schedule = data.scheduled_meetings || [];
        this.unscheduledMeetings = data.unscheduled_meetings || [];

        this.groupedSchedule = this.groupByInstructor(this.schedule);
        this.filteredGroupedSchedule = this.groupedSchedule;

        this.scheduleGenerated = true;
        this.showFacultyTable = false;
      } catch (err) {
        console.error(err);
        this.error = "Failed to generate schedule";
      } finally {
        this.loading = false;
      }
    },
    async fetchSchoolYears() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years"
        );
        this.schoolYears = res.data.map((y) => ({ ...y }));
      } catch (err) {
        console.error("Failed to fetch school years:", err);
      }
    },

    async saveScheduledConfirmed() {
      this.showConfirmSaved = false;

      try {
        // Always fetch latest school years before saving
        await this.fetchSchoolYears();

        const latestSchoolYear = this.latestActiveSchoolYear;
        if (!latestSchoolYear) {
          alert("❌ No active school year found. Cannot save schedule.");
          return;
        }

        // ----------------------------------------
        // 1️⃣ SAVE SCHEDULED MEETINGS
        // ----------------------------------------
        const scheduledPayload = this.schedule.map((item) => ({
          class_id: item.class_id,
          set_name: item.set_name,
          course_code: item.course_code,
          program_id: item.program_id,
          college_branch_id: item.college_branch_id,
          program_code: item.program_code,
          institute_id: item.institute_id,
          type: item.type,
          day: item.day,
          start_hour: item.start_hour,
          duration: item.duration,
          time_slot: `${this.formatTime(item.start_hour)} - ${this.formatTime(
            item.start_hour + Number(item.duration)
          )}`,
          room_id: item.room_id,
          room_name: item.room_name,
          room_type: item.room_type,
          room_capacity: item.room_capacity,
          class_size: item.class_size,
          faculty_id: item.faculty_id,
          faculty_name: item.faculty_name,
          school_year: latestSchoolYear.school_year_name,
          semester: latestSchoolYear.semester,
          mode: item.schedule_type,
        }));

        if (scheduledPayload.length > 0) {
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/bulk`,
            scheduledPayload,
            { withCredentials: true }
          );
        }

        // ----------------------------------------
        // 2️⃣ SAVE UNSCHEDULED MEETINGS
        // ----------------------------------------
        const unscheduledMeetings = this.unscheduledMeetings || [];

        const unscheduledPayload = unscheduledMeetings.map((item) => ({
          class_id: item.class_id,
          course_code: item.course_code,
          program_id: item.program_id,
          program_code: item.program_code,
          type: item.type,
          hours: item.hours,
          reason: item.reason,
          school_year: latestSchoolYear.school_year_name,
          semester: latestSchoolYear.semester,
        }));

        if (unscheduledPayload.length > 0) {
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/unscheduled-meetings/add-unscheduled-meetings`,
            unscheduledPayload,
            { withCredentials: true }
          );
        }

        toast.success("✅ Schedule and unscheduled meetings saved successfully!");
      } catch (error) {
        console.error(error);
        alert("❌ Failed to save schedule.");
      }
    },
  },

  async mounted() {
    const store = useFetchDataStore();

    await store.fetchInstitutes();
    await store.fetchPrograms();
    await store.fetchCollegeBranch();
    await store.fetchCourses();

    const data = await store.fetchGeneratedScheduled();
    if (!data) {
      this.schedule = [];
      this.unscheduledMeetings = [];
      this.groupedSchedule = {};
      this.filteredGroupedSchedule = {};
      return;
    }

    this.schedule = data.scheduled_meetings || [];
    this.unscheduledMeetings = data.unscheduled_meetings || [];

    this.groupedSchedule = this.groupByInstructor(this.schedule);
    this.filteredGroupedSchedule = this.groupedSchedule;
  },
};
</script>
<style>
/* Hide scrollbar but allow scrolling */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none; /* IE & Edge */
  scrollbar-width: none; /* Firefox */
}
</style>
