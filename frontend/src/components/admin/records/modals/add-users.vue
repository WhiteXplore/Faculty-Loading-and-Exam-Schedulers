<template>
  <div class="modal-overlay">
    <div class="modal-wrapper">
      <form
        @submit.prevent="submitData"
        class="modal-container"
        ref="usersForm"
      >
        <div class="modal-header">
          <div class="flex items-center gap-3">
            <!-- Icon -->
            <div class="glass-container">
              <icon name="circle-add2" class="text-white" />
            </div>

            <!-- Title -->
            <div>
              <h2 class="text-lg font-semibold text-white">
                {{ isEditMode ? "Edit User" : "Add User" }}
              </h2>

              <p class="text-xs text-green-100">
                View, add, and update user details
              </p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <div class="p-5 w-[37vw] space-y-6">
          <div class="w-full space-y-2 text-left flex flex-col">
            <label class="input-label">Account Status:</label>

            <div
              class="flex items-center justify-between rounded-xl border border-gray-200 px-4 py-3 bg-gray-50"
            >
              <div class="flex flex-col">
                <span class="font-medium text-sm text-gray-700">
                  {{ form.is_active ? "Active" : "Inactive" }}
                </span>

                <span class="text-xs text-gray-400">
                  User can login only when active
                </span>
              </div>

              <button
                type="button"
                @click="form.is_active = !form.is_active"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition',
                  form.is_active ? 'bg-green-500' : 'bg-gray-300',
                ]"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition',
                    form.is_active ? 'translate-x-6' : 'translate-x-1',
                  ]"
                />
              </button>
            </div>
          </div>
          <!-- STEP 1 -->
          <div
            v-if="currentStep === 1"
            class="grid grid-cols-2 items-start gap-3"
          >
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
                <option value="Department Chairperson">
                  Department Chairperson
                </option>
                <option value="Coordinator">Coordinator</option>
                <option value="Faculty">Faculty</option>
              </select>
            </div>
            <div class="w-full space-y-2 text-left flex flex-col">
              <label class="input-label">Employment Type:</label>
              <select v-model="form.employment_type" class="input-text">
                <option value="" disabled>Select employment type</option>
                <option value="Permanent">Permanent</option>
                <option value="Temporary">Temporary</option>
                <option value="Contract of Service">Contract of Service</option>
                <option value="Part Time">Part Time</option>
              </select>
            </div>

            <template v-if="!isAdminRole">
              <!-- Branch Coordinator: Department Chairperson only -->
              <div
                v-if="requiresCoorBranch"
                class="col-span-2 space-y-2 text-left flex flex-col"
              >
                <label class="input-label" for="college_branch_id">
                  Branch Coordinator:
                </label>

                <select
                  id="college_branch_id"
                  v-model.number="form.college_branch_id"
                  class="input-text"
                  :disabled="form.role === 'Faculty'"
                  :required="form.role === 'Coordinator'"
                >
                  <option :value="null">Select branch</option>

                  <option
                    v-for="branch in college_branch || []"
                    :key="branch.college_branch_id"
                    :value="Number(branch.college_branch_id)"
                  >
                    {{ branch.college_branch_name }}
                  </option>
                </select>

                <p
                  v-if="!(college_branch || []).length"
                  class="text-xs text-red-500"
                >
                  No branches available. Please add a branch first.
                </p>
              </div>

              <div class="w-full space-y-2 text-left flex flex-col">
                <label class="input-label">Designation:</label>
                <input
                  v-model="form.designation"
                  type="text"
                  class="input-text"
                  placeholder="Example: Instructor I"
                />
              </div>

              <!-- Department: Faculty and Program Chairperson only -->

              <div
                v-if="requiresDepartment"
                class="w-full space-y-2 text-left flex flex-col"
              >
                <label
                  class="input-label"
                  for="department_id"
                  :class="{ 'text-gray-400': !!form.college_branch_id }"
                >
                  Department:
                </label>

                <select
                  id="department_id"
                  v-model.number="form.department_id"
                  class="input-text transition-colors duration-200 truncate"
                  :class="
                    form.college_branch_id
                      ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed'
                      : 'bg-white text-gray-700 border-gray-300'
                  "
                  :disabled="form.role === 'Coordinator'"
                  :required="form.role === 'Faculty'"
                  :title="
                    departments.find(
                      (d) =>
                        Number(d.department_id) === Number(form.department_id),
                    )?.department_name || 'Select department'
                  "
                >
                  <option :value="null">Select department</option>

                  <option
                    v-for="department in departments"
                    :key="department.department_id"
                    :value="department.department_id"
                    :title="
                      department.department_name +
                      (department.institute?.institute_name
                        ? ` - ${department.institute.institute_name}`
                        : '')
                    "
                  >
                    {{ department.department_name }}
                    {{
                      department.institute?.institute_name
                        ? ` - ${department.institute.institute_name}`
                        : ""
                    }}
                  </option>
                </select>

                <p
                  v-if="!departments.length"
                  class="text-xs"
                  :class="
                    form.college_branch_id ? 'text-gray-400' : 'text-red-500'
                  "
                >
                  No departments available. Please add a department first.
                </p>
              </div>

              <div
                ref="instituteDropdown"
                class="flex flex-col space-y-2 w-full relative"
              >
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

              <div
                ref="programDropdown"
                class="flex flex-col space-y-2 w-full relative"
              >
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
                  @clickOutside="showProgramDropdown = false"
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

              <div class="w-full space-y-2 text-left flex flex-col">
                <label class="input-label">SP/MAS Unit:</label>

                <input
                  v-model.number="form.sp_mas_unit"
                  type="number"
                  min="0"
                  step="0.25"
                  class="input-text"
                  placeholder="Enter SP/MAS Unit"
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
            </template>
            <div class="col-span-2 w-full space-y-2 text-left">
              <label class="input-label">
                Preferred Rest Days (Choose up to 2)
              </label>

              <div class="flex flex-wrap gap-2">
                <label
                  v-for="day in restDays"
                  :key="day"
                  :class="[
                    'px-4 py-2 rounded-full border text-xs font-medium transition-all duration-200 cursor-pointer select-none',
                    form.preferred_rest_day.length >= 2 &&
                    !form.preferred_rest_day.includes(day)
                      ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed'
                      : form.preferred_rest_day.includes(day)
                      ? 'bg-defaultGreen text-white border-defaultGreen shadow-md'
                      : 'bg-white text-gray-700 border-gray-300 hover:border-defaultGreen hover:text-defaultGreen hover:bg-green-50',
                  ]"
                >
                  <input
                    type="checkbox"
                    :value="day"
                    v-model="form.preferred_rest_day"
                    :disabled="
                      form.preferred_rest_day.length >= 2 &&
                      !form.preferred_rest_day.includes(day)
                    "
                    class="hidden"
                  />

                  {{ day }}
                </label>
              </div>
            </div>
            <div class="col-span-2 flex justify-end pt-2">
              <button class="btn-save" type="button" @click="goToStep2">
                Next
              </button>
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

            <div
              v-if="!isEditMode"
              class="w-full space-y-2 text-left flex flex-col"
            >
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
        preferred_rest_day: [],
        sp_mas_unit: 0,
        unit_load: 0,
        is_active: true,
        institute_id: null,
        program_id: null,
        department_id: null,
        college_branch_id: null,
      },

      searchProgramQuery: "",
      showProgramDropdown: false,

      searchInstituteQuery: "",
      showInstituteDropdown: false,
      restDays: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ],
    };
  },

  computed: {
    ...mapState(useFetchDataStore, [
      "programs",
      "institutes",
      "departments",
      "college_branch",
    ]),

    isEditMode() {
      return !!this.userData;
    },

    isAdminRole() {
      return this.form.role === "Admin";
    },
    requiresDepartment() {
      return this.form.role === "Faculty";
    },

    requiresCoorBranch() {
      return this.form.role === "Coordinator";
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
            institute.institute_code?.toLowerCase().includes(query),
        )
        .sort((a, b) => a.institute_name.localeCompare(b.institute_name));
    },
  },

  watch: {
    "form.role"(newRole) {
      if (newRole === "Admin") {
        this.form.employment_type = "";
        this.form.designation = "";
        this.form.unit_load = 0;
        this.form.institute_id = null;
        this.form.program_id = null;
        this.form.department_id = null;
        this.form.is_under_dpt = false;

        this.searchInstituteQuery = "";
        this.searchProgramQuery = "";
      } else if (
        newRole !== "Coordinator" &&
        newRole !== "Department Chairperson"
      ) {
        this.form.college_branch_id = null;
      } else {
        if (!this.form.employment_type) {
          this.form.employment_type = "Full Time";
        }

        if (newRole === "Faculty") {
          this.form.is_under_dpt = true;
        } else {
          this.form.department_id = null;
          this.form.is_under_dpt = false;
        }
      }
    },
    "form.college_branch_id"(newBranchId) {
      if (newBranchId) {
        this.form.department_id = null;
        this.form.is_under_dpt = false;
      }
    },

    "form.department_id"(newDepartmentId) {
      this.form.is_under_dpt =
        newDepartmentId !== null &&
        newDepartmentId !== undefined &&
        newDepartmentId !== "";
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, [
      "fetchPrograms",
      "fetchInstitutes",
      "fetchDepartments",
      "fetchCollegeBranch",
    ]),
    handleClickOutside(event) {
      const dropdowns = [
        {
          ref: "instituteDropdown",
          state: "showInstituteDropdown",
        },
        {
          ref: "programDropdown",
          state: "showProgramDropdown",
        },
      ];

      dropdowns.forEach(({ ref, state }) => {
        const element = this.$refs[ref];

        if (element && !element.contains(event.target)) {
          this[state] = false;
        }
      });
    },
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
      const { first_name, last_name, role, institute_id, program_id } =
        this.form;

      if (!first_name || !last_name || !role) {
        toast.error("Please complete first name, last name, and role.");
        return;
      }

      if (role !== "Admin" && (!institute_id || !program_id)) {
        toast.error("Please select institute and program.");
        return;
      }

      if (
        role === "Faculty" &&
        !this.form.college_branch_id &&
        !this.form.department_id
      ) {
        toast.error("Please select a department or college branch.");
        return;
      }

      if (role === "Department Chairperson" && !this.form.college_branch_id) {
        toast.error("Please select a branch.");
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
        is_active: this.form.is_active,
      };

      if (!this.isAdminRole) {
        payload.employment_type = this.form.employment_type || "Full Time";

        payload.designation = this.form.designation?.trim() || "";
        payload.preferred_rest_day = this.form.preferred_rest_day;

        payload.sp_mas_unit =
          this.form.sp_mas_unit !== "" && this.form.sp_mas_unit !== null
            ? Number(this.form.sp_mas_unit)
            : null;

        payload.unit_load = Number(this.form.unit_load || 0);
        payload.institute_id = Number(this.form.institute_id);
        payload.program_id = Number(this.form.program_id);
      }

      if (this.requiresDepartment) {
        payload.department_id = this.form.department_id
          ? Number(this.form.department_id)
          : null;

        payload.college_branch_id = null;
        payload.is_under_dpt = payload.department_id !== null;
      } else if (this.requiresCoorBranch) {
        payload.department_id = null;
        payload.college_branch_id = this.form.college_branch_id
          ? Number(this.form.college_branch_id)
          : null;

        payload.is_under_dpt = false;
      } else {
        payload.department_id = null;
        payload.college_branch_id = null;
        payload.is_under_dpt = false;
      }

      if (this.requiresCoorBranch) {
        payload.college_branch_id =
          this.form.college_branch_id != null &&
          this.form.college_branch_id !== ""
            ? Number(this.form.college_branch_id)
            : null;
      } else {
        payload.college_branch_id = null;
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

      if (!this.isAdminRole && !this.form.institute_id) {
        toast.error("Institute is required.");
        return;
      }

      if (
        this.requiresDepartment &&
        !this.form.department_id &&
        !this.form.college_branch_id
      ) {
        toast.error("Please select a department or college branch.");
        this.currentStep = 1;
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
            { withCredentials: true },
          );

          toast.success("User updated successfully!");
        } else {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/auth/register",
            payload,
            {
              withCredentials: true,
            },
          );

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
      console.log("EDIT USER:", this.userData);
      console.log("BRANCH ID:", this.form.college_branch_id);
      console.log("AVAILABLE BRANCHES:", this.college_branch);
      this.form = {
        id: this.userData.id,
        email: this.userData.email || "",
        password: "",
        first_name: this.userData.first_name || "",
        last_name: this.userData.last_name || "",
        role: this.userData.role || "",
        employment_type: this.userData.employment_type || "Full Time",
        designation: this.userData.designation || "",
        preferred_rest_day: this.userData.preferred_rest_day || [],
        unit_load: Number(this.userData.unit_load || 0),
        is_active: this.userData.is_active ?? true,

        institute_id:
          this.userData.institute_id ||
          this.userData.institute?.institute_id ||
          null,

        program_id:
          this.userData.program_id || this.userData.program?.program_id || null,
        department_id:
          this.userData.department?.department_id != null
            ? Number(this.userData.department.department_id)
            : this.userData.department_id != null
            ? Number(this.userData.department_id)
            : null,

        college_branch_id:
          this.userData.college_branch?.college_branch_id != null
            ? Number(this.userData.college_branch.college_branch_id)
            : this.userData.college_branch_id != null
            ? Number(this.userData.college_branch_id)
            : null,

        is_under_dpt: this.userData.is_under_dpt ?? false,
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
      this.form.is_under_dpt = this.form.department_id != null;
      this.searchInstituteQuery =
        this.userData.institute?.institute_name ||
        this.userData.institute_name ||
        "";

      this.searchProgramQuery =
        this.userData.program?.program_name || this.userData.program_name || "";
    },
  },

  async mounted() {
    document.addEventListener("click", this.handleClickOutside);
    await Promise.all([
      this.fetchInstitutes(),
      this.fetchPrograms(),
      this.fetchDepartments(),
      this.fetchCollegeBranch(),
    ]);

    if (this.isEditMode) {
      this.fillEditForm();
    }
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleClickOutside);
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
