<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-black/40 flex justify-center items-center z-[5000]"
  >
    <div
      class="rounded-2xl shadow-lg w-[18%] bg-white py-6 px-5 flex flex-col items-center animate-slideUp"
    >
      <!-- Icon -->
      <div
        class="rounded-full w-16 h-16 flex justify-center items-center bg-red-400 animate-pulse"
      >
        <icon name="question" class="w-10 h-10 text-white" />
      </div>

      <!-- Title -->
      <h1 class="text-[15px] md:text-[17px] font-semibold mt-4 text-center">
        Log out Confirmation
      </h1>

      <p class="mt-2 text-[12px] md:text-[13px] text-gray-600 text-center">
        Are you sure you want to log out?
      </p>

      <!-- Divider -->
      <div class="w-full h-[1px] bg-gray-200 my-4"></div>

      <!-- Buttons -->
      <div class="w-full flex justify-center gap-2">
        <button
          class="bg-gray-100 py-2 px-4 text-[12px] md:text-[13px] rounded-md text-gray-600 hover:bg-white border hover:border-red-500 hover:text-red-500 hover:shadow-md transition"
          @click="closeModal"
        >
          No, Cancel
        </button>

        <button
          class="bg-defaultGreen py-2 px-4 text-[12px] md:text-[13px] rounded-md text-white hover:bg-white border hover:border-defaultGreen hover:text-defaultGreen hover:shadow-md transition"
          @click="toggleLogout"
        >
          Yes, Sign out
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import axios from "axios";

export default {
  name: "LogoutModal",
  components: {
    icon,
  },
  props: {
    isOpen: Boolean,
  },
  methods: {
    async toggleLogout() {
      try {
        await axios.post(process.env.VUE_APP_API_BASE_URL + "/auth/logout");
        this.$emit("close"); // Inform parent to close the modal
        localStorage.removeItem("role");
        localStorage.removeItem("studentData");
        localStorage.removeItem("transactionData");
        localStorage.removeItem("lastStudentId");
        this.$router.push("/");
      } catch (error) {
        console.error("Logout failed:", error);
      }
    },
    closeModal() {
      this.$emit("close");
    },
  },
};
</script>
