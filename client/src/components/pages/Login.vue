<template>
  <section class="has-text-white">
    <div class="box">
      <LoginForm @submit="submit" :loading="isLoading" />
    </div>
  </section>
</template>

<script>
import LoginForm from '../forms/LoginForm';

export default {
  components: {
    LoginForm,
  },
  data: () => ({
    isLoading: false,
  }),
  methods: {
    submit(data) {
      if (this.isLoading) return;
      this.isLoading = true;
      this.$store.dispatch('login', data).then(() => {
        this.isLoading = false;
        this.$router.push('calendar');
      });
    },
  },
};
</script>