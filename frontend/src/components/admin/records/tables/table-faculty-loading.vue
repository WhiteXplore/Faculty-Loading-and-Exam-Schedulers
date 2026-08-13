<template>
  <!-- TODO Loading Overlay -->
  <transition name="loader-fade" appear>
    <div v-if="loading" class="relative z-50" role="dialog" aria-modal="true">
      <div
        class="fixed inset-0 flex items-center justify-center bg-[#063f2f]/90 backdrop-blur-md"
      >
        <div class="flex flex-col items-center justify-center animate-loaderUp">
          <!-- Loader Container -->
          <div class="relative flex h-36 w-36 items-center justify-center">
            <!-- Outer Ring -->
            <div
              class="absolute h-36 w-36 rounded-full border-4 border-white/10 border-t-green-300 animate-spin"
            ></div>

            <!-- Pulse Ring -->
            <div
              class="absolute h-32 w-32 rounded-full border border-green-300/40 animate-ping"
            ></div>

            <!-- Middle Glow -->
            <div
              class="absolute h-28 w-28 rounded-full bg-white/10 blur-xl animate-pulse"
            ></div>

            <!-- Progress Card -->
            <div
              class="relative flex h-24 w-24 items-center justify-center rounded-full bg-white shadow-2xl ring-1 ring-white/40"
            >
              <span class="text-defaultGreen text-xl font-bold">
                {{ Math.floor(progress) }}%
              </span>
            </div>
          </div>

          <!-- Text -->
          <div class="mt-8 text-center animate-fadeDelay">
            <h2 class="text-lg font-bold tracking-wide text-white">
              Generating Schedule...
            </h2>

            <p class="mt-2 text-sm text-white/70">
              Please wait while we finalize your data.
            </p>
          </div>

          <!-- Progress Dots -->
          <div class="mt-5 flex gap-2">
            <span
              class="h-2 w-2 animate-bounce rounded-full bg-white/80"
            ></span>
            <span
              class="h-2 w-2 animate-bounce rounded-full bg-white/80"
              style="animation-delay: 0.15s"
            ></span>
            <span
              class="h-2 w-2 animate-bounce rounded-full bg-white/80"
              style="animation-delay: 0.3s"
            ></span>
          </div>
        </div>
      </div>
    </div>
  </transition>

  <!-- TODO  Confirm Save Modal -->
  <div
    v-if="showConfirmSaved"
    class="fixed inset-0 flex items-center justify-center bg-black/30 z-50"
  >
    <div class="bg-white rounded-2xl shadow-2xl p-6 w-96">
      <!-- TODO  Header -->
      <div class="flex items-center justify-between border-b pb-3 mb-4">
        <!-- Left: Icon + Title -->
        <div class="per-page-container">
          <icon
            name="exclamation-circle"
            class="w-7 h-7 p-1 rounded-full bg-green-200 text-green-900 flex items-center justify-center"
          />
          <h3 class="text-lg font-semibold text-gray-800 leading-none">
            Confirm Save
          </h3>
        </div>
      </div>

      <!-- TODO  Message -->
      <p class="text-gray-600 mb-6">
        Are you sure you want to save this schedule?
      </p>

      <!-- TODO  Buttons -->
      <div class="flex justify-center gap-2 text-sm">
        <button @click="showConfirmSaved = false" class="btn-cancel">
          Cancel
        </button>
        <button
          @click="saveScheduledConfirmed"
          :disabled="savingSchedule"
          class="btn-save disabled:opacity-70 disabled:cursor-not-allowed"
        >
          <span v-if="savingSchedule" class="flex items-center gap-2">
            <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
              <circle
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="3"
                opacity="0.25"
              />
              <path
                d="M22 12a10 10 0 0 1-10 10"
                stroke="currentColor"
                stroke-width="3"
              />
            </svg>
            Saving...
          </span>

          <span v-else>Yes, Save</span>
        </button>
      </div>
    </div>
  </div>
  <div class="flex flex-col h-[83vh] overflow-hidden">
    <!-- TODO  Top Controls -->
    <div class="flex flex-wrap items-center justify-between">
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
            :class="!selectedInstituteId ? 'opacity-60 cursor-not-allowed' : ''"
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

      <!-- RIGHT SIDE -->
      <div class="flex flex-wrap items-center gap-2 mt-1">
        <!-- Filters -->

        <!-- LEFT : Faculty Search -->
        <div class="search-wrapper">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search faculty..."
            class="search-input"
          />

          <div
            class="absolute inset-y-0 left-3 flex items-center text-defaultGreen pointer-events-none"
          >
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
        <!-- Actions -->
        <div class="per-page-container">
          <!-- Generate -->
          <button @click="generateSchedule" class="btn-download">
            <div class="btn-download-icon">
              <icon name="arrow-path" />
            </div>
            <span class="btn-download-text">Generate</span>
          </button>

          <!-- Save -->
          <!-- <button @click="showConfirmSaved = true" class="btn-download">
            <div class="btn-add-icon">
              <icon name="circle-check" />
            </div>
            <span class="btn-add-text">Save Schedule</span>
          </button> -->
          <button @click="showConfirmSaved = true" class="btn-add">
            <div class="btn-add-icon">
              <icon name="arrow-path" />
            </div>
            <span class="btn-add-text">Save Schedule</span>
          </button>

          <!-- Download -->
          <button
            @click="downloadSchedule"
            :disabled="downloadingSchedule"
            class="btn-download disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <div class="btn-download-icon">
              <icon name="download" />
            </div>
            <span class="btn-download-text">
              {{ downloadingSchedule ? "Downloading..." : "Download Schedule" }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- TODO  Scrollable Content -->
    <div class="flex-1 overflow-y-auto scrollbar-hide">
      <div>
        <!-- TODO  Faculty Cards -->
        <div
          v-if="Object.keys(filteredFacultyCards).length"
          :class="[
            'gap-2 grid  overflow-hidden mt-2',
            Object.keys(filteredFacultyCards).length === 1
              ? 'grid-cols-1'
              : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-2',
          ]"
        >
          <div
            v-for="(schedules, instructor) in filteredFacultyCards"
            :key="instructor"
            class="bg-white rounded-xl border flex flex-col relative"
          >
            <!-- TODO  Header -->
            <div
              class="flex items-center justify-between rounded-t-xl bg-gradient-to-r from-defaultGreen to-[#0F6345] px-5 py-3 text-white"
            >
              <!-- Faculty Name -->
              <h3 class="text-lg font-semibold tracking-wide">
                {{ instructor }}
              </h3>

              <!-- Summary -->
              <div
                v-if="facultyTotalUnits[instructor]"
                class="flex items-center gap-3"
              >
                <!-- Set Load -->
                <div
                  class="rounded-full bg-white/10 px-4 py-1.5 backdrop-blur-sm flex items-center gap-2"
                >
                  <p class="text-[10px] uppercase tracking-wider text-white">
                    Set Load:
                  </p>
                  <p class="text-xs font-semibold">
                    {{ facultyTotalUnits[instructor].unitLoad }}
                    <span class="">Units</span>
                  </p>
                </div>

                <!-- Total Units -->
                <div
                  class="rounded-full px-4 py-1.5 backdrop-blur-sm flex items-center gap-2"
                  :class="
                    Number(facultyTotalUnits[instructor].totalUnits) >
                    Number(facultyTotalUnits[instructor].unitLoad)
                      ? 'bg-red-600/70 text-red-100 border border-red-300'
                      : 'bg-white/10 text-white'
                  "
                >
                  <p class="text-[10px] uppercase tracking-wider">
                    Total Units
                  </p>
                  <p class="text-xs font-semibold">
                    {{ facultyTotalUnits[instructor].totalUnits }}
                    <span class="">Units</span>
                  </p>
                </div>

                <!-- Overload Badge -->
                <!-- <span
                  v-if="
                    Number(facultyTotalUnits[instructor].totalUnits) >
                    Number(facultyTotalUnits[instructor].unitLoad)
                  "
                  class="rounded-full bg-red-500 px-3 py-1 text-xs font-semibold uppercase tracking-wide"
                >
                  OVERLOAD
                </span> -->
              </div>
            </div>

            <!-- TODO  Schedule Table -->
            <div class="flex-1">
              <table class="w-full text-left border-collapse text-[11px]">
                <!-- <thead class="sticky top-0 bg-gray-100 z-10"></thead> -->
                <thead class="top-0 bg-gray-100 z-10">
                  <tr class="text-gray-700 border border-gray-200">
                    <th
                      class="px-4 py-2 border border-gray-200 bg-gray-100 text-gray-700 w-24 text-center"
                    >
                      Time
                    </th>
                    <th
                      v-for="day in days"
                      :key="day"
                      class="px-4 py-2 border border-gray-200 bg-gray-100 text-gray-700 text-center w-28"
                    >
                      {{ day }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="slot in timeSlots"
                    :key="slot.start + slot.end"
                    class="odd:bg-white even:bg-gray-50"
                  >
                    <td
                      class="px-3 border border-gray-200 text-center text-gray-700 whitespace-nowrap"
                    >
                      {{ formatTime(slot.start) }} - {{ formatTime(slot.end) }}
                    </td>
                    <td
                      v-for="day in days"
                      :key="day"
                      class="relative border border-gray-200 text-left align-top h-[60px] p-0"
                    >
                      <template
                        v-for="item in getScheduleForCell(
                          slot,
                          day,
                          instructor,
                        )"
                        :key="
                          item.course_name + item.start_hour + item.room_name
                        "
                      >
                        <div
                          v-if="isStartingSlot(item, slot)"
                          draggable="true"
                          @mouseenter="showScheduleTooltip($event, item)"
                          @mouseleave="hideScheduleTooltip"
                          @click="highlightRow(item)"
                          :class="[
                            'absolute inset-x-1 border rounded text-[11px] p-1 shadow-sm truncate cursor-pointer',
                            item.id?.toString().startsWith('temp-')
                              ? 'bg-purple-200 border-purple-400 text-purple-900'
                              : getTypeColor(item.type),
                            hasRoomConflict(item)
                              ? 'bg-red-300 border-red-500 text-red-900'
                              : '',
                          ]"
                          :style="{
                            top: getBlockTop(item, slot.start) + 'px',
                            height: getBlockHeight(item) + 'px',
                            width: 'calc(100% - 0.5rem)',
                            zIndex: 20,
                          }"
                        >
                          <!-- schedule_type BADGE -->
                          <span
                            v-if="item.schedule_type"
                            :class="[
                              'absolute top-1 right-1 w-auto h-4 px-1 rounded-full text-[10px] font-bold flex items-center justify-center text-white',
                              item.schedule_type === 'face to face'
                                ? 'bg-orange-500'
                                : '',
                              item.schedule_type === 'online'
                                ? 'bg-purple-500'
                                : '',
                            ]"
                          >
                            {{
                              item.schedule_type === "face to face"
                                ? "F2F"
                                : "OL"
                            }}
                          </span>
                          <div class="leading-snug truncate">
                            <p class="font-semibold truncate">
                              {{ item.course_code }}
                            </p>
                            <p class="text-gray-600 truncate">
                              {{ item.room_name }}
                            </p>
                            <p class="text-gray-600 truncate">
                              {{ item.program_code }}-{{ item.set_name }}
                            </p>
                            <button
                              v-if="hasRoomConflict(item) && !isJoined"
                              @click.stop="openConflictModal(item)"
                              class="absolute bottom-1 right-1 flex items-center justify-center w-4 h-4 rounded-full bg-red-600 text-white text-[9px] font-bold shadow hover:bg-red-700"
                              title="View conflict"
                            >
                              !
                            </button>
                          </div>
                        </div>
                      </template>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- 🔍 Schedule Tooltip -->
            <div
              v-if="scheduleTooltipVisible && tooltipItem"
              class="fixed z-[9999] pointer-events-none"
              :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
            >
              <div
                class="w-[280px] overflow-hidden rounded-xl border border-gray-200 bg-white"
              >
                <div
                  class="border-b border-gray-100 bg-gradient-to-r from-emerald-50 to-white px-4 py-3"
                >
                  <div class="flex items-start justify-between gap-3">
                    <div>
                      <p
                        class="text-[10px] font-semibold uppercase tracking-wide text-gray-400"
                      >
                        Schedule Details
                      </p>
                      <h3
                        class="mt-0.5 text-sm font-bold text-defaultGreen leading-tight"
                      >
                        {{ tooltipItem.course_code }}
                      </h3>
                    </div>

                    <span
                      v-if="tooltipItem.schedule_type"
                      class="shrink-0 inline-flex items-center rounded-full px-2.5 py-1 text-[9px] font-semibold text-white shadow-sm"
                      :class="
                        tooltipItem.schedule_type === 'face to face'
                          ? 'bg-orange-500'
                          : 'bg-purple-500'
                      "
                    >
                      {{
                        tooltipItem.schedule_type === "face to face"
                          ? "Face to Face"
                          : "Online"
                      }}
                    </span>
                  </div>
                </div>

                <div class="px-4 py-3 space-y-3 text-[11px] text-gray-700">
                  <!-- <div>
                    <p
                      class="text-[9px] font-semibold uppercase tracking-wide text-gray-400"
                    >
                      Faculty
                    </p>
                    <p class="mt-0.5 font-semibold text-gray-800">
                      {{ tooltipItem.faculty_name || "Not assigned" }}
                    </p>
                  </div> -->

                  <div>
                    <p
                      class="text-[9px] font-semibold uppercase tracking-wide text-gray-400"
                    >
                      Year & Section
                    </p>
                    <div
                      class="mt-1 rounded-lg border border-gray-100 bg-gray-50 px-2.5 py-1.5"
                    >
                      <p class="font-semibold text-gray-800">
                        {{ tooltipItem.program_code }} -
                        {{ tooltipItem.set_name }}
                      </p>
                    </div>
                  </div>

                  <div class="grid grid-cols-2 gap-2">
                    <div class="rounded-lg bg-gray-50 px-2.5 py-2">
                      <p
                        class="text-[9px] font-semibold uppercase text-gray-400"
                      >
                        Room
                      </p>
                      <p class="mt-0.5 font-semibold text-gray-800">
                        {{ tooltipItem.room_name || "TBA" }}
                      </p>
                    </div>

                    <div class="rounded-lg bg-gray-50 px-2.5 py-2">
                      <p
                        class="text-[9px] font-semibold uppercase text-gray-400"
                      >
                        Day
                      </p>
                      <p class="mt-0.5 font-semibold text-gray-800">
                        {{ tooltipItem.day || "-" }}
                      </p>
                    </div>

                    <div class="rounded-lg bg-gray-50 px-2.5 py-2 col-span-2">
                      <p
                        class="text-[9px] font-semibold uppercase text-gray-400"
                      >
                        Time
                      </p>
                      <p class="mt-0.5 font-semibold text-gray-800">
                        {{ formatTime(tooltipItem.start_hour) }} –
                        {{
                          formatTime(
                            tooltipItem.start_hour +
                              Number(tooltipItem.duration),
                          )
                        }}
                      </p>
                    </div>

                    <div class="rounded-lg bg-gray-50 px-2.5 py-2">
                      <p
                        class="text-[9px] font-semibold uppercase text-gray-400"
                      >
                        Type
                      </p>
                      <p class="mt-0.5 font-semibold text-gray-800">
                        {{ tooltipItem.type || "-" }}
                      </p>
                    </div>

                    <div class="rounded-lg bg-gray-50 px-2.5 py-2">
                      <p
                        class="text-[9px] font-semibold uppercase text-gray-400"
                      >
                        Campus
                      </p>
                      <p class="mt-0.5 font-semibold text-gray-800 truncate">
                        {{
                          getCollegeBranchName(tooltipItem.college_branch_id)
                        }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- TODO  Fallback ONLY for Faculty Cards -->
        <div
          v-else
          class="flex flex-col items-center justify-center min-h-[400px] text-center text-gray-500"
        >
          <div class="text-center text-gray-500">
            <p class="text-lg font-semibold mb-2">No schedule data available</p>
            <p class="text-sm text-gray-400">
              Please click
              <span class="font-medium text-defaultGreen">"Generate"</span>
              to generate schedule data.
            </p>
          </div>
        </div>
        <div
          v-if="totalCardPages > 1"
          class="flex justify-center items-center gap-2 mt-4"
        >
          <button
            @click="cardPage--"
            :disabled="cardPage === 1"
            class="px-3 py-1 rounded-lg bg-gray-200 disabled:opacity-50"
          >
            &lt;
          </button>

          <span class="text-sm font-medium text-gray-600">
            Page {{ cardPage }} of {{ totalCardPages }}
          </span>

          <button
            @click="cardPage++"
            :disabled="cardPage === totalCardPages"
            class="px-3 py-1 rounded-lg bg-gray-200 disabled:opacity-50"
          >
            &gt;
          </button>
        </div>
      </div>
    </div>
    <div
      v-if="showOverrideModal"
      class="fixed inset-0 z-[999] flex items-center justify-center bg-black/40"
    >
      <div class="w-[430px] rounded-2xl bg-white shadow-xl">
        <!-- Header -->
        <div class="flex items-center gap-3 px-6 py-5 border-b">
          <div
            class="flex h-10 w-10 items-center justify-center rounded-full bg-red-100"
          >
            <icon name="exclamation-circle" class="w-5 h-5 text-red-700" />
          </div>

          <div>
            <h3 class="text-base font-semibold text-gray-900">
              Schedule Already Generated
            </h3>
            <p class="text-sm text-gray-500">An existing schedule was found.</p>
          </div>
        </div>

        <!-- Content -->
        <div class="px-6 py-5">
          <div class="space-y-3">
            <div class="flex justify-between text-sm">
              <span class="text-gray-500">School Year</span>
              <span class="font-medium text-gray-900">
                {{ overrideInfo?.school_year }}
              </span>
            </div>

            <div class="flex justify-between text-sm">
              <span class="text-gray-500">Semester</span>
              <span class="font-medium text-gray-900">
                {{ overrideInfo?.semester }}
              </span>
            </div>
          </div>

          <p class="mt-5 text-sm text-gray-600 italic">
            Note: "Continuing will replace the existing generated schedule for
            this school year and semester".
          </p>
        </div>

        <!-- Footer -->
        <div
          class="flex justify-end gap-2 px-6 py-4 border-t bg-gray-50 rounded-b-2xl"
        >
          <button @click="showOverrideModal = false" class="btn-cancel">
            Cancel
          </button>

          <button
            @click="overrideSchedule"
            :disabled="overridingSchedule"
            class="btn-save disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <span v-if="overridingSchedule" class="flex items-center gap-2">
              <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                <circle
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="3"
                  opacity="0.25"
                />
                <path
                  d="M22 12a10 10 0 0 1-10 10"
                  stroke="currentColor"
                  stroke-width="3"
                />
              </svg>
              Saving...
            </span>

            <span v-else>Override & Save</span>
          </button>
        </div>
      </div>
    </div>

    <ConflictModal
      :visible="conflictModalVisible"
      :schedule="selectedSchedule"
      :conflicts="conflictRecords"
      @close="closeConflictModal"
      @cancel="closeConflictModal"
    />
  </div>
</template>

<script>
import axios from "axios";
import * as XLSX from "xlsx";
import icon from "@/assets/icon.vue";
import { useFetchDataStore } from "@/store/fetch-data-store";
import ConflictModal from "@/components/program-chairperson/program-record/faculty-components/conflict-modal.vue";
import { toast } from "vue3-toastify";
import { eventBus } from "@/bus/event-bus";
// import sample_schedule from "./sample_schedule.json";
export default {
  name: "FacultySchedule",
  components: { icon, ConflictModal },

  data() {
    return {
      user: {},
      schedule: [],
      unscheduledMeetings: [],
      groupedSchedule: {},
      filteredGroupedSchedule: {},
      loading: false,
      error: null,
      showFacultyTable: false,
      selectedInstructor: null,
      scheduleGenerated: false,
      selectedInstituteId: "",
      selectedProgramId: "",
      showConfirmSaved: false,
      days: [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ],

      timeSlots: Array.from({ length: 14 }, (_, i) => ({
        start: 7 + i, // 7, 8, 9 ... 20
        end: 8 + i, // 8, 9, 10 ... 21
      })),

      progress: 0,
      progressInterval: null,
      showConflictModal: false,
      selectedConflict: {},
      currentPage: 1,
      itemsPerPage: 10,
      timeSlotHeight: 60,

      schoolYears: [],

      conflictModalVisible: false,
      scheduleTooltipVisible: false,
      tooltipItem: null,
      tooltipX: 0,
      tooltipY: 0,
      cardPage: 1,
      cardsPerPage: 6,
      pageWindow: 3,
      searchQuery: "",
      showOverrideModal: false,
      overrideInfo: null,
      savingSchedule: false,
      overridingSchedule: false,
      downloadingSchedule: false,
      stopEventBus: null,
      activeSchoolYear: null,
      showInstituteDropdown: false,
      showProgramDropdown: false,
    };
  },

  computed: {
    filteredFacultyCards() {
      let entries = Object.entries(this.filteredGroupedSchedule);

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        entries = entries.filter(([faculty]) =>
          faculty.toLowerCase().includes(q),
        );
      }

      const start = (this.cardPage - 1) * this.cardsPerPage;
      const end = start + this.cardsPerPage;

      return Object.fromEntries(entries.slice(start, end));
    },
    totalCardPages() {
      const entries = Object.entries(this.filteredGroupedSchedule);

      const filtered = this.searchQuery
        ? entries.filter(([faculty]) =>
            faculty.toLowerCase().includes(this.searchQuery.toLowerCase()),
          )
        : entries;

      return Math.ceil(filtered.length / this.cardsPerPage);
    },

    coursesList() {
      const store = useFetchDataStore();
      return store.courses || [];
    },

    rawusers() {
      const store = useFetchDataStore();
      return store.rawusers || [];
    },
    collegeBranches() {
      const store = useFetchDataStore();
      return store.college_branch || [];
    },
    // Total units per faculty
    facultyTotalUnits() {
      const result = {};

      Object.entries(this.filteredGroupedSchedule).forEach(
        ([faculty, schedules]) => {
          let totalUnits = 0;
          const counted = new Set();

          schedules.forEach((sched) => {
            const key = `${sched.set_name}-${sched.course_code}`;

            if (counted.has(key)) return;
            counted.add(key);

            const course = this.coursesList.find(
              (c) => c.course_code === sched.course_code,
            );

            if (!course) return;

            const lec = Number(course.course_lec || 0);
            const lab = Number(course.course_lab || 0);

            totalUnits += lec + lab * 2.25;
          });

          // Find faculty in raw users
          const user = this.rawusers.find(
            (u) =>
              `${u.first_name} ${u.last_name}`.trim().toLowerCase() ===
              faculty.trim().toLowerCase(),
          );

          result[faculty] = {
            totalUnits: Number(totalUnits.toFixed(2)),
            unitLoad: Number(user?.unit_load || 0),
          };
        },
      );

      return result;
    },
    // Map institute IDs to their names
    uniqueInstitutes() {
      const store = useFetchDataStore();
      const institutes = store.institutes || [];

      const ids = [
        ...new Set(this.schedule.map((s) => Number(s.institute_id))),
      ];

      return ids.map((id) => {
        const inst = institutes.find((i) => Number(i.institute_id) === id);

        return {
          id,
          name: inst?.institute_code || `Institute ${id}`,
        };
      });
    },

    // Map program IDs to their names (filtered by selectedInstituteId if any)
    filteredPrograms() {
      const store = useFetchDataStore();
      const programs = store.programs || [];

      let ids;

      if (!this.selectedInstituteId) {
        ids = [...new Set(this.schedule.map((s) => Number(s.program_id)))];
      } else {
        ids = [
          ...new Set(
            this.schedule
              .filter(
                (s) =>
                  Number(s.institute_id) === Number(this.selectedInstituteId),
              )
              .map((s) => Number(s.program_id)),
          ),
        ];
      }

      return ids.map((id) => {
        const prog = programs.find((p) => Number(p.program_id) === id);

        return {
          id,
          name: prog?.program_code || `Program ${id}`,
        };
      });
    },

    // Compute latest active school year dynamically
    latestActiveSchoolYear() {
      if (!this.schoolYears.length) return null;
      const activeYears = this.schoolYears.filter((y) => y.is_active);
      if (!activeYears.length) return null;
      return activeYears.reduce((latest, current) =>
        new Date(current.updated_at) > new Date(latest.updated_at)
          ? current
          : latest,
      );
    },
    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage + 1;
    },

    endIndex() {
      return Math.min(
        this.currentPage * this.itemsPerPage,
        Object.keys(this.filteredGroupedSchedule).length,
      );
    },

    totalPages() {
      return Math.ceil(
        Object.keys(this.filteredGroupedSchedule).length / this.itemsPerPage,
      );
    },

    // --------------------------
    // Updated pageNumbers for windowed pagination
    // --------------------------
    pageNumbers() {
      const halfWindow = Math.floor(this.pageWindow / 2);
      let start = Math.max(1, this.currentPage - halfWindow);
      let end = Math.min(this.totalPages, start + this.pageWindow - 1);

      start = Math.max(1, end - this.pageWindow + 1);

      const pages = [];
      for (let i = start; i <= end; i++) pages.push(i);
      return pages;
    },

    paginatedFaculty() {
      let entries = Object.entries(this.filteredGroupedSchedule);

      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        entries = entries.filter(([faculty]) =>
          faculty.toLowerCase().includes(q),
        );
      }

      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return Object.fromEntries(entries.slice(start, end));
    },
  },

  watch: {
    selectedInstituteId() {
      this.filterSchedules();
      this.selectedProgramId = "";
      this.cardPage = 1;
    },

    selectedProgramId() {
      this.filterSchedules();
      this.cardPage = 1;
    },

    // ✅ FINAL FIX
    searchQuery() {
      this.currentPage = 1;
      this.cardPage = 1;
    },
  },

  methods: {
    async loadFetchData() {
      const store = useFetchDataStore();
      await store.fetchPrograms();
      await store.fetchInstitutes();
      await store.fetchCourses();
      await store.fetchCollegeBranch();
    },
    getCollegeBranchName(branchId) {
      const branch = this.collegeBranches.find(
        (b) => Number(b.college_branch_id) === Number(branchId),
      );

      return branch ? branch.college_branch_name : `Branch ${branchId}`;
    },
    showScheduleTooltip(event, item) {
      const rect = event.currentTarget.getBoundingClientRect();

      const tooltipWidth = 260;
      const tooltipHeight = 160;
      const padding = 10;

      let x = rect.right + padding;
      let y = rect.top;

      const screenWidth = window.innerWidth;
      const screenHeight = window.innerHeight;

      // Prevent overflow right
      if (x + tooltipWidth > screenWidth) {
        x = rect.left - tooltipWidth - padding;
      }

      // Prevent overflow bottom
      if (y + tooltipHeight > screenHeight) {
        y = screenHeight - tooltipHeight - padding;
      }

      this.tooltipX = x;
      this.tooltipY = y;
      this.tooltipItem = item;
      this.scheduleTooltipVisible = true;
    },

    hideScheduleTooltip() {
      this.scheduleTooltipVisible = false;
      this.tooltipItem = null;
    },

    backToFacultyTable() {
      this.filteredGroupedSchedule = this.groupedSchedule;
      this.showFacultyTable = true;
      this.currentPage = 1;
    },
    highlightRow(item) {
      this.highlightedRecordId = item.id || item.tempId;
      // optional: scroll to the row
      this.$nextTick(() => {
        const el = document.getElementById(`row-${this.highlightedRecordId}`);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    },

    // Normalize hour to 24h format
    normalizeHour(hour) {
      const h = Number(hour);
      if (Number.isNaN(h)) return null;
      return h; // ✅ already 24-hour based
    },

    // Get all conflicting records for a given schedule item
    getConflictingRecords(record) {
      const allSchedules = this.schedule || [];
      const recordStart = this.normalizeHour(record.start_hour);
      const recordEnd = recordStart + Number(record.duration);

      return allSchedules
        .map((r) => {
          const rId = r.id?.toString() || r.tempId;
          const recId = record.id?.toString() || record.tempId;

          // Skip the same record
          if (r.faculty_id === record.faculty_id && rId === recId) return null;

          // Must be on the same day
          if (r.day !== record.day) return null;

          // Check for time overlap
          const rStart = this.normalizeHour(r.start_hour);
          const rEnd = rStart + Number(r.duration);

          if (Math.max(rStart, recordStart) >= Math.min(rEnd, recordEnd))
            return null;

          // Determine conflict reasons
          let reason = [];

          // SAME CLASS SECTION
          if (r.class_id && record.class_id && r.class_id === record.class_id) {
            reason.push("Same class section in the same Day and Time");
          }

          // SAME ROOM (Face to Face)
          if (
            (record.schedule_type || "").toLowerCase() === "face to face" &&
            (r.schedule_type || "").toLowerCase() === "face to face" &&
            r.room_id === record.room_id
          ) {
            reason.push("Same Room");
          }

          // SAME FACULTY
          if (
            r.faculty_id === record.faculty_id &&
            (r.schedule_type || "").toLowerCase() ===
              (record.schedule_type || "").toLowerCase()
          ) {
            reason.push("Same Faculty + Same schedule_type");
          }

          // ✅ ONLINE CONFLICT (same program + same section only)
          if (
            (record.room_name || "").toLowerCase() === "online" &&
            (r.room_name || "").toLowerCase() === "online" &&
            r.set_name === record.set_name &&
            r.program_id === record.program_id &&
            r.college_branch_id === record.college_branch_id &&
            r.college_branch_id === record.college_branch_id
          ) {
            reason.push(
              "ONLINE conflict: Same program section cannot attend two online classes at the same time.",
            );
          }

          if (!reason.length) return null;

          return { ...r, reason: reason.join(", ") };
        })
        .filter(Boolean);
    },

    // Check if a record has any room/faculty conflicts
    hasRoomConflict(record) {
      return this.getConflictingRecords(record).length > 0;
    },

    // Open the conflict modal for a record
    openConflictModal(record) {
      const conflicts = this.getConflictingRecords(record);

      if (!conflicts.length) return;

      this.selectedSchedule = record; // 👈 LEFT SIDE
      this.conflictRecords = conflicts; // 👉 RIGHT SIDE
      this.conflictModalVisible = true;
    },

    closeConflictModal() {
      this.conflictModalVisible = false;
      this.conflictRecords = [];
      this.selectedSchedule = null;
    },

    isStartingSlot(item, slot) {
      return item.start_hour >= slot.start && item.start_hour < slot.end;
    },
    getBlockTop(item, slotStart) {
      if (!item || item.start_hour == null) return 0;

      const start = this.normalizeHour(Number(item.start_hour));
      return (start - slotStart) * this.timeSlotHeight;
    },

    getBlockHeight(item) {
      if (!item || !item.duration) return this.timeSlotHeight;

      return Number(item.duration) * this.timeSlotHeight - 1;
    },

    checkConflicts() {
      const conflicts = [];
      const allSchedules = this.schedule;

      for (let i = 0; i < allSchedules.length; i++) {
        for (let j = i + 1; j < allSchedules.length; j++) {
          const a = allSchedules[i];
          const b = allSchedules[j];

          const sameDay = a.day === b.day;
          const sameRoom = a.room_name === b.room_name;
          const sameCourse = a.course_code === b.course_code;

          const aStart = this.normalizeHour(a.start_hour);
          const aEnd = aStart + Number(a.duration);

          const bStart = this.normalizeHour(b.start_hour);
          const bEnd = bStart + Number(b.duration);

          const overlap = aEnd > bStart && aStart < bEnd;

          if (sameDay && sameRoom && sameCourse && overlap) {
            conflicts.push({ a, b });
          }
        }
      }
      return conflicts;
    },

    formatTime(h) {
      if (h == null) return "";
      const hour = Math.floor(h); // integer hour
      const minutes = Math.round((h - hour) * 60); // decimal -> minutes
      const period = hour >= 12 ? "PM" : "AM";
      const hour12 = hour % 12 || 12;
      const minutesStr = minutes.toString().padStart(2, "0");
      return `${hour12}:${minutesStr} ${period}`;
    },

    changePage(page) {
      if (page < 1) page = 1;
      if (page > this.totalPages) page = this.totalPages;
      this.currentPage = page;
    },

    filterSchedules() {
      let filtered = { ...this.groupedSchedule };

      if (this.selectedInstituteId)
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some((s) => s.institute_id == this.selectedInstituteId),
          ),
        );

      if (this.selectedProgramId)
        filtered = Object.fromEntries(
          Object.entries(filtered).filter(([, schedules]) =>
            schedules.some((s) => s.program_id == this.selectedProgramId),
          ),
        );

      this.filteredGroupedSchedule = filtered;
      this.cardPage = 1;
      this.changePage(1);
    },
    getScheduleForCell(slot, day, instructor) {
      const schedules = this.filteredGroupedSchedule[instructor] || [];
      return schedules.filter((item) => {
        if (item.day !== day) return false;

        const start = this.normalizeHour(item.start_hour);
        const end = start + Number(item.duration);
        return end > slot.start && start < slot.end;
      });
    },

    getTypeColor(room_type) {
      if (!room_type) return "bg-green-100 border-green-400";
      const normalized = room_type.toLowerCase();
      if (normalized === "laboratory" || normalized === "lab") {
        return "bg-blue-200 border-blue-400";
      }
      return "bg-green-200 border-green-400";
    },

    viewFacultySchedule(instructor) {
      this.filteredGroupedSchedule = {
        [instructor]: this.groupedSchedule[instructor],
      };
      this.showFacultyTable = false;
    },

    async fetchUser() {
      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/auth/me`,
          {
            withCredentials: true,
          },
        );
        this.user = res.data || {};
      } catch {
        this.user = {};
      }
    },

    async fetchSchedule() {
      this.loading = true;
      this.progress = 0;
      this.progressInterval = setInterval(() => {
        if (this.progress < 90) this.progress += Math.random() * 10;
      }, 200);

      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/generated-scheduled/load`,
        );

        const data = res.data.data || {};

        const allSchedules = data.scheduled_meetings || [];
        this.unscheduledMeetings = data.unscheduled_meetings || []; // ✅ IMPORTANT

        this.schedule = allSchedules;
        this.groupedSchedule = this.groupByInstructor(this.schedule);
        this.filteredGroupedSchedule = this.groupedSchedule;
      } catch {
        this.error = "Failed to fetch schedule.";
      } finally {
        clearInterval(this.progressInterval);
        this.progress = 100;

        setTimeout(() => {
          this.loading = false;
        }, 400);
      }
    },

    //     async fetchSchedule() {
    //   this.loading = true;

    //   try {
    //     // JSON content is already available
    //     const allSchedules = sample_schedule.scheduled_meetings || [];

    //     this.schedule = allSchedules;
    //     this.groupedSchedule = this.groupByInstructor(this.schedule);
    //     this.filteredGroupedSchedule = this.groupedSchedule;
    //   } catch (err) {
    //     this.error = "Failed to load schedule.";
    //   } finally {
    //     this.loading = false;
    //   }
    // },

    groupByInstructor(schedules) {
      return schedules.reduce((acc, s) => {
        const instructor = s.faculty_name || "Unknown Faculty";
        if (!acc[instructor]) acc[instructor] = [];
        acc[instructor].push(s);
        return acc;
      }, {});
    },

    async generateSchedule() {
      const store = useFetchDataStore();

      try {
        this.loading = true;
        this.progress = 0;

        // simulate progress animation
        this.progressInterval = setInterval(() => {
          if (this.progress < 90) {
            this.progress += Math.random() * 10;
          }
        }, 200);

        // 1️⃣ Trigger scheduler (updates JSON)
        await store.runScheduler();

        // 2️⃣ Fetch generated schedule from JSON
        const data = await store.fetchGeneratedScheduled();

        this.schedule = data.scheduled_meetings || [];
        this.unscheduledMeetings = data.unscheduled_meetings || [];

        this.groupedSchedule = this.groupByInstructor(this.schedule);
        this.filteredGroupedSchedule = this.groupedSchedule;

        this.scheduleGenerated = true;
        this.showFacultyTable = false;
      } catch (err) {
        console.error(err);
        this.error = "Failed to generate schedule";
      } finally {
        this.loading = false;
      }
    },
    async fetchSchoolYears() {
      try {
        const res = await axios.get(
          process.env.VUE_APP_API_BASE_URL + "/school-year/get-school-years",
        );
        this.schoolYears = res.data.map((y) => ({ ...y }));
      } catch (err) {
        console.error("Failed to fetch school years:", err);
      }
    },

    async saveScheduledConfirmed() {
      this.savingSchedule = true;

      try {
        // Always fetch latest school years before saving
        await this.fetchSchoolYears();

        const latestSchoolYear = this.latestActiveSchoolYear;
        if (!latestSchoolYear) {
          alert("❌ No active school year found. Cannot save schedule.");
          return;
        }

        // ----------------------------------------
        // 1️⃣ SAVE SCHEDULED MEETINGS
        // ----------------------------------------
        const scheduledPayload = this.schedule.map((item) => ({
          class_id: item.class_id,
          set_name: item.set_name,
          course_code: item.course_code,
          program_id: item.program_id,
          college_branch_id: item.college_branch_id,
          program_code: item.program_code,
          institute_id: item.institute_id,
          type: item.type,
          day: item.day,
          start_hour: item.start_hour,
          duration: item.duration,
          time_slot: `${this.formatTime(item.start_hour)} - ${this.formatTime(
            item.start_hour + Number(item.duration),
          )}`,
          room_id: item.room_id,
          room_name: item.room_name,
          room_type: item.room_type,
          room_capacity: item.room_capacity,
          class_size: item.class_size,
          faculty_id: item.faculty_id,
          faculty_name: item.faculty_name,
          school_year: latestSchoolYear.school_year_name,
          semester: latestSchoolYear.semester,
          mode: item.schedule_type,
        }));

        if (scheduledPayload.length > 0) {
          const response = await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/bulk`,
            scheduledPayload,
            { withCredentials: true },
          );

          if (response.data?.exists) {
            this.overrideInfo = response.data;

            this.showConfirmSaved = false;
            this.showOverrideModal = true;

            return;
          }
        }

        // ----------------------------------------
        // 2️⃣ SAVE UNSCHEDULED MEETINGS
        // ----------------------------------------
        const unscheduledMeetings = this.unscheduledMeetings || [];

        const unscheduledPayload = unscheduledMeetings.map((item) => ({
          class_id: item.class_id,
          course_code: item.course_code,
          course_id: item.course_id,
          class_size: item.class_size,
          faculty_name: item.faculty_name,
          program_id: item.program_id,
          program_code: item.program_code,
          type: item.type,
          hours: item.hours,
          reason: item.reason,
          school_year: latestSchoolYear.school_year_name,
          semester: latestSchoolYear.semester,
        }));

        if (unscheduledPayload.length > 0) {
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/unscheduled-meetings/add-unscheduled-meetings`,
            unscheduledPayload,
            { withCredentials: true },
          );
        }

        toast.success(
          "✅ Schedule and unscheduled meetings saved successfully!",
        );
        this.showConfirmSaved = false;
      } catch (error) {
        console.error(error);

        const data = error?.response?.data;

        // NestJS BadRequestException response
        if (data?.school_year && data?.semester) {
          toast.error(
            `Schedule for School Year ${data.school_year} Semester ${data.semester} is already generated.`,
            {
              autoClose: 5000,
            },
          );
          return;
        }

        toast.error(data?.message || "Failed to save schedule.");
      } finally {
        this.savingSchedule = false;
      }
    },
    async overrideSchedule() {
      this.overridingSchedule = true;

      try {
        await this.fetchSchoolYears();

        const latestSchoolYear = this.latestActiveSchoolYear;

        // ----------------------------------------
        // Scheduled meetings payload
        // ----------------------------------------
        const scheduledPayload = this.schedule.map((item) => ({
          class_id: item.class_id,
          set_name: item.set_name,
          course_code: item.course_code,
          program_id: item.program_id,
          college_branch_id: item.college_branch_id,
          program_code: item.program_code,
          institute_id: item.institute_id,
          type: item.type,
          day: item.day,
          start_hour: item.start_hour,
          duration: item.duration,
          time_slot: `${this.formatTime(item.start_hour)} - ${this.formatTime(
            item.start_hour + Number(item.duration),
          )}`,
          room_id: item.room_id,
          room_name: item.room_name,
          room_type: item.room_type,
          room_capacity: item.room_capacity,
          class_size: item.class_size,
          faculty_id: item.faculty_id,
          faculty_name: item.faculty_name,
          school_year: latestSchoolYear.school_year_name,
          semester: latestSchoolYear.semester,
          mode: item.schedule_type,
        }));

        // ----------------------------------------
        // Unscheduled meetings payload
        // ----------------------------------------
        const unscheduledPayload = (this.unscheduledMeetings || []).map(
          (item) => ({
            class_id: item.class_id,
            course_code: item.course_code,
            course_id: item.course_id,
            class_size: item.class_size,
            faculty_name: item.faculty_name,
            program_id: item.program_id,
            program_code: item.program_code,
            type: item.type,
            hours: item.hours,
            reason: item.reason,
            school_year: latestSchoolYear.school_year_name,
            semester: latestSchoolYear.semester,
          }),
        );

        // ----------------------------------------
        // Override final schedules
        // ----------------------------------------
        await axios.post(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/bulk`,
          {
            schedules: scheduledPayload,
            override: true,
          },
          { withCredentials: true },
        );

        // ----------------------------------------
        // Override unscheduled meetings
        // ----------------------------------------
        await axios.post(
          `${process.env.VUE_APP_API_BASE_URL}/unscheduled-meetings/add-unscheduled-meetings`,
          {
            meetings: unscheduledPayload,
            override: true,
          },
          { withCredentials: true },
        );

        this.showOverrideModal = false;

        toast.success(
          "Schedule and unscheduled meetings overridden successfully!",
        );
      } catch (error) {
        console.error(error);
        toast.error("Failed to override schedule.");
      } finally {
        this.overridingSchedule = false;
      }
    },

    getCourseTitle(courseCode) {
      const course = this.coursesList.find((c) => c.course_code === courseCode);
      return course?.course_title || "";
    },

    // Excel sheet names: max 31 chars, no : \ / ? * [ ], and unique per workbook
    sanitizeSheetName(name, used) {
      let clean = String(name || "Unassigned")
        .replace(/[:\\/?*[\]]/g, "-")
        .slice(0, 31);
      if (!clean) clean = "Sheet";

      let finalName = clean;
      let suffix = 1;
      while (used.has(finalName)) {
        const base = clean.slice(0, 31 - String(suffix).length - 1);
        finalName = `${base}_${suffix}`;
        suffix++;
      }
      return finalName;
    },

    async downloadSchedule() {
      this.downloadingSchedule = true;

      try {
        const res = await axios.get(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/get-all-final-schedules`,
        );

        const records = res.data || [];

        if (!records.length) {
          toast.error(
            "No saved schedule found. Save a schedule before downloading.",
          );
          return;
        }

        // Group rows by program so each program gets its own sheet
        const byProgram = {};
        records.forEach((r) => {
          const program = r.program_code || "Unassigned";
          if (!byProgram[program]) byProgram[program] = [];
          byProgram[program].push(r);
        });

        const wb = XLSX.utils.book_new();
        const usedSheetNames = new Set();

        Object.keys(byProgram)
          .sort()
          .forEach((program) => {
            const rows = byProgram[program]
              .slice()
              .sort((a, b) =>
                (a.faculty_name || "").localeCompare(b.faculty_name || ""),
              )
              .map((r) => ({
                "Faculty Name": r.faculty_name || "Unassigned",
                "Course Code": r.course_code || "",
                "Course Title": this.getCourseTitle(r.course_code),
                Section: r.set_name || "",
                Day: r.day || "",
                Time:
                  r.time_slot ||
                  (r.start_hour != null
                    ? `${this.formatTime(r.start_hour)} - ${this.formatTime(
                        r.start_hour + Number(r.duration || 0),
                      )}`
                    : ""),
                Room: r.room_name || "",
                Mode: r.mode || "",
              }));

            const ws = XLSX.utils.json_to_sheet(rows);
            ws["!cols"] = [
              { wch: 28 },
              { wch: 14 },
              { wch: 32 },
              { wch: 12 },
              { wch: 12 },
              { wch: 20 },
              { wch: 16 },
              { wch: 14 },
            ];

            const sheetName = this.sanitizeSheetName(program, usedSheetNames);
            usedSheetNames.add(sheetName);

            XLSX.utils.book_append_sheet(wb, ws, sheetName);
          });

        const timestamp = new Date().toISOString().slice(0, 10);
        XLSX.writeFile(wb, `Faculty_Schedule_${timestamp}.xlsx`);

        toast.success("Schedule downloaded successfully!");
      } catch (error) {
        console.error(error);
        toast.error("Failed to download schedule.");
      } finally {
        this.downloadingSchedule = false;
      }
    },
  },

  async mounted() {
    const store = useFetchDataStore();

    await store.fetchInstitutes();
    await store.fetchPrograms();
    await store.fetchCollegeBranch();
    await store.fetchCourses();
    await store.fetchRawUsers();
    const data = await store.fetchGeneratedScheduled();
    if (!data) {
      this.schedule = [];
      this.unscheduledMeetings = [];
      this.groupedSchedule = {};
      this.filteredGroupedSchedule = {};
      return;
    }

    this.schedule = data.scheduled_meetings || [];
    this.unscheduledMeetings = data.unscheduled_meetings || [];

    this.groupedSchedule = this.groupByInstructor(this.schedule);
    this.filteredGroupedSchedule = this.groupedSchedule;

    this.stopEventBus = eventBus.on((newYear) => {
      console.log("EventBus Data:", newYear);

      if (!newYear) return;

      this.activeSchoolYear = newYear;
      this.currentPage = 1;
    });
  },
};
</script>
<style>
/* Fade whole loader */
.loader-fade-enter-active,
.loader-fade-leave-active {
  transition: all 0.35s ease;
}

.loader-fade-enter-from,
.loader-fade-leave-to {
  opacity: 0;
}

/* Pop upward */
@keyframes loaderUp {
  from {
    opacity: 0;
    transform: translateY(25px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.animate-loaderUp {
  animation: loaderUp 0.55s ease-out;
}

/* Floating card */
@keyframes float {
  0%,
  100% {
    transform: translateY(0px);
  }

  50% {
    transform: translateY(-6px);
  }
}

.animate-float {
  animation: float 2.2s ease-in-out infinite;
}

/* Delayed text */
@keyframes fadeDelay {
  from {
    opacity: 0;
    transform: translateY(8px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeDelay {
  animation: fadeDelay 0.7s ease-out 0.2s both;
}
/* Hide scrollbar but allow scrolling */
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

.scrollbar-hide {
  -ms-overflow-style: none; /* IE & Edge */
  scrollbar-width: none; /* Firefox */
}
</style>
