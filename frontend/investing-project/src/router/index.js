import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import { useAuthStore } from '@/stores/login'


const routes =  [
  {
    path : '/',
    name : 'home',
    component : () => import('../views/HomePage.vue')
  },
  {
    path : '/price',
    name : 'price',
    component : () => import('../views/Price.vue'),
    meta : {requiresAuth:true}
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
  },
  {
    path : '/menu',
    name : 'menu',
    component : () => import('../views/Menu.vue')
  },
    {
        path: '/portfolios',
        name : 'portfolios',
        component : () => import('../views/Portfolios.vue')
    }
    ]



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})


router.beforeEach((to,from,next) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.isAuthenticated){
        next('/login')
        console.log("User is not authenticated, redirecting to login page")
    }
    else{
        next()
    }
})

export default router
