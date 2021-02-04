import axios from 'axios';
import Vuex from 'vuex';
import Vue from 'vue';

import user from './user';

Vue.use(Vuex);

const tokenName = 'ubrcal token';

export default new Vuex.Store({
  modules: { user },
  state: {},
  getters: {
    loggedIn: () => localStorage.getItem(tokenName) != null,
    token: () => localStorage.getItem(tokenName),
  },
  actions: {
    login({ commit, dispatch }, data) {
      return new Promise((resolve, reject) => {
        axios
          .post('/api/login', data)
          .then((response) => {
            const data = response.data.data;
            console.log(`data.token ${data.token}`);
            console.log(`data.user ${data.user}`);

            commit('SET_TOKEN', data.token);
            if (data.user) {
              dispatch('getCurrentUser').then(() => {
                resolve(data);
              });
            } else {
              resolve(data);
            }
          })
          .catch((error) => {
            commit('SET_TOKEN', null);
            dispatch('clearCurrentUser');
            console.log(`login error: ${error}`);
            reject(error);
          });
      });
    },
    logout({ commit }) {
      commit('REMOVE_TOKEN');
    },
  },
  mutations: {
    SET_TOKEN(_, token) {
      localStorage.setItem(tokenName, token);
    },
    REMOVE_TOKEN() {
      localStorage.removeItem(tokenName);
    },
  },
});
