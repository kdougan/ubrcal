<template>
  <section class="has-text-white">
    <div class="box">
      <CreateUserForm @submit="submit" :loading="isLoading" />
    </div>
  </section>
</template>

<script>
import CreateUserForm from '../forms/CreateUserForm';

export default {
  components: {
    CreateUserForm,
  },
  data: () => ({
    isLoading: false,
  }),
  methods: {
    submit(data) {
      if (this.isLoading) return;
      this.isLoading = true;
      this.$store
        .dispatch('createUser', data)
        .then(() => {
          this.isLoading = false;
          this.$router.push('calendar');
        })
        .catch((error) => {
          console.log(error);
          this.isLoading = false;
        });
    },
  },
};
</script>