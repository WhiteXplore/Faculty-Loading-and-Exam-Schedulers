<template>
  <div class="overflow-y-auto">
    <div class="mt-2 overflow-x-auto bg-white">
      <!-- FILTER BAR -->
      <div class="flex justify-between items-center mb-3 gap-4">
        <!-- CURRENT ROOM TITLE -->
        <span v-for="(schedules, room) in filteredRooms" :key="room" class="text-lg">
          <span class="font-bold text-defaultGreen">
            {{ room }} - {{ roomTypeMap[room] || "Unknown" }}
          </span>
        </span>

        <!-- PREMIUM SEARCH / ROOM DROPDOWN -->
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
              class="w-full rounded-xl bg-transparent py-2.5 pl-10 pr-10 text-sm font-medium text-gray-700 outline-none placeholder:text-gray-400"
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
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>

          <!-- DROPDOWN -->
          <div
            v-if="showRoomDropdown"
            class="absolute right-0 z-50 mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
          >
            <div class="border-b border-gray-100 px-4 py-3">
              <p class="text-xs font-semibold uppercase tracking-wide text-gray-400">
                Available Rooms
              </p>
            </div>

            <div class="max-h-[260px] overflow-y-auto p-1.5">
              <button
                v-for="room in filteredRoomOptions"
                :key="room"
                type="button"
                @click="selectRoom(room)"
                class="flex w-full items-center justify-between gap-3 rounded-lg px-3 py-2.5 text-left transition hover:bg-green-50"
                :class="searchQuery === room ? 'bg-green-50' : ''"
              >
                <div>
                  <p class="text-sm font-semibold text-gray-800">
                    {{ room }}
                  </p>
                  <p class="text-xs text-gray-500">
                    {{ roomTypeMap[room] || "Unknown" }}
                  </p>
                </div>

                <span
                  class="rounded-full px-2.5 py-1 text-[11px] font-semibold"
                  :class="
                    roomTypeMap[room] === 'Laboratory'
                      ? 'bg-blue-50 text-blue-700'
                      : 'bg-green-50 text-green-700'
                  "
                >
                  {{ roomTypeMap[room] || "Room" }}
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

      <div v-if="Object.keys(groupedSchedule).length" class="grid grid-cols-1 gap-3">
        <div
          v-for="(schedules, room) in filteredRooms"
          :key="room"
          class="bg-white rounded-xl border flex flex-col h-[75vh]"
        >
          <div class="overflow-auto border bg-white h-[83vh] rounded-t-xl">
            <table class="w-full text-[13px] border-collapse table-fixed">
              <thead class="bg-defaultGreen text-white sticky top-0 z-20">
                <tr>
                  <th class="py-3 w-[9%] text-center">Time</th>
                  <th v-for="day in days" :key="day" class="p-2 text-center">
                    {{ day }}
                  </th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="slot in timeSlots" :key="slot.start">
                  <td class="border p-2 text-center font-medium">
                    {{ formatTime(slot.start) }} -
                    {{ formatTime(slot.end) }}
                  </td>

                  <td v-for="day in days" :key="day" class="border relative h-[60px]">
                    <template v-if="room !== 'Online'">
                      <div
                        v-for="item in getScheduleForCell(slot, day, room)"
                        :key="item.id"
                        class="absolute inset-x-1 rounded p-1 text-[11px]"
                        :style="{
                          ...getProgramColor(item.program_code),
                          height: getBlockHeight(item) + 'px',
                          top: getBlockTop(item, slot) + 'px',
                        }"
                      >
                        <span
                          v-if="getInstituteBadge(item.program_code)"
                          :class="[
                            'absolute top-1 right-2 text-[9px] px-1.5 py-[1px] rounded-full font-semibold shadow',
                            getInstituteBadge(item.program_code).class,
                          ]"
                        >
                          {{ getInstituteBadge(item.program_code).label }}
                        </span>

                        <p class="font-semibold">{{ item.course_code }}</p>
                        <p class="text-gray-600">{{ item.faculty_name }}</p>
                        <p class="text-gray-600">
                          {{ item.program_code }} - {{ item.set_name }}
                        </p>

                        <button
                          v-if="hasRoomConflict(item)"
                          @click.stop="openConflictModal(item)"
                          class="absolute bottom-1 right-1 flex items-center justify-center w-4 h-4 rounded-full bg-red-600 text-white text-[9px] font-bold shadow hover:bg-red-700"
                        >
                          !
                        </button>
                      </div>
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div
          v-if="Object.keys(filteredRooms).length === 0"
          class="flex flex-col items-center justify-center min-h-[350px] text-center text-gray-500 border rounded-xl"
        >
          <p class="text-lg font-semibold mb-2">No room found</p>
          <p class="text-sm text-gray-400">
            Try searching another room name or room type.
          </p>
        </div>
      </div>

      <div
        v-else
        class="flex flex-col items-center justify-center min-h-[350px] text-center text-gray-500"
      >
        <p class="text-lg font-semibold mb-2">No schedule data available</p>
        <p class="text-sm text-gray-400">
          Please click
          <span class="font-medium text-defaultGreen">"Generation"</span>
          to generate schedule data.
        </p>
      </div>
    </div>

    <!-- CONFLICT MODAL -->
    <div
      v-if="showConflictModal"
      class="fixed inset-0 z-50 bg-black/40 flex items-center justify-center"
    >
      <div class="bg-white w-[900px] rounded-2xl p-6 shadow-xl">
        <div class="flex items-center justify-between border-b pb-3 mb-4">
          <div class="per-page-container">
            <icon
              name="exclamation-circle"
              class="w-7 h-7 p-1 rounded-full bg-red-200 text-red-900 flex items-center justify-center"
            />
            <h3 class="text-lg font-semibold text-gray-800">
              Scheduled Conflict Detected
            </h3>
          </div>

          <button
            @click="showConflictModal = false"
            class="text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        </div>

        <div class="grid grid-cols-2 gap-6 mt-6">
          <div class="relative bg-white rounded-2xl p-5 border">
            <span
              class="absolute -top-3 left-4 bg-green-600 text-white text-xs px-3 py-1 rounded-full shadow"
            >
              Selected Schedule
            </span>

            <div v-if="selectedSchedule" class="mt-3 space-y-3 text-sm">
              <h4 class="font-semibold text-base">
                {{ selectedSchedule.course_code }}
              </h4>

              <div class="grid grid-cols-2 gap-3">
                <div>
                  <p class="text-xs text-gray-500">Faculty</p>
                  <p class="font-medium">{{ selectedSchedule.faculty_name }}</p>
                </div>

                <div>
                  <p class="text-xs text-gray-500">Section</p>
                  <p class="font-medium">
                    {{ selectedSchedule.program_code }} -
                    {{ selectedSchedule.set_name }}
                  </p>
                </div>

                <div>
                  <p class="text-xs text-gray-500">Room</p>
                  <p class="font-medium">{{ selectedSchedule.room_name }}</p>
                </div>

                <div>
                  <p class="text-xs text-gray-500">Room Type</p>
                  <p class="font-medium">
                    {{ roomTypeMap[selectedSchedule.room_name] }}
                  </p>
                </div>

                <div>
                  <p class="text-xs text-gray-500">Day</p>
                  <p class="font-medium">{{ selectedSchedule.day }}</p>
                </div>

                <div>
                  <p class="text-xs text-gray-500">Time</p>
                  <p class="font-medium">
                    {{ formatTime(selectedSchedule.start_hour) }} –
                    {{
                      formatTime(selectedSchedule.start_hour + selectedSchedule.duration)
                    }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="relative bg-white rounded-2xl p-5 border">
            <span
              class="absolute -top-3 left-4 bg-red-600 text-white text-xs px-3 py-1 rounded-full shadow"
            >
              Conflicting Schedules
            </span>

            <div class="mt-3 space-y-4 max-h-[420px] overflow-y-auto pr-2">
              <div
                v-for="conflict in conflictRecords"
                :key="conflict.id"
                class="rounded-xl p-4 ring-1 ring-red-200 bg-red-50"
              >
                <div class="space-y-2 text-sm">
                  <h5 class="font-semibold text-gray-800">
                    {{ conflict.course_code }}
                  </h5>

                  <div class="grid grid-cols-2 gap-2 text-gray-700">
                    <div>
                      <p class="text-xs text-gray-500">Faculty</p>
                      <p class="font-medium">{{ conflict.faculty_name }}</p>
                    </div>

                    <div>
                      <p class="text-xs text-gray-500">Section</p>
                      <p class="font-medium">
                        {{ conflict.program_code }} -
                        {{ conflict.set_name }}
                      </p>
                    </div>

                    <div>
                      <p class="text-xs text-gray-500">Room</p>
                      <p class="font-medium">{{ conflict.room_name }}</p>
                    </div>

                    <div>
                      <p class="text-xs text-gray-500">Room Type</p>
                      <p class="font-medium">
                        {{ roomTypeMap[conflict.room_name] }}
                      </p>
                    </div>

                    <div>
                      <p class="text-xs text-gray-500">Day</p>
                      <p class="font-medium">{{ conflict.day }}</p>
                    </div>

                    <div>
                      <p class="text-xs text-gray-500">Time</p>
                      <p class="font-medium">
                        {{ formatTime(conflict.start_hour) }} –
                        {{ formatTime(conflict.start_hour + conflict.duration) }}
                      </p>
                    </div>
                  </div>

                  <div
                    class="flex items-center gap-2 mt-2 text-xs text-red-700 bg-red-100 p-2 rounded-lg"
                  >
                    ⚠ Schedule overlap detected
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="flex justify-end mt-5">
          <button
            @click="showConflictModal = false"
            class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-sm"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useFetchDataStore } from "@/store/fetch-data-store";

export default {
  name: "RoomScheduleCards",

  data() {
    return {
      searchQuery: "",
      showRoomDropdown: false,
      entriesLimit: 1,
      groupedSchedule: {},
      rooms: [],
      roomTypeMap: {},
      currentPage: 1,
      showConflictModal: false,
      conflictRecords: [],
      selectedSchedule: null,
      programs: [],
      programMap: {},
      instituteMap: {},

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
        start: 7 + i,
        end: 8 + i,
      })),
    };
  },

  computed: {
    usedRoomOptions() {
      return Object.keys(this.groupedSchedule)
        .filter((room) => room.toLowerCase() !== "online")
        .sort((a, b) => a.localeCompare(b));
    },

    filteredRoomOptions() {
      const query = this.searchQuery.toLowerCase().trim();

      return this.usedRoomOptions.filter((room) => {
        const roomName = room.toLowerCase();
        const roomType = (this.roomTypeMap[room] || "").toLowerCase();

        return roomName.includes(query) || roomType.includes(query);
      });
    },

    filteredRooms() {
      const query = this.searchQuery.toLowerCase().trim();

      const filtered = Object.entries(this.groupedSchedule).filter(([room]) => {
        const roomName = room.toLowerCase();
        const roomType = (this.roomTypeMap[room] || "").toLowerCase();

        return (
          roomName !== "online" && (roomName.includes(query) || roomType.includes(query))
        );
      });

      return Object.fromEntries(filtered.slice(0, this.entriesLimit));
    },
  },

  methods: {
    selectRoom(room) {
      this.searchQuery = room;
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

    getRoomBadge(room) {
      const type = this.roomTypeMap[room];

      if (type === "Lecture") {
        return {
          label: "Lec",
          class: "bg-green-600 text-white",
        };
      }

      if (type === "Laboratory") {
        return {
          label: "Lab",
          class: "bg-blue-600 text-white",
        };
      }

      return null;
    },

    getInstituteBadge(programCode) {
      const instituteId = this.programMap[programCode];
      const instituteName = this.instituteMap[instituteId];

      if (!instituteName) return null;

      const colors = {
        63: "bg-cyan-600 text-white",
        64: "bg-purple-800 text-white",
        65: "bg-red-600 text-white",
        66: "bg-blue-600 text-white",
      };

      return {
        label: instituteName,
        class: colors[instituteId] || "bg-gray-500 text-white",
      };
    },

    getProgramColor(programCode) {
      const instituteId = this.programMap[programCode];

      const instituteColors = {
        63: "118, 210, 219",
        64: "166, 166, 237",
        65: "168, 35, 35",
        66: "59, 130, 246",
      };

      const rgb = instituteColors[instituteId];

      return {
        background: rgb ? `rgba(${rgb}, 0.3)` : "rgba(220, 252, 231, 0.5)",
        border: rgb ? `1px solid rgba(${rgb}, 1)` : "1px solid #22C55E",
      };
    },

    changePage(page) {
      this.currentPage = page;
    },

    parseHour(timeStr) {
      const [time, modifier] = timeStr.split(" ");
      let [hours, minutes] = time.split(":").map(Number);

      if (modifier === "PM" && hours !== 12) hours += 12;
      if (modifier === "AM" && hours === 12) hours = 0;

      return hours + minutes / 60;
    },

    formatTime(h) {
      const hour = Math.floor(h);
      const minutes = Math.round((h - hour) * 60);
      const period = hour >= 12 ? "PM" : "AM";
      const hour12 = hour % 12 || 12;

      return `${hour12}:${minutes.toString().padStart(2, "0")} ${period}`;
    },

    transformRoomSchedule(roomData) {
      const result = {};

      Object.entries(roomData).forEach(([roomName, records]) => {
        const parsed = records.map((r, index) => {
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
            day,
            start_hour: startHour,
            duration: endHour - startHour,
          };
        });

        result[roomName] = parsed;
      });

      return result;
    },

    getScheduleForCell(slot, day, room) {
      const schedules = this.groupedSchedule[room] || [];

      return schedules.filter((item) => {
        if (item.day !== day) return false;

        return item.start_hour >= slot.start && item.start_hour < slot.end;
      });
    },

    getBlockHeight(item) {
      return item.duration * 60;
    },

    getBlockTop(item, slot) {
      return (item.start_hour - slot.start) * 60;
    },

    hasRoomConflict(record) {
      const roomSchedules = this.groupedSchedule[record.room_name] || [];

      return roomSchedules.some((r) => {
        if (r.id === record.id) return false;

        return (
          r.day === record.day &&
          r.start_hour === record.start_hour &&
          r.duration === record.duration &&
          r.set_name === record.set_name &&
          r.program_code === record.program_code
        );
      });
    },

    openConflictModal(record) {
      const roomSchedules = this.groupedSchedule[record.room_name] || [];

      this.selectedSchedule = record;

      this.conflictRecords = roomSchedules.filter((r) => {
        return (
          r.id !== record.id &&
          r.day === record.day &&
          r.start_hour === record.start_hour &&
          r.duration === record.duration &&
          r.set_name === record.set_name &&
          r.program_code === record.program_code
        );
      });

      this.showConflictModal = true;
    },

    async loadSchedules() {
      const store = useFetchDataStore();
      const data = await store.fetchGeneratedScheduled();
      const scheduleByRoom = data?.schedule_by_room;

      if (!scheduleByRoom || Object.keys(scheduleByRoom).length === 0) {
        this.groupedSchedule = {};
        return;
      }

      this.groupedSchedule = this.transformRoomSchedule(scheduleByRoom);
    },

    async fetchRooms() {
      const store = useFetchDataStore();
      await store.fetchRooms();

      this.rooms = store.rooms || [];

      this.roomTypeMap = this.rooms.reduce((map, room) => {
        map[room.room_name] = room.room_type;
        return map;
      }, {});
    },

    async fetchPrograms() {
      const store = useFetchDataStore();
      await store.fetchPrograms();

      this.programs = store.programs || [];

      this.programMap = this.programs.reduce((map, p) => {
        map[p.program_code] = p.institute_id;
        return map;
      }, {});

      this.instituteMap = this.programs.reduce((map, p) => {
        if (p.institute) {
          map[p.institute.institute_id] = p.institute.institute_code;
        }
        return map;
      }, {});
    },
  },

  async mounted() {
    document.addEventListener("click", this.handleClickOutside);

    await this.fetchPrograms();
    await this.fetchRooms();
    await this.loadSchedules();
  },

  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>
