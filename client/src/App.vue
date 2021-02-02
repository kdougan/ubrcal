<template>
  <div id="app" class="app has-background-dark">
    <Sidebar />
    <Calendar />
    <!-- <EventPanel /> -->
  </div>
</template>

<script>
import Sidebar from './components/layout/Sidebar';
import Calendar from './components/Calendar';
// import EventPanel from './components/EventPanel';

export default {
  name: 'App',
  components: {
    Sidebar,
    Calendar,
    // EventPanel,
  },
  methods: {
    submit(form) {
      this.$store.dispatch('createUser', form);
    },
  },
};
</script>

<style>
html,
body {
  position: fixed;
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: red;
}
.app {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
  overscroll-behavior: contain;
  background-color: hsl(0, 100%, 21%);
}
</style>
