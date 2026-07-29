<template>
  <div class="p-2">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="font-semibold tracking-wide text-sm px-1">Room Utilities</h1>
    </div>

    <!-- Tabs -->
    <div class="mt-2 justify-between flex items-center">
      <div class="flex gap-1">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="activeTab = tab.value"
          :class="[
            'px-4 py-2 rounded-t-lg  text-sm',
            activeTab === tab.value
              ? 'bg-defaultGreen text-white border border-gray-300 border-b-white shadow-sm'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200',
          ]"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- Content Card -->
    <div class="bg-white border-t-0 mt-2">
      <tableRooms v-if="activeTab === 'room'" />
      <tableBuildings v-if="activeTab === 'building'" />
      <tableBuildingAreas v-if="activeTab === 'setup'" />
      <tableCollegeBranch v-if="activeTab === 'branch'" />
    </div>
  </div>
</template>

<script>
import tableRooms from "./tables/table-rooms.vue";
import tableBuildings from "./tables/table-building.vue";
import tableCollegeBranch from "./tables/table-college_branch.vue";
import tableBuildingAreas from "./tables/table-building-areas.vue";

export default {
  name: "UtilitiesPage",

  components: {
    tableRooms,
    tableBuildings,
    tableCollegeBranch,
    tableBuildingAreas,
  },

  data() {
    return {
      activeTab: "room",
      tabs: [
        { label: "Room", value: "room" },
        { label: "Building", value: "building" },
        { label: "Setup Time", value: "setup" },
        { label: "College Branch", value: "branch" },
      ],
    };
  },
};
</script>

<style scoped>
/* Optional styling */
</style>
