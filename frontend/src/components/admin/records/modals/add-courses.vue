<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form
        @submit.prevent="submitData"
        class="modal-container"
        ref="coursesForm"
      >
        <!-- Header -->
        <div class="modal-header">
          <div class="flex items-center gap-3">
            <!-- Icon -->
            <div class="glass-container">
              <icon name="circle-add2" class="text-white" />
            </div>

            <!-- Title -->
            <div>
              <h2 class="text-lg font-semibold text-white">
                {{ isEdit ? "Edit Course" : "Add Course" }}
              </h2>

              <p class="text-xs text-green-100">
                View, add, and update course details
              </p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <div class="w-[35vw] modal-body">
          <!-- Curriculum -->
          <div class="dropdown-container">
            <label class="dropdown-label">Curriculum :</label>

            <div class="dropdown-wrapper">
              <input
                :value="curriculumDisplayText"
                type="text"
                placeholder="Search curriculum..."
                class="dropdown-input"
                :class="
                  isEdit ? 'bg-gray-100 cursor-not-allowed text-gray-500' : ''
                "
                :disabled="isEdit"
                @input="handleCurriculumInput"
                @focus="!isEdit && (showCurriculumDropdown = true)"
              />

              <div
                v-if="showCurriculumDropdown"
                class="dropdown-menu"
                @mouseleave="showCurriculumDropdown = false"
              >
                <div v-if="filteredCurriculum.length">
                  <div
                    v-for="curriculum in filteredCurriculum"
                    :key="curriculum.curriculum_id"
                    class="dropdown-item"
                    @mousedown.prevent="selectCurriculum(curriculum)"
                  >
                    {{ curriculum.curriculum_start_year }} -
                    {{ curriculum.curriculum_end_year }}
                    -
                    {{ curriculum.program?.program_name || "No Program" }}
                  </div>
                </div>

                <div v-else class="dropdown-item text-gray-400">
                  No curriculum found
                </div>
              </div>
            </div>
          </div>

          <!-- Course Code -->
          <div class="w-full space-y-2">
            <label class="input-label">Course Code:</label>
            <input
              v-model="form.course_code"
              type="text"
              required
              class="input-text"
              placeholder="Enter course code"
            />
          </div>

          <!-- Course Title -->
          <div class="w-full space-y-2">
            <label class="input-label">Course Description:</label>
            <textarea
              v-model="form.course_title"
              required
              class="input-text"
              placeholder="Enter course description"
            />
          </div>

          <!-- Year + Semester -->
          <div class="w-full flex gap-3">
            <div class="w-full space-y-2">
              <label class="input-label">Year Level:</label>
              <select v-model="form.course_level" required class="input-text">
                <option disabled value="">Select Level</option>
                <option value="1">First</option>
                <option value="2">Second</option>
                <option value="3">Third</option>
                <option value="4">Fourth</option>
              </select>
            </div>

            <div class="w-full space-y-2">
              <label class="input-label">Semester:</label>
              <select
                v-model="form.course_semester"
                required
                class="input-text"
              >
                <option disabled value="">Select Semester</option>
                <option value="1">First</option>
                <option value="2">Second</option>
                <option value="3">Summer</option>
              </select>
            </div>
          </div>

          <!-- Lec/Lab -->
          <div class="w-full flex gap-3">
            <div class="w-full space-y-2">
              <label class="input-label">Lecture (Hours):</label>
              <input
                v-model="form.course_lec"
                type="number"
                required
                class="input-text"
              />
            </div>

            <div class="w-full space-y-2">
              <label class="input-label">Laboratory (Hours):</label>
              <input
                v-model="form.course_lab"
                type="number"
                required
                class="input-text"
              />
            </div>
          </div>

          <!-- Requisites -->
          <div class="flex flex-col space-y-2 relative">
            <label class="input-label">Requisites :</label>

            <button
              v-if="!showRequisiteInput"
              type="button"
              class="bg-defaultGreen text-white px-3 py-3 tracking-wider rounded-md text-sm hover:bg-green-700"
              @click="openRequisiteInput"
            >
              {{
                form.course_requisite.length
                  ? "Update Requisite"
                  : "Add Requisite"
              }}
            </button>

            <div v-if="showRequisiteInput" class="flex flex-col gap-2">
              <div class="dropdown-wrapper">
                <div class="flex gap-2">
                  <input
                    v-model="searchRequisiteQuery"
                    @focus="showRequisiteDropdown = true"
                    type="text"
                    placeholder="Search course prerequisite..."
                    class="input-text"
                  />

                  <button
                    type="button"
                    @click="cancelRequisites"
                    class="text-red-600 px-2 py-1 border border-red-600 rounded-md hover:bg-red-600 hover:text-white"
                  >
                    Cancel
                  </button>
                </div>

                <div v-if="showRequisiteDropdown">
                  <div v-if="filteredCourse.length" class="dropdown-menu">
                    <div
                      v-for="course in filteredCourse"
                      :key="course.course_id"
                      class="dropdown-item"
                      @mousedown.prevent="selectCourse(course)"
                    >
                      {{ course.course_code }} - {{ course.course_title }}
                    </div>
                  </div>

                  <div v-else class="dropdown-menu">
                    <div class="dropdown-item text-gray-400">
                      No requisite found
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Selected Requisites -->
            <div
              v-if="form.course_requisite.length"
              class="flex flex-wrap gap-2 mt-2"
            >
              <div
                v-for="code in form.course_requisite"
                :key="code"
                class="flex items-center gap-2 bg-defaultGreen text-white px-3 py-1 rounded-md text-[13px] font-normal"
              >
                <span>{{ code }}</span>

                <button
                  type="button"
                  @click="removeRequisite(code)"
                  class="text-white hover:text-red-600"
                >
                  <icon name="delete" />
                </button>
              </div>
            </div>
          </div>

          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="$emit('close')">
              Cancel
            </button>

            <button class="btn-save" type="submit">
              {{ isEdit ? "Save Changes" : "Submit" }}
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import axios from "axios";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "CourseFormModal",
  components: { icon },

  props: {
    courseData: {
      type: Object,
      default: null,
    },
  },

  data() {
    return {
      form: {
        curriculum_id: "",
        course_code: "",
        course_title: "",
        course_semester: "",
        course_lab: "",
        course_lec: "",
        course_level: "",
        course_requisite: [],
      },
      user: null,
      selectedCurriculumText: "",
      searchCurriculumQuery: "",
      showCurriculumDropdown: false,

      showRequisiteInput: false,
      searchRequisiteQuery: "",
      showRequisiteDropdown: false,

      editLoaded: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, [
      "curriculums",
      "courses",
      "curriculum_courses",
    ]),
    curriculumCourseList() {
      if (Array.isArray(this.curriculum_courses))
        return this.curriculum_courses;
      if (Array.isArray(this.curriculum_courses?.data))
        return this.curriculum_courses.data;
      return [];
    },
    isEdit() {
      return !!this.courseData;
    },

    curriculumList() {
      if (Array.isArray(this.curriculums)) return this.curriculums;
      if (Array.isArray(this.curriculums?.data)) return this.curriculums.data;
      return [];
    },

    curriculumDisplayText() {
      if (this.searchCurriculumQuery) return this.searchCurriculumQuery;
      if (this.selectedCurriculumText) return this.selectedCurriculumText;

      const curriculum = this.findSelectedCurriculum();
      return curriculum ? this.formatCurriculum(curriculum) : "";
    },

    filteredCurriculum() {
      const q = String(this.searchCurriculumQuery || "")
        .toLowerCase()
        .trim();

      const role = String(this.user?.role || "").toLowerCase();

      let list = this.curriculumList;

      // Admin = show all
      // Program Chairperson = show only same program_id
      if (role === "program chairperson") {
        list = list.filter((c) => {
          const curriculumProgramId = Number(
            c.program_id || c.program?.program_id,
          );
          const userProgramId = Number(this.user?.program_id);

          return curriculumProgramId === userProgramId;
        });
      }

      if (!q) return list;

      return list.filter((c) => {
        const startYear = String(c.curriculum_start_year || "").toLowerCase();
        const endYear = String(c.curriculum_end_year || "").toLowerCase();
        const programName = String(c.program?.program_name || "").toLowerCase();
        const programCode = String(c.program?.program_code || "").toLowerCase();

        return (
          startYear.includes(q) ||
          endYear.includes(q) ||
          `${startYear} - ${endYear}`.includes(q) ||
          `${startYear}-${endYear}`.includes(q) ||
          programName.includes(q) ||
          programCode.includes(q)
        );
      });
    },

    filteredCourse() {
      const q = String(this.searchRequisiteQuery || "")
        .toLowerCase()
        .trim();
      const list = this.courses || [];

      return list.filter((course) => {
        const code = String(course.course_code || "").toLowerCase();
        const title = String(course.course_title || "").toLowerCase();

        const isSelected = this.form.course_requisite.includes(
          course.course_code,
        );

        const isCurrentCourse =
          this.isEdit &&
          Number(course.course_id) === Number(this.courseData?.course_id);

        const matchSearch = !q || code.includes(q) || title.includes(q);

        return !isSelected && !isCurrentCourse && matchSearch;
      });
    },
  },

  watch: {
    courseData: {
      immediate: true,
      deep: true,
      handler() {
        this.loadEditData();
      },
    },
    curriculum_courses: {
      immediate: true,
      deep: true,
      handler() {
        this.setSelectedCurriculumText();
      },
    },
    curriculums: {
      immediate: true,
      deep: true,
      handler() {
        this.setSelectedCurriculumText();
      },
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, [
      "fetchCurriculums",
      "fetchCourses",
      "fetchCurriculumCourses",
    ]),
    async fetchUser() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          },
        );

        if (response.data) {
          this.user = response.data;
          console.log("Authenticated User:", this.user);
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },
    getCurriculumId() {
      const directId =
        this.courseData?.curriculum_id ||
        this.courseData?.curriculum?.curriculum_id ||
        this.courseData?.curriculumCourse?.curriculum_id ||
        this.courseData?.curriculum_course?.curriculum_id ||
        this.courseData?.curriculumCourse?.curriculum?.curriculum_id ||
        this.courseData?.curriculum_course?.curriculum?.curriculum_id;

      if (directId) return directId;

      const match = this.curriculumCourseList.find(
        (item) => Number(item.course_id) === Number(this.courseData?.course_id),
      );

      console.log("MATCHED CURRICULUM COURSE:", match);

      return match?.curriculum_id || match?.curriculum?.curriculum_id || "";
    },

    formatCurriculum(curriculum) {
      return `${curriculum.curriculum_start_year} - ${
        curriculum.curriculum_end_year
      } - ${curriculum.program?.program_name || "No Program"}`;
    },

    findSelectedCurriculum() {
      const curriculumId = this.form.curriculum_id || this.getCurriculumId();

      return this.curriculumList.find(
        (c) => Number(c.curriculum_id) === Number(curriculumId),
      );
    },

    setSelectedCurriculumText() {
      const curriculum = this.findSelectedCurriculum();

      if (curriculum) {
        console.log("CURRICULUM START YEAR:", curriculum.curriculum_start_year);
        console.log("CURRICULUM END YEAR:", curriculum.curriculum_end_year);

        this.selectedCurriculumText = this.formatCurriculum(curriculum);
        return;
      }

      const match = this.curriculumCourseList.find(
        (item) => Number(item.course_id) === Number(this.courseData?.course_id),
      );

      if (match?.curriculum) {
        console.log(
          "CURRICULUM START YEAR:",
          match.curriculum.curriculum_start_year,
        );
        console.log(
          "CURRICULUM END YEAR:",
          match.curriculum.curriculum_end_year,
        );

        this.form.curriculum_id =
          match.curriculum_id || match.curriculum.curriculum_id;
        this.selectedCurriculumText = this.formatCurriculum(match.curriculum);
        return;
      }

      console.log("❌ STILL NO CURRICULUM FOUND");
    },

    handleCurriculumInput(event) {
      this.searchCurriculumQuery = event.target.value;
      this.selectedCurriculumText = "";
      this.showCurriculumDropdown = true;
    },

    selectCurriculum(curriculum) {
      this.form.curriculum_id = curriculum.curriculum_id;
      this.selectedCurriculumText = this.formatCurriculum(curriculum);
      this.searchCurriculumQuery = "";
      this.showCurriculumDropdown = false;
    },

    openRequisiteInput() {
      this.showRequisiteInput = true;
      this.showRequisiteDropdown = true;
    },

    selectCourse(course) {
      if (!this.form.course_requisite.includes(course.course_code)) {
        this.form.course_requisite.push(course.course_code);
      }

      this.searchRequisiteQuery = "";
      this.showRequisiteDropdown = false;
    },

    removeRequisite(code) {
      this.form.course_requisite = this.form.course_requisite.filter(
        (item) => item !== code,
      );
    },

    cancelRequisites() {
      this.showRequisiteInput = false;
      this.searchRequisiteQuery = "";
      this.showRequisiteDropdown = false;
    },

    normalizeRequisites(value) {
      if (!value) return [];

      if (Array.isArray(value)) {
        return value
          .map((item) => {
            if (typeof item === "string") return item.trim();
            return item?.course_code?.trim();
          })
          .filter(Boolean);
      }

      if (typeof value === "string") {
        return value
          .split(",")
          .map((item) => item.trim())
          .filter(Boolean);
      }

      return [];
    },

    loadEditData() {
      if (!this.isEdit) return;

      const curriculumId = this.getCurriculumId();

      this.form = {
        curriculum_id: curriculumId,
        course_code: this.courseData?.course_code || "",
        course_title: this.courseData?.course_title || "",
        course_semester: String(this.courseData?.course_semester || ""),
        course_lab: String(this.courseData?.course_lab || ""),
        course_lec: String(this.courseData?.course_lec || ""),
        course_level: String(this.courseData?.course_level || ""),
        course_requisite: this.normalizeRequisites(
          this.courseData?.course_requisite,
        ),
      };

      console.log("==================================");
      console.log("EDIT MODE COURSE DATA:");
      console.log(this.courseData);

      console.log("CURRICULUM ID:");
      console.log(curriculumId);

      console.log("ALL CURRICULUMS:");
      console.log(this.curriculumList);

      const curriculum = this.findSelectedCurriculum();

      console.log("FOUND CURRICULUM:");
      console.log(curriculum);

      if (curriculum) {
        console.log("CURRICULUM START YEAR:");
        console.log(curriculum.curriculum_start_year);

        console.log("CURRICULUM END YEAR:");
        console.log(curriculum.curriculum_end_year);

        console.log("PROGRAM:");
        console.log(curriculum.program);

        this.selectedCurriculumText = this.formatCurriculum(curriculum);
      } else {
        console.log("❌ CURRICULUM NOT FOUND");
      }

      console.log("==================================");

      if (this.form.course_requisite.length) {
        this.showRequisiteInput = true;
      }
    },

    async submitData() {
      try {
        if (!this.form.curriculum_id) {
          toast.error("Please select a curriculum from the dropdown.");
          return;
        }

        const payload = {
          curriculum_id: Number(this.form.curriculum_id),
          course_code: this.form.course_code.trim(),
          course_title: this.form.course_title.trim(),
          course_semester: Number(this.form.course_semester),
          course_lab: Number(this.form.course_lab),
          course_lec: Number(this.form.course_lec),
          course_level: Number(this.form.course_level),
          course_requisite: this.form.course_requisite.join(","),
        };

        console.log("COURSE PAYLOAD:", payload);

        if (this.isEdit) {
          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/courses/update-course/${this.courseData.course_id}`,
            payload,
          );
          toast.success("Course updated successfully!");
        } else {
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/courses/add-courses`,
            payload,
          );
          toast.success("Course added successfully!");
        }

        await this.fetchCourses();

        this.$emit("refresh");
        this.$emit("close");
      } catch (err) {
        console.error("SAVE COURSE ERROR:", err.response?.data || err);
        toast.error(err.response?.data?.message || "Failed to save course.");
      }
    },
  },

  async mounted() {
    await this.fetchUser();

    await Promise.all([
      this.fetchCurriculums(),
      this.fetchCourses(),
      this.fetchCurriculumCourses(),
    ]);

    this.loadEditData();
  },
};
</script>
