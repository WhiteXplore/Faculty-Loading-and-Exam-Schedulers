<template>
  <div class="text-sm">
    <!-- Action bar -->
    <div class="flex items-center justify-between flex-wrap gap-2">
      <p class="text-gray-500">
        Checks whether the current data (classes, faculty, rooms) can produce a
        <span class="font-medium text-gray-700">complete schedule</span> —
        without running the generator.
      </p>
      <button @click="runAssessment" :disabled="loading" class="btn-save">
        <span
          v-if="loading"
          class="h-3 w-3 rounded-full border-2 border-white border-t-transparent animate-spin"
        ></span>
        {{
          loading
            ? "Assessing…"
            : report
            ? "Re-run assessment"
            : "Run assessment"
        }}
      </button>
    </div>

    <!-- Error -->
    <div
      v-if="error"
      class="mt-4 rounded-md bg-red-50 border border-red-200 text-red-700 px-4 py-3"
    >
      {{ error }}
    </div>

    <!-- Empty -->
    <div
      v-if="!report && !loading && !error"
      class="mt-8 text-center text-gray-400"
    >
      <p>
        No assessment yet. Click
        <span class="font-medium">Run assessment</span> to evaluate readiness.
      </p>
    </div>

    <!-- Report -->
    <div v-if="report" class="mt-4">
      <!-- Verdict banner -->
      <div
        class="rounded-xl border p-4 flex flex-wrap items-center gap-6"
        :class="verdictBox.box"
      >
        <div>
          <div
            class="text-[11px] uppercase tracking-wider font-semibold"
            :class="verdictBox.text"
          >
            Readiness verdict
          </div>
          <div class="text-xl font-bold mt-0.5" :class="verdictBox.text">
            {{ verdictLabel }}
          </div>
          <div
            v-if="report.filter && (report.filter.institute_name || report.filter.program_code)"
            class="text-[10px] text-gray-500 mt-0.5"
          >
            Scoped to
            <span class="font-medium">{{ report.filter.institute_name }}</span>
            <span v-if="report.filter.program_code">
              · {{ report.filter.program_code }}</span
            >
          </div>
        </div>
        <div class="h-9 w-px bg-current opacity-20"></div>
        <div>
          <div class="text-2xl font-bold tabular-nums" :class="verdictBox.text">
            {{ report.schedulable_estimate_pct }}%
          </div>
          <div class="text-[11px] text-gray-500">estimated schedulable</div>
        </div>
        <div class="text-[11px] text-gray-600 ml-auto text-right space-y-0.5">
          <div>
            <b>{{ report.totals.sections }}</b> sections ·
            <b>{{ report.at_risk_sections }}</b> at-risk
          </div>
          <div>
            <b>{{ report.totals.active_faculty }}</b> faculty ·
            <b>{{ report.totals.faculty_total_capacity_units }}</b> units ·
            <b>{{ report.totals.rooms }}</b> rooms
          </div>
        </div>
      </div>

      <div class="flex justify-between items-center">
        <!-- Tabs -->
        <div class="mt-4 flex items-center justify-between">
          <div class="flex gap-1">
            <button
              v-for="t in tabs"
              :key="t.key"
              @click="activeTab = t.key"
              :class="[
                'px-4 py-2 rounded-t-lg text-sm border transition-all flex items-center gap-2',
                activeTab === t.key
                  ? 'bg-defaultGreen text-white border-gray-300 border-b-white shadow-sm'
                  : 'bg-gray-100 text-gray-600 border-transparent hover:bg-gray-200',
              ]"
            >
              <span>{{ t.label }}</span>

              <span
                class="text-[10px] font-semibold rounded-full px-1.5 py-0.5"
                :class="
                  activeTab === t.key
                    ? 'bg-white/20 text-white'
                    : 'bg-gray-200 text-gray-600'
                "
              >
                {{ t.count }}
              </span>
            </button>
          </div>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <!-- Institute -->
          <div class="relative">
            <!-- Select Box -->
            <div
              class="relative flex items-center rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 focus-within:border-defaultGreen focus-within:ring-4 focus-within:ring-green-100"
            >
              <!-- Icon -->
              <div class="absolute left-3 text-defaultGreen">
                <icon name="academic-cap" />
              </div>

              <!-- Selected -->
              <button
                type="button"
                @click="showInstituteDropdown = !showInstituteDropdown"
                class="w-full rounded-xl py-3 pl-10 pr-10 text-left text-sm font-semibold text-gray-700"
              >
                <span v-if="selectedInstituteId">
                  {{
                    uniqueInstitutes.find(
                      (i) => Number(i.id) === Number(selectedInstituteId),
                    )?.name
                  }}
                </span>

                <span v-else class="font-light text-gray-600">
                  All Institutes
                </span>
              </button>

              <!-- Arrow -->
              <button
                type="button"
                @click="showInstituteDropdown = !showInstituteDropdown"
                class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400 transition hover:bg-gray-100 hover:text-defaultGreen"
              >
                <svg
                  class="h-4 w-4 transition-transform duration-200"
                  :class="{ 'rotate-180': showInstituteDropdown }"
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
              v-if="showInstituteDropdown"
              class="absolute z-50 mt-2 w-[12vw] overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
            >
              <div class="border-b border-gray-100 px-4 py-3">
                <p
                  class="text-xs font-semibold uppercase tracking-wide text-gray-400"
                >
                  Institutes
                </p>
              </div>

              <div class="max-h-[260px] overflow-y-auto p-1.5">
                <!-- All Institutes -->
                <button
                  @click="
                    selectedInstituteId = '';
                    selectedProgramId = '';
                    showInstituteDropdown = false;
                  "
                  class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                  :class="selectedInstituteId === '' ? 'bg-green-50' : ''"
                >
                  <p class="text-sm text-gray-800">All Institutes</p>

                  <svg
                    v-if="selectedInstituteId === ''"
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

                <!-- Institutes -->
                <button
                  v-for="institute in uniqueInstitutes"
                  :key="institute.id"
                  @click="
                    selectedInstituteId = institute.id;
                    selectedProgramId = '';
                    showInstituteDropdown = false;
                  "
                  class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                  :class="
                    Number(selectedInstituteId) === Number(institute.id)
                      ? 'bg-green-50'
                      : ''
                  "
                >
                  <p class="text-sm text-gray-800">
                    {{ institute.name }}
                  </p>

                  <svg
                    v-if="Number(selectedInstituteId) === Number(institute.id)"
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

          <!-- Program -->
          <div class="relative">
            <!-- Select Box -->
            <div
              class="relative flex items-center rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 focus-within:border-defaultGreen focus-within:ring-4 focus-within:ring-green-100"
              :class="
                !selectedInstituteId ? 'opacity-60 cursor-not-allowed' : ''
              "
            >
              <!-- Icon -->
              <div class="absolute left-3 text-defaultGreen">
                <icon name="academic-cap" />
              </div>

              <!-- Selected -->
              <button
                type="button"
                :disabled="!selectedInstituteId"
                @click="showProgramDropdown = !showProgramDropdown"
                class="w-full rounded-xl py-3 pl-10 pr-10 text-left text-sm font-semibold text-gray-700 disabled:cursor-not-allowed"
              >
                <span v-if="selectedProgramId">
                  {{
                    filteredPrograms.find(
                      (p) => Number(p.id) === Number(selectedProgramId),
                    )?.name
                  }}
                </span>

                <span v-else class="font-light text-gray-600">
                  All Programs
                </span>
              </button>

              <!-- Arrow -->
              <button
                type="button"
                :disabled="!selectedInstituteId"
                @click="showProgramDropdown = !showProgramDropdown"
                class="absolute right-2 flex h-7 w-7 items-center justify-center rounded-lg text-gray-400 transition hover:bg-gray-100 hover:text-defaultGreen disabled:pointer-events-none"
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
              v-if="showProgramDropdown && selectedInstituteId"
              class="absolute z-50 mt-2 w-[12vw] overflow-hidden rounded-xl border border-gray-100 bg-white shadow-xl"
            >
              <div class="border-b border-gray-100 px-4 py-3">
                <p
                  class="text-xs font-semibold uppercase tracking-wide text-gray-400"
                >
                  Programs
                </p>
              </div>

              <div class="max-h-[260px] overflow-y-auto p-1.5">
                <!-- All Programs -->
                <button
                  @click="
                    selectedProgramId = '';
                    showProgramDropdown = false;
                  "
                  class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                  :class="selectedProgramId === '' ? 'bg-green-50' : ''"
                >
                  <p class="text-sm text-gray-800">All Programs</p>

                  <svg
                    v-if="selectedProgramId === ''"
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

                <!-- Programs -->
                <button
                  v-for="program in filteredPrograms"
                  :key="program.id"
                  @click="
                    selectedProgramId = program.id;
                    showProgramDropdown = false;
                  "
                  class="flex w-full items-center justify-between rounded-lg px-3 py-2.5 transition hover:bg-green-50"
                  :class="
                    Number(selectedProgramId) === Number(program.id)
                      ? 'bg-green-50'
                      : ''
                  "
                >
                  <p class="text-sm text-gray-800">
                    {{ program.name }}
                  </p>

                  <svg
                    v-if="Number(selectedProgramId) === Number(program.id)"
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
        </div>
      </div>

      <!-- TAB: Feasibility gates -->
      <div v-show="activeTab === 'gates'" class="mt-3 overflow-y-auto h-[70vh]">
        <table class="w-full text-left border-collapse text-[11px]">
          <thead class="bg-gray-100">
            <tr class="text-gray-700 border border-gray-200">
              <th class="px-3 py-2 border border-gray-200">Gate</th>
              <th class="px-3 py-2 border border-gray-200 text-center w-24">
                Status
              </th>
              <th class="px-3 py-2 border border-gray-200 text-center w-32">
                Lacking
              </th>
              <th class="px-3 py-2 border border-gray-200 text-center w-20">
                Supply
              </th>
              <th class="px-3 py-2 border border-gray-200 text-center w-20">
                Demand
              </th>
              <th class="px-3 py-2 border border-gray-200">
                Detail &amp; recommendation
              </th>
              <th class="px-3 py-2 border border-gray-200 text-center w-24">
                Items to fix
              </th>
            </tr>
          </thead>
          <tbody>
            <template v-for="g in report.gates" :key="g.id">
              <tr
                class="odd:bg-white even:bg-gray-50 border border-gray-200 align-top"
              >
                <td
                  class="px-3 py-2 border border-gray-200 font-semibold text-gray-800 whitespace-nowrap"
                >
                  {{ g.label }}
                </td>
                <td class="px-3 py-2 border border-gray-200 text-center">
                  <span
                    class="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full"
                    :class="statusPill(g.status)"
                  >
                    {{ statusText(g.status) }}
                  </span>
                </td>
                <td class="px-3 py-2 border border-gray-200">
                  <div class="flex items-center gap-2">
                    <div
                      class="flex-1 h-1.5 rounded-full bg-gray-200 overflow-hidden"
                    >
                      <div
                        class="h-full rounded-full"
                        :class="barColor(g.status)"
                        :style="{
                          width: Math.min(g.utilization_pct, 100) + '%',
                        }"
                      ></div>
                    </div>
                    <span
                      class="font-mono tabular-nums"
                      :class="
                        g.utilization_pct < 100
                          ? 'text-red-600 font-bold'
                          : 'text-gray-500'
                      "
                      >{{ g.utilization_pct }}%</span
                    >
                  </div>
                </td>
                <td
                  class="px-3 py-2 border border-gray-200 text-center font-mono tabular-nums"
                >
                  {{ g.supply }}
                </td>
                <td
                  class="px-3 py-2 border border-gray-200 text-center font-mono tabular-nums"
                >
                  {{ g.demand }}
                </td>
                <td class="px-3 py-2 border border-gray-200 text-gray-600">
                  <div v-if="g.required_online_pct !== undefined" class="mb-1">
                    <span
                      class="inline-block text-[10px] font-bold px-2 py-0.5 rounded"
                      :class="
                        g.required_online_pct > g.target_online_pct
                          ? 'bg-red-100 text-red-700'
                          : 'bg-green-100 text-green-700'
                      "
                    >
                      Room-forced online: {{ g.required_online_pct }}%
                      &nbsp;·&nbsp; max f2f {{ g.max_f2f_pct }}% &nbsp;·&nbsp;
                      policy target {{ g.target_online_pct }}%
                    </span>
                  </div>
                  {{ g.detail }}
                  <div
                    v-if="g.by_program && g.by_program.length"
                    class="mt-1.5 flex flex-wrap gap-1"
                  >
                    <span
                      v-for="bp in g.by_program"
                      :key="bp.program"
                      class="inline-block text-[10px] font-semibold px-2 py-0.5 rounded-full bg-red-50 text-red-700 border border-red-100"
                    >
                      {{ bp.program }} – {{ bp.count }}
                    </span>
                  </div>
                  <div
                    v-if="g.prescription"
                    class="mt-1 font-medium text-indigo-700"
                  >
                    → {{ g.prescription }}
                  </div>
                </td>
                <td class="px-3 py-2 border border-gray-200 text-center">
                  <button
                    v-if="g.offenders && g.offenders.length"
                    @click="toggleGate(g.id)"
                    class="text-indigo-600 hover:underline font-medium"
                  >
                    {{ gateOpen[g.id] ? "Hide" : "View"
                    }}<span v-if="g.offenders_total">
                      ({{ g.offenders_total }})</span
                    >
                  </button>
                  <span v-else class="text-gray-300">—</span>
                </td>
              </tr>
              <!-- expanded offenders -->
              <tr
                v-if="gateOpen[g.id] && g.offenders && g.offenders.length"
                class="bg-indigo-50/40"
              >
                <td colspan="7" class="px-3 py-2 border border-gray-200">
                  <div
                    class="max-h-64 overflow-y-auto rounded border border-gray-200 bg-white"
                  >
                    <table class="min-w-full text-[11px]">
                      <thead class="bg-gray-50 sticky top-0">
                        <tr>
                          <th
                            v-for="col in g.offender_columns"
                            :key="col.key"
                            class="text-left font-semibold text-white px-2 py-1 whitespace-nowrap"
                          >
                            {{ col.label }}
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="(o, i) in g.offenders"
                          :key="i"
                          class="border-t border-gray-100"
                        >
                          <td
                            v-for="col in g.offender_columns"
                            :key="col.key"
                            class="px-2 py-1 align-top text-gray-700"
                            :class="
                              [
                                'faculty',
                                'courses',
                                'programs',
                                'title',
                              ].includes(col.key)
                                ? 'whitespace-normal'
                                : 'whitespace-nowrap font-mono'
                            "
                          >
                            {{ o[col.key] }}
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <p
                    v-if="g.offenders_total > g.offenders.length"
                    class="text-[10px] text-gray-400 mt-1"
                  >
                    showing {{ g.offenders.length }} of {{ g.offenders_total }}
                  </p>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
        <p class="text-[10px] text-gray-400 mt-2 leading-relaxed">
          {{ report.assumptions && report.assumptions.note }}
        </p>
      </div>

      <!-- TAB: Recommendations -->
      <div v-show="activeTab === 'recs'" class="mt-3 overflow-y-auto h-[70vh]">
        <div
          v-if="!report.recommendations || !report.recommendations.length"
          class="rounded-lg border border-green-200 bg-green-50 p-4 text-green-800 text-sm font-medium"
        >
          ✓ No blocking gaps found — the data looks ready to produce a complete
          schedule.
        </div>
        <table v-else class="w-full text-left border-collapse text-[11px]">
          <thead class="bg-gray-100">
            <tr class="text-gray-700 border border-gray-200">
              <th class="px-3 py-2 border border-gray-200 text-center w-24">
                Priority
              </th>
              <th class="px-3 py-2 border border-gray-200">Recommendation</th>
              <th class="px-3 py-2 border border-gray-200">
                What &amp; impact
              </th>
              <th class="px-3 py-2 border border-gray-200 text-center w-24">
                Items
              </th>
            </tr>
          </thead>
          <tbody>
            <template v-for="rec in report.recommendations" :key="rec.key">
              <tr
                class="odd:bg-white even:bg-gray-50 border border-gray-200 align-top"
              >
                <td class="px-3 py-2 border border-gray-200 text-center">
                  <span
                    class="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full"
                    :class="recPill(rec.priority)"
                    >{{ rec.priority }}</span
                  >
                </td>
                <td
                  class="px-3 py-2 border border-gray-200 font-semibold text-gray-800 whitespace-nowrap"
                >
                  <span class="mr-1">{{ recIcon(rec.icon) }}</span
                  >{{ rec.title }}
                </td>
                <td class="px-3 py-2 border border-gray-200 text-gray-700">
                  {{ rec.summary }}
                  <div v-if="rec.impact" class="text-gray-400 mt-0.5">
                    {{ rec.impact }}
                  </div>
                </td>
                <td class="px-3 py-2 border border-gray-200 text-center">
                  <button
                    v-if="rec.items && rec.items.length"
                    @click="toggleRec(rec.key)"
                    class="text-indigo-600 hover:underline font-medium"
                  >
                    {{ recOpen[rec.key] ? "Hide" : "View" }} ({{
                      rec.items_total
                    }})
                  </button>
                  <span v-else class="text-gray-300">—</span>
                </td>
              </tr>
              <tr
                v-if="recOpen[rec.key] && rec.items && rec.items.length"
                class="bg-indigo-50/40"
              >
                <td colspan="4" class="px-3 py-2 border border-gray-200">
                  <div
                    class="max-h-64 overflow-y-auto rounded border border-gray-200 bg-white"
                  >
                    <table class="min-w-full text-[11px]">
                      <thead class="bg-gray-50 sticky top-0">
                        <tr>
                          <th
                            class="text-left font-semibold text-white px-2 py-1 w-40"
                          >
                            Item
                          </th>
                          <th
                            class="text-left font-semibold text-white px-2 py-1"
                          >
                            Detail
                          </th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr
                          v-for="(it, i) in rec.items"
                          :key="i"
                          class="border-t border-gray-100"
                        >
                          <td
                            class="px-2 py-1 font-mono font-semibold text-gray-800 whitespace-nowrap align-top"
                          >
                            {{ it.label }}
                          </td>
                          <td class="px-2 py-1 text-gray-600">{{ it.sub }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                  <p
                    v-if="rec.items_total > rec.items.length"
                    class="text-[10px] text-gray-400 mt-1"
                  >
                    showing {{ rec.items.length }} of {{ rec.items_total }}
                  </p>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import icon from "@/assets/icon.vue";

import { useFetchDataStore } from "@/store/fetch-data-store";
export default {
  name: "TablePreAssessment",
  components: { icon },
  data() {
    return {
      loading: false,
      error: "",
      report: null,
      requestSeq: 0,

      activeTab: "gates",
      gateOpen: {},
      recOpen: {},

      fetchDataStore: useFetchDataStore(),

      selectedInstituteId: "",
      selectedProgramId: "",

      showInstituteDropdown: false,
      showProgramDropdown: false,
    };
  },
  computed: {
    programs() {
      return this.fetchDataStore.programs;
    },

    uniqueInstitutes() {
      const map = new Map();

      this.programs.forEach((p) => {
        if (p.institute) {
          map.set(p.institute.institute_id, {
            id: p.institute.institute_id,
            name: p.institute.institute_code,
            code: p.institute.institute_code,
          });
        }
      });

      return [...map.values()];
    },

    filteredPrograms() {
      return this.programs
        .filter(
          (p) =>
            !this.selectedInstituteId ||
            Number(p.institute_id) === Number(this.selectedInstituteId),
        )
        .map((p) => ({
          id: p.program_id,
          name: p.program_code,
        }));
    },
    tabs() {
      return [
        {
          key: "gates",
          label: "Feasibility gates",
          count: this.report ? this.report.gates.length : 0,
        },
        {
          key: "recs",
          label: "Recommendations",
          count: this.report ? this.report.recommendations.length : 0,
        },
      ];
    },
    verdictLabel() {
      return (
        {
          READY: "Ready",
          READY_WITH_GAPS: "Ready with gaps",
          NOT_READY: "Not ready",
        }[this.report.verdict] || this.report.verdict
      );
    },
    verdictBox() {
      const v = this.report.verdict;
      if (v === "READY")
        return { box: "bg-green-50 border-green-200", text: "text-green-700" };
      if (v === "READY_WITH_GAPS")
        return { box: "bg-amber-50 border-amber-200", text: "text-amber-700" };
      return { box: "bg-red-50 border-red-200", text: "text-red-700" };
    },
  },
  watch: {
    selectedInstituteId() {
      this.runAssessment();
    },
    selectedProgramId() {
      this.runAssessment();
    },
  },
  methods: {
    async runAssessment() {
      const seq = ++this.requestSeq;
      this.loading = true;
      this.error = "";
      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/generated-scheduled/pre-assessment`,
          {
            params: {
              institute_id: this.selectedInstituteId || undefined,
              program_id: this.selectedProgramId || undefined,
            },
          },
        );
        if (seq !== this.requestSeq) return; // a newer request superseded this one
        this.report = res.data.data || null;
        this.gateOpen = {};
        this.recOpen = {};
        this.activeTab = "gates";
        if (!this.report) this.error = "Assessment returned no data.";
      } catch (e) {
        if (seq !== this.requestSeq) return;
        this.error = "Failed to run pre-assessment. Check the server / Python.";
      } finally {
        if (seq === this.requestSeq) this.loading = false;
      }
    },
    toggleGate(id) {
      this.gateOpen[id] = !this.gateOpen[id];
    },
    toggleRec(key) {
      this.recOpen[key] = !this.recOpen[key];
    },
    statusText(s) {
      return { PASS: "OK", WARN: "Warning", FAIL: "Shortage" }[s] || s;
    },
    statusPill(s) {
      return (
        {
          PASS: "bg-green-100 text-green-700",
          WARN: "bg-amber-100 text-amber-700",
          FAIL: "bg-red-100 text-red-700",
        }[s] || "bg-gray-100 text-gray-600"
      );
    },
    barColor(s) {
      return (
        { PASS: "bg-green-500", WARN: "bg-amber-500", FAIL: "bg-red-500" }[s] ||
        "bg-gray-400"
      );
    },
    recIcon(k) {
      return (
        {
          expertise: "🎓",
          faculty: "👤",
          lab: "🧪",
          room: "🏫",
          section: "📚",
        }[k] || "•"
      );
    },
    recPill(p) {
      return (
        {
          high: "bg-red-100 text-red-700",
          medium: "bg-amber-100 text-amber-700",
          low: "bg-gray-100 text-gray-600",
        }[p] || "bg-gray-100 text-gray-600"
      );
    },
  },
  async mounted() {
    if (!this.fetchDataStore.programs.length) {
      this.fetchDataStore.fetchPrograms();
    }
    this.runAssessment();
  },
};
</script>

<style scoped></style>
