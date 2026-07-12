<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form @submit.prevent="submitData" class="modal-container">
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
                {{ isEdit ? "Edit School Year" : "Add School Year" }}
              </h2>

              <p class="text-xs text-green-100">
                View, add, and update school year details
              </p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <!-- Body -->
        <div class="w-[25vw] modal-body">
          <!-- <div class="w-full space-y-2">
            <label class="input-label">School Year Name:</label>
            <input
              :value="schoolYearName"
              type="text"
              readonly
              class="w-full border px-3 py-3 rounded-md bg-gray-100"
            />
          </div> -->

          <div class="w-full flex gap-3">
            <div class="w-full space-y-2">
              <label class="input-label">Start Year:</label>
              <input
                v-model.number="form.start_year"
                type="number"
                required
                min="2000"
                max="2100"
                class="input-text"
                placeholder="e.g., 2024"
              />
            </div>
            <div class="w-full space-y-2">
              <label class="input-label">End Year:</label>
              <input
                v-model.number="form.end_year"
                type="number"
                required
                min="2000"
                max="2100"
                class="input-text"
                placeholder="e.g., 2025"
              />
            </div>
          </div>

          <div class="w-full space-y-2">
            <label class="input-label">Semester:</label>
            <select v-model.number="form.semester" required class="input-text">
              <option value="">Select Semester</option>
              <option value="1">1st Semester</option>
              <option value="2">2nd Semester</option>
            </select>
          </div>

          <div class="w-full space-y-2">
            <label class="flex items-center gap-2">
              <input
                type="checkbox"
                v-model="form.is_active"
                class="w-4 h-4 text-defaultGreen border-gray-300 rounded focus:ring-green-500"
              />
              Set as Active School Year
            </label>
          </div>

          <div class="flex justify-end gap-2 mt-4">
            <button type="button" @click="$emit('close')" class="btn-cancel">
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
import { toast } from "vue3-toastify";
import axios from "axios";
import { eventBus } from "@/bus/event-bus";

export default {
  name: "SchoolYearFormModal",
  components: { icon },
  props: { schoolYearData: { type: Object, default: null } },
  data() {
    return {
      form: {
        school_year_name: "",
        start_year: new Date().getFullYear(),
        end_year: new Date().getFullYear() + 1,
        semester: "",
        is_active: false,
      },
    };
  },
  computed: {
    isEdit() {
      return !!this.schoolYearData;
    },
    schoolYearName() {
      if (!this.form.start_year || !this.form.end_year) return "";
      return `${this.form.start_year}-${this.form.end_year}`;
    },
  },
  mounted() {
    if (this.isEdit)
      this.form = {
        school_year_name: this.schoolYearData.school_year_name,
        start_year: this.schoolYearData.start_year,
        end_year: this.schoolYearData.end_year,
        semester: this.schoolYearData.semester,
        is_active: this.schoolYearData.is_active,
      };
  },
  methods: {
    async submitData() {
      try {
        if (this.form.end_year <= this.form.start_year) {
          toast.error("End year must be greater than start year");
          return;
        }

        const payload = {
          school_year_name: this.schoolYearName,
          start_year: Number(this.form.start_year),
          end_year: Number(this.form.end_year),
          semester: Number(this.form.semester),
          is_active: Boolean(this.form.is_active),
        };
        if (this.isEdit) {
          await axios.patch(
            process.env.VUE_APP_API_BASE_URL +
              `/school-year/update-school-year/${this.schoolYearData.school_year_id}`,
            payload,
          );
          toast.success("School Year updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/school-year/add-school-year",
            payload,
          );
          toast.success("School Year added successfully!");
        }

        // inside submitData()
        if (this.form.is_active) {
          // Only emit if this is now the active school year
          eventBus.emit({
            school_year_id: this.form.school_year_id,
            isActive: true,
          });
        } else {
          eventBus.emit({
            school_year_id: this.form.school_year_id,
            isActive: false,
          });
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (err) {
        toast.error(
          this.isEdit
            ? "Failed to update school year."
            : "Failed to add school year.",
        );
      }
    },
  },
};
</script>
