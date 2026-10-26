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
              <h2 class="text-lg font-semibold text-white">
                Edit Unscheduled Classes
              </h2>

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
                    <thead class="sticky top-0 z-[10000] bg-gray-200">
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
                  <h3 class="text-lg font-semibold">
                    Update UNSCHEDULE Schedule
                  </h3>
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
                            <div v-if="filteredSectionsForExpanded.length">
                              <div
                                v-for="section in filteredSectionsForExpanded"
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
                            @input="expandedRecord.college_branch_id = null"
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
                                      .toLowerCase()
                                      .includes(
                                        (
                                          expandedRecord.searchCampusQuery || ''
                                        ).toLowerCase(),
                                      ),
                                )"
                                :key="campus.college_branch_id"
                                class="dropdown-item"
                                @mousedown.prevent="
                                  expandedRecord.college_branch_id =
                                    campus.college_branch_id;
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
                      <!-- ===================== ROOM ===================== -->
                      <div class="dropdown-container relative">
                        <label class="dropdown-label">Room :</label>

                        <div class="flex items-start gap-2">
                          <!-- ROOM SEARCH -->
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

                            <!-- ROOM DROPDOWN -->
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
                                  <div class="min-w-0">
                                    <div class="truncate font-medium">
                                      {{ room.room_name }}
                                    </div>

                                    <div class="text-[10px] text-gray-400">
                                      Capacity:
                                      {{ room.room_capacity || "-" }}
                                    </div>
                                  </div>

                                  <span
                                    class="shrink-0 inline-flex items-center px-2 py-0.5 rounded-full text-[9px] font-bold uppercase"
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
                                class="dropdown-item text-gray-400 text-center py-3"
                              >
                                No suitable room found
                              </div>
                            </div>
                          </div>

                          <!-- 2D ROOM MAP BUTTON -->
                          <button
                            type="button"
                            :disabled="!canEditSchedule(expandedRecord)"
                            class="flex h-[38px] w-[42px] shrink-0 items-center justify-center rounded-lg border border-gray-200 bg-white text-gray-600 shadow-sm transition hover:border-emerald-300 hover:bg-emerald-50 hover:text-emerald-600 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-300"
                            title="Select room from 2D map"
                            @click="openRoomMap"
                          >
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

                        <!-- SELECTED ROOM INFORMATION -->
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

  <!-- ============================================================ -->
  <!-- 2D ROOM MAP -->
  <!-- ============================================================ -->
  <RoomMapModal
    :show="showRoomMap"
    :rooms="expandedRecord ? roomMapRooms(expandedRecord) : []"
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
import RoomMapModal from "./room-map-modal.vue";
export default {
  name: "EditUnScheduleModal",
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

    // =====================================================
    // SELECTED UNSCHEDULED MEETING
    // KEPT SEPARATE FROM instructorData
    // =====================================================
    unscheduledMeeting: {
      type: Object,
      default: null,
    },

    activeSchoolYear: {
      type: Object,
      default: null,
    },
  },
  data() {
    return {
      user: {},
      localData: [],
      tempRecords: [],
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
      selectedUnscheduledMeeting: null,
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
      "all_school_years",
    ]),
    filteredSectionsForExpanded() {
      const record = this.expandedRecord;

      if (!record) {
        return [];
      }

      const fetchDataStore = useFetchDataStore();
      const sections = fetchDataStore.sections || [];

      let filtered = sections;

      // Department Chairperson
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

      const query = String(record.searchSectionQuery || "")
        .trim()
        .toLowerCase();

      if (!query) {
        return filtered;
      }

      return filtered.filter((section) => {
        const programCode = String(
          section.program?.program_code || "",
        ).toLowerCase();

        const setName = String(section.set_name || "").toLowerCase();

        return (
          programCode.includes(query) ||
          setName.includes(query) ||
          `${programCode} - ${setName}`.includes(query)
        );
      });
    },
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

      (this.localData || []).forEach((record) => {
        if (!record) return;

        const facultyId =
          record.faculty_id != null ? Number(record.faculty_id) : null;

        const facultyName = String(record.faculty_name || "").trim();

        if (!facultyName) return;

        const facultyKey =
          facultyId != null && !Number.isNaN(facultyId)
            ? `faculty-${facultyId}`
            : `name-${facultyName.toLowerCase()}`;

        const day = record.day || "";

        const key = `${facultyKey}-${day}`;

        if (!grid[key]) {
          grid[key] = [];
        }

        grid[key].push(record);
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
      const groupsByFacultyId = new Map();

      (this.localData || []).forEach((record) => {
        if (!record) return;

        const facultyId =
          record.faculty_id != null ? Number(record.faculty_id) : null;

        const normalizedName = String(record.faculty_name || "").trim();

        if (!normalizedName) return;

        // =====================================================
        // USE FACULTY ID AS THE REAL IDENTITY
        // =====================================================

        const groupKey =
          facultyId != null && !Number.isNaN(facultyId)
            ? `faculty-${facultyId}`
            : `name-${normalizedName.toLowerCase()}`;

        // =====================================================
        // CREATE FACULTY GROUP
        // =====================================================

        if (!groupsByFacultyId.has(groupKey)) {
          groupsByFacultyId.set(groupKey, {
            faculty_id: facultyId,
            faculty_name: normalizedName,
            schedules: [],
          });
        }

        const group = groupsByFacultyId.get(groupKey);

        // =====================================================
        // USE CANONICAL FACULTY NAME
        //
        // This prevents:
        // "Anselmo Anobong"
        // "anselmo anobong"
        //
        // from becoming two forms.
        // =====================================================

        if (!record.isUnscheduledMeeting && !record.isUnscheduledAssignment) {
          group.faculty_name = normalizedName;
        }

        group.schedules.push({
          ...record,

          faculty_id: group.faculty_id ?? record.faculty_id,

          faculty_name: group.faculty_name || normalizedName,
        });
      });

      // =====================================================
      // RETURN SAME FORMAT USED BY TEMPLATE
      // {
      //   "Anselmo Anobong": [ ...records ]
      // }
      // =====================================================

      const result = {};

      groupsByFacultyId.forEach((group) => {
        result[group.faculty_name] = group.schedules;
      });

      return result;
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
    unscheduledMeeting: {
      immediate: true,
      deep: true,

      handler(newMeeting) {
        if (!newMeeting) {
          this.selectedUnscheduledMeeting = null;
          return;
        }

        console.log(
          "[Edit Schedule] Unscheduled meeting received:",
          newMeeting,
        );

        // =====================================================
        // ONLY STORE THE SELECTION
        //
        // DO NOT CREATE expandedRecord HERE.
        // DO NOT PUSH INTO localData HERE.
        //
        // addUnscheduledToCalendar() is the ONLY place
        // responsible for creating the calendar record.
        // =====================================================

        this.selectedUnscheduledMeeting = structuredClone(newMeeting);
      },
    },
    // Watch for changes in instructorData to update localData
    instructorData: {
      immediate: true,
      async handler(newVal) {
        const fetchDataStore = useFetchDataStore();

        const incoming = Array.isArray(newVal) ? newVal : [];

        // Check whether incoming class IDs exist
        // in the current section store.
        const sections = fetchDataStore.sections || [];

        const sectionIds = new Set(
          sections
            .filter((section) => section?.class_id != null)
            .map((section) => Number(section.class_id)),
        );

        const missingClassId = incoming.some(
          (record) =>
            record?.class_id != null &&
            !sectionIds.has(Number(record.class_id)),
        );

        // Automatically refresh sections if the newly
        // assigned class is not yet in Pinia.
        if (missingClassId) {
          await this.fetchClassSections();
        }

        // Get the UPDATED sections after refresh
        const updatedSections = fetchDataStore.sections || [];

        const sectionMap = new Map(
          updatedSections
            .filter((section) => section?.class_id != null)
            .map((section) => [Number(section.class_id), section]),
        );

        this.localData = incoming.map((record) => {
          const classId =
            record.class_id != null ? Number(record.class_id) : null;

          const section = classId != null ? sectionMap.get(classId) : null;

          const setName = record.set_name || section?.set_name || "";

          return {
            ...structuredClone(record),

            class_id: record.class_id ?? section?.class_id ?? null,

            set_name: setName,

            searchSectionQuery: setName,

            program_id: record.program_id ?? section?.program_id ?? null,

            program_code: record.program_code || section?.program_code || "",

            class_size: record.class_size ?? section?.class_size ?? null,

            isUnscheduledMeeting:
              record.isUnscheduledMeeting === true ||
              record.isUnscheduledAssignment === true,

            searchRoomQuery: record.room_name || "",

            showRoomDropdown: false,

            searchCourseQuery: record.course_code || "",

            showCourseDropdown: false,

            searchCampusQuery:
              record.college_branch_name ||
              this.getCollegeBranchName(record.college_branch_id) ||
              "",

            showCampusDropdown: false,
          };
        });

        this.tempRecords = this.localData.filter(
          (record) =>
            record.isUnscheduledMeeting ||
            record.isUnscheduledAssignment ||
            String(record.tempId || "").startsWith("temp-"),
        );
      },
    },
    expandedRecord: {
      deep: true,

      handler(record) {
        if (!record) return;

        // Only process unscheduled records
        if (!record.isUnscheduledMeeting && !record.isUnscheduledAssignment) {
          return;
        }

        // -----------------------------------------
        // 1. Update time slot only when needed
        // -----------------------------------------
        const startHour = Number(record.start_hour);
        const duration = Number(record.duration);

        if (Number.isFinite(startHour) && Number.isFinite(duration)) {
          const newTimeSlot = this.generateTimeSlot(startHour, duration);

          if (record.time_slot !== newTimeSlot) {
            record.time_slot = newTimeSlot;
          }
        } else {
          record.time_slot = null;
        }

        // -----------------------------------------
        // 2. Synchronize localData
        // -----------------------------------------
        const index = this.localData.findIndex(
          (item) => item.tempId === record.tempId,
        );

        if (index === -1) {
          return;
        }

        // Only copy changed values
        Object.assign(this.localData[index], {
          day: record.day,
          start_hour: record.start_hour,
          duration: record.duration,
          time_slot: record.time_slot,
          room_id: record.room_id,
          room_name: record.room_name,
          room_type: record.room_type,
          room_capacity: record.room_capacity,
          college_branch_id: record.college_branch_id,
          college_branch_name: record.college_branch_name,
          mode: record.mode,
          class_id: record.class_id,
          set_name: record.set_name,
          program_id: record.program_id,
          program_code: record.program_code,
          class_size: record.class_size,
        });

        // -----------------------------------------
        // 3. DO NOT call this while typing Section
        // -----------------------------------------
        if (record.class_id && record.set_name) {
          this.setTemporaryUnscheduledRecord(record);
        }
      },
    },
    // Watch for modal open (show = true) to refresh all data
    show: {
      immediate: false,

      async handler(isVisible) {
        if (!isVisible) {
          return;
        }

        console.log("[Edit Schedule] Modal opened.");

        // =====================================================
        // LOAD ONLY EXISTING FACULTY SCHEDULES
        //
        // DO NOT INSERT UNSCHEDULED HERE.
        // DO NOT CREATE expandedRecord HERE.
        // =====================================================

        const incoming = Array.isArray(this.instructorData)
          ? this.instructorData
          : [];

        const fetchDataStore = useFetchDataStore();

        const sections = fetchDataStore.sections || [];

        this.localData = incoming.map((record) => {
          const class_size =
            record.class_size ||
            (record.class_id
              ? sections.find(
                  (section) =>
                    Number(section.class_id) === Number(record.class_id),
                )?.class_size
              : null);

          return {
            ...structuredClone(record),

            class_size,

            isUnscheduledMeeting:
              record.isUnscheduledMeeting === true ||
              record.isUnscheduledAssignment === true,

            searchRoomQuery: record.room_name || "",

            showRoomDropdown: false,

            searchCourseQuery: record.course_code || "",

            showCourseDropdown: false,

            searchSectionQuery: record.set_name || "",

            showSectionDropdown: false,

            searchCampusQuery:
              record.college_branch_name ||
              this.getCollegeBranchName(record.college_branch_id) ||
              "",

            showCampusDropdown: false,
          };
        });

        // =====================================================
        // CLEAR TEMP RECORDS WHEN OPENING A NEW EDIT SESSION
        // =====================================================

        this.tempRecords = [];

        // =====================================================
        // DO NOT DO THIS:
        //
        // selectedUnscheduledMeeting -> localData
        //
        // That happens ONLY when Assign is clicked.
        // =====================================================

        this.expandedRecord = null;

        console.log(
          "[Edit Schedule] Existing schedules loaded:",
          this.localData,
        );
      },
    },
  },

  methods: {
    // ============================================================
    // ROOM MAP
    // ============================================================
    // ============================================================
    // ROOM MAP ROOMS
    // ============================================================
    roomMapRooms(record) {
      if (!record) {
        return [];
      }

      let rooms = [...(this.rooms || [])];

      // ============================================================
      // 1. FILTER BY CAMPUS
      // ============================================================
      const campusId = Number(record.college_branch_id);

      if (campusId > 0) {
        rooms = rooms.filter((room) => {
          const roomCampusId = Number(
            room?.building?.buildingArea?.collegeBranch?.college_branch_id,
          );

          return roomCampusId === campusId;
        });
      }

      // ============================================================
      // 2. FILTER BY ROOM TYPE
      // ============================================================
      const type = String(record.type || "")
        .trim()
        .toLowerCase();

      if (
        type === "laboratory" ||
        type.includes("laboratory") ||
        type === "lab"
      ) {
        rooms = rooms.filter((room) => this.isLaboratoryRoom(room));
      } else if (
        type === "lecture" ||
        type.includes("lecture") ||
        type === "lec" ||
        type === "classroom"
      ) {
        rooms = rooms.filter((room) => this.isLectureRoom(room));
      }

      // ============================================================
      // 3. IF TYPE IS EMPTY
      // Show both lecture and laboratory rooms
      // ============================================================
      else {
        rooms = rooms.filter(
          (room) => this.isLectureRoom(room) || this.isLaboratoryRoom(room),
        );
      }

      return rooms;
    },
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

      // Open 2D room map
      this.showRoomMap = true;
    },

    selectRoomFromMap(room) {
      if (!this.expandedRecord || !room) {
        return;
      }

      // Reuse existing room selection logic
      this.selectRoom(this.expandedRecord, room);

      // Close map
      this.showRoomMap = false;
    },

    closeRoomMap() {
      this.showRoomMap = false;
    },
    isActuallyUnscheduled(record) {
      if (!record) return false;

      return (
        record.isUnscheduledMeeting === true ||
        record.unscheduled_id != null ||
        record.unscheduled_meeting_id != null
      );
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
    cancelEdit() {
      // Close inner panels
      this.showAddPanel = false;
      this.showUnscheduledPanel = false;

      // Clear selected/editing records
      this.expandedRecord = null;
      this.selectedUnscheduledMeeting = null;

      // Clear conflict modal
      this.conflictModalVisible = false;
      this.conflictRecords = [];

      // Clear drag state
      this.draggedRecord = null;
      this.draggedGroup = [];
      this.dragConflictMap = {};

      // Finally close the main modal
      this.$emit("close");
    },
    getAllSchedulesForConflict(record) {
      if (!record) return [];

      const scheduleMap = new Map();

      // -----------------------------------------
      // 1. ORIGINAL DATABASE SCHEDULES
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
      // 2. CURRENT EDIT SCHEDULES
      // -----------------------------------------
      (this.localData || []).forEach((schedule) => {
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
      // 3. TEMPORARY RECORDS
      // INCLUDING SELECTED UNSCHEDULED MEETING
      // -----------------------------------------
      (this.tempRecords || []).forEach((schedule) => {
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
      // 4. FILTER SCHOOL YEAR + SEMESTER
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
    addUnscheduledToCalendar(data) {
      console.log("[UNSCHEDULED] Selected:", data);

      if (!data) {
        console.warn("[UNSCHEDULED] No data received.");
        return;
      }

      // =====================================================
      // GET COURSE DATA
      // =====================================================

      const courses = Array.isArray(data)
        ? data
        : Array.isArray(data.courses)
        ? data.courses
        : [];

      if (!courses.length) {
        console.warn("[UNSCHEDULED] No courses found.");
        return;
      }

      const course = structuredClone(courses[0]);

      // =====================================================
      // GET FACULTY
      // =====================================================

      const selectedFacultyId =
        this.selectedUnscheduledMeeting?.faculty_id ??
        data.faculty_id ??
        data.facultyId ??
        course.faculty_id ??
        null;

      if (
        selectedFacultyId == null ||
        Number.isNaN(Number(selectedFacultyId))
      ) {
        console.error("[UNSCHEDULED] faculty_id is missing:", course);

        return;
      }

      // =====================================================
      // FIND SAME FACULTY IN CURRENT CALENDAR
      // =====================================================

      const existingFaculty = this.localData.find((record) => {
        if (!record) return false;

        return (
          record.faculty_id != null &&
          Number(record.faculty_id) === Number(selectedFacultyId) &&
          !record.isUnscheduledMeeting &&
          !record.isUnscheduledAssignment &&
          record.unscheduled_id == null &&
          record.unscheduled_meeting_id == null
        );
      });

      if (!existingFaculty) {
        console.error("[UNSCHEDULED] SAME FACULTY NOT FOUND.", {
          selectedFacultyId,
          facultyIds: this.localData.map((r) => r.faculty_id),
        });

        return;
      }

      console.log("[UNSCHEDULED] SAME FACULTY FOUND:", existingFaculty);
      const facultyId = Number(existingFaculty.faculty_id);
      const facultyName = existingFaculty.faculty_name;

      console.log("[UNSCHEDULED] CANONICAL FACULTY:", {
        facultyId,
        facultyName,
      });
      // =====================================================
      // PARSE HOURS
      // =====================================================

      const parsedHours = this.parseMeetingHours(course.hours);

      // =====================================================
      // DETERMINE DURATION
      //
      // Prefer actual duration from unscheduled record.
      // Otherwise derive it from its type.
      // =====================================================

      let duration = course.duration != null ? Number(course.duration) : null;

      const type = String(course.type || "").toLowerCase();

      if (duration == null || Number.isNaN(duration) || duration <= 0) {
        if (type === "lecture") {
          duration = Number(parsedHours.lec || 0);
        } else if (type === "laboratory") {
          duration = Number(parsedHours.lab || 0);
        } else {
          duration = Math.max(
            Number(parsedHours.lec || 0),
            Number(parsedHours.lab || 0),
          );
        }
      }

      // Safety fallback
      if (duration == null || Number.isNaN(duration) || duration <= 0) {
        duration = 1;
      }

      // =====================================================
      // FIND INITIAL DAY / TIME
      //
      // If unscheduled already has a day/time,
      // preserve it.
      //
      // Otherwise put it into the first available
      // calendar slot for this faculty.
      // =====================================================

      let selectedDay = course.day || null;

      let selectedStart =
        course.start_hour != null ? Number(course.start_hour) : null;

      if (
        !selectedDay ||
        selectedStart == null ||
        Number.isNaN(selectedStart)
      ) {
        selectedDay = null;
        selectedStart = null;

        // ---------------------------------------------
        // Search from Monday 7 AM
        // ---------------------------------------------

        outerLoop: for (const day of this.days) {
          for (let hour = 7; hour <= 20; hour += 0.5) {
            const endHour = hour + Number(duration);

            if (endHour > 21) {
              continue;
            }

            const hasConflict = this.localData.some((record) => {
              if (!record) return false;

              // Ignore unscheduled records
              if (
                record.isUnscheduledMeeting ||
                record.isUnscheduledAssignment
              ) {
                return false;
              }

              if (
                Number(record.faculty_id) !== Number(existingFaculty.faculty_id)
              ) {
                return false;
              }

              if (record.day !== day) {
                return false;
              }

              if (record.start_hour == null || record.duration == null) {
                return false;
              }

              const recordStart = Number(record.start_hour);

              const recordEnd = recordStart + Number(record.duration);

              return hour < recordEnd && endHour > recordStart;
            });

            if (!hasConflict) {
              selectedDay = day;
              selectedStart = hour;

              break outerLoop;
            }
          }
        }

        // ---------------------------------------------
        // Fallback
        // ---------------------------------------------

        if (!selectedDay) {
          selectedDay = "Monday";
          selectedStart = 7;
        }
      }

      // =====================================================
      // UNSCHEDULED ID
      // =====================================================

      const unscheduledId =
        course.unscheduled_id ??
        course.unscheduled_meeting_id ??
        data.unscheduled_id ??
        data.unscheduled_meeting_id ??
        this.selectedUnscheduledMeeting?.unscheduled_id ??
        this.selectedUnscheduledMeeting?.unscheduled_meeting_id ??
        course.id ??
        null;

      // =====================================================
      // TEMP ID
      // =====================================================

      const tempId = `temp-unscheduled-${unscheduledId ?? Date.now()}`;

      // =====================================================
      // BUILD CALENDAR RECORD
      // =====================================================
      const fetchDataStore = useFetchDataStore();
      const sections = fetchDataStore.sections || [];

      const classId = course.class_id ?? null;

      const section = sections.find(
        (s) => Number(s.class_id) === Number(classId),
      );

      const calendarRecord = {
        ...course,

        // ===================================================
        // FACULTY
        // ===================================================

        // ALWAYS USE EXISTING FACULTY
        faculty_id: facultyId,
        faculty_name: facultyName,

        // ===================================================
        // TEMP RECORD
        // ===================================================

        id: null,

        tempId,

        isNew: true,

        isUnscheduledMeeting: true,

        isUnscheduledAssignment: true,

        // ===================================================
        // UNSCHEDULED REFERENCE
        // ===================================================

        unscheduled_id: unscheduledId,

        unscheduled_meeting_id:
          course.unscheduled_meeting_id ??
          course.unscheduled_id ??
          unscheduledId,

        // ===================================================
        // CLASS / COURSE
        // ===================================================

        class_id: course.class_id ?? null,

        course_id: course.course_id ?? null,

        course_code: course.course_code || "",

        set_name: course.set_name || section?.set_name || "",

        // ===================================================
        // PROGRAM / INSTITUTE
        // ===================================================
        // Also fill these immediately
        program_id:
          course.class_program_id ??
          course.program_id ??
          section?.program_id ??
          existingFaculty.program_id ??
          null,

        program_code:
          course.program_code ??
          section?.program_code ??
          existingFaculty.program_code ??
          "",

        class_size: course.class_size ?? section?.class_size ?? null,

        institute_id:
          course.class_institute_id ??
          course.institute_id ??
          existingFaculty.institute_id ??
          null,

        institute_code:
          course.institute_code ?? existingFaculty.institute_code ?? "",

        // ===================================================
        // CAMPUS
        // ===================================================

        college_branch_id: course.college_branch_id ?? null,

        college_branch_name:
          course.college_branch_name ??
          this.getCollegeBranchName(course.college_branch_id) ??
          "",

        // ===================================================
        // ROOM
        // ===================================================

        room_id: course.room_id ?? null,

        room_name: course.room_name ?? "",

        room_type: course.room_type ?? "",

        room_capacity: course.room_capacity ?? null,

        // ===================================================
        // SCHEDULE
        // ===================================================

        day: selectedDay,

        start_hour: selectedStart,

        duration: duration,

        time_slot: this.generateTimeSlot(selectedStart, duration),

        // ===================================================
        // MODE
        // ===================================================

        mode: course.mode || "face to face",

        // ===================================================
        // TYPE
        // ===================================================

        type:
          course.type ||
          (parsedHours.lec > 0 && parsedHours.lab > 0
            ? "Lecture+Lab"
            : parsedHours.lab > 0
            ? "Laboratory"
            : "Lecture"),

        // ===================================================
        // HOURS
        // ===================================================

        lec_hours: parsedHours.lec,

        lab_hours: parsedHours.lab,

        // ===================================================
        // SEARCH FIELDS
        // ===================================================

        searchSectionQuery: course.set_name || "",

        searchCourseQuery: course.course_code || "",

        searchRoomQuery: course.room_name || "",

        searchCampusQuery:
          course.college_branch_name ||
          this.getCollegeBranchName(course.college_branch_id) ||
          "",

        // ===================================================
        // DROPDOWNS
        // ===================================================

        showSectionDropdown: false,

        showCourseDropdown: false,

        showRoomDropdown: false,

        showCampusDropdown: false,
      };

      // =====================================================
      // REMOVE EXISTING COPY
      // =====================================================

      this.localData = this.localData.filter((record) => {
        const existingId =
          record.unscheduled_id ?? record.unscheduled_meeting_id;

        if (existingId == null || unscheduledId == null) {
          return true;
        }

        return String(existingId) !== String(unscheduledId);
      });

      // =====================================================
      // INSERT INTO SAME FACULTY CALENDAR
      // =====================================================
      console.log("[UNSCHEDULED] FINAL FACULTY CHECK:", {
        newFacultyId: calendarRecord.faculty_id,
        newFacultyName: calendarRecord.faculty_name,

        existingFacultyIds: this.localData
          .filter((r) => Number(r.faculty_id) === Number(facultyId))
          .map((r) => ({
            faculty_id: r.faculty_id,
            faculty_name: r.faculty_name,
            course_code: r.course_code,
          })),
      });
      this.localData.push(calendarRecord);

      // =====================================================
      // IMPORTANT:
      // SAME OBJECT
      // =====================================================

      this.selectedUnscheduledMeeting = calendarRecord;

      this.expandedRecord = calendarRecord;

      // =====================================================
      // CONFLICT CHECK RECORD
      // =====================================================

      this.setTemporaryUnscheduledRecord(calendarRecord);

      // =====================================================
      // OPEN EDIT PANEL
      // =====================================================

      this.showUnscheduledPanel = false;

      this.showAddPanel = true;

      console.log("[UNSCHEDULED] ADDED TO CALENDAR:", calendarRecord);

      console.log("[UNSCHEDULED] localData:", this.localData);
    },
    setTemporaryUnscheduledRecord(record) {
      if (!record) {
        return;
      }

      const unscheduledId =
        record.unscheduled_id ?? record.unscheduled_meeting_id ?? null;

      const tempId =
        record.tempId || `temp-unscheduled-${unscheduledId ?? Date.now()}`;

      const tempRecord = {
        ...structuredClone(record),

        id: null,

        tempId,

        isNew: true,

        isUnscheduledMeeting: true,

        isUnscheduledAssignment: true,

        faculty_id: record.faculty_id ?? null,

        faculty_name: record.faculty_name || "",

        day: record.day ?? null,

        start_hour:
          record.start_hour != null ? Number(record.start_hour) : null,

        duration: record.duration != null ? Number(record.duration) : null,

        time_slot:
          record.start_hour != null && record.duration != null
            ? this.generateTimeSlot(
                Number(record.start_hour),
                Number(record.duration),
              )
            : null,
      };

      // =====================================================
      // REPLACE EXISTING TEMP RECORD
      // =====================================================

      this.tempRecords = [
        ...(this.tempRecords || []).filter((item) => {
          const itemId =
            item.unscheduled_id ?? item.unscheduled_meeting_id ?? null;

          // Prefer unscheduled ID
          if (itemId != null && unscheduledId != null) {
            return String(itemId) !== String(unscheduledId);
          }

          // Otherwise use tempId
          return item.tempId !== tempId;
        }),

        tempRecord,
      ];

      console.log("[CONFLICT] tempRecords:", this.tempRecords);
    },
    parseMeetingHours(hours) {
      const result = {
        lec: 0,
        lab: 0,
      };

      if (!hours) {
        return result;
      }

      const text = String(hours).toLowerCase();

      const lecMatch = text.match(/(\d+(?:\.\d+)?)\s*h\s*lec/);

      const labMatch = text.match(/(\d+(?:\.\d+)?)\s*h\s*lab/);

      if (lecMatch) {
        result.lec = Number(lecMatch[1]);
      }

      if (labMatch) {
        result.lab = Number(labMatch[1]);
      }

      console.log("[Edit Schedule] parseMeetingHours:", {
        hours,
        lec: result.lec,
        lab: result.lab,
      });

      return result;
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
        // =========================
        // CLASS / COURSE
        // =========================
        "class_id",
        "course_id",
        "course_code",
        "set_name",

        // =========================
        // PROGRAM / INSTITUTE
        // =========================
        "program_id",
        "program_code",
        "institute_id",

        // =========================
        // SCHEDULE
        // =========================
        "type",
        "day",
        "start_hour",
        "duration",
        "time_slot",

        // =========================
        // ROOM
        // =========================
        "room_id",
        "room_name",
        "room_type",
        "room_capacity",
        "college_branch_id",

        // =========================
        // FACULTY
        // =========================
        "faculty_id",
        "faculty_name",

        // =========================
        // CLASS
        // =========================
        "class_size",

        // =========================
        // SCHOOL YEAR
        // =========================
        "school_year",
        "semester",

        // =========================
        // MODE
        // =========================
        "mode",

        // =========================
        // JOINED SCHEDULE
        // =========================
        "is_joined",
        "join_group_id",
        "joined_with",
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

        // Fetch supporting data
        await fetchDataStore.fetchFinalSchedules();
        await this.fetchRooms();
        await this.fetchCurriculumCourses();
        await this.fetchRawUsers();
        await this.fetchClassSections();

        // ALL schedules are only for conflict checking
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
          },
        );

        console.log(
          "[Edit Schedule] Full schedules loaded:",
          this.fullSchedules.length,
        );

        // IMPORTANT:
        // DO NOT DO THIS:
        // this.localData = this.fullSchedules;

        // DO NOT replace instructorData/localData here.
      } catch (error) {
        console.error("[Edit Schedule] Failed to load data:", error);

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
      console.log("[Edit Schedule] refreshInstructorData input:", newData);

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

      console.log("[Edit Schedule] localData after refresh:", this.localData);
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

      return type.includes("lab") || type.includes("laboratory");
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
            room.building?.buildingArea?.collegeBranch?.college_branch_id,
          );

          return roomCampusId === selectedCampusId;
        });
      }

      // ============================================================
      // 2. GET COURSE REQUIREMENTS
      // ============================================================
      let courseLec = Number(record?.course_lec || 0);
      let courseLab = Number(record?.course_lab || 0);

      // Existing schedules may not contain course_lec/course_lab
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
      // 3. DETERMINE SCHEDULE TYPE
      // ============================================================
      const scheduleType = String(record?.type || "")
        .trim()
        .toLowerCase();

      // ============================================================
      // 4. GET CURRENT LOGGED-IN USER INSTITUTE
      // ============================================================
      const currentUserInstituteId = Number(this.user?.institute_id);

      // ============================================================
      // 5. HELPER: GET ROOM INSTITUTE ID
      // ============================================================
      const getRoomInstituteId = (room) => {
        return Number(
          room?.institute_id ??
            room?.institute?.institute_id ??
            room?.building?.institute_id ??
            room?.building?.institute?.institute_id ??
            room?.building?.buildingArea?.institute_id ??
            room?.building?.buildingArea?.institute?.institute_id ??
            room?.building?.buildingArea?.institute?.instituteId ??
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
        // ----------------------------------------------------------
        // ONLY LABORATORY ROOMS
        // ----------------------------------------------------------
        rooms = rooms.filter((room) => this.isLaboratoryRoom(room));

        // ----------------------------------------------------------
        // ONLY ROOMS BELONGING TO CURRENT USER'S INSTITUTE
        // ----------------------------------------------------------
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
        // Lecture rooms remain based on campus + room type.
        rooms = rooms.filter((room) => this.isLectureRoom(room));
      }

      // ============================================================
      // 8. FALLBACK WHEN TYPE IS NOT AVAILABLE
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

          // --------------------------------------------------------
          // CURRENT USER'S INSTITUTE ONLY
          // --------------------------------------------------------
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
          /*
           * Course has both Lecture and Laboratory.
           *
           * The schedule card must have a type:
           * - Lecture
           * - Laboratory
           *
           * Do not display both room types at the same time.
           */
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
          String(room.room_name || "")
            .toLowerCase()
            .includes(query),
        );
      }

      // ============================================================
      // 10. RETURN
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
      if (record.room_id !== room.room_id) {
        record.room_id = room.room_id;
        record.room_name = room.room_name;
        record.room_type = room.room_type;
        record.room_capacity = room.room_capacity;
      }

      record.searchRoomQuery = room.room_name;
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

      // ============================================
      // COURSE ROOM REQUIREMENTS
      // ============================================
      record.course_lec = Number(course.course_lec || 0);
      record.course_lab = Number(course.course_lab || 0);

      // ============================================
      // SCHOOL YEAR / SEMESTER
      // ============================================
      const currentSchoolYear = await this.getCurrentSchoolYear();

      record.school_year = currentSchoolYear.school_year;

      record.semester = String(currentSchoolYear.semester);

      // ============================================
      // CURRICULUM / PROGRAM
      // ============================================
      record.program_id = curriculum?.program_id || null;

      record.program_code = curriculum?.program?.program_code || "";

      record.institute_id = curriculum?.institute_id || null;

      // ============================================
      // DISPLAY
      // ============================================
      record.searchCourseQuery = course.course_code;

      record.showCourseDropdown = false;

      // ============================================
      // IMPORTANT:
      // RESET OLD ROOM
      // ============================================
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

      if (!Number.isFinite(recordStart) || !Number.isFinite(recordEnd)) {
        return [];
      }

      const sourceSchedules = this.getAllSchedulesForConflict(record);

      return sourceSchedules
        .filter((r) => {
          if (!r) return false;

          // =====================================================
          // 1. NEVER COMPARE A RECORD WITH ITSELF
          // =====================================================

          // Same database ID
          if (
            record.id != null &&
            r.id != null &&
            String(record.id) === String(r.id)
          ) {
            return false;
          }

          // Same temporary ID
          if (
            record.tempId &&
            r.tempId &&
            String(record.tempId) === String(r.tempId)
          ) {
            return false;
          }

          // Same unscheduled meeting
          //
          // This is IMPORTANT for newly assigned schedules.
          //
          const recordUnscheduledId =
            record.unscheduled_id ?? record.unscheduled_meeting_id ?? null;

          const otherUnscheduledId =
            r.unscheduled_id ?? r.unscheduled_meeting_id ?? null;

          if (
            recordUnscheduledId != null &&
            otherUnscheduledId != null &&
            String(recordUnscheduledId) === String(otherUnscheduledId)
          ) {
            return false;
          }

          // =====================================================
          // 2. SAME JOIN GROUP = NOT A CONFLICT
          // =====================================================

          if (
            record.join_group_id &&
            r.join_group_id &&
            Number(record.join_group_id) === Number(r.join_group_id)
          ) {
            return false;
          }

          // =====================================================
          // 3. SAME DAY
          // =====================================================

          if (String(r.day || "").trim() !== String(record.day || "").trim()) {
            return false;
          }

          // =====================================================
          // 4. VALID TIME
          // =====================================================

          if (r.start_hour == null || r.duration == null) {
            return false;
          }

          const rStart = Number(r.start_hour);
          const rEnd = rStart + Number(r.duration);

          if (!Number.isFinite(rStart) || !Number.isFinite(rEnd)) {
            return false;
          }

          // =====================================================
          // 5. TIME OVERLAP
          // =====================================================

          const overlaps =
            Math.max(recordStart, rStart) < Math.min(recordEnd, rEnd);

          if (!overlaps) {
            return false;
          }

          // =====================================================
          // 6. FACULTY CONFLICT
          // =====================================================

          const sameFaculty =
            (record.faculty_id != null &&
              r.faculty_id != null &&
              Number(record.faculty_id) === Number(r.faculty_id)) ||
            (record.faculty_name &&
              r.faculty_name &&
              String(record.faculty_name).trim().toLowerCase() ===
                String(r.faculty_name).trim().toLowerCase());

          // =====================================================
          // 7. ROOM CONFLICT
          // =====================================================

          const sameRoom =
            String(record.mode || "").toLowerCase() === "face to face" &&
            String(r.mode || "").toLowerCase() === "face to face" &&
            record.room_id != null &&
            r.room_id != null &&
            Number(record.room_id) === Number(r.room_id);

          // =====================================================
          // 8. CLASS / SECTION CONFLICT
          // =====================================================

          const sameClass =
            record.class_id != null &&
            r.class_id != null &&
            Number(record.class_id) === Number(r.class_id);

          // =====================================================
          // 9. ONLINE SECTION CONFLICT
          // =====================================================

          const sameOnlineSection =
            String(record.mode || "").toLowerCase() === "online" &&
            String(r.mode || "").toLowerCase() === "online" &&
            String(r.set_name || "").trim() ===
              String(record.set_name || "").trim() &&
            Number(r.program_id) === Number(record.program_id) &&
            Number(r.college_branch_id) === Number(record.college_branch_id);

          return sameFaculty || sameRoom || sameClass || sameOnlineSection;
        })
        .map((r) => {
          const reasons = [];

          // =====================================================
          // FACULTY
          // =====================================================

          const sameFaculty =
            (record.faculty_id != null &&
              r.faculty_id != null &&
              Number(record.faculty_id) === Number(r.faculty_id)) ||
            (record.faculty_name &&
              r.faculty_name &&
              String(record.faculty_name).trim().toLowerCase() ===
                String(r.faculty_name).trim().toLowerCase());

          if (sameFaculty) {
            reasons.push(
              `Faculty "${
                r.faculty_name
              }" is already assigned from ${this.formatTime(
                r.start_hour,
              )} to ${this.formatTime(r.start_hour + Number(r.duration))}.`,
            );
          }

          // =====================================================
          // ROOM
          // =====================================================

          const sameRoom =
            String(record.mode || "").toLowerCase() === "face to face" &&
            String(r.mode || "").toLowerCase() === "face to face" &&
            record.room_id != null &&
            r.room_id != null &&
            Number(record.room_id) === Number(r.room_id);

          if (sameRoom) {
            reasons.push(
              `Room "${r.room_name}" is already occupied by ${r.course_code} (${
                r.program_code
              }-${r.set_name}) from ${this.formatTime(
                r.start_hour,
              )} to ${this.formatTime(r.start_hour + Number(r.duration))}.`,
            );
          }

          // =====================================================
          // CLASS
          // =====================================================

          const sameClass =
            record.class_id != null &&
            r.class_id != null &&
            Number(record.class_id) === Number(r.class_id);

          if (sameClass) {
            reasons.push(
              `Section ${r.program_code}-${r.set_name} already has a class (${r.course_code}) scheduled during this time.`,
            );
          }

          // =====================================================
          // ONLINE SECTION
          // =====================================================

          const sameOnlineSection =
            String(record.mode || "").toLowerCase() === "online" &&
            String(r.mode || "").toLowerCase() === "online" &&
            String(r.set_name || "").trim() ===
              String(record.set_name || "").trim() &&
            Number(r.program_id) === Number(record.program_id) &&
            Number(r.college_branch_id) === Number(record.college_branch_id);

          if (sameOnlineSection) {
            reasons.push(
              `This online section (${r.program_code}-${r.set_name}) already has another online class during this time.`,
            );
          }

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
      const schedules = this.groupedSchedule[instructor] || [];

      return schedules.filter((record) => {
        if (record.start_hour == null || record.duration == null) {
          return false;
        }

        return (
          record.day === day &&
          Number(record.start_hour) < Number(slot.end) &&
          Number(record.start_hour) + Number(record.duration) >
            Number(slot.start)
        );
      });
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
      if (!record) return [];

      const clonedRecord = {
        ...structuredClone(record),

        faculty_name: targetInstructor,
        day: targetDay,
        start_hour: Number(targetStartHour),

        // KEEP ORIGINAL IDENTITY
        id: record.id ?? null,
        tempId: record.tempId ?? null,

        unscheduled_id:
          record.unscheduled_id ?? record.unscheduled_meeting_id ?? null,

        unscheduled_meeting_id:
          record.unscheduled_meeting_id ?? record.unscheduled_id ?? null,
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
        // =====================================================
        // UPDATE POSITION
        // =====================================================

        Object.assign(rec, {
          faculty_name: targetInstructor,
          day: targetDay,
          start_hour: Number(targetStartHour),
        });

        // =====================================================
        // UPDATE TIME SLOT
        // =====================================================

        rec.time_slot = this.generateTimeSlot(rec.start_hour, rec.duration);

        // =====================================================
        // FORCE REACTIVE UPDATE
        // =====================================================

        const index = this.localData.findIndex(
          (item) =>
            (rec.id != null &&
              item.id != null &&
              String(item.id) === String(rec.id)) ||
            (rec.tempId &&
              item.tempId &&
              String(item.tempId) === String(rec.tempId)),
        );

        if (index !== -1) {
          this.localData[index] = {
            ...this.localData[index],
            ...rec,

            day: targetDay,
            start_hour: Number(targetStartHour),
            time_slot: rec.time_slot,
          };
        }

        // =====================================================
        // SAVE TO DATABASE
        // =====================================================

        const payload = this.sanitizePayload(rec);

        this.cleanDropdownFields(payload);

        const id = rec.id || rec.schedule_id || rec.final_generated_id;

        if (!id) {
          console.warn("[DRAG] No database ID. Local move only:", rec);

          continue;
        }

        try {
          await axios.patch(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/${id}`,
            payload,
          );
        } catch (error) {
          console.error(
            "[DRAG] Failed to update schedule:",
            error.response?.data || error,
          );
        }
      }

      // =====================================================
      // IMPORTANT: RECALCULATE CONFLICTS
      // =====================================================

      this.$forceUpdate?.();

      // Clear old drag state
      this.draggedRecord = null;
      this.draggedGroup = [];
      this.dragConflictMap = {};
      this.conflictPreview = [];

      /* ===============================
     RESET
  =============================== */

      this.draggedRecord = null;
      this.draggedGroup = [];
    },
    /* ------------------ 9. SAVING TO DATABASE  ---------------- */
    async saveEdit() {
      this.saving = true;

      // Keep the original unscheduled ID until the whole save succeeds
      let savedUnscheduledId = null;

      try {
        const currentSchoolYear = await this.getCurrentSchoolYear();

        // =====================================================
        // 1. FINALIZE SELECTED UNSCHEDULED MEETING
        // =====================================================
        if (this.selectedUnscheduledMeeting && this.expandedRecord) {
          const selected = this.selectedUnscheduledMeeting;
          const edited = this.expandedRecord;

          const unscheduledId =
            selected.unscheduled_id ??
            selected.unscheduled_meeting_id ??
            selected.id ??
            null;

          // SAVE IT FOR DELETION AFTER DATABASE SAVE
          savedUnscheduledId = unscheduledId;

          const facultyId = edited.faculty_id ?? selected.faculty_id ?? null;

          const facultyName =
            edited.faculty_name ?? selected.faculty_name ?? "";

          if (!facultyId) {
            throw new Error(
              "Cannot save unscheduled meeting: faculty_id is missing.",
            );
          }

          const existingFacultyRecord = this.localData.find(
            (record) =>
              record &&
              !record.isUnscheduledMeeting &&
              !record.isUnscheduledAssignment &&
              Number(record.faculty_id) === Number(facultyId),
          );

          if (!existingFacultyRecord) {
            throw new Error(
              `Existing faculty schedule not found for ${facultyName} (${facultyId}).`,
            );
          }

          const finalRecord = {
            ...structuredClone(edited),

            faculty_id: existingFacultyRecord.faculty_id,
            faculty_name: existingFacultyRecord.faculty_name,

            isNew: false,
            isUnscheduledMeeting: false,
            isUnscheduledAssignment: false,

            unscheduled_id: unscheduledId,
            unscheduled_meeting_id: unscheduledId,

            school_year: currentSchoolYear.school_year,
            semester: String(currentSchoolYear.semester),

            mode:
              edited.mode?.toLowerCase() === "online"
                ? "online"
                : "face to face",
          };

          // Remove temporary unscheduled copy from calendar
          this.localData = this.localData.filter((record) => {
            const recordUnscheduledId =
              record.unscheduled_id ?? record.unscheduled_meeting_id ?? null;

            if (
              unscheduledId != null &&
              recordUnscheduledId != null &&
              String(recordUnscheduledId) === String(unscheduledId)
            ) {
              return false;
            }

            if (record === edited || record.tempId === edited.tempId) {
              return false;
            }

            return true;
          });

          // Add finalized schedule
          this.localData.push(finalRecord);

          this.expandedRecord = finalRecord;

          console.log("[SAVE UNSCHEDULED] FINAL RECORD:", finalRecord);
        }

        // =====================================================
        // 2. REMOVE DUPLICATES
        // =====================================================
        const seen = new Set();

        this.localData = this.localData.filter((record) => {
          const key =
            record.id ||
            record.tempId ||
            `${record.course_id}|${record.room_id}|${record.class_id}|${record.mode}|${record.day}|${record.start_hour}|${record.faculty_id}`;

          if (seen.has(key)) {
            return false;
          }

          seen.add(key);
          return true;
        });

        // =====================================================
        // 3. PREPARE CREATE / UPDATE
        // =====================================================
        const newRows = [];
        const updatedRows = [];

        this.localData.forEach((record) => {
          if (!record.id && !record.tempId) {
            record.tempId = `temp-${Date.now()}-${Math.floor(
              Math.random() * 1000,
            )}`;
          }

          const payload = this.sanitizePayload({
            ...record,

            school_year: currentSchoolYear.school_year,
            semester: String(currentSchoolYear.semester),

            mode:
              record.mode?.toLowerCase() === "online"
                ? "online"
                : "face to face",
          });

          const id =
            record.id || record.schedule_id || record.final_generated_id;

          if (id) {
            updatedRows.push({
              id,
              payload,
            });
          } else {
            payload.tempId = record.tempId;
            newRows.push(payload);
          }
        });

        // =====================================================
        // 4. CREATE NEW SCHEDULES
        // =====================================================
        if (newRows.length) {
          const { data } = await axios.post(
            `${process.env.VUE_APP_API_BASE_URL}/final-generated-class-schedule/manual-bulk`,
            {
              schedules: newRows,
              override: true,
            },
          );

          data.forEach((row) => {
            const tempRecord = this.localData.find(
              (r) => !r.id && r.tempId === row.tempId,
            );

            if (tempRecord) {
              tempRecord.id = row.id;
            }
          });
        }

        // =====================================================
        // 5. UPDATE EXISTING SCHEDULES
        // =====================================================
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

        // =====================================================
        // 6. DELETE FROM UNSCHEDULED AFTER SCHEDULE SAVE
        // =====================================================
        if (savedUnscheduledId != null) {
          console.log(
            "[SAVE UNSCHEDULED] Deleting unscheduled meeting:",
            savedUnscheduledId,
          );

          await axios.delete(
            `${process.env.VUE_APP_API_BASE_URL}/unscheduled-meetings/${savedUnscheduledId}`,
          );

          console.log(
            "[SAVE UNSCHEDULED] Successfully deleted:",
            savedUnscheduledId,
          );
        }

        // =====================================================
        // 7. REFRESH DATA
        // =====================================================
        await this.fetchClassSections();

        toast.success("Schedule saved successfully!");

        this.selectedUnscheduledMeeting = null;
        this.expandedRecord = null;

        this.$emit("saved", this.localData);
        this.$emit("close");
        this.$emit("refresh");
      } catch (err) {
        console.error("Failed to save schedules:", err);

        toast.error(
          err?.response?.data?.message ||
            err?.message ||
            "Failed to save schedules.",
        );
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

/* ================================
   SCHEDULE CARD DRAG EFFECT
   ================================ */
.schedule-dragging {
  animation: clothGrab 180ms ease-out forwards;

  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.2), 0 10px 25px rgba(0, 0, 0, 0.12);

  cursor: grabbing;
  z-index: 9999 !important;
}

/* Card slightly bends/tilts while dragging */
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
