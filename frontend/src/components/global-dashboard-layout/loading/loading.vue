<template>
  <transition name="loader-fade" appear>
    <div class="relative z-50" role="dialog" aria-modal="true">
      <div
        class="fixed inset-0 flex items-center justify-center bg-[#063f2f]/90 backdrop-blur-md"
      >
        <div class="flex flex-col items-center justify-center animate-loaderUp">
          <!-- Loader Container -->
          <div class="relative flex h-36 w-36 items-center justify-center">
            <!-- Outer Ring -->
            <div
              class="absolute h-36 w-36 rounded-full border-4 border-white/10 border-t-green-300 animate-spin"
            ></div>

            <!-- Pulse Ring -->
            <div
              class="absolute h-32 w-32 rounded-full border border-green-300/40 animate-ping"
            ></div>

            <!-- Middle Glow -->
            <div
              class="absolute h-28 w-28 rounded-full bg-white/10 blur-xl animate-pulse"
            ></div>

            <!-- Logo Card -->
            <div
              class="relative flex h-24 w-24 items-center justify-center rounded-3xl bg-white shadow-2xl ring-1 ring-white/40 animate-float"
            >
              <!-- <img
                src="../assets/rms_logo.png"
                alt="RMS Logo"
                class="h-16 w-16 object-contain"
              /> -->
            </div>
          </div>

          <!-- Text -->
          <div class="mt-8 text-center animate-fadeDelay">
            <h2 class="text-lg font-bold tracking-wide text-white">Loading...</h2>

            <p class="mt-2 text-sm text-white/70">
              {{ loadingMessage }}
            </p>
          </div>

          <!-- Progress Dots -->
          <div class="mt-5 flex gap-2">
            <span class="h-2 w-2 animate-bounce rounded-full bg-white/80"></span>
            <span
              class="h-2 w-2 animate-bounce rounded-full bg-white/80"
              style="animation-delay: 0.15s"
            ></span>
            <span
              class="h-2 w-2 animate-bounce rounded-full bg-white/80"
              style="animation-delay: 0.3s"
            ></span>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "LoadingPage",
  computed: {
    loadingMessage() {
      return this.$route.path === "/login"
        ? "Please wait while we prepare your workspace"
        : "Please wait for a while";
    },
  },
};
</script>

<style scoped>
/* Fade whole loader */
.loader-fade-enter-active,
.loader-fade-leave-active {
  transition: all 0.35s ease;
}

.loader-fade-enter-from,
.loader-fade-leave-to {
  opacity: 0;
}

/* Pop upward */
@keyframes loaderUp {
  from {
    opacity: 0;
    transform: translateY(25px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.animate-loaderUp {
  animation: loaderUp 0.55s ease-out;
}

/* Floating logo */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }

  50% {
    transform: translateY(-6px);
  }
}

.animate-float {
  animation: float 2.2s ease-in-out infinite;
}

/* Delayed text */
@keyframes fadeDelay {
  from {
    opacity: 0;
    transform: translateY(8px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeDelay {
  animation: fadeDelay 0.7s ease-out 0.2s both;
}
</style>
