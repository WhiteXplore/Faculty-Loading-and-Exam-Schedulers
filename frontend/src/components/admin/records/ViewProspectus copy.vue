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
        <div class="relative w-full sm:w-[22rem]">
          <select
            v-model="selectedProgram"
            id="program"
            class="h-11 w-full appearance-none rounded-xl border border-gray-200 bg-gray-50 px-4 pr-11 text-sm font-semibold text-gray-800 shadow-inner outline-none transition-all duration-300 hover:border-defaultGreen hover:bg-white focus:border-defaultGreen focus:bg-white focus:ring-4 focus:ring-green-100"
          >
            <option value="" disabled>Select a program</option>
            <option
              v-for="program in uniquePrograms"
              :key="program.program_id"
              :value="program.program_id"
            >
              {{ program.program_name }}
            </option>
          </select>

          <div class="pointer-events-none absolute inset-y-0 right-4 flex items-center">
            <svg
              class="h-4 w-4 text-defaultGreen"
              fill="none"
              stroke="currentColor"
              stroke-width="2.4"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>

        <!-- Generate Report Button -->
        <button
          type="button"
          @click="toggleGenerate"
          class="group inline-flex h-11 items-center justify-center gap-2 rounded-xl bg-defaultGreen px-5 text-sm font-semibold text-white shadow-md shadow-green-900/10 transition-all duration-300 hover:-translate-y-0.5 hover:bg-green-700 hover:shadow-lg"
        >
          <span
            class="flex h-6 w-6 items-center justify-center rounded-full bg-white/15 transition group-hover:bg-white/25"
          >
            <icon :name="'circle-add'" />
          </span>
          Generate Report
        </button>
      </div>
    </div>

    <!-- CONTENT -->
    <div
      v-if="groupedCourses.length"
      class="h-[82vh] overflow-auto rounded-2xl border border-gray-100 bg-white p-6 shadow-xl shadow-gray-200/60"
    >
      <!-- REPORT HEADER -->
      <div
        class="mb-6 overflow-hidden rounded-2xl border border-gray-100 bg-gradient-to-br from-white via-white to-green-50"
      >
        <!-- <div
          class="flex flex-col gap-5 p-6 lg:flex-row lg:items-center lg:justify-between"
        >
          <div class="flex items-center gap-4">
            <div
              class="flex h-20 w-20 shrink-0 items-center justify-center rounded-2xl bg-white shadow-sm ring-1 ring-gray-100"
            >
              <img
                src="@/assets/img/dnsc_logo.png"
                alt="DNSC Logo"
                class="h-16 w-16 object-contain"
              />
            </div>

            <div>
              <h2 class="text-2xl font-extrabold tracking-tight text-gray-900">
                DAVAO DEL NORTE
              </h2>
              <h3 class="text-xl font-medium tracking-wide text-gray-700">
                STATE COLLEGE
              </h3>
              <p class="mt-1 text-sm italic text-gray-500">
                "Inspiring Change, Creating Futures"
              </p>
            </div>
          </div>

          <div
            class="rounded-2xl border border-gray-100 bg-white/80 px-5 py-4 text-sm text-gray-600 shadow-sm"
          >
            <p class="font-medium">president@dnsc.edu.ph</p>
            <p>dnsc.edu.ph</p>
            <p>@officialdnsc</p>
          </div>
        </div> -->

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

      return this.programs
        .filter((program) => String(program.institute_id) === String(this.instituteId))
        .map((program) => ({
          program_id: program.program_id,
          program_name: program.program_name,
          program_code: program.program_code,
        }));
    },

    selectedProgramData() {
      return this.programs.find(
        (program) =>
          String(program.program_id) === String(this.selectedProgram) &&
          String(program.institute_id) === String(this.instituteId)
      );
    },

    filteredCourses() {
      if (!this.selectedProgram || !this.instituteId) return [];

      let result = this.curriculum_courses || [];

      result = result.filter((item) => {
        return (
          String(item.curriculum?.institute_id) === String(this.instituteId) &&
          String(item.curriculum?.program_id) === String(this.selectedProgram)
        );
      });

      if (this.activeSchoolYear) {
        result = result.filter((item) => {
          return (
            String(item.curriculum?.curriculum_start_year) ===
              String(this.activeSchoolYear.start_year) &&
            String(item.curriculum?.curriculum_end_year) ===
              String(this.activeSchoolYear.end_year) &&
            Number(item.course?.course_semester) ===
              Number(this.activeSchoolYear.semester)
          );
        });
      }

      return result.map((item) => ({
        curriculum_course_id: item.curriculum_course_id,
        curriculum: item.curriculum,
        course_id: item.course?.course_id,
        course_code: item.course?.course_code,
        course_description: item.course?.course_title || item.course?.course_description,
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
        if (!this.selectedProgram && programs.length) {
          this.selectedProgram = programs[0].program_id;
        }
      },
    },
  },

  methods: {
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
        default:
          return `Semester ${sem}`;
      }
    },

    toggleGenerate() {
      window.print();
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
