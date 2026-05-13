<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form ref="curriculumnForm" @submit.prevent="submitData" class="modal-container">
        <!-- Header -->
        <div class="modal-header">
          <div class="flex gap-1 items-center">
            <icon name="add-students" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit Curriculum" : "Add Curriculum" }}
            </h1>
          </div>
          <icon name="circle-close3" class="cursor-pointer" @click="$emit('close')" />
        </div>

        <!-- Body -->
        <div class="w-[25vw] modal-body">
          <!-- Curriculum Name -->
          <!-- <div class="flex flex-col space-y-2">
            <label class="input-label">Curriculum Name:</label>
            <input
              :value="formattedCurriculumName"
              type="text"
              disabled
              class="input-text"
            />
          </div> -->
          <!-- Program -->
          <div class="dropdown-container">
            <label class="dropdown-label">Program:</label>

            <div class="dropdown-wrapper">
              <input
                v-model="searchProgramQuery"
                type="text"
                placeholder="Search program..."
                class="dropdown-input"
                @focus="showProgramDropdown = true"
                :disabled="isEdit"
                required
              />

              <div
                v-if="showProgramDropdown && !isEdit"
                class="dropdown-menu"
                @mouseleave="showProgramDropdown = false"
              >
                <!-- WITH RESULTS -->
                <div v-if="filteredPrograms.length">
                  <div
                    v-for="program in filteredPrograms"
                    :key="program.program_id"
                    class="dropdown-item"
                    @mousedown.prevent="selectProgram(program)"
                  >
                    {{ program.program_name }}
                  </div>
                </div>

                <!-- EMPTY -->
                <div v-else>
                  <div class="dropdown-empty">No program found</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Effective Year -->

          <div class="flex flex-col space-y-2">
            <label class="input-label">Effective Year:</label>

            <div class="flex gap-3">
              <!-- FROM -->
              <div class="flex-1">
                <input
                  v-model="form.curriculum_start_year"
                  type="number"
                  required
                  class="input-text"
                  placeholder="e.g. 2025"
                />
              </div>

              <!-- TO -->
              <div class="flex-1">
                <input
                  v-model="form.curriculum_end_year"
                  type="number"
                  required
                  class="input-text"
                  placeholder="e.g. 2026"
                />
              </div>
            </div>
          </div>

          <!-- Divider -->
          <div class="h-[1px] bg-gray-200 my-4"></div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2">
            <button type="button" class="btn-cancel" @click="$emit('close')">
              Cancel
            </button>
            <button type="submit" class="btn-save">
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
import axios from "axios";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";

export default {
  name: "AddEditCurriculumPage",
  components: { icon },

  props: {
    curriculumData: {
      type: Object,
      default: null,
    },
  },

  data() {
    return {
      form: {
        institute_id: "",
        program_id: "",
        curriculum_start_year: "",
        curriculum_end_year: "",
      },
      searchProgramQuery: "",
      showProgramDropdown: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["programs"]),

    isEdit() {
      return !!this.curriculumData;
    },

    filteredPrograms() {
      if (!this.searchProgramQuery) return this.programs;
      return this.programs.filter((p) =>
        p.program_name.toLowerCase().includes(this.searchProgramQuery.toLowerCase())
      );
    },

    formattedCurriculumName() {
      if (!this.form.program_id || !this.form.curriculum_start_year) return "";
      const program = this.programs.find((p) => p.program_id === this.form.program_id);
      return program
        ? `${this.form.curriculum_start_year} - ${program.program_name}`
        : "";
    },
  },

  watch: {
    curriculumData: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.form.program_id = newVal.program_id;
          this.form.institute_id = newVal.institute_id;
          this.form.curriculum_start_year = newVal.curriculum_start_year;
          this.form.curriculum_end_year = newVal.curriculum_end_year;

          const program = this.programs.find((p) => p.program_id === newVal.program_id);

          if (program) {
            this.searchProgramQuery = program.program_name;
          }
        }
      },
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchPrograms"]),

    selectProgram(program) {
      this.form.institute_id = program.institute_id;
      this.form.program_id = program.program_id;
      this.searchProgramQuery = program.program_name;
      this.showProgramDropdown = false;
    },

    async submitData() {
      const formEl = this.$refs.curriculumnForm;

      if (!formEl.checkValidity()) {
        formEl.reportValidity();
        return;
      }

      try {
        // ✅ Duplicate validation only when adding
        if (!this.isEdit) {
          const res = await axios.get(
            `${process.env.VUE_APP_API_BASE_URL}/curriculums/get-curriculums`
          );

          const curriculums = Array.isArray(res.data) ? res.data : [];

          const duplicate = curriculums.find((item) => {
            return (
              Number(item.program_id) === Number(this.form.program_id) &&
              Number(item.curriculum_start_year) ===
                Number(this.form.curriculum_start_year) &&
              Number(item.curriculum_end_year) === Number(this.form.curriculum_end_year)
            );
          });

          if (duplicate) {
            toast.warning("This curriculum already exists.");
            return;
          }
        }

        if (this.isEdit) {
          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/curriculums/update-curriculum/${this.curriculumData.curriculum_id}`,
            this.form
          );

          toast.success("Curriculum updated successfully!");
        } else {
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/curriculums/add-curriculums`,
            this.form
          );

          toast.success("Curriculum added successfully!");
        }

        new Audio(require("@/assets/add.mp3")).play();
        this.$emit("refresh");
        this.$emit("close");
      } catch (err) {
        console.error(err);
        toast.error("Failed to save curriculum");
      }
    },
  },

  mounted() {
    this.fetchPrograms();
  },
};
</script>
