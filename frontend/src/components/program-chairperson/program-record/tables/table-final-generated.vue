<template>
  <div class="flex flex-col h-[82vh]">
    <!-- TODO  Top Controls -->

    <FacultyTopControls
      v-model:searchQuery="searchQuery"
      v-model:isJoined="isJoined"
      :showFacultyTable="showFacultyTable"
      :showCompareSelection="showCompareSelection"
      v-model:compareInstructorA="compareInstructorA"
      v-model:compareInstructorB="compareInstructorB"
      :instructorList="Object.keys(groupedSchedule)"
      @toggleFacultyTable="showFacultyTable = !showFacultyTable"
      @toggleCompareSelection="toggleShowCompareSelection"
      @compare="showCompareFacultyCards"
      @backFromCompare="backFromCompare"
    />

    <!-- TODO  Scrollable Content -->
    <div class="flex-1 overflow-y-auto mt-2">
      <!-- TODO  Faculty Cards -->
      <div
        :class="[
          'gap-2 grid h-auto',
          showCompareView
            ? 'grid-cols-1 md:grid-cols-2 h-[87vh] overflow-y-auto'
            : Object.keys(filteredBySearch).length === 1
            ? 'grid-cols-1'
            : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-2 overflow-y-auto',
        ]"
        class="overflow-y-auto scrollbar-hide"
      >
        <div
          v-for="(records, instructor) in paginatedFacultyCards"
          :key="instructor"
          class="bg-white rounded-xl border flex flex-col shadow-sm overflow-hidden"
        >
          <!-- Header -->
          <div
            class="flex justify-between items-center bg-defaultGreen text-white px-4 py-3 font-semibold text-sm rounded-t-xl"
          >
            <div class="flex flex-col">
              <span class="text-lg font-bold">{{ instructor }}</span>

              <div v-if="facultyTotalUnits[instructor]">
                <p class="font-normal">
                  Total Units:
                  {{ facultyTotalUnits[instructor].totalUnits }}
                </p>
              </div>
            </div>

            <button
              @click="openEditInstructorModal(instructor)"
              class="border border-white hover:bg-white hover:text-defaultGreen text-white px-3 py-1 rounded-full text-xs transition"
            >
              Edit
            </button>
          </div>

          <!-- Table wrapper -->
          <div class="overflow-x-auto overflow-y-auto flex-1">
            <table class="w-full text-left border-collapse text-[11px]">
              <thead class="sticky top-0 bg-gray-100 z-10">
                <tr class="text-gray-700 bg-gray-200 border">
                  <th class="py-3 w-2 text-center text-gray-700 bg-gray-100">Time</th>
                  <th
                    v-for="day in days"
                    :key="day"
                    class="px-4 py-2 text-center w-2 text-gray-700 bg-gray-100"
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
                  :style="{ height: timeSlotHeight + 'px' }"
                >
                  <!-- Time Column -->
                  <td class="py-4 border text-center whitespace-nowrap text-gray-700">
                    {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                  </td>

                  <!-- Schedule Cells -->
                  <td
                    v-for="day in days"
                    :key="day"
                    class="relative border p-0 overflow-visible transition-colors"
                    :class="{
                      'bg-green-100':
                        isJoined &&
                        draggedRecord &&
                        getJoinableSchedules(draggedRecord).some((j) => j.day === day),
                      'bg-red-100':
                        draggedRecord &&
                        getConflictsForDrag(draggedRecord, instructor, day, slot.start)
                          .length,
                    }"
                    @dragover.prevent
                    @drop="onDrop($event, instructor, day, slot.start)"
                  >
                    <template
                      v-for="item in getScheduleForCell(slot, day, instructor)"
                      :key="
                        item.id || item.course_code + item.start_hour + item.room_name
                      "
                    >
                      <div
                        v-if="isStartingSlot(item, slot)"
                        :draggable="
                          canEditSchedule(item) &&
                          !(isJoined && Number(item.class_size) >= 30)
                        "
                        @dblclick.stop="handleUnjoin(item)"
                        @dragstart="onDragStart($event, item)"
                        @mouseenter="showScheduleTooltip($event, item)"
                        @mouseleave="hideScheduleTooltip"
                        :class="[
                          'absolute inset-x-1 border rounded-md text-[11px] p-1 shadow-sm overflow-hidden transition-all duration-200 whitespace-nowrap',

                          // temp schedule
                          item.id?.toString().startsWith('temp-')
                            ? 'bg-purple-200 border-purple-400 text-purple-900'
                            : // cannot edit schedule → gray style
                            !canEditSchedule(item)
                            ? 'bg-gray-200 border-gray-300 text-gray-500 opacity-80 cursor-not-allowed'
                            : // normal type color
                              getTypeColor(item.type),

                          // room conflict
                          hasRoomConflict(item) && !isJoined
                            ? 'bg-red-300 border-red-500 text-red-900'
                            : '',

                          // swap selected
                          swapSelection.includes(item)
                            ? 'border-yellow-500 bg-yellow-100'
                            : '',

                          // joined schedule
                          item.is_joined ? 'bg-blue-100 border-blue-400' : '',

                          // joined disabled
                          isJoined && Number(item.class_size) >= 30
                            ? 'opacity-50 pointer-events-none cursor-not-allowed'
                            : '',

                          // hover only if editable
                          canEditSchedule(item)
                            ? 'cursor-pointer hover:bg-yellow-100'
                            : '',
                        ]"
                        :style="{
                          top: getBlockTop(item, slot.start) + 'px',
                          height: getBlockHeight(item) + 'px',
                          width: 'calc(100% - 0.5rem)',
                          zIndex: 10,
                        }"
                      >
                        <!-- Mode Badge -->
                        <span
                          v-if="item.mode"
                          :class="[
                            'absolute top-1 right-1 w-auto h-4 px-1 rounded-full text-[10px] font-bold flex items-center justify-center text-white',
                            item.mode === 'face to face' ? 'bg-orange-500' : '',
                            item.mode === 'online' ? 'bg-purple-500' : '',
                          ]"
                        >
                          {{ item.mode === "face to face" ? "F2F" : "OL" }}
                        </span>

                        <!-- Join Badge -->
                        <span
                          v-if="item.is_joined"
                          class="absolute bottom-2 right-2 px-2 h-5 flex items-center justify-center bg-blue-600 text-white text-[10px] font-bold rounded-full shadow"
                        >
                          J
                        </span>

                        <!-- Course Info -->
                        <div class="truncate font-semibold">
                          {{ item.course_code }}
                        </div>
                        <div class="truncate">{{ item.room_name }}</div>
                        <div class="truncate">
                          <template v-if="item.is_joined && item.join_group_id">
                            {{
                              finalSchedules
                                .filter((s) => s.join_group_id === item.join_group_id)
                                .map((s) => `${s.display_program_code}-${s.set_name}`)
                                .join(" + ")
                            }}
                          </template>

                          <template v-else>
                            {{ item.display_program_code }}-{{ item.set_name }}
                          </template>
                        </div>

                        <!-- Conflict Button -->
                        <!-- Conflict Icon -->
                        <button
                          v-if="hasRoomConflict(item) && !isJoined"
                          @click.stop="openConflictModal(item)"
                          class="absolute bottom-1 right-1 flex items-center justify-center w-4 h-4 rounded-md bg-red-600 text-white text-[9px] font-bold shadow hover:bg-red-700"
                          title="View conflict"
                        >
                          !
                        </button>
                        <!-- <div class="w-full flex justify-center mt-1">
                          <button
                            v-if="hasRoomConflict(item) && !isJoined"
                            @click.stop="openConflictModal(item)"
                            class="px-2 h-5 text-[10px] bg-red-100 text-red-600 rounded"
                          >
                            ⚠ View
                          </button>
                        </div> -->
                      </div>
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
            <!-- 🔍 Schedule Tooltip -->
            <div
              v-if="scheduleTooltipVisible && tooltipItem"
              class="fixed z-[9999] pointer-events-none"
              :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
            >
              <div
                class="w-[280px] overflow-hidden rounded-xl border border-gray-200 bg-white shadow-[0_18px_45px_rgba(15,23,42,0.18)]"
              >
                <!-- Header -->
                <div
                  class="border-b border-gray-100 bg-gradient-to-r from-emerald-50 to-white px-4 py-3"
                >
                  <div class="flex items-start justify-between gap-3">
                    <div>
                      <p
                        class="text-[10px] font-semibold uppercase tracking-wide text-gray-400"
                      >
                        Schedule Details
                      </p>

                      <h3
                        class="mt-0.5 text-sm font-bold text-defaultGreen leading-tight"
                      >
                        {{ tooltipItem.course_code }}
                      </h3>
                    </div>

                    <span
                      v-if="tooltipItem.mode"
                      class="shrink-0 inline-flex items-center rounded-full px-2.5 py-1 text-[9px] font-semibold text-white shadow-sm"
                      :class="
                        tooltipItem.mode === 'face to face'
                          ? 'bg-orange-500'
                          : 'bg-purple-500'
                      "
                    >
                      {{
                        tooltipItem.mode === "face to face" ? "Face to Face" : "Online"
                      }}
                    </span>
                  </div>
                </div>

                <!-- Body -->
                <div class="px-4 py-3">
                  <div class="space-y-3 text-[11px] text-gray-700">
                    <!-- Faculty -->
                    <!-- <div>
                      <p
                        class="text-[9px] font-semibold uppercase tracking-wide text-gray-400"
                      >
                        Faculty
                      </p>
                      <p class="mt-0.5 font-semibold text-gray-800">
                        {{ tooltipItem.faculty_name || "Not assigned" }}
                      </p>
                    </div> -->

                    <!-- Year and Section -->
                    <div>
                      <p
                        class="text-[9px] font-semibold uppercase tracking-wide text-gray-400"
                      >
                        Year & Section
                      </p>

                      <div class="mt-1 space-y-1">
                        <template
                          v-if="tooltipItem.is_joined && tooltipItem.join_group_id"
                        >
                          <div
                            v-for="s in finalSchedules.filter(
                              (s) => s.join_group_id === tooltipItem.join_group_id
                            )"
                            :key="s.class_id"
                            class="rounded-lg border border-gray-100 bg-gray-50 px-2.5 py-1.5"
                          >
                            <p class="font-semibold text-gray-800">
                              {{ s.display_program_code }} -
                              {{ s.set_name }}
                            </p>
                            <p class="text-[10px] text-gray-500">
                              Class Size: {{ s.class_size }}
                            </p>
                          </div>
                        </template>

                        <template v-else>
                          <div
                            class="rounded-lg border border-gray-100 bg-gray-50 px-2.5 py-1.5"
                          >
                            <!-- <p class="font-semibold text-gray-800">
                              {{ tooltipItem.display_institute_name }}
                            </p>

                            <p class="text-[10px] text-gray-600">
                              {{ tooltipItem.display_program_name }}
                              ({{ tooltipItem.display_program_code }})
                            </p> -->

                            <p class="font-semibold text-gray-800">
                              {{ tooltipItem.display_program_code }}-{{
                                tooltipItem.set_name
                              }}
                            </p>
                            <p class="text-[10px] text-gray-500">
                              Class Size: {{ tooltipItem.class_size }}
                            </p>
                          </div>
                        </template>
                      </div>
                    </div>

                    <!-- Details Grid -->
                    <div class="grid grid-cols-2 gap-2">
                      <div class="rounded-lg bg-gray-50 px-2.5 py-2">
                        <p class="text-[9px] font-semibold uppercase text-gray-400">
                          Room
                        </p>
                        <p class="mt-0.5 font-semibold text-gray-800">
                          {{ tooltipItem.room_name || "TBA" }}
                        </p>
                      </div>

                      <div class="rounded-lg bg-gray-50 px-2.5 py-2">
                        <p class="text-[9px] font-semibold uppercase text-gray-400">
                          Day
                        </p>
                        <p class="mt-0.5 font-semibold text-gray-800">
                          {{ tooltipItem.day || "-" }}
                        </p>
                      </div>

                      <div class="rounded-lg bg-gray-50 px-2.5 py-2 col-span-2">
                        <p class="text-[9px] font-semibold uppercase text-gray-400">
                          Time
                        </p>
                        <p class="mt-0.5 font-semibold text-gray-800">
                          {{ formatTime(tooltipItem.start_hour) }} –
                          {{
                            formatTime(
                              tooltipItem.start_hour + Number(tooltipItem.duration)
                            )
                          }}
                        </p>
                      </div>

                      <div class="rounded-lg bg-gray-50 px-2.5 py-2">
                        <p class="text-[9px] font-semibold uppercase text-gray-400">
                          Type
                        </p>
                        <p class="mt-0.5 font-semibold text-gray-800">
                          {{ tooltipItem.type || "-" }}
                        </p>
                      </div>

                      <div class="rounded-lg bg-gray-50 px-2.5 py-2">
                        <p class="text-[9px] font-semibold uppercase text-gray-400">
                          Campus
                        </p>
                        <p class="mt-0.5 font-semibold text-gray-800 truncate">
                          {{ getCollegeBranchName(tooltipItem.college_branch_id) }}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div
        v-if="!showFacultyTable && totalCardPages > 1"
        class="flex justify-center items-center gap-2 mt-4 w-full"
      >
        <button
          @click="currentCardPage--"
          :disabled="currentCardPage === 1"
          class="px-3 py-1 rounded-lg bg-gray-200 disabled:opacity-50"
        >
          &lt;
        </button>

        <span class="text-sm font-medium text-gray-600">
          Page {{ currentCardPage }} of {{ totalCardPages }}
        </span>

        <button
          @click="currentCardPage++"
          :disabled="currentCardPage === totalCardPages"
          class="px-3 py-1 rounded-lg bg-gray-200 disabled:opacity-50"
        >
          &gt;
        </button>
      </div>
    </div>
  </div>
  <!-- Conflict Modal -->
  <ConflictModal
    :visible="conflictModalVisible"
    :schedule="selectedSchedule"
    :conflicts="conflictRecords"
    @close="conflictModalVisible = false"
  />

  <!-- JOIN VALIDATION MODAL -->
  <JoinValidationModal
    :visible="joinValidationModalVisible"
    :pendingJoinRecord="pendingJoinRecord"
    :pendingJoinTargets="pendingJoinTargets"
    @cancel="cancelJoin"
    @confirm="confirmJoin"
  />

  <!-- Unjoin Confirmation Modal -->
  <UnjoinModal
    :visible="unjoinModalVisible"
    @close="cancelUnjoin"
    @confirm="confirmUnjoin"
  />

  <!-- TODO  Edit Instructor Modal -->
  <editSchedule
    :show="showEditModal"
    :instructorData="editInstructorData"
    @close="showEditModal = false"
    @saved="handleModalSaved"
    @refresh="fetchFinalSchedules"
    @deleted="handleDeletedSchedule"
  />
</template>

<script>
import axios from "axios";
// import icon from "@/assets/icon.vue";
import { useFetchDataStore } from "@/store/fetch-data-store";
import editSchedule from "../modals/edit-schedule.vue";
import { toast } from "vue3-toastify";
import FacultyTopControls from "../faculty-components/faculty-top-controls.vue";
import ConflictModal from "../faculty-components/conflict-modal.vue";
import UnjoinModal from "../faculty-components/unjoin-validation-modal.vue";
import JoinValidationModal from "../faculty-components/join-validation-modal.vue";
export default {
  name: "FacultySchedule",
  components: {
    // icon,
    editSchedule,
    FacultyTopControls,
    ConflictModal,
    UnjoinModal,
    JoinValidationModal,
  },
  data() {
    return {
      joinGroupCounter: 1,
      user: {},
      isJoined: false,
      groupedSchedule: {},
      filteredGroupedSchedule: {},
      finalSchedules: [],
      loading: false,
      error: null,
      showFacultyTable: false,
      selectedInstructor: null,
      selectedInstituteId: "",
      selectedProgramId: "",
      confirmSaveModal: false,
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

      currentPage: 1,
      itemsPerPage: 10,
      timeSlotHeight: 60,
      pageWindow: 3,
      schoolYears: [],
      swapSelection: [],
      showEditModal: false,
      editInstructorData: [],
      compareInstructorA: "",
      compareInstructorB: "",
      showCompareView: false,
      showCompareSelection: false,
      conflictModalVisible: false,
      scheduleTooltipVisible: false,
      tooltipItem: null,
      tooltipX: 0,
      tooltipY: 0,
      draggedRecord: null,
      selectedSchedule: null,
      conflictRecords: [],
      visibleCardCount: 6,
      currentCardPage: 1,
      cardsPerPage: 6,
      joinValidationModalVisible: false,
      joinTargetRecord: null,
      joinEligibleRecords: [],
      pendingJoinRecord: null,
      pendingJoinTargets: [],
      isDragging: false,
      unjoinModalVisible: false,
      unjoinTargetRecord: null,
      scheduleIndex: {
        byDay: {},
        byFaculty: {},
        byRoom: {},
        byClass: {},
      },
      joinIndex: {},
      searchQuery: "",
    };
  },

  computed: {
    filteredBySearch() {
      if (!this.searchQuery) return this.filteredGroupedSchedule;

      const q = this.searchQuery.toLowerCase();

      return Object.fromEntries(
        Object.entries(this.filteredGroupedSchedule).filter(
          ([name, schedules]) =>
            name.toLowerCase().includes(q) ||
            schedules.some((s) =>
              [s.course_code, s.room_name, s.set_name, s.day]
                .join(" ")
                .toLowerCase()
                .includes(q)
            )
        )
      );
    },
    collegeBranches() {
      const store = useFetchDataStore();
      return store.college_branch || [];
    },
    scheduleIndexByDay() {
      const map = {};
      this.finalSchedules.forEach((s) => {
        if (!map[s.day]) map[s.day] = [];
        map[s.day].push(s);
      });
      return map;
    },
    isDraggable(record) {
      // If Join is active and class size >= 30 → not draggable
      return !(this.isJoined && Number(record.class_size) >= 30);
    },
    paginatedFacultyCards() {
      const entries = Object.entries(this.filteredBySearch); // ✅ FIXED

      if (this.showCompareView) {
        return Object.fromEntries(entries);
      }

      const start = (this.currentCardPage - 1) * this.cardsPerPage;
      const end = start + this.cardsPerPage;

      return Object.fromEntries(entries.slice(start, end));
    },
    totalCardPages() {
      return Math.ceil(Object.keys(this.filteredBySearch).length / this.cardsPerPage);
    },
    paginatedSource() {
      if (!this.searchQuery) return this.filteredGroupedSchedule;

      const q = this.searchQuery.toLowerCase();
      return Object.fromEntries(
        Object.entries(this.filteredGroupedSchedule).filter(([name]) =>
          name.toLowerCase().includes(q)
        )
      );
    },
    visibleFacultyCards() {
      return Object.entries(this.filteredBySearch).slice(0, this.visibleCardCount);
    },

    hasMoreCards() {
      return Object.keys(this.filteredBySearch).length > this.visibleCardCount;
    },
    coursesList() {
      const store = useFetchDataStore();
      return store.courses || [];
    }, // Total units per faculty
    facultyTotalUnits() {
      const result = {};

      Object.entries(this.filteredGroupedSchedule).forEach(([faculty, schedules]) => {
        let totalUnits = 0;

        // prevent duplicate counting
        const counted = new Set();

        schedules.forEach((sched) => {
          const key = `${sched.set_name}-${sched.course_code}`;

          // skip if already counted
          if (counted.has(key)) return;

          counted.add(key);

          const course = this.coursesList.find(
            (c) => c.course_code === sched.course_code
          );

          if (!course) return;

          const lec = Number(course.course_lec || 0);
          const lab = Number(course.course_lab || 0);

          totalUnits += lec + lab;
        });

        result[faculty] = {
          totalUnits: Number(totalUnits.toFixed(2)),
        };
      });

      return result;
    },

    uniqueInstitutes() {
      const store = useFetchDataStore();
      const institutes = store.institutes || [];
      return Array.from(new Set(this.finalSchedules.map((s) => s.institute_id))).map(
        (id) => {
          const inst = institutes.find((i) => i.institute_id === id);
          return inst
            ? { id, name: inst.institute_name }
            : { id, name: `Institute ${id}` };
        }
      );
    },
    // Map program IDs to their names (filtered by selectedInstituteId if any)
    filteredPrograms() {
      const store = useFetchDataStore();
      const programs = store.programs || [];

      const programIds = Array.from(
        new Set(
          this.finalSchedules
            .filter((s) =>
              this.selectedInstituteId
                ? String(s.institute_id) === String(this.selectedInstituteId)
                : true
            )
            .map((s) => s.program_id)
        )
      );

      return programIds.map((id) => {
        const prog = programs.find((p) => String(p.program_id) === String(id));
        return prog ? { id, name: prog.program_code } : { id, name: `Program ${id}` };
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
    totalPages() {
      return Math.ceil(Object.keys(this.filteredBySearch).length / this.itemsPerPage);
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
    pageNumbers() {
      let pages = [];
      const halfWindow = Math.floor(this.pageWindow / 2);
      let start = Math.max(1, this.currentPage - halfWindow);
      let end = Math.min(this.totalPages, start + this.pageWindow - 1);

      // Adjust start if not enough pages at the end
      start = Math.max(1, end - this.pageWindow + 1);

      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    },

    paginatedFaculty() {
      const entries = Object.entries(this.filteredBySearch);

      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;

      return Object.fromEntries(entries.slice(start, end));
    },

    searchedFaculty() {
      if (!this.searchQuery) return this.filteredGroupedSchedule;
      const query = this.searchQuery.toLowerCase();
      return Object.fromEntries(
        Object.entries(this.filteredGroupedSchedule).filter(([name]) =>
          name.toLowerCase().includes(query)
        )
      );
    },
  },

  watch: {
    selectedInstituteId() {
      this.filterSchedules();
      this.selectedProgramId = "";
    },
    selectedProgramId() {
      this.filterSchedules();
    },
  },

  methods: {
    canEditSchedule(schedule) {
      if (!schedule) return false;

      // ✅ Newly added schedules always editable
      if (schedule.isNew) return true;

      // ================================
      // PROGRAM CHAIRPERSON
      // ONLY own institute + own program
      // ================================
      if (this.user.role === "Program Chairperson") {
        const sameClassProgram =
          Number(schedule.class_program_id) === Number(this.user.program_id);

        const sameClassInstitute =
          Number(schedule.class_institute_id) === Number(this.user.institute_id);

        return sameClassProgram && sameClassInstitute;
      }

      // ==========================================
      // DEPARTMENT CHAIRPERSON
      // Can edit EVERYTHING
      // EXCEPT own exact institute + program
      // ==========================================
      if (this.user.role === "Department Chairperson") {
        const sameClassProgram =
          Number(schedule.class_program_id) === Number(this.user.program_id);

        const sameClassInstitute =
          Number(schedule.class_institute_id) === Number(this.user.institute_id);

        // ❌ lock ONLY own exact program
        return !(sameClassProgram && sameClassInstitute);
      }

      // ✅ Other roles
      return true;
    },
    async fetchCollegeBranch() {
      const store = useFetchDataStore();
      await store.fetchCollegeBranch();

      this.collegeBranches = store.collegeBranches || [];
    },
    getCollegeBranchName(branchId) {
      const branch = this.collegeBranches.find(
        (b) => Number(b.college_branch_id) === Number(branchId)
      );

      return branch ? branch.college_branch_name : `Branch ${branchId}`;
    },
    buildJoinIndex() {
      const index = {};

      this.finalSchedules.forEach((r) => {
        const year = r.set_name?.split(" ")[0] || "";

        const key = `${r.course_code}|${r.type}|${r.semester}|${year}`;

        if (!index[key]) index[key] = [];
        index[key].push(r);
      });

      this.joinIndex = index;
    },
    rebuildAllIndexes() {
      this.groupedSchedule = this.groupByInstructor(this.finalSchedules);
      this.filteredGroupedSchedule = { ...this.groupedSchedule };

      this.buildScheduleIndex();
      this.buildJoinIndex();
    },
    handleUnjoin(record) {
      if (!record.is_joined || !record.join_group_id) return;

      // Show modal instead of alert
      this.unjoinTargetRecord = record;
      this.unjoinModalVisible = true;
    },

    async confirmUnjoin() {
      if (!this.unjoinTargetRecord) return;

      const record = this.unjoinTargetRecord;

      // Get all records in the same join group
      const groupRecords = this.finalSchedules.filter(
        (r) => r.join_group_id === record.join_group_id
      );

      try {
        await Promise.all(
          groupRecords.map((r) =>
            axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${r.id}`,
              {
                is_joined: false,
                join_group_id: null,
                joined_with: [],
              }
            )
          )
        );

        // Update local state
        this.finalSchedules = this.finalSchedules.map((r) => {
          if (r.join_group_id === record.join_group_id) {
            return {
              ...r,
              is_joined: false,
              join_group_id: null,
              joined_with: [],
            };
          }
          return r;
        });

        this.groupedSchedule = this.groupByInstructor(this.finalSchedules);
        this.filteredGroupedSchedule = { ...this.groupedSchedule };
        this.rebuildAllIndexes();
        // ✅ Automatically update global join mode if no more joined records
        const anyJoined = this.finalSchedules.some((r) => r.is_joined);
        this.isJoined = anyJoined;

        toast.success("Schedules successfully unjoined!");
      } catch (err) {
        console.error(err);
        toast.error("Failed to unjoin schedules.");
      } finally {
        this.unjoinModalVisible = false;
        this.unjoinTargetRecord = null;
      }
    },

    cancelUnjoin() {
      this.unjoinModalVisible = false;
      this.unjoinTargetRecord = null;
    },
    async confirmJoin() {
      if (!this.pendingJoinRecord || !this.pendingJoinTargets.length) return;

      const baseRecord = this.pendingJoinRecord;

      // Helper function to determine if two schedules can join
      const canJoin = (a, b) => {
        if (!a || !b) return false;

        const baseSet = a.set_name?.split(" ")[0];
        const targetSet = b.set_name?.split(" ")[0];
        const modeCompatible = a.mode?.toLowerCase() === b.mode?.toLowerCase();

        return (
          a.id !== b.id &&
          a.course_code === b.course_code &&
          a.type === b.type &&
          a.semester === b.semester &&
          baseSet === targetSet &&
          Number(a.class_size) < 30 &&
          Number(b.class_size) < 30 &&
          modeCompatible &&
          !b.is_joined
        );
      };

      // 🔥 STEP 1: Filter only truly joinable targets
      const validTargets = this.pendingJoinTargets.filter((target) =>
        canJoin(baseRecord, target)
      );

      if (!validTargets.length) {
        toast.error("No valid schedules to join based on the rules.");
        this.resetJoinState();
        return;
      }

      // 🔥 STEP 2: Combine schedules (base + valid targets)
      const allToJoin = [baseRecord, ...validTargets];

      const finalMode = baseRecord.mode?.toLowerCase();
      const joinGroupId = baseRecord.id;
      const joinedIds = allToJoin.map((s) => s.id);
      const totalStudents = allToJoin.reduce(
        (sum, s) => sum + Number(s.class_size || 0),
        0
      );

      allToJoin.forEach((s) => {
        s.day = baseRecord.day;
        s.start_hour = baseRecord.start_hour;
        s.duration = baseRecord.duration;
        s.mode = finalMode;

        if (finalMode === "face to face") {
          s.room_id = baseRecord.room_id || null;
          s.room_name = baseRecord.room_name || null;
          s.room_capacity = baseRecord.room_capacity || null;
          s.room_type = baseRecord.room_type || null;
        } else {
          s.room_id = null;
          s.room_name = null;
          s.room_capacity = null;
          s.room_type = null;
        }

        s.join_group_id = joinGroupId;
        s.is_joined = true;
        s.joined_with = joinedIds.filter((id) => id !== s.id);
      });

      try {
        await Promise.all(
          allToJoin.map((s) =>
            axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${s.id}`,
              {
                day: s.day,
                start_hour: s.start_hour,
                duration: s.duration,
                mode: s.mode,
                room_id: s.room_id,
                room_name: s.room_name,
                room_capacity: s.room_capacity,
                room_type: s.room_type,
                join_group_id: s.join_group_id,
                is_joined: s.is_joined,
                joined_with: s.joined_with,
              }
            )
          )
        );

        toast.success(`Classes successfully joined! Total students: ${totalStudents}`);
        this.rebuildAllIndexes();
        await this.fetchFinalSchedules();
      } catch (error) {
        console.error(error);
        toast.error("Failed to save joined schedules.");
      }

      this.resetJoinState();
    },
    cancelJoin() {
      this.resetJoinState();
    },
    resetJoinState() {
      this.pendingJoinRecord = null;
      this.pendingJoinTargets = [];
      this.joinValidationModalVisible = false;
    },
    async saveScheduleMove(record) {
      try {
        await axios.patch(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${record.id}`,
          {
            faculty_id: record.faculty_id,
            faculty_name: record.faculty_name,
            day: record.day,
            start_hour: record.start_hour,
            duration: record.duration,
            room_id: record.room_id,
            room_name: record.room_name,
            mode: record.mode,
            type: record.type,
          }
        );

        // toast.success("Schedule moved successfully!");
        await this.fetchFinalSchedules();
      } catch (error) {
        console.error(error);
        toast.error("Failed to save schedule.");
      }
    },
    getJoinableSchedules(baseRecord) {
      if (!baseRecord) return [];

      const year = baseRecord.set_name?.split(" ")[0] || "";
      const key = `${baseRecord.course_code}|${baseRecord.type}|${baseRecord.semester}|${year}`;

      const possible = this.joinIndex[key] || [];

      const baseMode = baseRecord.mode?.toLowerCase();

      return possible.filter((r) => {
        if (r.id === baseRecord.id) return false;
        if (r.is_joined) return false;

        if (Number(r.class_size) >= 30) return false;
        if (Number(baseRecord.class_size) >= 30) return false;

        if (r.mode?.toLowerCase() !== baseMode) return false;

        return true;
      });
    },
    canJoin(recordA, recordB) {
      if (!recordA || !recordB) return false;

      // Use full set_name (year + section) as group identifier
      const getGroupId = (set_name) => set_name?.trim() || "";

      const baseGroup = getGroupId(recordA.set_name);
      const targetGroup = getGroupId(recordB.set_name);

      // Both classes must be below 30 students
      const classSizeCheck =
        Number(recordA.class_size) < 30 && Number(recordB.class_size) < 30;

      // Must be the same mode to join
      const sameMode = recordA.mode?.toLowerCase() === recordB.mode?.toLowerCase();

      return (
        recordA.id !== recordB.id &&
        recordA.course_code === recordB.course_code &&
        recordA.type === recordB.type && // Lecture ↔ Lecture, Lab ↔ Lab
        recordA.semester === recordB.semester &&
        baseGroup === targetGroup && // Only same class/set
        classSizeCheck &&
        sameMode && // ✅ Ensure modes match exactly
        !recordB.is_joined // cannot join already joined
      );
    },
    getConflictsForDrag(record, targetInstructor, targetDay, targetStartHour) {
      const clonedRecord = { ...record };
      clonedRecord.faculty_name = targetInstructor;
      clonedRecord.day = targetDay;
      clonedRecord.start_hour = targetStartHour;

      return this.getConflictingRecords(clonedRecord);
    },
    showScheduleTooltip(event, item) {
      const tooltipWidth = 260;
      const tooltipHeight = 160;

      const padding = 20;

      let x = event.clientX + 15;
      let y = event.clientY + 15;

      const screenWidth = window.innerWidth;
      const screenHeight = window.innerHeight;

      // Prevent overflow on right side
      if (x + tooltipWidth + padding > screenWidth) {
        x = event.clientX - tooltipWidth - 15;
      }

      // Prevent overflow bottom
      if (y + tooltipHeight + padding > screenHeight) {
        y = event.clientY - tooltipHeight - 15;
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
    getConflictingRecords(record) {
      if (!record || record.start_hour == null || !record.duration) return [];

      const recordStart = this.normalizeHour(record.start_hour);
      const recordEnd = recordStart + Number(record.duration);

      const sameDaySchedules = this.scheduleIndex.byDay[record.day] || [];

      return sameDaySchedules
        .filter((r) => {
          if (!r || r.id === record.id) return false;

          if (
            record.is_joined &&
            r.is_joined &&
            record.join_group_id &&
            r.join_group_id &&
            record.join_group_id === r.join_group_id
          ) {
            return false;
          }

          const rStart = this.normalizeHour(r.start_hour);
          const rEnd = rStart + Number(r.duration);

          if (rStart == null || rEnd == null) return false;

          const overlaps = Math.max(rStart, recordStart) < Math.min(rEnd, recordEnd);
          if (!overlaps) return false;

          const sameFaculty =
            (r.faculty_id && record.faculty_id && r.faculty_id === record.faculty_id) ||
            (r.faculty_name &&
              record.faculty_name &&
              r.faculty_name.trim().toLowerCase() ===
                record.faculty_name.trim().toLowerCase());

          const sameRoom =
            r.room_id &&
            record.room_id &&
            r.room_id === record.room_id &&
            r.mode?.toLowerCase() === "face to face" &&
            record.mode?.toLowerCase() === "face to face";

          const sameClass =
            r.class_id && record.class_id && r.class_id === record.class_id;

          const sameOnlineSection =
            record.mode?.toLowerCase() === "online" &&
            r.mode?.toLowerCase() === "online" &&
            r.set_name === record.set_name &&
            r.program_id === record.program_id &&
            Number(r.college_branch_id) === Number(record.college_branch_id);

          return sameFaculty || sameRoom || sameClass || sameOnlineSection;
        })
        .map((r) => {
          const reason = [];

          const sameFaculty =
            (r.faculty_id && record.faculty_id && r.faculty_id === record.faculty_id) ||
            (r.faculty_name &&
              record.faculty_name &&
              r.faculty_name.trim().toLowerCase() ===
                record.faculty_name.trim().toLowerCase());

          if (sameFaculty) {
            reason.push("Same faculty assigned to overlapping schedules");
          }

          if (
            r.room_id &&
            record.room_id &&
            r.room_id === record.room_id &&
            r.mode?.toLowerCase() === "face to face" &&
            record.mode?.toLowerCase() === "face to face"
          ) {
            reason.push("Same room, same day, and overlapping time");
          }

          if (r.class_id && record.class_id && r.class_id === record.class_id) {
            reason.push("Same class/section has overlapping schedules");
          }

          if (
            record.mode?.toLowerCase() === "online" &&
            r.mode?.toLowerCase() === "online" &&
            r.set_name === record.set_name &&
            r.program_id === record.program_id &&
            Number(r.college_branch_id) === Number(record.college_branch_id)
          ) {
            reason.push(
              "ONLINE conflict: Same program section cannot attend two online classes at the same time"
            );
          }

          if (!reason.length) return null;

          return {
            ...r,
            reason: reason.join(", "),
          };
        })
        .filter(Boolean);
    },
    //   if (!record || record.start_hour == null || !record.duration) return [];

    //   const recordStart = this.normalizeHour(record.start_hour);
    //   const recordEnd = recordStart + Number(record.duration);

    //   const sameDaySchedules = this.scheduleIndex.byDay[record.day] || [];

    //   return sameDaySchedules
    //     .filter((r) => {
    //       if (!r || r.id === record.id) return false;

    //       // Ignore same join group
    //       if (
    //         record.is_joined &&
    //         r.is_joined &&
    //         record.join_group_id &&
    //         r.join_group_id &&
    //         record.join_group_id === r.join_group_id
    //       ) {
    //         return false;
    //       }

    //       const rStart = this.normalizeHour(r.start_hour);
    //       const rEnd = rStart + Number(r.duration);

    //       if (rStart == null || rEnd == null) return false;

    //       // Check time overlap first
    //       const overlaps = Math.max(rStart, recordStart) < Math.min(rEnd, recordEnd);

    //       if (!overlaps) return false;

    //       // ✅ 1. FACULTY CONFLICT (always conflict)
    //       const sameFaculty =
    //         (r.faculty_id && record.faculty_id && r.faculty_id === record.faculty_id) ||
    //         (r.faculty_name &&
    //           record.faculty_name &&
    //           r.faculty_name.trim().toLowerCase() ===
    //             record.faculty_name.trim().toLowerCase());

    //       if (sameFaculty) {
    //         return true;
    //       }

    //       // ✅ 2. ROOM CONFLICT (Face to Face only)
    //       if (
    //         r.room_id &&
    //         record.room_id &&
    //         r.room_id === record.room_id &&
    //         r.mode?.toLowerCase() === "face to face" &&
    //         record.mode?.toLowerCase() === "face to face"
    //       ) {
    //         if (!this.isJoined || r.faculty_id === record.faculty_id) {
    //           return true;
    //         }
    //       }

    //       // ✅ 3. CLASS CONFLICT
    //       if (r.class_id && record.class_id && r.class_id === record.class_id) {
    //         return true;
    //       }

    //       // ✅ 4. ONLINE SECTION CONFLICT (NEW RULE)
    //       if (
    //         record.mode?.toLowerCase() === "online" &&
    //         r.mode?.toLowerCase() === "online" &&
    //         r.set_name &&
    //         record.set_name &&
    //         r.set_name === record.set_name
    //       ) {
    //         return true;
    //       }

    //       return false;
    //     })
    //     .map((r) => {
    //       let reason = "";

    //       // Faculty conflict
    //       if (
    //         (r.faculty_id && record.faculty_id && r.faculty_id === record.faculty_id) ||
    //         (r.faculty_name &&
    //           record.faculty_name &&
    //           r.faculty_name.trim().toLowerCase() ===
    //             record.faculty_name.trim().toLowerCase())
    //       ) {
    //         reason =
    //           "Same faculty assigned to overlapping schedules (Mode does not matter)";
    //       }

    //       // Room conflict
    //       else if (
    //         r.room_id === record.room_id &&
    //         r.mode?.toLowerCase() === "face to face" &&
    //         record.mode?.toLowerCase() === "face to face"
    //       ) {
    //         reason = "Same room, same day, and overlapping time (Face-to-Face)";
    //       }

    //       // Class conflict
    //       else if (r.class_id === record.class_id) {
    //         reason = "Same class/section has overlapping schedules";
    //       }

    //       // ✅ Online conflict
    //       //   else if (
    //       //     record.mode?.toLowerCase() === "online" &&
    //       //     r.mode?.toLowerCase() === "online" &&
    //       //     r.set_name === record.set_name &&
    //       //     r.program_id === record.program_id &&
    //       //     Number(r.college_branch_id) === Number(record.college_branch_id)
    //       //   ) {
    //       //     reason =
    //       //       "ONLINE conflict: Same section cannot attend two online classes at the same time.";
    //       //   }

    //       //   return { ...r, reason };
    //       // });

    //       // ✅ ONLINE CONFLICT (same program + same section only)
    //       if (
    //         (record.room_name || "").toLowerCase() === "online" &&
    //         (r.mode || "").toLowerCase() === "online" &&
    //         r.set_name === record.set_name &&
    //         r.program_id === record.program_id &&
    //         r.college_branch_id === record.college_branch_id &&
    //         r.college_branch_id === record.college_branch_id
    //       ) {
    //         reason.push(
    //           "ONLINE conflict: Same program section cannot attend two online classes at the same time."
    //         );
    //       }

    //       if (!reason.length) return null;

    //       return { ...r, reason: reason.join(", ") };
    //     })
    //     .filter(Boolean);
    // },

    hasRoomConflict(record) {
      return this.getConflictingRecords(record).length > 0;
    }, // Open the conflict modal for a record
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

    toggleShowCompareSelection() {
      this.showCompareSelection = !this.showCompareSelection;
    },
    backFromCompare() {
      this.filteredGroupedSchedule = { ...this.groupedSchedule };
      this.compareInstructorA = "";
      this.compareInstructorB = "";
      this.showCompareView = false;
      this.showFacultyTable = false;
      this.showCompareSelection = false;
    },
    showCompareFacultyCards() {
      if (!this.compareInstructorA || !this.compareInstructorB) return;

      this.filteredGroupedSchedule = {
        [this.compareInstructorA]: this.groupedSchedule[this.compareInstructorA] || [],
        [this.compareInstructorB]: this.groupedSchedule[this.compareInstructorB] || [],
      };

      this.showFacultyTable = false;
      this.showCompareView = true;

      // ✅ RESET CARD PAGINATION
      this.currentCardPage = 1;
    },
    openEditInstructorModal(instructor) {
      // Send fresh copies of schedules to modal
      this.editInstructorData = (this.groupedSchedule[instructor] || []).map((r) => ({
        ...r,
      }));
      this.showEditModal = true;
    },
    handleModalSaved(updatedInstructorSchedules) {
      updatedInstructorSchedules.forEach((updated) => {
        const index = this.finalSchedules.findIndex((s) => s.id === updated.id);
        if (index > -1) {
          Object.assign(this.finalSchedules[index], updated); // reactive in place
        } else {
          this.finalSchedules.push(updated);
        }
      });

      // Only update groupedSchedule for affected instructors
      const affectedInstructors = Array.from(
        new Set(updatedInstructorSchedules.map((u) => u.faculty_name))
      );
      affectedInstructors.forEach((inst) => {
        this.groupedSchedule[inst] = this.finalSchedules.filter(
          (s) => s.faculty_name === inst
        );
      });

      // Update filteredGroupedSchedule only if necessary
      if (!this.showCompareView) {
        affectedInstructors.forEach((inst) => {
          this.filteredGroupedSchedule[inst] = this.groupedSchedule[inst];
        });
      }
    },
    handleDeletedSchedule(deletedId) {
      this.finalSchedules = this.finalSchedules.filter((s) => s.id !== deletedId);
      this.groupedSchedule = this.groupByInstructor(this.finalSchedules);
      this.filterSchedules();
    },
    closeEditInstructorModal() {
      this.showEditModal = false;
      this.editInstructorData = {};
    },

    onDragOver(event, instructor, day, slotStart) {
      if (!this.draggedRecord) return;

      requestAnimationFrame(() => {
        this.conflictPreview = this.getConflictsForDrag(
          this.draggedRecord,
          instructor,
          day,
          slotStart
        );
      });
    },
    onDragStart(event, record) {
      // Block large classes if Join is active
      if (this.isJoined && Number(record.class_size) >= 30) {
        toast.info("Cannot move classes with 30 or more students when Join is active.");
        event.preventDefault();
        return;
      }

      this.draggedRecord = { ...record };

      // ✅ Hide tooltip when dragging starts
      this.scheduleTooltipVisible = false;
      this.tooltipItem = null;

      event.dataTransfer.effectAllowed = "move";
    },

    async onDrop(event, targetInstructor, targetDay, targetStartHour) {
      if (!this.draggedRecord) return;
      // 🔒 BLOCK IF NO EDIT PERMISSION
      if (!this.canEditSchedule(this.draggedRecord)) {
        toast.error("This schedule is locked.");
        this.draggedRecord = null;
        return;
      }
      const baseRecord = this.draggedRecord;

      // 🔥 Join mode
      if (this.isJoined) {
        const joinable = this.getJoinableSchedules(baseRecord);

        if (joinable.length) {
          this.pendingJoinRecord = baseRecord;
          this.pendingJoinTargets = joinable;
          this.joinValidationModalVisible = true;
          this.draggedRecord = null;
          return; // wait for user confirmation
        }
      }

      // Determine records to move (single or joined)
      const recordsToMove =
        baseRecord.is_joined && baseRecord.join_group_id
          ? this.finalSchedules.filter(
              (r) => r.join_group_id === baseRecord.join_group_id
            )
          : [baseRecord];

      // Apply new position
      recordsToMove.forEach((r) => {
        r.faculty_name = targetInstructor;
        r.day = targetDay;
        r.start_hour = targetStartHour;
      });

      // Conflict check
      if (!this.isJoined) {
        for (const r of recordsToMove) {
          const conflicts = this.getConflictingRecords(r);
          if (conflicts.length) {
            this.selectedSchedule = r;
            this.conflictRecords = conflicts;
            this.conflictModalVisible = true;
            this.draggedRecord = null;
            return;
          }
        }
      }

      // Save
      try {
        await Promise.all(
          recordsToMove.map((r) =>
            axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${r.id}`,
              {
                faculty_id: r.faculty_id,
                faculty_name: r.faculty_name,
                day: r.day,
                start_hour: r.start_hour,
                duration: r.duration,
                room_id: r.room_id,
                room_name: r.room_name,
                mode: r.mode,
                type: r.type,
              }
            )
          )
        );
        // toast.success("Schedule moved successfully!");
        await this.fetchFinalSchedules();
      } catch (err) {
        console.error(err);
        toast.error("Failed to move schedule.");
      }

      this.draggedRecord = null;
    },

    async loadFetchData() {
      const store = useFetchDataStore();
      await store.fetchPrograms();
      await store.fetchInstitutes();
      await store.fetchCourses();
      await store.fetchCollegeBranch();
    },

    backToFacultyTable() {
      this.filteredGroupedSchedule = this.groupedSchedule;
      this.showFacultyTable = true;
      this.currentPage = 1;
    },

    normalizeHour(hour) {
      const h = Number(hour);
      if (Number.isNaN(h)) return null;
      return h; // ✅ already 24-hour based
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

    filterSchedules() {
      let filtered = { ...this.groupedSchedule };

      if (this.selectedInstituteId) {
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some(
              (s) => String(s.institute_id) === String(this.selectedInstituteId)
            )
          )
        );
      }

      if (this.selectedProgramId) {
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some((s) => String(s.program_id) === String(this.selectedProgramId))
          )
        );
      }

      this.filteredGroupedSchedule = filtered;
      this.currentPage = 1;
    },
    getScheduleForCell(slot, day, instructor) {
      const schedules = this.filteredGroupedSchedule[instructor] || [];
      const renderedGroups = new Set();

      return schedules.filter((item) => {
        if (item.day !== day) return false;

        const start = this.normalizeHour(item.start_hour);
        const end = start + Number(item.duration);
        const overlaps = end > slot.start && start < slot.end;
        if (!overlaps) return false;

        // 🔥 If joined → render only first occurrence
        if (item.is_joined && item.join_group_id) {
          if (renderedGroups.has(item.join_group_id)) {
            return false;
          }
          renderedGroups.add(item.join_group_id);
        }

        return true;
      });
    },
    getTypeColor(room_type) {
      if (!room_type) return "bg-green-100 border-green-400";
      const normalized = room_type.toLowerCase();
      if (normalized === "laboratory" || normalized === "lab") {
        return "bg-blue-100 border-blue-300";
      }
      return "bg-green-100 border-green-300";
    },

    viewFacultySchedule(instructor) {
      this.filteredGroupedSchedule = {
        [instructor]: this.groupedSchedule[instructor],
      };
      this.showFacultyTable = false;
    },

    changePage(page) {
      if (page >= 1 && page <= this.totalPages) this.currentPage = page;
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
    buildScheduleIndex() {
      const index = {
        byDay: {},
        byFaculty: {},
        byRoom: {},
        byClass: {},
      };

      this.finalSchedules.forEach((r) => {
        // Index by Day
        if (!index.byDay[r.day]) index.byDay[r.day] = [];
        index.byDay[r.day].push(r);

        // Index by Faculty
        if (!index.byFaculty[r.faculty_id]) index.byFaculty[r.faculty_id] = [];
        index.byFaculty[r.faculty_id].push(r);

        // Index by Room
        if (r.room_id) {
          if (!index.byRoom[r.room_id]) index.byRoom[r.room_id] = [];
          index.byRoom[r.room_id].push(r);
        }

        // Index by Class
        if (r.class_id) {
          if (!index.byClass[r.class_id]) index.byClass[r.class_id] = [];
          index.byClass[r.class_id].push(r);
        }
      });

      this.scheduleIndex = index;
    },

    async fetchClassSections() {
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/class/get-classes"
        );

        // classes under current user's institute/program
        this.sections = data.filter((cls) => {
          return (
            Number(cls.program_id) === Number(this.user.program_id) &&
            Number(cls.program?.institute_id) === Number(this.user.institute_id)
          );
        });
      } catch (err) {
        console.error(err);
      }
    },

    async fetchFinalSchedules() {
      this.loading = true;
      this.error = null;

      try {
        // ================================
        // FETCH SCHEDULES
        // ================================
        const { data: schedulesData } = await axios.get(
          process.env.VUE_APP_API_BASE_URL +
            "/final-generated-class-schedule/get-all-final-schedules",
          { withCredentials: true }
        );

        // ================================
        // FETCH CLASS SECTIONS
        // ================================
        const { data: classSections } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/class/get-classes",
          { withCredentials: true }
        );

        // ================================
        // CLASS MAP
        // ================================
        const classMap = {};

        classSections.forEach((cls) => {
          classMap[Number(cls.class_id)] = cls;
        });

        let schedules = schedulesData || [];

        // ================================
        // ATTACH CLASS / PROGRAM INFO
        // ================================
        schedules = schedules.map((s) => {
          const cls = classSections.find(
            (c) => Number(c.class_id) === Number(s.class_id)
          );

          return {
            ...s,

            classInfo: cls || null,

            // ====================================
            // FACULTY OWNER
            // original owner sa faculty
            // ====================================
            faculty_program_id: s.program_id || null,

            faculty_institute_id: s.institute_id || null,

            // ====================================
            // CLASS OWNER
            // gikan sa class/get-classes
            // ====================================
            class_program_id: cls?.program_id || null,

            class_institute_id: cls?.program?.institute_id || null,

            // ====================================
            // DISPLAY VALUES
            // ALWAYS gikan sa class/get-classes
            // ====================================
            // preserve original ownership
            program_id: s.program_id,
            institute_id: s.institute_id,

            // 🔥 DISPLAY ONLY
            display_program_code: cls?.program?.program_code || "Unknown Program",

            display_program_name: cls?.program?.program_name || "Unknown Program",

            display_institute_name:
              cls?.program?.institute?.institute_name || "Unknown Institute",

            display_institute_code: cls?.program?.institute?.institute_code || "",

            set_name: cls?.set_name || s.set_name,

            class_size: cls?.class_size || s.class_size,
          };
        });

        // ================================
        // PROGRAM CHAIRPERSON
        // show all schedules sa ilang faculty
        // ================================
        if (this.user.role === "Program Chairperson") {
          const ownedFacultyIds = [
            ...new Set(
              schedules
                .filter(
                  (s) =>
                    Number(s.faculty_program_id) === Number(this.user.program_id) &&
                    Number(s.faculty_institute_id) === Number(this.user.institute_id)
                )
                .map((s) => s.faculty_id)
            ),
          ];

          // show tanan schedules handled by their faculty
          schedules = schedules.filter((s) => ownedFacultyIds.includes(s.faculty_id));
        }

        // ================================
        // DEPARTMENT CHAIRPERSON
        // show all schedules sa ilang faculty
        // ================================
        else if (this.user.role === "Department Chairperson") {
          const ownedFacultyIds = [
            ...new Set(
              schedules
                .filter(
                  (s) =>
                    Number(s.faculty_program_id) === Number(this.user.program_id) &&
                    Number(s.faculty_institute_id) === Number(this.user.institute_id)
                )
                .map((s) => s.faculty_id)
            ),
          ];

          schedules = schedules.filter((s) => ownedFacultyIds.includes(s.faculty_id));
        }

        // ================================
        // SAVE
        // ================================
        this.finalSchedules = schedules;

        this.rebuildAllIndexes();
        this.changePage(1);
      } catch (err) {
        this.error = err.message || "Failed to fetch final schedules";

        console.error(err);
      } finally {
        this.loading = false;
      }
    },
    // Keep your existing groupByInstructor method
    groupByInstructor(schedules) {
      return schedules.reduce((acc, s) => {
        const instructor = s.faculty_name || "Unknown Faculty";
        if (!acc[instructor]) acc[instructor] = [];
        acc[instructor].push(s);
        return acc;
      }, {});
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
  },
  async mounted() {
    await this.fetchUser();
    await this.fetchClassSections();
    await this.loadFetchData();
    await this.fetchSchoolYears();
    await this.fetchFinalSchedules();
    await this.fetchCollegeBranch();
  },
};
</script>
