<template>
  <div class="px-2 mt-2">
    <!-- Headers -->

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <personalInformation />
    </div>
  </div>
</template>

<script>
import personalInformation from "./personal-information.vue";
export default {
  name: "AccuntSetting Page",
  components: {
    personalInformation,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
