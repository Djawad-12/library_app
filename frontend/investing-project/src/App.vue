<script setup>
import Button from 'primevue/button'
import InputText from 'primevue/inputtext';
import { ref, onMounted} from 'vue'
import { Form } from '@primevue/forms';
import Menubar from 'primevue/menubar';
import Toolbar from 'primevue/toolbar';
import axios from 'axios';
import { useAuthStore } from '@/stores/login'
import { useRouter } from 'vue-router'
   
const router = useRouter()

const menuData = [
  {label : 'Home',route : '/'},
  {label : 'Sign Up',route : '/register'},
  {label : 'Login', route :'/login'},

]

const MenuDataLogged = [
  {label : 'Price', route : '/price'},
  {label : 'Portfolios', route : '/portfolios'},
  {label : 'Logout', route : '/'}
]



const authStore = useAuthStore()

async function isLogged(){
       authStore.checkAuth()
   
}

async function handleLogOut(){
    authStore.logout()
    router.push("/")
}


</script>

<template>




<div>
  <Menubar v-if="authStore.isAuthenticated" :model="MenuDataLogged" class = 'rounded-input'>
    <template #start>
    </template>
    <template #item="{item, props, hasSubmenu, root}">
        <a class=rounded-input v-if="item.route === '/'" @click="handleLogOut" custom>
            <span><b>{{ item.label }}</b></span>
            
        </a>

        <router-link class=rounded-input v-if="item.route != '/'" v-slot="{href, navigate, isActive}" :to="item.route" custom>
      
          <a v-ripple :class="['flex items-center', { 'active-link': isActive }]" 
             v-bind="props.action" 
             @click="navigate">
            <span><b>{{ item.label }}</b></span>
          </a>
      </router-link>

    </template>
  </Menubar>



      <Menubar v-else :model="menuData" class = 'rounded-input'>
    <template #start>
    </template>
    <template #item="{item, props, hasSubmenu, root}">
      <router-link class=rounded-input v-if="item.route" v-slot="{href, navigate, isActive}" :to="item.route" custom>
      
          <a v-ripple :class="['flex items-center', { 'active-link': isActive }]" 
             v-bind="props.action" 
             @click="navigate">
            <span><b>{{ item.label }}</b></span>
          </a>
      </router-link>

    </template>
  </Menubar>


</div>


<router-view />
</template>






<style>
body {
    padding-left: 2vw;
    padding-right: 2vw;
    padding-top: 2vw;
    font-family: 'Courier New', Courier, monospace;
    background-color: black;
    color: var(--p-primary-color);
    margin: 0;
    min-height: 100vh;
}

/* Base styles for labels and text elements */
label, 
.p-dialog-header, 
.p-panel-title, 
.p-card-title, 
.p-card-subtitle, 
.p-card-content, 
.p-card-footer {
    color: var(--p-primary-color) !important;
}

/* Menubar & Navigation Links */
.p-menubar {
    border-radius: 40px !important;
    background-color: black !important;
    border: 2px solid var(--p-primary-color) !important;
}

.p-menubar .p-menubar-item-link {
    color: var(--p-primary-color) !important;
}

/* This is your new active state class for router-link */
.active-link {
    background-color: var(--p-primary-color) !important;
    border-radius: 8px;
    color: black !important;
}

/* Ensure ALL text inside an active link is black */
.active-link, 
.active-link span, 
.active-link b, 
.active-link i {
    color: black !important;
}

/* Menubar hover/focus states */
.p-menubar .p-menubar-item-content:hover,
.p-menubar .p-menubar-item-content.p-focus,
.p-menubar .p-menubar-item-link:hover {
    background-color: var(--p-primary-color) !important;
}

.p-menubar .p-menubar-item-content:hover span,
.p-menubar .p-menubar-item-content.p-focus span,
.p-menubar .p-menubar-item-link:hover span,
.p-menubar .p-menubar-item-content:hover b,
.p-menubar .p-menubar-item-content.p-focus b,
.p-menubar .p-menubar-item-link:hover b {
    color: black !important;
}

/* Inputs and interactive components */
.p-inputtext, 
.p-password input, 
.p-select, 
.p-dropdown {
    background-color: black !important;
    color: var(--p-primary-color) !important;
    border: 1px solid var(--p-primary-color) !important;
}

.p-panel, 
.p-card, 
.p-dialog-content, 
.p-dialog-header {
    background-color: black !important;
    color: var(--p-primary-color) !important;
    border: 1px solid var(--p-primary-color) !important;
}

/* Buttons */
.p-button {
    font-family: 'Courier New', Courier, monospace;
    background-color: black !important;
    border: 1px solid var(--p-primary-color) !important;
    color: var(--p-primary-color) !important;
}

.p-button:hover, 
.p-button:focus, 
.p-button:active {
    background-color: var(--p-primary-color) !important;
    color: black !important;
}

/* Specific fix for PrimeVue components that use grey/white by default */
* {
    border-color: var(--p-primary-color);
}

.rounded-input {
    border-radius: 20px;
}
</style>
