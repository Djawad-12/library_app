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




