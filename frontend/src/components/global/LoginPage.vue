<template>
  <div class="relative w-full min-h-screen flex flex-col">
    <!-- Background Image -->
    <img
      src="@/assets/img/landing-layer-1.png"
      alt="Background"
      class="absolute inset-0 object-cover w-full h-full z-0 opacity-95"
    />
    <div class="bg-gray-900 opacity-25 w-full min-h-screen z-10 absolute inset-0"></div>

    <!-- Form Container -->
    <div class="flex items-center justify-center min-h-screen relative z-20">
      <div
        class="w-auto h-auto rounded-xl shadow-lg flex overflow-hidden relative p-3 bg-opacity-90 backdrop-blur-2xl animate-slideUp"
      >
        <div class="flex justify-between gap-2 h-[45vh]">
          <div class="z-10 w-[20vw] flex justify-center items-start text-white p-3">
            <div class="flex flex-col justify-center items-center text-center">
              <img src="@/assets/img/dnsc_logo.png" alt="" class="w-20" />
              <h1 class="font-bold text-2xl mt-2">Davao del Norte State College</h1>
              <p class="text-sm text-justify mt-5">
                Davao del Norte State College is a distinguished public institution of
                higher learning located in New Visayas, Panabo City, Philippines. It
                offers diverse academic programs in Information Technology, Agriculture,
                Education, Tourism, and many more. The college is committed to academic
                excellence, research, and community service through a dynamic curriculum
                and dedicated faculty. By empowering students with knowledge, skills, and
                values, it helps shape innovative leaders who contribute to national
                development and global progres
                <a href="https://dnsc.edu.ph/" class="text-left flex mt-5 font-bold"
                  >Click here for more information!</a
                >
              </p>
            </div>
          </div>
          <div
            class="z-10 w-[20vw] flex flex-col justify-start items-center bg-white rounded-xl p-4 space-y-6 text-left text-[14px] animate-scaleUp"
          >
            <!-- Title -->
            <div class="w-full space-y-1 mt-3">
              <h2 class="text-xl font-semibold text-gray-800">Sign in to Your Account</h2>
              <p class="text-[13px] text-gray-600 tracking-wider">
                Welcome back! Please enter your details
              </p>
            </div>

            <!-- Login Form -->
            <form @submit.prevent="login" class="w-full space-y-4">
              <!-- Email Input -->
              <div>
                <label class="block text-sm font-medium text-gray-700">Email</label>
                <input
                  v-model="email"
                  type="email"
                  placeholder="Enter your email"
                  class="mt-1 w-full px-3 py-3 border rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500"
                />
              </div>

              <!-- Password Input -->
              <div>
                <label class="block text-sm font-medium text-gray-700">Password</label>
                <div class="relative">
                  <input
                    v-model="password"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Enter your password"
                    class="mt-1 w-full px-3 py-3 border rounded-md shadow-sm focus:outline-none focus:ring-green-500 focus:border-green-500"
                  />
                  <button
                    type="button"
                    @click="togglePassword"
                    class="absolute inset-y-0 right-3 flex items-center text-gray-500"
                  >
                    <icon :name="showPassword ? 'eye-close' : 'eye-open'" />
                  </button>
                </div>
              </div>

              <!-- Submit Button -->
              <button
                type="submit"
                class="w-full text-[16px] bg-defaultGreen text-white py-3 rounded-md hover:bg-defaultGreen transition"
              >
                Sign in
              </button>

              <!-- Logos -->
              <div
                class="flex justify-center items-center gap-2 pt-2 text-[12px] text-gray-600"
              >
                <img
                  src="@/assets/img/bagong-pilipinas.png"
                  alt="Bagong Pilipinas"
                  class="w-[55px] h-auto"
                />
                <a href="https://dnsc.edu.ph/">
                  <img
                    src="@/assets/img/dnsc_logo.png"
                    alt="DNSC Logo"
                    class="w-[51px] h-auto"
                /></a>
                <img
                  src="@/assets/img/corseal.png"
                  alt="DNSC Logo"
                  class="w-[30px] h-auto cursor-pointer"
                  @click="showRegistration = true"
                />
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Outside   -->
    <div
      v-if="showRegistration"
      class="fixed inset-0 z-[9999] flex items-center justify-center px-4"
    >
      <!-- BACKDROP -->
      <div
        class="absolute inset-0 bg-black/50 backdrop-blur-sm"
        @click="showRegistration = false"
      ></div>

      <!-- MODAL -->
      <div
        class="relative z-10 w-full max-w-5xl max-h-[90vh] overflow-y-auto p-4 sm:p-6 rounded-2xl bg-white/20 backdrop-blur-xl border border-white/30 shadow-2xl"
      >
        <!-- HEADER -->
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-white text-lg sm:text-xl md:text-2xl font-semibold">
            Certificate of Registration 2026
          </h2>

          <button
            @click="showRegistration = false"
            class="text-white text-lg p-2 hover:bg-white/20 rounded-full"
          >
            <icon name="close" />
          </button>
        </div>

        <!-- CONTENT -->
        <div class="flex flex-col lg:flex-row gap-6 items-center justify-center">
          <!-- CERTIFICATE -->
          <div class="w-full flex justify-center">
            <img
              src="@/assets/img/registration.jpg"
              class="w-full max-w-[500px] md:max-w-[600px] lg:max-w-[730px] object-contain rounded-lg"
            />
          </div>

          <!-- CORSEAL -->
          <div class="flex justify-center">
            <img
              src="@/assets/img/corseal.png"
              class="w-[230px] sm:w-[230px] md:w-[230px] lg:w-[300px] object-contain"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import authMixin from "../../mixin/authMixin";
export default {
  name: "LoginRegisterPage",
  mixins: [authMixin],
  components: {
    icon,
  },
  data() {
    return {
      showLogin: true,
      registrationStep: 1,
      showRegistration: false,
    };
  },
  methods: {
    toggleForm() {
      this.showLogin = !this.showLogin;
      this.registrationStep = 1;
      this.errorMessage = "";
    },
  },
};
</script>

<style scoped></style>
