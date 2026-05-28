<template>
  <div
    v-if="visible"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-[2px] px-4"
  >
    <!-- Modal -->
    <div
      class="w-full max-w-5xl overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_12px_40px_rgba(15,23,42,0.12)]"
    >
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-slate-200 px-5 py-4">
        <div class="flex items-center gap-3">
          <div
            class="flex h-10 w-10 items-center justify-center rounded-xl border border-red-100 bg-red-50 text-red-600"
          >
            <icon name="exclamation-circle" class="h-5 w-5" />
          </div>

          <div>
            <h3 class="text-[16px] font-semibold tracking-tight text-slate-900">
              Schedule Conflict
            </h3>

            <p class="mt-0.5 text-[12px] font-medium text-slate-500">
              Existing schedules overlap with the selected time slot.
            </p>
          </div>
        </div>

        <button
          @click="$emit('close')"
          class="flex h-8 w-8 items-center justify-center rounded-lg border border-slate-200 text-slate-400 transition-all duration-200 hover:bg-slate-100 hover:text-slate-700"
        >
          ✕
        </button>
      </div>

      <!-- Body -->
      <div class="grid grid-cols-1 gap-5 bg-slate-50/40 p-5 xl:grid-cols-2">
        <!-- Selected Schedule -->
        <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
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
              {{ schedule.mode === "face to face" ? "Face to Face" : "Online" }}
            </div>
          </div>

          <!-- Course -->
          <div class="mb-5">
            <h2 class="text-[20px] font-semibold tracking-tight text-slate-900">
              {{ schedule.course_code || "No Course" }}
            </h2>

            <p class="mt-1 text-[13px] text-slate-500">
              {{ schedule.program_code || "-" }} -
              {{ schedule.set_name || "-" }}
            </p>
          </div>

          <!-- Details -->
          <div class="grid grid-cols-2 gap-3">
            <div class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5">
              <p class="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
                Faculty
              </p>

              <p class="mt-1 text-[13px] font-medium text-slate-800">
                {{ schedule.faculty_name || "-" }}
              </p>
            </div>

            <div class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5">
              <p class="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
                Section
              </p>

              <p class="mt-1 text-[13px] font-medium text-slate-800">
                {{ schedule.program_code || "-" }}-{{ schedule.set_name || "-" }}
              </p>
            </div>

            <div class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5">
              <p class="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
                Room
              </p>

              <p class="mt-1 text-[13px] font-medium text-slate-800">
                {{ schedule.room_name || "-" }}
              </p>
            </div>

            <div class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5">
              <p class="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
                Room Type
              </p>

              <p class="mt-1 text-[13px] font-medium text-slate-800">
                {{ schedule.room_type || "-" }}
              </p>
            </div>

            <div class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5">
              <p class="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
                Day
              </p>

              <p class="mt-1 text-[13px] font-medium text-slate-800">
                {{ schedule.day || "-" }}
              </p>
            </div>

            <div class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5">
              <p class="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
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
        <div class="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
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
                'border-red-200': conflict.reason !== 'Part of the joined schedule',

                'border-amber-200': conflict.reason === 'Part of the joined schedule',
              }"
            >
              <!-- Top -->
              <div class="mb-4 flex items-start justify-between gap-3">
                <div>
                  <h4 class="text-[15px] font-semibold tracking-tight text-slate-900">
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
                  {{ conflict.mode === "face to face" ? "Face to Face" : "Online" }}
                </div>
              </div>

              <!-- Details -->
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <p class="text-[10px] uppercase tracking-wide text-slate-400">
                    Faculty
                  </p>

                  <p class="mt-1 text-[13px] font-medium text-slate-800">
                    {{ conflict.faculty_name || "-" }}
                  </p>
                </div>

                <div>
                  <p class="text-[10px] uppercase tracking-wide text-slate-400">Room</p>

                  <p class="mt-1 text-[13px] font-medium text-slate-800">
                    {{ conflict.room_name || "-" }}
                  </p>
                </div>

                <div>
                  <p class="text-[10px] uppercase tracking-wide text-slate-400">Day</p>

                  <p class="mt-1 text-[13px] font-medium text-slate-800">
                    {{ conflict.day || "-" }}
                  </p>
                </div>

                <div>
                  <p class="text-[10px] uppercase tracking-wide text-slate-400">Time</p>

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
        class="flex items-center justify-end border-t border-slate-200 bg-white px-5 py-4"
      >
        <button @click="$emit('close')" class="btn-cancel">Close</button>
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

      return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}`;
    },
  },
};
</script>
