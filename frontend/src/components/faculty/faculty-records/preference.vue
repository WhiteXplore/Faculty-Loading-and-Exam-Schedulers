<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">My Preference</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <viewFacultyPreference />
    </div>
  </div>
</template>

<script>
import viewFacultyPreference from "./modals/view-faculty-preference.vue";
export default {
  name: "LoadingPage",
  components: {
    viewFacultyPreference,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
