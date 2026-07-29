<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <div class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg">
        <!-- Header -->

        <div class="modal-header">
          <div class="flex items-center gap-3">
            <!-- Icon -->
            <div class="glass-container">
              <icon name="users" class="text-white" />
            </div>

            <!-- Title -->
            <div>
              <h2 class="text-lg font-semibold text-white">
                Account Information
              </h2>

              <p class="text-xs text-green-100">
                Account details and personal information overview
              </p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <!-- Content -->
        <div class="p-6 w-[500px]">
          <!-- Account Profile -->
          <div class="grid grid-cols-1 gap-4 text-sm">
            <div class="space-y-1">
              <p class="input-label">Faculty Name</p>
              <p class="font-medium text-gray-900">
                {{ userData.first_name }}
                {{ userData.last_name }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="input-label">Institute</p>
              <p class="font-medium text-gray-900">
                {{ userData.institute?.institute_name || "N/A" }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="input-label">Program</p>
              <p class="font-medium text-gray-900">
                {{ userData.program?.program_name || "N/A" }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="input-label">Designation</p>
              <p class="font-medium text-gray-900">
                {{ userData.designation || "N/A" }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="input-label">Employment Type</p>
              <p class="font-medium text-gray-900">
                {{ userData.employment_type || "N/A" }}
              </p>
            </div>

            <div class="space-y-1">
              <p class="input-label">Unit Load</p>
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
