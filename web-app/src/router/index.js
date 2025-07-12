import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/components/HomePage.vue';
import WallPreview from '@/components/WallPreview.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/app',
    name: 'WallPreview',
    component: WallPreview
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
