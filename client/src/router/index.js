import Vue from 'vue';
import Router from 'vue-router';

import store from '../store';

Vue.use(Router);

const routes = [
  {
    path: '*',
    redirect: { name: 'index' },
  },
  {
    path: '/',
    name: 'index',
    component: () =>
      import(
        /* webpackChunkName: 'index' */
        '../components/pages/Index.vue'
      ),
  },
  {
    path: '/login',
    name: 'login',
    component: () =>
      import(
        /* webpackChunkName:  'login'*/
        '../components/pages/Login'
      ),
  },
  {
    path: '/new-user',
    name: 'createUser',
    component: () =>
      import(
        /* webpackChunkName:  'createUser'*/
        '../components/pages/CreateUser'
      ),
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: '/new-account',
    name: 'createAccount',
    component: () =>
      import(
        /* webpackChunkName:  'createAccount'*/
        '../components/pages/CreateAccount'
      ),
  },
  {
    path: '/calendar',
    name: 'calendar',
    component: () =>
      import(
        /* webpackChunkName:  'calendar'*/
        '../components/pages/Calendar'
      ),
    meta: {
      requiresAuth: true,
      requiresUser: true,
    },
  },
];

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const requiresUser = to.matched.some((record) => record.meta.requiresUser);
  const loggedIn = store.getters.loggedIn;
  const hasUser = store.getters.hasUser;
  console.table({
    requiresAuth,
    requiresUser,
    loggedIn: store.getters.loggedIn,
    hasUser: store.getters.hasUser,
  });
  if (loggedIn && to.name === 'index') next({ name: 'createUser' });
  if (loggedIn && hasUser && to.name !== 'calendar') next({ name: 'calendar' });
  if (requiresAuth && !loggedIn && to.name !== 'login') next({ name: 'login' });
  if (requiresUser && !hasUser && to.name !== 'createUser')
    next({ name: 'createUser' });
  next();
});

export default router;
