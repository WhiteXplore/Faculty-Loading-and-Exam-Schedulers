<template>
  <div class="px-2 mt-2">
    <!-- Headers -->

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableLoading />
    </div>
  </div>
</template>

<script>
import tableLoading from "./tables/table-loading.vue";
export default {
  name: "LoadingPage",
  components: {
    tableLoading,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
