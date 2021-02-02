import Vue from 'vue';
import App from './App.vue';

import Buefy from 'buefy';
import '/src/style/ubrcal.scss';

import '@mdi/font/css/materialdesignicons.css';

import store from './store';

Vue.config.productionTip = false;

Vue.use(Buefy);

new Vue({
  store,
  render: (h) => h(App),
}).$mount('#app');
