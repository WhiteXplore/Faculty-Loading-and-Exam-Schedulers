<template>
  <div class="table-container">
    <!-- Top Controls -->
    <div class="table-controls flex justify-end">
      <!-- SEARCH -->
      <div class="mb-4">
        <div class="search-wrapper">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search courses..."
            class="search-input"
          />

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
    </div>
    <!-- LOADING -->
    <div v-if="loading" class="text-center py-14 text-gray-500">
      Loading schedules...
    </div>

    <!-- ERROR -->
    <div v-else-if="error" class="text-center py-14 text-red-500">
      {{ error }}
    </div>

    <!-- TABLE -->
    <div
      v-else
      class="bg-white rounded-2xl border border-gray-200 overflow-auto h-[75vh] shadow-sm"
    >
      <div class="overflow-x-auto">
        <table class="w-full text-sm text-left">
          <thead class="bg-gray-100 text-gray-700">
            <tr>
              <th class="px-4 py-3 font-semibold w-">Class</th>

              <th class="px-4 py-3 font-semibold">Course Code</th>

              <th class="px-4 py-3 font-semibold">Room</th>
              <th class="px-4 py-3 font-semibold">Day</th>
              <th class="px-4 py-3 font-semibold">Time</th>

              <th class="px-4 py-3 font-semibold">Faculty</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="item in filteredSchedules"
              :key="item.id"
              class="border-t hover:bg-gray-50 transition"
            >
              <!-- PROGRAM + SET -->
              <td class="px-4 py-3 font-medium text-gray-800">
                {{ item.class_display }}
              </td>

              <!-- COURSE -->
              <td class="px-4 py-3">
                {{ item.course_code || "N/A" }}
              </td>

              <!-- ROOM -->
              <td class="px-4 py-3">
                {{ item.room_name || "N/A" }}
              </td>

              <!-- DAY -->
              <td class="px-4 py-3">
                {{ item.day || "N/A" }}
              </td>

              <!-- TIME SLOT -->
              <td class="px-4 py-3">
                {{ item.time_slot || "N/A" }}
              </td>

              <!-- FACULTY -->
              <td class="px-4 py-3">
                {{ item.faculty_name }}
              </td>
            </tr>

            <!-- EMPTY -->
            <tr v-if="filteredSchedules.length === 0">
              <td colspan="4" class="text-center py-14 text-gray-400">
                No schedules found
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "TableTestSearch",

  data() {
    return {
      loading: false,
      error: null,
      searchQuery: "",

      final_schedules: [],
      sections: [],
      users: [],
    };
  },

  computed: {
    // CLEAN MERGED DATA
    schedules() {
      return this.final_schedules.map((schedule) => {
        // FIND CLASS SECTION
        const section = this.sections.find(
          (sec) => Number(sec.class_id) === Number(schedule.class_id),
        );

        // FIND FACULTY
        const faculty = this.users.find(
          (user) => Number(user.id) === Number(schedule.faculty_id),
        );

        return {
          ...schedule,

          // PROGRAM CODE + SET NAME
          class_display: section
            ? `${section.program?.program_code || ""} - ${
                section.set_name || ""
              }`
            : "N/A",

          // FACULTY NAME
          faculty_name: faculty
            ? `${faculty.first_name || ""} ${faculty.last_name || ""}`
            : "N/A",
        };
      });
    },

    // SEARCH
    filteredSchedules() {
      const keyword = this.searchQuery.toLowerCase();

      return this.schedules.filter((item) => {
        return (
          !keyword ||
          String(item.class_display).toLowerCase().includes(keyword) ||
          String(item.course_code).toLowerCase().includes(keyword) ||
          String(item.room_name).toLowerCase().includes(keyword) ||
          String(item.faculty_name).toLowerCase().includes(keyword) ||
          String(item.day).toLowerCase().includes(keyword) ||
          String(item.time_slot).toLowerCase().includes(keyword)
        );
      });
    },
  },

  methods: {
    // FETCH FINAL SCHEDULES
    async fetchFinalSchedules() {
      const { data } = await axios.get(
        process.env.VUE_APP_API_BASE_URL +
          "/final-generated-class-schedule/get-all-final-schedules",
      );

      this.final_schedules = data;
    },

    // FETCH CLASS SECTIONS
    async fetchClassSections() {
      const { data } = await axios.get(
        process.env.VUE_APP_API_BASE_URL + "/class/get-classes",
      );

      this.sections = data;
    },

    // FETCH USERS
    async fetchUsers() {
      const { data } = await axios.get(
        process.env.VUE_APP_API_BASE_URL + "/users/get-users",
      );

      this.users = data;
    },

    // LOAD ALL
    async loadData() {
      this.loading = true;
      this.error = null;

      try {
        await Promise.all([
          this.fetchFinalSchedules(),
          this.fetchClassSections(),
          this.fetchUsers(),
        ]);
      } catch (err) {
        this.error =
          err.response?.data?.message || err.message || "Failed to load data";
      } finally {
        this.loading = false;
      }
    },
  },

  mounted() {
    this.loadData();
  },
};
</script>

<style scoped>
table {
  border-collapse: collapse;
}

th,
td {
  white-space: nowrap;
}
</style>
