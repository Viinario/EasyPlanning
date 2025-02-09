import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/Home.vue';
import FormPage from '../views/Form.vue';
import DashboardPage from '../views/Dashboard.vue';

const routes = [
  { path: '/', component: HomePage },         
  { path: '/form', component: FormPage },     
  { path: '/dashboard', component: DashboardPage } 
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
