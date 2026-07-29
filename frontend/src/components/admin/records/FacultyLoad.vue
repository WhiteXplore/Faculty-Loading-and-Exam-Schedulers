<template>
  <div class="p-2">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="font-semibold tracking-wide text-sm px-1">
        Faculty Load Generations
      </h1>
    </div>

    <!-- Tabs -->
    <div class="mt-2 justify-between flex items-center">
      <div class="flex gap-1">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          @click="activeTab = tab.value"
          :class="[
            'px-4 py-2 rounded-t-lg text-sm',
            activeTab === tab.value
              ? 'bg-defaultGreen text-white  font-semibold border border-gray-300 border-b-white shadow-sm  '
              : 'bg-gray-200 text-gray-600 hover:bg-gray-300 ',
          ]"
        >
          {{ tab.label }}
        </button>
      </div>

      <!-- Breadcrumb -->
      <!-- <div class="text-[13px] text-gray-700 px-6 flex justify-end">
        Pages / Faculty Loading
        <span class="text-gray-400 mx-1">/</span>
        <span class="font-semibold text-defaultGreen">{{ activeTab }}</span>
      </div> -->
    </div>

    <!-- Content Card -->
    <div class="bg-white border-t-0 mt-2">
      <tableFacultyLoading v-if="activeTab === 'Faculty Loading'" />
      <tableUnscheduledMeetings v-if="activeTab === 'Unschededuled Meeting'" />
      <tableFacultyLoading2 v-if="activeTab === 'Scheduled by Rooms'" />
      <!-- <tableFacultyLoading3 v-if="activeTab === 'Scheduled by Rooms2'" /> -->
      <tableAvailableRooms v-if="activeTab === 'Available Rooms'" />
      <tableTestSearch v-if="activeTab === 'Table Search'" />
      <!-- Future tabs can be added here -->
    </div>
  </div>
</template>

<script>
import tableAvailableRooms from "./tables/table-available-rooms.vue";
import tableFacultyLoading from "./tables/table-faculty-loading.vue";
import tableFacultyLoading2 from "./tables/table-schedule-by-room.vue";
// import tableFacultyLoading3 from "./tables/table-schedule-by-room copy.vue";
import tableTestSearch from "./tables/table-test-search.vue";
import tableUnscheduledMeetings from "@/components/program-chairperson/program-record/tables/table-unscheduled-meetings.vue";
export default {
  name: "FacultyLoadingPage",
  components: {
    tableFacultyLoading,
    tableFacultyLoading2,
    tableAvailableRooms,
    // tableFacultyLoading3,
    tableTestSearch,
    tableUnscheduledMeetings,
  },
  data() {
    return {
      activeTab: "Faculty Loading",
      tabs: [
        { label: "Faculty Loading", value: "Faculty Loading" },
        { label: "Scheduled by Rooms", value: "Scheduled by Rooms" },
        { label: "Unschededuled Meetings", value: "Unschededuled Meeting" },
        // { label: "Scheduled by Rooms2", value: "Scheduled by Rooms2" },
        { label: "Available Rooms", value: "Available Rooms" },
        { label: "Table Search", value: "Table Search" },
      ],
    };
  },
};
</script>

<style scoped>
/* Optional styling */
</style>
