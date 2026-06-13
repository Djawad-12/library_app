 <script setup>
import { ref, Text } from 'vue'
import { useRouter } from 'vue-router'
import {defineStore} from 'pinia'
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import InputText from 'primevue/inputtext';  
import Button from 'primevue/button';
import axios from 'axios';
import Message from 'primevue/message';
import Panel from 'primevue/panel';
import Password from 'primevue/password';
import { useAuthStore } from '@/stores/login'
const username = ref("")
const password = ref("")
const errorMessage = ref("")
const successMessage = ref("")

const authStore = useAuthStore()
const router = useRouter()

async function handleSubmit(){
    try{
        await authStore.login(username.value,password.value)
        successMessage.value = "User logged in"
        router.push('/price')
    }
    catch(error){
        errorMessage.value = error
        }
}

	

</script>


<template>  

    <br><br>
    <br><br>
    <div class="test">
        <Panel class="panel" style="text-align: center;">
            <h1 size="5"><b>Sign In</b></h1>
            
            <div>
                <br><br>
                <InputText v-model="username" placeholder="Username" class="rounded-input"></InputText>
                <br><br>
                <Password v-model="password" placeholder="Password" class="rounded-input" :feedback="false"></Password>
                <br><br>
                
                <Button @click="handleSubmit" label="Submit" class="rounded-input"></Button>

                <br><br>
                <Message v-if="errorMessage" severity="error" :life="3000" class="rounded-input">{{ errorMessage }}</Message>
                <Message v-if="successMessage" severity="success" :life="3000" class="rounded-input"> {{ successMessage }}</Message>
            </div>
        </Panel>
    </div>
</template>



<style scoped>

.fields{
    padding-right : 35vw;
    padding-left: 35vw;
    padding-top: 10vw;
    gap : 5vw;
}

.rounded-input {
    border-radius: 20px;
}

.panel{
    border-radius : 40px;
    padding-top : 1vw;
    padding-bottom: 0vw;
    
}

:deep(.p-password.rounded-input input){
    border-radius: 20px !important;
}

.test{
    padding-right: 35vw;
    padding-left : 35vw;
    padding-bottom: 10vw;
}



 </style>
