<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form @submit.prevent="submitData" class="modal-container" ref="coursesForm">
        <!-- Header -->
        <div class="modal-header">
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit " : "Add " }} Course
            </h1>
          </div>
          <icon :name="'circle-close3'" @click="$emit('close')" class="cursor-pointer" />
        </div>

        <!-- Body -->
        <div class="w-[35vw] modal-body">
          <!-- Curriculum -->
          <div class="dropdown-container">
            <label class="dropdown-label">Curriculum :</label>

            <div class="dropdown-wrapper">
              <input
                v-model="searchCurriculumQuery"
                type="text"
                placeholder="Search curriculum..."
                class="dropdown-input"
                @focus="showCurriculumDropdown = true"
                :disabled="isEdit"
              />
              <div v-if="showCurriculumDropdown" class="dropdown-menu">
                <div v-if="filteredCurriculum.length">
                  <div
                    v-for="curriculum in filteredCurriculum"
                    :key="curriculum.curriculum_id"
                    class="dropdown-item"
                    @mousedown="selectcurriculum(curriculum)"
                  >
                    {{ curriculum.curriculum_end_year }} -
                    {{ curriculum.program.program_name }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Course Code -->
          <div class="w-full space-y-2">
            <label for="course_code" class="input-label">Course Code:</label>
            <input
              v-model="form.course_code"
              type="text"
              id="course_code"
              required
              class="input-text"
              placeholder="Enter course code"
            />
          </div>

          <!-- Description -->
          <div class="w-full space-y-2">
            <label for="course_title" class="input-label">Course Description:</label>
            <textarea
              v-model="form.course_title"
              id="course_title"
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
              <select v-model="form.course_semester" required class="input-text">
                <option disabled value="">Select Semester</option>
                <option value="1">First</option>
                <option value="2">Second</option>
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

          <div class="flex flex-col space-y-2 relative">
            <label class="input-label">Requisites :</label>

            <!-- Show Add button if input is hidden -->
            <button
              v-if="!showRequisiteInput"
              type="button"
              class="bg-defaultGreen text-white px-3 py-3 tracking-wider rounded-md text-sm hover:bg-green-700"
              @click="showRequisiteInput = true"
            >
              Add Requisite
            </button>

            <!-- Show input when button clicked -->
            <div v-if="showRequisiteInput" class="flex flex-col gap-2">
              <div class="dropdown-wrapper">
                <div class="flex gap-2">
                  <input
                    :value="form.course_requisite.join(', ')"
                    @input="searchRequisiteQuery = $event.target.value"
                    @focus="showRequisiteDropdown = true"
                    type="text"
                    placeholder="Search course prerequisite..."
                    class="input-text"
                  />
                  <!-- Cancel button -->
                  <button
                    type="button"
                    @click="cancelRequisites"
                    class="text-red-600 px-2 py-1 border border-red-600 rounded-md hover:bg-red-600 hover:text-white"
                  >
                    Cancel
                  </button>
                </div>

                <!-- Dropdown -->
                <div v-if="showRequisiteDropdown">
                  <div v-if="filteredCourse.length" class="dropdown-menu">
                    <div
                      v-for="course in filteredCourse"
                      :key="course.course_id"
                      class="dropdown-item"
                      @mousedown="selectcourse(course)"
                    >
                      {{ course.course_code }} - {{ course.course_title }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Display selected requisites -->
            <div class="flex flex-wrap gap-2 mt-2">
              <span
                v-for="code in form.course_requisite"
                :key="code"
                class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs cursor-pointer"
                @click="removeRequisite(code)"
              >
                {{ code }} ✕
              </span>
            </div>
          </div>
          <!-- Divider -->
          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>
          <!-- Buttons -->
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
    courseData: { type: Object, default: null },
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
      showRequisiteInput: false,
      searchCurriculumQuery: "",
      showCurriculumDropdown: false,
      searchRequisiteQuery: "",
      showRequisiteDropdown: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["curriculums", "courses"]),
    isEdit() {
      return !!this.courseData;
    },

    filteredCurriculum() {
      if (!this.searchCurriculumQuery) return this.curriculums;

      const q = this.searchCurriculumQuery.toLowerCase();
      return this.curriculums.filter(
        (c) =>
          c.curriculum_end_year?.toLowerCase().includes(q) ||
          c.program.program_name?.toLowerCase().includes(q)
      );
    },

    filteredCourse() {
      const q = this.searchRequisiteQuery.toLowerCase();
      return this.courses.filter(
        (course) =>
          (course.course_code?.toLowerCase().includes(q) ||
            course.course_title?.toLowerCase().includes(q)) &&
          this.form.curriculum_id === course.curriculum_id &&
          !this.form.course_requisite.includes(course.course_code)
      );
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchCurriculums", "fetchCourses"]),

    selectcurriculum(curr) {
      this.form.curriculum_id = curr.curriculum_id;
      this.searchCurriculumQuery = `${curr.curriculum_end_year} - ${curr.program.program_name}`;
      this.showCurriculumDropdown = false;
    },

    selectcourse(course) {
      if (!this.form.course_requisite.includes(course.course_code)) {
        this.form.course_requisite.push(course.course_code);
      }
      this.showRequisiteDropdown = false;
    },

    removeRequisite(code) {
      this.form.course_requisite = this.form.course_requisite.filter((c) => c !== code);
    },

    cancelRequisites() {
      this.showRequisiteInput = false;
      this.form.course_requisite = [];
      this.searchRequisiteQuery = "";
    },

    async submitData() {
      try {
        const payload = {
          ...this.form,
          course_requisite: this.form.course_requisite.join(","),
        };

        if (this.isEdit) {
          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/courses/update-course/${this.courseData.course_id}`,
            payload
          );
          toast.success("Course updated successfully!");
        } else {
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/courses/add-courses`,
            payload
          );
          toast.success("Course added successfully!");
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (err) {
        console.error(err);
        toast.error(this.isEdit ? "Failed to update course." : "Failed to add course.");
      }
    },
  },

  mounted() {
    this.fetchCurriculums();
    this.fetchCourses();

    if (this.isEdit) {
      this.form = {
        curriculum_id: this.courseData.curriculum_id,
        course_code: this.courseData.course_code,
        course_title: this.courseData.course_title,
        course_semester: this.courseData.course_semester,
        course_lab: this.courseData.course_lab,
        course_lec: this.courseData.course_lec,
        course_level: this.courseData.course_level,
        course_requisite: this.courseData.course_requisite
          ? this.courseData.course_requisite.split(",")
          : [],
      };

      // ✅ FINAL FIX FOR EDIT MODE
      if (this.courseData.curriculum) {
        this.searchCurriculumQuery =
          `${this.courseData.curriculum.curriculum_end_year} - ` +
          `${this.courseData.curriculum.program.program_name}`;
      }
    }
  },
};
</script>
