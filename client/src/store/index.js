import axios from 'axios';
import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex);

const state = {
  token: null,
  user: null,
};

const getters = {
  user(state) {
    return state.user;
  },
};

const actions = {
  login({ commit }, data) {
    const formData = new FormData();
    formData.append('username', data.username);
    formData.append('password', data.password);
    axios
      .post('/api/login', formData)
      .then((response) => {
        const data = response.data;
        console.log(response.data);
        commit('SET_TOKEN', data.token);
        commit('SET_USER', data.user);
      })
      .catch((error) => {
        commit('SET_TOKEN', null);
        commit('SET_USER', null);
        console.log(`login error: ${error}`);
      });
  },
  createUser({ commit }, data) {
    const formData = new FormData();
    formData.append('alias', data.alias);
    formData.append('dob', data.dob);
    formData.append('public', data.public);
    axios
      .post('/api/user')
      .then((response) => {
        commit('SET_USER', response.data);
      })
      .catch((error) => {
        commit('SET_USER', null);
        console.log(`createUser error: ${error}`);
      });
  },
};

const mutations = {
  SET_USER(state, user) {
    state.user = user;
  },
  SET_TOKEN(state, token) {
    state.token = token;
  },
};

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations,
});
