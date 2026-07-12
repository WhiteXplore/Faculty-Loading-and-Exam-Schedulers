<template>
  <div
    class="fixed inset-0 flex justify-center items-center bg-gray-800 bg-opacity-40 z-50"
  >
    <div
      class="rounded-[16px] shadow-lg flex flex-col animate-slideUp overflow-hidden"
    >
      <form
        @submit.prevent="submitData"
        class="w-[60vw] text-[13px] bg-white rounded-[16px] shadow-md flex flex-col"
        ref="yearSectionForm"
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
                Add Year/Section – {{ programData.program_name }}
              </h2>

              <p class="text-xs text-green-100">
                View, add, and update year & section details
              </p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <!-- BODY -->
        <div class="p-4 space-y-6 text-[13px] max-h-[80vh] overflow-y-auto">
          <!-- PROGRAM INFO -->
          <div class="p-4 bg-gray-50 border rounded-xl">
            <p class="text-gray-800">
              <span class="input-label">Program:</span>
              {{ programData.program_name }}
              ({{ programData.program_code }})
            </p>
          </div>

          <!-- Instructions -->
          <div class="p-4 bg-blue-50 border rounded-xl">
            <h3 class="font-bold text-gray-800">Instructions</h3>
            <ul
              class="list-disc list-inside text-gray-700 space-y-1 text-[12px]"
            >
              <li>Click "Add Year/Section" to configure sections.</li>
              <li>Set number of sections for each year level (1st–4th).</li>
              <li>Sections will be automatically named (A, B, C, etc.).</li>
            </ul>
          </div>

          <!-- SCHOOL YEAR -->
          <div class="flex flex-col space-y-2 w-full relative">
            <label class="input-label">
              School Year <span class="text-red-500">*</span>
            </label>

            <input
              v-model="searchSchoolYearQuery"
              type="text"
              placeholder="Search school year..."
              required
              class="px-4 py-3 border border-gray-300 rounded-lg text-gray-800 focus:ring-2 focus:ring-green-400 focus:border-green-400 outline-none"
              @focus="showSchoolYearDropdown = true"
            />

            <div
              v-if="showSchoolYearDropdown && filteredSchoolYears.length"
              class="absolute top-[75px] w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-40 overflow-y-auto z-10"
              @mouseleave="showSchoolYearDropdown = false"
            >
              <div
                v-for="sy in filteredSchoolYears"
                :key="sy.school_year_id"
                class="px-4 py-2 hover:bg-green-50 cursor-pointer"
                @mousedown="selectSchoolYear(sy)"
              >
                {{ sy.school_year_name }} - {{ formatSemester(sy.semester) }}
              </div>
            </div>
          </div>

          <div class="flex flex-col space-y-2 w-full relative">
            <label class="input-label">
              College Branch <span class="text-red-500">*</span>
            </label>

            <input
              v-model="searchCollegeBranchQuery"
              type="text"
              placeholder="Search college branch..."
              required
              class="px-4 py-3 border border-gray-300 rounded-lg text-gray-800 focus:ring-2 focus:ring-green-400 focus:border-green-400 outline-none"
              @focus="showCollegeBranchDropdown = true"
            />

            <div
              v-if="showCollegeBranchDropdown && filteredCollegeBranch.length"
              class="absolute top-[75px] w-full bg-white border border-gray-200 rounded-lg shadow-lg max-h-40 overflow-y-auto z-10"
            >
              <div
                v-for="cb in filteredCollegeBranch"
                :key="cb.college_branch_id"
                class="px-4 py-2 hover:bg-green-50 cursor-pointer"
                @mousedown.prevent="selectCollegeBranch(cb)"
              >
                {{ cb.college_branch_name }}
              </div>
            </div>
          </div>

          <!-- MAIN AREA -->
          <div class="flex flex-col lg:flex-row gap-6">
            <!-- LEFT: CONFIGURE SECTIONS -->
            <div class="flex-1">
              <h3
                class="font-semibold text-gray-800 text-sm mb-4 flex items-center gap-2"
              >
                <icon name="setting" class="text-green-700" />
                Configure Sections per Year Levels
              </h3>

              <div class="space-y-6">
                <div
                  v-for="year in yearLevels"
                  :key="year.value"
                  class="rounded-xl border border-gray-200 bg-white"
                >
                  <!-- HEADER -->
                  <div
                    class="flex justify-between items-center px-5 py-3 bg-gray-50 border-b rounded-t-xl"
                  >
                    <div class="per-page-container">
                      <icon name="calendar" class="size-5 text-green-700" />
                      <h4 class="font-semibold text-green-800">
                        {{ year.label }}
                      </h4>
                    </div>

                    <div class="flex items-center gap-2 text-sm">
                      <label class="text-gray-700 font-medium">
                        Sections:
                      </label>

                      <input
                        v-model.number="year.numSections"
                        type="number"
                        min="0"
                        max="10"
                        class="w-20 border border-gray-300 rounded-md px-3 py-1.5 text-center focus:ring-2 focus:ring-defaultGreen"
                        placeholder="0"
                        @input="updateSections(year)"
                      />
                    </div>
                  </div>

                  <!-- SECTION CARDS -->
                  <div
                    class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-2 gap-4 px-5 py-4"
                  >
                    <div
                      v-for="(section, index) in year.sections"
                      :key="index"
                      class="bg-green-50 border border-green-100 rounded-lg p-4 flex flex-col gap-2"
                    >
                      <div class="flex justify-between items-center">
                        <span class="font-semibold text-defaultGreen text-sm">
                          Section
                          {{
                            getSectionLetter(getStartIndex(year.label) + index)
                          }}
                        </span>

                        <span
                          class="bg-green-100 text-green-700 text-xs px-2 py-0.5 rounded-full"
                        >
                          {{ section.classSize || 0 }} students
                        </span>
                      </div>

                      <div class="per-page-container">
                        <icon name="users" class="size-4 text-defaultGreen" />

                        <input
                          v-model.number="section.classSize"
                          type="number"
                          min="1"
                          max="100"
                          class="flex-1 border border-gray-300 rounded-md px-3 py-2 text-center text-sm focus:ring-2 focus:ring-green-300"
                          placeholder="Enter size"
                        />
                      </div>
                    </div>
                  </div>

                  <div
                    v-if="year.numSections === 0"
                    class="text-gray-500 text-sm italic px-5 py-3 border-t border-green-100 bg-gray-50 rounded-b-xl"
                  >
                    No sections configured for {{ year.label }}.
                  </div>
                </div>
              </div>
            </div>

            <!-- RIGHT: SUMMARY -->
            <div
              v-if="totalSections > 0"
              class="flex-1 h-fit max-h-full overflow-y-auto"
            >
              <div class="flex items-center justify-between">
                <div class="font-semibold text-sm mb-2 flex items-center gap-2">
                  <icon name="summary" class="text-green-700" />
                  <h2>Summary</h2>
                </div>

                <p class="text-sm mb-3 text-gray-700">
                  Total sections:
                  <span class="font-bold text-green-700">
                    {{ totalSections }}
                  </span>
                </p>
              </div>

              <div class="space-y-4 text-sm mt-1.5">
                <div v-for="year in yearLevels" :key="year.value">
                  <div
                    v-if="year.numSections > 0"
                    class="bg-white rounded-xl border border-gray-200 p-3"
                  >
                    <h3 class="font-semibold text-green-700 mb-2">
                      {{ year.label }}
                    </h3>

                    <div class="space-y-2">
                      <div
                        v-for="(section, index) in year.sections"
                        :key="index"
                        class="flex justify-between items-center bg-gray-50 rounded-md px-3 py-3 border border-green-100"
                      >
                        <span>
                          Section
                          {{
                            getSectionLetter(getStartIndex(year.label) + index)
                          }}
                        </span>

                        <span class="text-xs text-gray-600">
                          {{ section.classSize }} students
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- BUTTONS -->
        <div class="flex justify-end gap-2 pt-4 border-t p-4">
          <button type="button" class="btn-cancel" @click="$emit('close')">
            Cancel
          </button>

          <button
            class="btn-save"
            type="submit"
            :disabled="totalSections === 0 || !selectedSchoolYearId"
          >
            Create Sections
          </button>
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
  name: "AddYearSectionModal",
  components: { icon },

  props: {
    programData: { type: Object, required: true },
  },

  data() {
    return {
      selectedSchoolYearId: null,
      selectedSchoolYear: null,
      searchSchoolYearQuery: "",
      showSchoolYearDropdown: false,

      searchCollegeBranchQuery: "",
      showCollegeBranchDropdown: false,
      selectedCollegeBranchId: null,

      yearLevels: [
        { value: 1, label: "1st Year", numSections: 0, sections: [] },
        { value: 2, label: "2nd Year", numSections: 0, sections: [] },
        { value: 3, label: "3rd Year", numSections: 0, sections: [] },
        { value: 4, label: "4th Year", numSections: 0, sections: [] },
      ],
    };
  },

  computed: {
    fetchStore() {
      return useFetchDataStore();
    },

    sections() {
      return this.fetchStore.sections;
    },

    schoolYears() {
      return this.fetchStore.school_years;
    },

    college_branch() {
      return this.fetchStore.college_branch;
    },

    filteredSchoolYears() {
      // show only active school years
      const activeSchoolYears = this.schoolYears.filter(
        (sy) => Number(sy.is_active) === 1,
      );

      // if no search query
      if (!this.searchSchoolYearQuery) {
        return activeSchoolYears;
      }

      const q = this.searchSchoolYearQuery.toLowerCase();

      return activeSchoolYears.filter((sy) =>
        sy.school_year_name?.toLowerCase().includes(q),
      );
    },

    filteredCollegeBranch() {
      if (!this.searchCollegeBranchQuery) return this.college_branch;

      const q = this.searchCollegeBranchQuery.toLowerCase();

      return this.college_branch.filter((cb) =>
        cb.college_branch_name?.toLowerCase().includes(q),
      );
    },

    totalSections() {
      return this.yearLevels.reduce(
        (sum, year) => sum + (year.numSections || 0),
        0,
      );
    },
  },

  methods: {
    formatSemester(value) {
      if (value === 1 || value === "1") return "First Semester";
      if (value === 2 || value === "2") return "Second Semester";
      return value;
    },

    selectSchoolYear(sy) {
      this.selectedSchoolYearId = sy.school_year_id;
      this.selectedSchoolYear = sy;

      this.searchSchoolYearQuery =
        sy.school_year_name + " - " + this.formatSemester(sy.semester);

      this.showSchoolYearDropdown = false;
    },

    selectCollegeBranch(cb) {
      this.selectedCollegeBranchId = cb.college_branch_id;
      this.searchCollegeBranchQuery = cb.college_branch_name;
      this.showCollegeBranchDropdown = false;
    },

    getSectionLetter(index) {
      const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
      return letters[index] || "?";
    },

    getStartIndex(yearLabel) {
      const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
      const nextLetter = this.getNextSectionLetter(yearLabel);
      return letters.indexOf(nextLetter);
    },

    getNextSectionLetter(yearLabel) {
      const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

      const filtered = this.sections.filter((cls) => {
        return (
          String(cls.program_id) === String(this.programData.program_id) &&
          String(cls.school_year_id) === String(this.selectedSchoolYearId) &&
          String(cls.college_branch_id) ===
            String(this.selectedCollegeBranchId) &&
          cls.set_name?.toLowerCase().includes(yearLabel.toLowerCase())
        );
      });

      if (!filtered.length) return "A";

      const existingLetters = filtered
        .map((cls) => {
          const parts = cls.set_name.split("-");
          return parts[1]?.trim();
        })
        .filter(Boolean);

      const indexes = existingLetters
        .map((l) => letters.indexOf(l))
        .filter((i) => i !== -1);

      if (!indexes.length) return "A";

      const highestIndex = Math.max(...indexes);

      return letters[highestIndex + 1] || "Z";
    },

    updateSections(year) {
      const currentNum = year.sections.length;
      const newNum = year.numSections || 0;

      if (newNum > currentNum) {
        for (let i = currentNum; i < newNum; i++) {
          year.sections.push({ classSize: 40 });
        }
      } else if (newNum < currentNum) {
        year.sections.splice(newNum);
      }
    },

    async submitData() {
      try {
        if (!this.selectedSchoolYearId) {
          toast.error("Please select a school year");
          return;
        }

        if (!this.selectedCollegeBranchId) {
          toast.error("Please select a college branch");
          return;
        }

        if (this.totalSections === 0) {
          toast.error("Please add at least one section");
          return;
        }

        const classesToCreate = [];
        const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        this.yearLevels.forEach((year) => {
          if (year.numSections > 0 && year.sections.length > 0) {
            const startIndex = this.getStartIndex(year.label);

            year.sections.forEach((section, index) => {
              const sectionLetter = letters[startIndex + index];

              classesToCreate.push({
                school_year_id: this.selectedSchoolYearId,
                college_branch_id: this.selectedCollegeBranchId,
                program_id: this.programData.program_id,
                set_name: `${year.label} - ${sectionLetter}`,
                class_size: section.classSize || 30,
              });
            });
          }
        });

        const promises = classesToCreate.map((classData) =>
          axios.post(
            process.env.VUE_APP_API_BASE_URL + "/class/add-class",
            classData,
          ),
        );

        await Promise.all(promises);

        toast.success(
          `Successfully created ${classesToCreate.length} section(s)!`,
        );

        this.$emit("refresh");
        this.$emit("close");
      } catch (err) {
        console.error(err);
        toast.error("Failed to create sections.");
      }
    },
  },

  async mounted() {
    const store = useFetchDataStore();

    if (!store.school_years.length) {
      await store.fetchSchoolYears();
    }

    if (!store.college_branch.length) {
      await store.fetchCollegeBranch();
    }

    if (!store.sections.length) {
      await store.fetchClassSections();
    }
  },
};
</script>
