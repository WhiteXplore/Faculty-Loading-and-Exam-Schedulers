<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">My Loading</h1>
    </div>

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
