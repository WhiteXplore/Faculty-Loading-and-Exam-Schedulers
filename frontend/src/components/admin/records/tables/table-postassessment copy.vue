<template>
  <div class="min-h-screen bg-gray-50 p-2 text-gray-800">
    <!-- =========================================================
         TABS
    ========================================================== -->
    <div class="mt-4 flex items-center justify-between">
      <div class="flex gap-1">
        <!-- Assessment Result -->
        <button
          type="button"
          @click="activeTab = 'result'"
          :class="[
            'px-4 py-2 rounded-t-lg text-sm border transition-all flex items-center gap-2',
            activeTab === 'result'
              ? 'bg-defaultGreen text-white border-gray-300 border-b-white shadow-sm'
              : 'bg-gray-100 text-gray-600 border-transparent hover:bg-gray-200',
          ]"
        >
          <span>Assessment Result</span>
        </button>

        <!-- Recommendations -->
        <button
          type="button"
          @click="activeTab = 'suggestion'"
          :class="[
            'px-4 py-2 rounded-t-lg text-sm border transition-all flex items-center gap-2',
            activeTab === 'suggestion'
              ? 'bg-defaultGreen text-white border-gray-300 border-b-white shadow-sm'
              : 'bg-gray-100 text-gray-600 border-transparent hover:bg-gray-200',
          ]"
        >
          <span>Recommendations</span>
        </button>
      </div>
    </div>

    <!-- =========================================================
         RESULT TAB
    ========================================================== -->
    <div v-if="activeTab === 'result'">
      <!-- SECTION HEADER -->
      <div class="mb-4">
        <h3 class="text-base font-bold text-gray-900">Scheduling Assessment</h3>

        <p class="mt-1 text-xs text-gray-500">
          Summary of classes successfully scheduled and classes that still
          require intervention.
        </p>
      </div>

      <!-- =======================================================
           RESULT CARDS
      ======================================================== -->
      <div class="mb-8 grid grid-cols-1 gap-4 md:grid-cols-3">
        <!-- Scheduled -->
        <div
          class="rounded-lg border border-gray-200 border-l-4 border-l-green-500 bg-white p-5"
        >
          <p class="text-xs font-medium text-gray-500">Scheduled Classes</p>

          <p class="mt-2 text-2xl font-bold text-gray-900">
            {{ scheduledClasses.length }}
          </p>

          <p class="mt-2 text-xs leading-5 text-gray-400">
            Classes successfully assigned to a faculty and schedule.
          </p>
        </div>

        <!-- Unscheduled -->
        <div
          class="rounded-lg border border-gray-200 border-l-4 border-l-red-500 bg-white p-5"
        >
          <p class="text-xs font-medium text-gray-500">Unscheduled Classes</p>

          <p class="mt-2 text-2xl font-bold text-red-600">
            {{ unscheduledMeetings.length }}
          </p>

          <p class="mt-2 text-xs leading-5 text-gray-400">
            Classes that require manual adjustment or additional faculty.
          </p>
        </div>

        <!-- Units -->
        <div class="rounded-lg border border-gray-200 bg-white p-5">
          <p class="text-xs font-medium text-gray-500">
            Required Unscheduled Units
          </p>

          <p class="mt-2 text-2xl font-bold text-gray-900">
            {{ totalUnscheduledUnits }}
          </p>

          <p class="mt-2 text-xs leading-5 text-gray-400">
            Total teaching units that still need to be assigned.
          </p>
        </div>
      </div>

      <!-- =======================================================
           UNSCHEDULED CLASSES
      ======================================================== -->
      <div class="mb-4">
        <h3 class="text-base font-bold text-gray-900">Unscheduled Classes</h3>

        <p class="mt-1 text-xs text-gray-500">
          Classes that could not be completely assigned during the scheduling
          process.
        </p>
      </div>

      <div
        v-if="unscheduledMeetings.length"
        class="overflow-hidden rounded-lg border border-gray-200 bg-white"
      >
        <div class="overflow-x-auto">
          <table class="w-full min-w-[1200px] text-left">
            <thead class="border-b border-gray-200 bg-gray-50">
              <tr>
                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Course
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Program
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Type
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Required Units
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Faculty
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Assessment
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Reason
                </th>
              </tr>
            </thead>

            <tbody class="divide-y divide-gray-100">
              <tr
                v-for="item in unscheduledMeetings"
                :key="item.id"
                class="transition hover:bg-gray-50"
              >
                <!-- COURSE -->
                <td class="px-4 py-4">
                  <div class="font-semibold text-gray-900">
                    {{ item.course_code || "—" }}
                  </div>

                  <div class="mt-1 text-[10px] text-gray-400">
                    {{ getCourseTitle(item) }}
                  </div>
                </td>

                <!-- PROGRAM -->
                <td class="px-4 py-4">
                  <span
                    class="rounded bg-gray-100 px-2 py-1 text-[10px] font-bold text-gray-600"
                  >
                    {{ item.program_code || "—" }}
                  </span>
                </td>

                <!-- TYPE -->
                <td class="px-4 py-4 text-xs text-gray-600">
                  {{ item.type || "—" }}
                </td>

                <!-- UNITS -->
                <td class="px-4 py-4">
                  <span class="font-bold text-gray-900">
                    {{ getRequiredUnits(item) }}
                  </span>
                </td>

                <!-- FACULTY -->
                <td class="px-4 py-4 text-xs text-gray-700">
                  {{ item.faculty_name || "Unassigned" }}
                </td>

                <!-- ASSESSMENT -->
                <td class="px-4 py-4">
                  <span
                    :class="[
                      'inline-flex rounded px-2 py-1 text-[10px] font-bold',
                      getAssessmentStatus(item) === 'danger'
                        ? 'bg-red-100 text-red-700'
                        : getAssessmentStatus(item) === 'warning'
                        ? 'bg-amber-100 text-amber-700'
                        : 'bg-gray-100 text-gray-600',
                    ]"
                  >
                    {{ getAssessmentLabel(item) }}
                  </span>
                </td>

                <!-- REASON -->
                <td
                  class="max-w-[420px] px-4 py-4 text-xs leading-5 text-gray-500"
                >
                  {{ item.reason || "No reason provided." }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- EMPTY -->
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
          All Classes Were Scheduled
        </h3>

        <p class="mt-1 text-xs text-gray-400">
          No unresolved class assignments were recorded.
        </p>
      </div>

      <!-- =======================================================
           FACULTY LOAD ASSESSMENT
      ======================================================== -->
      <div class="mb-4 mt-8">
        <h3 class="text-base font-bold text-gray-900">
          Faculty Load Assessment
        </h3>

        <p class="mt-1 text-xs text-gray-500">
          Current faculty loads calculated from the finalized schedules.
        </p>
      </div>

      <div class="overflow-hidden rounded-lg border border-gray-200 bg-white">
        <div class="overflow-x-auto">
          <table class="w-full min-w-[1000px] text-left">
            <thead class="border-b border-gray-200 bg-gray-50">
              <tr>
                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Faculty
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Program
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Maximum Load
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Current Load
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Available Capacity
                </th>

                <th
                  class="px-4 py-3 text-[10px] font-bold uppercase tracking-wide text-gray-500"
                >
                  Status
                </th>
              </tr>
            </thead>

            <tbody class="divide-y divide-gray-100">
              <tr
                v-for="faculty in facultyLoadAssessment"
                :key="faculty.id"
                class="hover:bg-gray-50"
              >
                <td class="px-4 py-4">
                  <div class="font-semibold text-gray-900">
                    {{ faculty.name }}
                  </div>

                  <div class="mt-1 text-[10px] text-gray-400">
                    {{ faculty.email || "—" }}
                  </div>
                </td>

                <td class="px-4 py-4 text-xs text-gray-600">
                  {{ faculty.programCode || "—" }}
                </td>

                <td class="px-4 py-4 text-xs text-gray-700">
                  {{ faculty.unitLoad }}
                </td>

                <td class="px-4 py-4">
                  <span class="font-bold text-gray-900">
                    {{ faculty.currentUnits }}
                  </span>
                </td>

                <td class="px-4 py-4">
                  <span
                    :class="[
                      'font-bold',
                      faculty.remainingCapacity > 0
                        ? 'text-green-600'
                        : faculty.remainingCapacity === 0
                        ? 'text-red-600'
                        : 'text-red-700',
                    ]"
                  >
                    {{ faculty.remainingCapacity }}
                  </span>
                </td>

                <td class="px-4 py-4">
                  <span
                    :class="[
                      'inline-flex rounded px-2 py-1 text-[10px] font-bold',
                      faculty.statusClass === 'available'
                        ? 'bg-green-100 text-green-700'
                        : faculty.statusClass === 'limited'
                        ? 'bg-amber-100 text-amber-700'
                        : faculty.statusClass === 'full'
                        ? 'bg-red-100 text-red-700'
                        : 'bg-red-100 text-red-700',
                    ]"
                  >
                    {{ faculty.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- =========================================================
         RECOMMENDATIONS TAB
    ========================================================== -->
    <div v-if="activeTab === 'suggestion'">
      <!-- HEADER -->
      <div class="mb-5">
        <h3 class="text-base font-bold text-gray-900">
          Faculty Adjustment Recommendations
        </h3>

        <p class="mt-1 text-xs leading-5 text-gray-500">
          Suggested faculty assignments based on their current teaching load and
          the faculty identified during the scheduling assessment.
        </p>
      </div>

      <!-- =======================================================
     RECOMMENDATIONS BY CLASS
======================================================== -->
      <div
        v-if="groupedRecommendations.length"
        class="space-y-5 h-[55vh] overflow-y-auto"
      >
        <div
          v-for="item in groupedRecommendations"
          :key="item.classId"
          class="overflow-hidden rounded-lg border border-gray-200 bg-white"
        >
          <!-- =====================================================
         CLASS HEADER
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

                <!-- CLASSES -->
                <div class="mt-3 flex flex-wrap items-center gap-2">
                  <span
                    class="text-[10px] font-medium uppercase tracking-wide text-gray-400"
                  >
                    Classes
                  </span>

                  <span
                    v-for="classItem in item.classes"
                    :key="classItem.classId"
                    class="rounded bg-white px-2 py-1 text-[10px] font-bold text-gray-700 ring-1 ring-gray-200"
                  >
                    {{ classItem.classId }}
                  </span>
                </div>
              </div>

              <!-- SUMMARY -->
              <div class="flex items-center gap-6">
                <!-- REQUIRED -->
                <div>
                  <p class="text-[10px] font-medium text-gray-400">Required</p>

                  <p class="mt-1 text-lg font-bold text-gray-900">
                    {{ item.requiredUnits }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- =====================================================
         FACULTY ALLOCATION TABLE
    ====================================================== -->
          <!-- =====================================================
     FACULTY ALLOCATION TABLE
====================================================== -->
          <div class="overflow-x-auto">
            <!-- SUGGESTION MODE -->
            <div class="mb-3 flex items-center justify-between">
              <div>
                <p class="text-xs font-bold text-gray-700">Suggestion Mode</p>

                <p class="mt-1 text-[10px] text-gray-400">
                  Choose how the suggested units should be calculated.
                </p>
              </div>

              <div
                class="inline-flex rounded-md border border-gray-300 bg-white p-1"
              >
                <button
                  type="button"
                  @click="suggestionMode = 'group'"
                  :class="[
                    'rounded px-3 py-1.5 text-[10px] font-bold transition',
                    suggestionMode === 'group'
                      ? 'bg-gray-900 text-white'
                      : 'text-gray-600 hover:bg-gray-100',
                  ]"
                >
                  Group
                </button>

                <button
                  type="button"
                  @click="suggestionMode = 'individual'"
                  :class="[
                    'rounded px-3 py-1.5 text-[10px] font-bold transition',
                    suggestionMode === 'individual'
                      ? 'bg-gray-900 text-white'
                      : 'text-gray-600 hover:bg-gray-100',
                  ]"
                >
                  Individual
                </button>
              </div>
            </div>
            <table class="w-full min-w-[1100px] text-left">
              <thead class="border-b border-gray-200 bg-white">
                <tr>
                  <!-- FACULTY -->
                  <th
                    class="px-5 py-3 text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Recommended Faculty
                  </th>

                  <!-- UNIT LOAD -->
                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Unit Load
                  </th>

                  <!-- CURRENT LOAD -->
                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Current Load
                  </th>

                  <!-- REQUIRED -->
                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Required
                  </th>

                  <!-- AVAILABLE -->
                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Available
                  </th>

                  <!-- GROUP SUGGESTED -->
                  <th
                    v-if="suggestionMode === 'group'"
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Group Suggested
                  </th>

                  <!-- Individual SUGGESTED -->
                  <th
                    v-if="suggestionMode === 'individual'"
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Individual Suggested
                  </th>

                  <!-- RECOMMENDATION -->
                  <th
                    class="px-5 py-3 text-right text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Recommendation
                  </th>
                  <!-- STATUS -->

                  <th
                    class="px-4 py-3 text-right text-[10px] font-bold uppercase tracking-wide text-gray-500"
                  >
                    Action
                  </th>
                </tr>
              </thead>

              <tbody class="divide-y divide-gray-100">
                <tr
                  v-for="faculty in item.facultyRecommendations"
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
                    <span class="text-xs font-semibold text-gray-700">
                      {{ faculty.currentUnits }}
                    </span>
                  </td>

                  <!-- REQUIRED -->
                  <td class="px-5 py-4 text-center">
                    <span class="text-xs font-bold text-gray-900">
                      {{ item.requiredUnits }}
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

                  <!-- GROUP SUGGESTED -->
                  <td
                    v-if="suggestionMode === 'group'"
                    class="px-5 py-4 text-center"
                  >
                    <span
                      :class="[
                        'inline-flex min-w-[32px] justify-center rounded px-3 py-1 text-xs font-bold',
                        faculty.suggestedUnits > 0
                          ? 'bg-blue-50 text-blue-700'
                          : 'bg-gray-100 text-gray-500',
                      ]"
                    >
                      {{ faculty.suggestedUnits }}
                    </span>
                  </td>

                  <!-- INDIVIDUAL SUGGESTED -->
                  <td
                    v-if="suggestionMode === 'individual'"
                    class="px-5 py-4 text-center"
                  >
                    <span
                      :class="[
                        'inline-flex min-w-[32px] justify-center rounded px-3 py-1 text-xs font-bold',
                        faculty.individualSuggestedUnits > 0
                          ? 'bg-amber-50 text-amber-700'
                          : 'bg-gray-100 text-gray-500',
                      ]"
                    >
                      {{ faculty.individualSuggestedUnits }}
                    </span>
                  </td>
                  <!-- RECOMMENDATION -->
                  <td class="px-5 py-4 text-right">
                    <span
                      v-if="faculty.recommendation === 'Fully Allocated'"
                      class="inline-flex rounded bg-green-100 px-2 py-1 text-[10px] font-bold text-green-700"
                    >
                      Fully Allocated
                    </span>

                    <span
                      v-else-if="
                        faculty.recommendation === 'Partial Allocation'
                      "
                      class="inline-flex rounded bg-amber-100 px-2 py-1 text-[10px] font-bold text-amber-700"
                    >
                      Partial Allocation
                    </span>

                    <span
                      v-else
                      class="inline-flex rounded bg-gray-100 px-2 py-1 text-[10px] font-bold text-gray-500"
                    >
                      No Capacity
                    </span>
                  </td>
                  <!-- STATUS -->

                  <td class="px-4 py-4 text-right">
                    <button
                      type="button"
                      @click="openAdjustUnitModal(faculty)"
                      class="inline-flex items-center rounded-md border border-gray-300 bg-white px-3 py-1.5 text-[10px] font-semibold text-gray-700 transition hover:border-gray-900 hover:bg-gray-50 disabled:cursor-not-allowed disabled:border-gray-200 disabled:bg-gray-100 disabled:text-gray-400 disabled:hover:border-gray-200 disabled:hover:bg-gray-100"
                    >
                      Adjust Unit
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- =====================================================
         CLASS FOOTER
    ====================================================== -->
        </div>
      </div>

      <!-- =======================================================
           NO RECOMMENDATION
      ======================================================== -->
      <div
        v-if="!recommendations.length && !newFacultyRecommendations.length"
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
          additional recommendations.
        </p>
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
    <div class="w-full max-w-md overflow-hidden rounded-lg bg-white shadow-xl">
      <!-- HEADER -->
      <div class="border-b border-gray-200 px-5 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-sm font-bold text-gray-900">Adjust Faculty Unit</h3>

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

        <!-- NEW UNIT -->
        <div>
          <label
            class="text-[10px] font-bold uppercase tracking-wide text-gray-500"
          >
            New Unit Load
          </label>

          <input
            v-model.number="adjustedUnitLoad"
            type="number"
            min="0"
            step="0.25"
            class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm outline-none transition focus:border-gray-900"
            placeholder="Enter unit load"
          />

          <p class="mt-1 text-[10px] text-gray-400">
            Enter the maximum teaching units allowed for this faculty.
          </p>
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
          type="button"
          :disabled="savingUnitLoad || adjustedUnitLoad < 0"
          @click="saveAdjustedUnit"
          class="rounded-md bg-gray-900 px-4 py-2 text-xs font-semibold text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {{ savingUnitLoad ? "Saving..." : "Save Changes" }}
        </button>
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
      activeTab: "result",
      loading: false,
      showAdjustUnitModal: false,
      selectedFaculty: null,
      adjustedUnitLoad: 0,
      savingUnitLoad: false,
      suggestionMode: "group",
      capturedUnits: {},
    };
  },

  computed: {
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

    scheduledClasses() {
      const unique = new Map();

      this.finalSchedules.forEach((schedule) => {
        const key = [
          schedule.class_id,
          schedule.course_id || "",
          schedule.course_code || "",
          schedule.faculty_id || "",
        ].join("|");

        if (!unique.has(key)) {
          unique.set(key, schedule);
        }
      });

      return Array.from(unique.values());
    },

    facultyLoadAssessment() {
      const facultyMap = new Map();

      this.rawUsers.forEach((user) => {
        /*
         * Don't depend strictly on role === "Faculty".
         * Some of your raw user records may have different
         * capitalization / role values.
         */
        const role = String(user.role || "").toLowerCase();

        if (role && role !== "faculty") {
          return;
        }

        if (!user.id) {
          return;
        }

        const id = Number(user.id);

        facultyMap.set(id, {
          id,
          name: this.getUserName(user),
          email: user.email || "",
          programCode: user.program_code || user.program?.program_code || "—",
          unitLoad: Number(user.unit_load) || 0,
          currentUnits: 0,
        });
      });

      /*
       * Calculate faculty load from final schedules.
       */
      const counted = new Set();

      this.finalSchedules.forEach((schedule) => {
        if (!schedule.faculty_id) {
          return;
        }

        const facultyId = Number(schedule.faculty_id);

        if (!facultyMap.has(facultyId)) {
          return;
        }

        const key = [facultyId, schedule.class_id, schedule.course_code].join(
          "|",
        );

        if (counted.has(key)) {
          return;
        }

        counted.add(key);

        const units = this.getScheduleUnits(schedule);

        facultyMap.get(facultyId).currentUnits = this.roundUnits(
          facultyMap.get(facultyId).currentUnits + units,
        );
      });

      return Array.from(facultyMap.values()).map((faculty) => {
        const remaining = this.roundUnits(
          faculty.unitLoad - faculty.currentUnits,
        );

        let status = "Available";
        let statusClass = "available";

        if (remaining < 0) {
          status = "Overloaded";
          statusClass = "overloaded";
        } else if (remaining === 0) {
          status = "At Maximum Load";
          statusClass = "full";
        } else if (remaining <= 3) {
          status = "Limited Capacity";
          statusClass = "limited";
        }

        return {
          ...faculty,
          remainingCapacity: remaining,
          status,
          statusClass,
        };
      });
    },

    recommendations() {
      const results = [];

      this.unscheduledMeetings.forEach((item) => {
        /*
         * =========================================================
         * REQUIRED UNITS
         * =========================================================
         */
        const requiredUnits = this.roundUnits(this.getRequiredUnits(item));

        if (!requiredUnits) {
          return;
        }

        const candidates = this.getPossibleFaculty(item);

        candidates.forEach((faculty) => {
          /*
           * =========================================================
           * FACULTY LOAD
           * =========================================================
           */
          const currentUnits = this.roundUnits(
            this.getFacultyCurrentUnits(faculty.id),
          );

          const maxUnits = Number(faculty.unitLoad) || 0;

          /*
           * Available capacity of faculty
           */
          const available = this.roundUnits(
            Math.max(0, maxUnits - currentUnits),
          );

          /*
           * =========================================================
           * SUGGESTED UNITS
           * =========================================================
           *
           * Suggested = how many units of the course
           * can actually be assigned to this faculty.
           *
           * Example:
           *
           * Required  = 7.50
           * Available = 5.00
           *
           * Suggested = 5.00
           * Remaining = 2.50
           */
          const suggestedUnits = this.roundUnits(
            Math.min(requiredUnits, available),
          );

          /*
           * =========================================================
           * REMAINING UNITS
           * =========================================================
           *
           * Remaining = course units that cannot be accommodated
           * by this faculty.
           */
          const remainingUnits = this.roundUnits(
            Math.max(0, requiredUnits - suggestedUnits),
          );

          /*
           * =========================================================
           * DEBUG LOG
           * =========================================================
           */
          console.log("========== FACULTY RECOMMENDATION ==========");
          console.log("Course:", item.course_code);
          console.log("Class:", item.class_id || item.classId || item.id);
          console.log("Faculty:", this.getUserName(faculty));
          console.log("Faculty ID:", faculty.id);

          console.log("--------------------------------------------");
          console.log("Required Units:", requiredUnits);
          console.log("Maximum Unit Load:", maxUnits);
          console.log("Current Units:", currentUnits);
          console.log("Available Capacity:", available);
          console.log("Suggested Units:", suggestedUnits);
          console.log("Remaining Units:", remainingUnits);
          console.log("--------------------------------------------");

          /*
           * =========================================================
           * RECOMMENDATION STATUS
           * =========================================================
           */
          let recommendation;
          let recommendationClass;

          if (remainingUnits === 0) {
            recommendation = "Fully Allocated";
            recommendationClass = "full";
          } else if (suggestedUnits > 0) {
            recommendation = "Partial Allocation";
            recommendationClass = "partial";
          } else {
            recommendation = "No Capacity";
            recommendationClass = "cannot-assign";
          }

          console.log("Recommendation:", recommendation);
          console.log("============================================");

          /*
           * =========================================================
           * RESULT
           * =========================================================
           */
          results.push({
            key: `${item.id}-${faculty.id}`,

            classId: item.class_id || item.classId || item.id,

            courseCode: item.course_code || "—",

            courseTitle: this.getCourseTitle(item),

            programCode: item.program_code || "—",

            /*
             * Actual course requirement
             */
            requiredUnits,

            facultyId: faculty.id,

            facultyName: this.getUserName(faculty),

            /*
             * Faculty load
             */
            currentUnits,

            unitLoad: maxUnits,

            /*
             * Faculty capacity
             */
            availableCapacity: available,

            /*
             * Amount that can actually be assigned
             */
            suggestedUnits,

            /*
             * Amount still needed
             */
            remainingUnits,

            recommendation,

            recommendationClass,
          });
        });
      });

      return results;
    },
    groupedRecommendations() {
      const groups = new Map();

      this.recommendations.forEach((recommendation) => {
        // =====================================================
        // GROUP BY COURSE + PROGRAM
        // =====================================================

        const groupKey = [recommendation.courseCode, recommendation.programCode]
          .join("|")
          .toLowerCase();

        if (!groups.has(groupKey)) {
          groups.set(groupKey, {
            key: groupKey,

            courseCode: recommendation.courseCode,
            courseTitle: recommendation.courseTitle,
            programCode: recommendation.programCode,

            // =====================================================
            // ALL UNIQUE SECTIONS
            // =====================================================
            classes: [],

            // Section-aware allocation
            sections: [],

            // =====================================================
            // TOTAL REQUIRED UNITS
            // =====================================================
            requiredUnits: 0,

            // =====================================================
            // UNITS ALREADY CAPTURED
            // =====================================================
            alreadyCapturedUnits: 0,

            // =====================================================
            // TOTAL GROUP SUGGESTED
            // =====================================================
            totalSuggestedUnits: 0,

            // =====================================================
            // TOTAL REMAINING
            // =====================================================
            remainingUnits: 0,

            // =====================================================
            // FACULTY
            // =====================================================
            facultyRecommendations: [],
          });
        }

        const group = groups.get(groupKey);

        // =====================================================
        // ADD UNIQUE SECTION
        // =====================================================

        const classId = recommendation.classId;

        const existingClass = group.classes.find(
          (item) => String(item.classId) === String(classId),
        );

        if (!existingClass) {
          const classRequiredUnits = this.roundUnits(
            Number(recommendation.requiredUnits || 0),
          );

          group.classes.push({
            classId,
            requiredUnits: classRequiredUnits,
          });

          // ===================================================
          // STORE SECTION
          // ===================================================

          group.sections.push({
            classId,
            requiredUnits: classRequiredUnits,
            allocations: [],
            remainingUnits: classRequiredUnits,
          });

          // ===================================================
          // TOTAL REQUIRED
          // ===================================================

          group.requiredUnits = this.roundUnits(
            group.requiredUnits + classRequiredUnits,
          );
        }

        // =====================================================
        // GROUP FACULTY
        // =====================================================

        let faculty = group.facultyRecommendations.find(
          (item) => String(item.facultyId) === String(recommendation.facultyId),
        );

        if (!faculty) {
          faculty = {
            key: `${groupKey}-${recommendation.facultyId}`,

            facultyId: recommendation.facultyId,
            facultyName: recommendation.facultyName,

            programCode: recommendation.programCode || "—",

            unitLoad: Number(recommendation.unitLoad) || 0,

            currentUnits: Number(recommendation.currentUnits) || 0,

            availableCapacity: Number(recommendation.availableCapacity) || 0,

            requiredUnits: 0,

            // =================================================
            // GROUP SUGGESTED
            // =================================================
            suggestedUnits: 0,

            // =================================================
            // INDIVIDUAL SUGGESTED
            // =================================================
            individualSuggestedUnits: 0,

            // =================================================
            // SECTION ALLOCATION
            // =================================================
            sectionAllocations: [],

            remainingUnits: 0,

            recommendation: "No Capacity",
            recommendationClass: "cannot-assign",
          };

          group.facultyRecommendations.push(faculty);
        }
      });

      // =====================================================
      // FINALIZE GROUPS
      // =====================================================

      groups.forEach((group) => {
        // =====================================================
        // ALREADY CAPTURED
        // =====================================================

        const alreadyCapturedUnits = this.getCapturedUnits(group);

        group.alreadyCapturedUnits = alreadyCapturedUnits;

        // =====================================================
        // TOTAL UNITS STILL NEEDED
        // =====================================================

        let remainingGroupUnits = this.roundUnits(
          Math.max(0, group.requiredUnits - alreadyCapturedUnits),
        );

        // =====================================================
        // RESET FACULTY VALUES
        // =====================================================

        group.facultyRecommendations.forEach((faculty) => {
          faculty.requiredUnits = this.roundUnits(group.requiredUnits);

          faculty.availableCapacity = this.roundUnits(
            Math.max(0, faculty.availableCapacity),
          );

          faculty.suggestedUnits = 0;

          faculty.remainingUnits = remainingGroupUnits;

          faculty.sectionAllocations = [];

          // =================================================
          // INDIVIDUAL SUGGESTION
          // =================================================

          faculty.individualSuggestedUnits = this.getIndividualSuggestion(
            faculty.requiredUnits,
            faculty.availableCapacity,
          );
        });

        // =====================================================
        // SECTION-BY-SECTION GROUP ALLOCATION
        // =====================================================
        //
        // Example:
        //
        // Section 1 = 4
        // Section 2 = 4
        //
        // Faculty A = 4 available
        // Faculty B = 2 available
        // Faculty C = 3 available
        //
        // Result:
        //
        // Section 1
        //   Faculty A = 4
        //
        // Section 2
        //   Faculty B = 2
        //   Faculty C = 2
        //
        // TOTAL = 8
        //
        // =====================================================

        const facultyRemainingCapacity = new Map();

        group.facultyRecommendations.forEach((faculty) => {
          facultyRemainingCapacity.set(
            String(faculty.facultyId),
            this.roundUnits(Math.max(0, faculty.availableCapacity)),
          );
        });

        group.sections.forEach((section) => {
          let remainingSectionUnits = this.roundUnits(section.requiredUnits);

          section.allocations = [];

          // ===================================================
          // ALLOCATE THIS SECTION
          // ===================================================

          for (const faculty of group.facultyRecommendations) {
            if (remainingSectionUnits <= 0 || remainingGroupUnits <= 0) {
              break;
            }

            const facultyId = String(faculty.facultyId);

            const facultyRemaining = this.roundUnits(
              facultyRemainingCapacity.get(facultyId) || 0,
            );

            if (facultyRemaining <= 0) {
              continue;
            }

            const suggested = this.roundUnits(
              Math.min(
                remainingSectionUnits,
                remainingGroupUnits,
                facultyRemaining,
              ),
            );

            if (suggested <= 0) {
              continue;
            }

            // ===============================================
            // CAPTURE SECTION ALLOCATION
            // ===============================================

            section.allocations.push({
              facultyId: faculty.facultyId,
              facultyName: faculty.facultyName,
              units: suggested,
            });

            faculty.sectionAllocations.push({
              classId: section.classId,
              units: suggested,
            });

            // ===============================================
            // ADD TO FACULTY TOTAL
            // ===============================================

            faculty.suggestedUnits = this.roundUnits(
              faculty.suggestedUnits + suggested,
            );

            // ===============================================
            // REDUCE FACULTY CAPACITY
            // ===============================================

            facultyRemainingCapacity.set(
              facultyId,
              this.roundUnits(facultyRemaining - suggested),
            );

            // ===============================================
            // REDUCE SECTION REQUIREMENT
            // ===============================================

            remainingSectionUnits = this.roundUnits(
              Math.max(0, remainingSectionUnits - suggested),
            );

            // ===============================================
            // REDUCE GROUP REQUIREMENT
            // ===============================================

            remainingGroupUnits = this.roundUnits(
              Math.max(0, remainingGroupUnits - suggested),
            );
          }

          // ===================================================
          // SECTION REMAINING
          // ===================================================

          section.remainingUnits = remainingSectionUnits;
        });

        // =====================================================
        // TOTAL GROUP SUGGESTED
        // =====================================================

        group.totalSuggestedUnits = this.roundUnits(
          group.facultyRecommendations.reduce(
            (total, faculty) => total + Number(faculty.suggestedUnits || 0),
            0,
          ),
        );

        // =====================================================
        // TOTAL GROUP REMAINING
        // =====================================================

        group.remainingUnits = this.roundUnits(
          Math.max(
            0,
            group.requiredUnits -
              group.alreadyCapturedUnits -
              group.totalSuggestedUnits,
          ),
        );

        // =====================================================
        // FACULTY STATUS
        // =====================================================

        group.facultyRecommendations.forEach((faculty) => {
          const suggested = this.roundUnits(faculty.suggestedUnits || 0);

          faculty.remainingUnits = group.remainingUnits;

          if (suggested <= 0) {
            faculty.recommendation = "No Capacity";

            faculty.recommendationClass = "cannot-assign";
          } else if (group.remainingUnits === 0) {
            faculty.recommendation = "Fully Allocated";

            faculty.recommendationClass = "full";
          } else {
            faculty.recommendation = "Partial Allocation";

            faculty.recommendationClass = "partial";
          }
        });

        // =====================================================
        // DISPLAY RULE
        // =====================================================
        //
        // IMPORTANT:
        // Do NOT hide faculty merely because another faculty
        // can individually handle the total requirement.
        //
        // For GROUP mode, we need all faculty required to
        // collectively accommodate multiple sections.
        //
        // =====================================================

        group.facultyRecommendations = group.facultyRecommendations.filter(
          (faculty) => faculty.facultyId != null,
        );

        // =====================================================
        // SORT
        // =====================================================

        group.facultyRecommendations.sort((a, b) => {
          // 1. Faculty with suggested units first
          const suggestedDiff =
            Number(b.suggestedUnits || 0) - Number(a.suggestedUnits || 0);

          if (suggestedDiff !== 0) {
            return suggestedDiff;
          }

          // 2. Higher available capacity
          const availableDiff =
            Number(b.availableCapacity || 0) - Number(a.availableCapacity || 0);

          if (availableDiff !== 0) {
            return availableDiff;
          }

          // 3. Faculty name
          return String(a.facultyName || "").localeCompare(
            String(b.facultyName || ""),
          );
        });
      });

      return Array.from(groups.values());
    },
    newFacultyRecommendations() {
      const results = [];

      this.unscheduledMeetings.forEach((item) => {
        const required = this.getRequiredUnits(item);

        if (!required) {
          return;
        }

        /*
         * Get ALL possible faculty from
         * the reason.
         */
        const possibleFaculty = this.getPossibleFaculty(item);

        /*
         * Calculate suggested units.
         *
         * We distribute the required units
         * across the possible faculty.
         */
        let remainingUnits = required;

        const facultyRows = possibleFaculty.map((faculty) => {
          const suggestedUnits = Math.min(
            remainingUnits,
            faculty.availableCapacity,
          );

          remainingUnits = this.roundUnits(remainingUnits - suggestedUnits);
          return {
            ...faculty,

            suggestedUnits,
          };
        });

        /*
         * How much existing capacity can
         * actually absorb the course?
         */
        const existingCapacity = this.roundUnits(
          facultyRows.reduce(
            (total, faculty) => total + Number(faculty.suggestedUnits || 0),
            0,
          ),
        );

        const additionalUnits = this.roundUnits(
          Math.max(0, required - existingCapacity),
        );
        /*
         * Only show this section when
         * there is still a unit shortage.
         */
        if (additionalUnits > 0) {
          results.push({
            key: `new-${item.id}`,

            courseCode: item.course_code || "—",

            courseTitle: this.getCourseTitle(item),

            programCode: item.program_code || "—",

            requiredUnits: required,

            existingCapacity,

            additionalUnits,

            possibleFaculty: facultyRows,
          });
        }
      });

      return results;
    },
  },

  async mounted() {
    await this.loadAssessmentData();
  },

  methods: {
    getCapturedUnits(group) {
      if (!group) {
        return 0;
      }

      let total = 0;

      group.facultyRecommendations.forEach((faculty) => {
        const key = `${group.key}-${faculty.facultyId}`;

        total += Number(this.capturedUnits[key] || 0);
      });

      return this.roundUnits(total);
    },
    getSuggestedUnits(faculty) {
      if (!faculty) {
        return 0;
      }

      if (this.suggestionMode === "individual") {
        return this.roundUnits(faculty.individualSuggestedUnits || 0);
      }

      return this.roundUnits(faculty.suggestedUnits || 0);
    },
    getIndividualSuggestion(requiredUnits, availableCapacity) {
      const required = this.roundUnits(requiredUnits);

      const available = this.roundUnits(Math.max(0, availableCapacity));

      return this.roundUnits(Math.min(required, available));
    },
    isFacultyFullyAllocatedForItem(item, faculty) {
      if (!item || !faculty) {
        return false;
      }

      const requiredUnits = this.roundUnits(this.getRequiredUnits(item));

      if (!requiredUnits) {
        return false;
      }

      const currentUnits = this.roundUnits(
        this.getFacultyCurrentUnits(faculty.id),
      );

      const maxUnits = Number(faculty.unit_load) || 0;

      const availableCapacity = this.roundUnits(
        Math.max(0, maxUnits - currentUnits),
      );

      // Same logic used by recommendations()
      const suggestedUnits = this.roundUnits(
        Math.min(requiredUnits, availableCapacity),
      );

      const remainingUnits = this.roundUnits(
        Math.max(0, requiredUnits - suggestedUnits),
      );

      return remainingUnits === 0;
    },
    openAdjustUnitModal(faculty) {
      // groupedRecommendations uses facultyId, not id
      const facultyId = faculty.facultyId || faculty.id;

      const rawUser = this.rawUsers.find(
        (user) => Number(user.id) === Number(facultyId),
      );

      if (!rawUser) {
        console.error("Faculty not found in rawUsers:", facultyId, faculty);
        return;
      }

      this.selectedFaculty = {
        id: rawUser.id,
        name: this.getUserName(rawUser),
        email: rawUser.email || "",
        programCode:
          rawUser.program_code || rawUser.program?.program_code || "—",
        unitLoad: Number(rawUser.unit_load) || 0,
      };

      this.adjustedUnitLoad = Number(rawUser.unit_load) || 0;

      this.showAdjustUnitModal = true;
    },

    closeAdjustUnitModal() {
      this.showAdjustUnitModal = false;
      this.selectedFaculty = null;
      this.adjustedUnitLoad = 0;
    },
    async saveAdjustedUnit() {
      if (!this.selectedFaculty) {
        return;
      }

      const facultyId = Number(this.selectedFaculty.id);
      const newUnitLoad = Number(this.adjustedUnitLoad);

      if (!facultyId) {
        console.error("Invalid faculty ID");
        return;
      }

      if (Number.isNaN(newUnitLoad) || newUnitLoad < 0) {
        console.error("Invalid unit load");
        return;
      }

      this.savingUnitLoad = true;

      try {
        console.log("Updating faculty unit load:", {
          facultyId,
          unit_load: newUnitLoad,
        });

        await axios.patch(`http://localhost:8000/users/${facultyId}`, {
          unit_load: newUnitLoad,
        });

        // Refresh raw users
        if (typeof this.fetchDataStore.fetchRawUsers === "function") {
          await this.fetchDataStore.fetchRawUsers();
        }

        this.closeAdjustUnitModal();

        console.log("Faculty unit load updated successfully.");
      } catch (error) {
        console.error(
          "Failed to update faculty unit load:",
          error.response?.data || error,
        );
      } finally {
        this.savingUnitLoad = false;
      }
    },
    roundUnits(value) {
      return Number(Number(value || 0).toFixed(2));
    },
    /* =========================================================
       LOAD DATA
    ========================================================== */

    async loadAssessmentData() {
      this.loading = true;

      try {
        /*
         * IMPORTANT:
         * Replace these method names with the exact methods
         * already existing in your Pinia store.
         */

        if (typeof this.fetchDataStore.fetchFinalSchedules === "function") {
          await this.fetchDataStore.fetchFinalSchedules();
        }

        if (
          typeof this.fetchDataStore.fetchUnscheduledMeetings === "function"
        ) {
          await this.fetchDataStore.fetchUnscheduledMeetings();
        }

        if (typeof this.fetchDataStore.fetchCourses === "function") {
          await this.fetchDataStore.fetchCourses();
        }

        if (typeof this.fetchDataStore.fetchRawUsers === "function") {
          await this.fetchDataStore.fetchRawUsers();
        }

        console.log("POST ASSESSMENT DATA");

        console.log("Final schedules:", this.finalSchedules);

        console.log("Unscheduled:", this.unscheduledMeetings);

        console.log("Courses:", this.courses);

        console.log("Users:", this.rawUsers);
      } catch (error) {
        console.error("Failed to load post assessment data:", error);
      } finally {
        this.loading = false;
      }
    },

    /* =========================================================
       COURSE
    ========================================================== */

    getCourse(item) {
      if (!item) {
        return null;
      }

      // =========================================================
      // 1. ALWAYS TRY COURSE ID FIRST
      // =========================================================
      if (item.course_id) {
        const courseById = this.courses.find(
          (course) => Number(course.course_id) === Number(item.course_id),
        );

        if (courseById) {
          console.log("COURSE FOUND BY ID:", {
            itemCourseId: item.course_id,
            course_id: courseById.course_id,
            course_code: courseById.course_code,
            course_lec: courseById.course_lec,
            course_lab: courseById.course_lab,
          });

          return courseById;
        }
      }

      // =========================================================
      // 2. FALLBACK TO COURSE CODE
      // =========================================================
      const itemCourseCode = String(item.course_code || "")
        .trim()
        .toLowerCase();

      if (itemCourseCode) {
        const courseByCode = this.courses.find(
          (course) =>
            String(course.course_code || "")
              .trim()
              .toLowerCase() === itemCourseCode,
        );

        if (courseByCode) {
          console.log("COURSE FOUND BY CODE:", {
            itemCourseCode,
            course_id: courseByCode.course_id,
            course_code: courseByCode.course_code,
            course_lec: courseByCode.course_lec,
            course_lab: courseByCode.course_lab,
          });

          return courseByCode;
        }
      }

      console.warn("COURSE NOT FOUND:", {
        course_id: item.course_id,
        course_code: item.course_code,
      });

      return null;
    },

    getCourseTitle(item) {
      const course = this.getCourse(item);

      return course?.course_title || "Course title unavailable";
    },

    /* =========================================================
       UNITS
    ========================================================== */

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

      const totalUnits = lectureTeachingUnits + laboratoryTeachingUnits;

      return Number(totalUnits.toFixed(2));
    },
    getScheduleUnits(schedule) {
      return this.getRequiredUnits(schedule);
    },

    /* =========================================================
       FACULTY NAME
    ========================================================== */

    getUserName(user) {
      if (!user) {
        return "Unknown Faculty";
      }

      const name = [user.first_name, user.middle_name, user.last_name]
        .filter(Boolean)
        .join(" ");

      return name || user.name || user.faculty_name || "Unknown Faculty";
    },

    /* =========================================================
       FIND FACULTY
    ========================================================== */

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

        const normalizedFullName = this.normalizeName(fullName);

        const normalizedFirstLast = this.normalizeName(firstLastName);

        return normalizedFullName === target || normalizedFirstLast === target;
      });
    },

    normalizeName(name) {
      return String(name || "")
        .toLowerCase()
        .replace(/\s+/g, " ")
        .trim();
    },

    /* =========================================================
       EXTRACT POSSIBLE FACULTY
    ========================================================== */

    getPossibleFaculty(item) {
      const candidates = [];
      const usedNames = new Set();

      // =========================================================
      // GET FACULTY ALREADY ASSIGNED TO THE SAME COURSE + PROGRAM
      // =========================================================
      //
      // Example:
      // ENTREP 4114 / BSENTREP
      //
      // Class 389 -> Sarah May Dimaocor
      // Class 390 -> Sarah May Dimaocor
      // Class 391 -> Bryan Macarayo
      // Class 392 -> Unassigned
      //
      // Therefore, when processing Class 392:
      // Sarah May Dimaocor and Bryan Macarayo must be excluded.
      // =========================================================

      const alreadyAssignedFaculty = new Set();

      this.unscheduledMeetings.forEach((other) => {
        // Same course
        const sameCourse =
          String(other.course_code || "")
            .trim()
            .toLowerCase() ===
          String(item.course_code || "")
            .trim()
            .toLowerCase();

        if (!sameCourse) {
          return;
        }

        // Same program
        const sameProgram =
          String(other.program_code || "")
            .trim()
            .toLowerCase() ===
          String(item.program_code || "")
            .trim()
            .toLowerCase();

        if (!sameProgram) {
          return;
        }

        // Ignore Unassigned
        if (
          !other.faculty_name ||
          String(other.faculty_name).trim().toLowerCase() === "unassigned"
        ) {
          return;
        }

        const assignedName = this.normalizeName(other.faculty_name);

        if (assignedName) {
          alreadyAssignedFaculty.add(assignedName);
        }
      });

      // =========================================================
      // CURRENT ITEM FACULTY
      // =========================================================
      if (item.faculty_name && item.faculty_name !== "Unassigned") {
        const facultyName = String(item.faculty_name).trim();
        const facultyKey = this.normalizeName(facultyName);

        usedNames.add(facultyKey);

        const faculty = this.findFacultyByName(facultyName);

        if (faculty) {
          const key = this.normalizeName(this.getUserName(faculty));

          const shouldHide = this.shouldHideUnresolvedFaculty(item, key);

          // Do not show faculty who can already fully accommodate
          // this class requirement.
          const isFullyAllocated = this.isFacultyFullyAllocatedForItem(
            item,
            faculty,
          );

          if (!shouldHide && !isFullyAllocated) {
            candidates.push(this.buildFacultyCandidate(faculty));
          }
        }
      }

      // =========================================================
      // FACULTY NAMES FROM REASON
      // =========================================================
      const names = this.extractFacultyNames(item.reason);

      names.forEach((name) => {
        const cleanName = String(name || "").trim();

        if (!cleanName) {
          return;
        }

        const key = this.normalizeName(cleanName);

        // -------------------------------------------------------
        // DO NOT DISPLAY IF ALREADY USED IN CURRENT ITEM
        // -------------------------------------------------------
        if (usedNames.has(key)) {
          return;
        }

        // -------------------------------------------------------
        // IMPORTANT:
        // DO NOT DISPLAY FACULTY ALREADY ASSIGNED TO ANOTHER
        // CLASS OF THE SAME COURSE + PROGRAM
        // -------------------------------------------------------
        if (alreadyAssignedFaculty.has(key)) {
          return;
        }

        // -------------------------------------------------------
        // EXISTING UNRESOLVED PROTECTION
        // -------------------------------------------------------
        if (this.shouldHideUnresolvedFaculty(item, key)) {
          return;
        }

        const faculty = this.findFacultyByName(cleanName);

        if (faculty) {
          const facultyKey = this.normalizeName(this.getUserName(faculty));

          // Extra duplicate protection
          if (usedNames.has(facultyKey)) {
            return;
          }

          // Also protect against assigned faculty
          if (alreadyAssignedFaculty.has(facultyKey)) {
            return;
          }

          usedNames.add(facultyKey);

          candidates.push(this.buildFacultyCandidate(faculty));
        } else {
          // Unknown faculty
          usedNames.add(key);

          candidates.push({
            id: null,
            name: cleanName,
            programCode: item.program_code || "—",
            currentUnits: null,
            unitLoad: null,
            availableCapacity: null,
            suggestedUnits: 0,
            facultyFound: false,
          });
        }
      });

      return candidates;
    },
    shouldHideUnresolvedFaculty(item, facultyName) {
      if (!item || !facultyName) {
        return false;
      }

      const reason = String(item.reason || "").toLowerCase();

      /*
       * This rule only applies to:
       * "Unresolved after repair pass (relaxed soft constraints)"
       */
      if (!reason.includes("unresolved after repair pass")) {
        return false;
      }

      const targetName = this.normalizeName(facultyName);

      /*
       * Look for another unscheduled record for the same
       * course + program that has:
       *
       * "No faculty assignment"
       *
       * and contains this faculty in:
       *
       * possible faculty: ...
       */
      return this.unscheduledMeetings.some((other) => {
        // Do not compare the record with itself
        if (String(other.id) === String(item.id)) {
          return false;
        }

        // Same course
        const sameCourse =
          String(other.course_code || "")
            .trim()
            .toLowerCase() ===
          String(item.course_code || "")
            .trim()
            .toLowerCase();

        if (!sameCourse) {
          return false;
        }

        // Same program
        const sameProgram =
          String(other.program_code || "")
            .trim()
            .toLowerCase() ===
          String(item.program_code || "")
            .trim()
            .toLowerCase();

        if (!sameProgram) {
          return false;
        }

        // Must be a "No faculty assignment" record
        const otherReason = String(other.reason || "").toLowerCase();

        if (!otherReason.includes("no faculty assignment")) {
          return false;
        }

        // Extract possible faculty from the other reason
        const possibleFaculty = this.extractFacultyNames(other.reason);

        return possibleFaculty.some(
          (name) => this.normalizeName(name) === targetName,
        );
      });
    },
    buildFacultyCandidate(faculty) {
      const currentUnits = this.getFacultyCurrentUnits(faculty.id);

      const unitLoad = Number(faculty.unit_load) || 0;

      const availableCapacity = Math.max(0, unitLoad - currentUnits);

      return {
        id: faculty.id,

        name: this.getUserName(faculty),

        programCode:
          faculty.program_code || faculty.program?.program_code || "—",

        currentUnits,

        unitLoad,

        availableCapacity,

        suggestedUnits: 0,

        facultyFound: true,
      };
    },
    extractFacultyNames(reason) {
      if (!reason) {
        return [];
      }

      const text = String(reason);

      // Find "possible faculty:"
      const match = text.match(/possible\s+faculty\s*:\s*(.*)$/i);

      if (!match) {
        return [];
      }

      let facultyText = match[1].trim();

      // Remove unwanted trailing text
      facultyText = facultyText
        .replace(/\s+and\s+hy\s*$/i, "")
        .replace(/\s+and\s+h(y)?\s*$/i, "")
        .trim();

      if (!facultyText) {
        return [];
      }

      /*
       * Example:
       *
       * Aunel Guillergan,
       * Gerry Louis Gallano,
       * AddedTM314 Faculty1,
       * AddedTM314 Faculty2 and hy
       */

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
        /*
         * Handle:
         *
         * Faculty A and Faculty B
         */
        const andParts = part.split(/\s+and\s+/i);

        andParts.forEach((name) => {
          const clean = name.trim();

          if (clean) {
            names.push(clean);
          }
        });
      });

      // Remove duplicates
      return [...new Set(names.map((name) => name.trim()))];
    },
    getFacultyCurrentUnits(facultyId) {
      const faculty = this.facultyLoadAssessment.find(
        (item) => Number(item.id) === Number(facultyId),
      );

      return faculty ? faculty.currentUnits : 0;
    },

    /* =========================================================
       ASSESSMENT
    ========================================================== */

    getAssessmentStatus(item) {
      const reason = String(item.reason || "").toLowerCase();

      if (reason.includes("no faculty assignment")) {
        return "danger";
      }

      if (reason.includes("maximum load")) {
        return "warning";
      }

      if (reason.includes("unresolved")) {
        return "warning";
      }

      return "neutral";
    },

    getAssessmentLabel(item) {
      const reason = String(item.reason || "").toLowerCase();

      if (reason.includes("no faculty assignment")) {
        return "Faculty Required";
      }

      if (reason.includes("maximum load")) {
        return "Faculty Load Limit";
      }

      if (reason.includes("unresolved")) {
        return "Unresolved";
      }

      return "Needs Review";
    },
  },
};
</script>
