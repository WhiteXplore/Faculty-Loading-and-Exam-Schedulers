<template>
  <div class="min-h-screen bg-gray-50 p-2 text-gray-800">
    <!-- =========================================================
         TABS
    ========================================================== -->
    <div class="mb-6 border-b border-gray-200">
      <div class="flex items-center gap-1">
        <button
          type="button"
          @click="activeTab = 'result'"
          :class="[
            'border-b-2 px-4 py-3 text-sm font-semibold transition',
            activeTab === 'result'
              ? 'border-gray-900 text-gray-900'
              : 'border-transparent text-gray-500 hover:text-gray-800',
          ]"
        >
          Assessment Result
        </button>

        <button
          type="button"
          @click="activeTab = 'suggestion'"
          :class="[
            'flex items-center gap-2 border-b-2 px-4 py-3 text-sm font-semibold transition',
            activeTab === 'suggestion'
              ? 'border-gray-900 text-gray-900'
              : 'border-transparent text-gray-500 hover:text-gray-800',
          ]"
        >
          Recommendations

          <span
            v-if="recommendations.length"
            class="rounded-full bg-red-100 px-2 py-0.5 text-[10px] font-bold text-red-700"
          >
            {{ recommendations.length }}
          </span>
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

                  <!-- SUGGESTED -->
                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Suggested
                  </th>

                  <!-- RECOMMENDATION -->
                  <th
                    class="px-5 py-3 text-right text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Recommendation
                  </th>
                  <!-- STATUS -->
                  <th
                    class="px-5 py-3 text-center text-[10px] font-bold uppercase tracking-wide text-white"
                  >
                    Status
                  </th>
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

                  <!-- SUGGESTED -->
                  <td class="px-5 py-4 text-center">
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

                  <!-- RECOMMENDATION -->
                  <td class="px-5 py-4 text-right">
                    <span
                      v-if="
                        faculty.suggestedUnits > 0 &&
                        faculty.remainingUnits === 0
                      "
                      class="inline-flex rounded bg-green-100 px-2 py-1 text-[10px] font-bold text-green-700"
                    >
                      Fully Allocated
                    </span>

                    <span
                      v-else-if="faculty.suggestedUnits > 0"
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
                  <td class="px-5 py-4 text-center">
                    <span
                      :class="[
                        'inline-flex rounded px-2 py-1 text-[10px] font-bold',
                        faculty.status === 'Requirement Met'
                          ? 'bg-green-100 text-green-700'
                          : 'bg-amber-100 text-amber-700',
                      ]"
                    >
                      {{ faculty.status }}
                    </span>
                  </td>
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
        const requiredUnits = this.getRequiredUnits(item);

        if (!requiredUnits) {
          return;
        }

        const candidates = this.getPossibleFaculty(item);

        candidates.forEach((faculty) => {
          const currentUnits = this.getFacultyCurrentUnits(faculty.id);

          const maxUnits = Number(faculty.unitLoad) || 0;

          const available = this.roundUnits(
            Math.max(0, maxUnits - currentUnits),
          );

          const suggested = this.roundUnits(
            Math.max(0, requiredUnits - available),
          );

          const remainingUnits = this.roundUnits(
            Math.max(0, requiredUnits - available),
          );

          let recommendation;
          let recommendationClass;

          if (suggested === 0) {
            recommendation = "No adjustment needed";
            recommendationClass = "cannot-assign";
          } else if (suggested <= available) {
            recommendation = "Partial allocation";
            recommendationClass = "partial";
          } else {
            recommendation = "Additional capacity needed";
            recommendationClass = "cannot-assign";
          }

          results.push({
            key: `${item.id}-${faculty.id}`,

            classId: item.class_id || item.classId || item.id,

            courseCode: item.course_code || "—",

            courseTitle: this.getCourseTitle(item),

            programCode: item.program_code || "—",

            requiredUnits,

            facultyId: faculty.id,

            facultyName: this.getUserName(faculty),

            currentUnits,

            unitLoad: maxUnits,

            availableCapacity: available,

            // REQUIRED - AVAILABLE
            suggestedUnits: suggested,

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
        // NOT BY CLASS ID
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

            // Every unique class under this course
            classes: [],

            // Total required units across ALL classes
            requiredUnits: 0,

            // Actual units that can currently be absorbed
            // by all possible faculty
            totalSuggestedUnits: 0,

            // Remaining units that cannot currently be absorbed
            remainingUnits: 0,

            // Faculty recommendations
            facultyRecommendations: [],
          });
        }

        const group = groups.get(groupKey);

        // =====================================================
        // ADD UNIQUE CLASS
        // =====================================================

        const classId = recommendation.classId;

        const existingClass = group.classes.find(
          (item) => String(item.classId) === String(classId),
        );

        if (!existingClass) {
          const classRequiredUnits = Number(recommendation.requiredUnits || 0);

          group.classes.push({
            classId,
            requiredUnits: classRequiredUnits,
          });

          // IMPORTANT:
          // Add the required units of every UNIQUE class.
          //
          // Example:
          // Class 405 = 4.25
          // Class 404 = 4.25
          // Total     = 8.50

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

            // This will be calculated AFTER the entire
            // course/group requirement is known.
            requiredUnits: 0,

            suggestedUnits: 0,

            remainingUnits: 0,
          };

          group.facultyRecommendations.push(faculty);
        }
      });

      // =====================================================
      // FINALIZE GROUPS
      // =====================================================

      groups.forEach((group) => {
        // Calculate each faculty recommendation
        group.facultyRecommendations.forEach((faculty) => {
          faculty.requiredUnits = this.roundUnits(group.requiredUnits);

          const available = this.roundUnits(
            Math.max(0, faculty.availableCapacity),
          );

          faculty.availableCapacity = available;

          const requirementMet = available >= faculty.requiredUnits;

          faculty.suggestedUnits = requirementMet
            ? 0
            : this.roundUnits(faculty.requiredUnits - available);

          faculty.remainingUnits = faculty.suggestedUnits;

          faculty.status = requirementMet
            ? "Requirement Met"
            : "Needs Capacity";

          faculty.statusClass = requirementMet ? "met" : "needs-capacity";
        });

        // =====================================================
        // SORT FACULTY RECOMMENDATIONS
        // 1. SMALLER MAX UNIT LOAD FIRST
        // 2. SMALLER AVAILABLE CAPACITY FIRST
        // 3. SMALLER SUGGESTED UNITS FIRST
        // =====================================================

        group.facultyRecommendations.sort((a, b) => {
          // Smallest unit load / max units first
          const unitLoadDiff =
            Number(a.unitLoad || 0) - Number(b.unitLoad || 0);

          if (unitLoadDiff !== 0) {
            return unitLoadDiff;
          }

          // If max units are equal,
          // smallest available capacity first
          const availableDiff =
            Number(a.availableCapacity || 0) - Number(b.availableCapacity || 0);

          if (availableDiff !== 0) {
            return availableDiff;
          }

          // If still equal,
          // smallest suggested units first
          const suggestedDiff =
            Number(a.suggestedUnits || 0) - Number(b.suggestedUnits || 0);

          if (suggestedDiff !== 0) {
            return suggestedDiff;
          }

          // Finally sort alphabetically
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

      return this.courses.find((course) => {
        /*
         * First priority: course_id
         */
        if (
          item.course_id &&
          course.course_id &&
          Number(course.course_id) === Number(item.course_id)
        ) {
          return true;
        }

        /*
         * Second priority: course_code
         *
         * Your final schedule sample has:
         *
         * course_id = empty
         * course_code = SS 111
         */
        if (item.course_code && course.course_code) {
          return (
            String(course.course_code).trim().toLowerCase() ===
            String(item.course_code).trim().toLowerCase()
          );
        }

        return false;
      });
    },

    getCourseTitle(item) {
      const course = this.getCourse(item);

      return course?.course_title || "Course title unavailable";
    },

    /* =========================================================
       UNITS
    ========================================================== */

    getRequiredUnits(item) {
      const course = this.getCourse(item);

      if (course) {
        const lectureUnits = Number(course.course_lec || 0);
        const laboratoryUnits = Number(course.course_lab || 0);

        // 1 lecture unit = 1 hour
        // 1 laboratory unit = 2.25 hours
        const totalUnits = lectureUnits + laboratoryUnits * 2.25;

        return Number(totalUnits.toFixed(2));
      }

      const hours = String(item.hours || "");

      const lec = hours.match(/([\d.]+)\s*h?\s*lec/i);
      const lab = hours.match(/([\d.]+)\s*h?\s*lab/i);

      const lectureUnits = Number(lec?.[1] || 0);
      const laboratoryHours = Number(lab?.[1] || 0);

      // If the fallback value is already laboratory hours,
      // use the hours directly.
      const totalUnits = lectureUnits + laboratoryHours;

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

      // ---------------------------------------------------------
      // FACULTY NAME FROM UNSCHEDULED RECORD
      // ---------------------------------------------------------
      if (item.faculty_name && item.faculty_name !== "Unassigned") {
        const faculty = this.findFacultyByName(item.faculty_name);

        if (faculty) {
          const key = this.normalizeName(this.getUserName(faculty));

          /*
           * IMPORTANT:
           * If this is an "Unresolved" record and the same faculty
           * appears in the possible-faculty list of another
           * "No faculty assignment" record for the same course/program,
           * DO NOT display that faculty here.
           */
          const shouldHide = this.shouldHideUnresolvedFaculty(item, key);

          if (!shouldHide && !usedNames.has(key)) {
            usedNames.add(key);
            candidates.push(this.buildFacultyCandidate(faculty));
          }
        }
      }

      // ---------------------------------------------------------
      // FACULTY NAMES FROM REASON
      // ---------------------------------------------------------
      const names = this.extractFacultyNames(item.reason);

      names.forEach((name) => {
        const cleanName = String(name || "").trim();

        if (!cleanName) {
          return;
        }

        const key = this.normalizeName(cleanName);

        if (usedNames.has(key)) {
          return;
        }

        /*
         * Apply the same protection to faculty names extracted
         * from the reason.
         */
        if (this.shouldHideUnresolvedFaculty(item, key)) {
          return;
        }

        const faculty = this.findFacultyByName(cleanName);

        if (faculty) {
          usedNames.add(key);

          candidates.push(this.buildFacultyCandidate(faculty));
        } else {
          /*
           * Keep unknown faculty visible unless the faculty is
           * explicitly blocked by the unresolved/no-assignment rule.
           */
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
