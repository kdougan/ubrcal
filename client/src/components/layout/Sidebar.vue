<template>
  <b-sidebar type="is-dark" position="static" fullheight open reduce>
    <div class="sidebar-layout has-text-centered">
      <div class="sidebar-layout-header">
        <span class="has-text-weight-bold has-text-light mr-1">übrcal</span>
      </div>
      <div class="p-2 m-0">
        <b-image
          :src="gravatar + '?s=64'"
          :alt="alias"
          class="is-64x64 my-1 avatar"
          rounded
        ></b-image>
      </div>
      <div class="sidebar-layout-content p-2">
        <b-image
          v-for="calendar in calendars"
          :key="calendar._id"
          src="https://bulma.io/images/placeholders/64x64.png"
          alt="The Buefy Logo"
          class="is-64x64 my-1 avatar"
          rounded
        ></b-image>
      </div>
      <div class="sidebar-layout-footer block p-2">
        <b-icon icon="plus" size="is-medium" type="is-primary"></b-icon>
      </div>
    </div>
  </b-sidebar>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  data: () => ({
    open: false,
    overlay: true,
    fullheight: true,
    fullwidth: false,
    right: false,
  }),
  computed: {
    ...mapGetters(['user']),
    alias() {
      return this.user.alias;
    },
    gravatar() {
      return this.user.avatar.indexOf('gravatar') != -1
        ? `${this.user.avatar}?s=64`
        : this.user.avatar;
    },
    calendars() {
      return this.user.calendars.data;
    },
  },
  methods: {
    ...mapActions([]),
  },
};
</script>

<style lang="scss">
$sidebar-box-shadow: none;

.sidebar-layout {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow-y: hidden;

  .sidebar-layout-header {
    height: 24px;
    letter-spacing: 2pt;
    background: var(--uc-primary-color);
    border-bottom-right-radius: 16px;
    box-shadow: 0 2px 2px rgba(0, 0, 0, 0.5);
  }

  .sidebar-layout-content {
    border-radius: 0 48px 48px 0;
    flex-grow: 1;
    overflow-y: auto;
    -webkit-overflow-scrolling: touch;
    background-color: rgba(0, 0, 0, 0.1);
    box-shadow: inset 0 0 24px -8px rgba(0, 0, 0, 0.5);

    .avatar {
      transform: scale(0.9);
      transition: all 0.1s ease-in-out;

      &:hover {
        transform: scale(1);
      }
    }
  }

  .sidebar-layout-footer {
  }
}
</style>