<template>
  <div
    class="w-[45vw] h-[47vh] bg-white border shadow-xl transition-all duration-300 flex flex-col justify-start rounded-xl overflow-hidden p-0.5"
  >
    <!-- Header -->
    <div
      class="flex items-center justify-between px-2 py-2 text-white bg-defaultGreen rounded-t-lg"
    >
      <h3 class="header1">Unscheduled Courses</h3>

      <input
        v-model="searchQuery"
        @input="changePage(1)"
        type="text"
        placeholder="Search course, type, SY..."
        class="rounded-lg border border-green-600 px-4 py-2 text-xs w-64 focus:outline-none focus:ring-2 focus:ring-green-400 text-gray-700"
      />
    </div>

    <!-- Body -->
    <div class="flex-1 overflow-y-auto">
      <div class="w-full h-[35vh] border bg-white overflow-auto">
        <table class="min-w-full text-xs text-gray-700">
          <thead class=" ">
            <tr>
              <th
                class="px-4 py-3 text-left bg-gray-50 text-defaultGreen font-semibold"
              >
                Set
              </th>
              <th
                class="px-4 py-3 text-left bg-gray-50 text-defaultGreen font-semibold"
              >
                Course
              </th>
              <th
                class="px-4 py-3 text-center bg-gray-50 text-defaultGreen font-semibold"
              >
                Type
              </th>
              <th
                class="px-4 py-3 text-center bg-gray-50 text-defaultGreen font-semibold"
              >
                Semester
              </th>
              <th
                class="px-4 py-3 text-center w-[25%] bg-gray-50 text-defaultGreen font-semibold"
              >
                Action
              </th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="item in paginatedData"
              :key="item.id"
              class="border-t hover:bg-green-50 transition"
            >
              <td class="px-4 py-3">
                {{ getSetName(item.class_id) || item.class_id }}
              </td>

              <td class="px-4 py-3 font-medium text-gray-800">
                {{ item.course_code }}
              </td>

              <td class="px-4 py-3 text-center">
                {{ item.type }}
              </td>

              <td class="px-4 py-3 text-center">
                {{ semesterLabel(item.semester) }}
              </td>

              <td class="px-4 py-3">
                <div class="flex items-center justify-center gap-2">
                  <button
                    @click="openDetailsModal(item)"
                    class="btn-see-details"
                  >
                    See Details
                  </button>

                  <button @click="openAssignModal(item)" class="btn-save">
                    Assign
                  </button>
                </div>
              </td>
            </tr>

            <tr v-if="paginatedData.length === 0">
              <td colspan="5" class="py-8">
                <div
                  class="flex justify-center items-center text-gray-400 text-xs"
                >
                  No unscheduled courses found
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4 text-xs mx-2">
        <div class="text-gray-700">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredData.length }} entries
        </div>

        <div class="flex items-center gap-1">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-2 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400 disabled:opacity-50"
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
            class="px-2 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400 disabled:opacity-50"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>

    <!-- Details Modal -->
    <div v-if="detailsModalVisible" class="modal-overlay">
      <div class="modal-wrapper">
        <div
          class="bg-white rounded-xl shadow-2xl w-[42vw] overflow-hidden border border-gray-100"
        >
          <!-- Header -->

          <div class="modal-header">
            <div class="flex items-center gap-3">
              <!-- Icon -->
              <div class="glass-container">
                <icon name="circle-add2" class="text-white" />
              </div>

              <!-- Title -->
              <div>
                <h2 class="text-lg font-semibold text-white">Course Detail</h2>

                <p class="text-xs text-green-100">View course details</p>
              </div>
            </div>

            <icon
              :name="'circle-close3'"
              @click="closeDetailsModal"
              class="close-button-header"
            />
          </div>

          <!-- Body -->
          <div class="p-5 space-y-5 max-h-[75vh] overflow-y-auto">
            <!-- Course Summary -->
            <div class="rounded-xl border border-gray-100 bg-gray-50 p-4">
              <div class="flex items-start justify-between gap-4">
                <div>
                  <p class="text-xs text-gray-500">Course</p>
                  <h2 class="text-lg font-bold text-gray-800">
                    {{ selectedCourse.course_code }}
                  </h2>
                  <p class="text-sm text-gray-600 mt-1">
                    {{ selectedCourse.course_title || "No course title" }}
                  </p>
                </div>

                <span
                  class="px-3 py-1 rounded-full bg-green-100 text-defaultGreen text-xs font-semibold"
                >
                  {{ selectedCourse.type }}
                </span>
              </div>
            </div>

            <!-- Full Details -->
            <div class="grid grid-cols-2 gap-3 text-xs">
              <div class="detail-card">
                <p class="detail-label">Set</p>
                <p class="detail-value">{{ selectedCourse.set_name }}</p>
              </div>

              <div class="detail-card">
                <p class="detail-label">Program</p>
                <p class="detail-value">
                  {{ selectedCourse.program_code || "N/A" }}
                </p>
              </div>

              <div class="detail-card">
                <p class="detail-label">Semester</p>
                <p class="detail-value">
                  {{ semesterLabel(selectedCourse.semester) }}
                </p>
              </div>

              <div class="detail-card">
                <p class="detail-label">School Year</p>
                <p class="detail-value">
                  {{ selectedCourse.school_year || "N/A" }}
                </p>
              </div>

              <div class="detail-card">
                <p class="detail-label">Hours</p>
                <p class="detail-value">
                  {{ selectedCourse.hours || "N/A" }}
                </p>
              </div>

              <div class="detail-card">
                <p class="detail-label">Mode</p>
                <p class="detail-value">
                  {{ selectedCourse.mode || "N/A" }}
                </p>
              </div>
            </div>

            <!-- Reason -->
            <div class="rounded-xl border border-red-100 bg-red-50 p-4">
              <p class="text-xs font-semibold text-red-700 mb-1">Reason</p>
              <p class="text-xs text-red-600 leading-relaxed">
                {{ selectedCourse.reason || "No reason provided" }}
              </p>
            </div>

            <!-- Assign Inside Details -->
            <div class="rounded-xl border border-gray-100 p-4 bg-white">
              <div class="flex items-center justify-between mb-3">
                <div>
                  <h3 class="font-semibold text-sm text-gray-800">
                    Assign Instructor
                  </h3>
                  <p class="text-xs text-gray-500">
                    You can assign directly here without going back.
                  </p>
                </div>
              </div>

              <div class="dropdown-container" ref="detailsInstructorDropdown">
                <label class="dropdown-label">Instructor:</label>

                <div class="dropdown-wrapper">
                  <input
                    v-model="searchInstructorQuery"
                    type="text"
                    placeholder="Search instructor..."
                    class="dropdown-input"
                    @focus="showInstructorDropdown = true"
                    @input="showInstructorDropdown = true"
                  />

                  <div v-if="showInstructorDropdown" class="dropdown-menu">
                    <div v-if="filteredInstructors.length">
                      <div
                        v-for="instr in filteredInstructors"
                        :key="instr.faculty_id"
                        class="dropdown-item"
                        @mousedown.prevent="selectInstructor(instr)"
                      >
                        {{ instr.faculty_name }}
                      </div>
                    </div>

                    <div v-else class="dropdown-empty">No instructor found</div>
                  </div>
                </div>
              </div>

              <div class="flex justify-end gap-2 mt-5">
                <button @click="closeDetailsModal" class="btn-cancel">
                  Close
                </button>

                <button @click="confirmAssign" class="btn-save">
                  Assign Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Existing Assign Modal -->
    <div v-if="assignModalVisible" class="modal-overlay">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <div class="flex items-center gap-3">
              <!-- Icon -->
              <div class="glass-container">
                <icon name="circle-add2" class="text-white" />
              </div>

              <!-- Title -->
              <div>
                <h2 class="text-lg font-semibold text-white">Assign Course</h2>

                <p class="text-xs text-green-100">
                  Select an instructor and assign a course.
                </p>
              </div>
            </div>

            <icon
              :name="'circle-close3'"
              @click="closeAssignModal"
              class="close-button-header"
            />
          </div>

          <div class="modal-body w-[25vw]">
            <p class="text-[13px]">
              Assign
              <span class="font-bold text-defaultGreen">
                {{ selectedCourse.course_code }}
              </span>
              to an instructor.
            </p>

            <div class="dropdown-container" ref="instructorDropdown">
              <label class="dropdown-label">Instructor:</label>

              <div class="dropdown-wrapper">
                <input
                  v-model="searchInstructorQuery"
                  type="text"
                  placeholder="Search instructor..."
                  class="dropdown-input"
                  @focus="showInstructorDropdown = true"
                  @input="showInstructorDropdown = true"
                />

                <div v-if="showInstructorDropdown" class="dropdown-menu">
                  <div v-if="filteredInstructors.length">
                    <div
                      v-for="instr in filteredInstructors"
                      :key="instr.faculty_id"
                      class="dropdown-item"
                      @mousedown.prevent="selectInstructor(instr)"
                    >
                      {{ instr.faculty_name }}
                    </div>
                  </div>

                  <div v-else>
                    <div class="dropdown-empty">No instructor found</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <button @click="closeAssignModal" class="btn-cancel">
                Cancel
              </button>
              <button @click="confirmAssign" class="btn-save">Assign</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Confirm Assign Modal -->
    <div
      v-if="showConfirmAssign"
      class="fixed inset-0 flex items-center justify-center bg-black/30 z-50"
    >
      <div class="bg-white rounded-2xl shadow-2xl p-6 w-[420px]">
        <!-- Header -->
        <div class="flex justify-between items-center border-b pb-3 mb-5">
          <div class="flex items-center gap-2">
            <icon
              name="exclamation-circle"
              class="w-7 h-7 p-1 rounded-full bg-green-100 text-defaultGreen"
            />

            <div>
              <h3 class="text-lg font-semibold text-gray-800">
                Confirm Assignment
              </h3>
              <p class="text-xs text-gray-500">Please confirm this action.</p>
            </div>
          </div>

          <button
            @click="cancelAssign"
            class="text-gray-400 hover:text-gray-600 transition"
          >
            ✕
          </button>
        </div>

        <!-- Content -->
        <div class="space-y-4">
          <p class="text-sm text-gray-600 leading-relaxed">
            Are you sure you want to assign
            <span class="font-semibold text-defaultGreen">
              {{ selectedCourse.course_code }}
            </span>
            to
            <span class="font-semibold text-defaultGreen">
              {{ searchInstructorQuery }}
            </span>
            ?
          </p>

          <div class="rounded-lg bg-amber-50 border border-amber-200 p-3">
            <div class="flex gap-2">
              <icon name="exclamation-circle" class="text-amber-600 mt-0.5" />

              <p class="text-xs text-amber-700">
                Once assigned, this course will be removed from the
                <strong>Unscheduled Courses</strong> list and opened in the
                schedule editor for further scheduling.
              </p>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex justify-center gap-2 mt-6 text-xs">
          <button @click="cancelAssign" class="btn-cancel">Cancel</button>

          <button @click="confirmAssignCourse" class="btn-save">
            Yes, Assign Course
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useFetchDataStore } from "@/store/fetch-data-store";
import axios from "axios";
import icon from "@/assets/icon.vue";

export default {
  name: "AssignCoursePage",

  components: {
    icon,
  },

  props: {
    closeAddSchedulePanel: {
      type: Function,
      required: true,
    },
  },

  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      showConfirmAssign: false,
      user: {},

      assignModalVisible: false,
      detailsModalVisible: false,

      selectedCourse: {},
      selectedInstructor: "",
      searchInstructorQuery: "",
      showInstructorDropdown: false,
    };
  },

  computed: {
    store() {
      return useFetchDataStore();
    },

    filteredInstructors() {
      const query = this.searchInstructorQuery?.toLowerCase() || "";

      return this.uniqueInstructors.filter((instr) =>
        instr.faculty_name?.toLowerCase().includes(query),
      );
    },

    sectionMap() {
      const map = {};

      (this.store.sections || []).forEach((sec) => {
        map[Number(sec.class_id)] = sec.set_name;
      });

      return map;
    },

    filteredData() {
      const query = this.searchQuery?.toLowerCase() || "";

      return (this.store.unscheduled_meetings || []).filter((item) => {
        const isSameProgram = this.user.program_id
          ? Number(item.program_id) === Number(this.user.program_id)
          : true;

        const matchesQuery =
          item.course_code?.toLowerCase().includes(query) ||
          item.course_title?.toLowerCase().includes(query) ||
          item.program_name?.toLowerCase().includes(query) ||
          item.program_code?.toLowerCase().includes(query) ||
          item.school_year?.toLowerCase().includes(query) ||
          item.type?.toLowerCase().includes(query) ||
          String(item.semester || "").includes(query) ||
          item.reason?.toLowerCase().includes(query);

        return isSameProgram && matchesQuery;
      });
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredData.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;
    },

    pageNumbers() {
      return Array.from({ length: this.totalPages }, (_, i) => i + 1);
    },

    startIndex() {
      return this.filteredData.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(
        this.currentPage * this.itemsPerPage,
        this.filteredData.length,
      );
    },

    uniqueInstructors() {
      if (!this.user.program_id) return [];

      const seen = new Set();

      return (this.store.final_schedules || [])
        .filter(
          (s) =>
            s.faculty_id &&
            Number(s.program_id) === Number(this.user.program_id),
        )
        .filter((s) => {
          if (seen.has(s.faculty_id)) return false;

          seen.add(s.faculty_id);
          return true;
        });
    },
  },

  methods: {
    confirmAssign() {
      if (!this.selectedInstructor) {
        return alert("Please select an instructor");
      }

      this.showConfirmAssign = true;
    },

    cancelAssign() {
      this.showConfirmAssign = false;
    },

    async confirmAssignCourse() {
      this.showConfirmAssign = false;
      await this.assignCourse();
    },
    handleClickOutside(event) {
      const instructorDropdown = this.$refs.instructorDropdown;
      const detailsInstructorDropdown = this.$refs.detailsInstructorDropdown;

      const clickedInsideAssign =
        instructorDropdown && instructorDropdown.contains(event.target);

      const clickedInsideDetails =
        detailsInstructorDropdown &&
        detailsInstructorDropdown.contains(event.target);

      if (!clickedInsideAssign && !clickedInsideDetails) {
        this.showInstructorDropdown = false;
      }
    },

    selectInstructor(instr) {
      this.selectedInstructor = instr.faculty_id;
      this.searchInstructorQuery = instr.faculty_name;
      this.showInstructorDropdown = false;
    },

    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },

    semesterLabel(sem) {
      return sem === "1" || sem === 1
        ? "1st Semester"
        : sem === "2" || sem === 2
        ? "2nd Semester"
        : sem;
    },

    getSetName(classId) {
      return this.sectionMap[Number(classId)] || "";
    },

    setSelectedCourse(item) {
      const courseInfo = this.store.courses?.find(
        (c) => Number(c.course_id) === Number(item.course_id),
      );

      const programInfo = this.store.programs?.find(
        (p) => Number(p.program_id) === Number(item.program_id),
      );

      this.selectedCourse = {
        ...item,
        course_code: item.course_code || courseInfo?.course_code || "Unknown",
        course_title: item.course_title || courseInfo?.course_title || "",
        program_code:
          item.program_code || programInfo?.program_code || "Unknown",
        program_name: item.program_name || programInfo?.program_name || "",
        set_name: this.getSetName(item.class_id) || item.class_id,
        hours: item.hours || "3h lec",
      };
    },

    openDetailsModal(item) {
      this.setSelectedCourse(item);

      this.detailsModalVisible = true;
      this.assignModalVisible = false;

      this.selectedInstructor = "";
      this.searchInstructorQuery = "";
      this.showInstructorDropdown = false;
    },

    closeDetailsModal() {
      this.detailsModalVisible = false;
      this.selectedCourse = {};
      this.selectedInstructor = "";
      this.searchInstructorQuery = "";
      this.showInstructorDropdown = false;
    },

    openAssignModal(item) {
      this.setSelectedCourse(item);

      this.assignModalVisible = true;
      this.detailsModalVisible = false;

      this.selectedInstructor = "";
      this.searchInstructorQuery = "";
      this.showInstructorDropdown = false;
    },

    closeAssignModal() {
      this.assignModalVisible = false;
      this.selectedCourse = {};
      this.selectedInstructor = "";
      this.searchInstructorQuery = "";
      this.showInstructorDropdown = false;
    },

    async assignCourse() {
      if (!this.selectedInstructor) {
        return alert("Please select an instructor");
      }

      // Keep the original unscheduled meeting ID
      const unscheduledId = this.selectedCourse.id;

      const course = {
        ...JSON.parse(JSON.stringify(this.selectedCourse)),
        faculty_id: this.selectedInstructor,
        faculty_name: this.getFacultyName(this.selectedInstructor),
        unscheduled_id: unscheduledId,
      };

      // Remove the original id since the schedule table has its own id
      delete course.id;

      const lectureMatch = course.hours?.match(/(\d+(\.\d+)?)h lec/);
      const labMatch = course.hours?.match(/(\d+(\.\d+)?)h lab/);

      const lectureDuration = lectureMatch ? parseFloat(lectureMatch[1]) : 3;
      const labDuration = labMatch ? parseFloat(labMatch[1]) : 3;

      const instituteId = this.getInstituteId(course.program_id);

      let payload = [];

      if (course.type === "Lecture+Lab") {
        payload = [
          {
            ...course,
            type: "Lecture",
            duration: lectureDuration,
            institute_id: instituteId,
            start_hour: 7,
            day: "Monday",
            time_slot: "7:00 AM - 10:00 AM",
            mode: course.mode || "online",
          },
          {
            ...course,
            type: "Laboratory",
            duration: labDuration,
            institute_id: instituteId,
            start_hour: 13,
            day: "Monday",
            time_slot: "1:00 PM - 4:00 PM",
            mode: "face to face",
          },
        ];
      } else {
        payload = [
          {
            ...course,
            duration: lectureDuration || labDuration,
            institute_id: instituteId,
            start_hour: 7,
            day: "Monday",
            time_slot: "7:00 AM - 10:00 AM",
            mode: course.mode || "face to face",
          },
        ];
      }

      // Delete from database
      await axios.delete(
        `${process.env.VUE_APP_API_BASE_URL}/unscheduled-meetings/${unscheduledId}`,
      );

      // Refresh the table
      await this.store.fetchUnscheduledMeetings();

      // Open Edit Schedule
      this.$emit("open-edit-schedule", payload);

      // Reset UI
      this.assignModalVisible = false;
      this.detailsModalVisible = false;
      this.selectedCourse = {};
      this.selectedInstructor = "";
      this.searchInstructorQuery = "";
      this.showInstructorDropdown = false;
    },

    async fetchUser() {
      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/auth/me`,
          {
            withCredentials: true,
          },
        );

        this.user = res.data || {};
      } catch {
        this.user = {};
      }
    },

    getInstituteId(programId) {
      const program = (this.store.programs || []).find(
        (p) => Number(p.program_id) === Number(programId),
      );

      return program ? program.institute_id : null;
    },

    getFacultyName(facultyId) {
      const user = (this.store.rawusers || []).find(
        (u) => Number(u.id) === Number(facultyId),
      );

      if (!user) return "Unknown Faculty";

      return [user.first_name, user.middle_name, user.last_name]
        .filter(Boolean)
        .join(" ");
    },
  },

  async mounted() {
    await this.fetchUser();

    await this.store.fetchUnscheduledMeetings();
    await this.store.fetchFinalSchedules();
    await this.store.fetchClassSections();
    await this.store.fetchRawUsers();

    if (this.store.fetchCourses) {
      await this.store.fetchCourses();
    }

    if (this.store.fetchPrograms) {
      await this.store.fetchPrograms();
    }

    document.addEventListener("click", this.handleClickOutside);
  },

  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>

<style scoped>
.detail-card {
  @apply rounded-xl border border-gray-100 bg-white p-3;
}

.detail-label {
  @apply text-[11px] uppercase tracking-wide text-gray-400 font-semibold;
}

.detail-value {
  @apply text-sm text-gray-800 font-semibold mt-1;
}
</style>
