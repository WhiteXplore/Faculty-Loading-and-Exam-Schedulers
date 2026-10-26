<template>
  <div class="min-h-screen bg-gray-50 p-2 text-gray-800">
    <!-- =========================================================
         FACULTY ADJUSTMENT / SECTION ASSIGNMENT
    ========================================================== -->
    <div>
      <!-- =======================================================
           COURSE GROUPS
      ======================================================== -->
      <div
        v-if="groupedFaculty.length"
        class="space-y-5 h-[79vh] overflow-y-auto"
      >
        <div
          v-for="item in groupedFaculty"
          :key="item.key"
          class="overflow-hidden rounded-lg border border-gray-200 bg-white"
        >
          <!-- =====================================================
               COURSE HEADER
          ====================================================== -->
          <div class="border-b border-gray-200 bg-gray-50 px-5 py-4">
            <div
              class="flex flex-col gap-4 md:flex-row md:items-start md:justify-between"
            >
              <!-- COURSE INFORMATION -->
              <div>
                <div class="flex items-center gap-2">
                  <h3 class="text-sm font-bold text-gray-900">
                    {{ item.courseCode }}
                  </h3>

                  <span
                    class="rounded bg-gray-100 px-2 py-1 text-[10px] font-bold text-gray-600"
                  >
                    {{ item.programCode }}
                  </span>
                </div>

                <p class="mt-1 max-w-2xl text-xs text-gray-500">
                  {{ item.courseTitle }}
                </p>

                <!-- SECTIONS -->
                <div class="mt-3">
                  <div class="flex flex-wrap items-center gap-2">
                    <span
                      class="text-[10px] font-medium uppercase tracking-wide text-gray-400"
                    >
                      Sections
                    </span>

                    <span
                      v-for="section in item.sections"
                      :key="section.classId"
                      :class="[
                        'rounded px-2 py-1 text-[10px] font-bold ring-1',
                        isSectionAssigned(section.classId, item.courseCode)
                          ? 'bg-green-50 text-green-700 ring-green-200'
                          : 'bg-white text-gray-700 ring-gray-200',
                      ]"
                    >
                      {{ getSectionDisplay(section) }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- COURSE SUMMARY -->
              <div class="flex flex-wrap items-center gap-6">
                <!-- REQUIRED -->
                <div>
                  <p
                    class="text-[10px] font-medium uppercase tracking-wide text-gray-400"
                  >
                    Required
                  </p>

                  <p class="mt-1 text-lg font-bold text-gray-900">
                    {{ item.requiredUnits }}
                  </p>

                  <p class="text-[9px] text-gray-400">total units</p>
                </div>

                <!-- ASSIGNED -->
                <div>
                  <p
                    class="text-[10px] font-medium uppercase tracking-wide text-gray-400"
                  >
                    Assigned
                  </p>

                  <p class="mt-1 text-lg font-bold text-green-600">
                    {{ item.assignedUnits }}
                  </p>

                  <p class="text-[9px] text-gray-400">assigned units</p>
                </div>

                <!-- SECTIONS -->
                <div>
                  <p
                    class="text-[10px] font-medium uppercase tracking-wide text-gray-400"
                  >
                    Sections
                  </p>

                  <p class="mt-1 text-lg font-bold text-gray-900">
                    {{ item.assignedSectionCount }}/{{ item.sections.length }}
                  </p>

                  <p class="text-[9px] text-gray-400">assigned</p>
                </div>
              </div>
            </div>

            <!-- COURSE ACTIONS -->
            <div
              class="mt-4 flex flex-wrap items-center justify-between gap-2 border-t border-gray-200 pt-3"
            >
              <div>
                <span
                  v-if="item.remainingUnits <= 0"
                  class="inline-flex rounded bg-green-100 px-2 py-1 text-[10px] font-bold text-green-700"
                >
                  Fully Assigned
                </span>

                <span
                  v-else-if="item.assignedUnits > 0"
                  class="inline-flex rounded bg-yellow-100 px-2 py-1 text-[10px] font-bold text-yellow-700"
                >
                  Partially Assigned
                </span>

                <span
                  v-else
                  class="inline-flex rounded bg-gray-100 px-2 py-1 text-[10px] font-bold text-gray-600"
                >
                  Awaiting Assignment
                </span>
              </div>

              <button
                type="button"
                :disabled="
                  item.remainingUnits <= 0 ||
                  item.unassignedSections.length === 0 ||
                  assigning
                "
                @click="openAutoAssignModal(item)"
                class="inline-flex items-center rounded-md bg-gray-900 px-4 py-2 text-[10px] font-bold text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-40"
              >
                {{ assigning ? "Processing..." : "Auto Assign Sections" }}
              </button>
            </div>
          </div>

          <!-- =====================================================
               FACULTY TABLE
          ====================================================== -->
          <div class="overflow-x-auto">
            <table class="w-full min-w-[1250px] text-left">
              <thead class="border-b border-gray-200 bg-gray-900">
                <tr>
                  <th
                    class="px-5 py-3 text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Faculty
                  </th>

                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Unit Load
                  </th>

                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Current Load
                  </th>

                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Available
                  </th>

                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Assigned Units
                  </th>

                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Recommended
                  </th>

                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Assigned Sections
                  </th>

                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Status
                  </th>

                  <th
                    class="px-4 py-3 text-right text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Action
                  </th>
                </tr>
              </thead>

              <tbody class="divide-y divide-gray-100">
                <tr
                  v-for="faculty in item.faculty"
                  :key="faculty.key"
                  class="transition hover:bg-gray-50"
                >
                  <!-- FACULTY -->
                  <td class="px-5 py-4">
                    <div class="text-xs font-bold text-gray-900">
                      {{ faculty.facultyName }}
                    </div>

                    <div class="mt-1 text-[10px] text-gray-400">
                      {{ faculty.programCode || "—" }}
                    </div>
                  </td>

                  <!-- UNIT LOAD -->
                  <td class="px-5 py-4 text-center">
                    <span class="text-xs font-bold text-gray-900">
                      {{ faculty.unitLoad }}
                    </span>

                    <div class="text-[9px] text-gray-400">max units</div>
                  </td>

                  <!-- CURRENT LOAD -->
                  <td class="px-5 py-4 text-center">
                    <span
                      :class="[
                        'text-xs font-semibold',
                        faculty.currentUnits > faculty.unitLoad
                          ? 'text-red-600'
                          : 'text-gray-700',
                      ]"
                    >
                      {{ faculty.currentUnits }}
                    </span>
                  </td>

                  <!-- AVAILABLE -->
                  <td class="px-5 py-4 text-center">
                    <span
                      :class="[
                        'text-xs font-bold',
                        faculty.availableCapacity > 0
                          ? 'text-green-600'
                          : 'text-red-600',
                      ]"
                    >
                      {{ faculty.availableCapacity }}
                    </span>
                  </td>

                  <!-- ASSIGNED UNITS -->
                  <td class="px-5 py-4 text-center">
                    <span
                      :class="[
                        'text-xs font-bold',
                        faculty.assignedUnits > 0
                          ? 'text-blue-600'
                          : 'text-gray-400',
                      ]"
                    >
                      {{ faculty.assignedUnits }}
                    </span>

                    <div class="text-[9px] text-gray-400">this group</div>
                  </td>

                  <!-- RECOMMENDED -->
                  <td class="px-5 py-4 text-center">
                    <span
                      :class="[
                        'text-xs font-bold',
                        faculty.recommendedUnits > 0
                          ? 'text-blue-600'
                          : 'text-gray-400',
                      ]"
                    >
                      {{ faculty.recommendedUnits }}
                    </span>

                    <div class="text-[9px] text-gray-400">units to add</div>
                  </td>

                  <!-- ASSIGNED SECTIONS -->
                  <td class="px-5 py-4">
                    <div
                      v-if="faculty.assignedSections.length"
                      class="flex flex-wrap justify-center gap-1"
                    >
                      <span
                        v-for="section in faculty.assignedSections"
                        :key="section.classId"
                        class="rounded bg-green-50 px-2 py-1 text-[9px] font-bold text-green-700 ring-1 ring-green-200"
                      >
                        {{ getSectionDisplay(section) }}
                      </span>
                    </div>

                    <span
                      v-else
                      class="block text-center text-[10px] text-gray-400"
                    >
                      —
                    </span>
                  </td>

                  <!-- STATUS -->
                  <!-- STATUS -->
                  <td class="px-5 py-4 text-center">
                    <span
                      v-if="faculty.status === 'Assigned'"
                      class="inline-flex rounded bg-green-100 px-2 py-1 text-[10px] font-bold text-green-700"
                    >
                      Assigned
                    </span>

                    <span
                      v-else-if="faculty.assignedSections.length"
                      class="inline-flex rounded bg-green-100 px-2 py-1 text-[10px] font-bold text-green-700"
                    >
                      Assigned
                    </span>

                    <span
                      v-else-if="faculty.availableCapacity > 0"
                      class="inline-flex rounded bg-gray-100 px-2 py-1 text-[10px] font-bold text-gray-600"
                    >
                      Available
                    </span>

                    <span
                      v-else
                      class="inline-flex rounded bg-red-100 px-2 py-1 text-[10px] font-bold text-red-700"
                    >
                      Needs Adjustment
                    </span>
                  </td>

                  <!-- ACTION -->
                  <td class="px-4 py-4 text-right">
                    <div class="flex justify-end gap-2">
                      <!-- ASSIGN -->
                      <button
                        v-if="item.unassignedSections.length"
                        type="button"
                        @click="openIndividualAssignModal(item, faculty)"
                        class="inline-flex items-center rounded-md bg-gray-900 px-3 py-1.5 text-[10px] font-semibold text-white transition hover:bg-gray-800"
                      >
                        Assign
                      </button>

                      <!-- ADJUST UNIT -->
                      <button
                        type="button"
                        @click="openAdjustUnitModal(faculty)"
                        class="inline-flex items-center rounded-md border border-gray-300 bg-white px-3 py-1.5 text-[10px] font-semibold text-gray-700 transition hover:border-gray-900 hover:bg-gray-50"
                      >
                        Adjust Unit
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- =====================================================
               COURSE FOOTER
          ====================================================== -->
          <div
            class="flex flex-col gap-3 border-t border-gray-200 bg-gray-50 px-5 py-3 sm:flex-row sm:items-center sm:justify-between"
          >
            <div>
              <p class="text-[10px] font-medium text-gray-500">
                Faculty Candidates
              </p>

              <p class="mt-0.5 text-[10px] text-gray-400">
                {{ item.faculty.length }}
                faculty candidate(s) ·
                {{ item.sections.length }}
                section(s)
              </p>
            </div>

            <div class="flex items-center gap-5">
              <div class="text-right">
                <p class="text-[9px] uppercase tracking-wide text-gray-400">
                  Required
                </p>

                <p class="text-xs font-bold text-gray-700">
                  {{ item.requiredUnits }}
                </p>
              </div>

              <div class="text-right">
                <p class="text-[9px] uppercase tracking-wide text-gray-400">
                  Assigned
                </p>

                <p class="text-xs font-bold text-green-600">
                  {{ item.assignedUnits }}
                </p>
              </div>

              <div class="text-right">
                <p class="text-[9px] uppercase tracking-wide text-gray-400">
                  Remaining
                </p>

                <p class="text-xs font-bold text-orange-600">
                  {{ item.remainingUnits }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- =======================================================
           NO DATA
      ======================================================== -->
      <div
        v-else
        class="rounded-lg border border-gray-200 bg-white px-6 py-16 text-center"
      >
        <div
          class="mx-auto flex h-10 w-10 items-center justify-center rounded-full bg-green-100 text-lg font-bold text-green-600"
        >
          ✓
        </div>

        <h3 class="mt-3 text-sm font-bold text-gray-900">
          No Faculty Adjustment Required
        </h3>

        <p class="mt-1 text-xs text-gray-400">
          There are currently no unresolved faculty assignments requiring
          adjustment.
        </p>
      </div>
    </div>

    <!-- =========================================================
         INDIVIDUAL ASSIGN MODAL
    ========================================================== -->
    <div
      v-if="showAssignModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
    >
      <div
        class="w-full max-w-lg overflow-hidden rounded-lg bg-white shadow-xl"
      >
        <!-- HEADER -->
        <div class="border-b border-gray-200 px-5 py-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-sm font-bold text-gray-900">Assign Faculty</h3>

              <p class="mt-1 text-xs text-gray-500">
                Review the section assignment before saving.
              </p>
            </div>

            <button
              type="button"
              @click="closeAssignModal"
              class="text-lg text-gray-400 hover:text-gray-700"
            >
              ×
            </button>
          </div>
        </div>

        <!-- BODY -->
        <div class="space-y-4 px-5 py-5">
          <!-- FACULTY -->
          <div>
            <label
              class="text-[10px] font-bold uppercase tracking-wide text-gray-500"
            >
              Faculty
            </label>

            <div
              class="mt-1 rounded-md border border-gray-200 bg-gray-50 px-3 py-2"
            >
              <p class="text-sm font-semibold text-gray-900">
                {{ selectedAssignment?.facultyName || "—" }}
              </p>

              <p class="mt-1 text-[10px] text-gray-400">
                Faculty ID: {{ selectedAssignment?.facultyId || "—" }}
              </p>
            </div>
          </div>

          <!-- COURSE -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label
                class="text-[10px] font-bold uppercase tracking-wide text-gray-500"
              >
                Course
              </label>

              <div
                class="mt-1 rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-xs font-semibold text-gray-700"
              >
                {{ selectedAssignment?.courseCode || "—" }}
              </div>
            </div>

            <div>
              <label
                class="text-[10px] font-bold uppercase tracking-wide text-gray-500"
              >
                Program
              </label>

              <div
                class="mt-1 rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-xs font-semibold text-gray-700"
              >
                {{ selectedAssignment?.programCode || "—" }}
              </div>
            </div>
          </div>

          <!-- SECTION -->
          <!-- MULTIPLE SECTIONS -->
          <div>
            <div class="flex items-center justify-between">
              <label
                class="text-[10px] font-bold uppercase tracking-wide text-gray-500"
              >
                Sections to Assign
              </label>

              <span class="text-[10px] font-bold text-blue-600">
                {{ selectedAssignment?.selectedSectionIds?.length || 0 }}
                selected
              </span>
            </div>

            <div class="mt-2 max-h-48 space-y-2 overflow-y-auto">
              <label
                v-for="section in selectedAssignment?.availableSections || []"
                :key="section.classId"
                class="flex cursor-pointer items-center justify-between rounded-md border border-gray-200 bg-white px-3 py-2 hover:bg-gray-50"
              >
                <div class="flex items-center gap-3">
                  <input
                    v-model="selectedAssignment.selectedSectionIds"
                    type="checkbox"
                    :value="section.classId"
                    @change="refreshSelectedAssignment"
                    class="h-4 w-4 rounded border-gray-300"
                  />

                  <div>
                    <p class="text-xs font-bold text-gray-800">
                      {{ getSectionDisplay(section) }}
                    </p>

                    <p class="text-[9px] text-gray-400">
                      Class ID: {{ section.classId }}
                    </p>
                  </div>
                </div>

                <span class="text-xs font-bold text-gray-700">
                  {{ section.requiredUnits }} units
                </span>
              </label>
            </div>
          </div>

          <!-- UNIT SUMMARY -->
          <div
            v-if="selectedAssignment?.selectedSectionIds?.length"
            class="grid grid-cols-2 gap-3"
          >
            <div
              class="rounded-md border border-gray-200 bg-gray-50 px-3 py-3 text-center"
            >
              <p class="text-[9px] uppercase tracking-wide text-gray-400">
                Sections
              </p>

              <p class="mt-1 text-sm font-bold text-gray-900">
                {{ selectedAssignment.selectedSectionIds.length }}
              </p>
            </div>

            <div
              class="rounded-md border border-gray-200 bg-gray-50 px-3 py-3 text-center"
            >
              <p class="text-[9px] uppercase tracking-wide text-gray-400">
                Total Units
              </p>

              <p class="mt-1 text-sm font-bold text-blue-600">
                {{ selectedAssignment.selectedTotalUnits }}
              </p>
            </div>
          </div>
        </div>

        <!-- FOOTER -->
        <div
          class="flex items-center justify-end gap-2 border-t border-gray-200 bg-gray-50 px-5 py-3"
        >
          <button
            type="button"
            @click="closeAssignModal"
            class="rounded-md border border-gray-300 bg-white px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100"
          >
            Cancel
          </button>

          <button
            type="button"
            :disabled="
              savingAssignment ||
              !selectedAssignment?.selectedSectionIds?.length
            "
            @click="confirmIndividualAssignment"
            class="rounded-md bg-gray-900 px-4 py-2 text-xs font-semibold text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {{
              savingAssignment
                ? "Saving..."
                : selectedAssignment?.requiredAdjustment > 0
                ? "Adjust & Assign"
                : "Confirm Assignment"
            }}
          </button>
        </div>
      </div>
    </div>

    <!-- =========================================================
         AUTO ASSIGN CONFIRMATION MODAL
    ========================================================== -->
    <div
      v-if="showAutoAssignModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
    >
      <div
        class="w-full max-w-5xl max-h-[90vh] overflow-hidden rounded-lg bg-white shadow-xl"
      >
        <!-- HEADER -->
        <div class="border-b border-gray-200 px-5 py-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-sm font-bold text-gray-900">
                Automatic Section Assignment
              </h3>

              <p class="mt-1 text-xs text-gray-500">
                Review the automatically balanced faculty distribution before
                saving.
              </p>
            </div>

            <button
              type="button"
              @click="closeAutoAssignModal"
              class="text-lg text-gray-400 hover:text-gray-700"
            >
              ×
            </button>
          </div>
        </div>

        <!-- BODY -->
        <div class="max-h-[65vh] overflow-y-auto px-5 py-5">
          <!-- SUMMARY -->
          <div
            v-if="autoAssignmentProposal"
            class="mb-5 grid grid-cols-2 gap-3 md:grid-cols-5"
          >
            <div
              class="rounded-md border border-gray-200 bg-gray-50 px-3 py-3 text-center"
            >
              <p class="text-[9px] uppercase text-gray-400">Required</p>

              <p class="mt-1 text-sm font-bold text-gray-900">
                {{ autoAssignmentProposal.requiredUnits }}
              </p>
            </div>

            <div
              class="rounded-md border border-gray-200 bg-gray-50 px-3 py-3 text-center"
            >
              <p class="text-[9px] uppercase text-gray-400">Assigning</p>

              <p class="mt-1 text-sm font-bold text-blue-600">
                {{ autoAssignmentProposal.assignedUnits }}
              </p>
            </div>

            <div
              class="rounded-md border border-gray-200 bg-gray-50 px-3 py-3 text-center"
            >
              <p class="text-[9px] uppercase text-gray-400">Remaining</p>

              <p class="mt-1 text-sm font-bold text-orange-600">
                {{ autoAssignmentProposal.remainingUnits }}
              </p>
            </div>

            <div
              class="rounded-md border border-gray-200 bg-gray-50 px-3 py-3 text-center"
            >
              <p class="text-[9px] uppercase text-gray-400">Sections</p>

              <p class="mt-1 text-sm font-bold text-gray-900">
                {{ autoAssignmentProposal.assignments.length }}
              </p>
            </div>

            <div
              class="rounded-md border border-orange-200 bg-orange-50 px-3 py-3 text-center"
            >
              <p class="text-[9px] uppercase text-orange-500">Adjustments</p>

              <p class="mt-1 text-sm font-bold text-orange-700">
                {{ autoAssignmentProposal.adjustmentCount }}
              </p>
            </div>
          </div>

          <!-- ASSIGNMENTS -->
          <div class="overflow-x-auto rounded-md border border-gray-200">
            <table class="w-full min-w-[850px] text-left">
              <thead class="bg-gray-900">
                <tr>
                  <th
                    class="px-4 py-3 text-[10px] font-bold uppercase text-white"
                  >
                    Section
                  </th>

                  <th
                    class="px-4 py-3 text-[10px] font-bold uppercase text-white"
                  >
                    Required
                  </th>

                  <th
                    class="px-4 py-3 text-[10px] font-bold uppercase text-white"
                  >
                    Faculty
                  </th>

                  <th
                    class="px-4 py-3 text-center text-[10px] font-bold uppercase text-white"
                  >
                    Current Load
                  </th>

                  <th
                    class="px-4 py-3 text-center text-[10px] font-bold uppercase text-white"
                  >
                    Available
                  </th>

                  <th
                    class="px-4 py-3 text-center text-[10px] font-bold uppercase text-white"
                  >
                    Adjustment
                  </th>

                  <th
                    class="px-4 py-3 text-center text-[10px] font-bold uppercase text-white"
                  >
                    New Unit Load
                  </th>

                  <th
                    class="px-4 py-3 text-center text-[10px] font-bold uppercase text-white"
                  >
                    Status
                  </th>
                </tr>
              </thead>

              <tbody class="divide-y divide-gray-100">
                <tr
                  v-for="assignment in autoAssignmentProposal?.assignments ||
                  []"
                  :key="`${assignment.classId}-${assignment.facultyId}`"
                  class="hover:bg-gray-50"
                >
                  <!-- SECTION -->
                  <td class="px-4 py-3">
                    <div class="text-xs font-bold text-gray-900">
                      {{ getSectionDisplay(assignment.section) }}
                    </div>
                  </td>

                  <!-- REQUIRED -->
                  <td class="px-4 py-3">
                    <span class="text-xs font-bold text-gray-900">
                      {{ assignment.requiredUnits }}
                    </span>
                  </td>

                  <!-- FACULTY -->
                  <td class="px-4 py-3">
                    <div class="text-xs font-bold text-gray-900">
                      {{ assignment.facultyName }}
                    </div>

                    <div class="mt-1 text-[9px] text-gray-400">
                      ID: {{ assignment.facultyId }}
                    </div>
                  </td>

                  <!-- CURRENT -->
                  <td class="px-4 py-3 text-center">
                    <span class="text-xs text-gray-700">
                      {{ assignment.currentUnits }}
                    </span>
                  </td>

                  <!-- AVAILABLE -->
                  <td class="px-4 py-3 text-center">
                    <span
                      :class="[
                        'text-xs font-bold',
                        assignment.availableCapacity >= assignment.requiredUnits
                          ? 'text-green-600'
                          : 'text-orange-600',
                      ]"
                    >
                      {{ assignment.availableCapacity }}
                    </span>
                  </td>

                  <!-- ADJUSTMENT -->
                  <td class="px-4 py-3 text-center">
                    <span
                      :class="[
                        'text-xs font-bold',
                        assignment.requiredAdjustment > 0
                          ? 'text-orange-600'
                          : 'text-green-600',
                      ]"
                    >
                      {{
                        assignment.requiredAdjustment > 0
                          ? `+${assignment.requiredAdjustment}`
                          : "0"
                      }}
                    </span>
                  </td>

                  <!-- NEW LOAD -->
                  <td class="px-4 py-3 text-center">
                    <span class="text-xs font-bold text-blue-600">
                      {{ assignment.newUnitLoad }}
                    </span>
                  </td>

                  <!-- STATUS -->
                  <td class="px-4 py-3 text-center">
                    <span
                      v-if="assignment.requiredAdjustment > 0"
                      class="inline-flex rounded bg-orange-100 px-2 py-1 text-[9px] font-bold text-orange-700"
                    >
                      Adjust + Assign
                    </span>

                    <span
                      v-else
                      class="inline-flex rounded bg-green-100 px-2 py-1 text-[9px] font-bold text-green-700"
                    >
                      Ready
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- INFO -->
          <div
            class="mt-4 rounded-md border border-blue-200 bg-blue-50 px-4 py-3"
          >
            <p class="text-xs font-bold text-blue-700">
              Automatic distribution
            </p>

            <p class="mt-1 text-[10px] leading-5 text-blue-600">
              The system distributes the available sections as evenly as
              possible among the possible faculty while considering their
              current load and available capacity. Any required unit adjustment
              will be applied together with the assignment after confirmation.
            </p>
          </div>
        </div>

        <!-- FOOTER -->
        <div
          class="flex items-center justify-end gap-2 border-t border-gray-200 bg-gray-50 px-5 py-3"
        >
          <button
            type="button"
            @click="closeAutoAssignModal"
            class="rounded-md border border-gray-300 bg-white px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100"
          >
            Cancel
          </button>

          <button
            type="button"
            :disabled="
              savingAutoAssignment ||
              !autoAssignmentProposal?.assignments?.length
            "
            @click="confirmAutoAssignment"
            class="rounded-md bg-gray-900 px-4 py-2 text-xs font-semibold text-white hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {{
              savingAutoAssignment
                ? "Saving Assignments..."
                : "Confirm & Save Assignments"
            }}
          </button>
        </div>
      </div>
    </div>

    <!-- =========================================================
         ADJUST FACULTY UNIT MODAL
    ========================================================== -->
    <div
      v-if="showAdjustUnitModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
    >
      <div
        class="w-full max-w-md overflow-hidden rounded-lg bg-white shadow-xl"
      >
        <!-- HEADER -->
        <div class="border-b border-gray-200 px-5 py-4">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-sm font-bold text-gray-900">
                Adjust Faculty Unit
              </h3>

              <p class="mt-1 text-xs text-gray-500">
                Update the maximum teaching unit of the selected faculty.
              </p>
            </div>

            <button
              type="button"
              @click="closeAdjustUnitModal"
              class="text-lg text-gray-400 hover:text-gray-700"
            >
              ×
            </button>
          </div>
        </div>

        <!-- BODY -->
        <div class="space-y-4 px-5 py-5">
          <!-- FACULTY -->
          <div>
            <label
              class="text-[10px] font-bold uppercase tracking-wide text-gray-500"
            >
              Faculty
            </label>

            <div
              class="mt-1 rounded-md border border-gray-200 bg-gray-50 px-3 py-2"
            >
              <p class="text-sm font-semibold text-gray-900">
                {{ selectedFaculty?.name || "—" }}
              </p>

              <p class="mt-1 text-[10px] text-gray-400">
                {{ selectedFaculty?.email || "—" }}
              </p>
            </div>
          </div>

          <!-- FACULTY ID -->
          <div>
            <label
              class="text-[10px] font-bold uppercase tracking-wide text-gray-500"
            >
              Faculty ID
            </label>

            <div
              class="mt-1 rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-xs font-semibold text-gray-700"
            >
              {{ selectedFaculty?.id || "—" }}
            </div>
          </div>

          <!-- CURRENT UNIT -->
          <div>
            <label
              class="text-[10px] font-bold uppercase tracking-wide text-gray-500"
            >
              Current Unit Load
            </label>

            <div
              class="mt-1 rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-xs font-semibold text-gray-700"
            >
              {{ selectedFaculty?.unitLoad || 0 }}
            </div>
          </div>

          <!-- PLUS UNIT -->
          <div>
            <label
              class="text-[10px] font-bold uppercase tracking-wide text-gray-500"
            >
              Plus Unit
            </label>

            <input
              v-model.number="plusUnit"
              type="number"
              min="0"
              step="0.25"
              class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm outline-none transition focus:border-gray-900"
              placeholder="Enter additional units"
            />

            <p class="mt-1 text-[10px] text-gray-400">
              Enter the additional units to add to the current unit load.
            </p>
          </div>

          <!-- NEW UNIT -->
          <div>
            <label
              class="text-[10px] font-bold uppercase tracking-wide text-gray-500"
            >
              New Unit Load
            </label>

            <div
              class="mt-1 rounded-md border border-gray-200 bg-gray-50 px-3 py-2 text-sm font-bold text-gray-900"
            >
              {{ adjustedUnitLoad }}
            </div>
          </div>

          <!-- ASSIGN SECTION -->
          <div
            v-if="adjustmentAssignment"
            class="rounded-md border border-blue-200 bg-blue-50 px-4 py-3"
          >
            <p class="text-[9px] uppercase text-blue-500">Sections to Assign</p>

            <div class="mt-2 space-y-1">
              <div
                v-for="section in adjustmentAssignment.sections || []"
                :key="section.classId"
                class="flex items-center justify-between"
              >
                <p class="text-xs font-bold text-blue-800">
                  {{ adjustmentAssignment.courseCode }} -
                  {{ getSectionDisplay(section) }}
                </p>

                <span class="text-xs font-bold text-blue-700">
                  {{ section.requiredUnits }}
                </span>
              </div>
            </div>

            <div class="mt-2 border-t border-blue-200 pt-2 text-right">
              <span class="text-[10px] font-semibold text-blue-600">
                Total: {{ adjustmentAssignment.totalUnits }} units
              </span>
            </div>
          </div>
        </div>

        <!-- FOOTER -->
        <div
          class="flex items-center justify-end gap-2 border-t border-gray-200 bg-gray-50 px-5 py-3"
        >
          <button
            type="button"
            @click="closeAdjustUnitModal"
            class="rounded-md border border-gray-300 bg-white px-4 py-2 text-xs font-semibold text-gray-600 hover:bg-gray-100"
          >
            Cancel
          </button>

          <button
            v-if="adjustmentAssignment"
            type="button"
            :disabled="
              savingUnitLoad ||
              adjustedUnitLoad < 0 ||
              adjustedUnitLoad === null ||
              adjustedUnitLoad === ''
            "
            @click="saveAdjustedUnitAndAssign"
            class="rounded-md bg-gray-900 px-4 py-2 text-xs font-semibold text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {{ savingUnitLoad ? "Saving..." : "Submit" }}
          </button>

          <button
            v-else
            type="button"
            :disabled="
              savingUnitLoad ||
              adjustedUnitLoad < 0 ||
              adjustedUnitLoad === null ||
              adjustedUnitLoad === ''
            "
            @click="saveAdjustedUnit"
            class="rounded-md bg-gray-900 px-4 py-2 text-xs font-semibold text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {{ savingUnitLoad ? "Saving..." : "Save Changes" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useFetchDataStore } from "../../../../store/fetch-data-store";
import axios from "axios";

export default {
  name: "TablePostAssessment",

  data() {
    return {
      fetchDataStore: useFetchDataStore(),

      loading: false,

      /* ============================================================
       * API
       * ========================================================== */

      /*
       * IMPORTANT:
       * Change this only if your NestJS assignment endpoint
       * has a different route.
       */
      ASSIGNMENT_API: "http://localhost:8000/unscheduled-meetings",

      /* ============================================================
       * ADJUST UNIT
       * ========================================================== */

      showAdjustUnitModal: false,
      selectedFaculty: null,
      adjustedUnitLoad: 0,
      plusUnit: 0,
      savingUnitLoad: false,

      /* ============================================================
       * INDIVIDUAL ASSIGNMENT
       * ========================================================== */

      showAssignModal: false,
      selectedAssignment: null,
      savingAssignment: false,

      /* ============================================================
       * AUTO ASSIGNMENT
       * ========================================================== */

      showAutoAssignModal: false,
      autoAssignmentProposal: null,
      savingAutoAssignment: false,
      assigning: false,

      /*
       * Local assignments are used immediately after saving
       * so the UI updates without requiring a full page reload.
       */
      localAssignments: {},

      /*
       * Temporary assignment proposals.
       */
      pendingAssignments: [],

      /*
       * Existing captured units.
       */
      capturedUnits: {},
      adjustmentAssignment: null,
      selectedSectionIds: [],
      selectedSections: [],
      selectedTotalUnits: 0,
      requiredAdjustment: 0,
      newUnitLoad: 0,
    };
  },

  watch: {
    plusUnit(newValue) {
      const current = Number(this.selectedFaculty?.unitLoad || 0);
      const plus = Number(newValue || 0);

      this.adjustedUnitLoad = this.roundUnits(Math.max(0, current + plus));
    },
  },

  computed: {
    /* ============================================================
     * DATA
     * ========================================================== */
    classSections() {
      return this.fetchDataStore.sections || [];
    },
    finalSchedules() {
      return this.fetchDataStore.final_schedules || [];
    },

    unscheduledMeetings() {
      return this.fetchDataStore.unscheduled_meetings || [];
    },

    courses() {
      return this.fetchDataStore.courses || [];
    },

    rawUsers() {
      return this.fetchDataStore.rawusers || [];
    },

    /* ============================================================
     * FACULTY LOAD
     * ========================================================== */

    facultyLoadAssessment() {
      const facultyMap = new Map();

      this.rawUsers.forEach((user) => {
        const role = String(user.role || "")
          .trim()
          .toLowerCase();

        if (role && role !== "faculty" && role !== "program chairperson") {
          return;
        }

        if (!user.id) return;

        const facultyId = Number(user.id);

        facultyMap.set(facultyId, {
          id: facultyId,
          name: this.getUserName(user),
          email: user.email || "",
          programCode: user.program_code || user.program?.program_code || "—",
          unitLoad: this.roundUnits(user.unit_load),
          currentUnits: 0,
        });
      });

      const countedSchedules = new Set();

      this.finalSchedules.forEach((schedule) => {
        if (!schedule?.faculty_id) return;

        const facultyId = Number(schedule.faculty_id);

        if (!facultyMap.has(facultyId)) return;

        // IMPORTANT:
        // Filter to the current school year and semester here.
        if (
          this.selectedSchoolYear &&
          this.normalizeValue(schedule.school_year) !==
            this.normalizeValue(this.selectedSchoolYear)
        ) {
          return;
        }

        if (
          this.selectedSemester &&
          Number(schedule.semester) !== Number(this.selectedSemester)
        ) {
          return;
        }

        const classId = schedule.class_id ?? schedule.classId ?? schedule.id;

        const courseId = schedule.course_id ?? schedule.course_code;

        const scheduleKey = [facultyId, classId, courseId].join("|");

        if (countedSchedules.has(scheduleKey)) {
          return;
        }

        countedSchedules.add(scheduleKey);

        const units = this.getScheduleUnits(schedule);

        facultyMap.get(facultyId).currentUnits = this.roundUnits(
          facultyMap.get(facultyId).currentUnits + units,
        );
      });

      return Array.from(facultyMap.values()).map((faculty) => {
        const remainingCapacity = this.roundUnits(
          Math.max(0, faculty.unitLoad - faculty.currentUnits),
        );

        return {
          ...faculty,
          remainingCapacity,
          availableCapacity: remainingCapacity,
          status:
            faculty.currentUnits > faculty.unitLoad
              ? "Overloaded"
              : remainingCapacity === 0
              ? "At Maximum Load"
              : remainingCapacity <= 3
              ? "Limited Capacity"
              : "Available",
        };
      });
    },

    /* ============================================================
     * FACULTY GROUPS
     * ========================================================== */

    groupedFaculty() {
      const groups = new Map();

      this.unscheduledMeetings.forEach((item) => {
        /*
         * Only unresolved sections.
         *
         * Once a section has been assigned and the database
         * contains faculty_name, it will no longer appear here.
         */
        if (!this.needsFacultyAssignment(item)) {
          return;
        }

        const requiredUnits = this.roundUnits(this.getRequiredUnits(item));

        if (requiredUnits <= 0) {
          return;
        }

        const candidates = this.getPossibleFaculty(item);

        if (!candidates.length) {
          return;
        }

        const courseCode = item.course_code || "—";
        const programCode = item.program_code || "—";

        const groupKey = [courseCode, programCode].join("|").toLowerCase();

        if (!groups.has(groupKey)) {
          groups.set(groupKey, {
            key: groupKey,

            courseCode,

            courseTitle: this.getCourseTitle(item),

            programCode,

            sections: [],

            requiredUnits: 0,

            alreadyCapturedUnits: 0,

            assignedUnits: 0,

            remainingUnits: 0,

            assignedSectionCount: 0,

            unassignedSections: [],

            faculty: [],
          });
        }

        const group = groups.get(groupKey);

        /*
         * SECTION
         */
        const classId = item.class_id || item.classId || item.id;

        const existingSection = group.sections.find(
          (section) => String(section.classId) === String(classId),
        );
        const setName =
          item.set_name ||
          item.setName ||
          item.section ||
          item.class_name ||
          this.getSetNameByClassId(classId) ||
          "";
        if (!existingSection) {
          group.sections.push({
            classId,

            classIdValue: classId,

            setName,

            classSize:
              item.class_size ||
              item.classSize ||
              this.getClassSizeByClassId(classId) ||
              null,

            requiredUnits,

            unscheduledId: item.id,

            originalItem: item,
          });

          group.requiredUnits = this.roundUnits(
            group.requiredUnits + requiredUnits,
          );
        }

        /*
         * FACULTY
         */
        candidates.forEach((candidate) => {
          if (!candidate || candidate.id == null) {
            return;
          }

          const facultyExists = group.faculty.some(
            (faculty) => String(faculty.facultyId) === String(candidate.id),
          );

          if (facultyExists) {
            return;
          }

          group.faculty.push({
            key: `${groupKey}-${candidate.id}`,

            facultyId: candidate.id,

            facultyName: candidate.name,

            programCode: candidate.programCode || "—",

            unitLoad: this.roundUnits(candidate.unitLoad),

            currentUnits: this.roundUnits(candidate.currentUnits),

            availableCapacity: this.roundUnits(candidate.availableCapacity),

            assignedUnits: 0,

            assignedSections: [],

            recommendedUnits: 0,

            requiredAdjustment: 0,
            status: "Available",
          });
        });
      });

      /*
       * FINAL CALCULATIONS
       */
      groups.forEach((group) => {
        /*
         * Already assigned schedules.
         */
        group.alreadyCapturedUnits = this.getCapturedUnits(group);

        /*
         * Local assignments already saved in this page.
         */
        const savedAssignments = this.getLocalAssignmentsForGroup(group);

        let assignedUnits = this.roundUnits(group.alreadyCapturedUnits);

        /*
         * Build assigned section list.
         */
        const assignedClassIds = new Set();

        savedAssignments.forEach((assignment) => {
          const classId = String(assignment.classId);

          assignedClassIds.add(classId);

          const section = group.sections.find(
            (item) => String(item.classId) === classId,
          );

          if (section) {
            assignedUnits = this.roundUnits(
              assignedUnits + Number(section.requiredUnits || 0),
            );
          }
        });

        /*
         * Check existing DB assignments.
         */
        this.unscheduledMeetings.forEach((item) => {
          const sameCourse =
            this.normalizeValue(item.course_code) ===
            this.normalizeValue(group.courseCode);

          const sameProgram =
            this.normalizeValue(item.program_code) ===
            this.normalizeValue(group.programCode);

          if (!sameCourse || !sameProgram) {
            return;
          }

          const facultyName = String(item.faculty_name || "").trim();

          if (!facultyName || facultyName.toLowerCase() === "unassigned") {
            return;
          }

          const classId = item.class_id || item.classId || item.id;

          const classKey = String(classId);

          if (assignedClassIds.has(classKey)) {
            return;
          }

          const section = group.sections.find(
            (item) => String(item.classId) === classKey,
          );

          if (!section) {
            return;
          }

          assignedClassIds.add(classKey);

          assignedUnits = this.roundUnits(
            assignedUnits + Number(section.requiredUnits || 0),
          );
        });

        group.assignedUnits = this.roundUnits(assignedUnits);

        group.remainingUnits = this.roundUnits(
          Math.max(0, group.requiredUnits - group.assignedUnits),
        );

        /*
         * Assigned section count.
         */
        group.assignedSectionCount = assignedClassIds.size;

        /*
         * Unassigned sections.
         */
        group.unassignedSections = group.sections.filter(
          (section) => !assignedClassIds.has(String(section.classId)),
        );

        /*
         * Faculty assignments for this group.
         */
        group.faculty.forEach((faculty) => {
          faculty.assignedUnits = 0;
          faculty.assignedSections = [];

          /*
           * Local assignments.
           */
          savedAssignments.forEach((assignment) => {
            if (Number(assignment.facultyId) !== Number(faculty.facultyId)) {
              return;
            }

            const section = group.sections.find(
              (item) => String(item.classId) === String(assignment.classId),
            );

            if (!section) {
              return;
            }

            faculty.assignedUnits = this.roundUnits(
              faculty.assignedUnits + section.requiredUnits,
            );

            faculty.assignedSections.push(section);
          });

          /*
           * Existing DB assignments.
           */
          this.unscheduledMeetings.forEach((meeting) => {
            const sameCourse =
              this.normalizeValue(meeting.course_code) ===
              this.normalizeValue(group.courseCode);

            const sameProgram =
              this.normalizeValue(meeting.program_code) ===
              this.normalizeValue(group.programCode);

            if (!sameCourse || !sameProgram) {
              return;
            }

            const meetingFaculty = this.findFacultyByName(meeting.faculty_name);

            if (
              !meetingFaculty ||
              Number(meetingFaculty.id) !== Number(faculty.facultyId)
            ) {
              return;
            }

            const classId = meeting.class_id || meeting.classId || meeting.id;

            const alreadyIncluded = faculty.assignedSections.some(
              (section) => String(section.classId) === String(classId),
            );

            if (alreadyIncluded) {
              return;
            }

            const section = group.sections.find(
              (item) => String(item.classId) === String(classId),
            );

            if (!section) {
              return;
            }

            faculty.assignedUnits = this.roundUnits(
              faculty.assignedUnits + section.requiredUnits,
            );

            faculty.assignedSections.push(section);
          });

          /*
           * Recommendation for remaining sections.
           */
          const available = Number(faculty.availableCapacity || 0);

          faculty.recommendedUnits = this.roundUnits(
            Math.max(0, group.remainingUnits - available),
          );
        });

        /*
         * Sort faculty.
         *
         * 1. Faculty with enough capacity
         * 2. Lowest assigned units
         * 3. Lowest current load
         * 4. Name
         */
        group.faculty.sort((a, b) => {
          const aCanFit =
            Number(a.availableCapacity || 0) >=
            Number(group.unassignedSections[0]?.requiredUnits || 0);

          const bCanFit =
            Number(b.availableCapacity || 0) >=
            Number(group.unassignedSections[0]?.requiredUnits || 0);

          if (aCanFit !== bCanFit) {
            return aCanFit ? -1 : 1;
          }

          const assignedDiff =
            Number(a.assignedUnits || 0) - Number(b.assignedUnits || 0);

          if (assignedDiff !== 0) {
            return assignedDiff;
          }

          const loadDiff =
            Number(a.currentUnits || 0) - Number(b.currentUnits || 0);

          if (loadDiff !== 0) {
            return loadDiff;
          }

          return String(a.facultyName || "").localeCompare(
            String(b.facultyName || ""),
          );
        });
      });

      /*
       * Only hide the course when ALL sections are assigned.
       *
       * If even ONE section is still unassigned,
       * keep the entire course group visible.
       */
      return Array.from(groups.values()).filter((group) => {
        return group.unassignedSections.length > 0;
      });
    },
  },

  async mounted() {
    await this.loadFacultyAdjustmentData();
  },

  methods: {
    getSetNameByClassId(classId) {
      if (!classId) {
        return "";
      }

      const foundClass = this.classSections.find(
        (item) => Number(item.class_id) === Number(classId),
      );

      return foundClass?.set_name || "";
    },
    /* ============================================================
     * NEEDS FACULTY ASSIGNMENT
     * ========================================================== */

    needsFacultyAssignment(item) {
      if (!item) {
        return false;
      }

      const facultyName = String(item.faculty_name || "")
        .trim()
        .toLowerCase();

      /*
       * Explicitly unassigned.
       */
      if (!facultyName || facultyName === "unassigned") {
        return true;
      }

      /*
       * Assignment status may exist.
       */
      const status = String(item.status || "").toLowerCase();

      if (status === "assigned" || status === "assign") {
        return false;
      }

      /*
       * Reason explicitly says no faculty.
       */
      const reason = String(item.reason || "").toLowerCase();

      if (reason.includes("no faculty assignment")) {
        return true;
      }

      return false;
    },

    /* ============================================================
     * CAPTURED UNITS
     * ========================================================== */

    getCapturedUnits(group) {
      if (!group) {
        return 0;
      }

      let total = 0;

      const counted = new Set();

      this.finalSchedules.forEach((schedule) => {
        if (!schedule || !schedule.faculty_id) {
          return;
        }

        const scheduleCourse = this.normalizeValue(schedule.course_code);

        const scheduleProgram = this.normalizeValue(schedule.program_code);

        const groupCourse = this.normalizeValue(group.courseCode);

        const groupProgram = this.normalizeValue(group.programCode);

        if (
          scheduleCourse !== groupCourse ||
          scheduleProgram !== groupProgram
        ) {
          return;
        }

        const key = [
          schedule.faculty_id,
          schedule.class_id || schedule.classId || schedule.id,
          schedule.course_id || schedule.course_code,
        ].join("|");

        if (counted.has(key)) {
          return;
        }

        counted.add(key);

        total += Number(this.getScheduleUnits(schedule) || 0);
      });

      return this.roundUnits(total);
    },

    /* ============================================================
     * AUTOMATIC ASSIGNMENT
     * ========================================================== */

    openAutoAssignModal(group) {
      if (!group) {
        return;
      }

      if (!group.unassignedSections.length) {
        return;
      }

      this.assigning = true;

      try {
        const proposal = this.generateAutomaticAssignment(group);

        this.autoAssignmentProposal = proposal;

        this.showAutoAssignModal = true;
      } finally {
        this.assigning = false;
      }
    },

    closeAutoAssignModal() {
      if (this.savingAutoAssignment) {
        return;
      }

      this.showAutoAssignModal = false;

      this.autoAssignmentProposal = null;

      this.pendingAssignments = [];
    },

    generateAutomaticAssignment(group) {
      const sections = [...group.unassignedSections];

      const faculty = group.faculty.map((item) => ({
        ...item,

        simulatedAssignedUnits: Number(item.assignedUnits || 0),

        simulatedSections: [...(item.assignedSections || [])],

        simulatedAvailable: Number(item.availableCapacity || 0),
      }));

      /*
       * Sort sections from largest to smallest.
       *
       * This is important because assigning the largest
       * section first avoids leaving a large section
       * impossible to allocate at the end.
       */
      sections.sort(
        (a, b) => Number(b.requiredUnits || 0) - Number(a.requiredUnits || 0),
      );

      const assignments = [];

      sections.forEach((section) => {
        /*
         * Faculty candidates.
         */
        const candidates = faculty.filter((item) => {
          const alreadyAssigned = item.simulatedSections.some(
            (assignedSection) =>
              String(assignedSection.classId) === String(section.classId),
          );

          return !alreadyAssigned;
        });

        if (!candidates.length) {
          return;
        }

        /*
         * Find faculty that can accommodate
         * the section without adjustment.
         */
        const fitting = candidates.filter(
          (item) =>
            Number(item.simulatedAvailable) >= Number(section.requiredUnits),
        );

        let selected;

        if (fitting.length) {
          /*
           * Balance:
           *
           * 1. Fewest assigned sections
           * 2. Lowest assigned units
           * 3. Highest remaining capacity
           * 4. Lowest current load
           */
          selected = [...fitting].sort((a, b) => {
            const sectionCountDiff =
              a.simulatedSections.length - b.simulatedSections.length;

            if (sectionCountDiff !== 0) {
              return sectionCountDiff;
            }

            const unitDiff =
              a.simulatedAssignedUnits - b.simulatedAssignedUnits;

            if (unitDiff !== 0) {
              return unitDiff;
            }

            const capacityDiff = b.simulatedAvailable - a.simulatedAvailable;

            if (capacityDiff !== 0) {
              return capacityDiff;
            }

            return Number(a.currentUnits) - Number(b.currentUnits);
          })[0];
        } else {
          /*
           * Nobody can fit without adjustment.
           *
           * Choose the faculty that needs the
           * smallest adjustment.
           */
          selected = [...candidates].sort((a, b) => {
            const aAdjustment = Math.max(
              0,
              Number(section.requiredUnits) - Number(a.simulatedAvailable),
            );

            const bAdjustment = Math.max(
              0,
              Number(section.requiredUnits) - Number(b.simulatedAvailable),
            );

            if (aAdjustment !== bAdjustment) {
              return aAdjustment - bAdjustment;
            }

            const sectionCountDiff =
              a.simulatedSections.length - b.simulatedSections.length;

            if (sectionCountDiff !== 0) {
              return sectionCountDiff;
            }

            return a.simulatedAssignedUnits - b.simulatedAssignedUnits;
          })[0];
        }

        if (!selected) {
          return;
        }

        const requiredAdjustment = this.roundUnits(
          Math.max(
            0,
            Number(section.requiredUnits) - Number(selected.simulatedAvailable),
          ),
        );

        const newUnitLoad = this.roundUnits(
          Number(selected.unitLoad || 0) + requiredAdjustment,
        );

        /*
         * Add to simulation.
         */
        selected.simulatedAssignedUnits = this.roundUnits(
          selected.simulatedAssignedUnits + Number(section.requiredUnits || 0),
        );

        selected.simulatedAvailable = this.roundUnits(
          selected.simulatedAvailable -
            Number(section.requiredUnits || 0) +
            requiredAdjustment,
        );

        selected.simulatedSections.push(section);

        assignments.push({
          classId: section.classId,

          unscheduledId: section.unscheduledId,

          section,

          courseId:
            group.sections.find(
              (item) => String(item.classId) === String(section.classId),
            )?.originalItem?.course_id || null,

          courseCode: group.courseCode,

          programCode: group.programCode,

          facultyId: selected.facultyId,

          facultyName: selected.facultyName,

          currentUnits: this.roundUnits(selected.currentUnits),

          availableCapacity: this.roundUnits(selected.availableCapacity),

          requiredUnits: this.roundUnits(section.requiredUnits),

          requiredAdjustment,

          newUnitLoad,

          status: requiredAdjustment > 0 ? "adjust_and_assign" : "ready",
        });
      });

      const assignedUnits = this.roundUnits(
        assignments.reduce(
          (sum, item) => sum + Number(item.requiredUnits || 0),
          0,
        ),
      );

      const remainingUnits = this.roundUnits(
        Math.max(0, Number(group.remainingUnits || 0) - assignedUnits),
      );

      const adjustmentCount = assignments.filter(
        (item) => Number(item.requiredAdjustment || 0) > 0,
      ).length;

      return {
        groupKey: group.key,

        courseCode: group.courseCode,

        programCode: group.programCode,

        requiredUnits: group.remainingUnits,

        assignedUnits,

        remainingUnits,

        adjustmentCount,

        assignments,
      };
    },

    async confirmAutoAssignment() {
      if (
        !this.autoAssignmentProposal ||
        !this.autoAssignmentProposal.assignments?.length
      ) {
        return;
      }

      this.savingAutoAssignment = true;

      try {
        const assignments = this.autoAssignmentProposal.assignments;

        /*
         * Save one by one.
         *
         * If your backend supports bulk assignment,
         * this can later be changed to a single request.
         */
        for (const assignment of assignments) {
          await this.saveAssignmentToDatabase(assignment);
        }

        /*
         * Refresh data after successful save.
         */
        await this.refreshAfterAssignment();

        this.showAutoAssignModal = false;

        this.autoAssignmentProposal = null;

        this.pendingAssignments = [];
      } catch (error) {
        console.error(
          "Failed to save automatic assignments:",
          error.response?.data || error.message || error,
        );
      } finally {
        this.savingAutoAssignment = false;
      }
    },

    /* ============================================================
     * INDIVIDUAL ASSIGNMENT
     * ========================================================== */

    openIndividualAssignModal(group, faculty) {
      if (!group || !faculty) {
        return;
      }

      const sections = group.unassignedSections || [];

      if (!sections.length) {
        return;
      }

      this.selectedAssignment = {
        groupKey: group.key,

        courseId: sections[0].originalItem?.course_id || null,

        courseCode: group.courseCode,
        programCode: group.programCode,

        facultyId: faculty.facultyId,
        facultyName: faculty.facultyName,

        currentUnits: this.roundUnits(faculty.currentUnits),
        availableCapacity: this.roundUnits(faculty.availableCapacity),

        availableSections: sections,

        selectedSectionIds: [],
        selectedSections: [],
        selectedTotalUnits: 0,

        requiredAdjustment: 0,
        newUnitLoad: this.roundUnits(faculty.unitLoad),
      };
      this.refreshSelectedAssignment();

      this.showAssignModal = true;
    },

    closeAssignModal() {
      this.showAssignModal = false;
      this.selectedAssignment = null;
    },
    refreshSelectedAssignment() {
      if (!this.selectedAssignment) {
        return;
      }

      const selectedIds = this.selectedAssignment.selectedSectionIds || [];

      const selectedSections =
        this.selectedAssignment.availableSections?.filter((section) =>
          selectedIds.some((id) => String(id) === String(section.classId)),
        ) || [];

      // TOTAL UNITS OF ALL SELECTED CLASSES
      const totalUnits = this.roundUnits(
        selectedSections.reduce(
          (total, section) => total + Number(section.requiredUnits || 0),
          0,
        ),
      );

      // CURRENT AVAILABLE CAPACITY
      const availableCapacity = this.roundUnits(
        Number(this.selectedAssignment.availableCapacity || 0),
      );

      // HOW MANY EXTRA MAXIMUM UNITS ARE REQUIRED
      const requiredAdjustment = this.roundUnits(
        Math.max(0, totalUnits - availableCapacity),
      );

      const faculty = this.rawUsers.find(
        (user) => Number(user.id) === Number(this.selectedAssignment.facultyId),
      );

      const unitLoad = this.roundUnits(
        faculty?.unit_load ?? this.selectedAssignment.unitLoad ?? 0,
      );

      const newUnitLoad = this.roundUnits(unitLoad + requiredAdjustment);

      // Update the existing reactive object.
      this.selectedAssignment.selectedSections = selectedSections;
      this.selectedAssignment.selectedTotalUnits = totalUnits;
      this.selectedAssignment.requiredAdjustment = requiredAdjustment;
      this.selectedAssignment.newUnitLoad = newUnitLoad;
    },

    async confirmIndividualAssignment() {
      const selected = this.selectedAssignment;

      if (!selected || !selected.selectedSectionIds?.length) {
        return;
      }

      const selectedSections = selected.availableSections.filter((section) =>
        selected.selectedSectionIds.some(
          (id) => String(id) === String(section.classId),
        ),
      );

      if (!selectedSections.length) {
        return;
      }

      const totalUnits = this.roundUnits(
        selectedSections.reduce(
          (total, section) => total + Number(section.requiredUnits || 0),
          0,
        ),
      );

      const availableCapacity = Number(selected.availableCapacity || 0);

      const requiredAdjustment = this.roundUnits(
        Math.max(0, totalUnits - availableCapacity),
      );

      const faculty = this.rawUsers.find(
        (user) => Number(user.id) === Number(selected.facultyId),
      );

      const unitLoad = Number(faculty?.unit_load || selected.unitLoad || 0);

      const newUnitLoad = this.roundUnits(unitLoad + requiredAdjustment);

      /*
       * If selected sections exceed available capacity,
       * adjust the faculty unit load first.
       */
      if (requiredAdjustment > 0) {
        this.showAssignModal = false;

        this.openAdjustUnitModal(
          {
            facultyId: selected.facultyId,
            facultyName: selected.facultyName,
            unitLoad,
          },
          {
            facultyId: selected.facultyId,
            facultyName: selected.facultyName,

            courseId: selected.courseId,
            courseCode: selected.courseCode,
            programCode: selected.programCode,

            sections: selectedSections,

            totalUnits,
            requiredAdjustment,
            newUnitLoad,
          },
        );

        return;
      }

      this.savingAssignment = true;

      try {
        for (const section of selectedSections) {
          const assignment = {
            classId: section.classId,
            unscheduledId: section.unscheduledId,

            section,

            courseId: selected.courseId,
            courseCode: selected.courseCode,
            programCode: selected.programCode,

            facultyId: Number(selected.facultyId),
            facultyName: selected.facultyName,

            currentUnits: this.roundUnits(selected.currentUnits),

            availableCapacity: this.roundUnits(availableCapacity),

            requiredUnits: this.roundUnits(section.requiredUnits),

            requiredAdjustment: 0,

            newUnitLoad: this.roundUnits(unitLoad),

            status: "ready",
          };

          await this.saveAssignmentToDatabase(assignment);
        }

        await this.refreshAfterAssignment();

        this.closeAssignModal();
      } catch (error) {
        console.error(
          "Failed to assign multiple sections:",
          error.response?.data || error.message || error,
        );

        alert(
          error.response?.data?.message ||
            error.message ||
            "Failed to assign sections.",
        );
      } finally {
        this.savingAssignment = false;
      }
    },

    /* ============================================================
     * SAVE ASSIGNMENT
     * ========================================================== */

    async saveAssignmentToDatabase(assignment) {
      if (!assignment) {
        throw new Error("Assignment is required.");
      }

      const facultyId = Number(assignment.facultyId);
      const classId = assignment.classId;
      const unscheduledId = assignment.unscheduledId;

      if (!facultyId) {
        throw new Error("Faculty ID is required.");
      }

      if (!classId) {
        throw new Error("Class ID is required.");
      }

      if (!unscheduledId) {
        throw new Error("Unscheduled meeting ID is required.");
      }

      /*
       * ============================================================
       * 1. ASSIGN FACULTY FIRST
       * ============================================================
       */
      await axios.patch(`${this.ASSIGNMENT_API}/${unscheduledId}`, {
        faculty_name: assignment.facultyName,
      });

      /*
       * ============================================================
       * 2. AFTER ASSIGNING, ADJUST ONLY FACULTY UNIT LOAD
       * ============================================================
       */
      if (Number(assignment.requiredAdjustment || 0) > 0) {
        await axios.patch(`http://localhost:8000/users/${facultyId}`, {
          unit_load: Number(assignment.newUnitLoad),
        });
      }

      /*
       * ============================================================
       * 3. LOCAL UI STATE
       * ============================================================
       */
      this.localAssignments[String(classId)] = {
        ...assignment,
        classId,
        facultyId,
        facultyName: assignment.facultyName,
      };
    },

    /* ============================================================
     * REFRESH
     * ========================================================== */

    async refreshAfterAssignment() {
      const requests = [];

      if (typeof this.fetchDataStore.fetchUnscheduledMeetings === "function") {
        requests.push(this.fetchDataStore.fetchUnscheduledMeetings());
      }

      if (typeof this.fetchDataStore.fetchRawUsers === "function") {
        requests.push(this.fetchDataStore.fetchRawUsers());
      }

      if (typeof this.fetchDataStore.fetchFinalSchedules === "function") {
        requests.push(this.fetchDataStore.fetchFinalSchedules());
      }

      await Promise.all(requests);
    },

    /* ============================================================
     * LOCAL ASSIGNMENTS
     * ========================================================== */

    getLocalAssignmentsForGroup(group) {
      if (!group) {
        return [];
      }

      return Object.values(this.localAssignments).filter((assignment) => {
        return (
          this.normalizeValue(assignment.courseCode) ===
            this.normalizeValue(group.courseCode) &&
          this.normalizeValue(assignment.programCode) ===
            this.normalizeValue(group.programCode)
        );
      });
    },

    isSectionAssigned(classId, courseCode) {
      if (!classId || !courseCode) {
        return false;
      }

      const normalizedClassId = String(classId);
      const normalizedCourseCode = this.normalizeValue(courseCode);

      /*
       * ============================================================
       * 1. LOCAL ASSIGNMENT
       * ============================================================
       *
       * The set/class AND course code must match.
       */
      const localAssignment = Object.values(this.localAssignments).find(
        (assignment) => {
          const assignmentClassId = String(
            assignment.classId ||
              assignment.class_id ||
              assignment.section?.classId ||
              "",
          );

          const assignmentCourseCode = this.normalizeValue(
            assignment.courseCode ||
              assignment.course_code ||
              assignment.section?.courseCode ||
              "",
          );

          return (
            assignmentClassId === normalizedClassId &&
            assignmentCourseCode === normalizedCourseCode
          );
        },
      );

      if (localAssignment) {
        return true;
      }

      /*
       * ============================================================
       * 2. DATABASE ASSIGNMENT
       * ============================================================
       *
       * The set/class AND course code must both match.
       */
      return this.unscheduledMeetings.some((item) => {
        const itemClassId = String(
          item.class_id || item.classId || item.id || "",
        );

        if (itemClassId !== normalizedClassId) {
          return false;
        }

        const itemCourseCode = this.normalizeValue(
          item.course_code || item.courseCode || "",
        );

        /*
         * IMPORTANT:
         * Same set/class but DIFFERENT course = NOT assigned.
         */
        if (itemCourseCode !== normalizedCourseCode) {
          return false;
        }

        const facultyName = String(item.faculty_name || "").trim();

        if (facultyName && facultyName.toLowerCase() !== "unassigned") {
          return true;
        }

        const status = String(item.status || "").toLowerCase();

        return status === "assigned" || status === "assign";
      });
    },

    getSectionDisplay(section) {
      if (!section) {
        return "—";
      }

      /*
       * Prefer set name when available.
       */
      if (section.setName) {
        return `${section.setName} / ${section.classId}`;
      }

      return `Class ${section.classId}`;
    },

    /* ============================================================
     * ADJUST FACULTY UNIT LOAD
     * ========================================================== */

    openAdjustUnitModal(faculty, assignment = null) {
      const facultyId = faculty?.facultyId || faculty?.id;

      if (!facultyId) {
        console.error("Faculty ID is missing.");
        return;
      }

      const rawUser = this.rawUsers.find(
        (user) => Number(user.id) === Number(facultyId),
      );

      if (!rawUser) {
        console.error("Faculty not found:", facultyId);
        return;
      }

      this.selectedFaculty = {
        id: Number(rawUser.id),
        name: this.getUserName(rawUser),
        email: rawUser.email || "",
        programCode:
          rawUser.program_code || rawUser.program?.program_code || "—",
        unitLoad: this.roundUnits(rawUser.unit_load),
      };

      /*
       * Keep the assignment when this modal was opened
       * from the Assign -> Adjust & Assign flow.
       */
      this.adjustmentAssignment = assignment
        ? {
            ...assignment,
            facultyId: Number(rawUser.id),
            facultyName: this.getUserName(rawUser),
          }
        : null;

      /*
       * If assignment exists, calculate the minimum required
       * additional units automatically.
       */
      if (assignment) {
        // Use the TOTAL of the selected sections.
        // Do not use assignment.requiredUnits because
        // multiple selected sections are stored in totalUnits.
        const selectedTotalUnits = this.roundUnits(
          Number(assignment.totalUnits || 0),
        );

        const availableCapacity = this.roundUnits(
          Number(assignment.availableCapacity || 0),
        );

        // Only increase the maximum unit load by the amount
        // that exceeds the faculty's available capacity.
        const requiredAdjustment = this.roundUnits(
          Math.max(0, selectedTotalUnits - availableCapacity),
        );

        const newUnitLoad = this.roundUnits(
          Number(rawUser.unit_load || 0) + requiredAdjustment,
        );

        this.adjustmentAssignment = {
          ...this.adjustmentAssignment,

          totalUnits: selectedTotalUnits,
          requiredAdjustment,
          newUnitLoad,
        };

        // Automatically show the required additional units.
        this.plusUnit = requiredAdjustment;

        this.adjustedUnitLoad = newUnitLoad;
      } else {
        this.plusUnit = 0;

        this.adjustedUnitLoad = this.roundUnits(Number(rawUser.unit_load || 0));
      }

      this.showAdjustUnitModal = true;
    },

    closeAdjustUnitModal() {
      if (this.savingUnitLoad) {
        return;
      }

      this.showAdjustUnitModal = false;

      this.selectedFaculty = null;

      this.adjustedUnitLoad = 0;

      this.plusUnit = 0;

      this.adjustmentAssignment = null;
    },

    async saveAdjustedUnit() {
      if (!this.selectedFaculty) {
        return;
      }

      const facultyId = Number(this.selectedFaculty.id);
      const newUnitLoad = Number(this.adjustedUnitLoad);

      if (!facultyId) {
        alert("Faculty ID is missing.");
        return;
      }

      if (Number.isNaN(newUnitLoad) || newUnitLoad < 0) {
        alert("Please enter a valid unit load.");
        return;
      }

      this.savingUnitLoad = true;

      try {
        console.log("Updating faculty unit load:", {
          facultyId,
          newUnitLoad,
        });

        await axios.patch(`http://localhost:8000/users/${facultyId}`, {
          unit_load: newUnitLoad,
        });

        if (typeof this.fetchDataStore.fetchRawUsers === "function") {
          await this.fetchDataStore.fetchRawUsers();
        }

        this.closeAdjustUnitModal();
      } catch (error) {
        console.error(
          "Failed to update faculty unit load:",
          error.response?.data || error.message || error,
        );

        alert(
          error.response?.data?.message ||
            error.message ||
            "Failed to update faculty unit load.",
        );
      } finally {
        this.savingUnitLoad = false;
      }
    },

    /*
     * Adjust unit AND assign section.
     */
    async saveAdjustedUnitAndAssign() {
      if (!this.adjustmentAssignment || !this.selectedFaculty) {
        return;
      }

      const assignment = this.adjustmentAssignment;

      const sections = Array.isArray(assignment.sections)
        ? assignment.sections
        : assignment.section
        ? [assignment.section]
        : [];

      if (!sections.length) {
        alert("Please select at least one section.");
        return;
      }

      const facultyId = Number(this.selectedFaculty.id);
      const facultyName = this.selectedFaculty.name;

      const newUnitLoad = this.roundUnits(this.adjustedUnitLoad);

      const requiredAdjustment = this.roundUnits(
        Math.max(0, newUnitLoad - Number(this.selectedFaculty.unitLoad || 0)),
      );

      this.savingUnitLoad = true;

      try {
        /*
         * IMPORTANT:
         * Assign EVERY selected section.
         *
         * The unit adjustment is applied only once to the
         * faculty maximum unit load.
         */
        for (const section of sections) {
          const sectionAssignment = {
            classId: section.classId,
            unscheduledId: section.unscheduledId,

            section,

            courseId: assignment.courseId,
            courseCode: assignment.courseCode,
            programCode: assignment.programCode,

            facultyId,
            facultyName,

            currentUnits: this.roundUnits(
              assignment.currentUnits || this.selectedFaculty.currentUnits || 0,
            ),

            availableCapacity: this.roundUnits(
              assignment.availableCapacity || 0,
            ),

            requiredUnits: this.roundUnits(section.requiredUnits || 0),

            /*
             * Do NOT apply the full adjustment to every section.
             * The faculty unit load is updated only once below.
             */
            requiredAdjustment: 0,

            newUnitLoad,

            status: "Assigned",
          };

          await this.saveAssignmentToDatabase(sectionAssignment);
        }

        /*
         * Update the faculty maximum unit load ONCE.
         */
        if (requiredAdjustment > 0) {
          await axios.patch(`http://localhost:8000/users/${facultyId}`, {
            unit_load: newUnitLoad,
          });
        }

        await this.refreshAfterAssignment();

        /*
         * Close both modals after successful assignment.
         */
        this.showAssignModal = false;
        this.selectedAssignment = null;
        this.showAdjustUnitModal = false;
        this.closeAdjustUnitModal();
      } catch (error) {
        console.error(
          "Failed to assign selected sections and adjust faculty:",
          error.response?.data || error.message || error,
        );

        alert(
          error.response?.data?.message ||
            error.message ||
            "Failed to assign sections and adjust faculty unit.",
        );
      } finally {
        this.savingUnitLoad = false;
      }
    },

    /* ============================================================
     * ROUNDING
     * ========================================================== */

    roundUnits(value) {
      const number = Number(value);

      if (!Number.isFinite(number)) {
        return 0;
      }

      return Number(number.toFixed(2));
    },

    /* ============================================================
     * LOAD DATA
     * ========================================================== */

    async loadFacultyAdjustmentData() {
      this.loading = true;

      try {
        const requests = [];

        if (typeof this.fetchDataStore.fetchClassSections === "function") {
          requests.push(this.fetchDataStore.fetchClassSections());
        }

        if (typeof this.fetchDataStore.fetchFinalSchedules === "function") {
          requests.push(this.fetchDataStore.fetchFinalSchedules());
        }

        if (
          typeof this.fetchDataStore.fetchUnscheduledMeetings === "function"
        ) {
          requests.push(this.fetchDataStore.fetchUnscheduledMeetings());
        }

        if (typeof this.fetchDataStore.fetchCourses === "function") {
          requests.push(this.fetchDataStore.fetchCourses());
        }

        if (typeof this.fetchDataStore.fetchRawUsers === "function") {
          requests.push(this.fetchDataStore.fetchRawUsers());
        }

        await Promise.all(requests);
      } catch (error) {
        console.error("Failed to load faculty adjustment data:", error);
      } finally {
        this.loading = false;
      }
    },

    /* ============================================================
     * COURSE LOOKUP
     * ========================================================== */

    getCourse(item) {
      if (!item) {
        return null;
      }

      /*
       * COURSE ID
       */
      if (item.course_id) {
        const courseById = this.courses.find(
          (course) => Number(course.course_id) === Number(item.course_id),
        );

        if (courseById) {
          return courseById;
        }
      }

      /*
       * COURSE CODE
       */
      const courseCode = String(item.course_code || "")
        .trim()
        .toLowerCase();

      if (courseCode) {
        const courseByCode = this.courses.find(
          (course) =>
            String(course.course_code || "")
              .trim()
              .toLowerCase() === courseCode,
        );

        if (courseByCode) {
          return courseByCode;
        }
      }

      return null;
    },

    getCourseTitle(item) {
      const course = this.getCourse(item);

      return (
        course?.course_title ||
        course?.course_name ||
        "Course title unavailable"
      );
    },

    /* ============================================================
     * REQUIRED TEACHING UNITS
     *
     * Lecture = 1 teaching unit
     * Laboratory = 2.25 teaching units
     * ========================================================== */

    getRequiredUnits(item) {
      if (!item) {
        return 0;
      }

      const course = this.getCourse(item);

      if (!course) {
        return 0;
      }

      const lectureUnits = Number(course.course_lec) || 0;

      const laboratoryUnits = Number(course.course_lab) || 0;

      const lectureTeachingUnits = lectureUnits;

      const laboratoryTeachingUnits = laboratoryUnits * 2.25;

      return this.roundUnits(lectureTeachingUnits + laboratoryTeachingUnits);
    },

    getScheduleUnits(schedule) {
      return this.getRequiredUnits(schedule);
    },

    /* ============================================================
     * FACULTY NAME
     * ========================================================== */

    getUserName(user) {
      if (!user) {
        return "Unknown Faculty";
      }

      const name = [user.first_name, user.middle_name, user.last_name]
        .filter(Boolean)
        .join(" ")
        .trim();

      return name || user.name || user.faculty_name || "Unknown Faculty";
    },

    normalizeName(name) {
      return String(name || "")
        .toLowerCase()
        .replace(/\s+/g, " ")
        .trim();
    },

    normalizeValue(value) {
      return String(value || "")
        .trim()
        .toLowerCase();
    },

    findFacultyByName(name) {
      if (!name) {
        return null;
      }

      const target = this.normalizeName(name);

      return this.rawUsers.find((user) => {
        const firstName = String(user.first_name || "").trim();

        const middleName = String(user.middle_name || "").trim();

        const lastName = String(user.last_name || "").trim();

        const fullName = [firstName, middleName, lastName]
          .filter(Boolean)
          .join(" ");

        const firstLastName = [firstName, lastName].filter(Boolean).join(" ");

        return (
          this.normalizeName(fullName) === target ||
          this.normalizeName(firstLastName) === target
        );
      });
    },

    /* ============================================================
     * POSSIBLE FACULTY
     * ========================================================== */

    getPossibleFaculty(item) {
      const candidates = [];
      const usedNames = new Set();

      /*
       * Faculty already assigned to another section
       * of the same COURSE + PROGRAM.
       *
       * Normally we don't show them again.
       *
       * EXCEPTION:
       * If that faculty is the ONLY possible faculty
       * remaining for the unresolved section, keep them visible.
       *
       * Example:
       *   Section A -> Faculty Juan
       *   Section B -> possible faculty: Juan
       *
       * Juan must remain visible so Section B can still
       * be assigned to him.
       */
      const alreadyAssignedFaculty = new Set();

      this.unscheduledMeetings.forEach((other) => {
        if (String(other.id) === String(item.id)) {
          return;
        }

        const sameCourse =
          this.normalizeValue(other.course_code) ===
          this.normalizeValue(item.course_code);

        const sameProgram =
          this.normalizeValue(other.program_code) ===
          this.normalizeValue(item.program_code);

        if (!sameCourse || !sameProgram) {
          return;
        }

        const facultyName = String(other.faculty_name || "").trim();

        if (!facultyName || facultyName.toLowerCase() === "unassigned") {
          return;
        }

        alreadyAssignedFaculty.add(this.normalizeName(facultyName));
      });

      /*
       * CURRENT FACULTY
       */
      if (
        item.faculty_name &&
        String(item.faculty_name).trim().toLowerCase() !== "unassigned"
      ) {
        usedNames.add(this.normalizeName(String(item.faculty_name).trim()));
      }

      /*
       * POSSIBLE FACULTY
       */
      const names = this.extractFacultyNames(item.reason);

      /*
       * First resolve all possible faculty names.
       * We need this before filtering because we must know
       * how many possible faculty remain.
       */
      const resolvedCandidates = [];

      names.forEach((name) => {
        const cleanName = String(name || "").trim();

        if (!cleanName) {
          return;
        }

        const key = this.normalizeName(cleanName);

        if (usedNames.has(key)) {
          return;
        }

        if (this.shouldHideUnresolvedFaculty(item, key)) {
          return;
        }

        const faculty = this.findFacultyByName(cleanName);

        if (!faculty) {
          return;
        }

        const facultyKey = this.normalizeName(this.getUserName(faculty));

        if (usedNames.has(facultyKey)) {
          return;
        }

        const candidate = this.buildFacultyCandidate(faculty);

        if (!candidate) {
          return;
        }

        resolvedCandidates.push({
          key: facultyKey,
          candidate,
          alreadyAssigned: alreadyAssignedFaculty.has(facultyKey),
        });
      });

      /*
       * IMPORTANT:
       *
       * Count the faculty that can still potentially handle
       * this unresolved section.
       */
      const remainingPossibleFaculty = resolvedCandidates.filter(
        (item) => !item.alreadyAssigned,
      );

      /*
       * Add candidates.
       */
      resolvedCandidates.forEach((item) => {
        /*
         * Normally don't show a faculty that is already assigned
         * to another section of this same course/program.
         */
        if (item.alreadyAssigned) {
          /*
           * EXCEPTION:
           *
           * If there is NO other possible faculty left,
           * this faculty is the ONLY remaining option.
           *
           * Keep the faculty visible.
           */
          if (remainingPossibleFaculty.length > 0) {
            return;
          }
        }

        if (usedNames.has(item.key)) {
          return;
        }

        usedNames.add(item.key);
        candidates.push(item.candidate);
      });

      return candidates;
    },

    /* ============================================================
     * UNRESOLVED FACULTY PROTECTION
     * ========================================================== */

    /* ============================================================
     * UNRESOLVED FACULTY PROTECTION
     * ========================================================== */
    shouldHideUnresolvedFaculty(item, facultyName) {
      if (!item || !facultyName) {
        return false;
      }

      /*
       * IMPORTANT:
       * If this record is already assigned, do NOT hide
       * the faculty even if the old reason still says
       * "unresolved after repair pass".
       */
      const status = String(item.status || "")
        .trim()
        .toLowerCase();

      const facultyAssigned = String(item.faculty_name || "")
        .trim()
        .toLowerCase();

      if (
        status === "assigned" ||
        status === "assign" ||
        (facultyAssigned && facultyAssigned !== "unassigned")
      ) {
        return false;
      }

      const reason = String(item.reason || "").toLowerCase();

      if (!reason.includes("unresolved after repair pass")) {
        return false;
      }

      const targetName = this.normalizeName(facultyName);

      return this.unscheduledMeetings.some((other) => {
        if (String(other.id) === String(item.id)) {
          return false;
        }

        const sameCourse =
          this.normalizeValue(other.course_code) ===
          this.normalizeValue(item.course_code);

        const sameProgram =
          this.normalizeValue(other.program_code) ===
          this.normalizeValue(item.program_code);

        if (!sameCourse || !sameProgram) {
          return false;
        }

        /*
         * If the other record is already assigned,
         * it must not cause the faculty to be hidden.
         */
        const otherStatus = String(other.status || "")
          .trim()
          .toLowerCase();

        const otherFaculty = String(other.faculty_name || "")
          .trim()
          .toLowerCase();

        if (
          otherStatus === "assigned" ||
          otherStatus === "assign" ||
          (otherFaculty && otherFaculty !== "unassigned")
        ) {
          return false;
        }

        const otherReason = String(other.reason || "").toLowerCase();

        if (!otherReason.includes("no faculty assignment")) {
          return false;
        }

        const possibleFaculty = this.extractFacultyNames(other.reason);

        return possibleFaculty.some(
          (name) => this.normalizeName(name) === targetName,
        );
      });
    },

    /* ============================================================
     * BUILD FACULTY CANDIDATE
     * ========================================================== */

    buildFacultyCandidate(faculty) {
      if (!faculty || !faculty.id) {
        return null;
      }

      const rawFaculty = this.rawUsers.find(
        (user) => Number(user.id) === Number(faculty.id),
      );

      if (!rawFaculty) {
        return null;
      }

      const currentUnits = this.roundUnits(
        this.getFacultyCurrentUnits(rawFaculty.id),
      );

      const unitLoad = this.roundUnits(rawFaculty.unit_load);

      const availableCapacity = this.roundUnits(
        Math.max(0, unitLoad - currentUnits),
      );

      return {
        id: rawFaculty.id,

        name: this.getUserName(rawFaculty),

        programCode:
          rawFaculty.program_code || rawFaculty.program?.program_code || "—",

        unitLoad,

        unit_load: unitLoad,

        currentUnits,

        availableCapacity,

        facultyFound: true,
      };
    },

    /* ============================================================
     * EXTRACT FACULTY NAMES
     * ========================================================== */

    extractFacultyNames(reason) {
      if (!reason) {
        return [];
      }

      const text = String(reason);

      const match = text.match(/possible\s+faculty\s*:\s*(.*)$/i);

      if (!match) {
        return [];
      }

      let facultyText = match[1].trim();

      facultyText = facultyText
        .replace(/\s+and\s+hy\s*$/i, "")
        .replace(/\s+and\s+h(y)?\s*$/i, "")
        .trim();

      if (!facultyText) {
        return [];
      }

      const parts = facultyText
        .split(",")
        .map((name) =>
          name
            .trim()
            .replace(/[.;]+$/, "")
            .trim(),
        )
        .filter(Boolean);

      const names = [];

      parts.forEach((part) => {
        const andParts = part.split(/\s+and\s+/i);

        andParts.forEach((name) => {
          const clean = name.trim();

          if (clean) {
            names.push(clean);
          }
        });
      });

      /*
       * Remove duplicates.
       */
      const unique = [];

      const seen = new Set();

      names.forEach((name) => {
        const key = this.normalizeName(name);

        if (!seen.has(key)) {
          seen.add(key);

          unique.push(name);
        }
      });

      return unique;
    },

    /* ============================================================
     * FACULTY CURRENT LOAD
     * ========================================================== */

    getFacultyCurrentUnits(facultyId) {
      const faculty = this.facultyLoadAssessment.find(
        (item) => Number(item.id) === Number(facultyId),
      );

      return faculty ? this.roundUnits(faculty.currentUnits) : 0;
    },
  },
};
</script>
