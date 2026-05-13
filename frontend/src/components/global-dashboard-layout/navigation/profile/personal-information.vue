<template>
  <div class="max-h-full overflow-auto bg-[#F5F7FA] p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-semibold text-gray-800">Account Settings</h1>
      <p class="text-sm text-gray-500 mt-1">Current signed-in user information.</p>
    </div>

    <div
      v-if="loading"
      class="bg-white border border-gray-100 rounded-xl p-10 text-center shadow-sm"
    >
      <p class="text-sm text-gray-500">Loading profile...</p>
    </div>

    <div
      v-else-if="currentUser"
      class="bg-white border border-gray-100 rounded-xl shadow-sm overflow-hidden"
    >
      <div class="h-[12vh] bg-gradient-to-r from-green-900 to-green-700"></div>

      <div class="px-8 pb-8">
        <div
          class="relative -mt-12 flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6"
        >
          <!-- Left -->
          <div class="flex items-center gap-5 min-w-0">
            <!-- Avatar -->
            <div
              class="w-28 h-28 min-w-[112px] bg-white border-[5px] border-white rounded-2xl shadow-lg overflow-hidden"
            >
              <img
                src="@/assets/img/employee_picture.png"
                alt="Profile"
                class="w-full h-full object-cover"
              />
            </div>

            <!-- User Info -->
            <div class="min-w-0 pb-2">
              <!-- Name -->
              <h2
                class="text-[30px] leading-tight font-bold text-white tracking-[-0.02em] break-words pb-2"
              >
                {{ fullName }}
              </h2>

              <!-- Badges -->
              <div class="flex flex-wrap items-center gap-2 mt-2">
                <span
                  class="px-4 py-1.5 rounded-full text-xs font-semibold shadow-sm border"
                  :class="roleBadge(currentUser.role)"
                >
                  {{ currentUser.role || "No Role" }}
                </span>

                <span
                  class="px-4 py-1.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200 shadow-sm"
                >
                  {{ currentUser.employment_type || "No Employment Type" }}
                </span>
              </div>
            </div>
          </div>

          <!-- Right Side -->
          <div class="flex items-center gap-3">
            <button
              type="button"
              @click="openEditModal"
              class="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white text-sm font-medium rounded-xl transition-all duration-200 shadow-md hover:shadow-lg"
            >
              Edit Profile
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5 mt-8">
          <div class="info-card">
            <p class="info-label">User ID</p>
            <p class="info-value">{{ currentUser.id || signedUserId || "-" }}</p>
          </div>

          <div class="info-card">
            <p class="info-label">Email Address</p>
            <p class="info-value">{{ currentUser.email || "-" }}</p>
          </div>

          <div class="info-card">
            <p class="info-label">Designation</p>
            <p class="info-value">{{ currentUser.designation || "-" }}</p>
          </div>

          <div class="info-card">
            <p class="info-label">Unit Load</p>
            <p class="info-value">{{ currentUser.unit_load ?? 0 }}</p>
          </div>

          <div class="info-card">
            <p class="info-label">Preferred Time</p>
            <p class="info-value">{{ currentUser.preffered_time || "-" }}</p>
          </div>

          <div class="info-card">
            <p class="info-label">Program</p>
            <p class="info-value">
              {{ currentUser.program?.program_name || "Not Assigned" }}
            </p>
          </div>

          <div class="info-card">
            <p class="info-label">Program Code</p>
            <p class="info-value">
              {{ currentUser.program?.program_code || "Not Assigned" }}
            </p>
          </div>

          <div class="info-card">
            <p class="info-label">Institute</p>
            <p class="info-value">
              {{ currentUser.institute?.institute_name || "Not Assigned" }}
            </p>
          </div>

          <div class="info-card">
            <p class="info-label">Institute Code</p>
            <p class="info-value">
              {{ currentUser.institute?.institute_code || "Not Assigned" }}
            </p>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5 mt-8">
          <div class="section-card">
            <div class="flex items-center justify-between mb-4">
              <h3 class="section-title">Expertise</h3>
              <span class="count-badge">
                {{ currentUser.expertise?.length || 0 }}
              </span>
            </div>

            <div v-if="currentUser.expertise?.length" class="flex flex-wrap gap-2">
              <span
                v-for="item in currentUser.expertise"
                :key="item.id"
                class="subject-chip"
              >
                {{ item.course?.course_code || item.course?.course_title || "Course" }}
              </span>
            </div>

            <p v-else class="empty-text">No expertise assigned.</p>
          </div>

          <div class="section-card">
            <div class="flex items-center justify-between mb-4">
              <h3 class="section-title">Other Expertise</h3>
              <span class="count-badge">
                {{ currentUser.other_expertise?.length || 0 }}
              </span>
            </div>

            <div v-if="currentUser.other_expertise?.length" class="flex flex-wrap gap-2">
              <span
                v-for="item in currentUser.other_expertise"
                :key="item.id"
                class="subject-chip"
              >
                {{ item.course?.course_code || item.course?.course_title || "Course" }}
              </span>
            </div>

            <p v-else class="empty-text">No other expertise assigned.</p>
          </div>
        </div>
      </div>
    </div>

    <div
      v-else
      class="bg-white border border-gray-100 rounded-xl p-10 text-center shadow-sm"
    >
      <p class="text-sm text-gray-500">No matching signed-in user found.</p>
    </div>
  </div>
  <UsersModal
    v-if="showEditModal"
    :userData="currentUser"
    @close="showEditModal = false"
    @refresh="handleProfileUpdated"
  />
</template>

<script>
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";
import axios from "axios";
import UsersModal from "@/components/faculty/faculty-records/modals/add-users.vue";

export default {
  name: "AccountSettingsPage",

  components: {
    UsersModal,
  },

  data() {
    return {
      authUser: null,
      pageLoading: false,
      showEditModal: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["rawusers", "loading"]),

    signedUserId() {
      return this.authUser?.sub || this.authUser?.id || null;
    },

    currentUser() {
      if (!this.signedUserId) return null;

      return (
        this.rawusers?.find((user) => Number(user.id) === Number(this.signedUserId)) ||
        this.authUser
      );
    },

    fullName() {
      return `${this.currentUser?.first_name || ""} ${
        this.currentUser?.last_name || ""
      }`.trim();
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchRawUsers"]),

    openEditModal() {
      this.showEditModal = true;
    },

    async handleProfileUpdated() {
      await this.fetchRawUsers();
      await this.fetchUser();
      this.showEditModal = false;
    },

    async fetchUser() {
      try {
        const response = await axios.get(process.env.VUE_APP_API_BASE_URL + "/auth/me", {
          withCredentials: true,
        });

        if (response.data) {
          this.authUser = response.data;
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },

    roleBadge(role) {
      switch (role) {
        case "Admin":
          return "bg-red-100 text-red-700 border-red-200";
        case "Program Chair":
        case "Program Chairperson":
          return "bg-blue-100 text-blue-700 border-blue-200";
        case "Faculty":
          return "bg-green-100 text-green-700 border-green-200";
        default:
          return "bg-gray-100 text-gray-700 border-gray-200";
      }
    },
  },

  async mounted() {
    this.pageLoading = true;
    await this.fetchUser();
    await this.fetchRawUsers();
    this.pageLoading = false;
  },
};
</script>

<style scoped>
.info-card {
  @apply bg-white border border-gray-100 rounded-xl p-5 transition-all duration-200 hover:shadow-md;
}

.info-label {
  @apply text-xs font-medium uppercase tracking-wide text-gray-400 mb-2;
}

.info-value {
  @apply text-sm font-medium text-gray-800 break-words;
}

.section-card {
  @apply border border-gray-100 rounded-xl p-5 bg-[#FAFBFC];
}

.section-title {
  @apply text-base font-semibold text-gray-800;
}

.count-badge {
  @apply text-xs px-3 py-1 rounded-full bg-gray-200 text-gray-700;
}

.subject-chip {
  @apply px-4 py-2 bg-white border border-gray-200 rounded-lg text-sm text-gray-700 shadow-sm;
}

.empty-text {
  @apply text-sm text-gray-400 italic;
}
</style>
