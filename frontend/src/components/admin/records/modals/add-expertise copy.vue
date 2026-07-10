<template>
  <div class="modal-overlay">
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form @submit.prevent="submitExpertise" class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg ">
        <!-- HEADER -->
        <div class="w-full px-4 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center">
          <h1 class="font-bold text-lg">Edit Expertise</h1>
          <icon :name="'circle-close3'" @click="$emit('close')" class="cursor-pointer" />
        </div>

        <div class="p-4 w-[28vw] space-y-4">
          <!-- YEAR -->
          <div class="space-y-2">
            <label>Year Level:</label>
            <select v-model="selectedYearLevel" class="w-full border px-3 py-2.5 rounded-md">
              <option v-for="y in [1, 2, 3, 4]" :key="y" :value="y">
                {{ getYearLevelName(y) }}
              </option>
            </select>
          </div>

          <!-- SEM -->
          <div class="space-y-2">
            <label>Semester:</label>
            <select v-model="selectedSemester" class="w-full border px-3 py-2.5 rounded-md">
              <option v-for="s in [1, 2, 3]" :key="s" :value="s">
                {{ getSemesterName(s) }}
              </option>
            </select>
          </div>

          <!-- EXPERTISE -->
          <div class="relative space-y-2">
            <label>Expertise</label>

            <input v-model="searchQuery" @focus="dropdownOpen = true" placeholder="Search courses..."
              class="w-full border px-3 py-2.5 rounded-md" />

            <ul v-if="dropdownOpen && filteredCourses.length" @mouseleave="dropdownOpen = false"
              class="absolute z-50 w-full bg-white border rounded-md mt-1 max-h-40 overflow-auto">
              <li v-for="course in filteredCourses" :key="course.course_id"
                @click="!isAlreadySelected(course) && addCourse(course)"
                class="px-3 py-2 flex justify-between items-center cursor-pointer" :class="isAlreadySelected(course)
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'hover:bg-green-100'
                  ">
                <span> {{ course.course_code }} - {{ course.course_title }} </span>

                <span v-if="isAlreadySelected(course)" class="text-[10px] bg-green-200 px-2 rounded">
                  Selected
                </span>
              </li>
            </ul>

            <div class="mt-3 space-y-1">
              <div v-for="(item, i) in currentSemesterData.expertise" :key="i"
                class="flex justify-between px-4 py-2 bg-defaultGreen text-white rounded">
                <span>{{ item.course_code }} — {{ item.course_title }}</span>
                <button @click="removeCourse(i)">✕</button>
              </div>
            </div>
          </div>

          <!-- OTHER EXPERTISE -->
          <div class="relative space-y-2">
            <label>Other Expertise</label>

            <input v-model="otherSearchQuery" @focus="otherDropdownOpen = true" placeholder="Search courses..."
              class="w-full border px-3 py-2.5 rounded-md" />

            <ul v-if="otherDropdownOpen && filteredOtherCourses.length" @mouseleave="otherDropdownOpen = false"
              class="absolute z-50 w-full bg-white border rounded-md mt-1 max-h-40 overflow-auto">
              <li v-for="course in filteredOtherCourses" :key="course.course_id"
                @click="!isAlreadySelected(course) && addOtherCourse(course)"
                class="px-3 py-2 flex justify-between items-center cursor-pointer" :class="isAlreadySelected(course)
                    ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                    : 'hover:bg-green-100'
                  ">
                <span> {{ course.course_code }} - {{ course.course_title }} </span>

                <span v-if="isAlreadySelected(course)" class="text-[10px] bg-green-200 px-2 rounded">
                  Selected
                </span>
              </li>
            </ul>

            <div class="mt-3 space-y-1">
              <div v-for="(item, i) in currentSemesterData.other_expertise" :key="i"
                class="flex justify-between px-4 py-2 bg-defaultGreen text-white rounded">
                <span>{{ item.course_code }} — {{ item.course_title }}</span>
                <button @click="removeOtherCourse(i)">✕</button>
              </div>
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
import { mapState, mapActions } from "pinia";
import { useFetchDataStore } from "@/store/fetch-data-store";
import axios from "axios";
import { toast } from "vue3-toastify";
export default {
  props: ["userData"],

  data() {
    return {
      selectedSemester: 1,
      selectedYearLevel: 1,
      searchQuery: "",
      otherSearchQuery: "",
      dropdownOpen: false,
      otherDropdownOpen: false,

      form: {
        semesters: {
          1: { expertise: [], other_expertise: [] },
          2: { expertise: [], other_expertise: [] },
          3: { expertise: [], other_expertise: [] },
        },
      },
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["courses"]),

    currentSemesterData() {
      return this.form.semesters[this.selectedSemester];
    },

    filteredCourses() {
      if (!this.courses?.length) return [];
      return this.courses.filter(
        (c) =>
          c.course_semester === this.selectedSemester &&
          c.curriculum?.program?.institute_id ===
          this.userData?.institute?.institute_id &&
          c.curriculum?.program_id === this.userData?.program?.program_id &&
          !this.currentSemesterData.other_expertise.some(
            (e) => e.course_id === c.course_id
          ) &&
          ((c.course_code?.toLowerCase() || "").includes(
            this.searchQuery.toLowerCase()
          ) ||
            (c.course_title?.toLowerCase() || "").includes(
              this.searchQuery.toLowerCase()
            ))
      );
    },
    filteredOtherCourses() {
      if (!this.courses?.length) return [];

      return this.courses.filter(
        (c) =>
          c.course_semester === this.selectedSemester &&
          c.curriculum?.program?.institute_id ===
          this.userData?.institute?.institute_id &&
          // ❌ REMOVE program_id restriction (this is the key change)

          !this.currentSemesterData.expertise.some((e) => e.course_id === c.course_id) &&
          ((c.course_code?.toLowerCase() || "").includes(
            this.otherSearchQuery.toLowerCase()
          ) ||
            (c.course_title?.toLowerCase() || "").includes(
              this.otherSearchQuery.toLowerCase()
            ))
      );
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchCourses"]),

    getSemesterName(s) {
      return s === 1 ? "1st" : s === 2 ? "2nd" : "Summer";
    },
    loadExistingExpertise() {
      if (!this.courses?.length || !this.userData) return;

      // ✅ RESET FIRST to avoid duplicates when reopening modal
      this.form.semesters = {
        1: { expertise: [], other_expertise: [] },
        2: { expertise: [], other_expertise: [] },
        3: { expertise: [], other_expertise: [] },
      };

      const mapCourse = (id) => this.courses.find((c) => c.course_id === id) || null;

      const normalizeCourse = (data) => {
        const matched = mapCourse(data.course_id);

        return (
          matched || {
            course_id: data.course_id,
            course_code: data.course_code,
            course_title: data.course_title,
            course_semester: data.course_semester || 1,
          }
        );
      };

      // ✅ Load regular expertise
      (this.userData.expertise || []).forEach((ex) => {
        const courseData = ex.course || ex;
        const courseObj = normalizeCourse(courseData);

        const sem = courseObj.course_semester || 1;

        if (
          !this.form.semesters[sem].expertise.some(
            (c) => c.course_id === courseObj.course_id
          )
        ) {
          this.form.semesters[sem].expertise.push(courseObj);
        }
      });

      // ✅ Load other expertise
      (this.userData.other_expertise || []).forEach((ex) => {
        const courseData = ex.course || ex;
        const courseObj = normalizeCourse(courseData);

        const sem = courseObj.course_semester || 1;

        if (
          !this.form.semesters[sem].other_expertise.some(
            (c) => c.course_id === courseObj.course_id
          )
        ) {
          this.form.semesters[sem].other_expertise.push(courseObj);
        }
      });
    },
    getYearLevelName(y) {
      return `${y}${["st", "nd", "rd", "th"][y - 1]} Year`;
    },

    isAlreadySelected(course) {
      return (
        this.currentSemesterData.expertise.some(
          (c) => c.course_id === course.course_id
        ) ||
        this.currentSemesterData.other_expertise.some(
          (c) => c.course_id === course.course_id
        )
      );
    },

    addCourse(course) {
      if (this.isAlreadySelected(course)) return;

      if (this.mode === "cross") {
        this.selectedCrossCourses.push(course);
        this.dropdownOpen = false;
        return;
      }

      this.currentSemesterData.expertise.push(course);
      this.dropdownOpen = false;
    },

    addOtherCourse(course) {
      if (this.mode === "cross") return;
      if (this.isAlreadySelected(course)) return;

      this.currentSemesterData.other_expertise.push(course);
      this.otherDropdownOpen = false;
    },

    removeCourse(i) {
      this.currentSemesterData.expertise.splice(i, 1);
    },

    removeOtherCourse(i) {
      this.currentSemesterData.other_expertise.splice(i, 1);
    },

    async submitExpertise() {
      const expertise = Object.values(this.form.semesters)
        .flatMap((s) => s.expertise)
        .map((c) => c.course_id);

      const other_expertise = Object.values(this.form.semesters)
        .flatMap((s) => s.other_expertise)
        .map((c) => c.course_id);

      await axios.patch(
        `${process.env.VUE_APP_API_BASE_URL}/auth/update/${this.userData.id}`,
        {
          expertise,
          other_expertise,
        }
      );
      toast.success("Expertise has been successfull added!");
      this.$emit("updated");
      this.$emit("close");
    },
  },

  async mounted() {
    await this.fetchCourses();

    this.loadExistingExpertise();
  },
};
</script>
