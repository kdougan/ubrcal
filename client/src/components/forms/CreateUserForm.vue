<template>
  <div class="box">
    <div class="card-content">
      <form action="" class="form-signin">
        <h2 class="title has-text-centered is-size-3">
          Just a little information about you...
        </h2>

        <b-field label="Full Name">
          <b-input type="text" v-model="name" placeholder="First Last">
          </b-input>
        </b-field>

        <b-field label="Alias">
          <b-input
            type="text"
            v-model="alias"
            placeholder="What your friends call ya"
          ></b-input>
        </b-field>

        <b-field label="Date of birth">
          <b-datepicker
            class="is-expanded"
            placeholder="Type or select a date..."
            icon="calendar-today"
            v-model="dob"
            editable
          >
          </b-datepicker>
        </b-field>

        <b-field class="pt-3">
          <b-button
            class="is-medium is-primary is-fullwidth"
            @click="submit"
            :loading="loading"
          >
            Let's Go!
          </b-button>
        </b-field>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    loading: Boolean,
  },
  data: () => ({
    name: '',
    alias: '',
    dob: null,
  }),
  methods: {
    submit() {
      this.$emit('submit', {
        name: this.name,
        alias: this.alias,
        dob: this.dob,
      });
    },
  },
};
</script>