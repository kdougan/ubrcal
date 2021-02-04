import axios from 'axios';
import Vuex from 'vuex';
import Vue from 'vue';

Vue.use(Vuex);

export default {
  state: () => ({
    user: null,
  }),
  getters: {
    hasUser: (state) => state.user != null,
    user: (state) => state.user,
  },
  actions: {
    createUser({ commit, dispatch }, data) {
      return new Promise((resolve, reject) => {
        axios
          .post('/api/user', data)
          .then((response) => {
            dispatch('getCurrentUser').then(() => {
              resolve(response.data.data);
            });
          })
          .catch((error) => {
            commit('SET_DATA', null);
            console.log(`createUser error: ${error}`);
            reject(error);
          });
      });
    },
    getCurrentUser({ commit }) {
      return new Promise((resolve, reject) => {
        const data = {
          query: `query {
              currentUser {
                _id
                alias
                avatar
                meta {
                  name
                  dob
                }
                calendars {
                  data {
                    _id
                  }
                }
              }
            }`,
          variables: {},
        };
        axios
          .post('/graphql', data)
          .then((response) => {
            if (response.data.errors) {
              commit('SET_DATA', null);
            } else {
              commit('SET_DATA', response.data.data.currentUser);
            }
            resolve(response.data);
          })
          .catch((error) => {
            commit('SET_DATA', null);
            console.log(`getCurrentUser error: ${error}`);
            reject(error);
          });
      });
    },
  },
  mutations: {
    SET_DATA(state, data) {
      state.user = data;
    },
  },
};
