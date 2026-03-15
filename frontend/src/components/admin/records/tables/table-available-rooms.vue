<template>
  <div class="flex flex-col space-y-3 overflow-hidden">
    <!-- SELECTOR -->
    <div class="flex justify-between">
      <div class="flex items-center gap-3">
        <select
          v-model="activeView"
          class="border rounded-lg px-3 py-2 text-sm"
        >
          <option value="used">Used Rooms</option>
          <option value="unused">Unused Rooms</option>
        </select>
      </div>

      <!-- TYPE FILTER -->
      <div class="flex gap-2" v-if="activeView === 'unused'">
        <button
          @click="roomFilter = 'Lecture'"
          :class="tabClass(roomFilter === 'Lecture')"
        >
          Lecture ({{ lectureRooms.length }})
        </button>

        <button
          @click="roomFilter = 'Laboratory'"
          :class="tabClass(roomFilter === 'Laboratory')"
          class="font-normal"
        >
          Laboratory ({{ laboratoryRooms.length }})
        </button>
      </div>
    </div>

    <!-- Table -->
    <div class="mt-2 overflow-x-auto border p-3 rounded-xl bg-white">
      <!-- Top Controls -->
      <div
        class="flex justify-between items-center flex-wrap gap-3 text-gray-700 bg-white"
      >
        <!-- Items per page -->
        <div class="flex items-center gap-2">
          <div class="relative">
            <select
              v-model="itemsPerPage"
              class="appearance-none rounded-full border border-green-600 bg-white px-3 py-1 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer"
              @change="changePage(1)"
            >
              <option :value="15">15</option>
              <option :value="20">20</option>
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
            placeholder="Search..."
            class="rounded-full border border-green-600 bg-white px-4 py-2 pl-10 text-sm shadow-sm w-full"
            @input="changePage(1)"
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

      <!-- TABLE -->
      <div class="border rounded-xl bg-white overflow-auto flex-1 mt-3">
        <div class="border max-h-[65vh] overflow-y-auto">
          <table class="w-full text-sm text-gray-700">
            <thead class="bg-defaultGreen text-white">
              <tr>
                <th class="px-4 py-3 text-left">Room</th>
                <th class="px-4 py-3 text-center">Type</th>

                <th v-if="activeView === 'used'" class="px-4 py-3 text-center">
                  Used Count
                </th>

                <th
                  v-if="activeView === 'unused'"
                  class="px-4 py-3 text-center"
                >
                  Capacity
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="room in paginatedData"
                :key="room.room_name || room.id"
                class="border-t hover:bg-green-50"
              >
                <td class="px-4 py-3">
                  {{ room.room_name }}
                </td>

                <td class="px-4 py-3 text-center">
                  {{ room.room_type }}
                </td>

                <td
                  v-if="activeView === 'used'"
                  class="px-4 py-3 text-center font-semibold text-green-700"
                >
                  {{ room.count }}
                </td>

                <td
                  v-if="activeView === 'unused'"
                  class="px-4 py-3 text-center"
                >
                  {{ room.room_capacity }}
                </td>
              </tr>

              <tr v-if="paginatedData.length === 0">
                <td colspan="4" class="text-center py-6 text-gray-400">
                  No data found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- PAGINATION -->
      <div class="flex justify-between items-center mt-2">
        <div class="text-gray-700 text-sm">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredData.length }} entries
        </div>

        <div class="flex items-center gap-1 text-sm">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md"
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
              class="px-3 py-1 rounded-md"
            >
              {{ page }}
            </button>
          </span>

          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md"
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
      scheduleByRoom: {},
      groupedSchedule: {},
      roomsFromAPI: [],
      activeView: "used",
      roomFilter: "Lecture",
      searchQuery: "",
      itemsPerPage: 15,
      currentPage: 1,
    };
  },

  computed: {
    usedRoomList() {
      const roomCounts = {};

      Object.values(this.groupedSchedule).forEach((records) => {
        records.forEach((r) => {
          if (!roomCounts[r.room_name]) {
            const room = this.roomsFromAPI.find(
              (x) => x.room_name === r.room_name,
            );

            roomCounts[r.room_name] = {
              room_name: r.room_name,
              room_type: room?.room_type || "-",
              count: 0,
            };
          }

          roomCounts[r.room_name].count++;
        });
      });

      return Object.values(roomCounts);
    },

    usedRooms() {
      return this.usedRoomList.map((r) => r.room_name);
    },

    availableRooms() {
      return this.roomsFromAPI.filter(
        (r) => !this.usedRooms.includes(r.room_name),
      );
    },

    lectureRooms() {
      return this.availableRooms.filter((r) => r.room_type === "Lecture");
    },

    laboratoryRooms() {
      return this.availableRooms.filter((r) => r.room_type === "Laboratory");
    },

    filteredAvailableRooms() {
      if (this.roomFilter === "Lecture") return this.lectureRooms;
      if (this.roomFilter === "Laboratory") return this.laboratoryRooms;
      return this.availableRooms;
    },

    tableData() {
      return this.activeView === "used"
        ? this.usedRoomList
        : this.filteredAvailableRooms;
    },

    filteredData() {
      if (!this.searchQuery) return this.tableData;

      const q = this.searchQuery.toLowerCase();

      return this.tableData.filter((row) =>
        Object.values(row).some((v) => String(v).toLowerCase().includes(q)),
      );
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredData.slice(start, start + this.itemsPerPage);
    },

    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;
    },

    pageNumbers() {
      const total = this.totalPages;

      if (total <= 3) return Array.from({ length: total }, (_, i) => i + 1);

      let start = this.currentPage - 1;
      let end = this.currentPage + 1;

      if (start < 1) start = 1;
      if (end > total) end = total;

      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
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
  },

  methods: {
    tabClass(active) {
      return [
        "px-4 py-2 rounded-lg text-sm",
        active ? "bg-defaultGreen text-white" : "bg-gray-200 text-gray-700",
      ];
    },

    changePage(page) {
      if (page < 1) page = 1;
      if (page > this.totalPages) page = this.totalPages;
      this.currentPage = page;
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

    async loadSchedules() {
      const store = useFetchDataStore();
      const data = await store.fetchGeneratedScheduled();

      this.scheduleByRoom = data.schedule_by_room || {};
      this.groupedSchedule = this.transformRoomSchedule(this.scheduleByRoom);
    },

    async loadRooms() {
      const store = useFetchDataStore();
      await store.fetchRooms();
      this.roomsFromAPI = store.rooms;
    },
  },

  async mounted() {
    await this.loadSchedules();
    await this.loadRooms();
  },
};
</script>
