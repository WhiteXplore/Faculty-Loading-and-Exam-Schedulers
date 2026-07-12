<template>
  <div class="bg-white shadow-md rounded-t-lg px-3 py-3">
    <!-- MOBILE -->
    <div class="lg:hidden flex items-center">
      <!-- Left Spacer -->
      <div class="w-10"></div>

      <!-- Center School Year -->
      <div class="flex-1 flex justify-center">
        <div class="relative w-[75%]" ref="schoolYearDropdownRef">
          <div
            class="relative flex items-center rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200"
          >
            <div class="absolute left-3 text-defaultGreen">
              <icon name="calendar" />
            </div>

            <button
              type="button"
              @click.stop="isDropdownOpen = !isDropdownOpen"
              class="w-full rounded-xl bg-transparent py-2.5 pl-10 pr-10 text-left text-sm font-semibold text-gray-700 truncate"
            >
              <span
                v-if="
                  activeYears.find(
                    (sy) => sy.school_year_id === selectedSchoolYearId,
                  )
                "
              >
                {{
                  activeYears.find(
                    (sy) => sy.school_year_id === selectedSchoolYearId,
                  ).school_year_name
                }}
                -
                {{
                  getSemesterLabel(
                    activeYears.find(
                      (sy) => sy.school_year_id === selectedSchoolYearId,
                    ).semester,
                  )
                }}
              </span>

              <span v-else class="text-gray-400"> Select School Year </span>
            </button>

            <button
              type="button"
              @click.stop="isDropdownOpen = !isDropdownOpen"
              class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400"
            >
              <svg
                class="h-4 w-4 transition-transform duration-200"
                :class="{ 'rotate-180': isDropdownOpen }"
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
            v-if="isDropdownOpen"
            class="absolute left-0 right-0 z-50 mt-2 overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
          >
            <div class="border-b border-gray-100 px-4 py-3">
              <p
                class="text-xs font-semibold uppercase tracking-wide text-gray-400"
              >
                School Year Options
              </p>
            </div>

            <div class="max-h-[260px] overflow-y-auto p-1.5">
              <button
                v-for="sy in activeYears"
                :key="sy.school_year_id"
                type="button"
                @click="
                  selectedSchoolYearId = sy.school_year_id;
                  updateSchoolYear();
                  isDropdownOpen = false;
                "
                class="flex w-full items-center justify-between gap-3 rounded-lg px-3 py-2.5 text-left transition hover:bg-green-50"
                :class="
                  selectedSchoolYearId === sy.school_year_id
                    ? 'bg-green-50'
                    : ''
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
                  class="rounded-full px-2.5 py-1 text-[11px] font-semibold"
                  :class="
                    selectedSchoolYearId === sy.school_year_id
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-100 text-gray-500'
                  "
                >
                  {{
                    selectedSchoolYearId === sy.school_year_id
                      ? "Active"
                      : "Select"
                  }}
                </span>
              </button>

              <div
                v-if="activeYears.length === 0"
                class="px-4 py-6 text-center text-sm text-gray-400"
              >
                No school year found
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Profile -->
      <div
        class="w-10 flex justify-end cursor-pointer"
        @click.stop="toggleOpenProfile"
      >
        <div
          ref="profileIcon"
          class="w-10 h-10 rounded-xl border border-green-600 overflow-hidden"
        >
          <img
            src="../../../assets/img/users1.png"
            class="w-full h-full object-cover"
          />
        </div>
      </div>
    </div>

    <!-- DESKTOP -->
    <div class="hidden lg:flex justify-between items-center">
      <!-- Left -->
      <div class="text-green-900 font-semibold text-md tracking-wide">
        Faculty Loading & Exam Scheduler
      </div>

      <!-- Date -->
      <div class="text-sm font-medium text-gray-600">
        {{ formattedDate }}
      </div>
      <div class="flex gap-2">
        <!-- School Year -->
        <div class="relative w-[260px]" ref="schoolYearDropdownRef">
          <div
            class="relative flex items-center rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 focus-within:border-defaultGreen focus-within:ring-4 focus-within:ring-green-100"
          >
            <div class="absolute left-3 text-defaultGreen">
              <icon name="calendar" />
            </div>

            <button
              type="button"
              @click.stop="isDropdownOpen = !isDropdownOpen"
              class="w-full rounded-xl bg-transparent py-2.5 pl-10 pr-10 text-left text-sm font-semibold text-gray-700"
            >
              <span
                v-if="
                  activeYears.find(
                    (sy) => sy.school_year_id === selectedSchoolYearId,
                  )
                "
              >
                {{
                  activeYears.find(
                    (sy) => sy.school_year_id === selectedSchoolYearId,
                  ).school_year_name
                }}
                -
                {{
                  getSemesterLabel(
                    activeYears.find(
                      (sy) => sy.school_year_id === selectedSchoolYearId,
                    ).semester,
                  )
                }}
              </span>

              <span v-else class="text-gray-400"> Select School Year </span>
            </button>

            <button
              type="button"
              @click.stop="isDropdownOpen = !isDropdownOpen"
              class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400 transition hover:bg-gray-100 hover:text-defaultGreen"
            >
              <svg
                class="h-4 w-4 transition-transform duration-200"
                :class="{ 'rotate-180': isDropdownOpen }"
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
            v-if="isDropdownOpen"
            class="absolute right-0 z-50 mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
          >
            <div class="border-b border-gray-100 px-4 py-3">
              <p
                class="text-xs font-semibold uppercase tracking-wide text-gray-400"
              >
                School Year Options
              </p>
            </div>

            <div class="max-h-[260px] overflow-y-auto p-1.5">
              <button
                v-for="sy in activeYears"
                :key="sy.school_year_id"
                type="button"
                @click="
                  selectedSchoolYearId = sy.school_year_id;
                  updateSchoolYear();
                  isDropdownOpen = false;
                "
                class="flex w-full items-center justify-between gap-3 rounded-lg px-3 py-2.5 text-left transition hover:bg-green-50"
                :class="
                  selectedSchoolYearId === sy.school_year_id
                    ? 'bg-green-50'
                    : ''
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
                  class="rounded-full px-2.5 py-1 text-[11px] font-semibold"
                  :class="
                    selectedSchoolYearId === sy.school_year_id
                      ? 'bg-green-50 text-green-700'
                      : 'bg-gray-50 text-gray-500'
                  "
                >
                  {{
                    selectedSchoolYearId === sy.school_year_id
                      ? "Active"
                      : "Select"
                  }}
                </span>
              </button>

              <div
                v-if="activeYears.length === 0"
                class="px-4 py-6 text-center text-sm text-gray-400"
              >
                No school year found
              </div>
            </div>
          </div>
        </div>

        <!-- Profile -->
        <div
          class="flex items-center gap-2 cursor-pointer"
          @click.stop="toggleOpenProfile"
        >
          <div
            ref="profileIcon"
            class="w-9 h-9 rounded-xl border border-green-600 overflow-hidden"
          >
            <img
              src="../../../assets/img/users1.png"
              class="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Profile Dropdown -->
  <div
    v-if="isOpenProfile"
    ref="profileDropdown"
    class="absolute top-[84px] lg:top-[68px] right-2.5 lg:right-1 z-50"
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
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          },
        );
        this.user = res.data || {};
      } catch {
        this.$router.push("/");
      }
    },

    async fetchSchoolYears() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years",
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
        (a, b) => new Date(b.updated_at) - new Date(a.updated_at),
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
        (y) => y.school_year_id === this.selectedSchoolYearId,
      );

      if (!selectedSY) return;

      try {
        await axios.patch(
          process.env.VUE_APP_API_BASE_URL +
            `/school-year/update-timestamp/${selectedSY.school_year_id}`,
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
