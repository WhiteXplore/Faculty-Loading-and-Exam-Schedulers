<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form @submit.prevent="submitData" class="modal-container" ref="programsForm">
        <div class="modal-header">
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEdit ? "Edit" : "Add" }} Institute
            </h1>
          </div>

          <icon :name="'circle-close3'" @click="$emit('close')" class="cursor-pointer" />
        </div>

        <div class="w-[25vw] modal-body">
          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="institute_code" class="input-label">Institute Code:</label>
            <input
              v-model.trim="form.institute_code"
              type="text"
              id="institute_code"
              required
              class="input-text"
              placeholder="Enter institute code"
            />
          </div>

          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="institute_name" class="input-label">Institute Name:</label>
            <input
              v-model.trim="form.institute_name"
              type="text"
              id="institute_name"
              required
              class="input-text"
              placeholder="Enter institute name"
            />
          </div>

          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="program_code" class="input-label">Program Code:</label>
            <input
              v-model.trim="form.program_code"
              type="text"
              id="program_code"
              required
              class="input-text"
              placeholder="Enter program code"
            />
          </div>

          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="program_name" class="input-label">Program Name:</label>
            <input
              v-model.trim="form.program_name"
              type="text"
              id="program_name"
              required
              class="input-text"
              placeholder="Enter program name"
            />
          </div>

          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <div class="modal-footer">
            <button type="button" class="btn-cancel" @click="$emit('close')">
              Cancel
            </button>

            <button class="btn-save" type="submit" :disabled="saving">
              {{ saving ? "Saving..." : isEdit ? "Save Changes" : "Submit" }}
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

export default {
  name: "AddInstitutePage",
  components: { icon },

  props: {
    editData: {
      type: Object,
      default: null,
    },
  },

  data() {
    return {
      fetchDataStore: null,
      saving: false,

      form: {
        institute_name: "",
        institute_code: "",
        program_code: "",
        program_name: "",
      },
    };
  },

  computed: {
    isEdit() {
      return !!this.editData;
    },

    currentInstituteId() {
      return (
        this.editData?.institute_id || this.editData?.institute?.institute_id || null
      );
    },

    currentProgramId() {
      return this.editData?.program_id || null;
    },
  },

  watch: {
    editData: {
      immediate: true,
      handler(newVal) {
        if (!newVal) return;

        this.form.institute_name = newVal.institute?.institute_name || "";
        this.form.institute_code = newVal.institute?.institute_code || "";
        this.form.program_name = newVal.program_name || "";
        this.form.program_code = newVal.program_code || "";
      },
    },
  },

  methods: {
    normalize(value) {
      return String(value || "")
        .trim()
        .toLowerCase();
    },

    async loadDuplicateReferences() {
      await Promise.all([this.fetchDataStore.fetchPrograms()]);
    },

    hasDuplicateProgram() {
      const programName = this.normalize(this.form.program_name);
      const programCode = this.normalize(this.form.program_code);

      return this.fetchDataStore.programs.some((item) => {
        const itemId = item.program_id;

        if (this.isEdit && itemId === this.currentProgramId) {
          return false;
        }

        return (
          this.normalize(item.program_name) === programName ||
          this.normalize(item.program_code) === programCode
        );
      });
    },

    async submitData() {
      const form = this.$refs.programsForm;

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      this.saving = true;

      try {
        await this.loadDuplicateReferences();

        if (this.hasDuplicateProgram()) {
          toast.error("Duplicate program name or program code already exists.");
          return;
        }

        let instituteId;

        if (this.isEdit) {
          const instituteResponse = await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/institute/update-institute/${this.currentInstituteId}`,
            {
              institute_name: this.form.institute_name,
              institute_code: this.form.institute_code,
            }
          );

          instituteId = instituteResponse.data.institute_id || this.currentInstituteId;

          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/programs/update-program/${this.currentProgramId}`,
            {
              program_name: this.form.program_name,
              program_code: this.form.program_code,
              institute_id: instituteId,
            }
          );

          toast.success("Institute and Program updated successfully!");
        } else {
          const instituteResponse = await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/institute/add-institute",
            {
              institute_name: this.form.institute_name,
              institute_code: this.form.institute_code,
            }
          );

          instituteId = instituteResponse.data.institute_id;

          await axios.post(process.env.VUE_APP_API_BASE_URL + "/programs/add-programs", {
            program_name: this.form.program_name,
            program_code: this.form.program_code,
            institute_id: instituteId,
          });

          toast.success("Institute and Program added successfully!");
        }

        const audio = new Audio(require("@/assets/add.mp3"));
        audio.play();

        await this.loadDuplicateReferences();

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error(error);
        toast.error("Failed to save institute or program.");
      } finally {
        this.saving = false;
      }
    },
  },

  async mounted() {
    this.fetchDataStore = useFetchDataStore();

    await this.loadDuplicateReferences();
  },
};
</script>
