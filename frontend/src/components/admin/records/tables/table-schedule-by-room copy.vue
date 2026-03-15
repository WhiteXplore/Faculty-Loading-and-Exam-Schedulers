<template>
  <div class="flex flex-col space-y-3 h-[83vh] overflow-hidden">
    <!-- TABLE CONTAINER -->
    <div class="mt-2 overflow-x-auto border p-3 rounded-xl bg-white">
      <!-- TOP CONTROLS (SAME DESIGN AS ROOM TABLE) -->
      <div
        class="flex justify-between items-center flex-wrap gap-3 text-gray-700 bg-white"
      >
        <!-- Items Per Page -->
        <div class="flex items-center gap-2">
          <div class="relative">
            <select
              v-model="itemsPerPage"
              class="appearance-none rounded-full border border-green-600 bg-white px-3 py-1 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500"
              @change="changePage(1)"
            >
              <option value="15">15</option>
              <option value="20">20</option>
            </select>

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

        <!-- SEARCH -->
        <div class="relative w-full sm:w-64 md:w-72 lg:w-80">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search room, faculty, course..."
            class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full transition-all duration-200 focus:ring-2 focus:ring-green-500"
            @input="changePage(1)"
          />

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
      </div>

      <!-- TABLE -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[69vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead
              class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
            >
              <tr>
                <th class="px-4 py-3 text-left font-normal">Room</th>
                <th class="px-4 py-3 text-center font-normal">Day</th>
                <th class="px-4 py-3 text-center font-normal">Time</th>
                <th class="px-4 py-3 text-center font-normal">Course</th>
                <th class="px-4 py-3 text-center font-normal">Program</th>
                <th class="px-4 py-3 text-center font-normal">Section</th>
                <th class="px-4 py-3 text-center font-normal">Faculty</th>
                <th class="px-4 py-3 text-center font-normal">Reason</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="item in paginatedData"
                :key="item.id"
                class="hover:bg-green-50 transition-all border-t"
              >
                <td class="px-4 py-3">{{ item.room_name }}</td>
                <td class="px-4 py-3 text-center">{{ item.day }}</td>

                <td class="px-4 py-3 text-center">
                  {{ formatTime(item.start_hour) }} -
                  {{ formatTime(item.start_hour + item.duration) }}
                </td>

                <td class="px-4 py-3 text-center">{{ item.course_code }}</td>
                <td class="px-4 py-3 text-center">{{ item.program_code }}</td>
                <td class="px-4 py-3 text-center">{{ item.set_name }}</td>
                <td class="px-4 py-3 text-center">{{ item.faculty_name }}</td>

                <td class="px-4 py-3 text-center text-gray-400">-</td>
              </tr>

              <tr v-if="paginatedData.length === 0">
                <td colspan="8" class="text-left py-6 text-gray-400">
                  No schedules found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- PAGINATION (EXACT DESIGN AS ROOM TABLE) -->
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
</template>

<script>
import { useFetchDataStore } from "@/store/fetch-data-store";

export default {
  data() {
    return {
      searchQuery: "",
      currentPage: 1,
      itemsPerPage: 15,

      scheduleByRoom: {},
      groupedSchedule: {},
      filteredGroupedSchedule: {},

      days: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ],
    };
  },

  computed: {
    filteredData() {
      let list = [];

      Object.values(this.filteredGroupedSchedule).forEach((schedules) => {
        if (!Array.isArray(schedules)) return;
        schedules.forEach((item) => list.push(item));
      });

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();

        list = list.filter(
          (s) =>
            (s.room_name && s.room_name.toLowerCase().includes(q)) ||
            (s.faculty_name && s.faculty_name.toLowerCase().includes(q)) ||
            (s.course_code && s.course_code.toLowerCase().includes(q)) ||
            (s.program_code && s.program_code.toLowerCase().includes(q)) ||
            (s.set_name && s.set_name.toLowerCase().includes(q)),
        );
      }

      return list.sort((a, b) => {
        if (a.room_name !== b.room_name)
          return a.room_name.localeCompare(b.room_name);

        if (a.day !== b.day)
          return this.days.indexOf(a.day) - this.days.indexOf(b.day);

        return a.start_hour - b.start_hour;
      });
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
    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },

    parseHour(timeStr) {
      const [time, modifier] = timeStr.split(" ");
      let [hours, minutes] = time.split(":").map(Number);

      if (modifier === "PM" && hours !== 12) hours += 12;
      if (modifier === "AM" && hours === 12) hours = 0;

      return hours + minutes / 60;
    },

    transformRoomSchedule(roomData) {
      const result = {};

      Object.entries(roomData).forEach(([roomName, records]) => {
        if (!Array.isArray(records)) return;

        result[roomName] = records.map((r, index) => {
          const parts = r.day_time.split(" ");

          const day = parts[0];
          const startTime = `${parts[1]} ${parts[2]}`;
          const endTime = `${parts[4]} ${parts[5]}`;

          const startHour = this.parseHour(startTime);
          const endHour = this.parseHour(endTime);

          return {
            id: `room-${roomName}-${index}`,
            faculty_name: r.faculty_name,
            course_code: r.course_code,
            program_code: r.program_code,
            set_name: r.class_name,
            room_name: roomName,
            day: day,
            start_hour: startHour,
            duration: endHour - startHour,
          };
        });
      });

      return result;
    },

    formatTime(h) {
      const hour = Math.floor(h);
      const minutes = Math.round((h - hour) * 60);
      const period = hour >= 12 ? "PM" : "AM";
      const hour12 = hour % 12 || 12;

      return `${hour12}:${minutes.toString().padStart(2, "0")} ${period}`;
    },

    async loadSchedules() {
      const store = useFetchDataStore();

      const data = await store.fetchGeneratedScheduled();

      this.scheduleByRoom = data.schedule_by_room || {};

      this.groupedSchedule = this.transformRoomSchedule(this.scheduleByRoom);

      this.filteredGroupedSchedule = this.groupedSchedule;
    },
  },

  async mounted() {
    await this.loadSchedules();
  },
};
</script>
