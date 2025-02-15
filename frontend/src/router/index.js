import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/Home.vue';
import FormPage from '../views/Form.vue';
import DashboardPage from '../views/Dashboard.vue';
import RespondForm from '../views/RespondForm.vue';
import AnswerForm from '@/views/AnswerForm.vue';

const routes = [
  { path: '/', component: HomePage },         
  { path: '/form', component: FormPage },     
  { path: "/form/:id", component: FormPage, props: true },
  { path: "/dashboard", component: DashboardPage },
  { path: "/respond", component: RespondForm },
  { path: "/answer/:id", component: AnswerForm, props: true },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
