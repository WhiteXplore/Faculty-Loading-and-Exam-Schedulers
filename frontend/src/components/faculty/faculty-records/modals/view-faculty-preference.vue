<template>
  <div
    v-if="currentUser && currentUser.role !== 'Admin'"
    class="w-full lg:flex-1 bg-white rounded-2xl"
  >
    <!-- Header / Edit Button -->
    <div class="flex justify-end mb-2">
      <div
        @click="showExpertiseModal = true"
        class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
      >
        <div
          class="p-1 bg-defaultGreen bg-opacity-20 rounded-full flex items-center justify-center"
        >
          <icon name="edit" />
        </div>

        <span class="font-medium text-sm">Edit Expertise</span>
      </div>
    </div>

    <!-- Content -->
    <div class="h-auto overflow-auto space-y-8">
      <div
        v-for="sem in [1, 2, 3]"
        :key="sem"
        class="bg-white border border-gray-200 rounded-xl p-4"
      >
        <!-- Semester Header -->
        <h2 class="text-xl font-bold text-green-800 mb-4">
          {{ getSemesterName(sem) }}
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Expertise -->
          <div class="border rounded-xl p-4">
            <h3 class="text-lg font-semibold text-green-900 mb-3 border-b pb-2">
              Expertise
            </h3>

            <ul class="flex flex-col gap-4">
              <li
                v-for="(item, idx) in filteredExpertiseBySemester(sem)"
                :key="'exp-' + sem + '-' + idx"
                class="flex items-center gap-3 px-3 py-2"
              >
                <span
                  class="w-6 h-6 flex items-center justify-center rounded-full bg-green-600 text-white text-xs"
                >
                  ✓
                </span>

                <div class="flex flex-col">
                  <span class="font-semibold text-sm">
                    {{ item.course?.course_code || "N/A" }}
                  </span>
                  <span class="text-xs text-gray-600">
                    {{ item.course?.course_title || "No Description" }}
                  </span>
                </div>
              </li>
            </ul>

            <p
              v-if="filteredExpertiseBySemester(sem).length === 0"
              class="text-sm text-gray-400 italic text-center mt-3"
            >
              No expertise for this semester.
            </p>
          </div>

          <!-- Other Expertise -->
          <div class="border rounded-xl p-4">
            <h3 class="text-lg font-semibold text-blue-900 mb-3 border-b pb-2">
              Other Expertise
            </h3>

            <ul class="flex flex-col gap-4">
              <li
                v-for="(item, idx) in filteredOtherBySemester(sem)"
                :key="'oth-' + sem + '-' + idx"
                class="flex items-center gap-3 px-3 py-2"
              >
                <span
                  class="w-6 h-6 flex items-center justify-center rounded-full bg-blue-600 text-white text-xs"
                >
                  ✓
                </span>

                <div class="flex flex-col">
                  <span class="font-semibold text-sm">
                    {{ item.course?.course_code || "N/A" }}
                  </span>
                  <span class="text-xs text-gray-600">
                    {{ item.course?.course_title || "No Description" }}
                  </span>
                </div>
              </li>
            </ul>

            <p
              v-if="filteredOtherBySemester(sem).length === 0"
              class="text-sm text-gray-400 italic text-center mt-3"
            >
              No other expertise for this semester.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- MODAL (FIXED) -->
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
import EditExpertiseModal from "./add-expertise.vue"; // your modal (rename if needed)

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
        this.currentUser?.expertise?.filter((e) => e.course?.course_semester === sem) ||
        []
      );
    },

    filteredOtherBySemester(sem) {
      return (
        this.currentUser?.other_expertise?.filter(
          (e) => e.course?.course_semester === sem
        ) || []
      );
    },

    async getSubId() {
      try {
        const res = await axios.get(process.env.VUE_APP_API_BASE_URL + "/auth/me", {
          withCredentials: true,
        });

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
