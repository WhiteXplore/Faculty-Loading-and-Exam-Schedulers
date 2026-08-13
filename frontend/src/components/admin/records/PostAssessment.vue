<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Post-assessment</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tablePostAssessment />
    </div>
  </div>
</template>

<script>
import tablePostAssessment from "./tables/table-postassessment.vue";
export default {
  name: "PostAssessmentPage",
  components: {
    tablePostAssessment,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
