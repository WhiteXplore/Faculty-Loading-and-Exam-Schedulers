<template>
  <div
    v-if="show"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 px-2 gap-2"
  >
    <div class="flex justify-center gap-2 w-full">
      <!-- MAIN MODAL WRAPPER -->
      <div
        class="bg-white w-full h-[98vh] rounded-xl shadow-xl flex flex-col overflow-hidden"
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
                <div class="max-h-[73vh] overflow-y-auto border rounded-lg">
                  <table
                    class="w-full table-auto border-separate border-spacing-0 text-[11px]"
                  >
                    <thead class="sticky top-0 z-[5000] bg-gray-200">
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
                          @dragover.prevent="
                            onDragOver($event, instructor, day, slot.start)
                          "
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
                              @mouseenter="showScheduleTooltip($event, item)"
                              @mouseleave="hideScheduleTooltip"
                              @dragstart="onDragStart($event, item)"
                              @dragend="onDragEnd"
                              @dblclick="attemptUnjoin(item)"
                              @click="highlightRow(item)"
                              :class="[
                                'absolute inset-x-1 border rounded text-[11px] p-1 shadow-sm truncate cursor-pointer',

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
                                height: getBlockHeight(item) + 'px',
                                width: 'calc(100% - 0.5rem)',
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
        :class="[
          'h-full flex gap-2',
          showAddPanel && showUnscheduledPanel
            ? 'w-[90vw]'
            : showAddPanel
            ? 'w-[30vw]'
            : 'w-[45vw]',
        ]"
      >
        <div
          v-if="showAddPanel"
          :class="[
            'w-[45vw] bg-white border shadow-xl transition-all duration-300 flex justify-start rounded-xl',
            showUnscheduledPanel ? 'h-full ' : '',
          ]"
        >
          <div class="flex flex-col w-full">
            <div
              v-if="expandedRecord"
              class="bg-white rounded-xl border shadow-lg overflow-hidden"
            >
              <!-- Header -->
              <div
                class="flex items-center justify-between px-6 py-2 border-b bg-defaultGreen text-white"
              >
                <div>
                  <h3 class="text-lg font-semibold">Update Schedule</h3>
                  <p class="text-xs text-green-100">
                    Update the selected schedule information
                  </p>
                </div>

                <button
                  @click="cancelNewRow"
                  class="w-8 h-8 rounded-full hover:bg-white/20 transition"
                >
                  ✕
                </button>
              </div>

              <div>
                <div class="p-2">
                  <div class="p-6 border-r">
                    <div class="grid grid-cols-1 gap-5">
                      <!-- ===================== SECTION ===================== -->
                      <div class="dropdown-container relative">
                        <label class="dropdown-label">Section :</label>

                        <div class="dropdown-wrapper">
                          <input
                            v-model="expandedRecord.searchSectionQuery"
                            :disabled="!canEditSchedule(expandedRecord)"
                            type="text"
                            placeholder="Search section..."
                            class="dropdown-input"
                            :class="
                              !canEditSchedule(expandedRecord)
                                ? 'bg-gray-100 cursor-not-allowed text-gray-500'
                                : ''
                            "
                            @focus="expandedRecord.showSectionDropdown = true"
                            @input="expandedRecord.class_id = null"
                          />

                          <div
                            v-if="expandedRecord.showSectionDropdown"
                            class="dropdown-menu"
                            @mouseleave="
                              expandedRecord.showSectionDropdown = false
                            "
                          >
                            <div v-if="filteredSections(expandedRecord).length">
                              <div
                                v-for="section in filteredSections(
                                  expandedRecord,
                                )"
                                :key="section.class_id"
                                class="dropdown-item"
                                @mousedown.prevent="
                                  selectSection(expandedRecord, section)
                                "
                              >
                                {{ section.program?.program_code }} -
                                {{ section.set_name }}
                              </div>
                            </div>

                            <div v-else class="dropdown-item text-gray-400">
                              No section found
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- ===================== COURSE ===================== -->

                      <div class="dropdown-container relative">
                        <label class="dropdown-label">Course :</label>

                        <div class="dropdown-wrapper">
                          <input
                            v-model="expandedRecord.searchCourseQuery"
                            :disabled="!canEditSchedule(expandedRecord)"
                            type="text"
                            placeholder="Search course..."
                            class="dropdown-input"
                            :class="
                              !canEditSchedule(expandedRecord)
                                ? 'bg-gray-100 cursor-not-allowed text-gray-500'
                                : ''
                            "
                            @focus="expandedRecord.showCourseDropdown = true"
                            @input="expandedRecord.course_id = null"
                          />

                          <div
                            v-if="expandedRecord.showCourseDropdown"
                            class="dropdown-menu"
                            @mouseleave="
                              expandedRecord.showCourseDropdown = false
                            "
                          >
                            <div v-if="filteredCourses(expandedRecord).length">
                              <div
                                v-for="item in filteredCourses(expandedRecord)"
                                :key="item.curriculum_course_id"
                                class="dropdown-item"
                                @mousedown.prevent="
                                  selectCourse(expandedRecord, item)
                                "
                              >
                                {{ item.course?.course_code }}
                              </div>
                            </div>

                            <div v-else class="dropdown-item text-gray-400">
                              No course found
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- ===================== CAMPUS ===================== -->
                      <div class="dropdown-container relative">
                        <label class="dropdown-label">Campus :</label>

                        <div class="dropdown-wrapper">
                          <input
                            v-model="expandedRecord.searchCampusQuery"
                            :disabled="!canEditSchedule(expandedRecord)"
                            type="text"
                            placeholder="Select campus..."
                            class="dropdown-input"
                            :class="
                              !canEditSchedule(expandedRecord)
                                ? 'bg-gray-100 cursor-not-allowed text-gray-500'
                                : ''
                            "
                            @focus="expandedRecord.showCampusDropdown = true"
                            @input="
                              expandedRecord.college_branch_id = null;
                              expandedRecord.college_branch_name = '';
                            "
                          />

                          <div
                            v-if="expandedRecord.showCampusDropdown"
                            class="dropdown-menu"
                            @mouseleave="
                              expandedRecord.showCampusDropdown = false
                            "
                          >
                            <div
                              v-if="
                                availableCampuses().filter((campus) =>
                                  campus.college_branch_name
                                    .toLowerCase()
                                    .includes(
                                      (
                                        expandedRecord.searchCampusQuery || ''
                                      ).toLowerCase(),
                                    ),
                                ).length
                              "
                            >
                              <div
                                v-for="campus in availableCampuses().filter(
                                  (campus) =>
                                    campus.college_branch_name
                                      ?.toLowerCase()
                                      .includes(
                                        (
                                          expandedRecord.searchCampusQuery || ''
                                        ).toLowerCase(),
                                      ),
                                )"
                                :key="campus.college_branch_id"
                                class="dropdown-item"
                                @mousedown.prevent="
                                  expandedRecord.college_branch_id = Number(
                                    campus.college_branch_id,
                                  );

                                  expandedRecord.college_branch_name =
                                    campus.college_branch_name;

                                  expandedRecord.searchCampusQuery =
                                    campus.college_branch_name;

                                  expandedRecord.showCampusDropdown = false;

                                  onCampusChange(expandedRecord);
                                "
                              >
                                {{ campus.college_branch_name }}
                              </div>
                            </div>

                            <div v-else class="dropdown-item text-gray-400">
                              No campus found
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- ===================== ROOM ===================== -->
                      <div class="dropdown-container relative">
                        <label class="dropdown-label"> Room : </label>

                        <div class="flex items-start gap-2">
                          <!-- ======================================================= -->
                          <!-- NORMAL ROOM SEARCH -->
                          <!-- ======================================================= -->
                          <div class="dropdown-wrapper relative flex-1">
                            <input
                              v-model="expandedRecord.searchRoomQuery"
                              :disabled="!canEditSchedule(expandedRecord)"
                              type="text"
                              placeholder="Select room..."
                              class="dropdown-input w-full"
                              :class="
                                !canEditSchedule(expandedRecord)
                                  ? 'bg-gray-100 cursor-not-allowed text-gray-500'
                                  : ''
                              "
                              @focus="expandedRecord.showRoomDropdown = true"
                              @input="
                                expandedRecord.room_id = null;
                                expandedRecord.room_name = null;
                                expandedRecord.room_type = null;
                                expandedRecord.room_capacity = null;
                              "
                            />

                            <!-- ===================================================== -->
                            <!-- ROOM DROPDOWN -->
                            <!-- ===================================================== -->
                            <div
                              v-if="expandedRecord.showRoomDropdown"
                              class="dropdown-menu"
                              @mouseleave="
                                expandedRecord.showRoomDropdown = false
                              "
                            >
                              <div v-if="filteredRooms(expandedRecord).length">
                                <div
                                  v-for="room in filteredRooms(expandedRecord)"
                                  :key="room.room_id"
                                  class="dropdown-item flex items-center justify-between gap-3"
                                  @mousedown.prevent="
                                    selectRoom(expandedRecord, room)
                                  "
                                >
                                  <!-- Room Information -->
                                  <div class="min-w-0">
                                    <div class="truncate font-medium">
                                      {{ room.room_name }}
                                    </div>

                                    <div class="text-[10px] text-gray-400">
                                      Capacity:
                                      {{ room.room_capacity || "-" }}
                                    </div>
                                  </div>

                                  <!-- Room Type -->
                                  <span
                                    class="inline-flex shrink-0 items-center rounded-full border px-2 py-0.5 text-[9px] font-bold uppercase"
                                    :class="
                                      getRoomTypeBadgeClass(room.room_type)
                                    "
                                  >
                                    {{ getRoomTypeLabel(room.room_type) }}
                                  </span>
                                </div>
                              </div>

                              <div
                                v-else
                                class="dropdown-item py-3 text-center text-gray-400"
                              >
                                No room found
                              </div>
                            </div>
                          </div>

                          <!-- ======================================================= -->
                          <!-- 2D MAP BUTTON -->
                          <!-- ======================================================= -->
                          <button
                            type="button"
                            :disabled="!canEditSchedule(expandedRecord)"
                            class="flex h-[38px] w-[42px] shrink-0 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-600 shadow-sm transition hover:border-emerald-300 hover:bg-emerald-50 hover:text-emerald-600 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-300"
                            title="Select room from 2D map"
                            @click="openRoomMap"
                          >
                            <!-- Map Icon -->
                            <svg
                              xmlns="http://www.w3.org/2000/svg"
                              class="h-[18px] w-[18px]"
                              viewBox="0 0 24 24"
                              fill="none"
                              stroke="currentColor"
                              stroke-width="1.8"
                            >
                              <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                d="M9 20.25 3.75 18V5.25L9 7.5m0 12.75 6-2.25m-6 2.25V7.5m6 10.5 5.25 2.25V7.5L15 5.25m0 12.75V5.25m0 0L9 7.5"
                              />
                            </svg>
                          </button>
                        </div>

                        <!-- ========================================================= -->
                        <!-- SELECTED ROOM INFORMATION -->
                        <!-- ========================================================= -->
                        <div
                          v-if="expandedRecord.room_id"
                          class="mt-1 flex items-center gap-2 text-[10px] text-gray-400"
                        >
                          <span>
                            Capacity:
                            {{ expandedRecord.room_capacity || "-" }}
                          </span>

                          <span>•</span>

                          <span>
                            {{ getRoomTypeLabel(expandedRecord.room_type) }}
                          </span>
                        </div>
                      </div>

                      <!-- ===================== DAY ===================== -->
                      <div class="space-y-2">
                        <label class="dropdown-label">Day :</label>

                        <div class="flex flex-wrap gap-2">
                          <button
                            v-for="day in [
                              'Monday',
                              'Tuesday',
                              'Wednesday',
                              'Thursday',
                              'Friday',
                              'Saturday',
                              'Sunday',
                            ]"
                            :key="day"
                            type="button"
                            @click="
                              canEditSchedule(expandedRecord) &&
                                (expandedRecord.day = day)
                            "
                            :disabled="!canEditSchedule(expandedRecord)"
                            :class="[
                              'px-4 py-2 rounded-full border text-xs font-medium transition-all duration-200',
                              !canEditSchedule(expandedRecord)
                                ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed'
                                : expandedRecord.day === day
                                ? 'bg-defaultGreen text-white border-defaultGreen shadow-md'
                                : 'bg-white text-gray-700 border-gray-300 hover:border-defaultGreen hover:text-defaultGreen hover:bg-green-50',
                            ]"
                          >
                            {{ day }}
                          </button>
                        </div>
                      </div>

                      <!-- ===================== MODE ===================== -->
                      <div>
                        <label class="dropdown-label">Mode :</label>

                        <select
                          v-model="expandedRecord.mode"
                          :disabled="!canEditSchedule(expandedRecord)"
                          class="dropdown-input"
                        >
                          <option value="face to face">Face to Face</option>
                          <option value="online">Online</option>
                        </select>
                      </div>

                      <div class="grid grid-cols-2 gap-2">
                        <!-- ===================== START HOUR ===================== -->
                        <div>
                          <label class="dropdown-label">Start Hour :</label>

                          <input
                            type="number"
                            step="0.5"
                            v-model.number="expandedRecord.start_hour"
                            :disabled="!canEditSchedule(expandedRecord)"
                            class="dropdown-input"
                          />
                        </div>

                        <!-- ===================== DURATION ===================== -->
                        <div>
                          <label class="dropdown-label">Duration :</label>

                          <input
                            type="number"
                            step="0.5"
                            v-model.number="expandedRecord.duration"
                            :disabled="!canEditSchedule(expandedRecord)"
                            class="dropdown-input"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <!-- Footer Buttons -->
              <div class="flex justify-end gap-2 p-3 text-xs border-t">
                <button
                  @click="toggleDelete"
                  class="btn-delete1"
                  v-if="expandedRecord?.id"
                >
                  Remove
                </button>
                <!-- <button
                  @click="addNewRow"
                  class="btn-save"
                  v-if="!expandedRecord?.id"
                >
               
                  Add Schedule
                </button> -->
                <button @click="cancelNewRow" class="btn-cancel">Clear</button>
              </div>
            </div>
          </div>
        </div>
        <!-- Expanded Details -->

        <div
          v-if="showUnscheduledPanel"
          class="relative z-[9999] w-[45vw] max-h-[90vh] overflow-hidden bg-white rounded-xl"
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
    class="absolute z-[9999] pointer-events-none"
    :style="{
      top: tooltipY + 'px',
      left: tooltipX + 'px',
      transform:
        tooltipPlacement === 'left' ? 'translateX(-100%)' : 'translateX(0)',
    }"
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
  <RoomMapModal
    :show="showRoomMap"
    :rooms="expandedRecord ? filteredRooms(expandedRecord) : rooms"
    :selected-room-id="expandedRecord?.room_id || null"
    @close="closeRoomMap"
    @select-room="selectRoomFromMap"
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
import RoomMapModal from "../modals/room-map-modal.vue";
export default {
  name: "EditScheduleModal",
  components: {
    icon,
    editJoinValdiation,
    unscheduled,
    UnjoinModal,
    RoomMapModal,
  },
  props: {
    show: Boolean,

    instructorData: {
      type: Array,
      default: () => [],
    },

    activeSchoolYear: {
      type: Object,
      default: null,
    },

    selectedUnscheduledMeeting: {
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
      highlightedRecordId: null, // Double Space detection
      lastSpacePressTime: 0,
      spaceDoubleTapDelay: 350,
      isJoined: false,
      joinValidationModalVisible: false,
      pendingJoinRecord: null,
      pendingJoinTargets: [],

      draggedGroup: [],
      scheduleTooltipVisible: false,
      tooltipItem: null,
      tooltipX: 0,
      tooltipY: 0,
      tooltipPlacement: "right",
      unjoinModalVisible: false,
      unjoinTarget: null,

      timeSlotHeight: 60,

      dragConflictMap: {},
      isDragging: false,
      conflictMapCache: {},

      panelMode: null,
      expandedRecord: null,
      college_branch: [],
      restoredUnscheduledMeetings: [],

      showRoomMap: false,
    };
  },
  computed: {
    ...mapState(useFetchDataStore, [
      "rooms",
      "curriculum_courses",
      "rawusers",
      "  all_school_years",
    ]),

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
    selectedUnscheduledMeeting: {
      immediate: true,
      deep: true,

      async handler(meeting) {
        if (!meeting) return;

        console.log("[Edit Schedule] Selected unscheduled meeting:", meeting);

        // =========================================================
        // 1. LOAD CURRENT INSTRUCTOR SCHEDULES
        // =========================================================
        this.localData = (this.instructorData || []).map((record) => ({
          ...record,
        }));

        // =========================================================
        // 2. GET SELECTED FACULTY
        //
        // IMPORTANT:
        // The faculty selected from the possible-faculty list
        // must be the faculty receiving this temporary schedule.
        // =========================================================
        const selectedFacultyName =
          meeting.selected_faculty_name ||
          meeting.faculty_name ||
          this.selectedInstructorName ||
          "";

        const normalizeName = (name) =>
          String(name || "")
            .trim()
            .replace(/\s+/g, " ")
            .toLowerCase();

        const normalizedFacultyName = normalizeName(selectedFacultyName);

        const selectedFaculty = (this.rawusers || []).find(
          (user) =>
            normalizeName(
              `${user.first_name || ""} ${user.last_name || ""}`,
            ) === normalizedFacultyName,
        );

        const selectedFacultyId =
          meeting.selected_faculty_id ||
          meeting.faculty_id ||
          selectedFaculty?.id ||
          selectedFaculty?.user_id ||
          null;

        console.log("[Edit Schedule] SELECTED FACULTY:", {
          name: selectedFacultyName,
          id: selectedFacultyId,
          user: selectedFaculty,
        });

        if (!selectedFacultyName) {
          console.error("[Edit Schedule] No selected faculty found.", meeting);

          toast.error("No faculty was selected.");
          return;
        }

        // =========================================================
        // 3. IDENTIFY THE ACTUAL CLASS / SECTION
        //
        // We MUST NOT rely only on meeting.class_id.
        //
        // Example:
        //
        // CHEM 111 - BSFAS 1st Year D
        //
        // must not accidentally become:
        //
        // CHEM 111 - BSFAS 1st Year C
        // =========================================================

        const store = useFetchDataStore();

        // Adjust this only if your Pinia store uses another
        // property name for the class sections.
        const sections = store.classes || store.classSections || [];

        const meetingProgramId = Number(
          meeting.class_program_id || meeting.program_id || 0,
        );

        const meetingSetName = String(meeting.set_name || "")
          .trim()
          .toLowerCase();

        const meetingCourseCode = String(meeting.course_code || "")
          .trim()
          .toLowerCase();

        console.log("[Edit Schedule] Searching class:", {
          meetingProgramId,
          meetingSetName,
          meetingCourseCode,
        });

        // =========================================================
        // FIRST: USE CLASS ID IF IT ALREADY EXISTS
        // =========================================================
        let matchedSection = null;

        const directClassId =
          meeting.class_id ||
          meeting.classId ||
          meeting.class?.class_id ||
          null;

        if (directClassId) {
          matchedSection = sections.find(
            (section) =>
              Number(section.class_id || section.id) === Number(directClassId),
          );
        }

        // =========================================================
        // SECOND: MATCH PROGRAM + SECTION
        // =========================================================
        if (!matchedSection && sections.length) {
          matchedSection = sections.find((section) => {
            const sectionProgramId = Number(
              section.program_id || section.program?.program_id || 0,
            );

            const sectionSetName = String(section.set_name || "")
              .trim()
              .toLowerCase();

            return (
              sectionProgramId === meetingProgramId &&
              sectionSetName === meetingSetName
            );
          });
        }

        // =========================================================
        // THIRD: MATCH PROGRAM + SECTION + COURSE
        //
        // This is the safest fallback when multiple sections
        // have the same course.
        // =========================================================
        if (!matchedSection && sections.length) {
          matchedSection = sections.find((section) => {
            const sectionProgramId = Number(
              section.program_id || section.program?.program_id || 0,
            );

            const sectionSetName = String(section.set_name || "")
              .trim()
              .toLowerCase();

            const sectionCourseCode = String(
              section.course_code || section.course?.course_code || "",
            )
              .trim()
              .toLowerCase();

            return (
              sectionProgramId === meetingProgramId &&
              sectionSetName === meetingSetName &&
              sectionCourseCode === meetingCourseCode
            );
          });
        }

        // =========================================================
        // RESOLVE FINAL CLASS ID
        // =========================================================
        const classId = Number(
          directClassId || matchedSection?.class_id || matchedSection?.id || 0,
        );

        console.log("[Edit Schedule] RESOLVED CLASS:", {
          classId,
          matchedSection,
          courseCode: meetingCourseCode,
          setName: meetingSetName,
          programId: meetingProgramId,
        });

        if (!classId) {
          console.error("[Edit Schedule] Unable to resolve class_id.", {
            meeting,
            matchedSection,
            sectionsCount: sections.length,
          });

          toast.error(
            `Unable to identify class section ${meeting.set_name || ""}.`,
          );

          return;
        }

        // =========================================================
        // 4. GET CLASS OWNERSHIP DATA
        // =========================================================
        const finalProgramId =
          meeting.class_program_id ||
          meeting.program_id ||
          matchedSection?.program_id ||
          matchedSection?.program?.program_id ||
          null;

        const finalInstituteId =
          meeting.class_institute_id ||
          meeting.institute_id ||
          matchedSection?.institute_id ||
          matchedSection?.program?.institute_id ||
          null;

        const finalCourseId =
          meeting.course_id ||
          matchedSection?.course_id ||
          matchedSection?.course?.course_id ||
          null;

        const finalCourseCode =
          meeting.course_code ||
          matchedSection?.course_code ||
          matchedSection?.course?.course_code ||
          "";

        const finalSetName = meeting.set_name || matchedSection?.set_name || "";

        const finalClassSize =
          meeting.class_size ||
          matchedSection?.class_size ||
          matchedSection?.class?.class_size ||
          null;

        // =========================================================
        // 5. PARSE HOURS
        // =========================================================
        const hoursText = String(meeting.hours || "");

        const lectureMatch = hoursText.match(/(\d+(?:\.\d+)?)\s*h\s*lec/i);

        const laboratoryMatch = hoursText.match(/(\d+(?:\.\d+)?)\s*h\s*lab/i);

        const lectureHours = lectureMatch ? Number(lectureMatch[1]) : 0;

        const laboratoryHours = laboratoryMatch
          ? Number(laboratoryMatch[1])
          : 0;

        console.log("[Edit Schedule] Parsed hours:", {
          lectureHours,
          laboratoryHours,
        });

        // =========================================================
        // 5.5. CAMPUS / COLLEGE BRANCH
        // =========================================================
        const incomingCollegeBranchId =
          meeting.college_branch_id ??
          matchedSection?.college_branch_id ??
          matchedSection?.collegeBranch?.college_branch_id ??
          null;

        const collegeBranchId =
          incomingCollegeBranchId !== null &&
          incomingCollegeBranchId !== undefined &&
          incomingCollegeBranchId !== ""
            ? Number(incomingCollegeBranchId)
            : null;

        const collegeBranchName =
          meeting.college_branch_name ||
          matchedSection?.college_branch_name ||
          matchedSection?.collegeBranch?.college_branch_name ||
          this.getCollegeBranchName(collegeBranchId) ||
          "";

        console.log("[Edit Schedule] RECEIVED CAMPUS:", {
          college_branch_id: collegeBranchId,
          college_branch_name: collegeBranchName,
        });

        // =========================================================
        // 6. CREATE BASE RECORD
        // =========================================================
        const recordsToAdd = [];

        const baseTempId = `temp-unscheduled-${
          meeting.id || classId
        }-${Date.now()}`;

        const baseRecord = {
          ...JSON.parse(JSON.stringify(meeting)),

          // =======================================================
          // ACTUAL CLASS
          // =======================================================
          class_id: classId,

          tempId: baseTempId,

          isNew: true,
          isUnscheduledAssignment: true,

          // =======================================================
          // SELECTED FACULTY
          // =======================================================
          faculty_name: selectedFacultyName,

          faculty_id: selectedFacultyId,

          selected_faculty_name: selectedFacultyName,

          selected_faculty_id: selectedFacultyId,

          // =======================================================
          // CLASS OWNERSHIP
          // =======================================================
          program_id: finalProgramId,

          institute_id: finalInstituteId,

          program_code:
            meeting.program_code ||
            matchedSection?.program_code ||
            matchedSection?.program?.program_code ||
            "",

          // =======================================================
          // COURSE
          // =======================================================
          course_id: finalCourseId,

          course_code: finalCourseCode,

          // =======================================================
          // SECTION
          // =======================================================
          set_name: finalSetName,

          class_size: finalClassSize,

          // =======================================================
          // CAMPUS / COLLEGE BRANCH
          // =======================================================
          college_branch_id: collegeBranchId,

          college_branch_name: collegeBranchName,

          // =======================================================
          // SCHOOL YEAR / SEMESTER
          // =======================================================
          school_year:
            meeting.school_year || this.activeSchoolYear?.school_year,

          semester: meeting.semester || this.activeSchoolYear?.semester,

          // =======================================================
          // ROOM
          // =======================================================
          room_id: null,

          room_name: "",

          room_type: "",

          room_capacity: null,

          // =======================================================
          // DEFAULT POSITION
          // =======================================================
          day: "Monday",

          start_hour: 7,

          // =======================================================
          // SEARCH FIELDS
          // =======================================================
          searchRoomQuery: "",

          showRoomDropdown: false,

          searchCourseQuery: finalCourseCode,

          showCourseDropdown: false,

          searchSectionQuery: finalSetName,

          showSectionDropdown: false,

          // IMPORTANT FOR CAMPUS DISPLAY
          searchCampusQuery: collegeBranchName,

          showCampusDropdown: false,
        };

        console.log("[Edit Schedule] BASE RECORD:", baseRecord);

        // =========================================================
        // 7. LECTURE RECORD
        // =========================================================
        if (lectureHours > 0) {
          recordsToAdd.push({
            ...baseRecord,

            tempId: `${baseTempId}-lecture`,

            type: "Lecture",

            duration: lectureHours,

            hours: `${lectureHours}h lec`,

            time_slot: `${this.formatTime(
              baseRecord.start_hour,
            )} - ${this.formatTime(baseRecord.start_hour + lectureHours)}`,
          });
        }

        // =========================================================
        // 8. LABORATORY RECORD
        // =========================================================
        if (laboratoryHours > 0) {
          const labStart = Number(baseRecord.start_hour) + lectureHours;

          recordsToAdd.push({
            ...baseRecord,

            tempId: `${baseTempId}-laboratory`,

            type: "Laboratory",

            duration: laboratoryHours,

            hours: `${laboratoryHours}h lab`,

            start_hour: labStart,

            time_slot: `${this.formatTime(labStart)} - ${this.formatTime(
              labStart + laboratoryHours,
            )}`,
          });
        }

        // =========================================================
        // 9. FALLBACK
        // =========================================================
        if (!recordsToAdd.length) {
          const duration = this.getUnscheduledDuration(meeting);

          recordsToAdd.push({
            ...baseRecord,

            tempId: `${baseTempId}-lecture`,

            type: "Lecture",

            duration,

            time_slot: `${this.formatTime(
              baseRecord.start_hour,
            )} - ${this.formatTime(baseRecord.start_hour + duration)}`,
          });
        }

        // =========================================================
        // 10. IMPORTANT VALIDATION
        //
        // Every generated record MUST belong to the selected
        // faculty and actual class.
        // =========================================================
        recordsToAdd.forEach((record) => {
          record.faculty_name = selectedFacultyName;

          record.faculty_id = selectedFacultyId;

          record.class_id = classId;

          record.program_id = finalProgramId;

          record.institute_id = finalInstituteId;

          record.course_id = finalCourseId;

          record.course_code = finalCourseCode;

          record.set_name = finalSetName;

          // =======================================================
          // CAMPUS / COLLEGE BRANCH
          // =======================================================
          record.college_branch_id = collegeBranchId;

          record.college_branch_name = collegeBranchName;

          record.searchCampusQuery = collegeBranchName;

          record.showCampusDropdown = false;

          record.isNew = true;

          record.isUnscheduledAssignment = true;
        });

        // =========================================================
        // 11. ADD ONLY TO SELECTED FACULTY CALENDAR
        // =========================================================
        this.localData.push(...recordsToAdd);

        console.log("[Edit Schedule] Added unscheduled records:", recordsToAdd);

        // =========================================================
        // 12. SELECT FIRST RECORD
        // =========================================================
        this.expandedRecord = recordsToAdd[0];

        this.highlightedRecordId = recordsToAdd[0].tempId;

        // =========================================================
        // 13. OPEN EDIT SCHEDULE
        // =========================================================
        this.showAddPanel = true;

        this.showUnscheduledPanel = false;

        await this.$nextTick();

        // =========================================================
        // 14. FINAL VALIDATION LOG
        // =========================================================
        console.log("[Edit Schedule] FINAL ASSIGNMENT:", {
          faculty_name: selectedFacultyName,

          faculty_id: selectedFacultyId,

          class_id: classId,

          program_id: finalProgramId,

          institute_id: finalInstituteId,

          course_id: finalCourseId,

          course_code: finalCourseCode,

          set_name: finalSetName,

          records: recordsToAdd,
        });

        console.log(
          "[Edit Schedule] Lecture/Lab records:",
          this.localData.filter(
            (record) =>
              record.isUnscheduledAssignment &&
              Number(record.class_id) === Number(classId) &&
              normalizeName(record.faculty_name) ===
                normalizeName(selectedFacultyName),
          ),
        );
      },
    },
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
            searchCampusQuery:
              rec.college_branch_name ||
              this.getCollegeBranchName(rec.college_branch_id) ||
              "",
            showCampusDropdown: false,

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
    // ============================================================
    // ROOM MAP
    // ============================================================

    openRoomMap() {
      if (!this.expandedRecord) {
        return;
      }

      if (!this.canEditSchedule(this.expandedRecord)) {
        return;
      }

      // Close normal room dropdown
      this.expandedRecord.showRoomDropdown = false;

      // DEBUG
      console.log("[Room Map] Expanded Record:", this.expandedRecord);
      console.log(
        "[Room Map] Filtered Rooms:",
        this.filteredRooms(this.expandedRecord),
      );

      // Open map
      this.showRoomMap = true;
    },
    selectRoomFromMap(room) {
      if (!this.expandedRecord || !room) {
        return;
      }

      // Use the EXISTING room selection logic
      this.selectRoom(this.expandedRecord, room);

      // Close map
      this.showRoomMap = false;
    },

    closeRoomMap() {
      this.showRoomMap = false;
    },
    getUnscheduledDuration(meeting) {
      const hours = String(meeting.hours || "");

      const lec = hours.match(/(\d+(?:\.\d+)?)h\s*lec/i);
      const lab = hours.match(/(\d+(?:\.\d+)?)h\s*lab/i);

      if (lec) return Number(lec[1]);
      if (lab) return Number(lab[1]);

      return 3;
    },
    ...mapActions(useFetchDataStore, [
      "fetchRooms",
      "fetchCurriculumCourses",
      "fetchClassSections",
      "fetchRawUsers",
      "fetchAllSchoolYears",
    ]),
    async getCurrentSchoolYear() {
      const store = useFetchDataStore();

      if (!store.all_school_years?.length) {
        await this.fetchAllSchoolYears();
      }

      const active = [...(store.all_school_years || [])]
        .filter((s) => s.is_active)
        .sort(
          (a, b) =>
            new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime(),
        );

      if (!active.length) {
        throw new Error("No active school year found.");
      }

      return {
        school_year: active[0].school_year_name,
        semester: active[0].semester,
      };
    },
    async cancelEdit() {
      try {
        // -----------------------------------------
        // CANCEL SPLIT CHANGES
        // -----------------------------------------

        const splitRecords = this.localData.filter((r) => r.isSplitRecord);

        if (splitRecords.length) {
          splitRecords.forEach((splitRecord) => {
            const parent = this.localData.find(
              (r) => (r.id || r.tempId) === splitRecord.splitParentId,
            );

            if (parent?._splitOriginal) {
              parent.duration = parent._splitOriginal.duration;

              parent.start_hour = parent._splitOriginal.start_hour;

              parent.time_slot = parent._splitOriginal.time_slot;

              delete parent._splitOriginal;
            }
          });

          this.localData = this.localData.filter((r) => !r.isSplitRecord);
        }

        // -----------------------------------------
        // RESTORE UNSCHEDULED MEETINGS
        // -----------------------------------------
        if (this.restoredUnscheduledMeetings.length) {
          // Group the original records back into their
          // original unscheduled meeting.
          const grouped = {};

          this.restoredUnscheduledMeetings.forEach((meeting) => {
            const key =
              meeting.unscheduled_id ||
              `${meeting.class_id}-${meeting.course_code}`;

            if (!grouped[key]) {
              grouped[key] = {
                ...JSON.parse(JSON.stringify(meeting)),
                type: "",
                lectureHours: 0,
                laboratoryHours: 0,
              };
            }

            const type = String(meeting.type || "").toLowerCase();

            if (type === "lecture") {
              grouped[key].lectureHours += Number(meeting.duration || 0);
            }

            if (type === "laboratory") {
              grouped[key].laboratoryHours += Number(meeting.duration || 0);
            }
          });

          const payload = Object.values(grouped).map((meeting) => {
            let type = "";

            if (meeting.lectureHours > 0 && meeting.laboratoryHours > 0) {
              type = "Lecture+Lab";
            } else if (meeting.lectureHours > 0) {
              type = "Lecture";
            } else if (meeting.laboratoryHours > 0) {
              type = "Laboratory";
            }

            const restored = {
              class_id: meeting.class_id,
              course_code: meeting.course_code,
              course_id: meeting.course_id,
              class_size: meeting.class_size,
              faculty_name: meeting.faculty_name,
              program_id: meeting.program_id,
              program_code: meeting.program_code,
              type,
              hours: meeting.hours,
              reason: meeting.reason,
              school_year: meeting.school_year,
              semester: meeting.semester,
            };

            return restored;
          });

          console.log(
            "[Cancel Edit] Restoring grouped unscheduled meetings:",
            payload,
          );

          const response = await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/unscheduled-meetings/add-unscheduled-meetings`,
            {
              meetings: payload,
              restore: true,
            },
          );

          console.log("[Cancel Edit] Restore response:", response.data);

          // Remove the temporary schedules from calendar
          this.localData = this.localData.filter(
            (r) =>
              !this.restoredUnscheduledMeetings.some(
                (u) =>
                  String(u.class_id) === String(r.class_id) &&
                  String(u.course_code) === String(r.course_code) &&
                  r.isNew,
              ),
          );
        }

        // -----------------------------------------
        // HANDLE MANUALLY ADDED SCHEDULES
        // -----------------------------------------

        const manualAddedSchedules = this.localData.filter(
          (r) =>
            r.isNew &&
            !this.restoredUnscheduledMeetings.some(
              (u) =>
                String(u.class_id) === String(r.class_id) &&
                String(u.course_code) === String(r.course_code),
            ),
        );

        if (manualAddedSchedules.length) {
          const grouped = {};

          manualAddedSchedules.forEach((r) => {
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

              hours =
                `${g.lecture.toFixed(1)}h lec + ` +
                `${g.laboratory.toFixed(1)}h lab per week`;
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

          await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/unscheduled-meetings/add-unscheduled-meetings`,
            payload,
          );
        }

        // -----------------------------------------
        // DELETE TEMPORARY SAVED SCHEDULES
        // -----------------------------------------

        await Promise.all(
          this.localData
            .filter((r) => r.isNew && r.id)
            .map((r) =>
              axios.delete(
                `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${r.id}`,
              ),
            ),
        );

        // -----------------------------------------
        // RESET
        // -----------------------------------------

        this.restoredUnscheduledMeetings = [];

        this.localData = this.localData.filter((r) => !r.isNew);

        this.expandedRecord = null;
        this.highlightedRecordId = null;

        this.showAddPanel = false;
        this.showUnscheduledPanel = false;

        this.selectedInstructorName = "";

        this.$emit("close");
      } catch (err) {
        console.error("[Cancel Edit] Failed:", err.response?.data || err);

        toast.error("Failed to cancel changes.");
      }
    },
    getAllSchedulesForConflict(record) {
      if (!record) return [];

      const scheduleMap = new Map();

      // -----------------------------------------
      // 1. ADD ORIGINAL DATABASE SCHEDULES
      // -----------------------------------------
      (this.fullSchedules || []).forEach((schedule) => {
        const key =
          schedule.id != null
            ? `id-${schedule.id}`
            : schedule.tempId
            ? `temp-${schedule.tempId}`
            : null;

        if (!key) return;

        scheduleMap.set(key, schedule);
      });

      // -----------------------------------------
      // 2. LOCAL DATA OVERRIDES ORIGINAL DATA
      // -----------------------------------------
      (this.localData || []).forEach((schedule) => {
        const key =
          schedule.id != null
            ? `id-${schedule.id}`
            : schedule.tempId
            ? `temp-${schedule.tempId}`
            : null;

        if (!key) return;

        // IMPORTANT:
        // The edited local version replaces the
        // original fullSchedules version.
        scheduleMap.set(key, schedule);
      });

      // -----------------------------------------
      // 3. FILTER SCHOOL YEAR + SEMESTER
      // -----------------------------------------
      return Array.from(scheduleMap.values()).filter(
        (schedule) =>
          String(schedule.school_year).trim() ===
            String(record.school_year).trim() &&
          Number(schedule.semester) === Number(record.semester),
      );
    },
    async fetchCollegeBranch() {
      const store = useFetchDataStore();
      await store.fetchCollegeBranch();

      this.college_branch = store.college_branch || [];
    },
    getCollegeBranchName(branchId) {
      if (!branchId) return "";

      const id = Number(branchId);

      // First: use fetched college_branch data
      const branch = (this.college_branch || []).find(
        (b) => Number(b.college_branch_id) === id,
      );

      if (branch?.college_branch_name) {
        return branch.college_branch_name;
      }

      // Fallback: get the name from rooms -> building -> buildingArea -> collegeBranch
      const campus = (this.rooms || [])
        .map((room) => room.building?.buildingArea?.collegeBranch)
        .find((b) => Number(b?.college_branch_id) === id);

      return campus?.college_branch_name || "";
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

      if (!Array.isArray(courses) || !courses.length) {
        return;
      }

      let selectedRecord = null;

      courses.forEach((course, index) => {
        // Keep original unscheduled record for Cancel
        this.restoredUnscheduledMeetings.push(
          JSON.parse(JSON.stringify(course)),
        );

        const tempId = `temp-${Date.now()}-${Math.floor(
          Math.random() * 100000,
        )}`;

        // =========================================================
        // FACULTY
        // =========================================================
        const facultyName =
          course.faculty_name || this.selectedInstructorName || "TBD";

        const faculty = (this.rawusers || []).find(
          (u) =>
            `${u.first_name} ${u.last_name}`.trim().toLowerCase() ===
            String(facultyName).trim().toLowerCase(),
        );

        // =========================================================
        // CAMPUS
        // =========================================================

        // =======================================================
        // CAMPUS / COLLEGE BRANCH
        // =======================================================

        // Always receive the ID from the unscheduled payload
        const collegeBranchId =
          course.college_branch_id !== null &&
          course.college_branch_id !== undefined &&
          course.college_branch_id !== ""
            ? Number(course.college_branch_id)
            : null;

        // Resolve the name using the ID
        const collegeBranchName =
          course.college_branch_name ||
          this.getCollegeBranchName(collegeBranchId) ||
          "";

        console.log("[Edit Schedule] UNSCHEDULED CAMPUS:", {
          college_branch_id: collegeBranchId,
          college_branch_name: collegeBranchName,
        });
        // =========================================================
        // NEW RECORD
        // =========================================================
        const newRecord = {
          ...JSON.parse(JSON.stringify(course)),

          tempId,
          isNew: true,
          isUnscheduledAssignment: true,

          // Faculty
          faculty_name: facultyName,

          faculty_id:
            course.faculty_id || faculty?.id || faculty?.user_id || null,

          // Section
          searchSectionQuery: course.set_name || "",
          showSectionDropdown: false,

          // Course
          searchCourseQuery: course.course_code || "",
          showCourseDropdown: false,

          // =====================================================
          // CAMPUS
          // =====================================================
          college_branch_id: collegeBranchId,

          college_branch_name: collegeBranchName,

          // IMPORTANT:
          // This is what the Campus input displays
          searchCampusQuery: collegeBranchName,

          showCampusDropdown: false,

          // Room
          searchRoomQuery: course.room_name || "",
          showRoomDropdown: false,

          // School Year / Semester
          school_year: this.activeSchoolYear?.school_year || course.school_year,

          semester: this.activeSchoolYear?.semester || course.semester,
        };

        // =========================================================
        // DEBUG
        // =========================================================
        console.log("[Unscheduled] Campus assigned:", {
          college_branch_id: newRecord.college_branch_id,
          college_branch_name: newRecord.college_branch_name,
          searchCampusQuery: newRecord.searchCampusQuery,
        });

        // =========================================================
        // ADD TO LOCAL DATA
        // =========================================================
        this.localData.push(newRecord);

        // First record = selected record
        if (index === 0) {
          selectedRecord = newRecord;
        }
      });

      // ===========================================================
      // SELECTED FACULTY
      // ===========================================================
      this.selectedInstructorName =
        selectedRecord?.faculty_name || this.selectedInstructorName;

      // ===========================================================
      // CLOSE UNSCHEDULED PANEL
      // ===========================================================
      this.showUnscheduledPanel = false;

      // ===========================================================
      // OPEN EDIT SCHEDULE PANEL
      // ===========================================================
      this.showAddPanel = true;

      // ===========================================================
      // DISPLAY SELECTED RECORD
      // ===========================================================
      this.expandedRecord = selectedRecord;

      // ===========================================================
      // HIGHLIGHT
      // ===========================================================
      this.highlightedRecordId = selectedRecord?.id || selectedRecord?.tempId;

      console.log("[Unscheduled] FINAL selected record:", this.expandedRecord);

      toast.success(
        `${courses.length} course(s) assigned to ${this.selectedInstructorName}.`,
      );
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

      this.tooltipItem = item;
      this.scheduleTooltipVisible = true;

      this.$nextTick(() => {
        const scheduleElement = event.currentTarget;

        if (!scheduleElement) return;

        const rect = scheduleElement.getBoundingClientRect();

        const tooltipWidth = 280;
        const tooltipHeight = 300; // estimated maximum height
        const gap = 8;

        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;

        let left;
        let top;

        // -----------------------------------------
        // HORIZONTAL POSITION
        // -----------------------------------------

        // Default: right side of schedule
        left = rect.right + gap;

        // If there is not enough space on the right,
        // display on the LEFT side
        if (left + tooltipWidth > viewportWidth - gap) {
          left = rect.left - tooltipWidth - gap;
        }

        // Make sure it does not go outside left side
        if (left < gap) {
          left = gap;
        }

        // -----------------------------------------
        // VERTICAL POSITION
        // -----------------------------------------

        // Default: below the schedule
        top = rect.bottom + gap;

        // If tooltip would go below viewport,
        // move it ABOVE the schedule
        if (top + tooltipHeight > viewportHeight - gap) {
          top = rect.top - tooltipHeight - gap;
        }

        // If it would go above viewport,
        // clamp it to the top
        if (top < gap) {
          top = gap;
        }

        this.tooltipX = left;
        this.tooltipY = top;
      });
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

      // Automatically open the Add Panel
      this.showAddPanel = true;
      this.showUnscheduledPanel = false;
      // Automatically display the selected schedule
      this.expandedRecord = item;

      this.$nextTick(() => {
        const el = document.getElementById(`row-${this.highlightedRecordId}`);

        if (el) {
          el.scrollIntoView({
            behavior: "smooth",
            block: "center",
          });
        }
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

              searchCampusQuery:
                cloned.college_branch_name ||
                this.getCollegeBranchName(cloned.college_branch_id) ||
                "",
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

          searchCampusQuery:
            cloned.college_branch_name ||
            this.getCollegeBranchName(cloned.college_branch_id) ||
            "",
          showCampusDropdown: false,
        };
      });

      this.draggedRecord = null;
    },
    async openAddSchedulePanel(instructor) {
      this.selectedInstructorName = instructor;

      // Close the unscheduled panel
      this.showUnscheduledPanel = false;

      // Open the add panel
      this.showAddPanel = true;

      // Clear any previous unscheduled selection
      this.expandedRecord = null;

      await this.$nextTick();

      this.addNewRow();
    },
    openUnscheduledPanel(instructor) {
      this.selectedInstructorName = instructor;

      // Hide Add Schedule panel
      this.showAddPanel = false;

      // Show only Unscheduled panel
      this.showUnscheduledPanel = true;

      // Optional: clear any selected schedule
      this.expandedRecord = null;
    },

    closeAddSchedulePanel() {
      this.showAddPanel = false;
      this.showUnscheduledPanel = false;
    },

    /* ------------------ 3. FILTERING ------------------ */
    isLectureRoom(room) {
      const type = String(room?.room_type || "")
        .trim()
        .toLowerCase();

      return (
        type.includes("lecture") || type.includes("lec") || type === "classroom"
      );
    },

    isLaboratoryRoom(room) {
      const type = String(room?.room_type || "")
        .trim()
        .toLowerCase();

      return type.includes("laboratory") || type.includes("lab");
    },

    getRoomTypeLabel(roomType) {
      const type = String(roomType || "")
        .trim()
        .toLowerCase();

      if (type.includes("lab") || type.includes("laboratory")) {
        return "LAB";
      }

      if (
        type.includes("lecture") ||
        type.includes("lec") ||
        type === "classroom"
      ) {
        return "LECTURE";
      }

      return roomType || "ROOM";
    },

    getRoomTypeBadgeClass(roomType) {
      const type = String(roomType || "")
        .trim()
        .toLowerCase();

      if (type.includes("lab") || type.includes("laboratory")) {
        return "bg-purple-100 text-purple-700 border border-purple-200";
      }

      if (
        type.includes("lecture") ||
        type.includes("lec") ||
        type === "classroom"
      ) {
        return "bg-blue-100 text-blue-700 border border-blue-200";
      }

      return "bg-gray-100 text-gray-600 border border-gray-200";
    },
    filteredRooms(record) {
      let rooms = [...(this.rooms || [])];

      // ============================================================
      // 1. FILTER BY CAMPUS
      // ============================================================
      const selectedCampusId = Number(record?.college_branch_id);

      if (selectedCampusId) {
        rooms = rooms.filter((room) => {
          const roomCampusId = Number(
            room?.building?.buildingArea?.collegeBranch?.college_branch_id,
          );

          return roomCampusId === selectedCampusId;
        });
      }

      // ============================================================
      // 2. COURSE REQUIREMENTS
      // ============================================================
      let courseLec = Number(record?.course_lec || 0);
      let courseLab = Number(record?.course_lab || 0);

      // Existing schedule may not contain course_lec/course_lab
      if (courseLec === 0 && courseLab === 0 && record?.course_id) {
        const selectedCourse = this.coursesList.find(
          (course) => Number(course.course_id) === Number(record.course_id),
        );

        if (selectedCourse) {
          courseLec = Number(selectedCourse.course_lec || 0);
          courseLab = Number(selectedCourse.course_lab || 0);
        }
      }

      // ============================================================
      // 3. CURRENT SCHEDULE TYPE
      // ============================================================
      const scheduleType = String(record?.type || "")
        .trim()
        .toLowerCase();

      // ============================================================
      // 4. CURRENT LOGGED-IN USER INSTITUTE
      // ============================================================
      const currentUserInstituteId = Number(this.user?.institute_id);

      // ============================================================
      // 5. GET ROOM INSTITUTE
      // ============================================================
      const getRoomInstituteId = (room) => {
        return Number(
          room?.institute_id ??
            room?.institute?.institute_id ??
            room?.building?.institute_id ??
            room?.building?.institute?.institute_id ??
            room?.building?.buildingArea?.institute_id ??
            room?.building?.buildingArea?.institute?.institute_id ??
            null,
        );
      };

      // ============================================================
      // 6. LABORATORY
      // ============================================================
      if (
        scheduleType === "laboratory" ||
        scheduleType.includes("laboratory") ||
        scheduleType === "lab"
      ) {
        // ONLY LABORATORY ROOMS
        rooms = rooms.filter((room) => this.isLaboratoryRoom(room));

        // ==========================================================
        // IMPORTANT:
        // LABORATORY ROOMS MUST BELONG TO
        // THE CURRENT LOGGED-IN USER'S INSTITUTE
        // ==========================================================
        if (currentUserInstituteId > 0) {
          rooms = rooms.filter((room) => {
            const roomInstituteId = getRoomInstituteId(room);

            return roomInstituteId === currentUserInstituteId;
          });
        }
      }

      // ============================================================
      // 7. LECTURE
      // ============================================================
      else if (
        scheduleType === "lecture" ||
        scheduleType.includes("lecture") ||
        scheduleType === "lec"
      ) {
        // Lecture rooms:
        // Campus + Lecture type only
        rooms = rooms.filter((room) => this.isLectureRoom(room));
      }

      // ============================================================
      // 8. FALLBACK WHEN RECORD TYPE IS EMPTY
      // ============================================================
      else {
        // ----------------------------------------------------------
        // LECTURE ONLY
        // ----------------------------------------------------------
        if (courseLec > 0 && courseLab === 0) {
          rooms = rooms.filter((room) => this.isLectureRoom(room));
        }

        // ----------------------------------------------------------
        // LAB ONLY
        // ----------------------------------------------------------
        else if (courseLec === 0 && courseLab > 0) {
          rooms = rooms.filter((room) => this.isLaboratoryRoom(room));

          // Laboratory must belong to logged-in user's institute
          if (currentUserInstituteId > 0) {
            rooms = rooms.filter((room) => {
              const roomInstituteId = getRoomInstituteId(room);

              return roomInstituteId === currentUserInstituteId;
            });
          }
        }

        // ----------------------------------------------------------
        // BOTH LECTURE + LAB
        // ----------------------------------------------------------
        else if (courseLec > 0 && courseLab > 0) {
          // The schedule must specify whether it is
          // Lecture or Laboratory.
          rooms = [];
        }
      }

      // ============================================================
      // 9. ROOM SEARCH
      // ============================================================
      const query = String(record?.searchRoomQuery || "")
        .trim()
        .toLowerCase();

      if (query) {
        rooms = rooms.filter((room) =>
          String(room?.room_name || "")
            .toLowerCase()
            .includes(query),
        );
      }

      // ============================================================
      // 10. RETURN FILTERED ROOMS
      // ============================================================
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
    async selectCourse(record, curriculumCourse) {
      const course = curriculumCourse.course;
      const curriculum = curriculumCourse.curriculum;

      record.course_id = course.course_id;
      record.course_code = course.course_code;

      // IMPORTANT: store course requirements
      record.course_lec = Number(course.course_lec || 0);
      record.course_lab = Number(course.course_lab || 0);

      const currentSchoolYear = await this.getCurrentSchoolYear();

      record.school_year = currentSchoolYear.school_year;
      record.semester = String(currentSchoolYear.semester);

      record.program_id = curriculum?.program_id || null;
      record.program_code = curriculum?.program?.program_code || "";
      record.institute_id = curriculum?.institute_id || null;

      record.searchCourseQuery = course.course_code;
      record.showCourseDropdown = false;

      // Reset room because the required room type may change
      record.room_id = null;
      record.room_name = "";
      record.room_type = "";
      record.room_capacity = null;
      record.searchRoomQuery = "";
    },
    /* ------------------ 5. ROW MANAGEMENT ------------- */

    async addNewRow() {
      const currentSchoolYear = await this.getCurrentSchoolYear();
      this.closeAddSchedulePanel(); // closes both panels
      this.expandedRecord = true;
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
        school_year: currentSchoolYear.school_year,
        semester: currentSchoolYear.semester.toString(),

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
      // Remove all newly added rows
      this.localData = this.localData.filter((record) => !record.isNew);

      // Clear selected record
      this.expandedRecord = null;
      this.highlightedRecordId = null;

      // Close the right panel
      this.showAddPanel = false;
      this.showUnscheduledPanel = false;

      // Reset instructor
      this.selectedInstructorName = "";
    },
    toggleDelete() {
      this.deleteTarget = this.expandedRecord;
      this.showConfirmDelete = true;
    },

    cancelDelete() {
      this.showConfirmDelete = false;
      this.deleteTarget = null;
    },
    async confirmDelete() {
      if (!this.deleteTarget) return;

      // New row - not yet saved
      if (this.deleteTarget.isNew || !this.deleteTarget.id) {
        this.localData = this.localData.filter(
          (r) =>
            (r.id || r.tempId) !==
            (this.deleteTarget.id || this.deleteTarget.tempId),
        );

        this.expandedRecord = null;
        this.highlightedRecordId = null;
        this.showConfirmDelete = false;
        this.deleteTarget = null;

        toast.success("Schedule removed.");
        return;
      }

      try {
        this.deleting = true;

        await axios.delete(
          `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${this.deleteTarget.id}`,
        );

        this.localData = this.localData.filter(
          (item) => item.id !== this.deleteTarget.id,
        );

        this.expandedRecord = null;
        this.highlightedRecordId = null;

        toast.success("Schedule deleted successfully.");
      } catch (error) {
        console.error(error);
        toast.error("Failed to delete schedule.");
      } finally {
        this.deleting = false;
        this.showConfirmDelete = false;
        this.deleteTarget = null;
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

      // -----------------------------------------
      // USE EDIT SCHEDULE DATA
      // -----------------------------------------
      const sourceSchedules = this.getAllSchedulesForConflict(record);

      return sourceSchedules
        .filter((r) => {
          if (!r) return false;

          // -----------------------------------------
          // DON'T COMPARE THE RECORD WITH ITSELF
          // -----------------------------------------
          const sameId =
            record.id != null &&
            r.id != null &&
            String(record.id) === String(r.id);

          const sameTempId =
            record.tempId != null &&
            r.tempId != null &&
            String(record.tempId) === String(r.tempId);

          if (sameId || sameTempId) {
            return false;
          }

          // -----------------------------------------
          // SAME JOIN GROUP = NOT A CONFLICT
          // -----------------------------------------
          if (
            record.join_group_id &&
            r.join_group_id &&
            Number(record.join_group_id) === Number(r.join_group_id)
          ) {
            return false;
          }

          // -----------------------------------------
          // SAME DAY ONLY
          // -----------------------------------------
          if (r.day !== record.day) {
            return false;
          }

          // -----------------------------------------
          // VALID TIME
          // -----------------------------------------
          if (r.start_hour == null || r.duration == null) {
            return false;
          }

          const rStart = Number(r.start_hour);
          const rEnd = rStart + Number(r.duration);

          // -----------------------------------------
          // TIME OVERLAP
          // -----------------------------------------
          const overlaps =
            Math.max(recordStart, rStart) < Math.min(recordEnd, rEnd);

          if (!overlaps) {
            return false;
          }

          // -----------------------------------------
          // SAME FACULTY
          // -----------------------------------------
          const sameFaculty =
            (r.faculty_id &&
              record.faculty_id &&
              Number(r.faculty_id) === Number(record.faculty_id)) ||
            (r.faculty_name &&
              record.faculty_name &&
              r.faculty_name.trim().toLowerCase() ===
                record.faculty_name.trim().toLowerCase());

          // -----------------------------------------
          // SAME ROOM
          // -----------------------------------------
          const sameRoom =
            (record.mode || "").toLowerCase() === "face to face" &&
            (r.mode || "").toLowerCase() === "face to face" &&
            r.room_id &&
            record.room_id &&
            Number(r.room_id) === Number(record.room_id);

          // -----------------------------------------
          // SAME CLASS
          // -----------------------------------------
          const sameClass =
            record.class_id &&
            r.class_id &&
            Number(r.class_id) === Number(record.class_id);

          // -----------------------------------------
          // SAME ONLINE SECTION
          // -----------------------------------------
          const sameOnlineSection =
            (record.mode || "").toLowerCase() === "online" &&
            (r.mode || "").toLowerCase() === "online" &&
            r.set_name === record.set_name &&
            Number(r.program_id) === Number(record.program_id) &&
            Number(r.college_branch_id) === Number(record.college_branch_id);

          return sameFaculty || sameRoom || sameClass || sameOnlineSection;
        })
        .map((r) => {
          const reasons = [];

          // -----------------------------------------
          // FACULTY CONFLICT
          // -----------------------------------------
          const sameFaculty =
            (record.faculty_id &&
              r.faculty_id &&
              Number(record.faculty_id) === Number(r.faculty_id)) ||
            (record.faculty_name &&
              r.faculty_name &&
              record.faculty_name.trim().toLowerCase() ===
                r.faculty_name.trim().toLowerCase());

          if (sameFaculty) {
            reasons.push(
              `Faculty "${
                r.faculty_name
              }" is already assigned from ${this.formatTime(
                r.start_hour,
              )} to ${this.formatTime(r.start_hour + Number(r.duration))}.`,
            );
          }

          // -----------------------------------------
          // ROOM CONFLICT
          // -----------------------------------------
          const sameRoom =
            (record.mode || "").toLowerCase() === "face to face" &&
            (r.mode || "").toLowerCase() === "face to face" &&
            r.room_id &&
            record.room_id &&
            Number(r.room_id) === Number(record.room_id);

          if (sameRoom) {
            reasons.push(
              `Room "${r.room_name}" is already occupied by ${r.course_code} (${
                r.program_code
              }-${r.set_name}) from ${this.formatTime(
                r.start_hour,
              )} to ${this.formatTime(r.start_hour + Number(r.duration))}.`,
            );
          }

          // -----------------------------------------
          // CLASS CONFLICT
          // -----------------------------------------
          if (
            record.class_id &&
            r.class_id &&
            Number(r.class_id) === Number(record.class_id)
          ) {
            reasons.push(
              `Section ${r.program_code}-${r.set_name} already has a class (${r.course_code}) scheduled during this time.`,
            );
          }

          // -----------------------------------------
          // ONLINE CONFLICT
          // -----------------------------------------
          const sameOnlineSection =
            (record.mode || "").toLowerCase() === "online" &&
            (r.mode || "").toLowerCase() === "online" &&
            r.set_name === record.set_name &&
            Number(r.program_id) === Number(record.program_id) &&
            Number(r.college_branch_id) === Number(record.college_branch_id);

          if (sameOnlineSection) {
            reasons.push(
              `This online section (${r.program_code}-${r.set_name}) already has another online class during this time.`,
            );
          }

          // -----------------------------------------
          // MULTIPLE CONFLICT SUMMARY
          // -----------------------------------------
          if (reasons.length > 1) {
            reasons.unshift(`This schedule has ${reasons.length} conflicts:`);
          }

          return {
            ...r,
            reason: reasons.join("\n• "),
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
      const clonedRecord = {
        ...record,
        faculty_name: targetInstructor,
        day: targetDay,
        start_hour: Number(targetStartHour),
      };

      return this.getConflictingRecords(clonedRecord);
    },
    onDragOver(event, instructor, day, slotStart) {
      event.preventDefault();

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
      if (!record) return;

      this.isDragging = true;

      event.dataTransfer.effectAllowed = "move";

      this.hideScheduleTooltip();

      this.draggedRecord = record;

      this.dragConflictMap = {};

      Object.keys(this.groupedSchedule).forEach((faculty) => {
        this.days.forEach((day) => {
          this.timeSlots.forEach((slot) => {
            const key = `${faculty}-${day}-${slot.start}`;

            const conflicts = this.getConflictsForDrag(
              record,
              faculty,
              day,
              slot.start,
            );

            this.dragConflictMap[key] = conflicts.length > 0;
          });
        });
      });
    },
    onDragEnd() {
      this.isDragging = false;

      this.hideScheduleTooltip();

      this.draggedRecord = null;

      this.draggedGroup = [];

      this.dragConflictMap = {};

      this.conflictPreview = [];
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
        const currentSchoolYear = await this.getCurrentSchoolYear();

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

            // ALWAYS USE CURRENT ACTIVE SCHOOL YEAR
            school_year: currentSchoolYear.school_year,
            semester: String(currentSchoolYear.semester),

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
    handleScheduleKeyboard(event) {
      // Only listen for the Space key
      if (event.code !== "Space") return;

      // Don't trigger while typing in an input
      const target = event.target;

      if (
        target?.tagName === "INPUT" ||
        target?.tagName === "TEXTAREA" ||
        target?.tagName === "SELECT" ||
        target?.isContentEditable
      ) {
        return;
      }

      // Prevent the browser from scrolling when Space is pressed
      event.preventDefault();

      const now = Date.now();

      // First Space press
      if (now - this.lastSpacePressTime > this.spaceDoubleTapDelay) {
        this.lastSpacePressTime = now;
        return;
      }

      // Second Space press
      this.lastSpacePressTime = 0;

      console.log("DOUBLE SPACE DETECTED");

      // We will call the split function in the next step
      this.splitSelectedLaboratory();
    },
    splitSelectedLaboratory() {
      const record = this.expandedRecord;

      // No schedule selected
      if (!record) {
        console.log("No schedule selected.");
        return;
      }

      // Only Laboratory
      if ((record.type || "").toLowerCase() !== "laboratory") {
        toast.info("Only Laboratory schedules can be split.");
        return;
      }

      const duration = Number(record.duration);

      // Laboratory must be MORE than 3 hours
      if (!Number.isFinite(duration) || duration <= 3) {
        toast.info(
          "Only Laboratory schedules longer than 3 hours can be split.",
        );
        return;
      }

      // Check edit permission
      if (!this.canEditSchedule(record)) {
        toast.warning("You cannot edit this schedule.");
        return;
      }

      console.log("Splitting laboratory:", record);

      // Split duration into two
      const firstDuration = Number((duration / 2).toFixed(2));
      const secondDuration = Number((duration - firstDuration).toFixed(2));

      const originalStart = Number(record.start_hour);

      // Second schedule starts after the first half
      const secondStart = Number((originalStart + firstDuration).toFixed(2));

      // ------------------------------------
      // FIRST HALF
      // ------------------------------------

      // Remember the original value so Cancel can restore it
      if (!record._splitOriginal) {
        record._splitOriginal = {
          duration: duration,
          start_hour: originalStart,
          time_slot: record.time_slot,
        };
      }

      record.duration = firstDuration;

      record.time_slot = this.generateTimeSlot(
        record.start_hour,
        record.duration,
      );

      // ------------------------------------
      // SECOND HALF
      // ------------------------------------

      const secondRecord = {
        ...structuredClone(record),

        id: null,

        tempId: `split-${Date.now()}-${Math.floor(Math.random() * 10000)}`,

        start_hour: secondStart,
        duration: secondDuration,

        time_slot: this.generateTimeSlot(secondStart, secondDuration),

        isNew: true,

        // Mark this as a split-created record
        isSplitRecord: true,

        // Remember which schedule it came from
        splitParentId: record.id || record.tempId,

        split_from_id: record.id || record.tempId,
      };

      // Don't duplicate these IDs
      delete secondRecord.schedule_id;
      delete secondRecord.final_generated_id;

      // Add second schedule to local data
      this.localData.push(secondRecord);

      // Select the newly created second schedule
      this.expandedRecord = secondRecord;
      this.highlightedRecordId = secondRecord.tempId;

      // Hide tooltip
      this.hideScheduleTooltip();

      console.log("Laboratory successfully split:", {
        original: record,
        second: secondRecord,
      });

      toast.success(
        `${record.course_code || "Laboratory"} split successfully.`,
      );
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
    await this.fetchAllSchoolYears();

    // Listen for keyboard shortcuts
    window.addEventListener("keydown", this.handleScheduleKeyboard);
  },

  beforeUnmount() {
    // Remove keyboard listener when component is destroyed
    window.removeEventListener("keydown", this.handleScheduleKeyboard);
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
