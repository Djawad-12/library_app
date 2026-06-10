import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'

const routes =  [
  {
    path : '/',
    name : 'home',
    component : () => import('../views/HomePage.vue')
  },
  {
    path : '/price',
    name : 'price',
    component : () => import('../views/Price.vue')
  },
  {
    path : '/register',
    name : 'register',
    component : () => import('../views/Register.vue')
  },
  {
    path : '/login',
    name : 'login',
    component : () => import('../views/Login.vue')
  }
]



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
