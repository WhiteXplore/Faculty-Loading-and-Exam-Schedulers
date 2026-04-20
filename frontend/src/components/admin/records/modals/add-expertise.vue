<template>
  <div
    class="fixed inset-0 bg-gray-800 bg-opacity-40 flex justify-center items-center z-50"
  >
    <div class="rounded-[16px] shadow-lg animate-slideUp">
      <form
        @submit.prevent="submitExpertise"
        class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg p-0.5"
      >
        <!-- HEADER -->
        <div
          class="w-full px-4 py-3 bg-defaultGreen text-white rounded-t-[16px] flex justify-between items-center"
        >
          <h1 class="font-bold text-lg">
            {{ mode === "cross" ? "Cross Assign Expertise" : "Assign Expertise" }}
          </h1>

          <icon :name="'circle-close3'" @click="$emit('close')" class="cursor-pointer" />
        </div>

        <div class="p-4 w-[28vw] space-y-4">
          <!-- ========================= -->
          <!-- 🔵 ASSIGN MODE ONLY -->
          <!-- ========================= -->
          <div v-if="mode === 'assign'" class="space-y-4">
            <!-- YEAR -->
            <div class="space-y-2">
              <label>Year Level:</label>
              <select
                v-model="selectedYearLevel"
                class="w-full border px-3 py-2.5 rounded-md"
              >
                <option v-for="y in [1, 2, 3, 4]" :key="y" :value="y">
                  {{ getYearLevelName(y) }}
                </option>
              </select>
            </div>

            <!-- SEM -->
            <div class="space-y-2">
              <label>Semester:</label>
              <select
                v-model="selectedSemester"
                class="w-full border px-3 py-2.5 rounded-md"
              >
                <option v-for="s in [1, 2, 3]" :key="s" :value="s">
                  {{ getSemesterName(s) }}
                </option>
              </select>
            </div>

            <!-- EXPERTISE -->
            <div class="relative space-y-2">
              <label>Expertise</label>

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
                  @click="!isAlreadySelected(course) && addCourse(course)"
                  class="px-3 py-2 flex justify-between items-center cursor-pointer"
                  :class="
                    isAlreadySelected(course)
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'hover:bg-green-100'
                  "
                >
                  <span> {{ course.course_code }} - {{ course.course_title }} </span>

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
                  :key="i"
                  class="flex justify-between px-4 py-2 bg-defaultGreen text-white rounded"
                >
                  <span>{{ item.course_code }} — {{ item.course_title }}</span>
                  <button @click="removeCourse(i)">✕</button>
                </div>
              </div>
            </div>

            <!-- OTHER EXPERTISE -->
            <div class="relative space-y-2">
              <label>Other Expertise</label>

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
                  @click="!isAlreadySelected(course) && addOtherCourse(course)"
                  class="px-3 py-2 flex justify-between items-center cursor-pointer"
                  :class="
                    isAlreadySelected(course)
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'hover:bg-green-100'
                  "
                >
                  <span>
                    <span class="px-2 py-0.5 rounded-full bg-defaultGreen text-white">
                      {{ course.curriculum?.program?.program_code }}</span
                    >

                    {{ course.course_code }} -
                    {{ course.course_title }}
                  </span>

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
                  :key="i"
                  class="flex justify-between px-4 py-2 bg-defaultGreen text-white rounded"
                >
                  <span>{{ item.course_code }} — {{ item.course_title }}</span>
                  <button @click="removeOtherCourse(i)">✕</button>
                </div>
              </div>
            </div>
          </div>

          <!-- ========================= -->
          <!-- 🟠 CROSS MODE ONLY -->
          <!-- ========================= -->

          <div v-else class="space-y-4">
            <div class="space-y-2">
              <label>Program</label>
              <select
                v-model="selectedProgramId"
                class="w-full border px-3 py-2.5 rounded-md"
              >
                <option value="">All Programs</option>
                <option v-for="p in programs" :key="p.program_id" :value="p.program_id">
                  {{ p.program_name }}
                </option>
              </select>
            </div>
            <div class="relative space-y-2">
              <label>Cross Expertise</label>

              <input
                v-model="searchQuery"
                @focus="dropdownOpen = true"
                placeholder="Search all courses..."
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
                  @click="!isAlreadySelected(course) && addCourse(course)"
                  class="px-3 py-2 flex justify-between items-center cursor-pointer"
                  :class="
                    isAlreadySelected(course)
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'hover:bg-green-100'
                  "
                >
                  <span>
                    <span class="px-2 py-0.5 rounded-full bg-defaultGreen text-white">
                      {{ course.curriculum?.program?.program_code }}</span
                    >
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

            <!-- SELECTED CROSS -->
            <div class="space-y-1">
              <div
                v-for="(item, i) in selectedCrossCourses"
                :key="i"
                class="flex justify-between px-4 py-2 bg-defaultGreen text-white rounded"
              >
                <span>{{ item.course_code }} — {{ item.course_title }}</span>
                <button @click="removeCourse(i)">✕</button>
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
      default: "assign", // assign | cross
    },
  },

  data() {
    return {
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

      // CROSS MODE DATA
      selectedCrossCourses: [],
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["courses", "programs"]),
    usedCourseIds() {
      if (!this.userData?.expertise || !Array.isArray(this.userData.expertise)) {
        return [];
      }

      return this.userData.expertise
        .map((e) => e?.course?.course_id || e?.course_id)
        .filter(Boolean); // removes undefined/null
    },
    currentSemesterData() {
      return this.form.semesters[this.selectedSemester];
    },
    filteredCourses() {
      if (!this.courses?.length) return [];

      const search = (this.searchQuery || "").toLowerCase();

      const matchSearch = (c) =>
        (c.course_code?.toLowerCase() || "").includes(search) ||
        (c.course_title?.toLowerCase() || "").includes(search);

      // =========================
      // 🟠 CROSS MODE → SHOW ALL COURSES
      // =========================
      if (this.mode === "cross") {
        return this.courses.filter((c) => {
          return (
            matchSearch(c) &&
            (!this.selectedProgramId ||
              c.curriculum?.program_id === this.selectedProgramId) && // ✅ FILTER HERE
            !this.selectedCrossCourses.some((e) => e.course_id === c.course_id)
          );
        });
      }

      // =========================
      // 🔵 ASSIGN MODE → FILTERED BY PROGRAM/INSTITUTE
      // =========================
      return this.courses.filter((c) => {
        return (
          matchSearch(c) &&
          c.course_semester === this.selectedSemester &&
          c.course_level === this.selectedYearLevel && // ✅ ADD THIS
          c.curriculum?.program?.institute_id ===
            this.userData?.institute?.institute_id &&
          c.curriculum?.program_id === this.userData?.program?.program_id &&
          !this.currentSemesterData.other_expertise.some(
            (e) => e.course_id === c.course_id
          )
        );
      });
    },
    filteredOtherCourses() {
      if (this.mode === "cross") return [];

      return this.courses.filter((c) => {
        const matchSearch =
          (c.course_code?.toLowerCase() || "").includes(
            this.otherSearchQuery.toLowerCase()
          ) ||
          (c.course_title?.toLowerCase() || "").includes(
            this.otherSearchQuery.toLowerCase()
          );

        return (
          matchSearch &&
          c.course_semester === this.selectedSemester &&
          c.course_level === this.selectedYearLevel &&
          c.curriculum?.program?.institute_id ===
            this.userData?.institute?.institute_id &&
          !this.currentSemesterData.expertise.some((e) => e.course_id === c.course_id)
        );
      });
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchCourses", "fetchPrograms"]),

    getSemesterName(s) {
      return s === 1 ? "1st" : s === 2 ? "2nd" : "Summer";
    },

    getYearLevelName(y) {
      return `${y}${["st", "nd", "rd", "th"][y - 1]} Year`;
    },

    // =========================
    // SELECT CHECK
    // =========================
    isAlreadySelected(course) {
      const id = course?.course_id;
      if (!id) return false;

      if (this.mode === "cross") {
        return (
          this.selectedCrossCourses?.some((c) => c.course_id === id) ||
          this.usedCourseIds?.includes(id)
        );
      }

      return (
        this.currentSemesterData?.expertise?.some((c) => c.course_id === id) ||
        this.currentSemesterData?.other_expertise?.some((c) => c.course_id === id)
      );
    },

    // =========================
    // ADD COURSE
    // =========================
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
      if (this.mode === "cross") {
        this.selectedCrossCourses.splice(i, 1);
      } else {
        this.currentSemesterData.expertise.splice(i, 1);
      }
    },

    removeOtherCourse(i) {
      if (this.mode !== "cross") {
        this.currentSemesterData.other_expertise.splice(i, 1);
      }
    },

    // =========================
    // 🚀 SUBMIT (FIXED)
    // =========================
    async submitExpertise() {
      try {
        // =========================
        // 🟠 CROSS MODE (FIXED: MERGE INSTEAD OF REPLACE)
        // =========================
        if (this.mode === "cross") {
          const existing = this.userData.expertise || [];

          const nonCross = existing
            .filter((e) => e.status !== "CROSS")
            .map((e) => ({
              course_id: e.course?.course_id || e.course_id,
              status: e.status,
            }));

          const cross = this.selectedCrossCourses.map((c) => ({
            course_id: c.course_id,
            status: "CROSS",
          }));

          const finalPayload = [...nonCross, ...cross];

          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/auth/update/${this.userData.id}`,
            {
              expertise: finalPayload,
            }
          );
        }

        // =========================
        // 🔵 ASSIGN MODE (UNCHANGED LOGIC)
        // =========================
        else {
          const existing = this.userData.expertise || [];

          // 🟠 KEEP EXISTING CROSS
          const cross = existing
            .filter((e) => e.status === "CROSS")
            .map((e) => ({
              course_id: e.course?.course_id || e.course_id,
              status: "CROSS",
            }));

          // 🔵 NEW PRIMARY + OTHER
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

          // ✅ MERGE EVERYTHING
          const finalPayload = [...assignPayload, ...cross];

          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/auth/update/${this.userData.id}`,
            {
              expertise: finalPayload,
            }
          );

          toast.success("Expertise updated successfully!");
        }

        this.$emit("updated");
        this.$emit("close");
      } catch (err) {
        console.error(err);
        toast.error("Failed to save.");
      }
    },

    // =========================
    // LOAD EXISTING (ONLY ASSIGN MODE)
    // =========================
    loadExistingExpertise() {
      if (!this.courses?.length || !this.userData) return;

      // reset assign mode structure
      this.form.semesters = {
        1: { expertise: [], other_expertise: [] },
        2: { expertise: [], other_expertise: [] },
        3: { expertise: [], other_expertise: [] },
      };

      this.selectedCrossCourses = []; // reset cross mode

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

      (this.userData.expertise || []).forEach((ex) => {
        const course = normalizeCourse(ex.course || ex);

        const status = ex.status || "PRIMARY";
        const sem = course.course_semester || 1;

        if (status === "PRIMARY") {
          if (
            !this.form.semesters[sem].expertise.some(
              (c) => c.course_id === course.course_id
            )
          ) {
            this.form.semesters[sem].expertise.push(course);
          }
        } else if (status === "OTHER") {
          if (
            !this.form.semesters[sem].other_expertise.some(
              (c) => c.course_id === course.course_id
            )
          ) {
            this.form.semesters[sem].other_expertise.push(course);
          }
        } else if (status === "CROSS") {
          if (!this.selectedCrossCourses.some((c) => c.course_id === course.course_id)) {
            this.selectedCrossCourses.push(course);
          }
        }
      });
    },
  },

  async mounted() {
    await this.fetchCourses();
    await this.fetchPrograms();
    this.loadExistingExpertise();
  },
};
</script>
