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

      <div class="relative w-[230px]">
        <button
          type="button"
          @click="isDropdownOpen = !isDropdownOpen"
          class="flex w-full items-center justify-between rounded-xl border border-gray-200 bg-white px-2 py-1 shadow-sm transition-all duration-300 hover:border-green-300 hover:shadow-md"
        >
          <div class="flex items-center gap-3">
            <div
              class="flex h-7 w-7 items-center justify-center rounded-md bg-green-50 text-gray-700"
            >
              <icon name="calendar" />
            </div>

            <div class="text-left">
              <p class="text-sm text-gray-800">
                {{
                  activeYears.find((sy) => sy.school_year_id === selectedSchoolYearId)
                    ? activeYears.find((sy) => sy.school_year_id === selectedSchoolYearId)
                        .school_year_name +
                      " • " +
                      getSemesterLabel(
                        activeYears.find(
                          (sy) => sy.school_year_id === selectedSchoolYearId
                        ).semester
                      )
                    : "Select School Year"
                }}
              </p>
            </div>
          </div>

          <svg
            class="h-4 w-4 text-gray-500 transition-transform duration-300"
            :class="{ 'rotate-180': isDropdownOpen }"
            fill="none"
            stroke="currentColor"
            stroke-width="2.4"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <div
          v-if="isDropdownOpen"
          class="absolute right-0 z-50 mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
        >
          <button
            v-for="sy in activeYears"
            :key="sy.school_year_id"
            type="button"
            @click="
              selectedSchoolYearId = sy.school_year_id;
              updateSchoolYear();
              isDropdownOpen = false;
            "
            class="flex w-full items-center justify-between px-4 py-3 text-left transition hover:bg-green-50"
            :class="
              selectedSchoolYearId === sy.school_year_id ? 'bg-green-50' : 'bg-white'
            "
          >
            <div>
              <p class="text-sm font-semibold text-gray-800">
                {{ sy.school_year_name }}
              </p>
              <p class="text-xs text-gray-500">
                {{ getSemesterLabel(sy.semester) }}
              </p>
            </div>

            <span
              v-if="selectedSchoolYearId === sy.school_year_id"
              class="rounded-full bg-green-100 px-2 py-1 text-[10px] font-bold text-green-700"
            >
              Active
            </span>
          </button>
        </div>
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

        <!-- <div class="text-left leading-tight">
          <h1 class="text-sm font-semibold text-gray-800">
            {{ user.last_name }}, {{ user.first_name || "Guest" }}
          </h1>
          <h2 class="text-xs text-gray-500">
            {{ user.role || "No Role" }}
          </h2>
        </div> -->
      </div>
    </div>
  </div>

  <!-- Profile Dropdown -->
  <div
    v-if="isOpenProfile"
    ref="profileDropdown"
    class="absolute top-[68px] right-1 z-50"
  >
    <Profile />
  </div>
</template>

<script>
import axios from "axios";
import Profile from "./profile-setting.vue";
import { eventBus } from "@/bus/event-bus";
import icon from "@/assets/icon.vue";
export default {
  name: "TopBarPage",
  components: { Profile, icon },

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
      return sem === 1 ? "1st Sem" : sem === 2 ? "2nd Sem" : "";
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
