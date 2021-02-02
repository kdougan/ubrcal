<template>
  <div class="box">
    <div class="card-content">
      <form action="" class="form-signin">
        <h2 class="title has-text-centered is-size-3">
          Start with an email and password
        </h2>

        <b-field label="Email">
          <b-input type="email" icon="email" v-model="username"> </b-input>
        </b-field>

        <b-field label="Password">
          <b-input
            type="password"
            icon="key"
            v-model="passwordA"
            password-reveal
          >
          </b-input>
        </b-field>

        <b-field label="Confirm Password">
          <b-input
            type="password"
            icon="key"
            v-model="passwordB"
            password-reveal
          >
          </b-input>
        </b-field>

        <b-field class="pt-3">
          <b-button class="is-medium is-primary is-fullwidth" @click="submit">
            Create
          </b-button>
        </b-field>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    username: '',
    passwordA: '',
    passwordB: '',
  }),
  methods: {
    submit() {
      if (!this.passwordA == this.passwordB) return;
      this.$emit('submit', {
        username: this.username,
        password: this.passwordA,
      });
    },
  },
};
</script>