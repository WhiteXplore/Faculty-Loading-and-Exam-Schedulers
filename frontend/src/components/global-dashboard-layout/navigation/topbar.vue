<template>
  <div
    class="bg-white shadow-md px-3 py-2 flex justify-between items-center rounded-t-lg"
  >
    <!-- Left: Title -->
    <div class="text-green-900 font-semibold text-md tracking-wide">
      Faculty Loading & Exam Scheduler
    </div>

    <!-- Center: Date -->
    <div class="flex flex-col items-center">
      <div class="text-sm font-medium text-gray-600">
        {{ formattedDate }}
      </div>
    </div>

    <!-- Right Section -->
    <div class="flex items-center gap-2">
      <!-- Dropdown -->
      <div v-if="activeYears.length > 1" class="relative flex items-center">
        <select
          v-model="selectedSchoolYearId"
          @change="updateSchoolYear"
          @focus="isDropdownOpen = true"
          @blur="isDropdownOpen = false"
          class="appearance-none rounded-xl border border-green-600 bg-white py-2 pl-4 pr-10 text-center text-green-900 text-sm font-semibold cursor-pointer transition-all duration-200 focus:ring-2 focus:ring-green-500 focus:border-green-500 hover:shadow-lg"
        >
          <option value="" disabled>Select Active School Year</option>
          <option
            v-for="sy in activeYears"
            :key="sy.school_year_id"
            :value="sy.school_year_id"
          >
            {{ sy.school_year_name }} {{ getSemesterLabel(sy.semester) }}
          </option>
        </select>

        <!-- Icon -->
        <div
          class="pointer-events-none absolute right-3 flex items-center transition-transform duration-300 text-green-700"
          :class="{ 'rotate-180': isDropdownOpen }"
        >
          <svg
            class="w-5 h-5"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>

      <!-- Static -->
      <div
        v-else
        class="border border-green-600 rounded-xl px-4 py-1.5 text-green-900 text-sm font-semibold flex items-center justify-center"
      >
        <span v-if="activeYears.length === 1">
          {{ activeYears[0].school_year_name }}
          {{ getSemesterLabel(activeYears[0].semester) }}
        </span>
        <span v-else class="text-gray-500">No Active Year</span>
      </div>

      <!-- Profile -->
      <div class="flex items-center gap-2 cursor-pointer" @click.stop="toggleOpenProfile">
        <div
          ref="profileIcon"
          class="w-9 h-9 rounded-xl border border-green-600 cursor-pointer transition"
        >
          <img
            src="../../../assets/img/users1.png"
            class="w-full h-full rounded-full object-cover"
          />
        </div>

        <div class="text-left leading-tight">
          <h1 class="text-sm font-semibold text-gray-800">
            {{ user.last_name }}, {{ user.first_name || "Guest" }}
          </h1>
          <h2 class="text-xs text-gray-500">
            {{ user.role || "No Role" }}
          </h2>
        </div>
      </div>
    </div>
  </div>

  <!-- Profile Dropdown -->
  <div
    v-if="isOpenProfile"
    ref="profileDropdown"
    class="absolute top-[70px] right-6 z-50"
  >
    <Profile />
  </div>
</template>

<script>
import axios from "axios";
import Profile from "./profile-setting.vue";
import { eventBus } from "@/bus/event-bus";

export default {
  name: "TopBarPage",
  components: { Profile },

  data() {
    return {
      isOpenProfile: false,
      user: {},
      schoolYears: [],
      selectedSchoolYearId: "",
      currentTime: new Date(),
      isDropdownOpen: false,
      stopBus: null,
    };
  },

  computed: {
    formattedDate() {
      return this.currentTime.toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "2-digit",
        year: "numeric",
      });
    },
    activeYears() {
      return this.schoolYears.filter((y) => y.is_active);
    },
  },

  methods: {
    toggleOpenProfile() {
      this.isOpenProfile = !this.isOpenProfile;
    },

    handleClickOutside(event) {
      const dropdown = this.$refs.profileDropdown;
      const icon = this.$refs.profileIcon;

      if (
        this.isOpenProfile &&
        dropdown &&
        !dropdown.contains(event.target) &&
        icon &&
        !icon.contains(event.target)
      ) {
        this.isOpenProfile = false;
      }
    },

    async fetchUser() {
      try {
        const res = await axios.get(process.env.VUE_APP_API_BASE_URL + "/auth/me", {
          withCredentials: true,
        });
        this.user = res.data || {};
      } catch {
        this.$router.push("/");
      }
    },

    async fetchSchoolYears() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years"
        );

        this.schoolYears = res.data.map((y) => ({ ...y }));

        if (!this.selectedSchoolYearId) {
          this.autoSelectActiveYear();
        }
      } catch (err) {
        console.error(err);
      }
    },

    autoSelectActiveYear() {
      const activeList = this.activeYears.sort(
        (a, b) => new Date(b.updated_at) - new Date(a.updated_at)
      );

      if (activeList.length > 0) {
        this.selectedSchoolYearId = activeList[0].school_year_id;
        eventBus.emit(activeList[0]);
      }
    },

    getSemesterLabel(sem) {
      return sem === 1 ? "1st Semester" : sem === 2 ? "2nd Semester" : "";
    },

    async updateSchoolYear() {
      const selectedSY = this.schoolYears.find(
        (y) => y.school_year_id === this.selectedSchoolYearId
      );

      if (!selectedSY) return;

      try {
        await axios.patch(
          process.env.VUE_APP_API_BASE_URL +
            `/school-year/update-timestamp/${selectedSY.school_year_id}`
        );

        eventBus.emit(selectedSY);
      } catch (err) {
        console.error(err);
      }
    },
  },

  mounted() {
    this.fetchUser();
    this.fetchSchoolYears();

    // ✅ Click outside listener
    document.addEventListener("click", this.handleClickOutside);

    this.stopBus = eventBus.on(async (newSY) => {
      if (!newSY) return;

      await this.fetchSchoolYears();

      if (newSY.is_active) {
        this.selectedSchoolYearId = newSY.school_year_id;
      }
    });
  },

  beforeUnmount() {
    if (this.stopBus) this.stopBus();

    // ✅ Cleanup
    document.removeEventListener("click", this.handleClickOutside);
  },
};
</script>
