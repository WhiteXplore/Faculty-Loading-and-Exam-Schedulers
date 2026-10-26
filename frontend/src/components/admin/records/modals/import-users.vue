<template>
  <div class="modal-overlay">
    <div class="rounded-[16px] shadow-lg justify-center animate-slideUp">
      <div class="w-auto bg-white text-[13px] rounded-[16px] shadow-lg">
        <!-- Header -->

        <div class="modal-header">
          <div class="flex items-center gap-3">
            <!-- Icon -->
            <div class="glass-container">
              <icon name="circle-add2" class="text-white" />
            </div>

            <!-- Title -->
            <div>
              <h2 class="text-lg font-semibold text-white">Import Users</h2>

              <p class="text-xs text-green-100">Upload user accounts data.</p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <!-- Form Content -->
        <div class="p-5 w-[25vw] space-y-4">
          <!-- Instructions -->

          <!-- <div class="rounded-lg border border-blue-100 bg-blue-50/60 p-4">
            <h3 class="mb-3 text-sm font-semibold text-blue-800">
              Import Instructions
            </h3>

            <ul class="space-y-2 text-sm text-gray-600">
              <li class="flex items-start gap-2">
                <span class="text-blue-500">•</span>
                <span>File must be in XLSX format (.xlsx).</span>
              </li>

              <li class="flex items-start gap-2">
                <span class="text-blue-500">•</span>
                <span>
                  Required columns: Last Name, First Name, Email, Role.
                </span>
              </li>

              <li class="flex items-start gap-2">
                <span class="text-blue-500">•</span>
                <span>
                  Optional column: Program (must match an existing program
                  name).
                </span>
              </li>

              <li class="flex items-start gap-2">
                <span class="text-blue-500">•</span>
                <span>
                  Default password will be:
                  <span class="font-semibold text-gray-800">Password123!</span>
                </span>
              </li>
            </ul>
          </div> -->

          <!-- Download Template Button -->

          <!-- File Upload Area -->
          <div class="space-y-2">
            <div
              @dragover.prevent="dragOver = true"
              @dragleave.prevent="dragOver = false"
              @drop.prevent="handleFileDrop"
              :class="[
                'border-2 border-dashed rounded-lg p-6 text-center transition-all',
                dragOver
                  ? 'border-green-500 bg-green-50'
                  : 'border-gray-300 bg-gray-50',
              ]"
            >
              <input
                ref="fileInput"
                type="file"
                accept=".xlsx"
                @change="handleFileChange"
                class="hidden"
              />

              <div v-if="!selectedFile" class="space-y-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-12 w-12 mx-auto text-gray-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
                <div class="text-center">
                  <!-- No file selected -->
                  <div v-if="!file">
                    <p class="text-gray-600">
                      <span class="text-defaultGreen font-semibold"
                        >Upload a file</span
                      >
                      or drag and drop, or
                      <button
                        type="button"
                        @click.stop="$refs.fileInput.click()"
                        class="text-defaultGreen hover:text-green-700 font-semibold underline"
                      >
                        browse
                      </button>
                    </p>

                    <p class="text-xs text-gray-500 mt-1">
                      Excel / CSV (.xlsx, .xls, .csv) up to 10MB
                    </p>
                  </div>

                  <!-- File selected -->
                  <p v-else class="text-defaultGreen font-medium">
                    File uploaded: {{ file.name }}
                  </p>

                  <!-- Hidden file input -->
                  <input
                    type="file"
                    class="hidden"
                    ref="fileInput"
                    @change="handleFileUpload"
                    accept=".csv, .xlsx, .xls"
                  />
                </div>
              </div>

              <div v-else class="space-y-2">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-12 w-12 mx-auto text-defaultGreen"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
                <p class="text-gray-800 font-semibold">
                  {{ selectedFile.name }}
                </p>
                <p class="text-gray-500 text-sm">
                  {{ formatFileSize(selectedFile.size) }}
                </p>
                <button
                  type="button"
                  @click="clearFile"
                  class="text-red-600 hover:text-red-700 text-sm font-semibold"
                >
                  Remove file
                </button>
              </div>
            </div>
          </div>
          <div class="flex w-full justify-center">
            <button class="btn-save-nobg" @click="downloadTemplate">
              Download Template
            </button>
          </div>
          <div class="w-full h-[1px] rounded-md bg-gray-200 mt-4"></div>
          <!-- Progress Bar -->
          <div v-if="uploading" class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-600">Uploading and processing...</span>
              <span class="text-gray-800 font-semibold"
                >{{ uploadProgress }}%</span
              >
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div
                class="bg-green-600 h-2.5 rounded-full transition-all duration-300"
                :style="{ width: uploadProgress + '%' }"
              ></div>
            </div>
          </div>

          <!-- Import Results -->
          <div v-if="importResults" class="space-y-3">
            <!-- Success Results -->
            <div
              v-if="importResults.success > 0"
              class="flex items-center gap-3 rounded-lg border border-green-200 bg-green-50/70 p-4"
            >
              <div
                class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-green-100 text-green-600"
              >
                <icon name="check" class="text-lg" />
              </div>

              <div>
                <p class="text-sm font-semibold text-green-800">
                  Import Successful
                </p>
                <p class="text-xs text-green-700">
                  Successfully imported
                  <span class="font-semibold">{{ importResults.success }}</span>
                  {{ importResults.success === 1 ? "user" : "users" }}.
                </p>
              </div>
            </div>

            <!-- Failed Results -->
            <div
              v-if="importResults.failed > 0"
              class="overflow-hidden rounded-lg border border-red-200 bg-white"
            >
              <!-- Error Header -->
              <div class="flex items-center gap-3 bg-red-50/70 p-4">
                <div
                  class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-red-100 text-red-600"
                >
                  <icon name="circle-close3" class="text-lg" />
                </div>

                <div>
                  <p class="text-sm font-semibold text-red-800">
                    Import Failed
                  </p>
                  <p class="text-xs text-red-700">
                    {{ importResults.failed }}
                    {{ importResults.failed === 1 ? "user" : "users" }}
                    could not be imported.
                  </p>
                </div>
              </div>

              <!-- Error Details -->
              <div class="p-3">
                <p
                  class="mb-2 text-xs font-semibold uppercase tracking-wide text-gray-500"
                >
                  Error Details
                </p>

                <div class="max-h-40 space-y-2 overflow-y-auto pr-1">
                  <div
                    v-for="(error, index) in importResults.errors"
                    :key="index"
                    class="rounded-md border border-red-100 bg-red-50/40 p-3"
                  >
                    <div class="flex items-start justify-between gap-2">
                      <p class="text-xs font-semibold text-gray-700">
                        Row {{ error.row }}
                      </p>

                      <span
                        class="rounded bg-red-100 px-2 py-0.5 text-[10px] font-medium text-red-700"
                      >
                        Failed
                      </span>
                    </div>

                    <p class="mt-1 text-sm text-red-700 break-words">
                      {{ error.error }}
                    </p>

                    <p
                      v-if="error.email"
                      class="mt-2 border-t border-red-100 pt-2 text-xs text-gray-500 break-all"
                    >
                      <span class="font-medium text-gray-600">Email:</span>
                      {{ error.email }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-end gap-3">
            <button type="button" @click="$emit('close')" class="btn-cancel">
              Cancel
            </button>
            <button
              type="button"
              @click="handleImport"
              :disabled="!selectedFile || uploading"
              :class="[
                'btn-save',
                selectedFile && !uploading
                  ? ''
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed',
              ]"
            >
              {{ uploading ? "Importing..." : "Import Users" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";
import axios from "axios";
import { toast } from "vue3-toastify";
import * as XLSX from "xlsx";

export default {
  name: "ImportUsers",
  components: {
    icon,
  },
  data() {
    return {
      selectedFile: null,
      uploading: false,
      uploadProgress: 0,
      dragOver: false,
      importResults: null,
    };
  },
  methods: {
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file && file.name.endsWith(".xlsx")) {
        this.selectedFile = file;
        this.importResults = null;
      } else {
        toast.error("Please select a valid XLSX file");
      }
    },
    handleFileDrop(event) {
      this.dragOver = false;
      const file = event.dataTransfer.files[0];
      if (file && file.name.endsWith(".xlsx")) {
        this.selectedFile = file;
        this.importResults = null;
      } else {
        toast.error("Please select a valid XLSX file");
      }
    },
    clearFile() {
      this.selectedFile = null;
      this.importResults = null;
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = "";
      }
    },
    formatFileSize(bytes) {
      if (bytes === 0) return "0 Bytes";
      const k = 1024;
      const sizes = ["Bytes", "KB", "MB", "GB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
    },
    downloadTemplate() {
      // Create sample data
      const templateData = [
        {
          "Last Name": "Acdal",
          "First Name": "April",
          Email: "acdal.april@dnsc.edu.ph",
          Role: "Faculty",
          Program: "BSDRM",
          Designation: "Instructor I",
          Unit: 3,
          "Employment Type": "Full Time",
          Department: "Language and Literature",
          BranchCoordinator: "Main",
        },
      ];

      // Create workbook and worksheet
      const ws = XLSX.utils.json_to_sheet(templateData);
      const wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, "Users");

      // Set column widths
      ws["!cols"] = [
        { wch: 20 },
        { wch: 20 },
        { wch: 35 },
        { wch: 25 },
        { wch: 15 },
        { wch: 25 },
        { wch: 10 },
        { wch: 20 },
      ];

      // Download file
      XLSX.writeFile(wb, "users_import_template.xlsx");
      toast.success("Template downloaded successfully");
    },
    async handleImport() {
      if (!this.selectedFile) {
        toast.error("Please select a file to import");
        return;
      }

      this.uploading = true;
      this.uploadProgress = 0;
      this.importResults = null;

      try {
        const formData = new FormData();
        formData.append("file", this.selectedFile);

        // Simulate progress
        const progressInterval = setInterval(() => {
          if (this.uploadProgress < 90) {
            this.uploadProgress += 10;
          }
        }, 200);

        const response = await axios.post(
          process.env.VUE_APP_API_BASE_URL + "/users/import-users",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          },
        );

        clearInterval(progressInterval);
        this.uploadProgress = 100;

        this.importResults = {
          success: response.data.success,
          failed: response.data.failed,
          errors: response.data.errors || [],
        };

        if (response.data.success > 0) {
          toast.success(
            `Successfully imported ${response.data.success} users!`,
          );
          this.$emit("refresh");
        }

        if (response.data.failed > 0) {
          toast.warning(
            `${response.data.failed} users failed to import. Check details below.`,
          );
        }
      } catch (error) {
        console.error("Import failed:", error);
        toast.error(
          error.response?.data?.message ||
            "Failed to import users. Please try again.",
        );
      } finally {
        this.uploading = false;
      }
    },
  },
};
</script>

<style scoped>
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slideUp {
  animation: slideUp 0.3s ease-out;
}
</style>
