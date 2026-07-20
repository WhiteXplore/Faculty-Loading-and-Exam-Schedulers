<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Pre-assessment</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tablePreAssessment />
    </div>
  </div>
</template>

<script>
import tablePreAssessment from "./tables/table-preassessment.vue";
export default {
  name: "PreAssessmentPage",
  components: {
    tablePreAssessment,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
