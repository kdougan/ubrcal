import Vue from 'vue';
import App from './App.vue';
import Buefy from 'buefy';
import '/src/style/ubrcal.scss';

import '@mdi/font/css/materialdesignicons.css';

import store from './store';
import router from './router';

import axios from 'axios';

const tokenName = 'ubrcal token';

axios.interceptors.request.use(
  (config) => {
    let token = localStorage.getItem(tokenName);
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

Vue.config.productionTip = false;

Vue.use(Buefy);

new Vue({
  store,
  router,
  render: (h) => h(App),
}).$mount('#app');
