<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form @submit.prevent="submitData" class="modal-container" ref="programsForm">
        <!-- Header -->
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
          <!-- Institute Fields -->
          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="institute_code" class="input-label">Institute Code:</label>
            <input
              v-model="form.institute_code"
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
              v-model="form.institute_name"
              type="text"
              id="institute_name"
              required
              class="input-text"
              placeholder="Enter institute name"
            />
          </div>

          <!-- Program Fields -->
          <div class="w-full space-y-2 text-left flex flex-col">
            <label for="program_code" class="input-label">Program Code:</label>
            <input
              v-model="form.program_code"
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
              v-model="form.program_name"
              type="text"
              id="program_name"
              required
              class="input-text"
              placeholder="Enter program name"
            />
          </div>

          <!-- Divider -->
          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

          <!-- Buttons -->
          <div class="modal-footer">
            <button class="btn-cancel" @click="$emit('close')">Cancel</button>
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
  },
  watch: {
    editData: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.form.institute_name = newVal.institute?.institute_name || "";
          this.form.institute_code = newVal.institute?.institute_code || "";
          this.form.program_name = newVal.program_name || "";
          this.form.program_code = newVal.program_code || "";
        }
      },
    },
  },

  methods: {
    async submitData() {
      const form = this.$refs.programsForm;
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      try {
        let instituteId;

        if (this.isEdit) {
          // Update Institute
          const instituteResponse = await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/institute/update-institute/${this.editData.institute_id}`,
            {
              institute_name: this.form.institute_name,
              institute_code: this.form.institute_code,
            }
          );
          instituteId = instituteResponse.data.institute_id;

          // Update Program
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/programs/update-program/${this.editData.program_id}`,
            {
              program_name: this.form.program_name,
              program_code: this.form.program_code,
              institute_id: instituteId,
            }
          );

          toast.success("Institute and Program updated successfully!");
        } else {
          // Add Institute
          const instituteResponse = await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/institute/add-institute",
            {
              institute_name: this.form.institute_name,
              institute_code: this.form.institute_code,
            }
          );
          instituteId = instituteResponse.data.institute_id;

          // Add Program
          await axios.post(process.env.VUE_APP_API_BASE_URL + "/programs/add-programs", {
            program_name: this.form.program_name,
            program_code: this.form.program_code,
            institute_id: instituteId,
          });

          toast.success("Institute and Program added successfully!");
        }

        const audio = new Audio(require("@/assets/add.mp3"));
        audio.play();

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error(error);
        toast.error("Failed to save institute or program.");
      }
    },
  },
  mounted() {
    if (this.isEdit && this.editData) {
      // populate form with editData
      this.form.institute_name = this.editData.institute?.institute_name || "";
      this.form.institute_code = this.editData.institute?.institute_code || "";
      this.form.program_name = this.editData.program_name || "";
      this.form.program_code = this.editData.program_code || "";
    }
  },
};
</script>
