<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submit"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
      >
        <!-- HEADER -->
        <div
          class="w-full px-4 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center"
        >
          <h1 class="font-bold text-lg">Cross Assign Expertise</h1>
          <span @click="$emit('close')" class="cursor-pointer">✕</span>
        </div>

        <div class="p-4 w-[28vw] space-y-4">
          <!-- SEARCH DROPDOWN -->
          <div class="relative space-y-2">
            <label>Search Courses</label>

            <input
              v-model="search"
              @focus="dropdownOpen = true"
              placeholder="Search courses..."
              class="w-full border px-3 py-2.5 rounded-md"
            />

            <ul
              v-if="dropdownOpen && filteredCourses.length"
              @mouseleave="dropdownOpen = false"
              class="absolute z-50 w-full bg-white border rounded-md mt-1 max-h-40 overflow-auto"
            >
              <li
                v-for="course in filteredCourses"
                :key="course.course_id"
                @click="add(course)"
                class="px-3 py-2 flex justify-between items-center cursor-pointer hover:bg-green-100"
                :class="
                  isSelected(course) ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : ''
                "
              >
                <span> {{ course.course_code }} - {{ course.course_title }} </span>

                <span
                  v-if="isSelected(course)"
                  class="text-[10px] bg-green-200 px-2 rounded"
                >
                  Selected
                </span>
              </li>
            </ul>
          </div>

          <!-- SELECTED COURSES -->
          <div class="space-y-1">
            <div
              v-for="(c, i) in selected"
              :key="i"
              class="flex justify-between px-4 py-2 bg-defaultGreen text-white rounded"
            >
              <span>{{ c.course_code }} — {{ c.course_title }}</span>
              <button @click.prevent="remove(i)">✕</button>
            </div>
          </div>

          <!-- ACTION -->
          <div class="flex justify-end gap-2">
            <button type="button" @click="$emit('close')" class="btn-cancel">
              Cancel
            </button>
            <button type="submit" class="btn-save">Save</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useFetchDataStore } from "@/store/fetch-data-store";
import axios from "axios";
import { toast } from "vue3-toastify";

export default {
  props: ["userData"],

  data() {
    return {
      search: "",
      dropdownOpen: false,
      selected: [],
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["courses"]),

    filteredCourses() {
      if (!this.courses?.length) return [];

      return this.courses.filter((c) => {
        const matchSearch = `${c.course_code} ${c.course_title}`
          .toLowerCase()
          .includes(this.search.toLowerCase());

        return matchSearch;
      });
    },
  },

  methods: {
    isSelected(course) {
      return this.selected.some((c) => c.course_id === course.course_id);
    },

    add(course) {
      if (!this.isSelected(course)) {
        this.selected.push(course);
      }
      this.dropdownOpen = false;
    },

    remove(i) {
      this.selected.splice(i, 1);
    },

    async submit() {
      if (!this.selected.length) {
        toast.warning("Please select at least one course.");
        return;
      }

      const payload = this.selected.map((c) => ({
        user_id: this.userData.id,
        course_id: c.course_id,
      }));

      try {
        await axios.post(`${process.env.VUE_APP_API_BASE_URL}/cross-assign`, payload);

        toast.success("Cross Assign saved!");
        this.$emit("updated");
        this.$emit("close");
      } catch (err) {
        toast.error("Failed to save cross assign.");
      }
    },
  },

  async mounted() {
    const store = useFetchDataStore();
    await store.fetchCourses();
  },
};
</script>
