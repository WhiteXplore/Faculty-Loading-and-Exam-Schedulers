<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form @submit.prevent="submitData" class="modal-container" ref="usersForm">
        <div class="modal-header">
          <div class="flex gap-1 items-center">
            <icon :name="'add-students'" />
            <h1 class="font-bold tracking-wide text-lg">
              {{ isEditMode ? "Edit User" : "Add User" }}
            </h1>
          </div>

          <icon :name="'circle-close3'" @click="$emit('close')" class="cursor-pointer" />
        </div>

        <div class="p-5 w-[32vw] space-y-6">
          <!-- STEP 1 -->
          <div v-if="currentStep === 1" class="grid grid-cols-2 items-start gap-3">
            <div class="w-full space-y-2 text-left flex flex-col">
              <label class="input-label">First Name:</label>
              <input
                v-model="form.first_name"
                type="text"
                required
                class="input-text"
                placeholder="Enter first name"
              />
            </div>

            <div class="w-full space-y-2 text-left flex flex-col">
              <label class="input-label">Last Name:</label>
              <input
                v-model="form.last_name"
                type="text"
                required
                class="input-text"
                placeholder="Enter last name"
              />
            </div>

            <div class="w-full space-y-2 text-left flex flex-col">
              <label class="input-label">Role:</label>
              <select v-model="form.role" required class="input-text">
                <option disabled value="">Select role</option>
                <option value="Admin">Admin</option>
                <option value="Program Chairperson">Program Chairperson</option>
                <option value="Faculty">Faculty</option>
              </select>
            </div>

            <template v-if="!isAdminRole">
              <div class="w-full space-y-2 text-left flex flex-col">
                <label class="input-label">Designation:</label>
                <input
                  v-model="form.designation"
                  type="text"
                  class="input-text"
                  placeholder="Example: Instructor I"
                />
              </div>

              <div class="w-full space-y-2 text-left flex flex-col">
                <label class="input-label">Unit Load:</label>
                <input
                  v-model.number="form.unit_load"
                  type="number"
                  min="0"
                  class="input-text"
                  placeholder="Enter unit load"
                />
              </div>

              <div class="w-full space-y-2 text-left flex flex-col">
                <label class="input-label">Employment Type:</label>
                <select v-model="form.employment_type" class="input-text">
                  <option value="">Select employment type</option>
                  <option value="Full Time">Full Time</option>
                  <option value="Part Time">Part Time</option>
                </select>
              </div>

              <div class="flex flex-col space-y-2 w-full relative">
                <label class="input-label">Institute:</label>
                <input
                  v-model="searchInstituteQuery"
                  type="text"
                  placeholder="Search institute..."
                  class="input-text"
                  @focus="showInstituteDropdown = true"
                />

                <div
                  v-if="showInstituteDropdown"
                  class="absolute top-[75px] left-0 w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-50 shadow-lg"
                >
                  <div
                    v-for="institute in filteredInstitutes"
                    :key="institute.institute_id"
                    class="px-3 py-3 hover:bg-gray-100 cursor-pointer"
                    @mousedown.prevent="selectInstitute(institute)"
                  >
                    {{ institute.institute_name }}
                  </div>

                  <div
                    v-if="!filteredInstitutes.length"
                    class="px-3 py-3 text-sm text-gray-400"
                  >
                    No institute found
                  </div>
                </div>
              </div>

              <div class="flex flex-col space-y-2 w-full relative">
                <label class="input-label">Program:</label>
                <input
                  v-model="searchProgramQuery"
                  type="text"
                  placeholder="Search program..."
                  class="input-text"
                  @focus="showProgramDropdown = true"
                />

                <div
                  v-if="showProgramDropdown"
                  class="absolute top-[75px] left-0 w-full bg-white border border-gray-300 rounded-md max-h-40 overflow-y-auto z-50 shadow-lg"
                >
                  <div
                    v-for="program in filteredPrograms"
                    :key="program.program_id"
                    class="px-3 py-3 hover:bg-gray-100 cursor-pointer"
                    @mousedown.prevent="selectProgram(program)"
                  >
                    {{ program.program_name }}
                  </div>

                  <div
                    v-if="!filteredPrograms.length"
                    class="px-3 py-3 text-sm text-gray-400"
                  >
                    No program found
                  </div>
                </div>
              </div>
            </template>

            <div class="col-span-2 flex justify-end pt-2">
              <button class="btn-save" type="button" @click="goToStep2">Next</button>
            </div>
          </div>

          <!-- STEP 2 -->
          <div v-if="currentStep === 2" class="space-y-3">
            <div class="w-full space-y-2 text-left flex flex-col">
              <label class="input-label">Email:</label>
              <input
                v-model="form.email"
                type="email"
                required
                class="input-text"
                placeholder="Enter email"
              />
            </div>

            <div v-if="!isEditMode" class="w-full space-y-2 text-left flex flex-col">
              <label class="input-label">Password:</label>
              <input
                v-model="form.password"
                type="password"
                required
                class="input-text"
                placeholder="Enter password"
              />
            </div>

            <div class="tracking-wide flex justify-between gap-2 pt-4">
              <button class="btn-cancel" type="button" @click="currentStep = 1">
                Back
              </button>

              <button class="btn-save" type="submit">
                {{ isEditMode ? "Save Changes" : "Submit" }}
              </button>
            </div>
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
  name: "UsersModal",
  components: { icon },

  props: {
    userData: {
      type: Object,
      default: null,
    },
  },

  data() {
    return {
      currentStep: 1,

      form: {
        id: null,
        email: "",
        password: "",
        first_name: "",
        last_name: "",
        role: "",
        employment_type: "Full Time",
        designation: "",
        preffered_time: "",
        unit_load: 0,
        institute_id: null,
        program_id: null,
      },

      searchProgramQuery: "",
      showProgramDropdown: false,

      searchInstituteQuery: "",
      showInstituteDropdown: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["programs", "institutes"]),

    isEditMode() {
      return !!this.userData;
    },

    isAdminRole() {
      return this.form.role === "Admin";
    },

    filteredPrograms() {
      const query = this.searchProgramQuery?.toLowerCase() || "";

      return this.programs
        .filter((program) => {
          const matchesSearch =
            program.program_name?.toLowerCase().includes(query) ||
            program.program_code?.toLowerCase().includes(query);

          const matchesInstitute = this.form.institute_id
            ? Number(program.institute_id) === Number(this.form.institute_id)
            : true;

          return matchesSearch && matchesInstitute;
        })
        .sort((a, b) => a.program_name.localeCompare(b.program_name));
    },

    filteredInstitutes() {
      const query = this.searchInstituteQuery?.toLowerCase() || "";

      return [...this.institutes]
        .filter(
          (institute) =>
            institute.institute_name?.toLowerCase().includes(query) ||
            institute.institute_code?.toLowerCase().includes(query)
        )
        .sort((a, b) => a.institute_name.localeCompare(b.institute_name));
    },
  },

  watch: {
    userData: {
      immediate: true,
      deep: true,
      handler() {
        if (this.userData) {
          this.fillEditForm();
        }
      },
    },

    "form.role"(newRole, oldRole) {
      // Do not clear edit data while loading existing user
      if (this.isEditMode && !oldRole) return;

      if (newRole === "Admin") {
        this.form.employment_type = "";
        this.form.designation = "";
        this.form.unit_load = 0;
        this.form.institute_id = null;
        this.form.program_id = null;
        this.searchInstituteQuery = "";
        this.searchProgramQuery = "";
      } else if (!this.form.employment_type) {
        this.form.employment_type = "Full Time";
      }
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, ["fetchPrograms", "fetchInstitutes"]),

    selectProgram(program) {
      this.form.program_id = program.program_id;
      this.searchProgramQuery = program.program_name;
      this.showProgramDropdown = false;
    },

    selectInstitute(institute) {
      this.form.institute_id = institute.institute_id;
      this.searchInstituteQuery = institute.institute_name;

      this.form.program_id = null;
      this.searchProgramQuery = "";

      this.showInstituteDropdown = false;
    },

    goToStep2() {
      const { first_name, last_name, role, institute_id, program_id } = this.form;

      if (!first_name || !last_name || !role) {
        toast.error("Please complete first name, last name, and role.");
        return;
      }

      if (role !== "Admin" && (!institute_id || !program_id)) {
        toast.error("Please select institute and program.");
        return;
      }

      this.currentStep = 2;
    },

    buildPayload() {
      const payload = {
        first_name: this.form.first_name?.trim(),
        last_name: this.form.last_name?.trim(),
        email: this.form.email?.trim().toLowerCase(),
        role: this.form.role,
      };

      if (!this.isAdminRole) {
        payload.employment_type = this.form.employment_type || "Full Time";
        payload.designation = this.form.designation?.trim() || "";

        payload.unit_load = Number(this.form.unit_load || 0);
        payload.institute_id = Number(this.form.institute_id);
        payload.program_id = Number(this.form.program_id);
      }

      if (!this.isEditMode) {
        payload.password = this.form.password;
      }

      return payload;
    },

    async submitData() {
      const form = this.$refs.usersForm;

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      if (!this.form.first_name || !this.form.last_name || !this.form.role) {
        toast.error("Please complete required fields.");
        return;
      }

      if (!this.form.email) {
        toast.error("Email is required.");
        return;
      }

      if (!this.isEditMode && !this.form.password) {
        toast.error("Password is required.");
        return;
      }

      if (!this.isAdminRole && (!this.form.institute_id || !this.form.program_id)) {
        toast.error("Institute and Program are required.");
        return;
      }

      try {
        const payload = this.buildPayload();

        console.log("USER PAYLOAD:", payload);
        console.log("USER ID:", this.form.id);

        if (this.isEditMode) {
          if (!this.form.id) {
            toast.error("Invalid user ID.");
            return;
          }

          await axios.patch(
            process.env.VUE_APP_API_BASE_URL + `/users/${this.form.id}`,
            payload,
            { withCredentials: true }
          );

          toast.success("User updated successfully!");
        } else {
          await axios.post(process.env.VUE_APP_API_BASE_URL + "/auth/register", payload, {
            withCredentials: true,
          });

          toast.success("User registered successfully!");

          const audio = new Audio(require("@/assets/add.mp3"));
          audio.play();
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error("Save user failed:", error);
        toast.error(error?.response?.data?.message || "Failed to save user");
      }
    },

    fillEditForm() {
      if (!this.userData) return;

      this.form = {
        id: this.userData.id,
        email: this.userData.email || "",
        password: "",
        first_name: this.userData.first_name || "",
        last_name: this.userData.last_name || "",
        role: this.userData.role || "",
        employment_type: this.userData.employment_type || "Full Time",
        designation: this.userData.designation || "",
        preffered_time: this.userData.preffered_time || "",
        unit_load: Number(this.userData.unit_load || 0),

        institute_id:
          this.userData.institute_id || this.userData.institute?.institute_id || null,

        program_id: this.userData.program_id || this.userData.program?.program_id || null,
      };

      if (this.form.role === "Admin") {
        this.form.employment_type = "";
        this.form.designation = "";
        this.form.unit_load = 0;
        this.form.institute_id = null;
        this.form.program_id = null;
        this.searchInstituteQuery = "";
        this.searchProgramQuery = "";
        return;
      }

      this.searchInstituteQuery =
        this.userData.institute?.institute_name || this.userData.institute_name || "";

      this.searchProgramQuery =
        this.userData.program?.program_name || this.userData.program_name || "";
    },
  },

  async mounted() {
    await this.fetchInstitutes();
    await this.fetchPrograms();

    if (this.isEditMode) {
      this.fillEditForm();
    }
  },
};
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    transform: translateY(40px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slideUp {
  animation: fadeInUp 0.3s ease-out;
}
</style>
