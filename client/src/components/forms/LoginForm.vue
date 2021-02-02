<template>
  <div class="box">
    <div class="card-content">
      <form action="" class="form-signin">
        <h2 class="title has-text-centered is-size-3">Please sign in</h2>
        <b-field label="Email">
          <b-input type="email" icon="email" v-model="username"> </b-input>
        </b-field>

        <b-field label="Password">
          <b-input
            type="password"
            icon="key"
            v-model="password"
            password-reveal
          >
          </b-input>
        </b-field>

        <b-field class="pt-3">
          <b-button class="is-medium is-primary is-fullwidth" @click="submit">
            Go
          </b-button>
        </b-field>

        <b-field class="has-text-centered">
          <a href="/new-account" class="text-muted d-block d-md-inline mt2">
            Create an account
          </a>
        </b-field>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    username: '',
    password: '',
  }),
  methods: {
    submit() {
      this.$emit('submit', {
        username: this.username,
        password: this.password,
      });
    },
  },
};
</script>