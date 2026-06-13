<script setup>
import Button from 'primevue/button'
import InputText from 'primevue/inputtext';
import { ref, onMounted} from 'vue'
import { Form } from '@primevue/forms';
import Menubar from 'primevue/menubar';
import Toolbar from 'primevue/toolbar';
import axios from 'axios';


const menuData = [
  {label : 'Price',route : '/price'}
]


</script>

<template>



    
<div>
  <Menubar :model="menuData" class = 'rounded-input'>
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
    font-family:sans-serif;
}

/* This is your new active state class */
.active-link {
    background-color: var(--p-primary-color) !important;
    color: white !important;
    border-radius: 8px; /* Optional: adds nice rounded corners inside the menu */
}

/* Make sure the text color stays white even when hovered */
.active-link span {
    color: rgb(13, 12, 12) !important;
}

.rounded-input {
    border-radius: 20px;
}

:deep(.rounded-input input) {
    border-radius: 20px;
}

.p-menubar.rounded-input {
    border-radius: 40px !important;
}



</style>
