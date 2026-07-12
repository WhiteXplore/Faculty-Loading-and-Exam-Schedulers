<template>
  <div
    class="min-h-screen bg-gray-50 p-2 lg:p-1 lg:px-2 lg:px-3 rounded-md font-dashboard"
  >
    <!-- KEEP YOUR HEADER + CARDS -->
    <div
      class="flex flex-col xl:flex-row xl:items-stretch xl:justify-between gap-4 mb-6"
    >
      <div
        class="relative overflow-hidden flex flex-col justify-between bg-defaultGreen xl:w-[43vw] w-full rounded-2xl px-5 py-9 text-white shadow-lg"
      >
        <div
          class="absolute -right-10 -top-10 w-32 h-32 bg-white/10 rounded-full"
        ></div>
        <div
          class="absolute right-10 bottom-[-60px] w-28 h-28 bg-white/10 rounded-full"
        ></div>

        <div class="relative z-10">
          <p class="text-xs text-white/70 mb-2">Faculty Loading Dashboard</p>
          <h1 class="text-xl font-semibold tracking-tight">
            Welcome, {{ user.first_name }} 👋
          </h1>
          <p class="text-xs text-white/80 mt-1">
            Monitor faculty loads, subject assignments, room usage, and exam
            schedule conflicts.
          </p>
        </div>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-2 xl:grid-cols-4 gap-4 w-full">
        <div
          v-for="card in dashboardCards"
          :key="card.title"
          class="relative overflow-hidden rounded-2xl bg-white border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 p-4 min-w-[180px]"
        >
          <div class="relative flex items-start justify-between">
            <div>
              <p class="text-xs font-medium text-gray-500">{{ card.title }}</p>
              <h2 class="mt-4 text-2xl font-semibold text-gray-900">
                {{ card.value }}
              </h2>

              <div class="mt-4 flex items-center gap-2">
                <span
                  class="rounded-full px-2.5 py-1 text-[11px] font-semibold"
                  :class="card.badgeClass"
                >
                  {{ card.badge }}
                </span>
                <span class="text-xs text-gray-400">{{ card.caption }}</span>
              </div>
            </div>

            <div
              class="flex h-10 w-10 items-center justify-center rounded-xl shadow-sm"
              :class="card.iconBox"
            >
              <icon :name="card.icon" class="w-5 h-5" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- MAIN CONTENT LIKE THE IMAGE -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-5">
      <!-- LEFT -->
      <div class="xl:col-span-2 space-y-5">
        <!-- BAR CHART -->
        <div class="dashboard-card">
          <div class="card-header">
            <div>
              <h2 class="card-title">Faculty Load Overview</h2>
              <p class="card-subtitle">
                Total teaching units assigned per faculty
              </p>
            </div>

            <button class="filter-btn">This Semester ▾</button>
          </div>

          <div class="mt-6 h-72">
            <div
              class="relative h-full border-b border-gray-200 flex items-end gap-5 px-4"
            >
              <div
                class="absolute left-4 right-4 border-t border-dashed border-emerald-300"
                style="bottom: 55%"
              ></div>

              <p
                class="absolute right-4 text-[11px] font-semibold text-defaultGreen"
                style="bottom: 56%"
              >
                Avg. Load (18)
              </p>

              <div
                v-for="item in facultyLoadData"
                :key="item.name"
                class="flex-1 h-full flex flex-col justify-end items-center group"
              >
                <p class="mb-2 text-xs font-semibold text-gray-700">
                  {{ item.units }}
                </p>

                <div
                  class="w-full max-w-[55px] rounded-t-md bg-gradient-to-t from-defaultGreen to-emerald-400 shadow-lg shadow-green-100 transition group-hover:scale-105"
                  :style="{ height: item.height + '%' }"
                ></div>

                <p
                  class="mt-3 text-[11px] text-gray-500 text-center whitespace-nowrap"
                >
                  {{ item.name }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- LINE CHART -->
        <div class="dashboard-card">
          <div class="card-header">
            <div>
              <h2 class="card-title">Exam Schedule Trend</h2>
              <p class="card-subtitle">Number of exams scheduled per day</p>
            </div>

            <button class="filter-btn">This Week ▾</button>
          </div>

          <div class="mt-5 rounded-2xl bg-gray-50 p-4 overflow-hidden">
            <svg viewBox="0 0 700 260" class="w-full h-[260px]">
              <line
                v-for="y in [45, 90, 135, 180, 225]"
                :key="y"
                x1="35"
                :y1="y"
                x2="670"
                :y2="y"
                stroke="#e5e7eb"
              />

              <path :d="examAreaPath" fill="rgba(124, 92, 255, 0.12)" />

              <path
                :d="examLinePath"
                fill="none"
                stroke="#7c5cff"
                stroke-width="4"
                stroke-linecap="round"
                stroke-linejoin="round"
              />

              <g v-for="point in examPoints" :key="point.label">
                <circle :cx="point.x" :cy="point.y" r="6" fill="#7c5cff" />
                <text
                  :x="point.x"
                  :y="point.y - 14"
                  text-anchor="middle"
                  font-size="13"
                  font-weight="600"
                  fill="#111827"
                >
                  {{ point.value }}
                </text>
                <text
                  :x="point.x"
                  y="245"
                  text-anchor="middle"
                  font-size="12"
                  fill="#6b7280"
                >
                  {{ point.label }}
                </text>
              </g>
            </svg>
          </div>
        </div>

        <!-- RECENT ACTIVITIES -->
        <div class="dashboard-card">
          <div class="card-header">
            <div>
              <h2 class="card-title">Recent Faculty Loading Activities</h2>
            </div>

            <button class="text-xs font-semibold text-blue-600">
              View All
            </button>
          </div>

          <div class="mt-5 overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="text-left text-xs text-gray-400 border-b">
                  <th class="pb-3 font-medium">Faculty</th>
                  <th class="pb-3 font-medium">Subject</th>
                  <th class="pb-3 font-medium">Units</th>
                  <th class="pb-3 font-medium">Schedule</th>
                  <th class="pb-3 font-medium">Status</th>
                  <th class="pb-3 font-medium">Date</th>
                </tr>
              </thead>

              <tbody>
                <tr
                  v-for="row in recentAssignments"
                  :key="row.faculty"
                  class="border-b last:border-b-0 hover:bg-gray-50"
                >
                  <td class="py-4">
                    <div class="flex items-center gap-3">
                      <div
                        class="h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold"
                        :class="row.avatarClass"
                      >
                        {{ row.initials }}
                      </div>
                      <span class="font-medium text-gray-800">{{
                        row.faculty
                      }}</span>
                    </div>
                  </td>
                  <td class="py-4 text-gray-500">{{ row.subject }}</td>
                  <td class="py-4 text-gray-500">{{ row.units }}</td>
                  <td class="py-4 text-gray-500">{{ row.schedule }}</td>
                  <td class="py-4">
                    <span class="status-badge" :class="row.statusClass">
                      {{ row.status }}
                    </span>
                  </td>
                  <td class="py-4 text-gray-500">{{ row.date }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- RIGHT -->
      <div class="space-y-5">
        <!-- DONUT -->
        <div class="dashboard-card">
          <h2 class="card-title">Load Distribution</h2>

          <div class="mt-6 flex items-center justify-center">
            <div class="donut-chart">
              <div class="donut-hole">
                <h3>48</h3>
                <p>Faculty</p>
              </div>
            </div>
          </div>

          <div class="mt-6 space-y-4">
            <div
              v-for="item in loadDistribution"
              :key="item.label"
              class="flex items-start justify-between gap-3"
            >
              <div class="flex gap-3">
                <span
                  class="mt-1 h-3 w-3 rounded-full"
                  :class="item.dot"
                ></span>
                <div>
                  <p class="text-sm text-gray-600">{{ item.label }}</p>
                  <p class="text-xs text-gray-400">{{ item.desc }}</p>
                </div>
              </div>
              <p class="text-sm font-semibold text-gray-800">
                {{ item.value }}
              </p>
            </div>
          </div>
        </div>

        <!-- UPCOMING EXAMS -->
        <div class="dashboard-card">
          <div class="card-header">
            <h2 class="card-title">Upcoming Exams</h2>
            <button class="filter-btn">View Calendar</button>
          </div>

          <div class="mt-5 space-y-3">
            <div
              v-for="exam in upcomingExams"
              :key="exam.subject"
              class="flex items-center gap-4 rounded-2xl border border-gray-100 p-3 hover:bg-gray-50"
            >
              <div
                class="w-12 rounded-xl text-center py-2 text-xs font-bold"
                :class="exam.dateClass"
              >
                <p>{{ exam.month }}</p>
                <h3 class="text-lg leading-5">{{ exam.day }}</h3>
              </div>

              <div class="flex-1">
                <p class="text-xs text-gray-400">{{ exam.time }}</p>
                <h3 class="text-sm font-semibold text-gray-800">
                  {{ exam.subject }}
                </h3>
              </div>

              <p class="text-xs text-gray-500">{{ exam.room }}</p>

              <span class="status-badge" :class="exam.statusClass">
                Scheduled
              </span>
            </div>
          </div>
        </div>

        <!-- CONFLICTS -->
        <div class="dashboard-card">
          <div class="card-header">
            <h2 class="card-title">Conflicts Overview</h2>
            <button class="text-xs font-semibold text-red-500">View All</button>
          </div>

          <div class="mt-5 space-y-3">
            <div
              v-for="conflict in conflicts"
              :key="conflict.title"
              class="flex items-center gap-4 rounded-2xl border border-gray-100 p-4 hover:bg-gray-50"
            >
              <div
                class="h-11 w-11 rounded-xl flex items-center justify-center text-white"
                :class="conflict.box"
              >
                <icon :name="conflict.icon" />
              </div>

              <div class="flex-1">
                <h3 class="text-sm font-semibold text-gray-800">
                  {{ conflict.title }}
                </h3>
                <p class="text-xs text-gray-400">{{ conflict.description }}</p>
              </div>

              <p class="text-lg font-bold text-gray-900">
                {{ conflict.count }}
              </p>
              <span class="text-gray-400">›</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import icon from "@/assets/icon.vue";

export default {
  name: "EmployeeDashboard",

  components: {
    icon,
  },

  data() {
    return {
      user: {
        first_name: "John",
      },

      dashboardCards: [
        {
          title: "Total Faculty",
          value: "48",
          badge: "+12%",
          caption: "active instructors",
          icon: "users",
          iconBox: "bg-green-50 text-green-700",
          badgeClass: "bg-green-50 text-green-700",
        },
        {
          title: "Loaded Subjects",
          value: "126",
          badge: "82%",
          caption: "assigned courses",
          icon: "book",
          iconBox: "bg-blue-50 text-blue-700",
          badgeClass: "bg-blue-50 text-blue-700",
        },
        {
          title: "Exam Schedules",
          value: "34",
          badge: "This week",
          caption: "scheduled exams",
          icon: "calendar",
          iconBox: "bg-purple-50 text-purple-700",
          badgeClass: "bg-purple-50 text-purple-700",
        },
        {
          title: "Conflicts Found",
          value: "7",
          badge: "Needs review",
          caption: "conflicts",
          icon: "warning1",
          iconBox: "bg-red-50 text-red-700",
          badgeClass: "bg-red-50 text-red-700",
        },
      ],

      facultyLoadData: [
        { name: "Prof. Smith", units: 18, height: 60 },
        { name: "Prof. Johnson", units: 22, height: 76 },
        { name: "Prof. Williams", units: 16, height: 54 },
        { name: "Prof. Brown", units: 20, height: 69 },
        { name: "Prof. Jones", units: 19, height: 65 },
        { name: "Prof. Garcia", units: 17, height: 58 },
        { name: "Prof. Miller", units: 21, height: 72 },
        { name: "Prof. Davis", units: 15, height: 50 },
      ],

      examTrend: [
        { label: "Mon", value: 4 },
        { label: "Tue", value: 7 },
        { label: "Wed", value: 5 },
        { label: "Thu", value: 9 },
        { label: "Fri", value: 6 },
        { label: "Sat", value: 3 },
        { label: "Sun", value: 0 },
      ],

      loadDistribution: [
        {
          label: "Normal Load",
          desc: "12-18 units",
          value: "36",
          dot: "bg-defaultGreen",
        },
        {
          label: "Overloaded",
          desc: "Above 18 units",
          value: "9",
          dot: "bg-yellow-400",
        },
        {
          label: "Underloaded",
          desc: "Below 12 units",
          value: "3",
          dot: "bg-red-500",
        },
      ],

      upcomingExams: [
        {
          month: "MAY",
          day: "20",
          time: "8:00 AM - 10:00 AM",
          subject: "Database Management",
          room: "Room 201",
          dateClass: "bg-purple-50 text-purple-700",
          statusClass: "bg-purple-50 text-purple-700",
        },
        {
          month: "MAY",
          day: "21",
          time: "1:00 PM - 3:00 PM",
          subject: "Data Structures",
          room: "Room 305",
          dateClass: "bg-green-50 text-green-700",
          statusClass: "bg-green-50 text-green-700",
        },
        {
          month: "MAY",
          day: "22",
          time: "9:00 AM - 11:00 AM",
          subject: "Operating Systems",
          room: "Room 204",
          dateClass: "bg-yellow-50 text-yellow-700",
          statusClass: "bg-yellow-50 text-yellow-700",
        },
        {
          month: "MAY",
          day: "23",
          time: "2:00 PM - 4:00 PM",
          subject: "Web Development",
          room: "Room 101",
          dateClass: "bg-red-50 text-red-700",
          statusClass: "bg-red-50 text-red-700",
        },
      ],

      conflicts: [
        {
          title: "Room Conflicts",
          description: "Multiple exams in same room and time",
          count: "3",
          icon: "calendar",
          box: "bg-red-500",
        },
        {
          title: "Faculty Conflicts",
          description: "Faculty assigned to overlapping schedules",
          count: "2",
          icon: "users",
          box: "bg-yellow-500",
        },
        {
          title: "Subject Conflicts",
          description: "Same subject with duplicate exam schedule",
          count: "2",
          icon: "book",
          box: "bg-blue-500",
        },
      ],

      recentAssignments: [
        {
          initials: "PS",
          faculty: "Prof. Smith",
          subject: "IT 101 - Programming 1",
          units: "3",
          schedule: "MWF 8:00 AM - 9:00 AM",
          status: "Assigned",
          date: "May 15, 2026",
          avatarClass: "bg-green-100 text-green-700",
          statusClass: "bg-green-50 text-green-700",
        },
        {
          initials: "MJ",
          faculty: "Prof. Johnson",
          subject: "IT 204 - Database Systems",
          units: "3",
          schedule: "TTH 10:00 AM - 11:30 AM",
          status: "Assigned",
          date: "May 15, 2026",
          avatarClass: "bg-emerald-100 text-emerald-700",
          statusClass: "bg-green-50 text-green-700",
        },
        {
          initials: "RW",
          faculty: "Prof. Williams",
          subject: "IT 301 - Software Engineering",
          units: "3",
          schedule: "MWF 1:00 PM - 2:00 PM",
          status: "Review",
          date: "May 14, 2026",
          avatarClass: "bg-blue-100 text-blue-700",
          statusClass: "bg-yellow-50 text-yellow-700",
        },
        {
          initials: "AB",
          faculty: "Prof. Brown",
          subject: "IT 401 - Capstone Project",
          units: "3",
          schedule: "TTH 3:00 PM - 4:30 PM",
          status: "Conflict",
          date: "May 14, 2026",
          avatarClass: "bg-red-100 text-red-700",
          statusClass: "bg-red-50 text-red-700",
        },
      ],
    };
  },

  computed: {
    examPoints() {
      const maxValue =
        Math.max(...this.examTrend.map((item) => item.value)) || 1;
      const startX = 55;
      const gap = 100;
      const chartBottom = 215;
      const chartHeight = 165;

      return this.examTrend.map((item, index) => ({
        ...item,
        x: startX + index * gap,
        y: chartBottom - (item.value / maxValue) * chartHeight,
      }));
    },

    examLinePath() {
      return this.examPoints
        .map(
          (point, index) => `${index === 0 ? "M" : "L"} ${point.x} ${point.y}`,
        )
        .join(" ");
    },

    examAreaPath() {
      const points = this.examPoints;
      if (!points.length) return "";

      const first = points[0];
      const last = points[points.length - 1];

      return `
        M ${first.x} 215
        L ${points.map((point) => `${point.x} ${point.y}`).join(" L ")}
        L ${last.x} 215
        Z
      `;
    },
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap");

.font-dashboard {
  font-family: "Poppins", sans-serif;
}

.dashboard-card {
  @apply rounded-2xl bg-white border border-gray-100 shadow-sm p-5;
}

.card-header {
  @apply flex items-start justify-between gap-4;
}

.card-title {
  @apply text-base font-semibold text-gray-900;
}

.card-subtitle {
  @apply text-xs text-gray-400 mt-1;
}

.filter-btn {
  @apply rounded-xl border border-gray-200 bg-white px-4 py-2 text-xs font-medium text-gray-600 hover:bg-gray-50 transition;
}

.status-badge {
  @apply rounded-full px-3 py-1 text-[11px] font-semibold whitespace-nowrap;
}

.donut-chart {
  width: 190px;
  height: 190px;
  border-radius: 9999px;
  background: conic-gradient(
    #147452 0deg 270deg,
    #facc15 270deg 330deg,
    #ef4444 330deg 360deg
  );
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 24px 50px rgba(20, 116, 82, 0.18);
}

.donut-hole {
  width: 118px;
  height: 118px;
  border-radius: 9999px;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  box-shadow: inset 0 0 0 1px #f3f4f6;
}

.donut-hole h3 {
  font-size: 30px;
  font-weight: 700;
  color: #111827;
}

.donut-hole p {
  font-size: 12px;
  color: #374151;
}
</style>
