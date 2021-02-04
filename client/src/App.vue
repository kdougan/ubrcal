<template>
  <div id="app" class="app has-background-dark">
    <router-view></router-view>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'App',
  computed: {
    ...mapGetters(['loggedIn', 'user']),
  },
  methods: {
    ...mapActions(['getCurrentUser']),
  },
  created() {
    if (this.loggedIn) {
      this.getCurrentUser().then(() => {
        if (this.hasUser) {
          console.log("this.$router.push('calendar')");
          this.$router.push('calendar');
        } else {
          console.log("this.$router.push('createUser')");
          this.$router.push('createUser');
        }
      });
    }
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
  background-color: hsl(0, 100%, 15%);
}
.app {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
  overscroll-behavior: contain;
  background-color: hsl(0, 100%, 15%);
}
</style>
