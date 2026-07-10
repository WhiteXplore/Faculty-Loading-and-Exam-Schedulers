<template>
  <div class="modal-overlay">
    <div class="rounded-[16px] shadow-lg animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="bg-white text-[13px] rounded-[16px] shadow-lg"
        ref="areaForm"
      >
        <!-- HEADER -->
        <!-- <div class="modal-header">
          <div class="flex gap-1 items-center">
            <icon name="circle-add" />
           <h1 class="header1">
              {{ isEditMode ? "Edit Building Area" : "Add Building Area" }}
            </h1>
          </div>

          <icon
            name="circle-close3"
            @click="$emit('close')"
            class="cursor-pointer"
          />
        </div> -->

        <div class="modal-header">
          <div class="flex items-center gap-3">
            <!-- Icon -->
            <div class="glass-container">
              <icon name="circle-add2" class="text-white" />
            </div>

            <!-- Title -->
            <div>
              <h2 class="text-lg font-semibold text-white">
                {{ isEdit ? "Edit Building Area" : "Add Building Area" }}
              </h2>

              <p class="text-xs text-green-100">
                View, add, and update building area details
              </p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <!-- FORM -->
        <div class="p-5 w-[28vw] space-y-4">
          <!-- COLLEGE BRANCH -->
          <div class="flex flex-col space-y-2 w-full relative">
            <label class="input-label">College Branch :</label>

            <input
              v-model="searchBranchQuery"
              type="text"
              placeholder="Search branch..."
              class="px-3 py-3 border border-gray-600 rounded-md"
              @focus="showBranchDropdown = true"
            />

            <div
              v-if="showBranchDropdown && filteredBranches.length"
              class="dropdown-menu"
              @mouseleave="showBranchDropdown = false"
            >
              <div
                v-for="branch in filteredBranches"
                :key="branch.college_branch_id"
                class="dropdown-item"
                @mousedown="selectBranch(branch)"
              >
                {{ branch.college_branch_name }}
              </div>
            </div>
          </div>

          <!-- AREA NAME -->
          <div class="w-full space-y-2">
            <label class="input-label">Area Name:</label>
            <input
              v-model="form.area_name"
              type="text"
              required
              class="input-text"
              placeholder="Enter area name"
            />
          </div>

          <!-- TRAVEL TIME -->
          <div class="dropdown-container">
            <label class="dropdown-label">Travel Time:</label>

            <div class="dropdown-wrapper">
              <!-- DISPLAY -->
              <div
                class="dropdown-input cursor-pointer flex items-center justify-between"
                @click="showTimeTravel = !showTimeTravel"
              >
                <span :class="form.time_travel ? '' : 'text-gray-400'">
                  {{ selectedTravelLabel || "Select Travel Time" }}
                </span>

                <!-- ARROW -->
                <svg
                  class="w-4 h-4 ml-2 transition-transform duration-200"
                  :class="{ 'rotate-180': showTimeTravel }"
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
              <div v-if="showTimeTravel" class="dropdown-menu">
                <div
                  v-for="time in travelTimes"
                  :key="time.value"
                  class="dropdown-item"
                  @click="selectTravelTime(time)"
                >
                  {{ time.label }}
                </div>
              </div>
            </div>
          </div>

          <!-- BUTTONS -->
          <div class="tracking-wide flex justify-end gap-2 pt-3">
            <button type="button" @click="$emit('close')" class="btn-cancel">
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
  <div
    v-if="showDeleteModal"
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50 w-min-screen"
  >
    <div
      class="rounded-xl shadow-lg w-[300px] md:w-[400px] bg-white py-6 px-4 flex flex-col items-center fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50"
    >
      <div
        class="rounded-full w-16 h-16 md:w-20 md:h-20 flex justify-center items-center bg-red-300 animate-pulse"
      >
        <icon
          name="question"
          class="w-8 h-8 md:w-10 md:h-10 text-white flex justify-center items-center"
        />
      </div>

      <h1 class="text-[14px] md:text-[16px] font-semibold mt-4">
        Delete Confirmation
      </h1>
      <p class="mt-2 text-[12px] md:text-[13px] text-center px-8">
        Are you sure you want to delete this record? This action cannot be
        undone.
      </p>

      <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

      <div class="tracking-wide flex gap-2 mt-4">
        <button
          class="bg-red-400 p-2 px-3 text-[11px] md:text-[13px] rounded-md text-white hover:bg-white border hover:border-red-800 hover:text-red-800 hover:shadow-md"
          @click="showDeleteModal = false"
        >
          No, Cancel
        </button>
        <button
          class="bg-green-400 p-2 px-3 text-[11px] md:text-[13px] rounded-md text-white hover:bg-white border hover:border-green-800 hover:text-green-800 hover:shadow-md"
          @click="confirmDelete"
        >
          Yes, Delete
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "BuildingAreaModal",

  components: { icon },

  props: {
    buildingData: {
      type: Object,
      default: null,
    },
  },

  data() {
    return {
      form: {
        building_area_id: null,
        area_name: "",
        time_travel: "",
        college_branch_id: "",
      },

      searchBranchQuery: "",
      showBranchDropdown: false,
      travelTimes: [
        { value: 15, label: "15 Minutes" },
        { value: 30, label: "30 Minutes" },
        { value: 60, label: "1 Hour" },
        { value: 90, label: "1 Hour 30 Minutes" },
        { value: 120, label: "2 Hours" },
        { value: 150, label: "2 Hours 30 Minutes" },
        { value: 180, label: "3 Hours" },
      ],
      showTimeTravel: false,
    };
  },

  computed: {
    isEditMode() {
      return !!this.buildingData;
    },

    ...mapState(useFetchDataStore, ["college_branch"]),

    filteredBranches() {
      const query = this.searchBranchQuery?.toLowerCase() || "";

      return this.college_branch
        .filter((b) => b.college_branch_name.toLowerCase().includes(query))
        .sort((a, b) =>
          a.college_branch_name.localeCompare(b.college_branch_name),
        );
    },
    selectedTravelLabel() {
      const selected = this.travelTimes.find(
        (t) => t.value === this.form.time_travel,
      );

      return selected ? selected.label : "";
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchCollegeBranch"]),
    selectTravelTime(time) {
      this.form.time_travel = time.value;
      this.showTimeTravel = false;
    },
    selectBranch(branch) {
      this.form.college_branch_id = branch.college_branch_id;
      this.searchBranchQuery = branch.college_branch_name;
      this.showBranchDropdown = false;
    },

    async submitData() {
      const form = this.$refs.areaForm;

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      try {
        const payload = {
          area_name: this.form.area_name,
          time_travel: Number(this.form.time_travel),
          college_branch_id: Number(this.form.college_branch_id),
        };

        if (this.isEditMode) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/building-areas/${this.form.building_area_id}`,
            payload,
          );

          toast.success("Building area updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL +
              "/building-areas/add-building-areas",
            payload,
          );

          toast.success("Building area created successfully!");
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        toast.error(
          error?.response?.data?.message || "Failed to save building area",
        );
      }
    },
  },

  mounted() {
    this.fetchCollegeBranch();

    if (this.isEditMode) {
      this.form = {
        ...this.form,
        ...this.buildingData,
      };

      this.searchBranchQuery =
        this.buildingData?.collegeBranch?.college_branch_name || "";
    }
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
