<template>
  <div
    class="w-[45vw] h-[47vh] bg-white border shadow-xl transition-all duration-300 flex flex-col justify-start rounded-xl overflow-hidden p-1"
  >
    <!-- Header -->
    <div
      class="flex items-center justify-between px-2 py-2 text-white bg-defaultGreen rounded-t-lg"
    >
      <h3 class="font-semibold text-base ml-2">Unscheduled Courses</h3>

      <div class="per-page-container">
        <input
          v-model="searchQuery"
          @input="changePage(1)"
          type="text"
          placeholder="Search course, program, SY..."
          class="rounded-xl border border-green-600 px-4 py-2 text-xs w-64 focus:outline-none focus:ring-2 focus:ring-green-400"
        />
      </div>
    </div>

    <!-- Body -->
    <div class="flex-1 overflow-y-auto">
      <!-- Table -->
      <div class="w-full h-[35vh] border bg-white overflow-auto">
        <table class="min-w-full text-xs text-gray-700">
          <thead class="bg-gray-100 text-defaultGreen">
            <tr>
              <th class="px-4 py-3 text-left">Set</th>
              <th class="px-4 py-3 text-center">Program</th>
              <th class="px-4 py-3 text-left">Course</th>
              <th class="px-4 py-3 text-center">Type</th>
              <th class="px-4 py-3 text-center">Semester</th>
              <th class="px-4 py-3 text-center w-[29%]">Reason</th>
              <th class="px-4 py-3 text-center">Action</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="item in paginatedData"
              :key="item.id"
              class="border-t hover:bg-green-50"
            >
              <td class="px-4 py-3">
                {{ getSetName(item.class_id) || item.class_id }}
              </td>
              <td class="px-4 py-3 text-center">{{ item.program_code }}</td>
              <td class="px-4 py-3">{{ item.course_code }}</td>
              <td class="px-4 py-3 text-center">{{ item.type }}</td>
              <td class="px-4 py-3 text-center">
                {{ semesterLabel(item.semester) }}
              </td>
              <td class="px-4 py-3 text-xs text-red-600 max-w-xs">
                {{ item.reason }}
              </td>
              <td class="px-4 py-3 text-center">
                <button @click="openAssignModal(item)" class="btn-save">Assign</button>
              </td>
            </tr>

            <tr v-if="paginatedData.length === 0">
              <td colspan="7" class="py-8">
                <div class="flex justify-center items-center text-gray-400 text-xs">
                  No unscheduled courses found
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4 text-xs">
        <div class="text-gray-700">
          Showing {{ startIndex }} to {{ endIndex }} of {{ filteredData.length }} entries
        </div>
        <div class="flex items-center gap-1">
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

    <!-- Assign Modal -->
    <div v-if="assignModalVisible" class="modal-overlay">
      <div class="modal-wrapper">
        <div class="modal-container">
          <!-- HEADER -->
          <div class="modal-header">
            <h1 class="font-bold text-lg">Assign Course</h1>
            <icon name="circle-close3" @click="closeAssignModal" class="cursor-pointer" />
          </div>

          <!-- BODY -->
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

                <!-- DROPDOWN LIST -->
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

            <!-- FOOTER -->
            <div class="modal-footer">
              <button @click="closeAssignModal" class="btn-cancel">Cancel</button>
              <button @click="assignCourse" class="btn-save">Assign</button>
            </div>
          </div>
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
      user: {},
      assignModalVisible: false,
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
        instr.faculty_name?.toLowerCase().includes(query)
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
          item.program_name?.toLowerCase().includes(query) ||
          item.school_year?.toLowerCase().includes(query) ||
          item.type?.toLowerCase().includes(query) ||
          String(item.semester || "")
            .toLowerCase()
            .includes(query) ||
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
      return Math.min(this.currentPage * this.itemsPerPage, this.filteredData.length);
    },

    uniqueInstructors() {
      if (!this.user.program_id) return [];

      const seen = new Set();

      return (this.store.final_schedules || [])
        .filter(
          (s) => s.faculty_id && Number(s.program_id) === Number(this.user.program_id)
        )
        .filter((s) => {
          if (seen.has(s.faculty_id)) return false;
          seen.add(s.faculty_id);
          return true;
        });
    },
  },

  methods: {
    handleClickOutside(event) {
      const dropdown = this.$refs.instructorDropdown;
      if (dropdown && !dropdown.contains(event.target)) {
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

    openAssignModal(item) {
      const courseInfo = this.store.courses?.find(
        (c) => Number(c.course_id) === Number(item.course_id)
      );

      const programInfo = this.store.programs?.find(
        (p) => Number(p.program_id) === Number(item.program_id)
      );

      this.selectedCourse = {
        ...item,
        course_code: item.course_code || courseInfo?.course_code || "Unknown",
        program_code: item.program_code || programInfo?.program_code || "Unknown",
        set_name: this.getSetName(item.class_id) || item.class_id,
        hours: item.hours || "3h lec",
      };

      this.assignModalVisible = true;
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

      const course = {
        ...JSON.parse(JSON.stringify(this.selectedCourse)),
        faculty_id: this.selectedInstructor,
        faculty_name: this.getFacultyName(this.selectedInstructor),
      };

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

      this.$emit("open-edit-schedule", payload);
      this.closeAssignModal();
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

    getInstituteId(programId) {
      const program = (this.store.programs || []).find(
        (p) => Number(p.program_id) === Number(programId)
      );
      return program ? program.institute_id : null;
    },

    getFacultyName(facultyId) {
      const user = (this.store.rawusers || []).find(
        (u) => Number(u.id) === Number(facultyId)
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

    // console.log("unscheduled_meetings:", this.store.unscheduled_meetings);
    // console.log("sections:", this.store.sections);
    // console.log("sectionMap:", this.sectionMap);
    document.addEventListener("click", this.handleClickOutside);
  },

  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>
