<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form
        @submit.prevent="submitData"
        class="modal-container"
        ref="roomsForm"
      >
        <!-- HEADER -->

        <div class="modal-header">
          <div class="flex items-center gap-3">
            <!-- Icon -->
            <div class="glass-container">
              <icon name="circle-add2" class="text-white" />
            </div>

            <!-- Title -->
            <div>
              <h2 class="text-lg font-semibold text-white">
                {{ isEdit ? "Edit Room" : "Add Room" }}
              </h2>

              <p class="text-xs text-green-100">
                View, add, and update room details
              </p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <!-- BODY -->
        <div class="w-[30vw] modal-body">
          <div class="w-full space-y-2">
            <label class="input-label">Room Name:</label>

            <input
              v-model="form.room_name"
              type="text"
              required
              class="input-text"
              placeholder="Enter room name"
            />
          </div>

          <div class="dropdown-container">
            <label class="dropdown-label">Room Type:</label>

            <div class="dropdown-wrapper">
              <!-- DISPLAY (acts like select) -->
              <div
                class="dropdown-input cursor-pointer flex items-center justify-between"
                @click="showRoomTypeDropdown = !showRoomTypeDropdown"
              >
                <span :class="form.room_type ? '' : 'text-gray-400'">
                  {{ form.room_type || "Select Room Type" }}
                </span>

                <!-- ARROW -->
                <svg
                  class="w-4 h-4 ml-2 transition-transform duration-200"
                  :class="{ 'rotate-180': showRoomTypeDropdown }"
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

              <!-- DROPDOWN -->
              <div v-if="showRoomTypeDropdown" class="dropdown-menu">
                <div
                  v-for="type in roomTypes"
                  :key="type"
                  class="dropdown-item"
                  @click="selectRoomType(type)"
                >
                  {{ type }}
                </div>
              </div>
            </div>
          </div>

          <!-- Room Capacity -->
          <div class="w-full space-y-2">
            <label class="input-label">Room Capacity:</label>

            <input
              v-model="form.room_capacity"
              type="number"
              required
              class="input-text"
              placeholder="Enter room capacity"
            />
          </div>
          <!-- Institute -->
          <div class="flex flex-col space-y-2 w-full relative">
            <label class="input-label">Institute :</label>

            <input
              v-model="searchInstituteQuery"
              type="text"
              placeholder="Search institute..."
              class="input-text"
              @focus="showInstituteDropdown = true"
              :disabled="form.room_type === 'Lecture'"
            />

            <div
              v-if="showInstituteDropdown && filteredInstitutes.length"
              class="absolute top-[60px] w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-10"
              @mouseleave="showInstituteDropdown = false"
            >
              <div
                v-for="institute in filteredInstitutes"
                :key="institute.institute_id"
                class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                @mousedown="selectInstitute(institute)"
              >
                {{ institute.institute_code }} -
                {{ institute.institute_name }}
              </div>
            </div>
          </div>

          <!-- Building -->
          <div class="dropdown-container">
            <label class="dropdown-label">Building :</label>
            <div class="dropdown-wrapper">
              <input
                v-model="searchBuildingQuery"
                type="text"
                placeholder="Search building..."
                class="dropdown-input"
                @focus="showBuildingDropdown = true"
              />
              <div
                v-if="showBuildingDropdown"
                class="dropdown-menu"
                @mouseleave="showBuildingDropdown = false"
              >
                <div v-if="filteredBuildings.length">
                  <div
                    v-for="building in filteredBuildings"
                    :key="building.building_id"
                    class="dropdown-item"
                    @mousedown="selectBuilding(building)"
                  >
                    {{
                      building.buildingArea?.collegeBranch?.college_branch_name
                    }}
                    -
                    {{ building.buildingArea?.area_name }}
                    -
                    {{ building.building_name }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Status -->
          <div class="w-full space-y-2 text-left flex flex-col">
            <label class="input-label">Room Status:</label>

            <div
              class="flex items-center justify-between rounded-xl border border-gray-200 px-4 py-3 bg-gray-50"
            >
              <div class="flex flex-col">
                <span class="font-medium text-sm text-gray-700">
                  {{ form.is_active ? "Active" : "Inactive" }}
                </span>

                <span class="text-xs text-gray-400">
                  Room can only be used when active
                </span>
              </div>

              <button
                type="button"
                @click="form.is_active = !form.is_active"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition',
                  form.is_active ? 'bg-green-500' : 'bg-gray-300',
                ]"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition',
                    form.is_active ? 'translate-x-6' : 'translate-x-1',
                  ]"
                />
              </button>
            </div>
          </div>

          <!-- Divider -->
          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <!-- Buttons -->
          <div class="tracking-wide flex justify-end gap-2 mt-4">
            <button type="button" class="btn-cancel" @click="$emit('close')">
              Cancel
            </button>

            <button type="submit" class="btn-save">
              {{ isEditMode ? "Save Changes" : "Submit" }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import axios from "axios";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "RoomFormModal",

  props: {
    roomData: {
      type: Object,
      default: null,
    },
  },

  components: { icon },
  data() {
    return {
      roomTypes: ["Lecture", "Laboratory"],

      showRoomTypeDropdown: false,

      form: {
        institute_id: "",
        building_id: "",
        room_name: "",
        room_type: "",
        room_capacity: "",
        is_active: true,
      },

      searchInstituteQuery: "",
      showInstituteDropdown: false,

      searchBuildingQuery: "",
      showBuildingDropdown: false,
    };
  },
  watch: {
    "form.room_type"(newType, oldType) {
      // Only clear when user actually changes room type, not while loading edit data
      if (!oldType) return;

      if (newType === "Lecture") {
        this.form.institute_id = null;
        this.searchInstituteQuery = "";
        // DO NOT clear building_id
      }

      if (newType === "Laboratory") {
        this.form.institute_id = null;
        this.searchInstituteQuery = "";
        // DO NOT clear building_id
      }
    },
  },
  computed: {
    ...mapState(useFetchDataStore, ["institutes", "buildings"]),

    filteredInstitutes() {
      if (!this.searchInstituteQuery) return this.institutes;

      return this.institutes.filter((institute) =>
        institute.institute_name
          .toLowerCase()
          .includes(this.searchInstituteQuery.toLowerCase()),
      );
    },

    filteredBuildings() {
      let filtered = this.buildings;

      if (this.searchBuildingQuery) {
        filtered = filtered.filter((building) =>
          building.building_name
            .toLowerCase()
            .includes(this.searchBuildingQuery.toLowerCase()),
        );
      }

      // Sort by Area number (Area 1 → Area 7)
      return filtered.sort((a, b) => {
        const areaA =
          parseInt(a.buildingArea?.area_name?.replace("Area ", "")) || 0;
        const areaB =
          parseInt(b.buildingArea?.area_name?.replace("Area ", "")) || 0;

        return areaA - areaB;
      });
    },
    isEditMode() {
      return !!this.roomData;
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchInstitutes", "fetchBuildings"]),

    handleClickOutside(e) {
      if (!this.$el.contains(e.target)) {
        this.showRoomTypeDropdown = false;
        this.showStatusDropdown = false;
      }
    },
    selectStatus(status) {
      this.form.status = status;
      this.showStatusDropdown = false;
    },
    selectRoomType(type) {
      this.form.room_type = type;

      if (type === "Lecture") {
        this.form.institute_id = null;
        this.searchInstituteQuery = "";
      }

      this.showRoomTypeDropdown = false;
    },
    selectInstitute(institute) {
      this.form.institute_id = institute.institute_id;
      this.searchInstituteQuery = institute.institute_name;
      this.showInstituteDropdown = false;
    },
    selectBuilding(building) {
      this.form.building_id = building.building_id;

      this.searchBuildingQuery =
        building.buildingArea?.collegeBranch?.college_branch_name +
        " - " +
        building.buildingArea?.area_name +
        " - " +
        building.building_name;

      this.showBuildingDropdown = false;
    },

    formatBuilding(building) {
      return `${
        building.buildingArea?.collegeBranch?.college_branch_name || ""
      } - ${building.buildingArea?.area_name || ""} - ${
        building.building_name || ""
      }`;
    },

    async submitData() {
      const form = this.$refs.roomsForm;

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }
      if (!this.searchInstituteQuery) {
        this.form.institute_id = null;
      }

      if (!this.searchBuildingQuery) {
        this.form.building_id = null;
      }

      try {
        const payload = {
          room_name: this.form.room_name,
          room_type: this.form.room_type,
          room_capacity: Number(this.form.room_capacity),

          is_active: this.form.is_active,

          institute_id:
            this.form.institute_id === "" || this.form.institute_id === null
              ? null
              : Number(this.form.institute_id),

          building_id:
            this.form.building_id === "" || this.form.building_id === null
              ? null
              : Number(this.form.building_id),
        };

        if (this.isEditMode) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/rooms/update-room/${this.roomData.room_id}`,
            payload,
          );

          toast.success("Room updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/rooms/add-rooms",
            payload,
          );

          toast.success("Room added successfully!");
        }

        const audio = new Audio(require("@/assets/add.mp3"));
        audio.play();

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        toast.error(
          this.isEditMode ? "Failed to update room" : "Failed to add room",
        );
      }
    },
  },

  mounted() {
    this.fetchInstitutes();
    this.fetchBuildings();

    if (this.isEditMode) {
      this.form = {
        institute_id: this.roomData.institute?.institute_id || "",
        building_id: this.roomData.building?.building_id || "",
        room_name: this.roomData.room_name,
        room_type: this.roomData.room_type,
        room_capacity: this.roomData.room_capacity,
        is_active: this.roomData.is_active ?? true,
      };

      this.searchInstituteQuery = this.roomData.institute?.institute_name || "";

      this.searchBuildingQuery = this.roomData.building
        ? this.formatBuilding(this.roomData.building)
        : "";
    }
    document.addEventListener("click", this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    transform: translateY(40px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slideUp {
  animation: fadeInUp 0.3s ease-out;
}
</style>
