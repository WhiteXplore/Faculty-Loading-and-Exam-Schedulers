<template>
  <div class="modal-overlay" v-if="visible">
    <div class="modal-wrapper">
      <div class="modal-container">
        <!-- Header -->

        <div class="modal-header">
          <div class="flex items-center gap-3">
            <!-- Icon -->
            <div class="glass-container">
              <icon name="exclamation-circle" class="h-5 w-5 text-white" />
            </div>

            <!-- Title -->
            <div>
              <h2 class="text-lg font-semibold text-white">
                Schedule Conflict
              </h2>

              <p class="text-xs text-green-100">
                Manage and check the conflicting records of the selected
                schedule.
              </p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <!-- Body -->

        <div class="grid grid-cols-1 gap-5 p-5 xl:grid-cols-2 w-[50vw]">
          <!-- Selected Schedule -->
          <div
            class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
          >
            <div class="mb-5 flex items-center justify-between">
              <div
                class="rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1 text-[10px] font-semibold uppercase tracking-wide text-emerald-700"
              >
                Selected Schedule
              </div>

              <div
                class="rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-wide"
                :class="{
                  'border border-orange-200 bg-orange-50 text-orange-700':
                    schedule.mode === 'face to face',

                  'border border-violet-200 bg-violet-50 text-violet-700':
                    schedule.mode === 'online',
                }"
              >
                {{
                  schedule.mode === "face to face" ? "Face to Face" : "Online"
                }}
              </div>
            </div>

            <!-- Course -->
            <div class="mb-5">
              <h2
                class="text-[20px] font-semibold tracking-tight text-slate-900"
              >
                {{ schedule.course_code || "No Course" }}
              </h2>

              <p class="mt-1 text-[13px] text-slate-500">
                {{ schedule.program_code || "-" }} -
                {{ schedule.set_name || "-" }}
              </p>
            </div>

            <!-- Details -->
            <div class="grid grid-cols-2 gap-3">
              <div class="rounded-lg px-3 py-2.5">
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Faculty
                </p>

                <p class="mt-1 text-[13px] font-medium text-slate-800">
                  {{ schedule.faculty_name || "-" }}
                </p>
              </div>

              <div class="rounded-lg px-3 py-2.5">
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Section
                </p>

                <p class="mt-1 text-[13px] font-medium text-slate-800">
                  {{ schedule.program_code || "-" }}-{{
                    schedule.set_name || "-"
                  }}
                </p>
              </div>

              <div class="rounded-lg px-3 py-2.5">
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Room
                </p>

                <p class="mt-1 text-[13px] font-medium text-slate-800">
                  {{ schedule.room_name || "-" }}
                </p>
              </div>

              <div class="rounded-lg px-3 py-2.5">
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Room Type
                </p>

                <p class="mt-1 text-[13px] font-medium text-slate-800">
                  {{ schedule.room_type || "-" }}
                </p>
              </div>

              <div class="rounded-lg px-3 py-2.5">
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Day
                </p>

                <p class="mt-1 text-[13px] font-medium text-slate-800">
                  {{ schedule.day || "-" }}
                </p>
              </div>

              <div class="rounded-lg px-3 py-2.5">
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Time
                </p>

                <p class="mt-1 text-[13px] font-semibold text-slate-900">
                  {{ formatTime(schedule.start_hour) }}
                  —
                  {{ formatTime(schedule.start_hour + schedule.duration) }}
                </p>
              </div>
            </div>
          </div>

          <!-- Conflict Records -->
          <div
            class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
          >
            <div class="mb-5 flex items-center justify-between">
              <div
                class="rounded-full border border-red-100 bg-red-50 px-3 py-1 text-[10px] font-semibold uppercase tracking-wide text-red-700"
              >
                Conflict Records
              </div>

              <div class="text-[12px] font-medium text-slate-400">
                {{ conflicts.length }} conflict(s)
              </div>
            </div>

            <div class="max-h-[480px] space-y-3 overflow-y-auto pr-1">
              <div
                v-for="conflict in conflicts"
                :key="conflict.id"
                class="rounded-xl border bg-white p-4 transition-all duration-200 hover:shadow-sm"
                :class="{
                  'border-red-200':
                    conflict.reason !== 'Part of the joined schedule',

                  'border-amber-200':
                    conflict.reason === 'Part of the joined schedule',
                }"
              >
                <!-- Top -->
                <div class="mb-4 flex items-start justify-between gap-3">
                  <div>
                    <h4
                      class="text-[15px] font-semibold tracking-tight text-slate-900"
                    >
                      {{ conflict.course_code || "-" }}
                    </h4>

                    <p class="mt-1 text-[12px] text-slate-500">
                      {{ conflict.program_code || "-" }} -
                      {{ conflict.set_name || "-" }}
                    </p>
                  </div>

                  <div
                    class="rounded-full px-3 py-1 text-[10px] font-semibold uppercase tracking-wide"
                    :class="{
                      'bg-orange-50 text-orange-700 border border-orange-200':
                        conflict.mode === 'face to face',

                      'bg-violet-50 text-violet-700 border border-violet-200':
                        conflict.mode === 'online',
                    }"
                  >
                    {{
                      conflict.mode === "face to face"
                        ? "Face to Face"
                        : "Online"
                    }}
                  </div>
                </div>

                <!-- Details -->
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <p
                      class="text-[10px] uppercase tracking-wide text-slate-400"
                    >
                      Faculty
                    </p>

                    <p class="mt-1 text-[13px] font-medium text-slate-800">
                      {{ conflict.faculty_name || "-" }}
                    </p>
                  </div>

                  <div>
                    <p
                      class="text-[10px] uppercase tracking-wide text-slate-400"
                    >
                      Room
                    </p>

                    <p class="mt-1 text-[13px] font-medium text-slate-800">
                      {{ conflict.room_name || "-" }}
                    </p>
                  </div>

                  <div>
                    <p
                      class="text-[10px] uppercase tracking-wide text-slate-400"
                    >
                      Day
                    </p>

                    <p class="mt-1 text-[13px] font-medium text-slate-800">
                      {{ conflict.day || "-" }}
                    </p>
                  </div>

                  <div>
                    <p
                      class="text-[10px] uppercase tracking-wide text-slate-400"
                    >
                      Time
                    </p>

                    <p class="mt-1 text-[13px] font-semibold text-slate-900">
                      {{ formatTime(conflict.start_hour) }}
                      —
                      {{ formatTime(conflict.start_hour + conflict.duration) }}
                    </p>
                  </div>
                </div>

                <!-- Reason -->
                <div
                  class="mt-4 flex items-start gap-2 rounded-lg border px-3 py-2 text-[12px] font-medium"
                  :class="{
                    'border-red-200 bg-red-50 text-red-700':
                      conflict.reason !== 'Part of the joined schedule',

                    'border-amber-200 bg-amber-50 text-amber-700':
                      conflict.reason === 'Part of the joined schedule',
                  }"
                >
                  <span>⚠</span>

                  <span>
                    {{ conflict.reason || "Schedule overlap detected." }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div
          class="flex items-center justify-end border-t border-slate-200 bg-white px-5 py-4 rounded-b-xl"
        >
          <button @click="$emit('close')" class="btn-cancel">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";

export default {
  name: "ConflictModal",

  components: {
    icon,
  },

  props: {
    visible: Boolean,
    schedule: {
      type: Object,
      default: () => ({}),
    },

    conflicts: {
      type: Array,
      default: () => [],
    },
  },

  methods: {
    formatTime(hour) {
      if (hour === null || hour === undefined) return "--:--";

      const h = Math.floor(hour);
      const m = (hour % 1) * 60;

      return `${h.toString().padStart(2, "0")}:${m
        .toString()
        .padStart(2, "0")}`;
    },
  },
};
</script>
