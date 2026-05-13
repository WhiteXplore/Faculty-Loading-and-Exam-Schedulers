<template>
  <div
    v-if="visible"
    class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/45 px-4 backdrop-blur-sm"
  >
    <div
      class="w-full max-w-[940px] overflow-hidden rounded-xl bg-white shadow-2xl ring-1 ring-slate-200"
    >
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-slate-100 px-6 py-5">
        <div class="flex items-center gap-3">
          <div
            class="flex h-10 w-10 items-center justify-center rounded-lg bg-red-50 text-red-600 ring-1 ring-red-100"
          >
            <icon name="exclamation-circle" class="h-6 w-6" />
          </div>

          <div>
            <h3 class="text-base font-semibold text-slate-900">
              Scheduled Conflict Detected
            </h3>
            <p class="mt-0.5 text-xs text-slate-500">
              Review the selected schedule and conflicting records below.
            </p>
          </div>
        </div>

        <button
          @click="$emit('cancel')"
          class="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
        >
          ✕
        </button>
      </div>

      <!-- Body -->
      <div class="grid grid-cols-1 gap-5 p-6 lg:grid-cols-2">
        <!-- Selected Schedule -->
        <div class="rounded-xl border border-slate-200 bg-slate-50/60 p-5">
          <div class="mb-4 flex items-center justify-between">
            <span
              class="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 ring-1 ring-emerald-100"
            >
              Selected Schedule
            </span>

            <span
              class="rounded-full px-2.5 py-1 text-xs font-semibold"
              :class="{
                'bg-orange-50 text-orange-700 ring-1 ring-orange-100':
                  schedule.mode === 'face to face',
                'bg-purple-50 text-purple-700 ring-1 ring-purple-100':
                  schedule.mode === 'online',
              }"
            >
              {{ schedule.mode === "face to face" ? "Face to Face" : "Online" }}
            </span>
          </div>

          <h4 class="mb-4 text-lg font-bold text-slate-900">
            {{ schedule.course_code }}
          </h4>

          <div class="grid grid-cols-2 gap-3 text-sm">
            <div class="rounded-lg bg-white p-3 ring-1 ring-slate-100">
              <p class="text-xs text-slate-500">Faculty</p>
              <p class="mt-1 font-semibold text-slate-800">
                {{ schedule.faculty_name }}
              </p>
            </div>

            <div class="rounded-lg bg-white p-3 ring-1 ring-slate-100">
              <p class="text-xs text-slate-500">Section</p>
              <p class="mt-1 font-semibold text-slate-800">
                {{ schedule.program_code }}-{{ schedule.set_name }}
              </p>
            </div>

            <div class="rounded-lg bg-white p-3 ring-1 ring-slate-100">
              <p class="text-xs text-slate-500">Room</p>
              <p class="mt-1 font-semibold text-slate-800">
                {{ schedule.room_name }}
              </p>
            </div>

            <div class="rounded-lg bg-white p-3 ring-1 ring-slate-100">
              <p class="text-xs text-slate-500">Room Type</p>
              <p class="mt-1 font-semibold text-slate-800">
                {{ schedule.room_type }}
              </p>
            </div>

            <div class="rounded-lg bg-white p-3 ring-1 ring-slate-100">
              <p class="text-xs text-slate-500">Day</p>
              <p class="mt-1 font-semibold text-slate-800">
                {{ schedule.day }}
              </p>
            </div>

            <div class="rounded-lg bg-white p-3 ring-1 ring-slate-100">
              <p class="text-xs text-slate-500">Time</p>
              <p class="mt-1 font-semibold text-slate-800">
                {{ formatTime(schedule.start_hour) }} –
                {{ formatTime(schedule.start_hour + schedule.duration) }}
              </p>
            </div>
          </div>
        </div>

        <!-- Conflicting Schedules -->
        <div class="rounded-xl border border-slate-200 bg-white p-5">
          <div class="mb-4 flex items-center justify-between">
            <span
              class="rounded-full bg-red-50 px-3 py-1 text-xs font-semibold text-red-700 ring-1 ring-red-100"
            >
              Conflicting Schedules
            </span>

            <span class="text-xs font-medium text-slate-400">
              {{ conflicts.length }} record(s)
            </span>
          </div>

          <div class="max-h-[420px] space-y-3 overflow-y-auto pr-2">
            <div
              v-for="conflict in conflicts"
              :key="conflict.id"
              class="rounded-xl border p-4 transition hover:shadow-sm"
              :class="{
                'border-red-100 bg-red-50/60':
                  conflict.reason !== 'Part of the joined schedule',
                'border-amber-100 bg-amber-50/70':
                  conflict.reason === 'Part of the joined schedule',
              }"
            >
              <div class="mb-3 flex items-center justify-between gap-3">
                <h5 class="font-semibold text-slate-900">
                  {{ conflict.course_code }}
                </h5>

                <span
                  class="shrink-0 rounded-full px-2.5 py-1 text-xs font-semibold"
                  :class="{
                    'bg-orange-100 text-orange-700': conflict.mode === 'face to face',
                    'bg-purple-100 text-purple-700': conflict.mode === 'online',
                  }"
                >
                  {{ conflict.mode === "face to face" ? "Face to Face" : "Online" }}
                </span>
              </div>

              <div class="grid grid-cols-2 gap-3 text-sm">
                <div>
                  <p class="text-xs text-slate-500">Faculty</p>
                  <p class="font-medium text-slate-800">
                    {{ conflict.faculty_name }}
                  </p>
                </div>

                <div>
                  <p class="text-xs text-slate-500">Section</p>
                  <p class="font-medium text-slate-800">
                    {{ conflict.program_code }}-{{ conflict.set_name }}
                  </p>
                </div>

                <div>
                  <p class="text-xs text-slate-500">Room</p>
                  <p class="font-medium text-slate-800">
                    {{ conflict.room_name }}
                  </p>
                </div>

                <div>
                  <p class="text-xs text-slate-500">Room Type</p>
                  <p class="font-medium text-slate-800">
                    {{ conflict.room_type }}
                  </p>
                </div>

                <div>
                  <p class="text-xs text-slate-500">Day</p>
                  <p class="font-medium text-slate-800">
                    {{ conflict.day }}
                  </p>
                </div>

                <div>
                  <p class="text-xs text-slate-500">Time</p>
                  <p class="font-medium text-slate-800">
                    {{ formatTime(conflict.start_hour) }} –
                    {{ formatTime(conflict.start_hour + conflict.duration) }}
                  </p>
                </div>
              </div>

              <div
                class="mt-4 flex items-start gap-2 rounded-lg px-3 py-2 text-xs font-medium"
                :class="{
                  'bg-white text-red-700 ring-1 ring-red-100':
                    conflict.reason !== 'Part of the joined schedule',
                  'bg-white text-amber-700 ring-1 ring-amber-100':
                    conflict.reason === 'Part of the joined schedule',
                }"
              >
                <span>⚠</span>
                <span>{{ conflict.reason || "Schedule overlap detected" }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="flex justify-end border-t border-slate-100 bg-slate-50 px-6 py-4">
        <button
          @click="$emit('close')"
          class="rounded-lg bg-slate-900 px-5 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
        >
          Close
        </button>
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
    schedule: Object,
    conflicts: Array,
  },
  methods: {
    formatTime(hour) {
      const h = Math.floor(hour);
      const m = (hour % 1) * 60;
      return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}`;
    },
  },
};
</script>
