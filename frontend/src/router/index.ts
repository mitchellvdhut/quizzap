import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/QuestionView.vue'
import CreateQuizView from "@/views/CreateQuizView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/create',
      name: 'create',
      component: CreateQuizView,
    },
  ],
})

export default router
