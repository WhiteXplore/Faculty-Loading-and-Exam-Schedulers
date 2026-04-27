<template>
  <div
    class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50 w-screen"
  >
    <div
      class="flex justify-center items-center w-full max-w-md bg-white p-4 rounded-xl shadow-lg"
    >
      <div class="flex flex-col w-full">
        <!-- Header -->
        <div class="flex justify-start">
          <h1 class="font-semibold text-lg text-gray-800">Upload Courses</h1>
        </div>
        <p class="text-sm text-gray-500 mt-1">
          Upload an Excel or CSV file containing the course list.
        </p>

        <!-- Drag & Drop / Click Zone -->
        <div
          class="flex justify-center items-center cursor-pointer border-2 border-dashed border-gray-300 rounded-md p-8 w-full max-w-xl mx-auto mt-3"
          :class="{ 'bg-gray-100': dragging }"
          @dragover.prevent="dragging = true"
          @dragleave.prevent="dragging = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
        >
          <div class="text-center">
            <p v-if="!file" class="text-gray-600">
              <span class="text-defaultGreen">Upload a file</span> or drag and drop<br />
              Excel / CSV (.xlsx, .xls, .csv) up to 10MB
            </p>
            <p v-else class="text-defaultGreen">File uploaded: {{ file.name }}</p>

            <input
              type="file"
              class="hidden"
              ref="fileInput"
              @change="handleFileUpload"
              accept=".csv, .xlsx, .xls"
            />
          </div>
        </div>

        <!-- Accepted Files Info -->
        <div class="mt-3 text-[13px] flex justify-between text-left">
          <div>
            <p class="text-gray-600">Accepted Files: .xlsx, .xls, .csv</p>
            <p class="text-green-700">example.xlsx</p>
          </div>
        </div>

        <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>

        <!-- Uploading Status -->
        <div
          v-if="uploading"
          class="text-defaultGreen text-sm flex items-center gap-2 mt-2"
        >
          <span
            class="animate-spin border-2 border-green-600 border-t-transparent rounded-full w-4 h-4"
          ></span>
          Uploading...
        </div>

        <!-- Duplicate course_code container -->
        <div
          v-if="duplicateCourseCodes.length"
          class="mt-3 rounded-lg border border-yellow-300 bg-yellow-50 p-3"
        >
          <p class="text-sm font-semibold text-yellow-800">
            These course codes already exist in the database:
          </p>

          <div class="mt-2 flex flex-wrap gap-2 max-h-28 overflow-y-auto">
            <span
              v-for="code in duplicateCourseCodes"
              :key="code"
              class="px-2 py-1 rounded-full bg-yellow-200 text-yellow-900 text-xs font-medium"
            >
              {{ code }}
            </span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="tracking-wide flex justify-end gap-2 mt-4">
          <button class="btn-cancel" @click="$emit('close')">Cancel</button>
          <button class="btn-save" @click="submitUpload" :disabled="!file || uploading">
            {{ uploading ? "Processing..." : "Upload" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as XLSX from "xlsx";
import axios from "axios";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";

export default {
  name: "UploadCoursesPage",
  data() {
    return {
      file: null,
      dragging: false,
      uploading: false,
      parsedData: null,
      duplicateCourseCodes: [],
    };
  },

  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },

    handleDrop(e) {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files.length) this.handleFileUpload({ target: { files } });
      this.dragging = false;
    },

    handleFileUpload(event) {
      const selected = event.target.files[0];
      if (!selected) return;

      this.file = selected;
      this.duplicateCourseCodes = [];

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: "array" });
          const worksheet = workbook.Sheets[workbook.SheetNames[0]];
          const json = XLSX.utils.sheet_to_json(worksheet, { defval: "" });

          if (!json.length) throw new Error("Empty file");

          const instituteMap = {
            IC: "Institute of Computing",
            ITED: "Institute of Teacher Education",
            ILEGG: "Institute of Leadership, Entrepreneurship and Good Governance",
            IAAS: "Institute of Applied and Aquatic Sciences",
          };

          const programMap = {
            BSIT: "Bachelor of Science in Information Technology",
            BSIS: "Bachelor of Science in Information Systems",
            BSAF: "Bachelor of Science in Agro-Forestry",
            BSFAS: "Bachelor of Science in Fisheries and Aquatic Sciences",
            BSFT: "Bachelor of Science in Food Technology",
            BSMB: "Bachelor of Science in Marine Biology",
            BPA: "Bachelor of Public Administration",
            BSDRM: "Bachelor of Science in Disaster Resiliency and Management",
            BSENTREP: "Bachelor of Science in Entrepreneurship",
            BSSW: "Bachelor of Science in Social Work",
            BSTM: "Bachelor of Science in Tourism Management",
            BSEDMATH: "Bachelor of Secondary Education Major in Math",
            BSEDSCI: "Bachelor of Secondary Education Major in Science",
            BSEDENG: "Bachelor of Secondary Education Major in English",
            BACOMM: "Bachelor of Arts in Communication",
            BTLEd: "Bachelor of Technology and Livelihood Education",
            BPE: "Bachelor of Physical Education",
          };

          this.parsedData = json.map((row) => {
            const [start, end] = String(row["School Year"] || "")
              .split("-")
              .map((y) => Number(String(y).trim()));

            return {
              curriculum_start_year: start,
              curriculum_end_year: end,
              institute_code: String(row.Institute || "").trim(),
              institute_name: instituteMap[String(row.Institute || "").trim()] || "",
              program_code: String(row.Program || "").trim(),
              program_name:
                programMap[String(row.Program || "").trim()] ||
                String(row.Program || "").trim(),
              course_level: Number(row["Year Level"]),
              course_semester: Number(row.Semester),
              course_code: String(row["Course Code"] || "").trim(),
              course_title: String(row["Course Title"] || "").trim(),
              course_lec: Number(row["Lecture Units"]),
              course_lab: Number(row["Laboratory Units"]),
            };
          });

          console.log("Transformed Data:", this.parsedData);
        } catch (err) {
          console.error("Error parsing file:", err);
          alert("Invalid or corrupted file.");
        }
      };

      reader.readAsArrayBuffer(selected);
    },

    async submitUpload() {
      if (!this.parsedData || !this.parsedData.length) {
        toast.warning("Please upload a valid file first!");
        return;
      }

      this.uploading = true;
      this.duplicateCourseCodes = [];

      try {
        const fetchDataStore = useFetchDataStore();

        if (!fetchDataStore.courses.length) {
          await fetchDataStore.fetchCourses();
        }

        const existingCourses = fetchDataStore.courses;

        const normalize = (val) =>
          String(val || "")
            .replace(/\s+/g, "")
            .toUpperCase()
            .trim();

        // existing course_code in database
        const existingCourseCodeSet = new Set(
          existingCourses.map((course) => normalize(course.course_code)).filter(Boolean)
        );

        // duplicate course_code inside uploaded file itself
        const seenUploadCodes = new Set();
        const uploadDuplicateCodes = new Set();

        this.parsedData.forEach((row) => {
          const code = normalize(row.course_code);
          if (!code) return;

          if (seenUploadCodes.has(code)) {
            uploadDuplicateCodes.add(code);
          } else {
            seenUploadCodes.add(code);
          }
        });

        // codes already in database
        const duplicateInDatabase = this.parsedData
          .map((row) => normalize(row.course_code))
          .filter((code) => code && existingCourseCodeSet.has(code));

        this.duplicateCourseCodes = [...new Set(duplicateInDatabase)];

        // =========================================================
        // SAVE INSTITUTES FROM ALL ROWS
        // =========================================================
        const uniqueInstitutes = [
          ...new Map(
            this.parsedData
              .filter((row) => row.institute_code)
              .map((row) => [row.institute_code, row])
          ).values(),
        ];

        const instituteMap = new Map();

        for (const inst of uniqueInstitutes) {
          const res = await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/institute/add-institute",
            {
              institute_code: inst.institute_code,
              institute_name: inst.institute_name,
            }
          );

          instituteMap.set(inst.institute_code, res.data.institute_id);
        }

        // =========================================================
        // SAVE PROGRAMS + CURRICULUMS FROM ALL ROWS
        // =========================================================
        const uniquePrograms = [
          ...new Map(
            this.parsedData
              .filter(
                (row) =>
                  row.institute_code &&
                  row.program_code &&
                  row.curriculum_start_year &&
                  row.curriculum_end_year
              )
              .map((row) => [
                `${row.institute_code}-${row.program_code}-${row.curriculum_start_year}-${row.curriculum_end_year}`,
                row,
              ])
          ).values(),
        ];

        const programMap = new Map();
        const curriculumMap = new Map();

        for (const prog of uniquePrograms) {
          const programRes = await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/programs/add-programs",
            {
              program_code: prog.program_code,
              program_name: prog.program_name,
              institute_id: instituteMap.get(prog.institute_code),
            }
          );

          const program = programRes.data;

          programMap.set(
            `${prog.institute_code}-${prog.program_code}`,
            program.program_id
          );

          const curriculumKey = `${prog.institute_code}-${prog.program_code}-${prog.curriculum_start_year}-${prog.curriculum_end_year}`;

          if (!curriculumMap.has(curriculumKey)) {
            const curriculumRes = await axios.post(
              process.env.VUE_APP_API_BASE_URL + "/curriculums/add-curriculums",
              {
                curriculum_start_year: prog.curriculum_start_year,
                curriculum_end_year: prog.curriculum_end_year,
                institute_id: instituteMap.get(prog.institute_code),
                program_id: program.program_id,
              }
            );

            const curriculum = curriculumRes.data;
            curriculumMap.set(curriculumKey, curriculum.curriculum_id);
          }
        }

        // =========================================================
        // SAVE ONLY NEW COURSES
        // =========================================================
        const addedInThisBatch = new Set();

        const filteredParsedData = this.parsedData.filter((row) => {
          const code = normalize(row.course_code);
          if (!code) return false;

          if (existingCourseCodeSet.has(code)) return false;
          if (addedInThisBatch.has(code)) return false;

          addedInThisBatch.add(code);
          return true;
        });

        const newCourses = filteredParsedData.map((row) => ({
          course_level: row.course_level,
          course_semester: row.course_semester,
          course_code: row.course_code,
          course_title: row.course_title,
          course_lec: row.course_lec,
          course_lab: row.course_lab,
        }));

        if (newCourses.length) {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL + "/courses/add-courses",
            newCourses
          );
        }

        // refresh all courses so we can get course_id of both old + newly inserted
        await fetchDataStore.fetchCourses();

        const allCourses = fetchDataStore.courses;

        const courseIdMap = new Map();
        allCourses.forEach((course) => {
          const normalizedCode = normalize(course.course_code);
          if (normalizedCode) {
            courseIdMap.set(normalizedCode, course.course_id);
          }
        });

        // =========================================================
        // BUILD CURRICULUM-COURSE LINKS
        // use ALL uploaded rows, including existing course codes
        // =========================================================
        const curriculumCourseLinks = [];
        const seenLinks = new Set();

        this.parsedData.forEach((row) => {
          const curriculumKey = `${row.institute_code}-${row.program_code}-${row.curriculum_start_year}-${row.curriculum_end_year}`;
          const curriculum_id = curriculumMap.get(curriculumKey);
          const course_id = courseIdMap.get(normalize(row.course_code));

          if (!curriculum_id || !course_id) return;

          const linkKey = `${curriculum_id}-${course_id}`;
          if (seenLinks.has(linkKey)) return;

          seenLinks.add(linkKey);

          curriculumCourseLinks.push({
            curriculum_id,
            course_id,
          });
        });

        if (curriculumCourseLinks.length) {
          await axios.post(
            process.env.VUE_APP_API_BASE_URL +
              "/curriculum-courses/submit-curriculum-courses",
            {
              links: curriculumCourseLinks,
              raw_payload: this.parsedData,
            }
          );
        }

        // =========================================================
        // TOAST MESSAGES
        // =========================================================
        if (!newCourses.length && this.duplicateCourseCodes.length) {
          toast.warning(
            "All uploaded course codes already exist in the database. Institute, program, curriculum, and curriculum-course links were still processed."
          );
        } else if (this.duplicateCourseCodes.length) {
          toast.success(
            `${newCourses.length} new courses uploaded successfully. Existing course codes were skipped, and curriculum-course links were saved.`
          );
        } else if (uploadDuplicateCodes.size) {
          toast.success(
            `${newCourses.length} new courses uploaded successfully. Duplicate course codes in the file were skipped, and curriculum-course links were saved.`
          );
        } else {
          toast.success(
            `${newCourses.length} new courses uploaded successfully with curriculum-course links.`
          );
        }

        this.$emit("refresh");
        this.$emit("close");
      } catch (error) {
        console.error("Upload failed:", error);
        toast.error("Upload failed.");
      } finally {
        this.uploading = false;
      }
    },
  },
};
</script>

<style scoped>
input[type="file"]:focus + div {
  outline: 2px dashed #22c55e;
  outline-offset: 2px;
}
</style>
