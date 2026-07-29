<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 px-2 gap-2"
  >
    <div class="flex justify-center gap-2 w-full">
      <!-- MAIN MODAL WRAPPER -->
      <div
        class="bg-white w-[60vw] h-[98vh] rounded-xl shadow-xl flex flex-col overflow-hidden"
      >
        <!-- HEADER -->

        <div class="modal-header">
          <div class="flex items-center gap-3">
            <!-- Icon -->
            <div class="glass-container">
              <icon name="circle-add2" class="text-white" />
            </div>

            <!-- Title -->
            <div>
              <h2 class="text-lg font-semibold text-white">Edit Schedules</h2>

              <p class="text-xs text-green-100">
                View, add, and update faculty schedule details
              </p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="$emit('close')"
            class="close-button-header"
          />
        </div>

        <!-- BODY -->
        <div class="flex flex-1 overflow-hidden">
          <!-- LEFT: CALENDAR AREA -->
          <div
            :class="[
              'transition-all duration-300 overflow-hidden h-full',
              panelMode ? 'w-[100%]' : 'w-full',
            ]"
          >
            <div class="flex-1 overflow-auto bg-gray-50 h-full">
              <div
                v-for="(records, instructor) in groupedSchedule"
                :key="instructor"
                class="border rounded-lg shadow-sm bg-white"
              >
                <!-- Instructor Header -->
                <div
                  class="py-3 px-4 border-b bg-gray-100 flex items-center justify-between"
                >
                  <div class="flex flex-col">
                    <div class="flex items-center gap-2">
                      <span class="text-md font-bold">{{ instructor }}</span>

                      <!-- Overload Badge -->
                      <span
                        v-if="
                          facultyTotalUnits[instructor] &&
                          Number(facultyTotalUnits[instructor].totalUnits) >
                            Number(facultyTotalUnits[instructor].unitLoad)
                        "
                        class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[11px] font-semibold bg-red-100 text-red-700 border border-red-200"
                      >
                        OVERLOAD
                      </span>
                    </div>

                    <div
                      v-if="facultyTotalUnits[instructor]"
                      class="mt-2 flex items-center gap-2 flex-wrap text-xs"
                    >
                      <!-- Unit Load -->
                      <div
                        class="px-3 py-1 rounded-full border border-blue-200 bg-white text-blue-600 font-medium"
                      >
                        Set Load: {{ facultyTotalUnits[instructor].unitLoad }}
                      </div>
                      <!-- Total Units -->
                      <div
                        class="px-3 py-1 rounded-full border font-medium"
                        :class="
                          Number(facultyTotalUnits[instructor].totalUnits) >
                          Number(facultyTotalUnits[instructor].unitLoad)
                            ? 'bg-white border-red-200 text-red-600'
                            : 'bg-white border-green-200 text-green-600'
                        "
                      >
                        Total Units:
                        {{ facultyTotalUnits[instructor].totalUnits }} Units
                      </div>

                      <!-- Status -->
                      <!-- <div
                        v-if="
                          Number(facultyTotalUnits[instructor].totalUnits) >
                          Number(facultyTotalUnits[instructor].unitLoad)
                        "
                        class="px-3 py-1 rounded-full bg-red-100 text-red-700 font-semibold"
                      >
                        <i class="mdi mdi-alert-circle mr-1"></i>
                        OVERLOAD
                      </div> -->
                    </div>
                  </div>
                  <div class="flex gap-1 items-center">
                    <div
                      class="flex items-center gap-4 py-2 px-3 ml-2 rounded-full border w-max bg-gray-50 text-xs"
                    >
                      <span class="font-medium text-gray-700"
                        >Join Scheduled:</span
                      >

                      <div class="per-page-container">
                        <span
                          class="font-semibold"
                          :class="isJoined ? 'text-green-600' : 'text-gray-400'"
                        >
                          {{ isJoined ? "YES" : "NOT" }}
                        </span>

                        <button
                          @click="toggleJoin"
                          :class="[
                            'w-12 h-6 rounded-full p-1 flex items-center transition-colors duration-300 focus:outline-none',
                            isJoined ? 'bg-green-500' : 'bg-gray-300',
                          ]"
                        >
                          <span
                            class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-300"
                            :class="
                              isJoined ? 'translate-x-6' : 'translate-x-0'
                            "
                          ></span>
                        </button>
                      </div>
                    </div>
                    <button
                      @click="openUnscheduledPanel(instructor)"
                      class="btn-save"
                    >
                      Unscheduled
                    </button>

                    <button
                      @click="openAddSchedulePanel(instructor)"
                      class="btn-save"
                    >
                      Add
                    </button>
                  </div>
                </div>

                <!-- TABLE -->
                <div class="">
                  <table
                    class="w-full table-auto border-separate border-spacing-0 text-[11px]"
                  >
                    <thead class="bg-gray-200 sticky top-0 z-10">
                      <tr>
                        <th class="px-3 py-3 border text-center w-24">Time</th>
                        <th
                          v-for="day in days"
                          :key="day"
                          class="px-3 py-2 border text-center w-28"
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
                        :style="{ height: timeSlotHeight + 'px' }"
                      >
                        <!-- Time Column -->
                        <td
                          class="px-2 py-5 border text-center text-[12px] w-auto whitespace-nowrap text-gray-700"
                        >
                          {{ formatTime(slot.start) }} -
                          {{ formatTime(slot.end) }}
                        </td>

                        <!-- Days Columns -->
                        <td
                          v-for="day in days"
                          :key="day"
                          class="relative border p-0 overflow-visible transition-colors"
                          :class="{
                            'bg-red-100':
                              draggedRecord &&
                              dragConflictMap[
                                `${instructor}-${day}-${slot.start}`
                              ],
                          }"
                          :style="{ height: timeSlotHeight + 'px' }"
                          @dragover.prevent
                          @drop="onDrop($event, instructor, day, slot.start)"
                        >
                          <template
                            v-for="item in getScheduleForCell(
                              slot,
                              day,
                              instructor,
                            )"
                            :key="item.id || item.tempId"
                          >
                            <div
                              v-if="isStartingSlot(item, slot)"
                              :draggable="
                                canEditSchedule(item) &&
                                !(isJoined && Number(item.class_size) >= 30)
                              "
                              @mouseenter.passive="
                                showScheduleTooltip($event, item)
                              "
                              @mouseleave="hideScheduleTooltip"
                              @dragstart="onDragStart($event, item)"
                              @dragend="onDragEnd"
                              @dblclick="attemptUnjoin(item)"
                              @click="highlightRow(item)"
                              :class="[
                                'absolute border rounded-lg text-[11px] p-1 shadow-sm truncate transition overflow-hidden',

                                // temp schedule
                                item.id?.toString().startsWith('temp-')
                                  ? 'bg-purple-200 border-purple-400 text-purple-900'
                                  : // cannot edit → gray disabled style
                                  !canEditSchedule(item)
                                  ? 'bg-gray-200 border-gray-300 text-gray-500 opacity-80 cursor-not-allowed'
                                  : // normal schedule color
                                    getTypeColor(item.type),

                                // room conflict
                                hasRoomConflict(item)
                                  ? 'bg-red-300 border-red-500 text-red-900'
                                  : '',

                                // joined schedule
                                item.is_joined
                                  ? 'bg-blue-100 border-blue-400'
                                  : '',

                                // joined disabled
                                isJoined && Number(item.class_size) >= 30
                                  ? 'opacity-50 pointer-events-none cursor-not-allowed'
                                  : '',

                                // hover only if editable
                                canEditSchedule(item)
                                  ? 'cursor-pointer hover:bg-yellow-100'
                                  : '',
                                draggedRecord?.id === item.id
                                  ? 'schedule-dragging'
                                  : '',
                              ]"
                              :style="{
                                top: getBlockTop(item, slot.start) + 'px',
                                left: '50%',
                                transform: 'translateX(-50%)',
                                width: 'calc(100% - 12px)',
                                height: getBlockHeight(item) + 'px',
                                zIndex: 1,
                              }"
                            >
                              <!-- Mode Badge -->
                              <span
                                v-if="item.mode"
                                :class="[
                                  'absolute top-2 right-2 w-auto h-4 px-1 rounded-full text-[10px] font-bold flex items-center justify-center text-white',
                                  item.mode === 'face to face'
                                    ? 'bg-orange-500'
                                    : '',
                                  item.mode === 'online' ? 'bg-purple-500' : '',
                                ]"
                              >
                                {{
                                  item.mode === "face to face" ? "F2F" : "OL"
                                }}
                              </span>
                              <span
                                v-if="item.is_joined"
                                class="absolute bottom-2 right-2 px-2 h-5 flex items-center justify-center bg-blue-600 text-white text-[10px] font-bold rounded-full shadow"
                              >
                                J
                              </span>
                              <div class="truncate font-semibold">
                                {{ item.course_code }}
                              </div>
                              <div class="truncate">{{ item.room_name }}</div>

                              <div class="truncate">
                                {{
                                  item.classInfo?.program?.program_code ||
                                  item.program_code
                                }}
                                -
                                {{ item.set_name }}
                              </div>

                              <div class="w-full flex justify-center">
                                <button
                                  v-if="hasRoomConflict(item)"
                                  @click.stop="openConflictModal(item)"
                                  class="absolute bottom-1 right-1 flex items-center justify-center w-4 h-4 rounded-md bg-red-600 text-white text-[9px] font-bold shadow hover:bg-red-700"
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
              </div>
              <!-- instructor loop -->
            </div>
          </div>
        </div>

        <!-- FOOTER -->
        <div
          class="flex justify-end gap-2 p-4 bg-white border-t shadow-md text-xs"
        >
          <button @click="cancelEdit" class="btn-cancel">Cancel</button>

          <button
            @click="saveEdit"
            class="btn-save"
            :disabled="saving || !isValid"
          >
            {{ saving ? "Saving..." : "Save" }}
          </button>
        </div>
      </div>
      <!-- RIGHT: SLIDING ADD PANEL -->
      <div
        v-if="showAddPanel || showUnscheduledPanel"
        class="w-[45vw] h-[98vh] flex flex-col gap-2"
      >
        <div
          v-if="showAddPanel"
          :class="[
            'w-[45vw] bg-white border shadow-xl transition-all duration-300 flex justify-start rounded-xl',
            showUnscheduledPanel ? 'h-[50vh]' : 'h-full',
          ]"
        >
          <div class="p-0.5 flex flex-col">
            <!-- Table Wrapper for Scroll -->
            <div class="overflow-y-auto h-full border-t rounded-t-xl">
              <table class="min-w-full divide-y divide-gray-200 text-xs">
                <!-- Table Head -->
                <thead class="bg-gray-100 sticky top-0 z-20">
                  <tr>
                    <th class="px-4 py-3 border w-[13%]">Section</th>
                    <th class="px-4 py-3 border w-[10%]">Course</th>
                    <th class="px-4 py-3 border w-[5%]">Campus</th>
                    <th class="px-4 py-3 border w-[13%]">Room</th>
                    <th class="px-4 py-3 border w-[13%]">Day</th>
                    <th class="px-4 py-3 border w-[7%]">Start</th>
                    <th class="px-4 py-3 border w-[7%]">Hours</th>
                    <th class="px-4 py-3 border w-[5%]">Set-up</th>

                    <th class="px-4 py-3 border text-center w-[2%]">Action</th>
                  </tr>
                </thead>

                <!-- Table Body -->
                <tbody>
                  <tr
                    v-for="record in sortedLocalData"
                    :key="record.id || record.tempId"
                    :id="'row-' + (record.id || record.tempId)"
                    :class="[
                      'hover:bg-green-200 relative',
                      highlightedRecordId === (record.id || record.tempId)
                        ? 'bg-blue-100'
                        : '',
                      record.join_group_id
                        ? 'border-l-4 ' + getJoinColor(record.join_group_id)
                        : '',
                    ]"
                  >
                    <!-- Section Input -->
                    <td class="px-2 py-2 border relative">
                      <input
                        v-model="record.searchSectionQuery"
                        :disabled="!canEditSchedule(record)"
                        type="text"
                        placeholder="Select section..."
                        class="px-3 py-2 w-full rounded-md text-xs"
                        @focus="record.showSectionDropdown = true"
                        @input="record.class_id = null"
                      />
                      <div
                        v-if="
                          record.showSectionDropdown &&
                          filteredSections(record).length
                        "
                        class="absolute z-10 w-[8vw] bg-white border rounded-md max-h-40 overflow-y-auto mt-1"
                        @mouseleave="record.showSectionDropdown = false"
                      >
                        <div
                          v-for="section in filteredSections(record)"
                          :key="section.class_id"
                          class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                          @mousedown.prevent="selectSection(record, section)"
                        >
                          {{ section?.program?.program_code }} -
                          {{ section.set_name }}
                        </div>
                      </div>
                    </td>

                    <!-- Course Input -->
                    <td class="px-2 py-2 border relative">
                      <input
                        v-model="record.searchCourseQuery"
                        :disabled="!canEditSchedule(record)"
                        type="text"
                        placeholder="Select course..."
                        class="px-3 py-2 w-full rounded-md text-xs"
                        @focus="record.showCourseDropdown = true"
                        @input="record.course_id = null"
                      />
                      <div
                        @mouseleave="record.showCourseDropdown = false"
                        v-if="
                          record.showCourseDropdown &&
                          filteredCourses(record).length
                        "
                        class="absolute z-10 w-full bg-white border rounded-md max-h-40 overflow-y-auto mt-1"
                      >
                        <div
                          v-for="item in filteredCourses(record)"
                          :key="item.curriculum_course_id"
                          class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                          @mousedown="selectCourse(record, item)"
                        >
                          {{ item.course?.course_code }}
                        </div>
                      </div>
                    </td>

                    <!-- Campus -->
                    <td class="px-2 py-2 border relative">
                      <select
                        v-model.number="record.college_branch_id"
                        :disabled="!canEditSchedule(record)"
                        class="w-full rounded px-2 py-2 text-xs"
                        @change="onCampusChange(record)"
                      >
                        <option :value="null" disabled>Select Campus</option>

                        <option
                          v-for="campus in availableCampuses()"
                          :key="campus.college_branch_id"
                          :value="campus.college_branch_id"
                        >
                          {{ campus.college_branch_name }}
                        </option>
                      </select>
                    </td>

                    <!-- Room Input -->
                    <td class="px-2 py-2 border relative">
                      <input
                        v-model="record.searchRoomQuery"
                        :disabled="!canEditSchedule(record)"
                        type="text"
                        placeholder="Select room..."
                        class="px-3 py-2 w-full rounded-md text-xs"
                        @focus="record.showRoomDropdown = true"
                        @input="record.room_id = null"
                      />
                      <div
                        @mouseleave="record.showRoomDropdown = false"
                        v-if="
                          record.showRoomDropdown &&
                          filteredRooms(record).length
                        "
                        class="absolute z-10 w-full bg-white border rounded-md max-h-40 overflow-y-auto mt-1"
                      >
                        <div
                          v-for="room in filteredRooms(record)"
                          :key="room.room_id"
                          class="px-3 py-2 hover:bg-gray-100 cursor-pointer"
                          @mousedown="selectRoom(record, room)"
                        >
                          {{ room.room_name }}
                        </div>
                      </div>
                    </td>

                    <!-- Day -->
                    <td class="px-2 py-2 border">
                      <input
                        v-model="record.day"
                        :disabled="!canEditSchedule(record)"
                        class="w-full px-3 py-2 boder rounded-md text-center text-xs"
                      />
                    </td>

                    <!-- Start Hour -->
                    <td class="px-2 py-2 border text-center">
                      <input
                        v-model.number="record.start_hour"
                        :disabled="!canEditSchedule(record)"
                        type="number"
                        step="0.5"
                        min="8"
                        max="20"
                        class="w-full px-3 py-2 boder rounded-md text-center text-xs"
                      />
                    </td>

                    <!-- Duration -->
                    <td class="px-2 py-2 border text-center">
                      <input
                        v-model.number="record.duration"
                        :disabled="!canEditSchedule(record)"
                        type="number"
                        class="w-full px-3 py-2 boder rounded-md text-center text-xs"
                      />
                    </td>

                    <!-- Mode -->
                    <td class="px-2 py-2 border">
                      <select
                        v-model="record.mode"
                        :disabled="!canEditSchedule(record)"
                        @change="onModeChange(record)"
                        class="w-full rounded px-2 py-1 text-xs"
                      >
                        <option value="" disabled selected>Select mode</option>
                        <option value="face to face">F2F</option>
                        <option value="online">OL</option>
                      </select>
                    </td>

                    <!-- Action -->
                    <td class="px-2 py-3 border text-center">
                      <button
                        @click="toggleDelete(record)"
                        :disabled="!canEditSchedule(record)"
                        class="hover:text-red-900"
                      >
                        <icon name="delete" />
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Footer Buttons -->
            <div class="flex justify-end gap-2 p-3 text-xs border-t">
              <button @click="addNewRow" class="btn-save">
                <!-- <icon name="circle-add1" /> -->
                Add Row
              </button>
              <button @click="cancelNewRow" class="btn-cancel">Clear</button>
            </div>
          </div>
        </div>
        <div
          v-if="showUnscheduledPanel"
          class="relative z-[9999] w-[45vw] h-[50vh] overflow-hidden bg-white rounded-xl"
        >
          <unscheduled
            :close-add-schedule-panel="closeAddSchedulePanel"
            @open-edit-schedule="addUnscheduledToCalendar"
          />
        </div>
      </div>
    </div>
    <div
      v-if="conflictModalVisible"
      class="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-[2px] px-4"
    >
      <!-- Modal -->
      <div
        class="w-full max-w-5xl overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-[0_12px_40px_rgba(15,23,42,0.12)]"
      >
        <!-- Header -->
        <!-- <div
          class="flex items-center justify-between border-b border-slate-200 px-5 py-4"
        >
          <div class="flex items-center gap-3">
            <div
              class="flex h-10 w-10 items-center justify-center rounded-xl border border-red-100 bg-red-50 text-red-600"
            >
              <icon name="exclamation-circle" class="h-5 w-5" />
            </div>

            <div>
              <h3
                class="text-[16px] font-semibold tracking-tight text-slate-900"
              >
                Schedule Conflicts
              </h3>

              <p class="mt-0.5 text-[12px] font-medium text-slate-500">
                Existing schedules overlap with the selected time slot.
              </p>
            </div>
          </div>

          <button
            @click="closeConflictModal"
            class="flex h-8 w-8 items-center justify-center rounded-lg border border-slate-200 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
          >
            ✕
          </button>
        </div> -->
        <div class="modal-header">
          <div class="flex items-center gap-3">
            <!-- Icon -->
            <div class="glass-container">
              <icon name="exclamation-circle" class="text-white" />
            </div>

            <!-- Title -->
            <div>
              <h2 class="text-lg font-semibold text-white">
                Schedule Conflicts
              </h2>

              <p class="text-xs text-green-100">
                Existing schedules overlap with the selected time slot.
              </p>
            </div>
          </div>

          <icon
            :name="'circle-close3'"
            @click="closeConflictModal"
            class="close-button-header"
          />
        </div>

        <!-- Body -->
        <div class="grid grid-cols-1 gap-5 bg-slate-50/40 p-5 xl:grid-cols-2">
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
                    selectedSchedule.mode === 'face to face',

                  'border border-violet-200 bg-violet-50 text-violet-700':
                    selectedSchedule.mode === 'online',
                }"
              >
                {{
                  selectedSchedule.mode === "face to face"
                    ? "Face to Face"
                    : "Online"
                }}
              </div>
            </div>

            <!-- Course -->
            <div class="mb-5">
              <h2
                class="text-[20px] font-semibold tracking-tight text-slate-900"
              >
                {{ selectedSchedule.course_code || "No Course" }}
              </h2>

              <p class="mt-1 text-[13px] text-slate-500">
                {{ selectedSchedule.program_code || "-" }} -
                {{ selectedSchedule.set_name || "-" }}
              </p>
            </div>

            <!-- Details -->
            <div class="grid grid-cols-2 gap-3">
              <div
                class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5"
              >
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Faculty
                </p>

                <p class="mt-1 text-[13px] font-medium text-slate-800">
                  {{ selectedSchedule.faculty_name || "-" }}
                </p>
              </div>

              <div
                class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5"
              >
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Room
                </p>

                <p class="mt-1 text-[13px] font-medium text-slate-800">
                  {{ selectedSchedule.room_name || "-" }}
                </p>
              </div>

              <div
                class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5"
              >
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Room Type
                </p>

                <p class="mt-1 text-[13px] font-medium text-slate-800">
                  {{ selectedSchedule.room_type || "-" }}
                </p>
              </div>

              <div
                class="rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5"
              >
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Day
                </p>

                <p class="mt-1 text-[13px] font-medium text-slate-800">
                  {{ selectedSchedule.day || "-" }}
                </p>
              </div>

              <div
                class="col-span-2 rounded-lg border border-slate-200 bg-slate-50 px-3 py-2.5"
              >
                <p
                  class="text-[10px] font-semibold uppercase tracking-wide text-slate-400"
                >
                  Time Schedule
                </p>

                <p class="mt-1 text-[14px] font-semibold text-slate-900">
                  {{ formatTime(selectedSchedule.time_start) }}
                  —
                  {{ formatTime(selectedSchedule.time_end) }}
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
                {{ conflictRecords.length }} conflict(s)
              </div>
            </div>

            <div class="max-h-[480px] space-y-3 overflow-y-auto pr-1">
              <div
                v-for="conflict in conflictRecords"
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
          class="flex items-center justify-end border-t border-slate-200 bg-white px-5 py-4"
        >
          <button @click="closeConflictModal" class="btn-cancel">Close</button>
        </div>
      </div>
    </div>

    <!-- TODO CONFIRM DELETE MODAL -->
    <div
      v-if="showConfirmDelete"
      class="fixed inset-0 flex items-center justify-center bg-black/30 z-50"
    >
      <div class="bg-white rounded-2xl shadow-2xl p-6 w-96">
        <!-- TODO  Header -->
        <div class="flex justify-between items-center border-b pb-3 mb-4">
          <div class="flex gap-1 items-center">
            <icon
              name="exclamation-circle"
              class="text-red-900 w-7 p-1 rounded-full bg-red-200"
            />
            <h3 class="text-lg font-semibold text-gray-800">Confirm Delete</h3>
          </div>

          <button
            @click="$emit('close')"
            class="text-gray-400 hover:text-gray-600 transition"
          >
            ✕
          </button>
        </div>

        <!-- TODO  Message -->
        <p class="text-gray-600 mb-6">
          Are you sure you want to delete this schedule?
          <strong>This action cannot be undone!</strong>
        </p>

        <!-- TODO  Buttons -->
        <div class="flex justify-center gap-2 text-xs">
          <button @click="cancelDelete" class="btn-cancel">Cancel</button>
          <button @click="confirmDelete" class="btn-cancel-confirm">
            Yes, Delete
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- Schedule Tooltip -->
  <div
    v-if="scheduleTooltipVisible && tooltipItem && !draggedRecord"
    class="fixed z-[9999] pointer-events-none"
    :style="{ top: tooltipY + 'px', left: tooltipX + 'px' }"
  >
    <div
      class="w-[280px] overflow-hidden rounded-xl border border-gray-200 bg-white"
    >
      <!-- Header -->
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
            v-if="tooltipItem.mode"
            class="shrink-0 inline-flex items-center rounded-full px-2.5 py-1 text-[9px] font-semibold text-white shadow-sm"
            :class="
              tooltipItem.mode === 'face to face'
                ? 'bg-orange-500'
                : 'bg-purple-500'
            "
          >
            {{
              tooltipItem.mode === "face to face" ? "Face to Face" : "Online"
            }}
          </span>
        </div>
      </div>

      <!-- Body -->
      <div class="px-4 py-3">
        <div class="space-y-3 text-[11px] text-gray-700">
          <!-- Faculty -->
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

          <!-- Year and Section -->
          <div>
            <p
              class="text-[9px] font-semibold uppercase tracking-wide text-gray-400"
            >
              Year & Section
            </p>

            <div class="mt-1 space-y-1">
              <template
                v-if="tooltipItem.is_joined && tooltipItem.join_group_id"
              >
                <div
                  v-for="s in finalSchedules.filter(
                    (s) => s.join_group_id === tooltipItem.join_group_id,
                  )"
                  :key="s.class_id"
                  class="rounded-lg border border-gray-100 bg-gray-50 px-2.5 py-1.5"
                >
                  <p class="font-semibold text-gray-800">
                    {{ s.display_program_code }} -
                    {{ s.set_name }}
                  </p>
                  <p class="text-[10px] text-gray-500">
                    Class Size: {{ s.class_size }}
                  </p>
                </div>
              </template>

              <template v-else>
                <div
                  class="rounded-lg border border-gray-100 bg-gray-50 px-2.5 py-1.5"
                >
                  <!-- <p class="font-semibold text-gray-800">
                              {{ tooltipItem.display_institute_name }}
                            </p>

                            <p class="text-[10px] text-gray-600">
                              {{ tooltipItem.display_program_name }}
                              ({{ tooltipItem.display_program_code }})
                            </p> -->

                  <p class="font-semibold text-gray-800">
                    {{ tooltipItem.display_program_code }}-{{
                      tooltipItem.set_name
                    }}
                  </p>
                  <p class="text-[10px] text-gray-500">
                    Class Size: {{ tooltipItem.class_size }}
                  </p>
                </div>
              </template>
            </div>
          </div>

          <!-- Details Grid -->
          <div class="grid grid-cols-2 gap-2">
            <div class="rounded-lg bg-gray-50 px-2.5 py-2">
              <p class="text-[9px] font-semibold uppercase text-gray-400">
                Room
              </p>
              <p class="mt-0.5 font-semibold text-gray-800">
                {{ tooltipItem.room_name || "TBA" }}
              </p>
            </div>

            <div class="rounded-lg bg-gray-50 px-2.5 py-2">
              <p class="text-[9px] font-semibold uppercase text-gray-400">
                Day
              </p>
              <p class="mt-0.5 font-semibold text-gray-800">
                {{ tooltipItem.day || "-" }}
              </p>
            </div>

            <div class="rounded-lg bg-gray-50 px-2.5 py-2 col-span-2">
              <p class="text-[9px] font-semibold uppercase text-gray-400">
                Time
              </p>
              <p class="mt-0.5 font-semibold text-gray-800">
                {{ formatTime(tooltipItem.start_hour) }} –
                {{
                  formatTime(
                    tooltipItem.start_hour + Number(tooltipItem.duration),
                  )
                }}
              </p>
            </div>

            <div class="rounded-lg bg-gray-50 px-2.5 py-2">
              <p class="text-[9px] font-semibold uppercase text-gray-400">
                Type
              </p>
              <p class="mt-0.5 font-semibold text-gray-800">
                {{ tooltipItem.type || "-" }}
              </p>
            </div>

            <div class="rounded-lg bg-gray-50 px-2.5 py-2">
              <p class="text-[9px] font-semibold uppercase text-gray-400">
                Campus
              </p>
              <p class="mt-0.5 font-semibold text-gray-800 truncate">
                {{ getCollegeBranchName(tooltipItem.college_branch_id) }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Unjoin Confirmation Modal -->
  <UnjoinModal
    :visible="unjoinModalVisible"
    @confirm="confirmUnjoin"
    @close="cancelUnjoin"
  />

  <editJoinValdiation
    :visible="joinValidationModalVisible"
    :baseRecord="pendingJoinRecord"
    :targets="pendingJoinTargets"
    @close="cancelJoin"
    @confirm="confirmJoin"
  />
</template>

<script>
import axios from "axios";
import { toast } from "vue3-toastify";
import { useFetchDataStore } from "@/store/fetch-data-store";
import { mapState, mapActions } from "pinia";
import icon from "@/assets/icon.vue";
import editJoinValdiation from "../faculty-components/edit-join-valdiation.vue";
import unscheduled from "../faculty-components/unscheduled.vue";
import UnjoinModal from "../faculty-components/unjoin-validation-modal.vue";
export default {
  components: { icon, editJoinValdiation, unscheduled, UnjoinModal },
  props: {
    show: Boolean,
    instructorData: { type: Array, default: () => [] },
    activeSchoolYear: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      user: {},
      localData: [],
      saving: false,
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
      selectedSchedule: {},
      draggedRecord: null,
      hourHeight: 60,
      fullSchedules: [],
      conflictModalVisible: false,
      conflictRecords: [],

      showConfirmDelete: false,
      deleteTarget: null,
      deleting: false,

      showAddSchedulePanel: false,
      selectedInstructorName: "",
      showAddPanel: false,
      showUnscheduledPanel: false,
      deletedIds: new Set(),
      highlightedRecordId: null,
      isJoined: false,
      joinValidationModalVisible: false,
      pendingJoinRecord: null,
      pendingJoinTargets: [],

      draggedGroup: [],
      scheduleTooltipVisible: false,
      tooltipItem: null,
      tooltipX: 0,
      tooltipY: 0,
      unjoinModalVisible: false,
      unjoinTarget: null,

      timeSlotHeight: 60,

      dragConflictMap: {},
      isDragging: false,
      conflictMapCache: {},

      panelMode: null,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, ["rooms", "curriculum_courses", "rawusers"]),

    conflictMap() {
      const map = {};

      this.localData.forEach((record) => {
        const key = record.id || record.tempId;

        map[key] = this.getConflictingRecords(record);
      });

      return map;
    },
    scheduleGrid() {
      const grid = {};

      this.localData.forEach((r) => {
        const key = `${r.faculty_name}-${r.day}`;

        if (!grid[key]) {
          grid[key] = [];
        }

        grid[key].push(r);
      });

      return grid;
    },
    canEditSchedule() {
      return (item) => {
        // ✅ Newly added rows always editable
        if (item.isNew) return true;

        // ✅ Program Chairperson
        // ONLY own program editable
        if (this.user.role === "Program Chairperson") {
          return (
            Number(item.institute_id) === Number(this.user.institute_id) &&
            Number(item.program_id) === Number(this.user.program_id)
          );
        }

        // ✅ Department Chairperson
        // EVERYTHING editable EXCEPT own exact program
        if (this.user.role === "Department Chairperson") {
          return !(
            Number(item.institute_id) === Number(this.user.institute_id) &&
            Number(item.program_id) === Number(this.user.program_id)
          );
        }

        return true;
      };
    },
    isDraggable(record) {
      // If Join is active and class size >= 30 → not draggable
      return !(this.isJoined && Number(record.class_size) >= 30);
    },
    sortedLocalData() {
      const dayOrder = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
      ];

      return [...this.localData].sort((a, b) => {
        const dayA = dayOrder.indexOf(a.day);
        const dayB = dayOrder.indexOf(b.day);

        // Unknown days go last
        if (dayA === -1 && dayB === -1) return 0;
        if (dayA === -1) return 1;
        if (dayB === -1) return -1;

        // Sort by day first
        if (dayA !== dayB) return dayA - dayB;

        // Then sort by start time
        return (a.start_hour ?? 0) - (b.start_hour ?? 0);
      });
    },

    coursesList() {
      const store = useFetchDataStore();

      return (store.curriculum_courses || [])
        .map((cc) => ({
          ...cc.course,
          curriculum: cc.curriculum,
          program_id: cc.curriculum?.program_id,
          institute_id: cc.curriculum?.institute_id,
          program_code: cc.curriculum?.program?.program_code,
        }))
        .filter(Boolean);
    }, // Total units per faculty
    facultyTotalUnits() {
      const result = {};

      Object.entries(this.groupedSchedule).forEach(([faculty, schedules]) => {
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
          let compute = 0;
          compute = lab * 2.25;
          totalUnits += lec + compute;
        });

        // Match faculty from raw users
        const user = this.rawusers.find(
          (u) => `${u.first_name} ${u.last_name}`.trim() === faculty.trim(),
          // Better:
          // u.id === schedules[0]?.faculty_id
        );

        result[faculty] = {
          totalUnits: Number(totalUnits.toFixed(2)),
          unitLoad: Number(user?.unit_load || 0),
        };
      });

      return result;
    },

    unscheduledCourses() {
      const scheduledCourseIds = new Set(
        this.localData.map((r) => r.course_id).filter(Boolean),
      );

      const fetchDataStore = useFetchDataStore();

      let courses = fetchDataStore.courses.filter(
        (c) => !scheduledCourseIds.has(c.course_id),
      );

      // Only show courses matching user's institute & program if Program Chairperson
      if (this.user.role === "Program Chairperson") {
        courses = courses.filter(
          (c) =>
            c.institute_id === this.user.institute_id &&
            c.program_id === this.user.program_id,
        );
      }

      return courses;
    },
    groupedSchedule() {
      const groups = {};
      this.localData.forEach((rec) => {
        if (!rec.faculty_name) return; // skip rows without instructor
        if (!groups[rec.faculty_name]) groups[rec.faculty_name] = [];
        groups[rec.faculty_name].push(rec);
      });
      return groups;
    },

    allData() {
      const merged = [...this.localData];

      const localKeys = new Set(this.localData.map((r) => r.id || r.tempId));

      (this.fullSchedules || []).forEach((r) => {
        const key = r.id || r.tempId;
        if (!localKeys.has(key)) {
          merged.push({
            ...r,
            searchRoomQuery: r.room_name || "",
            showRoomDropdown: false,
            searchCourseQuery: r.course_code || "",
            showCourseDropdown: false,
            searchSectionQuery: r.set_name || "",
            showSectionDropdown: false,
          });
        }
      });

      return merged;
    },
  },
  watch: {
    // Watch for changes in instructorData to update localData
    instructorData: {
      immediate: true,
      handler(newVal) {
        const fetchDataStore = useFetchDataStore();
        const sections = fetchDataStore.sections || [];

        // Create fresh reactive copy
        this.localData = (newVal || []).map((rec) => {
          const class_size =
            rec.class_size ||
            (rec.class_id
              ? sections.find((s) => s.class_id === rec.class_id)?.class_size
              : null);

          return {
            ...rec,
            class_size,
            searchRoomQuery: rec.room_name || "",
            showRoomDropdown: false,
            searchCourseQuery: rec.course_code || "",
            showCourseDropdown: false,
            searchSectionQuery: rec.set_name || "",
            showSectionDropdown: false,
            program_id:
              rec.class_program_id ||
              rec.program_id ||
              this.user.program_id ||
              null,

            institute_id:
              rec.class_institute_id ||
              rec.institute_id ||
              this.user.institute_id ||
              null,
          };
        });

        // Reset drag state to prevent false conflicts
        this.draggedRecord = null;
      },
    },

    // Watch for modal open (show = true) to refresh all data
    show: {
      immediate: false,
      async handler(isVisible) {
        if (isVisible) {
          this.refreshInstructorData([...this.instructorData]);

          await this.loadData(); // ADD THIS
        }
      },
    },
  },

  methods: {
    ...mapActions(useFetchDataStore, [
      "fetchRooms",
      "fetchCurriculumCourses",
      "fetchClassSections",
      "fetchRawUsers",
    ]),
    async cancelEdit() {
      try {
        const addedSchedules = this.localData.filter((r) => r.isNew);

        if (addedSchedules.length) {
          // Merge Lecture and Laboratory
          const grouped = {};

          addedSchedules.forEach((r) => {
            const key = `${r.class_id}-${r.course_code}`;

            if (!grouped[key]) {
              grouped[key] = {
                class_id: r.class_id,
                course_code: r.course_code,
                program_id: r.program_id,
                program_code: r.program_code,
                school_year: r.school_year,
                semester: r.semester,
                reason: "Faculty time conflict",
                lecture: 0,
                laboratory: 0,
              };
            }

            if (r.type === "Lecture") {
              grouped[key].lecture = Number(r.duration || 0);
            }

            if (r.type === "Laboratory") {
              grouped[key].laboratory = Number(r.duration || 0);
            }
          });

          const payload = Object.values(grouped).map((g) => {
            let type = "";
            let hours = "";

            if (g.lecture && g.laboratory) {
              type = "Lecture+Lab";
              hours = `${g.lecture.toFixed(1)}h lec + ${g.laboratory.toFixed(
                1,
              )}h lab per week`;
            } else if (g.lecture) {
              type = "Lecture";
              hours = `${g.lecture.toFixed(1)}h lec per week`;
            } else {
              type = "Laboratory";
              hours = `${g.laboratory.toFixed(1)}h lab per week`;
            }

            return {
              class_id: g.class_id,
              course_code: g.course_code,
              program_id: g.program_id,
              program_code: g.program_code,
              type,
              hours,
              reason: g.reason,
              school_year: g.school_year,
              semester: g.semester,
            };
          });

          // Save merged records to unscheduled
          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/unscheduled-meetings/add-unscheduled-meetings`,
            payload,
          );

          // Delete added schedules from final schedule
          await Promise.all(
            addedSchedules
              .filter((r) => r.id)
              .map((r) =>
                axios.delete(
                  `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${r.id}`,
                ),
              ),
          );
        }

        this.$emit("close");
      } catch (err) {
        console.error(err);
        toast.error("Failed to cancel changes.");
      }
    },
    getAllSchedulesForConflict(record) {
      return [
        ...this.fullSchedules,
        ...this.localData.filter(
          (r) => !this.fullSchedules.some((f) => Number(f.id) === Number(r.id)),
        ),
      ].filter(
        (s) =>
          String(s.school_year).trim() === String(record.school_year).trim() &&
          Number(s.semester) === Number(record.semester),
      );
    },
    async fetchCollegeBranch() {
      const store = useFetchDataStore();
      await store.fetchCollegeBranch();

      this.collegeBranches = store.collegeBranches || [];
    },
    getCollegeBranchName(branchId) {
      const branch = this.collegeBranches.find(
        (b) => Number(b.college_branch_id) === Number(branchId),
      );

      return branch ? branch.college_branch_name : `Branch ${branchId}`;
    },
    onCampusChange(record) {
      const selectedCampus = this.availableCampuses().find(
        (campus) =>
          Number(campus.college_branch_id) === Number(record.college_branch_id),
      );

      record.college_branch_name = selectedCampus?.college_branch_name || "";

      record.room_id = null;
      record.room_name = "";
      record.room_type = "";
      record.room_capacity = "";
      record.searchRoomQuery = "";
    },

    availableCampuses() {
      const map = new Map();

      (this.rooms || []).forEach((room) => {
        const campus = room.building?.buildingArea?.collegeBranch;
        if (!campus?.college_branch_id) return;

        map.set(Number(campus.college_branch_id), {
          college_branch_id: Number(campus.college_branch_id),
          college_branch_name: campus.college_branch_name,
        });
      });

      return Array.from(map.values());
    },
    generateTimeSlot(startHour, duration) {
      if (startHour == null || duration == null) return null;

      const format = (h) => {
        const hour = Math.floor(h);
        const minutes = Math.round((h - hour) * 60);
        const period = hour >= 12 ? "PM" : "AM";
        const hour12 = hour % 12 || 12;
        const minutesStr = minutes.toString().padStart(2, "0");
        return `${hour12}:${minutesStr} ${period}`;
      };

      const endHour = Number(startHour) + Number(duration);

      return `${format(startHour)} - ${format(endHour)}`;
    },
    addUnscheduledToCalendar(courses) {
      console.log("Payload sent by the child:", courses);

      courses.forEach((course) => {
        const tempId = `temp-${Date.now()}-${Math.floor(Math.random() * 1000)}`;

        const newRecord = {
          ...JSON.parse(JSON.stringify(course)),
          tempId,
          isNew: true,
          searchRoomQuery: course.room_name || "",
          showRoomDropdown: false,
          searchCourseQuery: course.course_code || "",
          showCourseDropdown: false,
          searchSectionQuery: course.set_name || "",
          showSectionDropdown: false,
        };

        this.localData.push(newRecord);
      });

      toast.success(`${courses.length} course(s) assigned!`);
      this.closeAddSchedulePanel();
    },
    cancelJoin() {
      this.resetJoinState();
    },
    attemptUnjoin(item) {
      if (item.is_joined) {
        this.unjoinTarget = item;
        this.unjoinModalVisible = true;
      }
    },
    async confirmUnjoin() {
      if (!this.unjoinTarget) return;

      const record = this.unjoinTarget;
      const groupId = record.join_group_id;

      // Find all schedules in this join group
      const groupRecords = this.localData.filter(
        (r) => r.join_group_id === groupId,
      );

      // Reset join info for the entire group
      groupRecords.forEach((r) => {
        r.is_joined = false;
        r.join_group_id = null;
        r.joined_with = [];
      });

      // Clear global join modal state
      this.pendingJoinRecord = null;
      this.pendingJoinTargets = [];
      this.isJoined = false;

      // Optionally update backend
      try {
        await Promise.all(
          groupRecords.map((r) =>
            axios.patch(
              `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${r.id}`,
              {
                is_joined: false,
                join_group_id: null,
                joined_with: [],
              },
            ),
          ),
        );
        toast.success("All schedules in the join group have been unjoined!");
      } catch (err) {
        console.error("Failed to unjoin schedules:", err);
        toast.error("Failed to unjoin schedules.");
        // Rollback if needed
        groupRecords.forEach((r) => {
          r.is_joined = true;
          r.join_group_id = groupId;
          r.joined_with = groupRecords
            .filter((x) => x.id !== r.id)
            .map((x) => x.id);
        });
      } finally {
        this.unjoinModalVisible = false;
        this.unjoinTarget = null;
      }
    },

    cancelUnjoin() {
      this.unjoinModalVisible = false;
      this.unjoinTarget = null;
    },
    onMouseMoveTooltip(event) {
      if (this.scheduleTooltipVisible) {
        // Slight offset so the tooltip doesn’t cover the cursor
        this.tooltipX = event.clientX + 10;
        this.tooltipY = event.clientY + 10;
      }
    },
    hideScheduleTooltip() {
      this.scheduleTooltipVisible = false;
      this.tooltipItem = null;
    },
    showScheduleTooltip(event, item) {
      if (this.draggedRecord) return;

      const rect = event.currentTarget.getBoundingClientRect();

      // ✅ SAFE fallback
      const schedules = this.finalSchedules || this.localData || [];

      let joinedItems = [];

      if (item.is_joined && item.join_group_id) {
        joinedItems = schedules.filter(
          (s) => s.join_group_id === item.join_group_id,
        );
      }

      this.tooltipItem = {
        ...item,
        joinedItems,
      };

      this.scheduleTooltipVisible = true;

      const tooltipWidth = 260;
      const tooltipHeight = 200;

      this.tooltipX = Math.min(
        rect.right + 12,
        window.innerWidth - tooltipWidth,
      );

      this.tooltipY = Math.min(rect.top, window.innerHeight - tooltipHeight);
    },
    toggleJoin() {
      this.isJoined = !this.isJoined;
    },
    getJoinColor(groupId) {
      if (!groupId) return null;

      const colors = [
        "border-blue-500",
        "border-green-500",
        "border-purple-500",
        "border-pink-500",
        "border-yellow-500",
        "border-indigo-500",
      ];

      const index = Math.abs(groupId) % colors.length;
      return colors[index];
    },
    canJoin(recordA, recordB) {
      if (!recordA || !recordB) return false;
      if (recordA.id === recordB.id) return false;
      if (recordB.is_joined) return false;

      const getSetPrefix = (set_name) => set_name?.split(" ")[0]?.trim() || "";

      const baseSet = getSetPrefix(recordA.set_name);
      const targetSet = getSetPrefix(recordB.set_name);

      const validModes = ["online", "face to face"];
      const modeA = recordA.mode?.toLowerCase();
      const modeB = recordB.mode?.toLowerCase();

      return (
        recordA.course_code === recordB.course_code &&
        recordA.type === recordB.type &&
        recordA.semester === recordB.semester &&
        baseSet === targetSet &&
        Number(recordA.class_size) < 30 &&
        Number(recordB.class_size) < 30 &&
        validModes.includes(modeA) &&
        validModes.includes(modeB) &&
        modeA === modeB // <-- make sure the modes match exactly
      );
    },
    getJoinableSchedules(record) {
      if (!this.localData || !Array.isArray(this.localData)) {
        return [];
      }

      return this.localData.filter((r) => this.canJoin(record, r));
    },
    resetJoinState() {
      this.pendingJoinRecord = null;
      this.pendingJoinTargets = [];
      this.joinValidationModalVisible = false;
    },
    cleanDropdownFields(payload) {
      delete payload.searchRoomQuery;
      delete payload.showRoomDropdown;
      delete payload.searchCourseQuery;
      delete payload.showCourseDropdown;
      delete payload.searchSectionQuery;
      delete payload.showSectionDropdown;
    },
    async confirmJoin() {
      if (!this.pendingJoinRecord || !this.pendingJoinTargets.length) return;

      const baseRecord = this.pendingJoinRecord;

      // Filter only valid join targets
      const validTargets = this.pendingJoinTargets.filter((target) =>
        this.canJoin(baseRecord, target),
      );

      if (!validTargets.length) {
        toast.error("No valid schedules to join based on the rules.");
        this.resetJoinState();
        return;
      }

      const allToJoin = [baseRecord, ...validTargets];
      const finalMode = baseRecord.mode?.toLowerCase();
      const joinGroupId = baseRecord.id;
      const joinedIds = allToJoin.map((s) => s.id);

      // ✅ Update UI instantly
      allToJoin.forEach((s) => {
        s.day = baseRecord.day;
        s.start_hour = baseRecord.start_hour;
        s.duration = baseRecord.duration;
        s.time_slot = this.generateTimeSlot(s.start_hour, s.duration);
        s.mode = finalMode;

        if (finalMode === "face to face") {
          s.room_id = baseRecord.room_id || null;
          s.room_name = baseRecord.room_name || null;
          s.room_capacity = baseRecord.room_capacity || null;
          s.room_type = baseRecord.room_type || null;
        } else {
          s.room_id = null;
          s.room_name = null;
          s.room_capacity = null;
          s.room_type = null;
        }

        s.join_group_id = joinGroupId;
        s.is_joined = true;
        s.joined_with = joinedIds.filter((id) => id !== s.id);
      });

      this.resetJoinState();

      // ✅ Send PATCH request in background (batch style)
      axios
        .patch(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/bulk-join`,
          allToJoin.map((s) => ({
            id: s.id,
            day: s.day,
            start_hour: s.start_hour,
            duration: s.duration,
            mode: s.mode,
            room_id: s.room_id,
            room_name: s.room_name,
            room_capacity: s.room_capacity,
            room_type: s.room_type,
            join_group_id: s.join_group_id,
            is_joined: s.is_joined,
            joined_with: s.joined_with,
          })),
        )
        .catch((err) => console.error("Failed to save joined schedules:", err));

      toast.success(
        `Classes joined! Total students: ${allToJoin.reduce(
          (a, s) => a + Number(s.class_size || 0),
          0,
        )}`,
      );
    }, // called whenever mode changes
    /* ------------------ 1. UTILITY ------------------ */ sanitizePayload(
      record,
    ) {
      const allowed = [
        "class_id",
        "course_id",
        "course_code", // ✅ ADD THIS
        "set_name", // ✅ ADD THIS
        "program_id",
        "program_code",
        "institute_id",
        "type",
        "day",
        "start_hour",
        "duration",
        "time_slot", // ✅ ADD THIS
        "room_id",
        "room_name", // ✅ ADD THIS
        "room_type",
        "room_capacity",
        "class_size",
        "faculty_id",
        "faculty_name", // ✅ ADD THIS
        "school_year",
        "semester",
        "mode",
        "is_joined",
        "join_group_id",
        "joined_with",
        "college_branch_id",
      ];

      const payload = {};

      allowed.forEach((key) => {
        payload[key] = record[key] ?? null;
      });

      // ✅ ALWAYS regenerate time_slot
      payload.time_slot = this.generateTimeSlot(
        record.start_hour,
        record.duration,
      );

      return payload;
    },
    highlightRow(item) {
      this.highlightedRecordId = item.id || item.tempId;
      // optional: scroll to the row
      this.$nextTick(() => {
        const el = document.getElementById(`row-${this.highlightedRecordId}`);
        if (el) el.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    },
    onModeChange(record) {
      if ((record.mode || "").toLowerCase() === "online") {
        record.room_id = null;
        record.room_name = "None";
        record.room_type = null;
        record.room_capacity = null;
        record.searchRoomQuery = "None";
      } else {
        record.room_name = "";
        record.searchRoomQuery = "";
      }
    },
    normalizeHour(hour) {
      const h = Number(hour);
      if (Number.isNaN(h)) return null;
      return h; // ✅ already 24-hour based
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
    getTypeColor(type) {
      switch (type) {
        case "Lecture":
          return "bg-green-200 border-green-400";
        case "Laboratory":
          return "bg-blue-200 border-blue-400";
        default:
          return "bg-gray-200 border-gray-400";
      }
    },

    /* ------------------ 2. FETCHING ------------------ */
    async loadData() {
      try {
        const fetchDataStore = useFetchDataStore();

        // Always fetch latest schedules
        await fetchDataStore.fetchFinalSchedules();

        // Load ALL final schedules
        // Conflict filtering will be handled later in getSchedulesForConflictCheck()
        this.fullSchedules = (fetchDataStore.final_schedules || []).map(
          (rec) => {
            const cloned = structuredClone(rec);

            if (!cloned.id && !cloned.tempId) {
              cloned.tempId = `temp-${Date.now()}-${Math.floor(
                Math.random() * 1000,
              )}`;
            }

            return {
              ...cloned,

              // UI fields
              searchRoomQuery: cloned.room_name || "",
              showRoomDropdown: false,

              searchCourseQuery: cloned.course_code || "",
              showCourseDropdown: false,

              searchSectionQuery: cloned.set_name || "",
              showSectionDropdown: false,
            };
          },
        );

        console.log(
          "[Edit Schedule] Loaded Final Schedules:",
          this.fullSchedules.length,
        );
      } catch (error) {
        console.error("Failed to load full schedules:", error);
        this.fullSchedules = [];
      }
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
        await this.fetchCoursesForUser();
      } catch {
        this.user = {};
      }
    },

    async fetchCoursesForUser() {
      const fetchDataStore = useFetchDataStore();
      if (!this.user.role) return;

      let url = `${process.env.VUE_APP_API_BASE_URL}/courses/get-courses`;

      if (
        this.user.role === "Program Chairperson" ||
        this.user.role === "Department Chairperson"
      ) {
        const params = new URLSearchParams();
        if (this.user.institute_id)
          params.append("institute_id", this.user.institute_id);
        if (this.user.program_id)
          params.append("program_id", this.user.program_id);
        url += `?${params.toString()}`;
      }

      try {
        const { data } = await axios.get(url);
        fetchDataStore.courses = data;
      } catch {
        fetchDataStore.courses = [];
      }
    },
    refreshInstructorData(newData) {
      this.localData = (newData || []).map((rec) => {
        const cloned = structuredClone(rec);

        if (!cloned.id && !cloned.tempId) {
          cloned.tempId = `temp-${Date.now()}-${Math.floor(
            Math.random() * 1000,
          )}`;
        }

        return {
          ...cloned,
          searchRoomQuery: cloned.room_name || "",
          showRoomDropdown: false,

          searchCourseQuery: cloned.course_code || "",
          showCourseDropdown: false,

          searchSectionQuery: cloned.set_name || "",
          showSectionDropdown: false,
        };
      });

      this.draggedRecord = null;
    },
    openAddSchedulePanel(instructor) {
      this.selectedInstructorName = instructor;

      this.showAddPanel = true;
      this.showUnscheduledPanel = false;
    },

    openUnscheduledPanel(instructor) {
      this.selectedInstructorName = instructor;

      // Show BOTH panels
      this.showAddPanel = true;
      this.showUnscheduledPanel = true;
    },

    closeAddSchedulePanel() {
      this.showAddPanel = false;
      this.showUnscheduledPanel = false;
    },

    /* ------------------ 3. FILTERING ------------------ */

    filteredRooms(record) {
      let rooms = this.rooms || [];

      const selectedCampusId = Number(record.college_branch_id);

      if (selectedCampusId) {
        rooms = rooms.filter((room) => {
          const roomCampusId = Number(
            room.building?.buildingArea?.collegeBranch?.college_branch_id,
          );

          return roomCampusId === selectedCampusId;
        });
      }

      const query = record.searchRoomQuery?.trim().toLowerCase();

      if (query) {
        rooms = rooms.filter((room) =>
          room.room_name?.toLowerCase().includes(query),
        );
      }

      return rooms;
    },
    filteredSections(record) {
      const fetchDataStore = useFetchDataStore();
      const sections = fetchDataStore.sections || [];

      let filtered = sections;

      // ✅ Department Chairperson
      // cannot select own exact program
      if (this.user.role === "Department Chairperson") {
        filtered = filtered.filter(
          (s) =>
            !(
              Number(s.program?.institute?.institute_id) ===
                Number(this.user.institute_id) &&
              Number(s.program_id) === Number(this.user.program_id)
            ),
        );
      }

      // ✅ Program Chairperson
      // only own program
      if (this.user.role === "Program Chairperson") {
        filtered = filtered.filter(
          (s) =>
            Number(s.program?.institute?.institute_id) ===
              Number(this.user.institute_id) &&
            Number(s.program_id) === Number(this.user.program_id),
        );
      }

      const query = record.searchSectionQuery?.trim().toLowerCase();

      if (query) {
        filtered = filtered.filter((s) => {
          const display = `${s.program?.program_code || ""} - ${
            s.set_name || ""
          }`.toLowerCase();

          return display.includes(query);
        });
      }

      return filtered;
    },
    filteredCourses(record) {
      const fetchDataStore = useFetchDataStore();
      const curriculumCourses = fetchDataStore.curriculum_courses || [];

      let filtered = curriculumCourses;

      // ✅ Restrict BOTH Program Chairperson and Department Chairperson
      if (
        this.user.role === "Program Chairperson" ||
        this.user.role === "Department Chairperson"
      ) {
        filtered = filtered.filter(
          (cc) =>
            cc.curriculum?.institute_id === this.user.institute_id &&
            cc.curriculum?.program_id === this.user.program_id,
        );
      }

      const query = record.searchCourseQuery?.trim().toLowerCase();

      if (query) {
        filtered = filtered.filter((cc) => {
          const courseCode = cc.course?.course_code?.toLowerCase() || "";
          const courseTitle = cc.course?.course_title?.toLowerCase() || "";

          return courseCode.includes(query) || courseTitle.includes(query);
        });
      }

      return filtered;
    },
    /* ------------------ 4. SELECT ACTIONS ------------- */
    selectRoom(record, room) {
      // Only update if room changed
      if (record.room_id !== room.room_id) {
        record.room_id = room.room_id;
        record.room_name = room.room_name;
        record.room_type = room.room_type;
        record.room_capacity = room.room_capacity;
      }
      record.searchRoomQuery = room.room_name; // for display only
      record.showRoomDropdown = false;
    },
    selectSection(record, section) {
      // ✅ CLASS INFO
      record.class_id = section.class_id;
      record.set_name = section.set_name;
      record.class_size = section.class_size || 0;

      // ✅ PROGRAM INFO
      record.program_id = section.program?.program_id || null;

      record.program_code = section.program?.program_code || "";

      record.program_name = section.program?.program_name || "";

      // ✅ INSTITUTE INFO
      record.institute_id = section.program?.institute?.institute_id || null;

      record.institute_name = section.program?.institute?.institute_name || "";

      record.institute_code = section.program?.institute?.institute_code || "";

      // ✅ CAMPUS INFO
      record.college_branch_id =
        section.college_branch_id ||
        section.classInfo?.college_branch_id ||
        null;

      record.college_branch_name =
        section.classInfo?.collegeBranch?.college_branch_name || "";

      // ✅ DISPLAY VALUE
      record.searchSectionQuery = `${section.program?.program_code || ""} - ${
        section.set_name
      }`;

      record.showSectionDropdown = false;

      // ✅ RESET ROOM WHEN SECTION CHANGES
      record.room_id = null;
      record.room_name = "";
      record.room_type = "";
      record.room_capacity = "";
      record.searchRoomQuery = "";
    },
    selectCourse(record, curriculumCourse) {
      const course = curriculumCourse.course;
      const curriculum = curriculumCourse.curriculum;

      record.course_id = course.course_id;
      record.course_code = course.course_code;

      // ✅ gikan sa PROP
      record.school_year = this.activeSchoolYear?.school_year_name || "";
      record.semester = String(this.activeSchoolYear?.semester || "");

      record.program_id = curriculum?.program_id || null;
      record.program_code = curriculum?.program?.program_code || "";
      record.institute_id = curriculum?.institute_id || null;

      record.searchCourseQuery = course.course_code;
      record.showCourseDropdown = false;
    },
    /* ------------------ 5. ROW MANAGEMENT ------------- */

    addNewRow() {
      this.closeAddSchedulePanel(); // closes both panels

      // Reopen only Add panel
      this.showAddPanel = true;
      console.log("activeSchoolYear", this.activeSchoolYear);
      const first = this.instructorData[0];

      const tempId = `temp-${Date.now()}`;

      const class_id = first?.class_id || null;
      const class_size = first?.class_size || null;

      // ✅ FIND FIRST AVAILABLE SLOT
      let selectedDay = "Monday";
      let selectedHour = 7;

      outerLoop: for (const day of this.days) {
        for (let hour = 7; hour <= 20; hour++) {
          const occupied = this.localData.some(
            (r) => r.day === day && Number(r.start_hour) === Number(hour),
          );

          if (!occupied) {
            selectedDay = day;
            selectedHour = hour;
            break outerLoop;
          }
        }
      }

      const formatTime = (h) => {
        const period = h >= 12 ? "PM" : "AM";
        const hour = h % 12 || 12;
        return `${hour}:00 ${period}`;
      };

      this.localData.push({
        tempId,
        isNew: true,

        faculty_name: first?.faculty_name || "TBD",
        faculty_id: first?.faculty_id || null,

        class_id,
        class_size,

        mode: "face to face",

        day: selectedDay,
        start_hour: selectedHour,
        duration: 3,

        time_slot: `${formatTime(selectedHour)} - ${formatTime(
          selectedHour + 3,
        )}`,

        room_id: null,
        room_name: "",
        room_type: "",
        room_capacity: "",

        course_id: null,
        course_code: "",
        type: "Lecture",

        // ✅ GET FROM PROP
        school_year:
          this.activeSchoolYear?.school_year_name ||
          this.activeSchoolYear?.school_year ||
          "",

        semester: this.activeSchoolYear?.semester || "",

        program_id: this.user.program_id || null,
        institute_id: this.user.institute_id || null,

        searchRoomQuery: "",
        showRoomDropdown: false,

        searchCourseQuery: "",
        showCourseDropdown: false,

        searchSectionQuery: "",
        showSectionDropdown: false,
      });

      console.log("Added row using activeSchoolYear:", this.activeSchoolYear);
    },
    cancelNewRow() {
      // Remove the last temp row only
      for (let i = this.localData.length - 1; i >= 0; i--) {
        if (
          this.localData[i].tempId &&
          this.localData[i].tempId.startsWith("temp-")
        ) {
          this.localData.splice(i, 1);
          break;
        }
      }
    },
    toggleDelete(record) {
      this.deleteTarget = record;
      this.showConfirmDelete = true;
    },

    cancelDelete() {
      this.showConfirmDelete = false;
      this.deleteTarget = null;
    },
    async confirmDelete() {
      if (!this.deleteTarget) return;

      try {
        this.deleting = true;

        // 🔥 CALL API DELETE ENDPOINT
        await axios.delete(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${this.deleteTarget.id}`,
        );

        // After removing locally
        this.localData = this.localData.filter(
          (item) => item.id !== this.deleteTarget.id,
        );

        this.$emit("deleted", this.deleteTarget.id);
        toast.success("Schedule deleted successfully.");
      } catch (error) {
        console.error(error);
        toast.error("Failed to delete schedule.");
      } finally {
        this.deleting = false;
        this.showConfirmDelete = false;
        this.deleteTarget = null;

        // 🔄 OPTIONAL: refresh all schedules from Pinia store
        if (this.fetchFacultyLoads) {
          await this.fetchFacultyLoads();
        }
      }
    },
    /* ------------------ 6. SCHEDULE GRID -------------- */
    getConflictsInCell(slot, day, instructor) {
      const cellRecords = this.getScheduleForCell(slot, day, instructor);
      return cellRecords
        .map((r) => this.getConflictingRecords(r))
        .flat()
        .filter((r) => r.faculty_name !== instructor);
    },
    getSchedulesForConflictCheck(record) {
      return this.fullSchedules.filter(
        (s) =>
          String(s.school_year).trim() === String(record.school_year).trim() &&
          Number(s.semester) === Number(record.semester),
      );
    },

    getConflictingRecords(record) {
      if (!record || record.start_hour == null || record.duration == null) {
        return [];
      }

      const recordStart = Number(record.start_hour);
      const recordEnd = recordStart + Number(record.duration);

      const sourceSchedules = this.getAllSchedulesForConflict(record);

      return sourceSchedules
        .filter((r) => {
          if (!r) return false;

          // Skip itself
          if (
            (record.id && r.id === record.id) ||
            (record.tempId && r.tempId === record.tempId)
          ) {
            return false;
          }

          // Ignore schedules in the same joined group
          if (
            record.join_group_id &&
            r.join_group_id &&
            Number(record.join_group_id) === Number(r.join_group_id)
          ) {
            return false;
          }

          // Same day only
          if (r.day !== record.day) return false;

          const rStart = Number(r.start_hour);
          const rEnd = rStart + Number(r.duration);

          // Time overlap
          if (Math.max(recordStart, rStart) >= Math.min(recordEnd, rEnd)) {
            return false;
          }

          const sameFaculty =
            (record.faculty_id &&
              r.faculty_id &&
              Number(record.faculty_id) === Number(r.faculty_id)) ||
            (record.faculty_name &&
              r.faculty_name &&
              record.faculty_name.trim().toLowerCase() ===
                r.faculty_name.trim().toLowerCase());

          const sameRoom =
            record.mode?.toLowerCase() === "face to face" &&
            r.mode?.toLowerCase() === "face to face" &&
            record.room_id &&
            r.room_id &&
            Number(record.room_id) === Number(r.room_id);

          const sameClass =
            record.class_id &&
            r.class_id &&
            Number(record.class_id) === Number(r.class_id);

          const sameOnlineSection =
            record.mode?.toLowerCase() === "online" &&
            r.mode?.toLowerCase() === "online" &&
            record.set_name === r.set_name &&
            Number(record.program_id) === Number(r.program_id) &&
            Number(record.college_branch_id) === Number(r.college_branch_id);

          const reasons = [];

          if (sameFaculty) reasons.push("Faculty conflict");
          if (sameRoom) reasons.push("Room conflict");
          if (sameClass) reasons.push("Class conflict");
          if (sameOnlineSection) reasons.push("Online section conflict");

          if (!reasons.length) return false;

          return true;
        })
        .map((r) => {
          const reasons = [];

          const sameFaculty =
            (record.faculty_id &&
              r.faculty_id &&
              Number(record.faculty_id) === Number(r.faculty_id)) ||
            (record.faculty_name &&
              r.faculty_name &&
              record.faculty_name.trim().toLowerCase() ===
                r.faculty_name.trim().toLowerCase());

          const sameRoom =
            record.mode?.toLowerCase() === "face to face" &&
            r.mode?.toLowerCase() === "face to face" &&
            Number(record.room_id) === Number(r.room_id);

          const sameClass = Number(record.class_id) === Number(r.class_id);

          const sameOnlineSection =
            record.mode?.toLowerCase() === "online" &&
            r.mode?.toLowerCase() === "online" &&
            record.set_name === r.set_name &&
            Number(record.program_id) === Number(r.program_id) &&
            Number(record.college_branch_id) === Number(r.college_branch_id);

          if (sameFaculty) reasons.push("Faculty conflict");
          if (sameRoom) reasons.push("Room conflict");
          if (sameClass) reasons.push("Class conflict");
          if (sameOnlineSection) reasons.push("Online section conflict");

          return {
            ...r,
            reason: reasons.join(", "),
          };
        });
    },
    openConflictModal(record) {
      this.selectedSchedule = {
        ...record,
        time_start: record.start_hour ?? 0,
        time_end: (record.start_hour ?? 0) + (record.duration ?? 0),
        course_code: record.course_code || "N/A",
        faculty_name: record.faculty_name || "TBD",
        set_name: record.set_name || "TBD",
        room_name: record.room_name || "TBD",
        day: record.day || "TBD",
        mode: record.mode || "face to face",
      };

      this.conflictRecords = this.getConflictingRecords(record);
      this.conflictModalVisible = true;
    },
    closeConflictModal() {
      this.conflictModalVisible = false;
      this.conflictRecords = [];
    },

    /* ------------------ 7. CONFLICT LOGIC ------------- */

    hasRoomConflict(record) {
      const key = record.id || record.tempId;

      return (this.conflictMap[key] || []).length > 0;
    },

    getConflictTooltip(record) {
      const conflicts = this.getConflictingRecords(record);
      if (!conflicts.length) return "";
      return conflicts
        .map(
          (c) =>
            `Conflict with: ${c.faculty_name} (${c.course_code}) in ${c.room_name}`,
        )
        .join("\n");
    },

    getScheduleForCell(slot, day, instructor) {
      const key = `${instructor}-${day}`;

      return (this.scheduleGrid[key] || []).filter(
        (r) =>
          r.start_hour != null &&
          r.duration != null &&
          r.start_hour < slot.end &&
          r.start_hour + r.duration > slot.start,
      );
    },
    isValid() {
      return this.localData.every(
        (r) =>
          r.faculty_name &&
          r.day &&
          r.start_hour != null &&
          r.duration != null &&
          !this.hasRoomConflict(r),
      );
    },

    /* ------------------ 8. DRAG & DROP ---------------- */
    getConflictsForDrag(record, targetInstructor, targetDay, targetStartHour) {
      const clonedRecord = { ...record };
      clonedRecord.faculty_name = targetInstructor;
      clonedRecord.day = targetDay;
      clonedRecord.start_hour = targetStartHour;

      return this.getConflictingRecords(clonedRecord);
    },
    onDragOver(event, instructor, day, slotStart) {
      if (!this.draggedRecord) return;
      this.previewX = event.clientX + 12;
      this.previewY = event.clientY + 12;
      this.conflictPreview = this.getConflictsForDrag(
        this.draggedRecord,
        instructor,
        day,
        slotStart,
      );
    },
    onDragStart(event, record) {
      this.isDragging = true;
      event.dataTransfer.effectAllowed = "move";

      this.hideScheduleTooltip();

      this.draggedRecord = record;
      this.dragConflictMap = {};

      Object.keys(this.groupedSchedule).forEach((faculty) => {
        this.days.forEach((day) => {
          this.timeSlots.forEach((slot) => {
            const key = `${faculty}-${day}-${slot.start}`;

            // Simulate dropping the schedule here
            const tempRecord = {
              ...record,
              faculty_name: faculty,
              day,
              start_hour: slot.start,
            };

            // Is this drop location invalid?
            this.dragConflictMap[key] =
              this.getConflictingRecords(tempRecord).length > 0;
          });
        });
      });
    },
    onDragEnd() {
      this.isDragging = false;
      this.hideScheduleTooltip();

      this.draggedRecord = null;
      this.draggedGroup = [];
    },
    async onDrop(event, targetInstructor, targetDay, targetStartHour) {
      if (!this.draggedRecord) return;

      const group = this.draggedGroup?.length
        ? this.draggedGroup
        : [this.draggedRecord];

      /* ===============================
     STEP 1: JOIN MODE CHECK
  =============================== */

      if (this.isJoined && group.length === 1) {
        const tempRecord = {
          ...this.draggedRecord,
          faculty_name: targetInstructor,
          day: targetDay,
          start_hour: targetStartHour,
        };

        const joinables = this.getJoinableSchedules(tempRecord);

        if (joinables.length) {
          this.pendingJoinRecord = this.draggedRecord;
          this.pendingJoinTargets = joinables;
          this.joinValidationModalVisible = true;
          return;
        }
      }

      /* ===============================
     STEP 2: GROUP CONFLICT CHECK
  =============================== */

      const groupConflicts = [];

      for (const rec of group) {
        const tempRecord = {
          ...rec,
          faculty_name: targetInstructor,
          day: targetDay,
          start_hour: targetStartHour,
        };

        const conflicts = this.getConflictingRecords(tempRecord).filter(
          (c) => !group.some((g) => g.id === c.id),
        );

        groupConflicts.push(...conflicts);
      }

      if (groupConflicts.length) {
        this.selectedSchedule = {
          ...this.draggedRecord,
          time_start: targetStartHour ?? 0,
          time_end: (targetStartHour ?? 0) + (this.draggedRecord.duration ?? 0),
          faculty_name: targetInstructor,
          day: targetDay,
        };

        this.conflictRecords = groupConflicts;
        this.conflictModalVisible = true;

        this.draggedRecord = null;
        this.draggedGroup = [];
        return;
      }

      /* ===============================
     STEP 3: MOVE ENTIRE GROUP
  =============================== */

      for (const rec of group) {
        Object.assign(rec, {
          faculty_name: targetInstructor,
          day: targetDay,
          start_hour: targetStartHour,
        });

        rec.time_slot = this.generateTimeSlot(rec.start_hour, rec.duration);

        const payload = this.sanitizePayload(rec);
        this.cleanDropdownFields(payload);

        const id = rec.id || rec.schedule_id || rec.final_generated_id;

        if (!id) continue;

        try {
          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
            payload,
          );
        } catch (error) {
          console.error("Failed to update schedule:", error);
        }
      }

      /* ===============================
     RESET
  =============================== */

      this.draggedRecord = null;
      this.draggedGroup = [];
    },
    /* ------------------ 9. SAVING TO DATABASE  ---------------- */
    async saveEdit() {
      this.saving = true;

      try {
        // -----------------------------
        // 1️⃣ Remove duplicates locally
        // -----------------------------
        const seen = new Set();
        this.localData = this.localData.filter((record) => {
          const key =
            record.id ||
            record.tempId ||
            `${record.course_id}|${record.room_id}|${record.class_id}|${record.mode}|${record.day}|${record.start_hour}|${record.faculty_id}`;
          if (seen.has(key)) return false;
          seen.add(key);
          return true;
        });

        const newRows = [];
        const updatedRows = [];

        this.localData.forEach((record) => {
          // Ensure new records have a tempId
          if (!record.id && !record.tempId) {
            record.tempId = `temp-${Date.now()}-${Math.floor(
              Math.random() * 1000,
            )}`;
          }

          const payload = this.sanitizePayload({
            ...record,
            mode:
              record.mode?.toLowerCase() === "online"
                ? "online"
                : "face to face",
          });

          const id =
            record.id || record.schedule_id || record.final_generated_id;

          if (id) updatedRows.push({ id, payload });
          else {
            // Attach tempId to payload for matching later
            payload.tempId = record.tempId;
            newRows.push(payload);
          }
        });

        // -----------------------------
        // 2️⃣ Create new schedules (bulk)
        // -----------------------------
        if (newRows.length) {
          const { data } = await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/manual-bulk`,
            {
              schedules: newRows,
              override: true,
            },
          );

          // Assign returned IDs to localData
          data.forEach((row) => {
            const tempRecord = this.localData.find(
              (r) => !r.id && r.tempId === row.tempId,
            );
            if (tempRecord) tempRecord.id = row.id;
          });
        }

        // -----------------------------
        // 3️⃣ Update existing schedules
        // -----------------------------
        if (updatedRows.length) {
          await Promise.all(
            updatedRows.map(({ id, payload }) =>
              axios.patch(
                `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
                payload,
              ),
            ),
          );
        }

        toast.success("Schedules saved successfully!");
        this.$emit("saved", this.localData);
        this.$emit("close");
        this.$emit("refresh");
      } catch (err) {
        console.error("Failed to save schedules:", err);
        toast.error("Failed to save schedules.");
      } finally {
        this.saving = false;
      }
    },
  },
  async mounted() {
    await this.fetchUser();

    const roomsPromise = this.fetchRooms();
    if (roomsPromise && roomsPromise.then) await roomsPromise;

    await this.fetchClassSections();
    await this.fetchCurriculumCourses();
    await this.fetchCollegeBranch();
    await this.fetchRawUsers();
    await this.loadData();
  },
};
</script>

<style scoped>
td {
  transition: background 0.2s;
  position: relative;
}
.schedule-dragging {
  animation: clothGrab 180ms ease-out forwards;

  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2), 0 10px 25px rgba(0, 0, 0, 0.12);

  cursor: grabbing;
  z-index: 9999 !important;
}

@keyframes clothGrab {
  0% {
    transform: scale(1);
  }

  40% {
    transform: scaleX(1.03) scaleY(0.97);
  }

  100% {
    transform: scale(1.06) rotate(-2deg);
  }
}
</style>
