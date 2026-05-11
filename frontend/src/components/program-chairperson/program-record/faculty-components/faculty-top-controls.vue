<template>
  <div class="flex justify-between items-center">
    <!-- LEFT: JOIN TOGGLE -->
    <div
      class="flex items-center gap-4 py-2 px-3 rounded-full border w-max bg-white text-sm"
    >
      <span class="font-medium text-gray-700">Join Scheduled:</span>

 <div class="per-page-container">
        <span
          class="font-semibold"
          :class="isJoined ? 'text-green-600' : 'text-gray-400'"
        >
          {{ isJoined ? "YES" : "NOT" }}
        </span>

        <button
          @click="$emit('update:isJoined', !isJoined)"
          :class="[
            'w-12 h-6 rounded-full p-1 flex items-center transition-colors duration-300 focus:outline-none',
            isJoined ? 'bg-green-500' : 'bg-gray-300',
          ]"
        >
          <span
            class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300"
            :class="isJoined ? 'translate-x-6' : 'translate-x-0'"
          ></span>
        </button>
      </div>
    </div>

    <!-- RIGHT SIDE -->
    <div class="flex items-center gap-2 flex-wrap">
      <!-- VIEW TOGGLE -->
      <!-- SEARCH INPUT -->

      <div class="relative w-full sm:w-[280px]">
        <input
          :value="searchQuery"
          @input="$emit('update:searchQuery', $event.target.value)"
          type="text"
          placeholder="Search faculty..."
          class="rounded-xl border border-defaultGreen px-4 py-2.5 pl-10 text-sm shadow-sm w-full"
        />
        <div
          class="absolute inset-y-0 left-3 flex items-center text-green-700 pointer-events-none"
        >
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
        </div>
      </div>
      <!-- COMPARE BUTTON -->
      <div
        v-show="!showCompareSelection"
        @click="$emit('toggleCompareSelection')"
        class="flex items-center gap-2 px-3 py-2 border text-defaultGreen border-defaultGreen rounded-xl hover:bg-defaultGreen hover:text-white hover:shadow-lg cursor-pointer transition duration-200"
      >
        <div
          class="btn-add-icon"
        >
          <icon name="faculty-loading1" />
        </div>
           <span class="btn-add-text">Compare</span>
      </div>

      <!-- COMPARE SECTION -->
      <div v-show="showCompareSelection" class="flex items-center gap-2 flex-wrap">
        <div class="flex gap-2 items-center">
          <!-- Instructor A -->
          <select
            :value="compareInstructorA"
            @change="$emit('update:compareInstructorA', $event.target.value)"
            class="rounded-xl border border-defaultGreen px-2 py-2.5 text-sm text-defaultGreen shadow-sm"
          >
            <option value="">Select Instructor</option>
            <option
              v-for="instructor in instructorList"
              :key="'a-' + instructor"
              :value="instructor"
            >
              {{ instructor }}
            </option>
          </select>

          <!-- Instructor B -->
          <select
            :value="compareInstructorB"
            @change="$emit('update:compareInstructorB', $event.target.value)"
            class="rounded-xl border border-defaultGreen px-2 py-2.5 text-sm text-defaultGreen shadow-sm"
          >
            <option value="">Select Instructor</option>
            <option
              v-for="instructor in instructorList"
              :key="'b-' + instructor"
              :value="instructor"
            >
              {{ instructor }}
            </option>
          </select>

          <!-- COMPARE BUTTON -->
          <div
            @click="emitCompare"
            :class="[
              'flex items-center gap-2 px-3 py-2 border rounded-xl transition duration-200',
              canCompare
                ? 'text-defaultGreen border-defaultGreen hover:bg-defaultGreen hover:text-white hover:shadow-lg cursor-pointer'
                : 'text-gray-400 border-gray-300 cursor-not-allowed',
            ]"
          >
            <div
              class="btn-add-icon"
            >
              <icon name="faculty-loading1" />
            </div>
               <span class="btn-add-text">Compare</span>
          </div>
        </div>

        <!-- CLOSE -->
        <button
          @click="$emit('backFromCompare')"
          class="flex items-center gap-2 p-1 border border-gray-400 rounded-full shadow-sm hover:bg-gray-100 transition"
        >
          <icon name="circle-close" class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
export default {
  name: "FacultyTopControls",
  components: {
    icon,
  },
  props: {
    isJoined: Boolean,
    showFacultyTable: Boolean,
    showCompareSelection: Boolean,
    compareInstructorA: String,
    compareInstructorB: String,
    instructorList: Array,
    searchQuery: String,
  },
  computed: {
    canCompare() {
      return (
        this.compareInstructorA &&
        this.compareInstructorB &&
        this.compareInstructorA !== this.compareInstructorB
      );
    },
  },
  methods: {
    emitCompare() {
      if (this.canCompare) {
        this.$emit("compare");
      }
    },
  },
};
</script>
