<template>
  <div class="min-h-screen rounded-xl bg-[#F4F7F5] p-5 text-gray-800">
    <!-- TOP BAR -->
    <div
      class="mb-5 flex flex-col gap-4 rounded-2xl border border-white/80 bg-white/90 p-5 shadow-sm backdrop-blur md:flex-row md:items-center md:justify-between"
    >
      <div>
        <p class="text-xs font-semibold uppercase tracking-[0.25em] text-defaultGreen">
          Curriculum Report
        </p>
        <h1 class="mt-1 text-2xl font-bold tracking-tight text-gray-900">
          {{ currentInstituteName }}
        </h1>
        <p class="mt-1 text-sm text-gray-500">
          View and generate curriculum checklist by program.
        </p>
      </div>

      <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
        <!-- Program Select -->
        <div class="relative w-full sm:w-[22rem]" ref="programDropdownRef">
          <div
            class="relative flex items-center rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 focus-within:border-defaultGreen focus-within:ring-4 focus-within:ring-green-100"
          >
            <div class="absolute left-3 text-defaultGreen">
              <svg
                class="h-4 w-4"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6l4 2" />
                <circle cx="12" cy="12" r="9" />
              </svg>
            </div>

            <button
              type="button"
              @click="showProgramDropdown = !showProgramDropdown"
              class="w-full rounded-xl bg-transparent py-2.5 pl-10 pr-10 text-left text-sm font-semibold text-gray-700 outline-none"
            >
              <span v-if="selectedProgramData">
                {{ selectedProgramData.program_code }} -
                {{ selectedProgramData.curriculum_start_year }} -
                {{ selectedProgramData.curriculum_end_year }}
              </span>
              <span v-else class="text-gray-400">Select a program</span>
            </button>

            <button
              type="button"
              @click="showProgramDropdown = !showProgramDropdown"
              class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400 transition hover:bg-gray-100 hover:text-defaultGreen"
            >
              <svg
                class="h-4 w-4 transition-transform duration-200"
                :class="{ 'rotate-180': showProgramDropdown }"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
          </div>

          <div
            v-if="showProgramDropdown"
            class="absolute right-0 z-50 mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
          >
            <div class="border-b border-gray-100 px-4 py-3">
              <p class="text-xs font-semibold uppercase tracking-wide text-gray-400">
                Curriculum Prospectus
              </p>
            </div>

            <div class="max-h-[260px] overflow-y-auto p-1.5">
              <button
                v-for="program in uniquePrograms"
                :key="program.value"
                type="button"
                @click="selectProgram(program)"
                class="flex w-full items-center justify-between gap-3 rounded-lg px-3 py-2.5 text-left transition hover:bg-green-50"
                :class="selectedProgram === program.value ? 'bg-green-50' : ''"
              >
                <div>
                  <div class="flex justify-between items-center w-[16vw]">
                    <p class="text-sm font-semibold text-gray-800">
                      {{ program.program_code }}
                    </p>
                    <span
                      class="rounded-full bg-green-50 px-2.5 py-1 text-[11px] font-semibold text-green-700"
                    >
                      {{ program.curriculum_start_year }} -
                      {{ program.curriculum_end_year }}
                    </span>
                  </div>

                  <p class="text-xs text-gray-500">
                    {{ program.program_name }}
                  </p>
                </div>
              </button>

              <div
                v-if="uniquePrograms.length === 0"
                class="px-4 py-6 text-center text-sm text-gray-400"
              >
                No program found
              </div>
            </div>

            <div v-if="selectedProgram" class="border-t border-gray-100 p-2">
              <button
                type="button"
                @click="clearProgramSelection"
                class="w-full rounded-lg px-3 py-2 text-sm font-medium text-gray-500 transition hover:bg-gray-50 hover:text-gray-700"
              >
                Clear selection
              </button>
            </div>
          </div>
        </div>

        <!-- Generate Report Button -->
        <button
          type="button"
          @click="downloadProspectusPdf"
          class="group inline-flex h-11 items-center justify-center gap-2 rounded-xl bg-defaultGreen px-5 text-sm font-semibold text-white shadow-md shadow-green-900/10 transition-all duration-300 hover:-translate-y-0.5 hover:bg-green-700 hover:shadow-lg"
        >
          <span class="flex h-6 w-6 items-center justify-center rounded-full bg-white/15">
            <icon :name="'circle-add'" />
          </span>
          Download Prospectus
        </button>
      </div>
    </div>

    <!-- CONTENT -->
    <div
      v-if="groupedCourses.length"
      class="h-[82vh] overflow-auto rounded-2xl border border-gray-100 bg-white p-6 shadow-xl shadow-gray-200/60"
    >
      <!-- REPORT HEADER -->
      <div class="mb-4 overflow-hidden">
        <div class="px-6 py-5 text-center">
          <p class="text-xs font-semibold uppercase tracking-[0.25em] text-defaultGreen">
            Curriculum Checklist
          </p>
          <h2 class="mt-1 text-xl font-bold text-gray-900">
            {{ currentInstituteName }}
          </h2>
          <p class="mt-1 text-base font-medium text-gray-600">
            {{ selectedProgramData?.program_name || "No program selected" }}
          </p>
          <p v-if="filteredCourses.length" class="mt-2 text-sm text-gray-500">
            Curriculum Year
            <span class="font-semibold text-gray-800">
              {{ filteredCourses[0].curriculum?.curriculum_start_year }} -
              {{ filteredCourses[0].curriculum?.curriculum_end_year }}
            </span>
          </p>
        </div>
      </div>

      <!-- GROUPED TABLES -->
      <div class="space-y-6">
        <div
          v-for="(group, index) in groupedCourses"
          :key="index"
          class="overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm"
        >
          <div
            class="flex flex-col gap-1 border-b border-gray-100 bg-gray-50/80 px-5 py-4 sm:flex-row sm:items-center sm:justify-between"
          >
            <div>
              <h3 class="text-base font-bold text-gray-900">
                {{ formatYearLevel(group.level) }}
              </h3>
              <p class="text-sm font-medium text-defaultGreen">
                {{ formatSemester(group.semester) }}
              </p>
            </div>

            <div
              class="w-fit rounded-full bg-green-100 px-3 py-1 text-xs font-bold text-defaultGreen"
            >
              {{ group.courses.length }} Courses
            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="min-w-full table-fixed text-sm">
              <thead>
                <tr class="bg-white text-xs uppercase tracking-wide text-gray-500">
                  <th class="w-[10%] px-5 py-3 text-left font-bold">Code</th>
                  <th class="w-[30%] px-5 py-3 text-left font-bold">Description</th>
                  <th class="w-[9%] px-5 py-3 text-center font-bold">Sem</th>
                  <th class="w-[9%] px-5 py-3 text-center font-bold">Level</th>
                  <th class="w-[9%] px-5 py-3 text-center font-bold">Lec</th>
                  <th class="w-[9%] px-5 py-3 text-center font-bold">Lab</th>
                  <th class="w-[10%] px-5 py-3 text-center font-bold">Units</th>
                  <th class="w-[14%] px-5 py-3 text-left font-bold">Requisite</th>
                </tr>
              </thead>

              <tbody class="divide-y divide-gray-100">
                <tr
                  v-for="course in group.courses"
                  :key="course.course_id"
                  class="transition duration-200 hover:bg-green-50/70"
                >
                  <td class="px-5 py-3 font-bold text-defaultGreen">
                    {{ course.course_code }}
                  </td>

                  <td class="px-5 py-3 text-gray-700">
                    {{ course.course_description || course.course_title }}
                  </td>

                  <td class="px-5 py-3 text-center text-gray-600">
                    {{ course.course_semester }}
                  </td>

                  <td class="px-5 py-3 text-center text-gray-600">
                    {{ course.course_level }}
                  </td>

                  <td class="px-5 py-3 text-center text-gray-600">
                    {{ course.course_lec }}
                  </td>

                  <td class="px-5 py-3 text-center text-gray-600">
                    {{ course.course_lab }}
                  </td>

                  <td class="px-5 py-3 text-center">
                    <span
                      class="inline-flex min-w-8 items-center justify-center rounded-full bg-gray-100 px-2 py-1 text-xs font-bold text-gray-700"
                    >
                      {{ course.course_lec + course.course_lab }}
                    </span>
                  </td>

                  <td class="px-5 py-3 text-gray-600">
                    <span
                      v-if="course.course_requisite"
                      class="inline-flex rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700"
                    >
                      {{ course.course_requisite }}
                    </span>
                    <span v-else class="text-xs text-gray-400">None</span>
                  </td>
                </tr>

                <!-- TOTAL -->
                <tr class="bg-gray-50 font-bold text-gray-800">
                  <td colspan="6" class="px-5 py-4 text-right">Total Credit Units</td>
                  <td class="px-5 py-4 text-center text-defaultGreen">
                    {{
                      group.courses.reduce(
                        (sum, course) => sum + course.course_lec + course.course_lab,
                        0
                      )
                    }}
                  </td>
                  <td></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- NO COURSES -->
    <div
      v-else-if="selectedProgram"
      class="flex h-[70vh] flex-col items-center justify-center rounded-2xl border border-dashed border-gray-200 bg-white text-center shadow-sm"
    >
      <div
        class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-50 text-defaultGreen"
      >
        <icon :name="'book'" />
      </div>
      <h2 class="text-lg font-bold text-gray-800">No courses found</h2>
      <p class="mt-1 text-sm text-gray-500">
        No curriculum courses are available for this selected program.
      </p>
    </div>

    <!-- SELECT PROGRAM EMPTY STATE -->
    <div
      v-else
      class="flex h-[70vh] flex-col items-center justify-center rounded-2xl border border-gray-100 bg-white text-center shadow-sm"
    >
      <div
        class="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-50 text-defaultGreen"
      >
        <icon :name="'book'" />
      </div>
      <h2 class="text-lg font-bold text-gray-800">Select a program</h2>
      <p class="mt-1 text-sm text-gray-500">
        Choose a program above to view the curriculum checklist.
      </p>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import { mapState } from "pinia";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { eventBus } from "@/bus/event-bus";
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
pdfMake.vfs = pdfFonts.vfs;
export default {
  name: "ViewReportCurriculumPage",

  components: {
    icon,
  },

  data() {
    return {
      selectedProgram: "",
      instituteId: null,
      activeSchoolYear: null,
      stopEventBus: null,
      showProgramDropdown: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, [
      "detailedReportCurriculum",
      "curriculum_courses",
      "programs",
    ]),

    currentInstituteName() {
      const program = this.programs.find(
        (p) => String(p.institute_id) === String(this.instituteId)
      );

      if (program?.institute?.institute_name) {
        return program.institute.institute_name;
      }

      const report = this.detailedReportCurriculum.find(
        (item) => String(item.institute_id) === String(this.instituteId)
      );

      return report?.institute_name || "No institute name found";
    },

    uniquePrograms() {
      if (!this.instituteId) return [];

      const map = new Map();

      (this.curriculum_courses || []).forEach((item) => {
        const curriculum = item.curriculum;
        const program = curriculum?.program;

        if (!curriculum || !program) return;

        if (String(curriculum.institute_id) !== String(this.instituteId)) return;

        // IMPORTANT
        const key = String(curriculum.curriculum_id);

        if (!map.has(key)) {
          map.set(key, {
            value: String(curriculum.curriculum_id),

            curriculum_id: curriculum.curriculum_id,

            program_id: curriculum.program_id,

            program_name: program.program_name,

            program_code: program.program_code,

            curriculum_start_year: curriculum.curriculum_start_year,

            curriculum_end_year: curriculum.curriculum_end_year,
          });
        }
      });

      return Array.from(map.values());
    },
    selectedProgramData() {
      return this.uniquePrograms.find(
        (program) => String(program.value) === String(this.selectedProgram)
      );
    },

    filteredCourses() {
      if (!this.selectedProgram || !this.instituteId) return [];

      return (this.curriculum_courses || [])
        .filter((item) => {
          return (
            String(item.curriculum?.institute_id) === String(this.instituteId) &&
            // ONLY FILTER BY CURRICULUM ID
            String(item.curriculum?.curriculum_id) === String(this.selectedProgram)
          );
        })
        .map((item) => ({
          curriculum_course_id: item.curriculum_course_id,

          curriculum: item.curriculum,

          course_id: item.course?.course_id,

          course_code: item.course?.course_code,

          course_description:
            item.course?.course_title || item.course?.course_description,

          course_semester: item.course?.course_semester,

          course_level: item.course?.course_level,

          course_lec: Number(item.course?.course_lec || 0),

          course_lab: Number(item.course?.course_lab || 0),

          course_requisite: item.course?.course_requisite || "",
        }));
    },

    groupedCourses() {
      const groups = {};

      this.filteredCourses.forEach((course) => {
        const key = `${course.course_level}-${course.course_semester}`;

        if (!groups[key]) {
          groups[key] = {
            level: course.course_level,
            semester: course.course_semester,
            courses: [],
          };
        }

        groups[key].courses.push(course);
      });

      return Object.values(groups).sort((a, b) => {
        if (a.level === b.level) return a.semester - b.semester;
        return a.level - b.level;
      });
    },
  },

  watch: {
    uniquePrograms: {
      immediate: true,
      handler(programs) {
        if (!programs.length) {
          this.selectedProgram = "";
        }
      },
    },
  },

  methods: {
    selectProgram(program) {
      this.selectedProgram = program.value;
      this.showProgramDropdown = false;
    },

    clearProgramSelection() {
      this.selectedProgram = "";
      this.showProgramDropdown = false;
    },
    formatYearLevel(level) {
      switch (Number(level)) {
        case 1:
          return "First Year";
        case 2:
          return "Second Year";
        case 3:
          return "Third Year";
        case 4:
          return "Fourth Year";
        default:
          return `Year ${level}`;
      }
    },

    formatSemester(sem) {
      switch (Number(sem)) {
        case 1:
          return "First Semester";
        case 2:
          return "Second Semester";
        case 3:
          return "Summer";
        default:
          return `Semester ${sem}`;
      }
    },
    downloadProspectusPdf() {
      if (!this.groupedCourses.length) {
        alert("No curriculum checklist available to download.");
        return;
      }

      const body = [];

      body.push([
        { text: "Code", bold: true },
        { text: "Description", bold: true },
        { text: "Sem", bold: true, alignment: "center" },
        { text: "Level", bold: true, alignment: "center" },
        { text: "Lec", bold: true, alignment: "center" },
        { text: "Lab", bold: true, alignment: "center" },
        { text: "Units", bold: true, alignment: "center" },
        { text: "Requisite", bold: true },
      ]);

      this.groupedCourses.forEach((group) => {
        body.push([
          {
            text: `${this.formatYearLevel(group.level)} - ${this.formatSemester(
              group.semester
            )}`,
            colSpan: 8,
            bold: true,
            fillColor: "#EAF5EE",
            color: "#166534",
            margin: [0, 5, 0, 5],
          },
          {},
          {},
          {},
          {},
          {},
          {},
          {},
        ]);

        group.courses.forEach((course) => {
          body.push([
            course.course_code || "",
            course.course_description || course.course_title || "",
            { text: String(course.course_semester || ""), alignment: "center" },
            { text: String(course.course_level || ""), alignment: "center" },
            { text: String(course.course_lec || 0), alignment: "center" },
            { text: String(course.course_lab || 0), alignment: "center" },
            {
              text: String(
                Number(course.course_lec || 0) + Number(course.course_lab || 0)
              ),
              alignment: "center",
              bold: true,
            },
            course.course_requisite || "None",
          ]);
        });

        const totalUnits = group.courses.reduce(
          (sum, course) =>
            sum + Number(course.course_lec || 0) + Number(course.course_lab || 0),
          0
        );

        body.push([
          { text: "Total Credit Units", colSpan: 6, alignment: "right", bold: true },
          {},
          {},
          {},
          {},
          {},
          { text: String(totalUnits), alignment: "center", bold: true, color: "#166534" },
          "",
        ]);
      });

      const docDefinition = {
        pageSize: "A4",
        pageOrientation: "landscape",
        pageMargins: [30, 30, 30, 30],

        content: [
          {
            text: this.currentInstituteName,
            alignment: "center",
            bold: true,
            fontSize: 13,
          },
          {
            text: this.selectedProgramData?.program_name || "No program selected",
            alignment: "center",
            fontSize: 11,
            margin: [0, 2, 0, 2],
          },
          {
            text: this.filteredCourses.length
              ? `Curriculum Year ${
                  this.filteredCourses[0].curriculum?.curriculum_start_year || ""
                } - ${this.filteredCourses[0].curriculum?.curriculum_end_year || ""}`
              : "",
            alignment: "center",
            fontSize: 10,
            margin: [0, 0, 0, 15],
          },
          {
            table: {
              headerRows: 1,
              widths: ["10%", "30%", "7%", "7%", "7%", "7%", "8%", "24%"],
              body,
            },
            layout: {
              fillColor(rowIndex) {
                return rowIndex === 0 ? "#F3F4F6" : null;
              },
              hLineColor() {
                return "#D1D5DB";
              },
              vLineColor() {
                return "#D1D5DB";
              },
            },
            fontSize: 8,
          },
        ],

        defaultStyle: {
          fontSize: 9,
        },
      };

      const startYear =
        this.filteredCourses[0]?.curriculum?.curriculum_start_year || "Unknown";

      const endYear =
        this.filteredCourses[0]?.curriculum?.curriculum_end_year || "Unknown";

      const fileName = `Curriculum_Checklist_${
        this.selectedProgramData?.program_code || "Prospectus"
      }_${startYear}-${endYear}.pdf`;

      pdfMake.createPdf(docDefinition).download(fileName);
    },
  },

  async mounted() {
    const store = useFetchDataStore();

    this.instituteId = Number(this.$route.params.institute_id);

    const { sy_start, sy_end, semester, program_id } = this.$route.query;

    if (sy_start && sy_end && semester) {
      this.activeSchoolYear = {
        start_year: sy_start,
        end_year: sy_end,
        semester: Number(semester),
      };
    }

    if (program_id) {
      this.selectedProgram = Number(program_id);
    }

    await Promise.all([
      store.fetchPrograms(),
      store.fetchReportCurriculum(),
      store.fetchCurriculumCourses(),
    ]);

    this.stopEventBus = eventBus.on((newYear) => {
      if (!newYear) return;
      this.activeSchoolYear = newYear;
    });
  },

  beforeUnmount() {
    this.stopEventBus?.();
  },
};
</script>
