<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form @submit.prevent="submitData" class="modal-container">
        <!-- Header -->
        <div class="modal-header">
          <div class="flex items-center gap-3">
            <div class="glass-container">
              <icon name="circle-add2" class="text-white" />
            </div>

            <div>
              <h2 class="text-lg font-semibold text-white">
                {{ isEdit ? "Edit Department" : "Add Department" }}
              </h2>

              <p class="text-xs text-green-100">
                Manage department and institute information
              </p>
            </div>
          </div>

          <icon
            name="circle-close3"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <!-- Body -->
        <div class="w-[25vw] modal-body space-y-4">
          <!-- Institute -->
          <div class="w-full space-y-2">
            <label class="input-label" for="institute_id"> Institute: </label>

            <select
              id="institute_id"
              v-model="form.institute_id"
              required
              class="input-text"
              :disabled="isSubmitting || isLoadingInstitutes"
            >
              <option :value="null" disabled>
                {{
                  isLoadingInstitutes
                    ? "Loading institutes..."
                    : "Select Institute"
                }}
              </option>

              <option
                v-for="institute in institutes"
                :key="institute.institute_id"
                :value="Number(institute.institute_id)"
              >
                {{ institute.institute_name }}
              </option>
            </select>

            <p v-if="instituteError" class="text-xs text-red-500">
              {{ instituteError }}
            </p>
          </div>

          <!-- Department Name -->
          <div class="w-full space-y-2">
            <label class="input-label" for="department_name">
              Department Name:
            </label>

            <input
              id="department_name"
              v-model.trim="form.department_name"
              type="text"
              required
              maxlength="255"
              class="input-text"
              placeholder="Enter department name"
              autocomplete="off"
              :disabled="isSubmitting"
            />
          </div>

          <!-- Actions -->
          <div class="flex justify-end gap-2 mt-4">
            <button
              type="button"
              @click="$emit('close')"
              class="btn-cancel"
              :disabled="isSubmitting"
            >
              Cancel
            </button>

            <button
              type="submit"
              class="btn-save"
              :disabled="
                isSubmitting ||
                isLoadingInstitutes ||
                !form.department_name.trim() ||
                form.institute_id === null
              "
            >
              {{
                isSubmitting ? "Saving..." : isEdit ? "Save Changes" : "Submit"
              }}
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
  name: "AddDepartmentModal",

  components: {
    icon,
  },

  props: {
    editData: {
      type: Object,
      default: null,
    },
  },

  emits: ["close", "refresh"],

  data() {
    return {
      fetchDataStore: useFetchDataStore(),

      form: {
        department_name: "",
        institute_id: null,
      },

      isSubmitting: false,
      isLoadingInstitutes: false,
      instituteError: "",
    };
  },

  computed: {
    isEdit() {
      return !!this.editData;
    },

    institutes() {
      return this.fetchDataStore.institutes || [];
    },
  },

  watch: {
    editData: {
      immediate: true,
      handler(department) {
        this.form = {
          department_name: department?.department_name || "",
          institute_id:
            department?.institute_id != null
              ? Number(department.institute_id)
              : department?.institute?.institute_id != null
              ? Number(department.institute.institute_id)
              : null,
        };
      },
    },
  },

  async mounted() {
    await this.loadInstitutes();
  },

  methods: {
    async loadInstitutes() {
      this.isLoadingInstitutes = true;
      this.instituteError = "";

      try {
        await this.fetchDataStore.fetchInstitutes();

        if (this.fetchDataStore.error) {
          throw new Error(this.fetchDataStore.error);
        }

        if (!this.institutes.length) {
          this.instituteError = "No institutes available.";
        }
      } catch (error) {
        console.error("Failed to load institutes:", error);

        this.instituteError = "Failed to load institutes.";
        toast.error("Failed to load institutes.");
      } finally {
        this.isLoadingInstitutes = false;
      }
    },

    async submitData() {
      const departmentName = this.form.department_name.trim();
      const instituteId = Number(this.form.institute_id);

      if (!departmentName) {
        toast.error("Department name is required.");
        return;
      }

      if (
        this.form.institute_id === null ||
        this.form.institute_id === "" ||
        !Number.isInteger(instituteId) ||
        instituteId <= 0
      ) {
        toast.error("Please select an institute.");
        return;
      }

      if (this.isSubmitting) return;

      this.isSubmitting = true;

      const payload = {
        department_name: departmentName,
        institute_id: instituteId,
      };

      try {
        if (this.isEdit) {
          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/departments/${this.editData.department_id}`,
            payload,
          );

          toast.success("Department updated successfully!");
        } else {
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/departments`,
            payload,
          );

          toast.success("Department added successfully!");
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error("Failed to save department:", error);

        const message = error.response?.data?.message;

        if (
          error.response?.status === 409 ||
          (Array.isArray(message) &&
            message.some(
              (item) =>
                typeof item === "string" &&
                item.toLowerCase().includes("already exists"),
            ))
        ) {
          toast.error("This department name already exists.");
        } else {
          toast.error(
            typeof message === "string"
              ? message
              : Array.isArray(message)
              ? message.join(", ")
              : this.isEdit
              ? "Failed to update department."
              : "Failed to add department.",
          );
        }
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>
