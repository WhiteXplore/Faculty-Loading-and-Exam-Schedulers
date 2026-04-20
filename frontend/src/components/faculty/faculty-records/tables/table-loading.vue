<template>
  <div class="bg-white w-full rounded-md">
    <!-- HEADER -->
    <div class="flex justify-between flex-wrap gap-2 items-center">
      <div class="flex gap-2 items-center flex-wrap">
        <!-- School Year -->
        <select
          v-model="selectedSchoolYear"
          class="px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
        >
          <option v-for="year in schoolYearOptions" :key="year" :value="year">
            {{ year }}
          </option>
        </select>

        <!-- Semester -->
        <button @click="selectSemester(1)" :class="semesterBtn(selectedSemester === 1)">
          First Semester
        </button>
        <button @click="selectSemester(2)" :class="semesterBtn(selectedSemester === 2)">
          Second Semester
        </button>
      </div>

      <!-- DOWNLOAD BUTTON -->
      <div
        @click="previewPDF"
        class="flex items-center gap-2 px-3 py-2 border bg-defaultGreen text-white border-green-600 rounded-xl hover:bg-white hover:text-defaultGreen hover:shadow-lg cursor-pointer transition duration-200"
      >
        <div class="p-1 bg-white bg-opacity-20 rounded-full">
          <icon name="edit" />
        </div>
        <span class="font-medium text-sm">Download</span>
      </div>
    </div>

    <!-- TABLE -->
    <div class="h-[75vh] overflow-y-auto mt-2">
      <div v-if="tableRows.length">
        <table class="min-w-full text-sm">
          <thead class="bg-defaultGreen text-white text-xs uppercase">
            <tr>
              <th class="py-3 w-[7%] rounded-tl-lg">Section</th>
              <th class="py-3 w-[5%]">Code</th>
              <th class="py-3 px-4 w-[25%] text-left">Description</th>
              <th class="py-3 w-[5%]">Lec</th>
              <th class="py-3 w-[5%]">Lab</th>
              <th class="py-3 w-[5%]">Units</th>
              <th class="py-3 w-[10%]">Mode</th>
              <th class="py-3 w-[7%]">Day</th>
              <th class="py-3 w-[10%]">Time</th>
              <th class="py-3 w-[10%]">Room</th>
              <th class="py-3 w-[10%] rounded-tr-lg">Campus</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="row in tableRows"
              :key="row.id"
              class="hover:bg-green-50 border-t text-xs"
            >
              <td class="py-3 border text-center">{{ row.section }}</td>
              <td class="py-3 border text-center">{{ row.code }}</td>
              <td class="py-3 border px-4 text-left">{{ row.description }}</td>
              <td class="py-3 border text-center">{{ row.lec }}</td>
              <td class="py-3 border text-center">{{ row.lab }}</td>
              <td class="py-3 border text-center">{{ row.units }}</td>
              <td class="py-3 border text-center font-semibold">{{ row.mode }}</td>
              <td class="py-3 border text-center">{{ row.day }}</td>
              <td class="py-3 border text-center">{{ row.time }}</td>
              <td class="py-3 border text-center">{{ row.room }}</td>
              <td class="py-3 border text-center">{{ row.campus }}</td>
            </tr>

            <!-- TOTAL -->
            <tr class="bg-gray-100 font-bold text-center border rounded-b-lg">
              <td colspan="5" class="text-right px-2 py-3 rounded-b-lg">TOTAL</td>
              <td>{{ totalUnits }}</td>
              <td colspan="5"></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="text-center text-gray-500 mt-10">
        No schedule data available.
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
          <button @click="showPreviewModal = false" class="px-4 py-2 border rounded">
            Close
          </button>
          <button @click="downloadPDF" class="px-4 py-2 bg-green-600 text-white rounded">
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

pdfMake.vfs = pdfFonts.vfs;

export default {
  data() {
    return {
      selectedSemester: 1,
      selectedSchoolYear: "2025-2026",
      schoolYearOptions: ["2025-2026", "2024-2025", "2023-2024"],
      authenticatedEmployeeId: null,

      showPreviewModal: false,
      pdfDoc: null,
      pdfUrl: "",

      // ✅ FIX: base64 logo
      schoolLogo: "",
    };
  },

  computed: {
    ...mapState(useFetchDataStore, ["final_schedules", "courses", "college_branch"]),

    semesterName() {
      return this.selectedSemester === 1 ? "First" : "Second";
    },

    collegeBranchMap() {
      return Object.fromEntries(
        (this.college_branch || []).map((b) => [
          Number(b.college_branch_id),
          b.college_branch_name,
        ])
      );
    },

    courseMap() {
      return Object.fromEntries((this.courses || []).map((c) => [c.course_code, c]));
    },

    filteredFacultyLoads() {
      return (this.final_schedules || []).filter(
        (item) =>
          Number(item.faculty_id) === Number(this.authenticatedEmployeeId) &&
          Number(item.semester) === Number(this.selectedSemester) &&
          item.school_year === this.selectedSchoolYear
      );
    },

    tableRows() {
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

    totalUnits() {
      const counted = new Set();
      return this.tableRows.reduce((sum, row) => {
        const key = row.section + row.code;
        if (!counted.has(key)) {
          counted.add(key);
          return sum + row.units;
        }
        return sum;
      }, 0);
    },
  },

  methods: {
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
        const { data } = await axios.get(process.env.VUE_APP_API_BASE_URL + "/auth/me", {
          withCredentials: true,
        });
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
                  { text: "Davao Del Norte State College", style: "schoolName" },
                  {
                    text: "New Visayas, Panabo City, Davao Del Norte, Philippines 8105",
                    fontSize: 8,
                  },
                  { text: "Website: www.ddnsc.edu.ph", fontSize: 8 },
                  {
                    text:
                      "Email Address: president@ddnsc.edu.ph | registrars@ddnsc.edu.ph",
                    fontSize: 8,
                  },
                  { text: "Telephone #: (084) 628 4301 | (084) 628 6342", fontSize: 8 },
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
  },
};
</script>
