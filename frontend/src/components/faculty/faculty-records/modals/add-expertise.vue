<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form @submit.prevent="submitExpertise" class="modal-container">
        <div class="modal-header">
          <div class="flex gap-1 items-center">
            <icon :name="'edit'" />
            <h1 class="font-bold tracking-wide text-lg">Edit Expertises</h1>
          </div>

          <icon :name="'circle-close3'" @click="$emit('close')" class="cursor-pointer" />
        </div>

        <div class="w-[25vw] modal-body">
          <div class="w-full space-y-2">
            <label class="input-label">Select Year Level:</label>
            <select
              v-model="selectedYearLevel"
              class="w-full border px-3 py-2.5 rounded-md text-sm"
            >
              <option v-for="y in [1, 2, 3, 4]" :key="y" :value="y">
                {{ getYearLevelName(y) }}
              </option>
            </select>
          </div>

          <div class="w-full space-y-2">
            <label class="input-label">Select Semester:</label>
            <select
              v-model="selectedSemester"
              class="w-full border px-3 py-2.5 rounded-md text-sm"
            >
              <option v-for="sem in [1, 2, 3]" :key="sem" :value="sem">
                {{ getSemesterName(sem) }}
              </option>
            </select>
          </div>

          <div class="space-y-5">
            <div class="w-full space-y-2 relative">
              <label class="input-label">
                Expertise ({{ getSemesterName(selectedSemester) }})
              </label>

              <input
                v-model="searchQuery"
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
                  @click="addCourse(course)"
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
                v-if="currentSemesterData.expertise.length"
                class="border rounded-md mt-2 space-y-1"
              >
                <div
                  v-for="(item, i) in currentSemesterData.expertise"
                  :key="`${item.course_id}-primary-${i}`"
                  class="flex justify-between items-center px-4 py-2 bg-defaultGreen text-white rounded gap-3"
                >
                  <span> {{ item.course_code }} - {{ item.course_title }} </span>

                  <button type="button" @click="removeCourse(i)">❌</button>
                </div>
              </div>
            </div>

            <div class="w-full space-y-2 relative">
              <label class="input-label">
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
                @mouseleave="otherDropdownOpen = false"
                class="absolute z-50 w-full bg-white border rounded-md mt-1 max-h-40 overflow-auto"
              >
                <li
                  v-for="course in filteredOtherCourses"
                  :key="course.course_id"
                  @click="addOtherCourse(course)"
                  class="px-3 py-2 hover:bg-green-100 cursor-pointer"
                >
                  <span>
                    <span
                      v-if="course.program_code"
                      class="px-2 py-0.5 rounded-full bg-defaultGreen text-white text-[10px] mr-1"
                    >
                      {{ course.program_code }}
                    </span>

                    {{ course.course_code }} - {{ course.course_title }}
                  </span>
                </li>
              </ul>

              <div
                v-if="currentSemesterData.other_expertise.length"
                class="border rounded-md mt-2 space-y-1"
              >
                <div
                  v-for="(item, i) in currentSemesterData.other_expertise"
                  :key="`${item.course_id}-other-${i}`"
                  class="flex justify-between items-center px-4 py-2 bg-defaultGreen text-white rounded gap-3"
                >
                  <span> {{ item.course_code }} - {{ item.course_title }} </span>

                  <button type="button" @click="removeOtherCourse(i)">❌</button>
                </div>
              </div>
            </div>
          </div>

          <div class="flex gap-2 justify-end">
            <button type="button" class="btn-cancel" @click="$emit('close')">
              Cancel
            </button>

            <button type="submit" class="btn-save">Submit</button>
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
import icon from "@/assets/icon.vue";

export default {
  props: {
    userData: Object,
  },

  components: {
    icon,
  },

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
    ...mapState(useFetchDataStore, ["courses", "programs", "curriculum_courses"]),

    currentUserInstituteId() {
      return Number(this.userData?.institute?.institute_id || 0);
    },

    currentUserProgramId() {
      return Number(this.userData?.program?.program_id || 0);
    },

    currentSemesterData() {
      return this.form.semesters[this.selectedSemester];
    },

    normalizedCurriculumCourses() {
      if (!Array.isArray(this.curriculum_courses)) return [];

      return this.curriculum_courses
        .map((item) => ({
          curriculum_course_id: item.curriculum_course_id,
          curriculum_id: item.curriculum_id,
          course_id: Number(item.course?.course_id || item.course_id),
          course_code: item.course?.course_code || "",
          course_title: item.course?.course_title || "",
          course_semester: Number(item.course?.course_semester || 0),
          course_level: Number(item.course?.course_level || 0),

          institute_id: Number(item.curriculum?.institute_id || 0),
          program_id: Number(item.curriculum?.program_id || 0),

          program_code: item.curriculum?.program?.program_code || "",
          program_name: item.curriculum?.program?.program_name || "",
          curriculum: item.curriculum || null,
        }))
        .filter((c) => c.course_id);
    },

    normalizedCourses() {
      if (!Array.isArray(this.courses)) return [];

      return this.courses.map((c) => ({
        course_id: Number(c.course_id),
        course_code: c.course_code || "",
        course_title: c.course_title || "",
        course_semester: Number(c.course_semester || 0),
        course_level: Number(c.course_level || 0),
        program_id: Number(c.program_id || c.program?.program_id || 0),
        program_code: c.program?.program_code || "",
        program_name: c.program?.program_name || "",
        institute_id: Number(c.institute_id || c.program?.institute_id || 0),
        curriculum: c.curriculum || null,
      }));
    },

    filteredCourses() {
      const search = (this.searchQuery || "").toLowerCase().trim();

      const matchSearch = (c) =>
        !search ||
        (c.course_code || "").toLowerCase().includes(search) ||
        (c.course_title || "").toLowerCase().includes(search);

      const sameProgramCourses = this.normalizedCurriculumCourses.filter((c) => {
        return (
          Number(c.institute_id) === this.currentUserInstituteId &&
          Number(c.program_id) === this.currentUserProgramId
        );
      });

      const strictMatch = sameProgramCourses.filter((c) => {
        return (
          Number(c.course_semester) === Number(this.selectedSemester) &&
          Number(c.course_level) === Number(this.selectedYearLevel)
        );
      });

      const source = strictMatch.length ? strictMatch : sameProgramCourses;

      return source.filter((c) => {
        const notInPrimary = !this.currentSemesterData.expertise.some(
          (e) => Number(e.course_id) === Number(c.course_id)
        );

        const notInOther = !this.currentSemesterData.other_expertise.some(
          (e) => Number(e.course_id) === Number(c.course_id)
        );

        return matchSearch(c) && notInPrimary && notInOther;
      });
    },

    filteredOtherCourses() {
      const search = (this.otherSearchQuery || "").toLowerCase().trim();

      const matchSearch = (c) =>
        !search ||
        (c.course_code || "").toLowerCase().includes(search) ||
        (c.course_title || "").toLowerCase().includes(search);

      const otherProgramCurriculumCourses = this.normalizedCurriculumCourses.filter(
        (c) => {
          return (
            Number(c.institute_id) === this.currentUserInstituteId &&
            Number(c.program_id) !== this.currentUserProgramId
          );
        }
      );

      const strictMatch = otherProgramCurriculumCourses.filter((c) => {
        return (
          Number(c.course_semester) === Number(this.selectedSemester) &&
          Number(c.course_level) === Number(this.selectedYearLevel)
        );
      });

      const source = strictMatch.length ? strictMatch : otherProgramCurriculumCourses;

      const uniqueCourseIds = [
        ...new Set(source.map((c) => Number(c.course_id)).filter(Boolean)),
      ];

      return this.normalizedCourses
        .filter((c) => uniqueCourseIds.includes(Number(c.course_id)))
        .filter((c) => {
          const notInPrimary = !this.currentSemesterData.expertise.some(
            (e) => Number(e.course_id) === Number(c.course_id)
          );

          const notInOther = !this.currentSemesterData.other_expertise.some(
            (e) => Number(e.course_id) === Number(c.course_id)
          );

          return matchSearch(c) && notInPrimary && notInOther;
        })
        .sort((a, b) => (a.course_code || "").localeCompare(b.course_code || ""));
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
    ...mapActions(useFetchDataStore, [
      "fetchCourses",
      "fetchPrograms",
      "fetchCurriculumCourses",
    ]),

    getSemesterName(s) {
      return Number(s) === 1 ? "1st" : Number(s) === 2 ? "2nd" : "Summer";
    },

    getYearLevelName(y) {
      return `${y}${["st", "nd", "rd", "th"][y - 1]} Year`;
    },

    isAlreadySelected(course) {
      const id = Number(course?.course_id);
      if (!id) return false;

      return (
        this.currentSemesterData.expertise.some((c) => Number(c.course_id) === id) ||
        this.currentSemesterData.other_expertise.some((c) => Number(c.course_id) === id)
      );
    },

    addCourse(course) {
      if (this.isAlreadySelected(course)) return;

      this.currentSemesterData.expertise.push({ ...course });
      this.dropdownOpen = false;
      this.searchQuery = "";
    },

    addOtherCourse(course) {
      if (this.isAlreadySelected(course)) return;

      this.currentSemesterData.other_expertise.push({ ...course });
      this.otherDropdownOpen = false;
      this.otherSearchQuery = "";
    },

    removeCourse(i) {
      this.currentSemesterData.expertise.splice(i, 1);
    },

    removeOtherCourse(i) {
      this.currentSemesterData.other_expertise.splice(i, 1);
    },

    loadExistingData(user) {
      const semesters = {
        1: { expertise: [], other_expertise: [] },
        2: { expertise: [], other_expertise: [] },
        3: { expertise: [], other_expertise: [] },
      };

      const allMappedCourses = [
        ...this.normalizedCurriculumCourses,
        ...this.normalizedCourses,
      ];

      const mapCourse = (id) =>
        allMappedCourses.find((c) => Number(c.course_id) === Number(id)) || null;

      const fallbackCourse = (ex) => ({
        course_id: Number(ex?.course?.course_id || ex?.course_id),
        course_code: ex?.course?.course_code || "",
        course_title: ex?.course?.course_title || "",
        course_semester: Number(ex?.course?.course_semester || 1),
        course_level: Number(ex?.course?.course_level || 1),
        program_id: Number(ex?.course?.program_id || 0),
        program_code: ex?.course?.program?.program_code || "",
        curriculum: ex?.course?.curriculum || null,
      });

      (user.expertise || []).forEach((ex) => {
        if (ex.status === "CROSS") return;

        const rawId = ex?.course?.course_id || ex?.course_id;
        const course = mapCourse(rawId) || fallbackCourse(ex);

        const sem = Number(course.course_semester || 1);

        if (!semesters[sem]) {
          semesters[sem] = { expertise: [], other_expertise: [] };
        }

        if (ex.status === "OTHER") {
          semesters[sem].other_expertise.push(course);
        } else {
          semesters[sem].expertise.push(course);
        }
      });

      this.form.semesters = semesters;
    },

    async submitExpertise() {
      try {
        const existingCross = (this.userData.expertise || [])
          .filter((e) => e.status === "CROSS")
          .map((e) => ({
            course_id: e.course?.course_id || e.course_id,
            status: "CROSS",
          }));

        const assignPayload = Object.values(this.form.semesters).flatMap((s) => [
          ...s.expertise.map((c) => ({
            course_id: c.course_id,
            status: "PRIMARY",
          })),
          ...s.other_expertise.map((c) => ({
            course_id: c.course_id,
            status: "OTHER",
          })),
        ]);

        await axios.patch(
          `${process.env.VUE_APP_API_BASE_URL}/auth/update/${this.userData.id}`,
          {
            expertise: [...assignPayload, ...existingCross],
          },
          { withCredentials: true }
        );

        toast.success("Expertise updated successfully!");
        this.$emit("updated");
        this.$emit("close");
      } catch (error) {
        console.error(error);
        toast.error(error?.response?.data?.message || "Failed to update expertise");
      }
    },
  },

  async mounted() {
    await this.fetchCourses();
    await this.fetchPrograms();
    await this.fetchCurriculumCourses();

    if (this.userData) {
      this.loadExistingData(this.userData);
    }
  },
};
</script>
