<template>
  <div
    v-if="show"
    class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/60 backdrop-blur-[2px] p-4"
    @click.self="closeModal"
  >
    <div
      class="relative flex h-[92vh] w-[96vw] max-w-[1500px] flex-col overflow-hidden rounded-2xl bg-white shadow-2xl"
    >
      <!-- ========================================================= -->
      <!-- HEADER -->
      <!-- ========================================================= -->
      <div
        class="flex shrink-0 items-center justify-between border-b bg-white px-5 py-3"
      >
        <div class="flex items-center gap-3">
          <!-- Map Icon -->
          <div
            class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M9 20.25 3.75 18V5.25L9 7.5m0 12.75 6-2.25m-6 2.25V7.5m6 10.5 5.25 2.25V7.5L15 5.25m0 12.75V5.25m0 0L9 7.5"
              />
            </svg>
          </div>

          <div>
            <h2 class="text-[16px] font-semibold text-gray-800">
              Select Room from Map
            </h2>

            <p class="text-[11px] text-gray-400">
              Select a room from the building layout
            </p>
          </div>
        </div>

        <button
          type="button"
          class="flex h-9 w-9 items-center justify-center rounded-lg text-gray-400 transition hover:bg-gray-100 hover:text-gray-700"
          @click="closeModal"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M6 18 18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>

      <!-- ========================================================= -->
      <!-- TOOLBAR -->
      <!-- ========================================================= -->
      <div
        class="flex shrink-0 flex-wrap items-center justify-between gap-3 border-b bg-gray-50 px-5 py-3"
      >
        <!-- SEARCH -->
        <div class="relative w-full max-w-[350px]">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.8"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="m21 21-4.35-4.35m1.35-5.4a6.75 6.75 0 1 1-13.5 0 6.75 6.75 0 0 1 13.5 0Z"
            />
          </svg>

          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search room..."
            class="h-9 w-full rounded-lg border border-gray-200 bg-white pl-9 pr-3 text-xs text-gray-700 outline-none transition focus:border-emerald-400 focus:ring-2 focus:ring-emerald-100"
          />
        </div>

        <!-- CONTROLS -->
        <div class="flex items-center gap-2">
          <!-- Zoom Out -->
          <button
            type="button"
            class="flex h-9 w-9 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-600 transition hover:bg-gray-100"
            title="Zoom out"
            @click="zoomOut"
          >
            <span class="text-lg font-semibold">−</span>
          </button>

          <div
            class="flex h-9 min-w-[65px] items-center justify-center rounded-lg border border-gray-200 bg-white px-2 text-[11px] font-semibold text-gray-600"
          >
            {{ Math.round(zoom * 100) }}%
          </div>

          <!-- Zoom In -->
          <button
            type="button"
            class="flex h-9 w-9 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-600 transition hover:bg-gray-100"
            title="Zoom in"
            @click="zoomIn"
          >
            <span class="text-lg font-semibold">+</span>
          </button>

          <!-- Reset -->
          <button
            type="button"
            class="h-9 rounded-lg border border-gray-200 bg-white px-3 text-[11px] font-medium text-gray-600 transition hover:bg-gray-100"
            @click="resetZoom"
          >
            Reset
          </button>
        </div>
      </div>

      <!-- ========================================================= -->
      <!-- MAP -->
      <!-- ========================================================= -->
      <div
        ref="mapContainer"
        class="relative flex-1 overflow-auto bg-[#eef2f5]"
      >
        <!-- GRID BACKGROUND -->
        <div
          class="pointer-events-none absolute inset-0 opacity-40"
          style="
            background-image: linear-gradient(#d7dde3 1px, transparent 1px),
              linear-gradient(90deg, #d7dde3 1px, transparent 1px);
            background-size: 25px 25px;
          "
        ></div>

        <!-- EMPTY -->
        <div
          v-if="!filteredRooms.length"
          class="absolute inset-0 flex items-center justify-center"
        >
          <div class="text-center">
            <div
              class="mx-auto mb-3 flex h-14 w-14 items-center justify-center rounded-full bg-white shadow-sm"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-7 w-7 text-gray-300"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M3.75 6.75 9 4.5l6 2.25 5.25-2.25v13.5L15 20.25 9 18l-5.25 2.25V6.75Z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9 4.5V18m6-11.25v13.5"
                />
              </svg>
            </div>

            <p class="text-sm font-semibold text-gray-500">
              No rooms available
            </p>

            <p class="mt-1 text-xs text-gray-400">
              No rooms matched the current schedule requirements.
            </p>
          </div>
        </div>

        <!-- SVG MAP -->
        <div v-else class="relative z-10 min-w-full min-h-full p-8">
          <svg
            :viewBox="`0 0 ${mapWidth} ${mapHeight}`"
            :width="mapWidth * zoom"
            :height="mapHeight * zoom"
            xmlns="http://www.w3.org/2000/svg"
            class="block mx-auto"
          >
            <!-- ===================================================== -->
            <!-- SITE MAP -->
            <!-- ===================================================== -->
            <g>
              <!-- Campus Ground -->
              <rect
                x="10"
                y="10"
                :width="mapWidth - 20"
                :height="mapHeight - 20"
                rx="20"
                fill="#f8fafc"
                stroke="#d8dee5"
                stroke-width="2"
              />

              <!-- Ground title -->
              <text
                x="40"
                y="50"
                font-size="18"
                font-weight="700"
                fill="#475569"
              >
                Campus Room Map
              </text>

              <text x="40" y="72" font-size="11" fill="#94a3b8">
                {{ buildings.length }}
                {{ buildings.length === 1 ? "building" : "buildings" }}
                ·
                {{ filteredRooms.length }}
                {{ filteredRooms.length === 1 ? "room" : "rooms" }}
              </text>

              <!-- ================================================= -->
              <!-- BUILDINGS -->
              <!-- ================================================= -->
              <g v-for="building in buildings" :key="building.id">
                <!-- Building shadow -->
                <rect
                  :x="building.x + 5"
                  :y="building.y + 6"
                  :width="building.width"
                  :height="building.height"
                  rx="12"
                  fill="#cbd5e1"
                  opacity="0.35"
                />

                <!-- Building -->
                <rect
                  :x="building.x"
                  :y="building.y"
                  :width="building.width"
                  :height="building.height"
                  rx="12"
                  fill="#ffffff"
                  stroke="#94a3b8"
                  stroke-width="2"
                />

                <!-- Building Header -->
                <rect
                  :x="building.x"
                  :y="building.y"
                  :width="building.width"
                  height="48"
                  rx="12"
                  fill="#334155"
                />

                <!-- Remove bottom rounding visually -->
                <rect
                  :x="building.x"
                  :y="building.y + 35"
                  :width="building.width"
                  height="13"
                  fill="#334155"
                />

                <!-- Building Icon -->
                <rect
                  :x="building.x + 16"
                  :y="building.y + 13"
                  width="22"
                  height="22"
                  rx="5"
                  fill="#ffffff"
                  opacity="0.16"
                />

                <path
                  :d="buildingIconPath(building.x + 20, building.y + 17)"
                  fill="none"
                  stroke="#ffffff"
                  stroke-width="1.4"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />

                <!-- Building Name -->
                <text
                  :x="building.x + 50"
                  :y="building.y + 25"
                  font-size="13"
                  font-weight="700"
                  fill="#ffffff"
                >
                  {{ building.name }}
                </text>

                <!-- Room Count -->
                <text
                  :x="building.x + 50"
                  :y="building.y + 39"
                  font-size="9"
                  fill="#cbd5e1"
                >
                  {{ building.rooms.length }}
                  {{ building.rooms.length === 1 ? "room" : "rooms" }}
                </text>

                <!-- ================================================= -->
                <!-- ROOMS -->
                <!-- ================================================= -->
                <g
                  v-for="room in building.rooms"
                  :key="room.room_id"
                  class="room-node"
                  :class="{
                    'room-selected': isSelected(room),
                  }"
                  @click="selectRoom(room)"
                >
                  <!-- Room shadow -->
                  <rect
                    :x="room.x + 2"
                    :y="room.y + 3"
                    :width="room.width"
                    :height="room.height"
                    rx="7"
                    fill="#94a3b8"
                    opacity="0.18"
                  />

                  <!-- Room -->
                  <rect
                    :x="room.x"
                    :y="room.y"
                    :width="room.width"
                    :height="room.height"
                    rx="7"
                    :fill="getRoomFill(room.room_type)"
                    :stroke="
                      isSelected(room)
                        ? '#111827'
                        : getRoomStroke(room.room_type)
                    "
                    :stroke-width="isSelected(room) ? 3 : 1.5"
                  />

                  <!-- Selected indicator -->
                  <circle
                    v-if="isSelected(room)"
                    :cx="room.x + room.width - 11"
                    :cy="room.y + 11"
                    r="6"
                    fill="#111827"
                  />

                  <path
                    v-if="isSelected(room)"
                    :d="`M${room.x + room.width - 14} ${room.y + 11}
                       l2 2
                       l4 -5`"
                    fill="none"
                    stroke="#ffffff"
                    stroke-width="1.5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />

                  <!-- Room Name -->
                  <text
                    :x="room.x + room.width / 2"
                    :y="room.y + 22"
                    text-anchor="middle"
                    font-size="11"
                    font-weight="700"
                    fill="#1f2937"
                    pointer-events="none"
                  >
                    {{ truncateRoomName(room.room_name) }}
                  </text>

                  <!-- Room Type -->
                  <text
                    :x="room.x + room.width / 2"
                    :y="room.y + 36"
                    text-anchor="middle"
                    font-size="8"
                    font-weight="700"
                    fill="#64748b"
                    pointer-events="none"
                  >
                    {{ getRoomTypeLabel(room.room_type) }}
                  </text>

                  <!-- Capacity -->
                  <text
                    :x="room.x + room.width / 2"
                    :y="room.y + 47"
                    text-anchor="middle"
                    font-size="7"
                    fill="#94a3b8"
                    pointer-events="none"
                  >
                    CAP:
                    {{ room.room_capacity || "-" }}
                  </text>
                </g>
              </g>
            </g>
          </svg>
        </div>

        <!-- ======================================================= -->
        <!-- LEGEND -->
        <!-- ======================================================= -->
        <div
          class="absolute bottom-4 left-4 z-20 flex flex-wrap items-center gap-3 rounded-xl border border-gray-200 bg-white/95 px-4 py-3 shadow-lg backdrop-blur"
        >
          <div class="flex items-center gap-2">
            <span
              class="h-3 w-3 rounded-sm border border-blue-300 bg-blue-100"
            ></span>
            <span class="text-[10px] font-medium text-gray-600"> Lecture </span>
          </div>

          <div class="flex items-center gap-2">
            <span
              class="h-3 w-3 rounded-sm border border-purple-300 bg-purple-100"
            ></span>
            <span class="text-[10px] font-medium text-gray-600">
              Laboratory
            </span>
          </div>

          <div class="flex items-center gap-2">
            <span
              class="h-3 w-3 rounded-sm border-2 border-gray-900 bg-white"
            ></span>
            <span class="text-[10px] font-medium text-gray-600">
              Selected
            </span>
          </div>
        </div>
      </div>

      <!-- ========================================================= -->
      <!-- FOOTER -->
      <!-- ========================================================= -->
      <div
        class="flex shrink-0 items-center justify-between gap-4 border-t bg-white px-5 py-3"
      >
        <!-- SELECTED ROOM -->
        <div class="min-w-0">
          <template v-if="selectedRoom">
            <p
              class="text-[9px] font-semibold uppercase tracking-wide text-gray-400"
            >
              Selected Room
            </p>

            <div class="mt-0.5 flex items-center gap-2">
              <span class="truncate text-sm font-semibold text-gray-800">
                {{ selectedRoom.room_name }}
              </span>

              <span
                class="shrink-0 rounded-full border px-2 py-0.5 text-[9px] font-bold uppercase"
                :class="getRoomTypeBadgeClass(selectedRoom.room_type)"
              >
                {{ getRoomTypeLabel(selectedRoom.room_type) }}
              </span>

              <span class="text-[10px] text-gray-400">
                Capacity:
                {{ selectedRoom.room_capacity || "-" }}
              </span>
            </div>
          </template>

          <template v-else>
            <p class="text-xs text-gray-400">
              Click a room on the map to select it.
            </p>
          </template>
        </div>

        <!-- ACTIONS -->
        <div class="flex shrink-0 items-center gap-2">
          <button
            type="button"
            class="h-9 rounded-lg border border-gray-200 bg-white px-4 text-xs font-medium text-gray-600 transition hover:bg-gray-50"
            @click="closeModal"
          >
            Cancel
          </button>

          <button
            type="button"
            :disabled="!selectedRoom"
            class="h-9 rounded-lg bg-emerald-600 px-5 text-xs font-semibold text-white shadow-sm transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-gray-300"
            @click="confirmSelection"
          >
            Select Room
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RoomMapModal",

  props: {
    show: {
      type: Boolean,
      default: false,
    },

    rooms: {
      type: Array,
      default: () => [],
    },

    selectedRoomId: {
      type: [Number, String, null],
      default: null,
    },
  },

  emits: ["close", "select-room"],

  data() {
    return {
      searchQuery: "",
      selectedRoom: null,
      zoom: 1,

      ROOM_WIDTH: 118,
      ROOM_HEIGHT: 58,
      ROOM_GAP: 10,

      BUILDING_PADDING: 18,
      BUILDING_HEADER: 48,

      BUILDING_WIDTH: 570,
      BUILDING_GAP_X: 70,
      BUILDING_GAP_Y: 65,

      SITE_MARGIN_X: 40,
      SITE_MARGIN_Y: 110,

      BUILDINGS_PER_ROW: 2,
    };
  },

  computed: {
    /**
     * Filter rooms based on the search box.
     *
     * IMPORTANT:
     * The parent already passes filteredRooms(expandedRecord),
     * so this does NOT replace the parent's room filtering.
     */
    filteredRooms() {
      const query = String(this.searchQuery || "")
        .trim()
        .toLowerCase();

      if (!query) {
        return this.rooms || [];
      }

      return (this.rooms || []).filter((room) => {
        const roomName = String(room?.room_name || "").toLowerCase();
        const roomType = String(room?.room_type || "").toLowerCase();

        const buildingName = String(
          room?.building?.building_name ||
            room?.building?.name ||
            room?.building_name ||
            "",
        ).toLowerCase();

        return (
          roomName.includes(query) ||
          roomType.includes(query) ||
          buildingName.includes(query)
        );
      });
    },

    /**
     * Automatically creates a 2D building layout.
     *
     * No database map coordinates are required yet.
     */
    buildings() {
      const groups = {};

      this.filteredRooms.forEach((room, index) => {
        const buildingId = this.getBuildingId(room);

        if (!groups[buildingId]) {
          groups[buildingId] = {
            id: buildingId,
            name: this.getBuildingName(room),
            rooms: [],
          };
        }

        groups[buildingId].rooms.push({
          ...room,
          _originalIndex: index,
        });
      });

      const rawBuildings = Object.values(groups);

      const columns = this.BUILDINGS_PER_ROW;

      const buildingRows = [];

      for (let i = 0; i < rawBuildings.length; i += columns) {
        buildingRows.push(rawBuildings.slice(i, i + columns));
      }

      const layouts = [];

      let currentY = this.SITE_MARGIN_Y;

      buildingRows.forEach((row) => {
        let rowHeight = 0;

        const preparedRow = row.map((building, columnIndex) => {
          const roomColumns = 4;

          const roomRows = Math.max(
            1,
            Math.ceil(building.rooms.length / roomColumns),
          );

          const roomAreaHeight =
            roomRows * (this.ROOM_HEIGHT + this.ROOM_GAP) - this.ROOM_GAP;

          const buildingHeight =
            this.BUILDING_HEADER + this.BUILDING_PADDING * 2 + roomAreaHeight;

          rowHeight = Math.max(rowHeight, buildingHeight);

          const x =
            this.SITE_MARGIN_X +
            columnIndex * (this.BUILDING_WIDTH + this.BUILDING_GAP_X);

          const y = currentY;

          const rooms = building.rooms.map((room, roomIndex) => {
            const col = roomIndex % roomColumns;
            const roomRow = Math.floor(roomIndex / roomColumns);

            const xPosition =
              x +
              this.BUILDING_PADDING +
              col * (this.ROOM_WIDTH + this.ROOM_GAP);

            const yPosition =
              y +
              this.BUILDING_HEADER +
              this.BUILDING_PADDING +
              roomRow * (this.ROOM_HEIGHT + this.ROOM_GAP);

            return {
              ...room,

              x: xPosition,
              y: yPosition,

              width: this.ROOM_WIDTH,
              height: this.ROOM_HEIGHT,
            };
          });

          return {
            ...building,
            x,
            y,
            width: this.BUILDING_WIDTH,
            height: buildingHeight,
            rooms,
          };
        });

        layouts.push(...preparedRow);

        currentY += rowHeight + this.BUILDING_GAP_Y;
      });

      return layouts;
    },

    mapWidth() {
      const columns = Math.min(
        this.BUILDINGS_PER_ROW,
        Math.max(this.buildings.length, 1),
      );

      return (
        this.SITE_MARGIN_X * 2 +
        columns * this.BUILDING_WIDTH +
        Math.max(columns - 1, 0) * this.BUILDING_GAP_X
      );
    },

    mapHeight() {
      if (!this.buildings.length) {
        return 700;
      }

      let maxY = 0;

      this.buildings.forEach((building) => {
        maxY = Math.max(maxY, building.y + building.height);
      });

      return maxY + this.SITE_MARGIN_Y;
    },
  },

  watch: {
    show(newValue) {
      if (newValue) {
        this.searchQuery = "";
        this.zoom = 1;

        this.$nextTick(() => {
          this.setInitialSelectedRoom();
        });
      }
    },

    rooms: {
      deep: true,

      handler() {
        if (this.show) {
          this.setInitialSelectedRoom();
        }
      },
    },

    selectedRoomId() {
      if (this.show) {
        this.setInitialSelectedRoom();
      }
    },
  },

  methods: {
    // ============================================================
    // BUILDING HELPERS
    // ============================================================

    getBuildingId(room) {
      return (
        room?.building?.building_id ??
        room?.building_id ??
        room?.building?.id ??
        `building-${room?.room_id ?? "unknown"}`
      );
    },

    getBuildingName(room) {
      return (
        room?.building?.building_name ||
        room?.building?.name ||
        room?.building_name ||
        "Building"
      );
    },

    buildingIconPath(x, y) {
      return `
        M ${x} ${y + 5}
        H ${x + 14}
        V ${y + 15}
        H ${x}
        Z
      `;
    },

    // ============================================================
    // ROOM HELPERS
    // ============================================================

    isLaboratory(roomType) {
      const type = String(roomType || "")
        .trim()
        .toLowerCase();

      return type.includes("lab") || type.includes("laboratory");
    },

    isLecture(roomType) {
      const type = String(roomType || "")
        .trim()
        .toLowerCase();

      return (
        type.includes("lecture") || type.includes("lec") || type === "classroom"
      );
    },

    getRoomTypeLabel(roomType) {
      if (this.isLaboratory(roomType)) {
        return "LAB";
      }

      if (this.isLecture(roomType)) {
        return "LECTURE";
      }

      return roomType || "ROOM";
    },

    getRoomFill(roomType) {
      if (this.isLaboratory(roomType)) {
        return "#f3e8ff";
      }

      if (this.isLecture(roomType)) {
        return "#dbeafe";
      }

      return "#f1f5f9";
    },

    getRoomStroke(roomType) {
      if (this.isLaboratory(roomType)) {
        return "#c084fc";
      }

      if (this.isLecture(roomType)) {
        return "#60a5fa";
      }

      return "#cbd5e1";
    },

    getRoomTypeBadgeClass(roomType) {
      if (this.isLaboratory(roomType)) {
        return "border-purple-200 bg-purple-100 text-purple-700";
      }

      if (this.isLecture(roomType)) {
        return "border-blue-200 bg-blue-100 text-blue-700";
      }

      return "border-gray-200 bg-gray-100 text-gray-600";
    },

    truncateRoomName(name) {
      const value = String(name || "Room");

      if (value.length <= 17) {
        return value;
      }

      return `${value.substring(0, 15)}...`;
    },

    isSelected(room) {
      if (!this.selectedRoom) {
        return false;
      }

      return Number(this.selectedRoom.room_id) === Number(room.room_id);
    },

    setInitialSelectedRoom() {
      if (!this.selectedRoomId) {
        this.selectedRoom = null;
        return;
      }

      const room = (this.rooms || []).find(
        (item) => Number(item?.room_id) === Number(this.selectedRoomId),
      );

      this.selectedRoom = room || null;
    },

    // ============================================================
    // ROOM SELECTION
    // ============================================================

    selectRoom(room) {
      if (!room) {
        return;
      }

      this.selectedRoom = room;
    },

    confirmSelection() {
      if (!this.selectedRoom) {
        return;
      }

      this.$emit("select-room", this.selectedRoom);
    },

    closeModal() {
      this.$emit("close");
    },

    // ============================================================
    // ZOOM
    // ============================================================

    zoomIn() {
      this.zoom = Math.min(Number((this.zoom + 0.1).toFixed(2)), 1.8);
    },

    zoomOut() {
      this.zoom = Math.max(Number((this.zoom - 0.1).toFixed(2)), 0.6);
    },

    resetZoom() {
      this.zoom = 1;
    },
  },
};
</script>

<style scoped>
.room-node {
  cursor: pointer;
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.room-node:hover {
  opacity: 0.85;
}

.room-node rect {
  transition: fill 0.15s ease, stroke 0.15s ease;
}

.room-selected {
  filter: drop-shadow(0 2px 4px rgba(15, 23, 42, 0.25));
}
</style>
