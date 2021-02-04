<template>
  <div class="calendar-view container has-text-white is-fluid m-0 p-0">
    <Sidebar style="z-index: 1000" />
    <Calendar style="z-index: 1" />
  </div>
</template>

<script>
import Sidebar from '/src/components/layout/Sidebar';
import Calendar from '/src/components/layout/Calendar';
export default {
  components: {
    Sidebar,
    Calendar,
  },
};
</script>

<style lang="scss">
.calendar-view {
  display: flex;
  flex-direction: row;
}
</style>