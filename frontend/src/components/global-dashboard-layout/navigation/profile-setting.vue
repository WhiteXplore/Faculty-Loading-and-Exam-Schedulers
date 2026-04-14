<template>
  <!-- Profile Menu -->
  <div
    v-if="isProfileMenuOpen"
    @mouseenter="isProfileMenuOpen = true"
    @mouseleave="isProfileMenuOpen = false"
    @click.stop
  >
    <div
      class="bg-white rounded-xl shadow-lg w-[280px] max-h-[27.5vh] p-2 flex flex-col gap-2 overflow-y-auto border text-gray-700"
    >
      <!-- User Info -->
      <div class="flex items-center gap-3">
        <div
          ref="profileIcon"
          class="w-10 h-10 rounded-xl border border-green-600 cursor-pointer transition"
        >
          <img
            src="../../../assets/img/users1.png"
            class="w-full h-full rounded-full object-cover"
          />
        </div>
        <div class="flex flex-col text-left text-gray-600">
          <div class="uppercase text-sm font-semibold">
            {{ user.last_name }}, {{ user.first_name }}
          </div>
          <div class="text-xs">{{ user.email }}</div>
        </div>
      </div>

      <div class="w-full h-[1px] bg-gray-200"></div>

      <router-link to="/profile-view" @click="toggleCloseProfile">
        <div
          class="py-3 px-4 flex items-center gap-4 hover:bg-gray-100 rounded-lg cursor-pointer"
        >
          <icon name="users" />
          <div class="text-sm">Profile</div>
        </div>
      </router-link>
      <router-link to="/setting" @click="toggleCloseSetting">
        <div
          class="py-3 px-4 flex items-center gap-4 hover:bg-gray-100 rounded-lg cursor-pointer"
        >
          <icon name="cog" class="w-5 h-5" />
          <div class="text-sm">Security</div>
        </div>
      </router-link>

      <div class="w-full h-[1px] bg-gray-200"></div>
      <!-- Logout -->
      <div
        @click="toggleOpenLogout"
        class="py-2 px-4 text-center border hover:bg-defaultGreen hover:text-white rounded-lg cursor-pointer"
      >
        <div class="text-sm">Logout</div>
      </div>
    </div>
  </div>

  <!-- Logout Modal -->
  <Logout :isOpen="isOpenLogout" @close="isOpenLogout = false" />
</template>

<script>
import Logout from "./alert/logout.vue";
import icon from "@/assets/icon.vue";
import axios from "axios";
export default {
  name: "ProfilePage",
  components: {
    Logout,
    icon,
  },
  data() {
    return {
      isOpenLogout: false,
      isProfileMenuOpen: true,
      user: {},
    };
  },
  methods: {
    toggleCloseProfile() {
      this.isProfileMenuOpen = false;
    },
    toggleOpenLogout() {
      this.isOpenLogout = true; // Show the logout modal
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
  },
  watch: {
    $route(to) {
      if (to.path === "/profile-view") {
        this.isProfileMenuOpen = false;
      }
    },
  },
  mounted() {
    this.fetchUser();
    if (this.$route.path === "/profile-view") {
      this.isProfileMenuOpen = false;
    }
  },
};
</script>
