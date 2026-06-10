<script setup>
import { ref, Text } from 'vue'

import {defineStore} from 'pinia'
import InputGroup from 'primevue/inputgroup';
import InputGroupAddon from 'primevue/inputgroupaddon';
import InputText from 'primevue/inputtext';  
import Button from 'primevue/button';
import axios from 'axios';
import Message from 'primevue/message';
import Panel from 'primevue/panel';
import Password from 'primevue/password';

const username = ref("")
const password = ref("")
const errorMessage = ref("")
const successMessage = ref("")


const useAuthStore = defineStore('auth',{
    state : () => ({
        user : null,
        isAuthentificated : false,
        accessToken : null
    }),

    actions : {
        
            async login(credentials){
                try{
                    const response = await axios.post("http://127.0.0.1:8000/api/user/token",credentials, {
                        withCredentials : true
                    })
                    this.user = response.data.user
                    this.isAuthentificated = true 
                    this.accessToken = response.data.accessToken

                    }
                }
                catch (error) {
                    throw new Error("login failed")
                }
            }
        

    }
})

async function loginUser(){
    errorMessage.value = ""
    if (username.value ==="" || password.value === ""){
        errorMessage.value = "One of the fields is empty"
        return
    }
    try{
        const response = await axios.post("http://127.0.0.1:8000/api/user/",{
            username : username.value,
            password : password.value
        })
        successMessage.value = "Your account was successfully created"

        //email.value = ""
        //username.value = ""
        //password.value = ""
    }
    catch(error){
        if(error.response.status === 409){
            errorMessage.value = error.response.data.detail
        }
        else if(error.response.status === 422
            && (error.response.data.detail[0].msg === "value is not a valid email address: An email address must have an @-sign."
            || error.response.data.detail[0].msg === "value is not a valid email address: An email address cannot have a period immediately after the @-sign."
        )){
            errorMessage.value = "Email adress is not correct"
        }
        else if(error.response.status === 422
            && error.response.data.detail[0].msg === "String should have at least 8 characters"
        ){
            errorMessage.value = "Password should have at least 8 characters"
        }

        

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
                <Password v-model="password" placeholder="Password" class="rounded-input"></Password>
                <br><br>
                
                <Button @click="loginUser" label="Submit" class="rounded-input"></Button>
                
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