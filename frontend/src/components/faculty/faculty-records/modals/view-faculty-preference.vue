<template>
  <div
    v-if="currentUser && currentUser.role !== 'Admin'"
    class="w-full lg:flex-1 rounded bg-gray-50"
  >
    <!-- Header -->
    <div
      class="mb-2 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
    >
      <div>
        <h1 class="mt-1 text-xl font-bold text-gray-900">
          My Teaching Preferences
        </h1>
        <p class="mt-1 text-xs text-gray-500">
          View and manage your assigned expertise by semester.
        </p>
      </div>

      <div @click="showExpertiseModal = true" class="btn-add">
        <div class="btn-add-icon">
          <icon name="edit" />
        </div>
        <span class="btn-add-text">Edit Expertise</span>
      </div>
    </div>

    <!-- Content -->
    <div class="space-y-4 h-[85vh] overflow-auto">
      <div
        v-for="sem in [1, 2, 3]"
        :key="sem"
        class="relative overflow-hidden rounded-xl border border-gray-100 bg-white p-5 shadow-sm"
      >
        <!-- Semester Header -->
        <div class="relative mb-5 flex items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <div
              class="flex h-12 w-12 items-center justify-center rounded-2xl bg-defaultGreen text-white shadow-lg shadow-green-100"
            >
              <icon name="book-open" />
            </div>

            <div>
              <h2 class="text-lg font-bold text-gray-900">
                {{ getSemesterName(sem) }}
              </h2>
              <p class="text-xs text-gray-400">
                {{ getTotalBySemester(sem) }} total course preferences
              </p>
            </div>
          </div>

          <span
            class="rounded-full bg-green-50 px-3 py-1 text-[11px] font-semibold text-defaultGreen"
          >
            Active
          </span>
        </div>

        <!-- Cards -->
        <div class="relative grid grid-cols-1 gap-4 xl:grid-cols-3">
          <!-- Primary Expertise -->
          <div class="expertise-card">
            <div class="expertise-card-header">
              <div>
                <h3 class="expertise-title text-green-800">Expertise</h3>
                <p class="expertise-subtitle">
                  Courses you are strongly qualified to handle
                </p>
              </div>

              <span class="count-pill bg-green-50 text-green-700">
                {{ filteredExpertiseBySemester(sem).length }}
              </span>
            </div>

            <div class="mt-4 space-y-3">
              <div
                v-for="(item, idx) in filteredExpertiseBySemester(sem)"
                :key="'exp-' + sem + '-' + idx"
                class="course-item hover:border-green-200 hover:bg-green-50/40"
              >
                <div class="course-check bg-green-600">✓</div>

                <div class="min-w-0 flex-1">
                  <div class="flex items-center gap-2">
                    <h4 class="truncate text-sm font-bold text-gray-900">
                      {{ item.course?.course_code || "N/A" }}
                    </h4>
                    <span
                      class="rounded-full bg-green-100 px-2 py-0.5 text-[10px] font-semibold text-green-700"
                    >
                      Primary
                    </span>
                  </div>

                  <p class="mt-1 line-clamp-2 text-xs text-gray-500">
                    {{ item.course?.course_title || "No Description" }}
                  </p>
                </div>
              </div>

              <div
                v-if="filteredExpertiseBySemester(sem).length === 0"
                class="empty-state"
              >
                <div class="empty-icon bg-green-50 text-green-700">
                  <icon name="exclamationmark" />
                </div>
                <p>No expertise for this semester.</p>
              </div>
            </div>
          </div>

          <!-- Other Expertise -->
          <div class="expertise-card">
            <div class="expertise-card-header">
              <div>
                <h3 class="expertise-title text-blue-800">Other Expertise</h3>
                <p class="expertise-subtitle">
                  Secondary courses you can also handle
                </p>
              </div>

              <span class="count-pill bg-blue-50 text-blue-700">
                {{ filteredOtherBySemester(sem).length }}
              </span>
            </div>

            <div class="mt-4 space-y-3">
              <div
                v-for="(item, idx) in filteredOtherBySemester(sem)"
                :key="'oth-' + sem + '-' + idx"
                class="course-item hover:border-blue-200 hover:bg-blue-50/40"
              >
                <div class="course-check bg-blue-600">✓</div>

                <div class="min-w-0 flex-1">
                  <div class="flex items-center gap-2">
                    <h4 class="truncate text-sm font-bold text-gray-900">
                      {{ item.course?.course_code || "N/A" }}
                    </h4>
                    <span
                      class="rounded-full bg-blue-100 px-2 py-0.5 text-[10px] font-semibold text-blue-700"
                    >
                      Other
                    </span>
                  </div>

                  <p class="mt-1 line-clamp-2 text-xs text-gray-500">
                    {{ item.course?.course_title || "No Description" }}
                  </p>
                </div>
              </div>

              <div
                v-if="filteredOtherBySemester(sem).length === 0"
                class="empty-state"
              >
                <div class="empty-icon bg-blue-50 text-blue-700">
                  <icon name="exclamationmark" />
                </div>
                <p>No other expertise for this semester.</p>
              </div>
            </div>
          </div>

          <!-- Cross Assign Expertise -->
          <div class="expertise-card">
            <div class="expertise-card-header">
              <div>
                <h3 class="expertise-title text-amber-800">
                  Cross Assign Expertise
                </h3>
                <p class="expertise-subtitle">
                  Courses assigned across programs or institutes
                </p>
              </div>

              <span class="count-pill bg-amber-50 text-amber-700">
                {{ filteredCrossBySemester(sem).length }}
              </span>
            </div>

            <div class="mt-4 space-y-3">
              <div
                v-for="(item, idx) in filteredCrossBySemester(sem)"
                :key="'cross-' + sem + '-' + idx"
                class="course-item hover:border-amber-200 hover:bg-amber-50/40"
              >
                <div class="course-check bg-amber-500">✓</div>

                <div class="min-w-0 flex-1">
                  <div class="flex items-center gap-2">
                    <h4 class="truncate text-sm font-bold text-gray-900">
                      {{ item.course?.course_code || "N/A" }}
                    </h4>
                    <span
                      class="rounded-full bg-amber-100 px-2 py-0.5 text-[10px] font-semibold text-amber-700"
                    >
                      Cross
                    </span>
                  </div>

                  <p class="mt-1 line-clamp-2 text-xs text-gray-500">
                    {{ item.course?.course_title || "No Description" }}
                  </p>
                </div>
              </div>

              <div
                v-if="filteredCrossBySemester(sem).length === 0"
                class="empty-state"
              >
                <div class="empty-icon bg-amber-50 text-amber-700">
                  <icon name="exclamationmark" />
                </div>
                <p>No cross assign expertise for this semester.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <EditExpertiseModal
      v-if="showExpertiseModal && currentUser"
      :userData="currentUser"
      @close="showExpertiseModal = false"
      @updated="handleUpdated"
    />
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { mapState, mapActions } from "pinia";
import { useFetchDataStore } from "@/store/fetch-data-store";
import axios from "axios";
import EditExpertiseModal from "./add-expertise.vue";

export default {
  name: "PreferenceSection",
  components: { icon, EditExpertiseModal },

  data() {
    return {
      subId: null,
      showExpertiseModal: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["rawusers"]),

    currentUser() {
      if (!this.subId || !this.rawusers) return null;
      return this.rawusers.find((u) => u.id === this.subId) || null;
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchRawUsers"]),

    handleUpdated() {
      this.showExpertiseModal = false;
      this.fetchRawUsers();
    },

    getSemesterName(sem) {
      if (sem === 1) return "1st Semester";
      if (sem === 2) return "2nd Semester";
      if (sem === 3) return "Summer";
      return "N/A";
    },

    filteredExpertiseBySemester(sem) {
      return (
        this.currentUser?.expertise?.filter(
          (e) =>
            e.status === "PRIMARY" &&
            Number(e.course?.course_semester) === Number(sem),
        ) || []
      );
    },

    filteredOtherBySemester(sem) {
      return (
        this.currentUser?.expertise?.filter(
          (e) =>
            e.status === "OTHER" &&
            Number(e.course?.course_semester) === Number(sem),
        ) || []
      );
    },

    filteredCrossBySemester(sem) {
      return (
        this.currentUser?.expertise?.filter(
          (e) =>
            e.status === "CROSS" &&
            Number(e.course?.course_semester) === Number(sem),
        ) || []
      );
    },

    getTotalBySemester(sem) {
      return (
        this.filteredExpertiseBySemester(sem).length +
        this.filteredOtherBySemester(sem).length +
        this.filteredCrossBySemester(sem).length
      );
    },

    async getSubId() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          },
        );

        if (res.data?.sub) {
          this.subId = res.data.sub;
          await this.fetchRawUsers();
        } else {
          this.$router.push("/");
        }
      } catch (err) {
        console.error(err);
        this.$router.push("/");
      }
    },
  },

  async mounted() {
    await this.getSubId();
  },
};
</script>

<style scoped>
.expertise-card {
  @apply rounded-2xl border border-gray-100 bg-white p-4 shadow-sm;
}

.expertise-card-header {
  @apply flex items-start justify-between gap-3 border-b border-gray-100 pb-3;
}

.expertise-title {
  @apply text-sm font-bold;
}

.expertise-subtitle {
  @apply mt-1 text-xs text-gray-400;
}

.count-pill {
  @apply rounded-full px-3 py-1 text-xs font-bold;
}

.course-item {
  @apply flex items-start gap-3 rounded-2xl border border-gray-100 bg-gray-50/70 p-3 transition-all duration-200;
}

.course-check {
  @apply flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-xs font-bold text-white shadow-sm;
}

.empty-state {
  @apply flex min-h-[120px] flex-col items-center justify-center rounded-2xl border border-dashed border-gray-200 bg-gray-50 text-center text-sm text-gray-400;
}

.empty-icon {
  @apply mb-2 flex h-10 w-10 items-center justify-center rounded-2xl;
}
</style>
