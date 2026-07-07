<template>
  <div class="modal-overlay">
    <div
      class="rounded-[16px] shadow-lg justify-center animate-slideUp max-h-[90vh] overflow-y-auto"
    >
      <div class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5">
        <!-- Header -->
        <div class="flex items-center justify-between px-6 py-4 border-b">
          <div class="flex items-center gap-2">
            <div
              class="w-10 h-10 rounded-xl bg-green-600 flex items-center justify-center shadow-sm"
            >
              <icon name="users" class="text-white" />
            </div>
            <div>
              <h2 class="text-lg font-semibold text-gray-900">Account Information</h2>
              <p class="text-xs text-gray-500">
                Account details and personal information overview
              </p>
            </div>
          </div>
          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 transition"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <!-- Content -->
        <div class="p-6 w-[500px]">
          <!-- Account Profile -->
          <div class="grid grid-cols-1 gap-4 text-sm">
            <div class="space-y-1">
              <p class="text-gray-500">Faculty Name</p>
              <p class="font-medium text-gray-900">
                {{ userData.first_name }}
                {{ userData.last_name }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="text-gray-500">Institute</p>
              <p class="font-medium text-gray-900">
                {{ userData.institute?.institute_name || "N/A" }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="text-gray-500">Program</p>
              <p class="font-medium text-gray-900">
                {{ userData.program?.program_name || "N/A" }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="text-gray-500">Designation</p>
              <p class="font-medium text-gray-900">
                {{ userData.designation || "N/A" }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="text-gray-500">Employment Type</p>
              <p class="font-medium text-gray-900">
                {{ userData.employment_type || "N/A" }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="text-gray-500">Unit Load</p>
              <p class="font-medium text-gray-900">
                {{ userData.unit_load ?? "N/A" }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
export default {
  name: "ViewUserExpertise",
  components: {
    icon,
  },
  props: {
    userData: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb {
  background: #9333ea;
  border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
  background: #7e22ce;
}
</style>
