<template>
   <div class="modal-overlay">
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <form
        @submit.prevent="submitExpertise"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
      >
        <!-- Header -->
       <div class="modal-header">
          <div class="flex gap-1 items-center">
            <icon :name="'edit'" />
            <h1 class="font-bold tracking-wide text-lg">Edit Expertise</h1>
          </div>
          <icon :name="'circle-close3'" @click="$emit('close')" class="cursor-pointer" />
        </div>

        <!-- Content -->
        <div class="p-5 w-[32vw] space-y-6">
          <!-- ✅ YEAR LEVEL -->
          <div>
            <label class="font-bold text-sm">Select Year Level:</label>
            <select
              v-model="selectedYearLevel"
              class="w-full border px-3 py-2.5 rounded-md text-sm"
            >
              <option v-for="y in [1, 2, 3, 4]" :key="y" :value="y">
                {{ getYearLevelName(y) }}
              </option>
            </select>
          </div>

          <!-- SEMESTER -->
          <div>
            <label class="font-bold text-sm">Select Semester:</label>
            <select
              v-model="selectedSemester"
              class="w-full border px-3 py-2.5 rounded-md text-sm"
            >
              <option v-for="sem in [1, 2, 3]" :key="sem" :value="sem">
                {{ getSemesterName(sem) }}
              </option>
            </select>
          </div>

          <!-- CONTENT -->
          <div class="space-y-5">
            <!-- ===================== -->
            <!-- EXPERTISE -->
            <!-- ===================== -->
            <div class="space-y-2 relative">
              <label class="font-bold">
                Expertise ({{ getSemesterName(selectedSemester) }})
              </label>

              <input
                v-model="searchQuery"
                @focus="dropdownOpen = true"
                placeholder="Search courses..."
                class="w-full border px-3 py-2.5 rounded-md"
              />

              <!-- DROPDOWN -->
              <ul
                v-if="dropdownOpen && filteredCourses.length"
                class="absolute z-50 w-full bg-white border rounded-md mt-1 max-h-40 overflow-auto"
              >
                <li
                  v-for="course in filteredCourses"
                  :key="course.course_id"
                  @click="addCourse(course)"
                  class="px-3 py-2 hover:bg-green-100 cursor-pointer"
                >
                  <span>
                    {{ course.course_code }} - {{ course.course_title }}

                    <!-- ✅ CURRICULUM DISPLAY -->
                    <span v-if="course.curriculum" class="text-xs text-gray-500 ml-2">
                      ({{ course.curriculum.curriculum_start_year }} -
                      {{ course.curriculum.curriculum_end_year }})
                    </span>
                  </span>
                </li>
              </ul>

              <!-- SELECTED -->
              <div
                v-if="currentSemesterData.expertise.length"
                class="border rounded-md mt-2"
              >
                <div
                  v-for="(item, i) in currentSemesterData.expertise"
                  :key="i"
                  class="flex justify-between px-3 py-2 bg-green-50"
                >
                  <span>
                    {{ item.course_code }} - {{ item.course_title }}

                    <span v-if="item.curriculum" class="text-xs text-gray-500 ml-2">
                      ({{ item.curriculum.curriculum_start_year }} -
                      {{ item.curriculum.curriculum_end_year }})
                    </span>
                  </span>

                  <button type="button" @click="removeCourse(i)">❌</button>
                </div>
              </div>
            </div>

            <!-- ===================== -->
            <!-- OTHER -->
            <!-- ===================== -->
            <div class="space-y-2 relative">
              <label class="font-bold">
                Other Expertise ({{ getSemesterName(selectedSemester) }})
              </label>

              <input
                v-model="otherSearchQuery"
                @focus="otherDropdownOpen = true"
                placeholder="Search courses..."
                class="w-full border px-3 py-2.5 rounded-md"
              />

              <ul
                v-if="otherDropdownOpen && filteredOtherCourses.length"
                class="absolute z-50 w-full bg-white border rounded-md mt-1 max-h-40 overflow-auto"
              >
                <li
                  v-for="course in filteredOtherCourses"
                  :key="course.course_id"
                  @click="addOtherCourse(course)"
                  class="px-3 py-2 hover:bg-green-100 cursor-pointer"
                >
                  <span>
                    {{ course.course_code }} - {{ course.course_title }}

                    <span v-if="course.curriculum" class="text-xs text-gray-500 ml-2">
                      ({{ course.curriculum.curriculum_start_year }} -
                      {{ course.curriculum.curriculum_end_year }})
                    </span>
                  </span>
                </li>
              </ul>

              <div
                v-if="currentSemesterData.other_expertise.length"
                class="border rounded-md mt-2"
              >
                <div
                  v-for="(item, i) in currentSemesterData.other_expertise"
                  :key="i"
                  class="flex justify-between px-3 py-2 bg-green-50"
                >
                  <span>
                    {{ item.course_code }} - {{ item.course_title }}

                    <span v-if="item.curriculum" class="text-xs text-gray-500 ml-2">
                      ({{ item.curriculum.curriculum_start_year }} -
                      {{ item.curriculum.curriculum_end_year }})
                    </span>
                  </span>

                  <button type="button" @click="removeOtherCourse(i)">❌</button>
                </div>
              </div>
            </div>
          </div>

          <!-- SAVE -->
          <div class="flex justify-end">
            <button class="bg-green-600 text-white px-4 py-2 rounded">Save</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";
import axios from "axios";
import { toast } from "vue3-toastify";
export default {
  props: { userData: Object },

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

    // ✅ Get latest curriculum year
    latestCurriculumYear() {
      const years = this.courses
        .map((c) => c.curriculum?.curriculum_start_year)
        .filter(Boolean);

      return years.length ? Math.max(...years) : null;
    },

    // ✅ TRUE only if BOTH old and new curriculum exist
    hasNewCurriculum() {
      const years = this.courses
        .map((c) => c.curriculum?.curriculum_start_year)
        .filter(Boolean);

      const unique = [...new Set(years)];

      return unique.length > 1;
    },

    // =========================
    // EXPERTISE FILTER (FIXED)
    // =========================
    filteredCourses() {
      return this.courses.filter((c) => {
        const year = c.curriculum?.curriculum_start_year;

        let validCurriculum = true;

        if (this.hasNewCurriculum) {
          if (this.selectedYearLevel === 1) {
            validCurriculum = year === this.latestCurriculumYear;
          } else {
            validCurriculum = year !== this.latestCurriculumYear;
          }
        }

        return (
          c.course_semester === this.selectedSemester &&
          c.course_level === this.selectedYearLevel &&
          validCurriculum &&
          c.curriculum?.program_id === this.userData.program.program_id &&
          c.curriculum?.program?.institute_id === this.userData.institute.institute_id &&
          c.course_code.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      });
    },

    // =========================
    // OTHER EXPERTISE FILTER (FIXED)
    // =========================
    filteredOtherCourses() {
      return this.courses.filter((c) => {
        const year = c.curriculum?.curriculum_start_year;

        let validCurriculum = true;

        if (this.hasNewCurriculum) {
          if (this.selectedYearLevel === 1) {
            validCurriculum = year === this.latestCurriculumYear;
          } else {
            validCurriculum = year !== this.latestCurriculumYear;
          }
        }

        return (
          c.course_semester === this.selectedSemester &&
          c.course_level === this.selectedYearLevel &&
          validCurriculum &&
          c.curriculum?.program?.institute_id === this.userData.institute.institute_id &&
          c.course_code.toLowerCase().includes(this.otherSearchQuery.toLowerCase())
        );
      });
    },
  },

  watch: {
    userData: {
      immediate: true,
      handler(val) {
        if (val) {
          this.loadExistingData(val);
        }
      },
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchCourses"]),

    getSemesterName(s) {
      return s === 1 ? "1st" : s === 2 ? "2nd" : "Summer";
    },

    getYearLevelName(y) {
      return `${y}${["st", "nd", "rd", "th"][y - 1]} Year`;
    },

    // =========================
    // LOAD EXISTING DATA (SAFE)
    // =========================
    loadExistingData(user) {
      const semesters = {
        1: { expertise: [], other_expertise: [] },
        2: { expertise: [], other_expertise: [] },
        3: { expertise: [], other_expertise: [] },
      };

      const groupBySemester = (list, target) => {
        (list || []).forEach((item) => {
          const sem = item.course?.course_semester;

          if (sem && semesters[sem]) {
            semesters[sem][target].push(item.course);
          }
        });
      };

      groupBySemester(user.expertise, "expertise");
      groupBySemester(user.other_expertise, "other_expertise");

      this.form.semesters = semesters;
    },

    addCourse(c) {
      this.currentSemesterData.expertise.push(c);
      this.dropdownOpen = false;
    },

    addOtherCourse(c) {
      this.currentSemesterData.other_expertise.push(c);
      this.otherDropdownOpen = false;
    },

    removeCourse(i) {
      this.currentSemesterData.expertise.splice(i, 1);
    },

    removeOtherCourse(i) {
      this.currentSemesterData.other_expertise.splice(i, 1);
    },
    async submitExpertise() {
      try {
        const allExpertise = Object.values(this.form.semesters)
          .flatMap((s) => s.expertise)
          .map((c) => c.course_id);
        const allOther = Object.values(this.form.semesters)
          .flatMap((s) => s.other_expertise)
          .map((c) => c.course_id);

        const payload = { expertise: allExpertise, other_expertise: allOther };

        await axios.patch(
          process.env.VUE_APP_API_BASE_URL + `/auth/update/${this.userData.id}`,
          payload,
          { withCredentials: true }
        );

        toast.success("Expertise updated successfully!");
        this.$emit("updated");
        this.$emit("close");
      } catch (error) {
        toast.error(error?.response?.data?.message || "Failed to update expertise");
      }
    },
  },

  async mounted() {
    await this.fetchCourses();
  },
};
</script>
