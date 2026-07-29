<template>
  <div class="flex flex-col space-y-3 overflow-hidden">
    <!-- Table -->
    <div class="table-container">
      <!-- Top Controls -->
      <div class="table-controls">
        <!-- Items per page -->
        <div class="per-page-container">
          <div class="select-wrapper">
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
        <div class="flex gap-2">
          <!-- SELECTOR -->
          <div class="flex justify-between gap-2">
            <div class="flex items-center gap-3">
              <div class="relative w-56" ref="activeViewDropdownRef">
                <div
                  class="relative flex items-center rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 focus-within:border-defaultGreen focus-within:ring-4 focus-within:ring-green-100"
                >
                  <!-- Icon -->
                  <div class="absolute left-3 text-defaultGreen">
                    <svg
                      class="h-4 w-4"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                      />
                    </svg>
                  </div>

                  <!-- Selected Value -->
                  <button
                    type="button"
                    @click="showActiveViewDropdown = !showActiveViewDropdown"
                    class="w-full rounded-xl py-3 pl-10 pr-10 text-left text-sm font-semibold text-gray-700"
                  >
                    <span v-if="activeView === 'used'"> Used Rooms </span>

                    <span v-else-if="activeView === 'unused'">
                      Unused Rooms
                    </span>

                    <span v-else class="text-gray-600 font-light">
                      Select View
                    </span>
                  </button>

                  <!-- Dropdown Arrow -->
                  <button
                    type="button"
                    @click="showActiveViewDropdown = !showActiveViewDropdown"
                    class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 hover:text-defaultGreen"
                  >
                    <svg
                      class="h-4 w-4 transition-transform duration-200"
                      :class="{ 'rotate-180': showActiveViewDropdown }"
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
                  </button>
                </div>

                <!-- Dropdown -->
                <div
                  v-if="showActiveViewDropdown"
                  class="absolute z-[9999] mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
                >
                  <div class="border-b border-gray-100 px-4 py-3">
                    <p class="text-xs uppercase tracking-wide text-gray-400">
                      Room View
                    </p>
                  </div>

                  <div class="p-1.5">
                    <button
                      @click="
                        activeView = 'used';
                        showActiveViewDropdown = false;
                      "
                      class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                      :class="activeView === 'used' ? 'bg-green-50' : ''"
                    >
                      <p class="text-sm text-gray-800">Used Rooms</p>

                      <svg
                        v-if="activeView === 'used'"
                        class="h-5 w-5 text-defaultGreen"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </button>

                    <button
                      @click="
                        activeView = 'unused';
                        showActiveViewDropdown = false;
                      "
                      class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                      :class="activeView === 'unused' ? 'bg-green-50' : ''"
                    >
                      <p class="text-sm text-gray-800">Unused Rooms</p>

                      <svg
                        v-if="activeView === 'unused'"
                        class="h-5 w-5 text-defaultGreen"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        viewBox="0 0 24 24"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M5 13l4 4L19 7"
                        />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- TYPE FILTER -->
            <div
              v-if="activeView === 'unused'"
              class="inline-flex items-center gap-1 rounded-xl border border-gray-200 bg-gray-50 shadow-sm"
            >
              <button
                type="button"
                @click="
                  roomFilter = 'Lecture';
                  changePage(1);
                "
                :class="[
                  'flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition-all duration-200',
                  roomFilter === 'Lecture'
                    ? 'bg-white text-defaultGreen shadow-sm ring-1 ring-green-100'
                    : 'text-gray-500 hover:bg-white hover:text-gray-700',
                ]"
              >
                <span>Lecture</span>
                <span
                  :class="[
                    'rounded-full px-2 py-0.5 text-[11px] font-bold',
                    roomFilter === 'Lecture'
                      ? 'bg-green-50 text-green-700'
                      : 'bg-gray-200 text-gray-600',
                  ]"
                >
                  {{ lectureRooms.length }}
                </span>
              </button>

              <button
                type="button"
                @click="
                  roomFilter = 'Laboratory';
                  changePage(1);
                "
                :class="[
                  'flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition-all duration-200',
                  roomFilter === 'Laboratory'
                    ? 'bg-white text-blue-700 shadow-sm ring-1 ring-blue-100'
                    : 'text-gray-500 hover:bg-white hover:text-gray-700',
                ]"
              >
                <span>Laboratory</span>
                <span
                  :class="[
                    'rounded-full px-2 py-0.5 text-[11px] font-bold',
                    roomFilter === 'Laboratory'
                      ? 'bg-blue-50 text-blue-700'
                      : 'bg-gray-200 text-gray-600',
                  ]"
                >
                  {{ laboratoryRooms.length }}
                </span>
              </button>
            </div>
          </div>

          <!-- SEARCH -->

          <div class="relative w-[320px]" ref="roomDropdownRef">
            <div
              class="relative flex items-center rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 focus-within:border-defaultGreen focus-within:ring-4 focus-within:ring-green-100"
            >
              <div class="absolute left-3 text-defaultGreen">
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

              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search or select room..."
                class="w-full rounded-xl bg-transparent py-3 pl-10 pr-10 text-sm font-medium text-gray-700 outline-none placeholder:text-gray-400"
                @focus="showRoomDropdown = true"
                @input="
                  showRoomDropdown = true;
                  changePage(1);
                "
              />

              <button
                type="button"
                @click="showRoomDropdown = !showRoomDropdown"
                class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400 transition hover:bg-gray-100 hover:text-defaultGreen"
              >
                <svg
                  class="w-4 h-4 transition-transform duration-200"
                  :class="{ 'rotate-180': showRoomDropdown }"
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
              </button>
            </div>

            <div
              v-if="showRoomDropdown"
              class="absolute right-0 z-50 mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
            >
              <div class="border-b border-gray-100 px-4 py-3">
                <p
                  class="text-xs font-semibold uppercase tracking-wide text-gray-400"
                >
                  {{ activeView === "used" ? "Used Rooms" : "Unused Rooms" }}
                </p>
              </div>

              <div class="max-h-[260px] overflow-y-auto p-1.5">
                <button
                  v-for="room in filteredRoomOptions"
                  :key="room.room_name"
                  type="button"
                  @click="selectRoom(room.room_name)"
                  class="flex w-full items-center justify-between gap-3 rounded-lg px-3 py-2.5 text-left transition hover:bg-green-50"
                  :class="searchQuery === room.room_name ? 'bg-green-50' : ''"
                >
                  <div>
                    <p class="text-sm font-semibold text-gray-800">
                      {{ room.room_name }}
                    </p>
                    <p class="text-xs text-gray-500">
                      {{ room.room_type || "Unknown" }}
                    </p>
                  </div>

                  <span
                    class="rounded-full px-2.5 py-1 text-[11px] font-semibold"
                    :class="
                      room.room_type === 'Laboratory'
                        ? 'bg-blue-50 text-blue-700'
                        : 'bg-green-50 text-green-700'
                    "
                  >
                    {{ room.room_type || "Room" }}
                  </span>
                </button>

                <div
                  v-if="filteredRoomOptions.length === 0"
                  class="px-4 py-6 text-center text-sm text-gray-400"
                >
                  No room found
                </div>
              </div>

              <div v-if="searchQuery" class="border-t border-gray-100 p-2">
                <button
                  type="button"
                  @click="clearRoomSearch"
                  class="w-full rounded-lg px-3 py-2 text-sm font-medium text-gray-500 transition hover:bg-gray-50 hover:text-gray-700"
                >
                  Clear search
                </button>
              </div>
            </div>
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
                <th class="px-4 py-3 text-left">Campus</th>
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
                <td>
                  {{ room.room_name }}
                </td>

                <td>
                  {{
                    room?.building?.buildingArea?.collegeBranch
                      ?.college_branch_name || "-"
                  }}
                </td>

                <td class="text-center">
                  {{ room.room_type }}
                </td>

                <td
                  v-if="activeView === 'used'"
                  class="text-center font-semibold text-green-700"
                >
                  {{ room.count }}
                </td>

                <td v-if="activeView === 'unused'" class="text-center">
                  {{ room.room_capacity }}
                </td>
              </tr>

              <tr v-if="paginatedData.length === 0">
                <td colspan="8" class="text-center py-6 text-gray-400">
                  <div
                    class="flex flex-col items-center justify-center text-center text-gray-500"
                  >
                    <div class="text-center text-gray-500">
                      <p class="text-lg font-semibold mb-2">
                        No schedule data available
                      </p>
                      <p class="text-sm text-gray-400">
                        Please click
                        <span class="font-medium text-defaultGreen"
                          >"Generate"</span
                        >
                        to generate schedule data.
                      </p>
                    </div>
                  </div>
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
      showRoomDropdown: false,
      scheduleByRoom: {},
      groupedSchedule: {},
      roomsFromAPI: [],
      activeView: "used",
      roomFilter: "Lecture",
      searchQuery: "",
      itemsPerPage: 15,
      currentPage: 1,
      showActiveViewDropdown: false,
    };
  },

  computed: {
    filteredRoomOptions() {
      const query = this.searchQuery.toLowerCase().trim();

      return this.tableData.filter((room) => {
        const roomName = String(room.room_name || "").toLowerCase();
        const roomType = String(room.room_type || "").toLowerCase();

        return roomName.includes(query) || roomType.includes(query);
      });
    },
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
              room_capacity: room?.room_capacity || 0,
              building: room?.building || null,
              institute: room?.institute || null,
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
    selectRoom(roomName) {
      this.searchQuery = roomName;
      this.showRoomDropdown = false;
      this.changePage(1);
    },

    clearRoomSearch() {
      this.searchQuery = "";
      this.showRoomDropdown = false;
      this.changePage(1);
    },

    handleClickOutside(event) {
      const dropdown = this.$refs.roomDropdownRef;

      if (dropdown && !dropdown.contains(event.target)) {
        this.showRoomDropdown = false;
      }
    },
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
      const scheduleByRoom = data?.schedule_by_room;
      // If wala unod ang json
      if (!scheduleByRoom || Object.keys(scheduleByRoom).length === 0) {
        this.scheduleByRoom = {};
        this.groupedSchedule = {};
        return;
      }
      this.scheduleByRoom = scheduleByRoom;
      this.groupedSchedule = this.transformRoomSchedule(scheduleByRoom);
    },
    async loadRooms() {
      const store = useFetchDataStore();
      await store.fetchRooms();
      this.roomsFromAPI = store.rooms;
    },
  },

  async mounted() {
    document.addEventListener("click", this.handleClickOutside);

    await this.loadSchedules();
    await this.loadRooms();
  },

  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>
