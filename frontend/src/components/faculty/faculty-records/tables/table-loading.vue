<template>
  <div class="bg-white w-full rounded-md">
    <!-- HEADER -->
    <div class="flex justify-between flex-wrap gap-2 items-center">
      <div class="flex gap-2 items-center flex-wrap">
        <!-- School Year -->
        <select
          v-model="selectedSchoolYear"
          class="px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
        >
          <option v-for="year in schoolYearOptions" :key="year" :value="year">
            {{ year }}
          </option>
        </select>

        <!-- First Semester -->
        <button @click="selectSemester(1)" :class="semesterBtn(selectedSemester === 1)">
          First Semester
        </button>

        <!-- Second Semester -->
        <button @click="selectSemester(2)" :class="semesterBtn(selectedSemester === 2)">
          Second Semester
        </button>
      </div>
    </div>

    <!-- CONTENT -->
    <div class="h-[75vh] overflow-y-auto mt-2">
      <div v-if="tableRows.length">
        <table class="min-w-full text-sm">
          <thead class="bg-defaultGreen text-white text-xs uppercase">
            <tr>
              <th class="py-3 font-medium rounded-tl-xl w-[7%]">Section</th>
              <th class="py-3 font-medium w-[5%]">Code</th>
              <th class="py-3 font-medium w-[15%]">Description</th>
              <th class="py-3 font-medium w-[5%]">Lec</th>
              <th class="py-3 font-medium w-[5%]">Lab</th>
              <th class="py-3 font-medium w-[5%]">Units</th>
              <th class="py-3 font-medium w-[10%]">Mode</th>

              <!-- ✅ NEW -->
              <th class="py-3 font-medium w-[7%]">Day</th>
              <th class="py-3 font-medium w-[10%]">Time</th>
              <th class="py-3 font-medium w-[10%]">Room</th>
              <th class="py-3 font-medium rounded-tr-xl">Campus</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="row in tableRows" :key="row.id" class="text-xs">
              <td class="border py-3 text-center">{{ row.section }}</td>
              <td class="border py-3 text-center">{{ row.code }}</td>
              <td class="border py-3 px-2">{{ row.description }}</td>
              <td class="border py-3 text-center">{{ row.lec }}</td>
              <td class="border py-3 text-center">{{ row.lab }}</td>
              <td class="border py-3 text-center">{{ row.units }}</td>

              <!-- MODE -->
              <td class="border py-3 text-center font-semibold">
                {{ row.mode }}
              </td>

              <!-- ✅ SEPARATED -->
              <td class="border py-3 text-center">{{ row.day }}</td>
              <td class="border py-3 text-center">{{ row.time }}</td>
              <td class="border py-3 text-center">{{ row.room }}</td>
              <td class="border py-3 text-center">
                {{ row.campus }}
              </td>
            </tr>

            <!-- TOTAL -->
            <tr class="bg-gray-100 font-bold text-center">
              <td colspan="5" class="border text-right px-2">TOTAL</td>
              <td class="border py-3">{{ totalUnits }}</td>
              <td colspan="5" class="border"></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="text-center text-gray-500 mt-10">
        No schedule data available.
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState } from "pinia";

export default {
  data() {
    return {
      selectedSemester: 1,
      selectedSchoolYear: "2025-2026",
      schoolYearOptions: ["2025-2026", "2024-2025", "2023-2024"],
      authenticatedEmployeeId: null,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["final_schedules", "courses", "college_branch"]),

    semesterName() {
      return this.selectedSemester === 1 ? "First" : "Second";
    },
    collegeBranchMap() {
      return Object.fromEntries(
        (this.college_branch || []).map((b) => [
          Number(b.college_branch_id), // ✅ FIXED
          b.college_branch_name,
        ])
      );
    },
    courseMap() {
      return Object.fromEntries((this.courses || []).map((c) => [c.course_code, c]));
    },

    filteredFacultyLoads() {
      return (this.final_schedules || []).filter(
        (item) =>
          Number(item.faculty_id) === Number(this.authenticatedEmployeeId) &&
          Number(item.semester) === Number(this.selectedSemester) &&
          item.school_year === this.selectedSchoolYear
      );
    },

    // ✅ FLAT TABLE ROWS (IMPORTANT CHANGE)
    tableRows() {
      return this.filteredFacultyLoads.map((item) => {
        const course = this.courseMap[item.course_code] || {};

        let start = "",
          end = "";
        if (item.time_slot?.includes(" - ")) {
          [start, end] = item.time_slot.split(" - ");
        }

        return {
          id: item.id,
          section: item.set_name,
          code: item.course_code,
          description: course.course_title || item.course_code,

          lec: course.course_lec || 0,
          lab: course.course_lab || 0,
          units: (course.course_lec || 0) + (course.course_lab || 0),

          // ✅ MODE
          mode: item.mode || "Face-to-Face",

          // ✅ SEPARATED FIELDS
          day: item.day,
          time: `${start} - ${end}`,
          room: item.room_name,

          campus: this.collegeBranchMap[item.college_branch_id] || "Unknown Campus",
        };
      });
    },

    totalUnits() {
      const counted = new Set();

      return this.tableRows.reduce((sum, row) => {
        const key = row.section + row.code;

        if (!counted.has(key)) {
          counted.add(key);
          return sum + row.units;
        }

        return sum;
      }, 0);
    },
  },

  methods: {
    selectSemester(sem) {
      this.selectedSemester = sem;
    },
    semesterBtn(active) {
      return [
        "px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200",
        "border",
        active
          ? "bg-defaultGreen text-white border-green-600 shadow-md"
          : "bg-white text-defaultGreen border-defaultGreen hover:bg-green-600 hover:text-white",
      ];
    },

    async fetchUser() {
      try {
        const { data } = await axios.get(process.env.VUE_APP_API_BASE_URL + "/auth/me", {
          withCredentials: true,
        });
        this.authenticatedEmployeeId = data.sub;
      } catch {
        this.$router.push("/");
      }
    },
  },

  async mounted() {
    const store = useFetchDataStore();
    await this.fetchUser();
    await store.fetchCourses();
    await store.fetchFinalSchedules();
    await store.fetchCollegeBranch();
  },
};
</script>
