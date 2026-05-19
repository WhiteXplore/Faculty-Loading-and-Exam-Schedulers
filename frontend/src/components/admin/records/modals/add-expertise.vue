<template>
  <div class="modal-overlay">
    <div class="rounded-[16px] shadow-lg animate-slideUp">
      <form
        @submit.prevent="submitExpertise"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
      >
        <!-- HEADER -->
        <div
          class="w-full px-4 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center"
        >
          <h1 class="font-bold text-lg">Assign Expertise</h1>

          <icon :name="'circle-close3'" @click="$emit('close')" class="cursor-pointer" />
        </div>

        <div class="p-3 w-[34vw] space-y-4">
          <!-- TABS -->
          <div class="grid grid-cols-2 bg-gray-100 p-1 rounded-xl">
            <button
              type="button"
              @click="switchTab('assign')"
              class="py-2.5 rounded-lg font-semibold transition"
              :class="
                activeTab === 'assign'
                  ? 'bg-defaultGreen text-white shadow'
                  : 'text-gray-600 hover:text-defaultGreen'
              "
            >
              Expertise Assignment
            </button>

            <button
              type="button"
              @click="switchTab('cross')"
              class="py-2.5 rounded-lg font-semibold transition"
              :class="
                activeTab === 'cross'
                  ? 'bg-defaultGreen text-white shadow'
                  : 'text-gray-600 hover:text-defaultGreen'
              "
            >
              Cross Assign
            </button>
          </div>

          <!-- ========================= -->
          <!-- TAB 1: ASSIGN EXPERTISE -->
          <!-- ========================= -->
          <div v-if="activeTab === 'assign'" class="space-y-4">
            <!-- YEAR + SEMESTER -->
            <div class="grid grid-cols-2 gap-3">
              <div class="space-y-2">
                <label class="font-semibold text-gray-700">Year Level</label>
                <select
                  v-model="selectedYearLevel"
                  class="w-full border px-3 py-2.5 rounded-md outline-none focus:ring-2 focus:ring-green-600/20"
                >
                  <option v-for="y in [1, 2, 3, 4]" :key="y" :value="y">
                    {{ getYearLevelName(y) }}
                  </option>
                </select>
              </div>

              <div class="space-y-2">
                <label class="font-semibold text-gray-700">Semester</label>
                <select
                  v-model="selectedSemester"
                  class="w-full border px-3 py-2.5 rounded-md outline-none focus:ring-2 focus:ring-green-600/20"
                >
                  <option v-for="s in [1, 2, 3]" :key="s" :value="s">
                    {{ getSemesterName(s) }}
                  </option>
                </select>
              </div>
            </div>

            <!-- EXPERTISE -->
            <div class="relative space-y-2">
              <label class="font-semibold text-gray-700">Expertise</label>

              <input
                v-model="searchQuery"
                @focus="dropdownOpen = true"
                placeholder="Search courses..."
                class="w-full border px-3 py-2.5 rounded-md outline-none focus:ring-2 focus:ring-green-600/20"
              />

              <p v-if="noStrictAssignCourses" class="text-xs text-orange-600">
                No matching courses for this semester/year. Showing fallback data.
              </p>

              <ul
                v-if="dropdownOpen && filteredCourses.length"
                @mouseleave="dropdownOpen = false"
                class="absolute z-50 w-full bg-white border rounded-md mt-1 max-h-40 overflow-auto shadow-lg"
              >
                <li
                  v-for="course in filteredCourses"
                  :key="course.course_id"
                  @click="!isAlreadySelected(course) && addCourse(course)"
                  class="px-3 py-2 flex justify-between items-center cursor-pointer"
                  :class="
                    isAlreadySelected(course)
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'hover:bg-green-100'
                  "
                >
                  <span>{{ course.course_code }} - {{ course.course_title }}</span>

                  <span
                    v-if="isAlreadySelected(course)"
                    class="text-[10px] bg-green-200 px-2 rounded"
                  >
                    Selected
                  </span>
                </li>
              </ul>

              <div class="mt-3 space-y-1">
                <div
                  v-for="(item, i) in currentSemesterData.expertise"
                  :key="`${item.course_id}-primary-${i}`"
                  class="flex justify-between items-center px-4 py-2 bg-defaultGreen text-white rounded-lg"
                >
                  <span>{{ item.course_code }} — {{ item.course_title }}</span>
                  <button type="button" @click="removeCourse(i)">✕</button>
                </div>
              </div>
            </div>

            <!-- OTHER EXPERTISE -->
            <div class="relative space-y-2">
              <label class="font-semibold text-gray-700">Other Expertise</label>

              <input
                v-model="otherSearchQuery"
                @focus="otherDropdownOpen = true"
                placeholder="Search courses..."
                class="w-full border px-3 py-2.5 rounded-md outline-none focus:ring-2 focus:ring-green-600/20"
              />

              <ul
                v-if="otherDropdownOpen && filteredOtherCourses.length"
                @mouseleave="otherDropdownOpen = false"
                class="absolute z-50 w-full bg-white border rounded-md mt-1 max-h-40 overflow-auto shadow-lg"
              >
                <li
                  v-for="course in filteredOtherCourses"
                  :key="course.course_id"
                  @click="!isAlreadySelected(course) && addOtherCourse(course)"
                  class="px-3 py-2 flex justify-between items-center cursor-pointer"
                  :class="
                    isAlreadySelected(course)
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'hover:bg-green-100'
                  "
                >
                  <span>{{ course.course_code }} - {{ course.course_title }}</span>

                  <span
                    v-if="isAlreadySelected(course)"
                    class="text-[10px] bg-green-200 px-2 rounded"
                  >
                    Selected
                  </span>
                </li>
              </ul>

              <div class="mt-3 space-y-1">
                <div
                  v-for="(item, i) in currentSemesterData.other_expertise"
                  :key="`${item.course_id}-other-${i}`"
                  class="flex justify-between items-center px-4 py-2 bg-defaultGreen text-white rounded-lg"
                >
                  <span>{{ item.course_code }} — {{ item.course_title }}</span>
                  <button type="button" @click="removeOtherCourse(i)">✕</button>
                </div>
              </div>
            </div>
          </div>

          <!-- ========================= -->
          <!-- TAB 2: CROSS ASSIGN -->
          <!-- ========================= -->
          <div v-else class="space-y-4">
            <div class="relative space-y-2">
              <label class="font-semibold text-gray-700">Cross Expertise</label>

              <input
                v-model="searchQuery"
                @focus="dropdownOpen = true"
                placeholder="Search all courses..."
                class="w-full border px-3 py-2.5 rounded-md outline-none focus:ring-2 focus:ring-green-600/20"
              />

              <ul
                v-if="dropdownOpen && filteredCourses.length"
                @mouseleave="dropdownOpen = false"
                class="absolute z-50 w-full bg-white border rounded-md mt-1 max-h-40 overflow-auto shadow-lg"
              >
                <li
                  v-for="course in filteredCourses"
                  :key="course.course_id"
                  @click="!isAlreadySelected(course) && addCourse(course)"
                  class="px-3 py-2 flex justify-between items-center cursor-pointer"
                  :class="
                    isAlreadySelected(course)
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'hover:bg-green-100'
                  "
                >
                  <span>
                    <span
                      v-if="course.program_code"
                      class="px-2 py-0.5 mr-2 rounded-full bg-defaultGreen text-white text-[10px]"
                    >
                      {{ course.program_code }}
                    </span>
                    {{ course.course_code }} - {{ course.course_title }}
                  </span>

                  <span
                    v-if="isAlreadySelected(course)"
                    class="text-[10px] bg-green-200 px-2 rounded"
                  >
                    Selected
                  </span>
                </li>
              </ul>
            </div>

            <div class="space-y-1">
              <div
                v-for="(item, i) in selectedCrossCourses"
                :key="`${item.course_id}-cross-${i}`"
                class="flex justify-between items-center px-4 py-2 bg-defaultGreen text-white rounded-lg"
              >
                <span>
                  <span
                    v-if="item.program_code"
                    class="px-2 py-0.5 mr-2 rounded-full bg-white text-defaultGreen text-[10px]"
                  >
                    {{ item.program_code }}
                  </span>
                  {{ item.course_code }} — {{ item.course_title }}
                </span>

                <button type="button" @click="removeCourse(i)">✕</button>
              </div>
            </div>
          </div>

          <!-- ACTION -->
          <div class="flex justify-end gap-2 pt-2">
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
  props: {
    userData: Object,
    mode: {
      type: String,
      default: "assign",
    },
  },

  data() {
    return {
      activeTab: this.mode === "cross" ? "cross" : "assign",

      selectedSemester: 1,
      selectedYearLevel: 1,

      searchQuery: "",
      otherSearchQuery: "",

      dropdownOpen: false,
      otherDropdownOpen: false,

      selectedProgramId: "",

      form: {
        semesters: {
          1: { expertise: [], other_expertise: [] },
          2: { expertise: [], other_expertise: [] },
          3: { expertise: [], other_expertise: [] },
        },
      },

      selectedCrossCourses: [],
      originalAssignSnapshot: "",
      originalCrossSnapshot: "",
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["courses", "programs", "curriculum_courses"]),
    hasUnsavedAssignChanges() {
      return (
        this.originalAssignSnapshot &&
        this.originalAssignSnapshot !== this.getAssignSnapshot()
      );
    },

    hasUnsavedCrossChanges() {
      return (
        this.originalCrossSnapshot &&
        this.originalCrossSnapshot !== this.getCrossSnapshot()
      );
    },
    currentUserInstituteId() {
      return Number(this.userData?.institute?.institute_id || 0);
    },

    currentUserProgramId() {
      return Number(this.userData?.program?.program_id || 0);
    },

    usedCourseIds() {
      if (!Array.isArray(this.userData?.expertise)) return [];

      return this.userData.expertise
        .map((e) => e?.course?.course_id || e?.course_id)
        .filter(Boolean)
        .map(Number);
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
          course_lec: item.course?.course_lec ?? null,
          course_lab: item.course?.course_lab ?? null,
          course_requisite: item.course?.course_requisite ?? null,

          institute_id: Number(item.curriculum?.institute_id || 0),
          program_id: Number(item.curriculum?.program_id || 0),

          program_code: item.curriculum?.program?.program_code || "",
          program_name: item.curriculum?.program?.program_name || "",
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
        course_lec: c.course_lec ?? null,
        course_lab: c.course_lab ?? null,
        course_requisite: c.course_requisite ?? null,
        program_id: Number(c.program_id || c.program?.program_id || 0),
        program_code: c.program?.program_code || "",
        program_name: c.program?.program_name || "",
        institute_id: Number(c.institute_id || c.program?.institute_id || 0),
      }));
    },

    noStrictAssignCourses() {
      if (this.activeTab !== "assign") return false;

      return (
        this.normalizedCurriculumCourses.filter(
          (c) =>
            Number(c.institute_id) === this.currentUserInstituteId &&
            Number(c.program_id) === this.currentUserProgramId &&
            Number(c.course_semester) === Number(this.selectedSemester) &&
            Number(c.course_level) === Number(this.selectedYearLevel)
        ).length === 0
      );
    },

    filteredCourses() {
      const search = (this.searchQuery || "").toLowerCase().trim();

      const matchSearch = (c) =>
        !search ||
        (c.course_code || "").toLowerCase().includes(search) ||
        (c.course_title || "").toLowerCase().includes(search);

      if (this.activeTab === "cross") {
        return this.normalizedCourses.filter((c) => {
          const sameProgram =
            !this.selectedProgramId ||
            Number(c.program_id) === Number(this.selectedProgramId);

          const notSelected = !this.selectedCrossCourses.some(
            (e) => Number(e.course_id) === Number(c.course_id)
          );

          return matchSearch(c) && sameProgram && notSelected;
        });
      }

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
        const notInOther = !this.currentSemesterData.other_expertise.some(
          (e) => Number(e.course_id) === Number(c.course_id)
        );

        return matchSearch(c) && notInOther;
      });
    },

    filteredOtherCourses() {
      if (this.activeTab === "cross") return [];

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

  methods: {
    ...mapActions(useFetchDataStore, [
      "fetchCourses",
      "fetchPrograms",
      "fetchCurriculumCourses",
    ]),
    getCrossSnapshot() {
      const payload = this.selectedCrossCourses.map((c) => ({
        course_id: Number(c.course_id),
        status: "CROSS",
      }));

      return JSON.stringify(payload.sort((a, b) => a.course_id - b.course_id));
    },
    getAssignSnapshot() {
      const payload = Object.values(this.form.semesters).flatMap((s) => [
        ...s.expertise.map((c) => ({
          course_id: Number(c.course_id),
          status: "PRIMARY",
        })),
        ...s.other_expertise.map((c) => ({
          course_id: Number(c.course_id),
          status: "OTHER",
        })),
      ]);

      return JSON.stringify(
        payload.sort((a, b) => {
          if (a.status !== b.status) return a.status.localeCompare(b.status);
          return a.course_id - b.course_id;
        })
      );
    },

    switchTab(tab) {
      if (tab === this.activeTab) return;

      if (
        this.activeTab === "assign" &&
        tab === "cross" &&
        this.hasUnsavedAssignChanges
      ) {
        toast.warning(
          "Please save your Expertise Assignment changes first before proceeding to Cross Assign."
        );
        return;
      }

      if (this.activeTab === "cross" && tab === "assign" && this.hasUnsavedCrossChanges) {
        toast.warning(
          "Please save your Cross Assign changes first before proceeding to Expertise Assignment."
        );
        return;
      }

      this.activeTab = tab;
      this.searchQuery = "";
      this.otherSearchQuery = "";
      this.dropdownOpen = false;
      this.otherDropdownOpen = false;
    },
    getSemesterName(s) {
      return s === 1 ? "1st Semester" : s === 2 ? "2nd Semester" : "Summer";
    },

    getYearLevelName(y) {
      return `${y}${["st", "nd", "rd", "th"][y - 1]} Year`;
    },

    isAlreadySelected(course) {
      const id = Number(course?.course_id);
      if (!id) return false;

      if (this.activeTab === "cross") {
        return (
          this.selectedCrossCourses.some((c) => Number(c.course_id) === Number(id)) ||
          this.usedCourseIds.includes(id)
        );
      }

      return (
        this.currentSemesterData.expertise.some(
          (c) => Number(c.course_id) === Number(id)
        ) ||
        this.currentSemesterData.other_expertise.some(
          (c) => Number(c.course_id) === Number(id)
        )
      );
    },

    addCourse(course) {
      if (this.isAlreadySelected(course)) return;

      if (this.activeTab === "cross") {
        this.selectedCrossCourses.push({ ...course });
      } else {
        this.currentSemesterData.expertise.push({ ...course });
      }

      this.dropdownOpen = false;
      this.searchQuery = "";
    },

    addOtherCourse(course) {
      if (this.activeTab === "cross") return;
      if (this.isAlreadySelected(course)) return;

      this.currentSemesterData.other_expertise.push({ ...course });
      this.otherDropdownOpen = false;
      this.otherSearchQuery = "";
    },

    removeCourse(i) {
      if (this.activeTab === "cross") {
        this.selectedCrossCourses.splice(i, 1);
      } else {
        this.currentSemesterData.expertise.splice(i, 1);
      }
    },

    removeOtherCourse(i) {
      this.currentSemesterData.other_expertise.splice(i, 1);
    },

    async submitExpertise() {
      try {
        const existing = this.userData.expertise || [];

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

        const crossPayload = this.selectedCrossCourses.map((c) => ({
          course_id: c.course_id,
          status: "CROSS",
        }));

        const oldCrossPayload = existing
          .filter((e) => e.status === "CROSS")
          .map((e) => ({
            course_id: e.course?.course_id || e.course_id,
            status: "CROSS",
          }));

        const oldAssignPayload = existing
          .filter((e) => e.status !== "CROSS")
          .map((e) => ({
            course_id: e.course?.course_id || e.course_id,
            status: e.status || "PRIMARY",
          }));

        const finalPayload =
          this.activeTab === "cross"
            ? [...oldAssignPayload, ...crossPayload]
            : [...assignPayload, ...oldCrossPayload];

        await axios.patch(
          `${process.env.VUE_APP_API_BASE_URL}/auth/update/${this.userData.id}`,
          {
            expertise: finalPayload,
          }
        );

        toast.success(
          this.activeTab === "cross"
            ? "Cross expertise updated successfully!"
            : "Expertise updated successfully!"
        );

        this.$emit("updated");

        if (this.activeTab === "assign") {
          this.originalAssignSnapshot = this.getAssignSnapshot();
        }

        if (this.activeTab === "cross") {
          this.originalCrossSnapshot = this.getCrossSnapshot();
        }
      } catch (err) {
        console.error(err);
        toast.error("Failed to save.");
      }
    },

    loadExistingExpertise() {
      this.form.semesters = {
        1: { expertise: [], other_expertise: [] },
        2: { expertise: [], other_expertise: [] },
        3: { expertise: [], other_expertise: [] },
      };

      this.selectedCrossCourses = [];

      const allMappedCourses = [
        ...this.normalizedCurriculumCourses,
        ...this.normalizedCourses,
      ];

      const mapCourse = (id) =>
        allMappedCourses.find((c) => Number(c.course_id) === Number(id)) || null;

      const normalizeFallbackCourse = (data) => ({
        course_id: data?.course?.course_id || data?.course_id,
        course_code: data?.course_code || data?.course?.course_code || "",
        course_title: data?.course_title || data?.course?.course_title || "",
        course_semester: Number(
          data?.course_semester || data?.course?.course_semester || 1
        ),
        course_level: Number(data?.course_level || data?.course?.course_level || 1),
        program_id: data?.program_id || data?.course?.program_id || null,
        program_code: data?.program_code || data?.course?.program?.program_code || "",
      });

      (this.userData.expertise || []).forEach((ex) => {
        const rawId = ex?.course?.course_id || ex?.course_id;
        const course = mapCourse(rawId) || normalizeFallbackCourse(ex);

        const status = ex.status || "PRIMARY";
        const sem = Number(course.course_semester || 1);

        if (!this.form.semesters[sem]) {
          this.form.semesters[sem] = {
            expertise: [],
            other_expertise: [],
          };
        }

        if (status === "PRIMARY") {
          if (
            !this.form.semesters[sem].expertise.some(
              (c) => Number(c.course_id) === Number(course.course_id)
            )
          ) {
            this.form.semesters[sem].expertise.push(course);
          }
        }

        if (status === "OTHER") {
          if (
            !this.form.semesters[sem].other_expertise.some(
              (c) => Number(c.course_id) === Number(course.course_id)
            )
          ) {
            this.form.semesters[sem].other_expertise.push(course);
          }
        }

        if (status === "CROSS") {
          if (
            !this.selectedCrossCourses.some(
              (c) => Number(c.course_id) === Number(course.course_id)
            )
          ) {
            this.selectedCrossCourses.push(course);
          }
        }
      });
    },
  },

  async mounted() {
    await this.fetchCourses();
    await this.fetchPrograms();
    await this.fetchCurriculumCourses();

    this.loadExistingExpertise();
    this.originalAssignSnapshot = this.getAssignSnapshot();
    this.originalCrossSnapshot = this.getCrossSnapshot();
  },
};
</script>
