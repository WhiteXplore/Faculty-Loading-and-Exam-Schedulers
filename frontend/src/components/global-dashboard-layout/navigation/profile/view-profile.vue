<template>
  <div v-if="currentUser" class="p-6 bg-[#F4F6F8] min-h-[70vh] rounded-t-xl">
    <div class="bg-white rounded-xl p-6 shadow-sm">
      <div class="space-y-3">
        <personalInformation :user="currentUser" @edit="openEditModal" />
      </div>
    </div>

    <!-- Edit Modal -->
    <addInstructor
      v-if="showEditModal"
      :isEdit="true"
      :userData="currentUser"
      @close="showEditModal = false"
      @updated="fetchRawUsers"
    />
  </div>

  <!-- Loading -->
  <div v-else class="flex justify-center items-center h-screen">
    <p class="text-gray-500">Loading profile...</p>
  </div>
</template>

<script>
import axios from "axios";
import addInstructor from "@/components/faculty/faculty-records/modals/add-users.vue";
import personalInformation from "./personal-information.vue";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "ProfileContentPage",
  components: {
    addInstructor,
    personalInformation,
  },
  data() {
    return {
      subId: null,
      showEditModal: false,
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

    async getSubId() {
      try {
        const response = await axios.get(process.env.VUE_APP_API_BASE_URL + "/auth/me", {
          withCredentials: true,
        });

        if (response.data?.sub) {
          this.subId = response.data.sub;
          await this.fetchRawUsers();
        } else {
          this.$router.push("/");
          location.reload();
        }
      } catch (error) {
        console.error("Failed to fetch logged user:", error);
        this.$router.push("/");
      }
    },

    openEditModal() {
      this.showEditModal = true;
    },
  },

  async mounted() {
    await this.getSubId();
  },
};
</script>
