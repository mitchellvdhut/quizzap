import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/QuestionView.vue'
import CreateQuizView from "@/views/CreateQuizView.vue";
import QuizzesView from "@/views/QuizzesView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: QuizzesView,
    },
    {
      path: '/:id',
      name: 'quiz',
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
