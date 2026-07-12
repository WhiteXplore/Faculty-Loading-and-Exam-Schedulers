<template>
  <div class="bg-white w-full rounded-md space-y-4 h-screen overflow-y-auto">
    <!-- DASHBOARD HEADER -->
    <div class="mb-2 lg:mb-6">
      <div
        class="grid grid-cols-2 md:grid-cols-2 xl:grid-cols-4 gap-2 lg:gap-3"
      >
        <div
          class="bg-white rounded-2xl lg:rounded-3xl border border-gray-100 p-5 shadow-sm hover:shadow-lg transition-all duration-300"
        >
          <div class="flex items-start justify-between">
            <div>
              <p
                class="text-[11px] uppercase tracking-[0.2em] text-gray-400 font-semibold"
              >
                Schedule
              </p>

              <h2 class="text-4xl font-black text-gray-900 mt-3">
                {{ scheduleCount }}
              </h2>

              <p class="text-sm text-gray-500 mt-1">
                Active Class Schedule{{ scheduleCount > 1 ? "s" : "" }}
              </p>
            </div>

            <div
              class="w-12 h-12 rounded-2xl bg-green-50 flex items-center justify-center"
            >
              <icon name="circle-check2" class="text-green-600" />
            </div>
          </div>
        </div>
        <!-- SUBJECTS -->
        <div
          class="bg-white rounded-2xl lg:rounded-3xl border border-gray-100 p-5 shadow-sm hover:shadow-lg transition-all duration-300"
        >
          <div class="flex items-start justify-between">
            <div>
              <p
                class="text-[11px] uppercase tracking-[0.2em] text-gray-400 font-semibold"
              >
                Subjects
              </p>

              <h2 class="text-4xl font-black text-gray-900 mt-3">
                {{ uniqueSubjects }}
              </h2>

              <p class="text-sm text-gray-500 mt-1">Preparation Subjects</p>
            </div>

            <div
              class="w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center"
            >
              <icon name="book-open" class="text-blue-600" />
            </div>
          </div>
        </div>

        <!-- TEACHING DAYS -->
        <div
          class="bg-white rounded-2xl lg:rounded-3xl border border-gray-100 p-5 shadow-sm hover:shadow-lg transition-all duration-300"
        >
          <div class="flex items-start justify-between">
            <div>
              <p
                class="text-[11px] uppercase tracking-[0.2em] text-gray-400 font-semibold"
              >
                Teaching Days
              </p>

              <h2 class="text-4xl font-black text-gray-900 mt-3">
                {{ activeDays }}
              </h2>

              <p class="text-sm text-gray-500 mt-1">Days Scheduled</p>
            </div>

            <div
              class="w-12 h-12 rounded-2xl bg-amber-50 flex items-center justify-center"
            >
              <icon name="calendar3" class="text-amber-600" />
            </div>
          </div>
        </div>

        <!-- UNITS -->
        <div
          class="bg-white rounded-2xl lg:rounded-3xl border border-gray-100 p-5 shadow-sm hover:shadow-lg transition-all duration-300 xl:col-span-1"
        >
          <div class="flex items-start justify-between">
            <div>
              <p
                class="text-[11px] uppercase tracking-[0.2em] text-gray-400 font-semibold"
              >
                Units
              </p>

              <h2 class="text-4xl font-black text-gray-900 mt-3">
                {{ totalUnits }}
              </h2>

              <p class="text-sm text-gray-500 mt-1">Total Teaching Units</p>
            </div>

            <div
              class="w-12 h-12 rounded-2xl bg-emerald-50 flex items-center justify-center"
            >
              <icon name="compute" class="text-emerald-600" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- HEADER -->
    <div
      class="flex flex-col lg:flex-row lg:justify-between lg:items-center gap-3"
    >
      <!-- DAY FILTER -->
      <div class="flex-1">
        <!-- MOBILE -->
        <div class="sticky top-0 z-30 bg-white">
          <div class="lg:hidden overflow-x-auto scrollbar-hide">
            <div class="flex gap-2 min-w-max pb-1">
              <button
                @click="selectedDay = 'ALL'"
                :class="[
                  'whitespace-nowrap px-4 py-2 rounded-full text-sm font-medium transition-all',
                  selectedDay === 'ALL'
                    ? 'bg-defaultGreen text-white shadow-sm'
                    : 'bg-gray-100 text-gray-500',
                ]"
              >
                All Days
              </button>

              <button
                v-for="day in days"
                :key="day"
                @click="selectedDay = day"
                :class="[
                  'whitespace-nowrap px-4 py-2 rounded-full text-sm font-medium transition-all',
                  selectedDay === day
                    ? 'bg-defaultGreen text-white shadow-sm'
                    : 'bg-gray-100 text-gray-500',
                ]"
              >
                {{ day }}
              </button>
            </div>
          </div>
        </div>

        <!-- DESKTOP (YOUR CURRENT DESIGN) -->
        <div class="hidden lg:flex flex-wrap items-center gap-2">
          <button
            @click="selectedDay = 'ALL'"
            :class="[
              'px-4 py-3 rounded-t-lg text-sm transition-all border',
              selectedDay === 'ALL'
                ? 'bg-defaultGreen text-white font-semibold border-gray-300 border-b-white shadow-sm'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200 border-transparent',
            ]"
          >
            All Days
          </button>

          <button
            v-for="day in days"
            :key="day"
            @click="selectedDay = day"
            :class="[
              'px-4 py-2 rounded-t-lg text-sm transition-all border',
              selectedDay === day
                ? 'bg-defaultGreen text-white font-semibold border-gray-300 border-b-white shadow-sm'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200 border-transparent',
            ]"
          >
            {{ day }}
          </button>
        </div>
      </div>

      <!-- DOWNLOAD BUTTON -->
      <div class="flex justify-end hidden lg:block">
        <div @click="previewPDF" class="btn-add">
          <div class="p-1 bg-white bg-opacity-20 rounded-full">
            <icon name="circle-down" />
          </div>
          <span class="btn-add-text">Download</span>
        </div>
      </div>
    </div>

    <!-- TABLE CARDS -->
    <div
      class="h-[92vh] lg:h-[70vh] pb-[12vh] lg:pb-8 rounded-xl overflow-y-auto mt-4"
    >
      <div
        v-if="tableRows.length"
        class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-5"
      >
        <div
          v-for="row in tableRows"
          :key="row.id"
          class="bg-white border border-gray-200 rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 overflow-hidden"
        >
          <!-- HEADER -->
          <div
            class="bg-gradient-to-r from-defaultGreen to-green-700 px-5 py-4 text-white"
          >
            <div class="flex items-start justify-between gap-3">
              <div class="min-w-0">
                <h3 class="text-lg font-bold truncate">
                  {{ row.code }}
                </h3>

                <p class="text-green-100 text-sm truncate">
                  {{ row.section }}
                </p>
              </div>

              <div
                class="bg-white/20 px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap"
              >
                {{ row.day }}
              </div>
            </div>
          </div>

          <!-- BODY -->
          <div class="p-5">
            <!-- DESCRIPTION -->
            <div class="mb-4">
              <p class="text-[11px] uppercase tracking-wide text-gray-400 mb-1">
                Course Description
              </p>

              <p class="font-medium text-gray-700">
                {{ row.description }}
              </p>
            </div>

            <!-- SCHEDULE -->
            <div class="space-y-3 mb-4">
              <div class="grid grid-cols-2 gap-3">
                <div
                  class="flex items-center gap-2 text-sm text-gray-600 min-w-0"
                >
                  <icon name="time" />
                  <span class="truncate">{{ row.time }}</span>
                </div>

                <div
                  class="flex items-center gap-2 text-sm text-gray-600 min-w-0"
                >
                  <icon name="location" />
                  <span class="truncate">{{ row.room }}</span>
                </div>
              </div>

              <div class="grid grid-cols-2 gap-3">
                <div
                  class="flex items-center gap-2 text-sm text-gray-600 min-w-0"
                >
                  <icon name="building" />
                  <span class="truncate">{{ row.campus }}</span>
                </div>

                <div
                  class="flex items-center gap-2 text-sm text-gray-600 min-w-0"
                >
                  <icon name="book-open1" />
                  <span class="truncate">{{ row.mode }}</span>
                </div>
              </div>
            </div>
            <!-- STATS -->
            <div class="flex gap-3 mb-4">
              <!-- ROOM TYPE -->
              <div
                class="flex-1 bg-gray-50 border border-gray-100 rounded-xl px-4 py-3"
              >
                <p
                  class="text-[11px] uppercase tracking-wide text-gray-400 font-medium"
                >
                  Type
                </p>

                <p class="mt-1 text-sm font-semibold text-gray-700">
                  {{ row.room_type || "N/A" }}
                </p>
              </div>

              <!-- MODE -->
              <div
                class="flex-1 bg-gray-50 border border-gray-100 rounded-xl px-4 py-3"
              >
                <p
                  class="text-[11px] uppercase tracking-wide text-gray-400 font-medium"
                >
                  Mode
                </p>

                <div class="mt-1">
                  <span
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold"
                    :class="
                      row.mode?.toLowerCase().includes('online')
                        ? 'bg-violet-100 text-violet-700'
                        : 'bg-orange-100 text-orange-700'
                    "
                  >
                    <span
                      class="w-1.5 h-1.5 rounded-full mr-1.5"
                      :class="
                        row.mode?.toLowerCase().includes('online')
                          ? 'bg-violet-500'
                          : 'bg-orange-500'
                      "
                    />
                    {{ row.mode }}
                  </span>
                </div>
              </div>
            </div>

            <!-- FOOTER -->
            <div
              class="border-t pt-3 flex items-center justify-between text-xs text-gray-500"
            >
              <span>Faculty Load</span>

              <span class="font-semibold text-defaultGreen">
                {{ row.units }} Units
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- EMPTY -->
      <div
        v-else
        class="flex flex-col items-center justify-center h-[50vh] text-gray-500"
      >
        <icon name="calendar" class="text-5xl mb-3 opacity-40" />

        <p class="font-medium">No schedule data available</p>

        <p class="text-sm text-gray-400 text-center lg:text-left px-10 lg:px-0">
          No faculty load found for the selected school year and semester.
        </p>
      </div>
    </div>

    <!-- ✅ PDF PREVIEW MODAL -->
    <div
      v-if="showPreviewModal"
      class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50"
    >
      <div class="bg-white w-[90vw] h-[90vh] rounded-2xl flex flex-col">
        <!-- HEADER -->
        <div class="flex justify-between items-center p-4 border-b">
          <h2 class="font-semibold text-lg">PDF Preview</h2>
          <button @click="showPreviewModal = false">✕</button>
        </div>

        <!-- PDF VIEW -->
        <iframe class="flex-1 w-full" :src="pdfUrl"></iframe>

        <!-- FOOTER -->
        <div class="p-4 flex justify-end gap-2 border-t">
          <button
            @click="showPreviewModal = false"
            class="px-4 py-2 border rounded"
          >
            Close
          </button>
          <button
            @click="downloadPDF"
            class="px-4 py-2 bg-green-600 text-white rounded"
          >
            Download
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState } from "pinia";
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";
import icon from "@/assets/icon.vue";
pdfMake.vfs = pdfFonts.vfs;
import { eventBus } from "@/bus/event-bus";
export default {
  components: {
    icon,
  },
  data() {
    return {
      selectedSemester: null,
      selectedSchoolYear: null,

      isSchoolYearOpen: false,
      isSemesterOpen: false,

      schoolYearOptions: ["2025-2026", "2024-2025", "2023-2024"],

      semesters: [
        { value: 1, label: "First Semester" },
        { value: 2, label: "Second Semester" },
      ],
      authenticatedEmployeeId: null,

      showPreviewModal: false,
      pdfDoc: null,
      pdfUrl: "",

      // ✅ FIX: base64 logo
      schoolLogo: "",
      // ADD THIS
      selectedDay: "ALL",
      days: [
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
      "final_schedules",
      "courses",
      "college_branch",
    ]),
    dashboardRows() {
      return this.filteredFacultyLoads.map((item) => {
        const course = this.courseMap[item.course_code] || {};

        let start = "",
          end = "";

        if (item.time_slot?.includes(" - ")) {
          [start, end] = item.time_slot.split(" - ");
        }

        return {
          id: item.id,
          section: item.set_name,
          code: item.course_code,
          description: course.course_title || item.course_code,
          lec: course.course_lec || 0,
          lab: course.course_lab || 0,
          units: (course.course_lec || 0) + (course.course_lab || 0),
          mode: item.mode || "Face-to-Face",
          day: item.day,
          time: `${start} - ${end}`,
          room: item.room_name,
          campus: this.collegeBranchMap[item.college_branch_id] || "Unknown",
        };
      });
    },
    scheduleCount() {
      return this.dashboardRows.length;
    },

    uniqueSubjects() {
      return new Set(this.dashboardRows.map((row) => row.code)).size;
    },

    activeDays() {
      return new Set(this.dashboardRows.map((row) => row.day)).size;
    },

    totalUnits() {
      const counted = new Set();

      return this.dashboardRows.reduce((sum, row) => {
        const key = row.section + row.code;

        if (!counted.has(key)) {
          counted.add(key);
          return sum + row.units;
        }

        return sum;
      }, 0);
    },
    semesterName() {
      return this.selectedSemester === 1 ? "First" : "Second";
    },

    collegeBranchMap() {
      return Object.fromEntries(
        (this.college_branch || []).map((b) => [
          Number(b.college_branch_id),
          b.college_branch_name,
        ]),
      );
    },

    courseMap() {
      return Object.fromEntries(
        (this.courses || []).map((c) => [c.course_code, c]),
      );
    },

    filteredFacultyLoads() {
      return (this.final_schedules || []).filter(
        (item) =>
          Number(item.faculty_id) === Number(this.authenticatedEmployeeId) &&
          item.school_year === this.selectedSchoolYear &&
          Number(item.semester) === Number(this.selectedSemester),
      );
    },

    tableRows() {
      const rows = this.filteredFacultyLoads.map((item) => {
        const course = this.courseMap[item.course_code] || {};

        let start = "",
          end = "";

        if (item.time_slot?.includes(" - ")) {
          [start, end] = item.time_slot.split(" - ");
        }

        return {
          id: item.id,
          section: item.set_name,
          code: item.course_code,
          description: course.course_title || item.course_code,
          lec: course.course_lec || 0,
          lab: course.course_lab || 0,
          units: (course.course_lec || 0) + (course.course_lab || 0),
          room_type: item.room_type || "N/A",
          mode: item.mode || "Face-to-Face",
          day: item.day,
          time: `${start} - ${end}`,
          room: item.room_name,
          campus: this.collegeBranchMap[item.college_branch_id] || "Unknown",
        };
      });

      if (this.selectedDay === "ALL") {
        return rows;
      }

      return rows.filter((row) => {
        const scheduleDay = (row.day || "").toUpperCase();
        return scheduleDay.includes(this.selectedDay.toUpperCase());
      });
    },
  },

  methods: {
    setCurrentDay() {
      const today = new Date().getDay();

      const dayMap = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        0: "Sunday",
      };

      this.selectedDay = dayMap[today] || "ALL";
    },
    getSemesterLabel(value) {
      const sem = this.semesters.find((s) => s.value === value);
      return sem ? sem.label : "";
    },
    selectSemester(sem) {
      this.selectedSemester = sem;
    },

    semesterBtn(active) {
      return [
        "px-4 py-2 rounded-xl text-sm font-semibold border  transition duration-200",
        active
          ? "bg-defaultGreen text-white"
          : "bg-white text-defaultGreen hover:bg-defaultGreen/80 hover:text-white",
      ];
    },

    async fetchUser() {
      try {
        const { data } = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          },
        );
        this.authenticatedEmployeeId = data.sub;
      } catch {
        this.$router.push("/");
      }
    },

    // ✅ LOAD LOGO AS BASE64
    async loadLogo() {
      const response = await fetch(require("@/assets/img/dnsc_logo.png"));
      const blob = await response.blob();

      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onloadend = () => resolve(reader.result);
        reader.readAsDataURL(blob);
      });
    },

    // ✅ PREVIEW PDF
    async previewPDF() {
      this.schoolLogo = await this.loadLogo();

      const headerRow = [
        "Section",
        "Code",
        "Description",
        "Lec",
        "Lab",
        "Units",
        "Mode",
        "Day",
        "Time",
        "Room",
        "Campus",
      ];

      const body = [
        headerRow.map((h) => ({
          text: h,
          style: "tableHeader",
          alignment: "center",
        })),
      ];

      this.tableRows.forEach((row) => {
        body.push([
          { text: row.section, alignment: "center" },
          { text: row.code, alignment: "center" },
          { text: row.description },
          { text: row.lec, alignment: "center" },
          { text: row.lab, alignment: "center" },
          { text: row.units, alignment: "center" },
          { text: row.mode, alignment: "center" },
          { text: row.day, alignment: "center" },
          { text: row.time, alignment: "center" },
          { text: row.room, alignment: "center" },
          { text: row.campus, alignment: "center" },
        ]);
      });

      body.push([
        { text: "TOTAL", colSpan: 5, alignment: "right", bold: true },
        {},
        {},
        {},
        {},
        { text: this.totalUnits, alignment: "center", bold: true },
        {},
        {},
        {},
        {},
        {},
      ]);

      const docDefinition = {
        pageOrientation: "landscape",
        pageMargins: [30, 40, 30, 30],

        content: [
          // ✅ HEADER
          {
            columns: [
              {
                image: this.schoolLogo,
                width: 70,
              },
              {
                width: "*",
                alignment: "center",
                stack: [
                  { text: "Republic of the Philippines", fontSize: 9 },
                  {
                    text: "Davao Del Norte State College",
                    style: "schoolName",
                  },
                  {
                    text: "New Visayas, Panabo City, Davao Del Norte, Philippines 8105",
                    fontSize: 8,
                  },
                  { text: "Website: www.ddnsc.edu.ph", fontSize: 8 },
                  {
                    text: "Email Address: president@ddnsc.edu.ph | registrars@ddnsc.edu.ph",
                    fontSize: 8,
                  },
                  {
                    text: "Telephone #: (084) 628 4301 | (084) 628 6342",
                    fontSize: 8,
                  },
                ],
              },
              { width: 70, text: "" },
            ],
          },

          // ✅ DIVIDER LINE
          {
            canvas: [
              {
                type: "line",
                x1: 0,
                y1: 5,
                x2: 770,
                y2: 5,
                lineWidth: 1,
              },
            ],
            margin: [0, 10, 0, 10],
          },

          // ✅ TITLE
          {
            text: "TEACHER'S LOAD",
            style: "mainTitle",
            alignment: "center",
          },
          {
            text: `${this.semesterName} Sem/Term: School Year ${this.selectedSchoolYear}`,
            alignment: "center",
            margin: [0, 0, 0, 10],
          },

          // ✅ TABLE
          {
            table: {
              headerRows: 1,
              widths: [
                "auto",
                "auto",
                "*",
                "auto",
                "auto",
                "auto",
                "auto",
                "auto",
                "auto",
                "auto",
                "auto",
              ],
              body,
            },
            layout: {
              hLineColor: () => "#ccc",
              vLineColor: () => "#ccc",
              fillColor: (rowIndex) => {
                if (rowIndex === 0) return "#16a34a";
                return rowIndex % 2 === 0 ? "#f9fafb" : null;
              },
            },
          },
        ],

        styles: {
          schoolName: { fontSize: 14, bold: true },
          mainTitle: { fontSize: 16, bold: true },
          tableHeader: { color: "white", bold: true, fontSize: 9 },
        },

        defaultStyle: { fontSize: 8 },
      };

      this.pdfDoc = pdfMake.createPdf(docDefinition);

      this.pdfDoc.getBlob((blob) => {
        this.pdfUrl = URL.createObjectURL(blob);
        this.showPreviewModal = true;
      });
    },

    downloadPDF() {
      this.pdfDoc.download("faculty-schedule.pdf");
    },
  },

  async mounted() {
    const store = useFetchDataStore();
    await this.fetchUser();
    await store.fetchCourses();
    await store.fetchFinalSchedules();
    await store.fetchCollegeBranch();
    this.setCurrentDay();

    this.stopEventBus = eventBus.on((activeYear) => {
      console.log("EventBus Data:", activeYear);

      if (!activeYear) return;

      this.selectedSchoolYear = activeYear.school_year_name;
      this.selectedSemester = Number(activeYear.semester);

      console.log(
        "Active School Year:",
        this.selectedSchoolYear,
        "Semester:",
        this.selectedSemester,
      );
    });
  },
};
</script>
