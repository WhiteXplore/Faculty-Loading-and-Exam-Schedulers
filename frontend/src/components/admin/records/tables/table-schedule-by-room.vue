<template>
  <div class="overflow-y-auto">
    <div class="mt-2 overflow-x-auto bg-white">
      <!-- FILTER BAR -->
      <div class="flex justify-between items-center mb-3">
        <!-- <div class="flex items-center gap-2">
          <div class="relative">
            <select
              v-model="entriesLimit"
              class="appearance-none rounded-full border border-green-600 bg-white px-3 py-1 pr-8 text-green-900 text-sm font-semibold shadow-sm cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
            >
              <option :value="5">5</option>
              <option :value="10">10</option>
              <option :value="15">15</option>
              <option :value="20">20</option>
              <option :value="999">All</option>
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
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>

          <span class="text-sm font-medium text-gray-600">Per page</span>
        </div> -->
        <!-- SHOW ENTRIES -->
        <span v-for="(schedules, room) in filteredRooms" :key="room" class="text-lg">
          <span class="font-bold text-defaultGreen"
            >{{ room }} - {{ roomTypeMap[room] || "Unknown" }}</span
          >
        </span>

        <!-- SEARCH -->

        <div class="relative w-full sm:w-64 md:w-72 lg:w-80">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search room..."
            class="rounded-xl border border-green-600 bg-white px-4 py-2.5 pl-10 text-sm shadow-sm w-full transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-md focus:shadow-md"
            @input="changePage(1)"
          />
          <!-- Search icon -->
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
      <div v-if="Object.keys(groupedSchedule).length" class="grid grid-cols-1 gap-3">
        <div
          v-for="(schedules, room) in filteredRooms"
          :key="room"
          class="bg-white rounded-xl border flex flex-col h-[75vh]"
        >
          <!-- HEADER -->
          <!-- <div class="bg-defaultGreen text-white px-4 py-3 rounded-t-xl">
            <span class="text-lg font-bold">
              {{ room }} - {{ roomTypeMap[room] || "Unknown" }}
            </span>
          </div> -->
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
                  <!-- TIME -->
                  <td class="border p-2 text-center font-medium">
                    {{ formatTime(slot.start) }} -
                    {{ formatTime(slot.end) }}
                  </td>

                  <!-- DAYS -->
                  <td v-for="day in days" :key="day" class="border relative h-[60px]">
                    <!-- ONLINE ROOM -->
                    <div v-if="room === 'Online'" class="flex flex-col gap-1 p-1 w-full">
                      <div
                        v-for="item in getScheduleForCell(slot, day, room)"
                        :key="item.id"
                        class="absolute inset-x-1 rounded-lg p-1 text-[11px] relative"
                        :style="{
                          ...getProgramColor(item.program_code),
                          height: getBlockHeight(item) + 'px',
                          top: getBlockTop(item, slot) + 'px',
                        }"
                      >
                        <!-- 🔥 BADGE -->
                        <span
                          v-if="getRoomBadge(room)"
                          :class="[
                            'absolute top-1 left-1 text-[9px] px-1.5 py-[1px] rounded font-semibold shadow',
                            getRoomBadge(room).class,
                          ]"
                        >
                          {{ getRoomBadge(room).label }}
                        </span>

                        <p class="font-semibold mt-3">{{ item.course_code }}</p>
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
                    </div>

                    <!-- NORMAL ROOM -->
                    <template v-else>
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
                        <!-- <span
                        v-if="getRoomBadge(room)"
                        :class="[
                          'absolute top-1 right-1 text-[9px] px-1.5 py-[1px] rounded-full font-semibold shadow',
                          getRoomBadge(room).class,
                        ]"
                      >
                        {{ getRoomBadge(room).label }}
                      </span> -->

                        <!-- ✅ INSTITUTE BADGE (FIXED) -->
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
        <!-- Header -->
        <div class="flex items-center justify-between border-b pb-3 mb-4">
          <div class="flex items-center gap-2">
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

        <!-- BODY -->
        <div class="grid grid-cols-2 gap-6 mt-6">
          <!-- SELECTED SCHEDULE -->
          <div class="relative bg-white rounded-2xl p-5 border">
            <span
              class="absolute -top-3 left-4 bg-green-600 text-white text-xs px-3 py-1 rounded-full shadow"
            >
              Selected Schedule
            </span>

            <div v-if="selectedSchedule" class="mt-3 space-y-3 text-sm">
              <div class="flex justify-between items-center">
                <h4 class="font-semibold text-base">
                  {{ selectedSchedule.course_code }}
                </h4>
              </div>

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

          <!-- CONFLICT LIST -->
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

        <!-- FOOTER -->
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
    filteredRooms() {
      const query = this.searchQuery.toLowerCase();
      const filtered = Object.entries(this.groupedSchedule).filter(([room]) => {
        const roomName = room.toLowerCase();
        const roomType = (this.roomTypeMap[room] || "").toLowerCase();

        return (
          (roomName.includes(query) || roomType.includes(query)) && roomName !== "online"
        );
      });
      return Object.fromEntries(filtered.slice(0, this.entriesLimit));
    },
  },

  methods: {
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
        // IAAS - Sky Blue
        63: "bg-cyan-600 text-white",
        // IC - Violet
        64: "bg-purple-800 text-white",
        // ILEGG - Maroon
        65: "bg-red-600 text-white",
        // ITED - Blue
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
        63: "118, 210, 219", // IAAS
        64: "166, 166, 237", // IC
        65: "168, 35, 35", // ILEGG
        66: "59, 130, 246", // ITED
      };

      const rgb = instituteColors[instituteId];

      return {
        background: rgb
          ? `rgba(${rgb}, 0.3)` //
          : "rgba(220, 252, 231, 0.5)",

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

    getRoomColor(room) {
      const type = this.roomTypeMap[room];

      if (type === "Laboratory") {
        return {
          background: "#DBEAFE",
          border: "1px solid #3B82F6",
        };
      }

      return {
        background: "#DCFCE7",
        border: "1px solid #22C55E",
      };
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
      // if wala unod ang json
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

      // ✅ program_code -> institute_id
      this.programMap = this.programs.reduce((map, p) => {
        map[p.program_code] = p.institute_id;
        return map;
      }, {});

      // ✅ institute_id -> institute_name (FIXED 🔥)
      this.instituteMap = this.programs.reduce((map, p) => {
        if (p.institute) {
          map[p.institute.institute_id] = p.institute.institute_code;
        }
        return map;
      }, {});
    },
  },

  async mounted() {
    await this.fetchPrograms();
    await this.fetchRooms();
    await this.loadSchedules();
  },
};
</script>
