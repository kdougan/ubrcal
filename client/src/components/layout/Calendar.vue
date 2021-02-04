<template>
  <div class="calendar-container box has-background-dark">
    <FullCalendar :options="calendarOptions" />
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import listPlugin from '@fullcalendar/list';
import interactionPlugin from '@fullcalendar/interaction';

export default {
  components: {
    FullCalendar,
  },
  data() {
    return {
      calendarOptions: {
        height: '100%',
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin, listPlugin],
        initialView: 'dayGridMonth',
        headerToolbar: {
          left: 'title',
          center: 'timeGridDay,timeGridWeek,dayGridMonth,listWeek',
          right: 'prev,today,next',
        },
        dateClick: this.handleDateClick,
        events: [
          { title: 'event 1', date: '2021-01-01' },
          { title: 'event 2', date: '2021-01-23' },
        ],
      },
    };
  },
  methods: {
    handleDateClick: function (arg) {
      alert('date click! ' + arg.dateStr);
    },
  },
};
</script>

<style>
@import '../../style/fullcalendar.scss';

.calendar-container {
  width: 100%;
  height: 100%;
}

.fc-header-toolbar {
  color: white;
}
</style>