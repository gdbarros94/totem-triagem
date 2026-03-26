import { createRouter, createWebHistory } from 'vue-router'
import TotemLayout from '../layouts/TotemLayout.vue'
import AdminLayout from '../layouts/AdminLayout.vue'

const routes = [
  {
    path: '/',
    redirect: '/totem'
  },
  {
    path: '/totem',
    component: TotemLayout,
    children: [
      { path: '', component: () => import('../pages/totem/TotemFlow.vue') }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', component: () => import('../pages/admin/AdminDashboard.vue') },
      { path: 'prompt', component: () => import('../pages/admin/PromptSettings.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
