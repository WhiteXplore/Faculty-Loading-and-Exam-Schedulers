<template>
  <div>
    <!-- Header -->
    <!-- <div class="text-sm flex justify-between px-1">
      <div class="text-[13px] text-text mt-4 font-regular">
        Pages /
        <span class="font-semibold text-green-900">
          {{
            user && user.role === "Program Chairperson"
              ? "Faculty Under My Program"
              : "Faculty List"
          }}
        </span>
      </div>
    </div> -->

    <!-- Table Container -->
    <div class="table-container">
      <div class="table-controls">
        <!-- Items per page -->
        <div class="per-page-container">
          <div class="select-wrapper">
            <select
              v-model="itemsPerPage"
              class="select-input"
              @change="changePage(1)"
            >
              <option value="10">10</option>
              <option value="15">15</option>
              <option value="20">20</option>
            </select>

            <div
              class="absolute inset-y-0 right-3 flex items-center pointer-events-none text-defaultGreen"
            >
              <svg
                class="w-4 h-4"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </div>
          </div>

          <span class="text-sm font-medium text-gray-600">Per page</span>
        </div>
        <div class="flex gap-2">
          <div class="flex gap-2">
            <!-- Admin Program Filter -->
            <div
              class="relative w-56"
              ref="programDropdownRef"
              v-if="user?.role === 'Admin'"
            >
              <div
                class="relative flex items-center rounded-xl border border-gray-200 bg-white transition-all duration-200 focus-within:border-defaultGreen focus-within:ring-4 focus-within:ring-green-100"
              >
                <!-- Icon -->
                <div class="absolute left-3 text-gray-400">
                  <svg
                    class="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M4 7h16M4 12h16M4 17h16"
                    />
                  </svg>
                </div>

                <!-- Selected -->
                <button
                  type="button"
                  @click="showProgramDropdown = !showProgramDropdown"
                  class="w-full rounded-xl py-3 pl-10 pr-10 text-left text-sm font-semibold text-gray-700"
                >
                  <span v-if="selectedProgram !== 'all'">
                    {{
                      availablePrograms.find(
                        (p) => Number(p.program_id) === Number(selectedProgram),
                      )?.program_code
                    }}
                  </span>

                  <span v-else class="text-gray-600 font-light">
                    Select All Programs
                  </span>
                </button>

                <!-- Arrow -->
                <button
                  type="button"
                  @click="showProgramDropdown = !showProgramDropdown"
                  class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400 hover:bg-gray-100 hover:text-defaultGreen"
                >
                  <svg
                    class="h-4 w-4 transition-transform duration-200"
                    :class="{ 'rotate-180': showProgramDropdown }"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M19 9l-7 7-7-7"
                    />
                  </svg>
                </button>
              </div>

              <!-- Dropdown -->
              <div
                v-if="showProgramDropdown"
                class="absolute z-[9999] mt-2 w-full overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
              >
                <div class="border-b border-gray-100 px-4 py-3">
                  <p
                    class="text-xs font-semibold uppercase tracking-wide text-gray-400"
                  >
                    Programs
                  </p>
                </div>

                <div class="max-h-[260px] overflow-y-auto p-1.5">
                  <!-- All -->
                  <button
                    @click="selectProgram('all')"
                    class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-defaultGreen hover:text-white"
                    :class="
                      selectedProgram === 'all'
                        ? 'bg-defaultGreen text-white'
                        : ''
                    "
                  >
                    <div>
                      <p class="text-sm">All Programs</p>
                    </div>
                  </button>

                  <!-- Programs -->
                  <button
                    v-for="program in availablePrograms"
                    :key="program.program_id"
                    @click="selectProgram(program.program_id)"
                    class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-defaultGreen hover:text-white"
                    :class="
                      Number(selectedProgram) === Number(program.program_id)
                        ? 'bg-defaultGreen text-white'
                        : ''
                    "
                  >
                    <p class="text-sm">
                      {{ program.program_code }}
                    </p>

                    <svg
                      v-if="
                        Number(selectedProgram) === Number(program.program_id)
                      "
                      class="h-5 w-5 text-defaultGreen"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
            <!-- Search -->
            <div class="search-wrapper">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search faculty..."
                class="search-input"
                @input="changePage(1)"
              />

              <div class="search-icon">
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <circle cx="11" cy="11" r="8" />
                  <path d="M21 21l-4.35-4.35" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Faculty Table -->
      <div class="w-full mt-3 rounded-xl border bg-white overflow-hidden">
        <div class="max-h-[73vh] overflow-y-auto">
          <table class="min-w-full text-sm text-gray-700 border-collapse">
            <thead
              class="bg-defaultGreen text-white sticky top-0 z-10 tracking-wide"
            >
              <tr>
                <th class="px-4 py-3 text-left font-normal w-[15%]">
                  Faculty Name
                </th>
                <th class="px-4 py-3 text-center font-normal w-[8%]">
                  Unit Loads
                </th>

                <th class="px-4 py-3 text-center font-normal w-[15%]">
                  Department
                </th>
                <th class="px-4 py-3 text-center font-normal w-[15%]">
                  Employment Status
                </th>

                <th class="px-4 py-3 text-center font-normal w-[15%]">
                  Branch Coordinator
                </th>
                <th class="px-4 py-3 text-center font-normal w-[20%]">
                  Preferred Time
                </th>
                <th class="px-4 py-3 text-center font-normal w-[16%]">
                  Inter-branch
                </th>
                <th
                  class="px-4 py-3 text-center rounded-tr-lg font-normal w-[10%]"
                >
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="faculty in paginatedData"
                :key="faculty.id"
                class="hover:bg-green-50 transition-all border-t"
              >
                <td class="px-4 py-3">
                  {{ faculty.first_name }} {{ faculty.last_name }}
                </td>
                <td class="px-4 py-3 text-center">
                  {{ faculty.unit_load || "-" }}
                </td>

                <td class="px-4 py-3 text-center">
                  {{
                    faculty.department?.department_id
                      ? faculty.department.department_name
                      : "-"
                  }}
                </td>

                <td class="px-4 py-3 text-center">
                  <span
                    :class="{
                      'border border-green-600 text-green-800':
                        faculty.employment_type === 'Permanent',

                      'border border-blue-600 text-blue-800':
                        faculty.employment_type === 'Temporary',

                      'border border-purple-600 text-purple-800':
                        faculty.employment_type === 'Contract of Service',

                      'border border-orange-600 text-orange-800':
                        faculty.employment_type === 'Part-Timer',

                      'text-gray-400 border-gray-300': !faculty.employment_type,
                    }"
                    class="text-xs px-2 py-1 rounded-full"
                  >
                    {{ faculty.employment_type || "-" }}
                  </span>
                </td>

                <td class="px-4 py-3 text-center">
                  {{
                    faculty.college_branch?.college_branch_name ||
                    college_branch?.find(
                      (branch) =>
                        Number(branch.college_branch_id) ===
                        Number(
                          faculty.college_branch_id ??
                            faculty.college_branch?.college_branch_id,
                        ),
                    )?.college_branch_name ||
                    "-"
                  }}
                </td>

                <td class="px-4 py-3 text-center">
                  {{ faculty.preffered_time || "-" }}
                </td>

                <td class="px-4 py-3 text-center">
                  <div
                    v-if="facultyBranchesByUser[faculty.id]?.length"
                    class="flex flex-wrap gap-1 justify-center"
                  >
                    <span
                      v-for="(branchName, idx) in facultyBranchesByUser[
                        faculty.id
                      ]"
                      :key="idx"
                      class="border border-green-600 text-green-800 text-xs px-2 py-1 rounded-full"
                    >
                      {{ branchName }}
                    </span>
                  </div>

                  <span v-else class="text-gray-400">-</span>
                </td>

                <td
                  class="px-4 py-3 flex items-center justify-center relative"
                  :class="{ 'z-50': openActionMenuId === faculty.id }"
                >
                  <div class="per-page-container">
                    <!-- See Details -->
                    <button
                      class="btn-see-details"
                      @click="toggleView(faculty)"
                    >
                      See Details
                    </button>

                    <!-- Three dots button -->
                    <button
                      class="w-5.5 h-8 rounded-md border border-gray-300 flex items-center justify-center hover:bg-gray-100"
                      @click.stop="toggleActionMenu(faculty.id)"
                    >
                      <icon name="3dots" class="rotate-90" />
                    </button>
                  </div>

                  <!-- Dropdown actions with overlay positioning -->
                  <div
                    v-if="openActionMenuId === faculty.id"
                    @mouseleave="openActionMenuId = null"
                    :class="[
                      'absolute right-0 z-[99999] w-40 bg-white border border-gray-200 rounded-lg shadow-xl p-2 space-y-0.5',
                      paginatedData.length === 1
                        ? 'bottom-0 top-auto'
                        : 'top-12 bottom-auto',
                    ]"
                  >
                    <!-- Update -->
                    <button
                      class="w-full flex gap-2 items-center text-left px-2 py-2 hover:bg-green-50 rounded-md text-xs"
                      @click="handleAction('update', faculty)"
                    >
                      <icon
                        name="edit"
                        class="rounded-lg bg-defaultGreen text-white p-1"
                      />
                      Update
                    </button>

                    <!-- Assign -->
                    <button
                      class="w-full flex gap-2 items-center text-left px-2 py-2 hover:bg-green-50 rounded-md text-xs"
                      @click="handleAction('assign', faculty)"
                    >
                      <icon
                        name="edit"
                        class="rounded-lg bg-defaultGreen text-white p-1"
                      />
                      Assign
                    </button>
                  </div>
                </td>
              </tr>

              <tr v-if="paginatedData.length === 0">
                <td colspan="6" class="text-center py-8 text-gray-400">
                  No faculty found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div class="flex justify-between items-center mt-4">
        <div class="text-gray-700 text-sm">
          Showing {{ startIndex }} to {{ endIndex }} of
          {{ filteredData.length }} faculty
        </div>

        <div class="flex items-center gap-1 text-sm">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-l-md hover:bg-gray-400 disabled:opacity-50"
          >
            &lt;
          </button>

          <span v-for="page in pageNumbers" :key="'page-' + page">
            <button
              @click="changePage(page)"
              :class="{
                'bg-defaultGreen text-white': currentPage === page,
                'bg-gray-200 text-gray-700': currentPage !== page,
              }"
              class="px-3 py-1 rounded-md hover:bg-green-300"
            >
              {{ page }}
            </button>
          </span>

          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 bg-gray-300 text-gray-700 rounded-r-md hover:bg-gray-400 disabled:opacity-50"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Update Modal -->
  <div v-if="showAddModal" class="modal-overlay">
    <div class="rounded-[16px] shadow-lg animate-slideUp">
      <form
        @submit.prevent="submitData"
        class="w-[34vw] bg-white text-[13px] rounded-[16px] shadow-lg"
      >
        <!-- Header -->
        <div class="modal-header">
          <div class="flex items-center gap-3">
            <!-- Glass Icon -->
            <div class="glass-container">
              <icon name="user-account3" class="text-white" />
            </div>

            <!-- Title -->
            <div>
              <h2 class="text-lg font-semibold text-white">Update Faculty</h2>

              <p class="text-xs text-green-100">
                Review and update faculty information and assignment details
              </p>
            </div>
          </div>

          <!-- Close Button -->
          <icon
            :name="'circle-close3'"
            @click="closeUpdateModal"
            class="close-button-header"
          />
        </div>

        <!-- Body -->
        <div class="px-4 py-3 space-y-4 text-sm">
          <!-- Faculty Fixed Info -->
          <div class="rounded-xl bg-gray-50 p-4">
            <div class="space-y-3">
              <div>
                <p class="text-xs text-gray-500">Faculty</p>
                <p class="font-medium text-gray-900">
                  {{ selectedFaculty?.first_name }}
                  {{ selectedFaculty?.last_name }}
                </p>
              </div>

              <div>
                <p class="text-xs text-gray-500">Institute</p>
                <p class="font-medium text-gray-900">
                  {{ selectedFaculty?.institute?.institute_name || "N/A" }}
                </p>
              </div>

              <div>
                <p class="text-xs text-gray-500">Program</p>
                <p class="font-medium text-gray-900">
                  {{ selectedFaculty?.program?.program_name || "N/A" }}
                </p>
              </div>
            </div>
          </div>

          <!-- Active Tabs -->
          <div class="flex bg-gray-100 p-1 rounded-xl border">
            <button
              type="button"
              @click="activeUpdateTab = 'faculty'"
              :class="
                activeUpdateTab === 'faculty'
                  ? 'bg-defaultGreen text-white shadow'
                  : 'text-gray-600 hover:bg-white'
              "
              class="flex-1 py-3 rounded-lg text-xs font-semibold transition"
            >
              Faculty Information
            </button>

            <button
              type="button"
              @click="activeUpdateTab = 'preferred'"
              :class="
                activeUpdateTab === 'preferred'
                  ? 'bg-defaultGreen text-white shadow'
                  : 'text-gray-600 hover:bg-white'
              "
              class="flex-1 py-2 rounded-lg text-xs font-semibold transition"
            >
              Preferred
            </button>
          </div>

          <!-- Faculty Information Tab -->
          <div v-if="activeUpdateTab === 'faculty'" class="space-y-3">
            <div class="w-full space-y-2 text-left flex flex-col">
              <label class="input-label">Designation:</label>

              <input
                v-model="form.designation"
                class="input-text"
                placeholder="Enter designation"
              />
            </div>

            <div class="w-full space-y-2 text-left flex flex-col">
              <label class="input-label">Unit Load:</label>

              <input
                v-model.number="form.unit_load"
                type="number"
                min="0"
                step="0.25"
                class="input-text"
                placeholder="Enter unit load"
              />
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Role -->
              <div class="flex flex-col space-y-2 w-full">
                <label class="input-label">Role:</label>
                <select v-model="form.role" class="input-text cursor-pointer">
                  <option disabled value="">-- Select Role --</option>
                  <option value="Faculty">Faculty</option>
                  <option value="Program Chairperson">
                    Program Chairperson
                  </option>
                  <option value="Admin">Admin</option>
                </select>
              </div>

              <!-- Employment Type -->
              <div class="flex flex-col space-y-2 w-full">
                <label class="input-label">Employment Type:</label>
                <select
                  v-model="form.employment_type"
                  class="input-text cursor-pointer"
                >
                  <option disabled value="">Select Employment Type</option>
                  <option value="Permanent">Permanent</option>
                  <option value="Temporary">Temporary</option>
                  <option value="Contract of Service">
                    Contract of Service
                  </option>
                  <option value="Part Time">Part Time</option>
                </select>
              </div>
            </div>
            <!-- Department -->

            <div class="flex flex-col space-y-2 w-full">
              <label class="input-label">Department:</label>

              <select
                v-model.number="form.department_id"
                class="input-text cursor-pointer"
              >
                <option :value="null">No Department</option>

                <option
                  v-for="department in departments || []"
                  :key="department.department_id"
                  :value="Number(department.department_id)"
                >
                  {{ department.department_name }}
                </option>
              </select>
            </div>
          </div>

          <!-- Preferred Tab -->
          <div v-if="activeUpdateTab === 'preferred'" class="space-y-4">
            <!-- Update Mode Selection -->
            <div class="space-y-2 text-[13px] text-gray-600">
              <label class="font-normal block mb-1">Select Update Type</label>

              <select
                v-model="updateMode"
                class="w-full border px-3 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-green-600 cursor-pointer font-normal"
              >
                <option disabled value="">-- Select Option --</option>
                <option value="preffered_time">Preferred Time</option>
                <option value="interbranch">Inter-branch</option>
                <option value="all">All (Preferred Time + Inter-branch)</option>
              </select>
            </div>

            <!-- Preferred Time Section -->
            <div
              v-if="updateMode === 'preffered_time' || updateMode === 'all'"
              class="space-y-3"
            >
              <div
                v-if="formattedSlot"
                class="bg-green-50 p-3 rounded-lg border border-green-200 space-y-2"
              >
                <p class="font-semibold">Selected Time Slot:</p>
                <p>{{ formattedSlot }}</p>
                <p>Total Hours: {{ totalHours }} hrs</p>
              </div>

              <!-- Morning -->
              <div class="rounded-lg space-y-3">
                <h3 class="font-normal text-green-800 text-sm">
                  Morning Schedule
                </h3>

                <div class="flex gap-4">
                  <div class="flex-1">
                    <label class="font-normal block mb-1">Start</label>
                    <input
                      type="time"
                      v-model="form.morningStart"
                      class="w-full border px-3 py-2 rounded-md"
                    />
                  </div>

                  <div class="flex-1">
                    <label class="font-normal block mb-1">End</label>
                    <input
                      type="time"
                      v-model="form.morningEnd"
                      class="w-full border px-3 py-2 rounded-md"
                    />
                  </div>
                </div>
              </div>

              <!-- Afternoon -->
              <div class="rounded-lg space-y-3">
                <h3 class="font-normal text-green-800 text-sm">
                  Afternoon Schedule
                </h3>

                <div class="flex gap-4">
                  <div class="flex-1">
                    <label class="font-normal block mb-1">Start</label>
                    <input
                      type="time"
                      v-model="form.afternoonStart"
                      class="w-full border px-3 py-2 rounded-md"
                    />
                  </div>

                  <div class="flex-1">
                    <label class="font-normal block mb-1">End</label>
                    <input
                      type="time"
                      v-model="form.afternoonEnd"
                      class="w-full border px-3 py-2 rounded-md"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Interbranch Section -->
            <div
              v-if="updateMode === 'interbranch' || updateMode === 'all'"
              class="space-y-3 text-[13px]"
            >
              <label class="font-normal block mb-1">
                Select Inter-branch Campus
              </label>

              <div class="relative">
                <button
                  type="button"
                  @click="showBranchDropdown = !showBranchDropdown"
                  class="w-full border px-3 py-2 rounded-md bg-white text-left flex justify-between items-center font-normal"
                >
                  <span v-if="form.interbranchCampus.length">
                    {{ form.interbranchCampus.length }} campus(es) selected
                  </span>
                  <span v-else class="text-gray-400">Select campuses</span>
                  <span>▾</span>
                </button>

                <div
                  v-if="showBranchDropdown"
                  @mouseleave="showBranchDropdown = false"
                  class="absolute z-50 mt-1 w-full bg-white border rounded-md shadow-lg max-h-60 overflow-y-auto"
                >
                  <label
                    v-for="branch in college_branch"
                    :key="branch.college_branch_id"
                    class="flex items-center gap-2 px-3 py-2 hover:bg-gray-100 cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      :value="branch.college_branch_id"
                      :checked="
                        form.interbranchCampus.includes(
                          branch.college_branch_id,
                        )
                      "
                      @change="toggleBranch(branch.college_branch_id)"
                    />
                    {{ branch.college_branch_name }}
                  </label>
                </div>
              </div>

              <p class="input-label">You can select multiple campuses.</p>

              <div
                v-if="form.interbranchCampus.length"
                class="flex flex-wrap gap-2 mt-2"
              >
                <div
                  v-for="id in form.interbranchCampus"
                  :key="id"
                  class="flex items-center gap-2 bg-defaultGreen text-white px-3 py-1 rounded-md text-[13px] font-normal"
                >
                  {{
                    college_branch.find((b) => b.college_branch_id === id)
                      ?.college_branch_name
                  }}

                  <button
                    type="button"
                    @click="removeBranch(id)"
                    class="text-white hover:text-red-600"
                  >
                    <icon name="delete" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Buttons -->
          <div class="flex justify-end gap-2 pt-3">
            <button type="button" @click="closeUpdateModal" class="btn-cancel">
              Cancel
            </button>

            <button type="submit" class="btn-save">Save Changes</button>
          </div>
        </div>
      </form>
    </div>
  </div>

  <!-- View Modal -->
  <div v-if="showViewModal" class="modal-overlay">
    <div class="w-full h-screen rounded-2xl bg-white shadow-xl overflow-hidden">
      <!-- Header -->
      <div class="modal-header">
        <div class="flex items-center gap-3">
          <!-- Glass Icon -->
          <div class="glass-container">
            <icon name="user-account3" class="text-white" />
          </div>

          <!-- Title -->
          <div>
            <h2 class="text-lg font-semibold text-white">
              Faculty Information
            </h2>

            <p class="text-xs text-green-100">
              Review faculty details, qualifications, and expertise information
            </p>
          </div>
        </div>

        <!-- Close Button -->
        <icon
          :name="'circle-close3'"
          @click="showViewModal = false"
          class="cursor-pointer text-white hover:bg-white/20 rounded-full p-2 duration-300 ease-in-out"
        />
      </div>

      <div
        v-if="selectedFaculty"
        class="p-6 space-y-6 max-h-[85vh] overflow-y-auto"
      >
        <!-- Faculty Overview -->

        <!-- Faculty Profile Overview -->
        <div
          class="overflow-hidden rounded-2xl border border-gray-200 bg-white shadow-sm"
        >
          <!-- Profile Header -->
          <div
            class="relative overflow-hidden border-b border-gray-100 p-5 sm:p-6 bg-gradient-to-r from-defaultGreen/10 via-white to-defaultGreen/10"
          >
            <div class="flex flex-col gap-4 sm:flex-row sm:items-center">
              <!-- Faculty Avatar -->
              <div
                class="flex h-24 w-24 shrink-0 items-center justify-center overflow-hidden rounded-2xl border-4 border-white bg-green-50 text-2xl font-bold text-green-800 shadow-sm"
              >
                <img
                  v-if="
                    selectedFaculty.profile_image_url ||
                    selectedFaculty.profile_image
                  "
                  :src="
                    selectedFaculty.profile_image_url ||
                    selectedFaculty.profile_image
                  "
                  :alt="`${selectedFaculty.first_name} ${selectedFaculty.last_name}`"
                  class="h-full w-full object-cover"
                  @error="$event.target.style.display = 'none'"
                />

                <span v-else>
                  {{ selectedFaculty.first_name?.charAt(0) || ""
                  }}{{ selectedFaculty.last_name?.charAt(0) || "" }}
                </span>
              </div>

              <!-- Faculty Name -->
              <div class="min-w-0 flex-1">
                <p
                  class="mb-1 text-[10px] font-semibold uppercase tracking-[0.2em] text-green-700"
                >
                  Faculty Profile
                </p>

                <h3
                  class="text-xl font-bold tracking-tight text-gray-900 sm:text-2xl"
                >
                  {{ selectedFaculty.first_name }}
                  {{ selectedFaculty.last_name }}
                </h3>

                <p class="mt-1 text-sm text-gray-500">
                  {{ selectedFaculty.designation || "Faculty Member" }}
                </p>

                <div class="mt-3 flex flex-wrap gap-2">
                  <span
                    class="inline-flex items-center gap-1.5 rounded-full border border-green-200 bg-green-50 px-3 py-1 text-xs font-medium text-green-800"
                  >
                    <span class="h-1.5 w-1.5 rounded-full bg-green-600"></span>
                    {{
                      selectedFaculty.employment_type || "Employment not set"
                    }}
                  </span>

                  <span
                    class="inline-flex items-center gap-1.5 rounded-full border border-gray-200 bg-white px-3 py-1 text-xs font-medium text-gray-600"
                  >
                    {{ selectedFaculty.unit_load ?? 0 }} Unit Load
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Faculty Details -->
          <div class="p-4 sm:p-5">
            <div class="mb-4 flex items-center gap-2">
              <div
                class="flex h-8 w-8 items-center justify-center rounded-lg bg-green-100 text-green-800"
              >
                <icon name="user-account" />
              </div>
              <div>
                <h4 class="text-sm font-semibold text-gray-800">
                  Faculty Information
                </h4>
                <p class="text-xs text-gray-400">
                  Academic assignment and employment details
                </p>
              </div>
            </div>

            <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-2">
              <!-- Institute -->
              <div
                class="rounded-xl border border-gray-100 bg-gray-50/70 p-3.5"
              >
                <div class="mb-2 flex items-center gap-2 text-gray-400">
                  <span class="text-xs font-medium">Institute</span>
                </div>
                <p class="text-sm font-semibold leading-relaxed text-gray-800">
                  {{ selectedFaculty.institute?.institute_name || "N/A" }}
                </p>
              </div>

              <!-- Department -->
              <div
                class="rounded-xl border border-gray-100 bg-gray-50/70 p-3.5"
              >
                <div class="mb-2 flex items-center gap-2 text-gray-400">
                  <span class="text-xs font-medium">Department</span>
                </div>
                <p class="text-sm font-semibold leading-relaxed text-gray-800">
                  {{
                    (selectedFaculty.department?.department_id,
                    selectedFaculty.department?.department_name || "N/A")
                  }}
                </p>
              </div>

              <!-- Program -->
              <div
                class="rounded-xl border border-gray-100 bg-gray-50/70 p-3.5"
              >
                <div class="mb-2 flex items-center gap-2 text-gray-400">
                  <span class="text-xs font-medium">Program</span>
                </div>
                <p class="text-sm font-semibold leading-relaxed text-gray-800">
                  {{ selectedFaculty.program?.program_name || "N/A" }}
                </p>
              </div>

              <!-- Designation -->
              <div
                class="rounded-xl border border-gray-100 bg-gray-50/70 p-3.5"
              >
                <div class="mb-2 flex items-center gap-2 text-gray-400">
                  <span class="text-xs font-medium">Designation</span>
                </div>
                <p class="text-sm font-semibold leading-relaxed text-gray-800">
                  {{ selectedFaculty.designation || "N/A" }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Expertise Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <!-- Expertise -->
          <div
            class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm hover:shadow-md transition"
          >
            <div class="flex items-center gap-2 mb-5">
              <div
                class="w-8 h-8 rounded-xl bg-defaultGreen flex items-center justify-center shadow-sm"
              >
                <svg
                  class="w-5 h-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12h6m-6 4h6M7 4h10a2 2 0 012 2v12a2 2 0 01-2 2H7a2 2 0 01-2-2V6a2 2 0 012-2z"
                  />
                </svg>
              </div>

              <h3 class="text-sm font-semibold text-gray-800">Expertise</h3>
            </div>

            <div
              v-if="filteredExpertise.primary.length"
              class="space-y-5 text-sm"
            >
              <div
                v-for="(group, key) in groupByYearSemester(
                  filteredExpertise.primary,
                )"
                :key="key"
              >
                <p class="text-xs font-semibold text-green-700 mb-3">
                  {{ key }}
                </p>

                <ul class="space-y-2">
                  <li
                    v-for="(exp, i) in group"
                    :key="i"
                    class="flex items-start gap-2 text-gray-700"
                  >
                    <span class="w-2 h-2 rounded-full bg-green-500 mt-2"></span>

                    <span>
                      {{ exp.course?.course_code }} -
                      {{ exp.course?.course_title }}
                    </span>
                  </li>
                </ul>
              </div>
            </div>

            <p v-else class="text-xs font-light text-gray-400 italic">
              No expertise added
            </p>
          </div>

          <!-- Other Expertise -->
          <div
            class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm hover:shadow-md transition"
          >
            <div class="flex items-center gap-2 mb-5">
              <div
                class="w-8 h-8 rounded-xl bg-defaultGreen flex items-center justify-center shadow-sm"
              >
                <svg
                  class="w-5 h-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8v4l3 3"
                  />
                </svg>
              </div>

              <h3 class="text-sm font-semibold text-gray-800">
                Other Expertise
              </h3>
            </div>

            <div
              v-if="filteredExpertise.other.length"
              class="space-y-5 text-sm"
            >
              <div
                v-for="(group, key) in groupByYearSemester(
                  filteredExpertise.other,
                )"
                :key="key"
              >
                <p class="text-xs font-semibold text-orange-600 mb-3">
                  {{ key }}
                </p>

                <ul class="space-y-2">
                  <li
                    v-for="(exp, i) in group"
                    :key="i"
                    class="flex items-start gap-2 text-gray-700"
                  >
                    <span
                      class="w-2 h-2 rounded-full bg-orange-500 mt-2"
                    ></span>

                    <span>
                      {{ exp.course?.course_code }} -
                      {{ exp.course?.course_title }}
                    </span>
                  </li>
                </ul>
              </div>
            </div>

            <p v-else class="text-xs font-light text-gray-400 italic">
              No other expertise added
            </p>
          </div>

          <!-- Cross Expertise -->
          <div
            class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm hover:shadow-md transition"
          >
            <div class="flex items-center gap-2 mb-5">
              <div
                class="w-8 h-8 rounded-xl bg-defaultGreen flex items-center justify-center shadow-sm"
              >
                <svg
                  class="w-5 h-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M8 9l4-4 4 4m0 6l-4 4-4-4"
                  />
                </svg>
              </div>

              <h3 class="text-sm font-semibold text-gray-800">
                Cross Expertise
              </h3>
            </div>

            <div
              v-if="filteredExpertise.cross.length"
              class="space-y-5 text-sm"
            >
              <div
                v-for="(group, key) in groupByYearSemester(
                  filteredExpertise.cross,
                )"
                :key="key"
              >
                <p class="text-xs font-semibold text-blue-600 mb-3">
                  {{ key }}
                </p>

                <ul class="space-y-2">
                  <li
                    v-for="(exp, i) in group"
                    :key="i"
                    class="flex items-start gap-2 text-gray-700"
                  >
                    <span class="w-2 h-2 rounded-full bg-blue-500 mt-2"></span>

                    <span>
                      {{ exp.course?.course_code }} -
                      {{ exp.course?.course_title }}
                    </span>
                  </li>
                </ul>
              </div>
            </div>

            <p v-else class="text-xs font-light text-gray-400 italic">
              No cross expertise assigned
            </p>
          </div>
        </div>

        <!-- Additional Info -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <!-- Preferred Time -->
          <div
            class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm hover:shadow-md transition"
          >
            <div class="flex items-center gap-2 mb-4">
              <div
                class="w-8 h-8 rounded-xl bg-defaultGreen flex items-center justify-center shadow-sm"
              >
                <svg
                  class="w-5 h-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>

              <h3 class="text-sm font-semibold text-gray-800">
                Preferred Time
              </h3>
            </div>

            <p
              v-if="selectedFaculty.preffered_time"
              class="text-sm text-gray-700"
            >
              {{ selectedFaculty.preffered_time }}
            </p>

            <p v-else class="text-xs font-light text-gray-400 italic">
              No preferred time set
            </p>
          </div>

          <!-- Inter-branch -->
          <div
            class="bg-white border border-gray-100 rounded-2xl p-4 shadow-sm hover:shadow-md transition"
          >
            <div class="flex items-center gap-2 mb-4">
              <div
                class="w-8 h-8 rounded-xl bg-defaultGreen flex items-center justify-center shadow-sm"
              >
                <svg
                  class="w-5 h-5 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M17.657 16.657L13.414 20.9a2 2 0 01-2.828 0l-4.243-4.243a8 8 0 1111.314 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                </svg>
              </div>

              <h3 class="text-sm font-semibold text-gray-800">
                Inter-branch Campuses
              </h3>
            </div>

            <div
              v-if="
                selectedFaculty.faculty_branches &&
                selectedFaculty.faculty_branches.length
              "
              class="flex flex-wrap gap-2"
            >
              <span
                v-for="(branchName, i) in selectedFaculty.faculty_branches"
                :key="i"
                class="px-3 py-1.5 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-100"
              >
                {{ branchName }}
              </span>
            </div>

            <p v-else class="text-xs font-light text-gray-400 italic">
              No inter-branch campuses
            </p>
          </div>
        </div>

        <!-- Footer -->
        <div class="flex justify-end pt-2">
          <button @click="showViewModal = false" class="btn-cancel">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>

  <addExpertise
    v-if="showExpertiseModal"
    :userData="selectedFaculty"
    :mode="modalMode"
    @close="showExpertiseModal = false"
    @updated="loadUsers"
  />
</template>

<script>
import icon from "@/assets/icon.vue";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import { mapState } from "pinia";
import axios from "axios";
import addExpertise from "../modals/add-expertise.vue";

export default {
  name: "TableFaculty",
  components: { icon, addExpertise },

  data() {
    return {
      currentPage: 1,
      itemsPerPage: 10,
      searchQuery: "",
      isTable: true,

      selectedFaculty: null,
      showViewModal: false,
      showAddModal: false,
      showExpertiseModal: false,

      user: null,
      openActionMenuId: null,
      modalMode: "",

      activeUpdateTab: "faculty",

      form: {
        designation: "",
        unit_load: null,
        role: "",
        employment_type: "",
        department_id: null,
        morningStart: "",
        morningEnd: "",
        afternoonStart: "",
        afternoonEnd: "",
        interbranchCampus: [],
      },

      updateMode: "",
      showBranchDropdown: false,
      facultyBranches: [],
      selectedProgram: "all",
      showProgramDropdown: false,
    };
  },

  computed: {
    ...mapState(useFetchDataStore, [
      "rawusers",
      "college_branch",
      "faculty_branch",
      "programs",
      "departments",
    ]),
    availablePrograms() {
      return this.programs || [];
    },
    filteredExpertise() {
      const list = this.selectedFaculty?.expertise || [];

      return {
        primary: list.filter((e) => e.status === "PRIMARY"),
        other: list.filter((e) => e.status === "OTHER"),
        cross: list.filter((e) => e.status === "CROSS"),
      };
    },

    facultyBranchesByUser() {
      const map = {};

      (this.faculty_branch || []).forEach((fb) => {
        const uid = fb.user?.id;
        const branchName = fb.collegeBranch?.college_branch_name;

        if (!uid || !branchName) return;

        if (!map[uid]) map[uid] = [];
        map[uid].push(branchName);
      });

      return map;
    },

    totalHours() {
      let total = 0;

      const calc = (start, end) => {
        if (!start || !end) return 0;

        const s = new Date(`1970-01-01T${start}`);
        const e = new Date(`1970-01-01T${end}`);

        if (isNaN(s) || isNaN(e)) return 0;

        return (e - s) / (1000 * 60 * 60);
      };

      total += calc(this.form.morningStart, this.form.morningEnd);
      total += calc(this.form.afternoonStart, this.form.afternoonEnd);

      return total;
    },

    formattedSlot() {
      const parts = [];

      if (this.form.morningStart && this.form.morningEnd) {
        parts.push(
          `${this.formatTo12(this.form.morningStart)} - ${this.formatTo12(
            this.form.morningEnd,
          )}`,
        );
      }

      if (this.form.afternoonStart && this.form.afternoonEnd) {
        parts.push(
          `${this.formatTo12(this.form.afternoonStart)} - ${this.formatTo12(
            this.form.afternoonEnd,
          )}`,
        );
      }

      return parts.join(" , ");
    },

    filteredData() {
      const query = (this.searchQuery || "").toLowerCase();
      const currentUser = this.user;

      if (!this.rawusers || !currentUser) return [];

      let list = [];

      // ==========================
      // ADMIN
      // ==========================
      if (currentUser.role === "Admin") {
        const allowedRoles = [
          "Faculty",
          "Program Chairperson",
          "Department Chairperson",
          "Coordinator",
        ];

        list = this.rawusers.filter((u) => allowedRoles.includes(u.role));

        // Program filter
        if (this.selectedProgram !== "all") {
          list = list.filter(
            (u) =>
              Number(u.program?.program_id ?? u.program_id) ===
              Number(this.selectedProgram),
          );
        }
      }

      // ==========================
      // PROGRAM CHAIRPERSON
      // ==========================
      else if (currentUser.role === "Program Chairperson") {
        const programId =
          currentUser.program?.program_id ?? currentUser.program_id;

        const instituteId =
          currentUser.institute?.institute_id ?? currentUser.institute_id;

        list = this.rawusers.filter(
          (u) =>
            u.role === "Faculty" &&
            Number(u.program?.program_id ?? u.program_id) ===
              Number(programId) &&
            Number(u.institute?.institute_id ?? u.institute_id) ===
              Number(instituteId),
        );
      }

      // ==========================
      // DEPARTMENT CHAIRPERSON
      // ==========================
      else if (currentUser.role === "Department Chairperson") {
        const departmentId =
          currentUser.department?.department_id ?? currentUser.department_id;

        list = this.rawusers.filter(
          (u) =>
            u.role === "Faculty" &&
            departmentId != null &&
            Number(u.department?.department_id ?? u.department_id) ===
              Number(departmentId),
        );
      }

      // ==========================
      // SEARCH FILTER
      // ==========================
      return list.filter((u) =>
        [
          `${u.first_name || ""} ${u.last_name || ""}`,
          u.program?.program_name || "",
          u.program?.program_code || "",
          u.institute?.institute_name || "",
          u.department?.department_name || "",
          u.college_branch?.college_branch_name || "",
          u.designation || "",
          u.role || "",
          u.employment_type || "",
        ]
          .join(" ")
          .toLowerCase()
          .includes(query),
      );
    },

    totalPages() {
      return Math.ceil(this.filteredData.length / this.itemsPerPage) || 1;
    },

    paginatedData() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      return this.filteredData.slice(start, start + Number(this.itemsPerPage));
    },

    startIndex() {
      return this.filteredData.length === 0
        ? 0
        : (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      const end = this.currentPage * this.itemsPerPage;
      return end > this.filteredData.length ? this.filteredData.length : end;
    },

    pageNumbers() {
      const total = this.totalPages;

      if (total <= 3) {
        return Array.from({ length: total }, (_, i) => i + 1);
      }

      let start = this.currentPage - 1;
      let end = this.currentPage + 1;

      if (start < 1) {
        start = 1;
        end = 3;
      }

      if (end > total) {
        end = total;
        start = total - 2;
      }

      return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    },
  },

  methods: {
    selectProgram(programId) {
      this.selectedProgram = programId;
      this.showProgramDropdown = false;
      this.changePage(1);
    },
    toggleActionMenu(userId) {
      this.openActionMenuId = this.openActionMenuId === userId ? null : userId;
    },

    handleAction(action, user) {
      this.openActionMenuId = null;

      if (action === "update") {
        this.openAddModal(user);
      } else if (action === "assign") {
        this.openAssignModal(user);
      } else if (action === "cross") {
        this.openCrossAssignModal(user);
      }
    },
    groupByYearSemester(list) {
      const grouped = {};

      const formatYear = (year) => {
        if (!year) return "N/A Year";

        const suffix =
          year == 1
            ? "1st"
            : year == 2
            ? "2nd"
            : year == 3
            ? "3rd"
            : `${year}th`;

        return `${suffix} Year`;
      };

      const formatSem = (sem) => {
        if (!sem) return "N/A Semester";

        const suffix =
          sem == 1 ? "1st" : sem == 2 ? "2nd" : sem == 3 ? "3rd" : `${sem}th`;

        return `${suffix} Semester`;
      };

      (list || []).forEach((item) => {
        const year = item.course?.course_level;
        const sem = item.course?.course_semester;
        const key = `${formatYear(year)} • ${formatSem(sem)}`;

        if (!grouped[key]) grouped[key] = [];
        grouped[key].push(item);
      });

      return grouped;
    },

    convertTo24(time12) {
      if (!time12) return "";

      const clean = time12.replace(/\s+/g, "").toUpperCase();
      const match = clean.match(/(\d{1,2}):(\d{2})(AM|PM)/);

      if (!match) return "";

      let hours = parseInt(match[1]);
      const minutes = match[2];
      const modifier = match[3];

      if (modifier === "PM" && hours !== 12) hours += 12;
      if (modifier === "AM" && hours === 12) hours = 0;

      return `${hours.toString().padStart(2, "0")}:${minutes}`;
    },

    formatTo12(time) {
      if (!time) return "";

      const [hour, minute] = time.split(":");
      let h = parseInt(hour);

      const ampm = h >= 12 ? "PM" : "AM";
      h = h % 12 || 12;

      return `${h}:${minute.padStart(2, "0")} ${ampm}`;
    },

    toggleBranch(id) {
      const index = this.form.interbranchCampus.indexOf(id);

      if (index > -1) {
        this.form.interbranchCampus.splice(index, 1);
      } else {
        this.form.interbranchCampus.push(id);
      }
    },

    removeBranch(id) {
      this.form.interbranchCampus = this.form.interbranchCampus.filter(
        (branchId) => branchId !== id,
      );
    },

    async loadUsers() {
      const store = useFetchDataStore();
      console.log("FACULTY DATA:", store.rawusers);
      console.log("COLLEGE BRANCHES:", store.college_branch);
      await store.fetchRawUsers();
      await store.fetchFacultyBranch();
      await store.fetchPrograms();
      await store.fetchDepartments();
      await store.fetchCollegeBranch();
    },

    openAssignModal(user) {
      this.selectedFaculty = user;
      this.modalMode = "assign";
      this.showExpertiseModal = true;
    },

    openCrossAssignModal(user) {
      this.selectedFaculty = user;
      this.modalMode = "cross";
      this.showExpertiseModal = true;
    },

    openAddModal(user) {
      this.selectedFaculty = user;
      this.activeUpdateTab = "faculty";

      this.form = {
        designation: user.designation || "",
        unit_load: user.unit_load ?? null,
        role: user.role || "",
        employment_type: user.employment_type || "",
        department_id:
          user.department?.department_id != null
            ? Number(user.department.department_id)
            : null,
        morningStart: "",
        morningEnd: "",
        afternoonStart: "",
        afternoonEnd: "",
        interbranchCampus: [],
      };

      if (user.preffered_time) {
        const parts = user.preffered_time.split(",");

        parts.forEach((slot, index) => {
          const [rawStart, rawEnd] = slot.trim().split(" - ");

          if (!rawStart || !rawEnd) return;

          const start24 = this.convertTo24(rawStart.trim());
          const end24 = this.convertTo24(rawEnd.trim());

          if (index === 0) {
            this.form.morningStart = start24;
            this.form.morningEnd = end24;
          } else if (index === 1) {
            this.form.afternoonStart = start24;
            this.form.afternoonEnd = end24;
          }
        });
      }

      this.form.interbranchCampus = (this.faculty_branch || [])
        .filter((fb) => fb.user?.id === user.id)
        .map((fb) => fb.collegeBranch?.college_branch_id)
        .filter(Boolean);

      if (user.preffered_time && this.form.interbranchCampus.length) {
        this.updateMode = "all";
      } else if (user.preffered_time) {
        this.updateMode = "preffered_time";
      } else if (this.form.interbranchCampus.length) {
        this.updateMode = "interbranch";
      } else {
        this.updateMode = "";
      }

      this.showAddModal = true;
    },

    closeUpdateModal() {
      this.showAddModal = false;
      this.showBranchDropdown = false;
      this.activeUpdateTab = "faculty";
      this.updateMode = "";
    },

    toggleView(user) {
      this.selectedFaculty = {
        ...user,
        faculty_branches: this.facultyBranchesByUser[user.id] || [],
      };

      this.showViewModal = true;
    },

    changePage(page) {
      this.currentPage = Math.max(1, Math.min(page, this.totalPages));
    },

    async fetchUser() {
      try {
        const response = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/auth/me",
          {
            withCredentials: true,
          },
        );

        if (response.data) {
          this.user = response.data;
        } else {
          this.$router.push("/");
        }
      } catch (error) {
        console.error("Failed to fetch user:", error);
        this.$router.push("/");
      }
    },

    async submitData() {
      try {
        const userId = this.selectedFaculty.id;

        if (this.activeUpdateTab === "faculty") {
          if (!this.form.role) {
            alert("Please select role.");
            return;
          }

          if (!this.form.employment_type) {
            alert("Please select employment type.");
            return;
          }

          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/users/${userId}`,
            {
              designation: this.form.designation,
              unit_load: this.form.unit_load,
              role: this.form.role,
              employment_type: this.form.employment_type,
              department_id: this.form.department_id,
            },
            { withCredentials: true },
          );

          toast.success("Faculty information updated successfully!");
          this.showAddModal = false;
          await this.loadUsers();
          return;
        }

        if (this.activeUpdateTab === "preferred") {
          if (!this.updateMode) {
            alert("Please select update type.");
            return;
          }

          if (this.updateMode === "preffered_time") {
            if (this.totalHours !== 8) {
              alert("Total time must equal exactly 8 hours.");
              return;
            }

            await axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/users/${userId}`,
              { preffered_time: this.formattedSlot },
              { withCredentials: true },
            );

            toast.success("Preferred time updated successfully!");
            this.showAddModal = false;
            await this.loadUsers();
            return;
          }

          if (this.updateMode === "interbranch") {
            if (!this.form.interbranchCampus.length) {
              alert("Please select at least one inter-branch campus.");
              return;
            }

            await this.updateFacultyBranches(userId);

            toast.success("Inter branch updated successfully!");
            this.showAddModal = false;
            await this.loadUsers();
            return;
          }

          if (this.updateMode === "all") {
            if (this.totalHours !== 8) {
              alert("Total time must equal exactly 8 hours.");
              return;
            }

            await axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/users/${userId}`,
              { preffered_time: this.formattedSlot },
              { withCredentials: true },
            );

            await this.updateFacultyBranches(userId);

            toast.success(
              "Preferred time and Inter Branch updated successfully!",
            );
            this.showAddModal = false;
            await this.loadUsers();
          }
        }
      } catch (error) {
        console.error(error);
        alert("Failed to update data. Check console for details.");
      }
    },

    async updateFacultyBranches(userId) {
      const existingBranches = (this.faculty_branch || []).filter(
        (fb) => fb.user?.id === userId,
      );

      for (const fb of existingBranches) {
        await axios.delete(
          `${process.env.VUE_APP_API_BASE_URL}/faculty-branch/${fb.faculty_branch_id}`,
          { withCredentials: true },
        );
      }

      for (const branchId of this.form.interbranchCampus) {
        await axios.post(
          `${process.env.VUE_APP_API_BASE_URL}/faculty-branch`,
          {
            user_id: userId,
            college_branch_id: branchId,
          },
          { withCredentials: true },
        );
      }
    },
  },

  async mounted() {
    await this.fetchUser();
    await this.loadUsers();

    const store = useFetchDataStore();
    await store.fetchCollegeBranch();
    await store.fetchFacultyBranch();
  },
};
</script>
