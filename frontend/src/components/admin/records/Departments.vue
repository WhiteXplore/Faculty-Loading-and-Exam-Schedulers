<template>
  <div class="px-2 mt-2">
    <!-- Headers -->
    <div class="flex justify-between items-start">
      <h1 class="font-semibold tracking-wide text-sm px-1">Departments</h1>
    </div>

    <!-- Main Content  -->
    <div class="mt-3">
      <!-- Table -->
      <tableDepartments />
    </div>
  </div>
</template>

<script>
import tableDepartments from "./tables/table-departments.vue";
export default {
  name: "DepartmentsPage",
  components: {
    tableDepartments,
  },
};
</script>

<style scoped>
/* Add any required styles here */
</style>
