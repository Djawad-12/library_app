<script setup>
import Panel from 'primevue/panel';
import Dropdown from 'primevue/dropdown';
import axios from 'axios'
import Card from 'primevue/card';
import { ref } from 'vue'
import Message from 'primevue/message';
import { useAuthStore } from '@/stores/login'
import InputText from 'primevue/inputtext';
import Listbox from 'primevue/listbox';
import DataView from 'primevue/dataview';
import Tag from 'primevue/tag';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';  
import Row from 'primevue/row';                   
import Dialog from 'primevue/dialog';
import { onMounted } from 'vue'
import CascadeSelect from 'primevue/cascadeselect';

const dialogPortVisible = ref(true)
const allAssets = ref([])
const dialogVisible = ref(false)
const errorMessage = ref("")
const successMessage = ref("")
const portfolios = ref([])
const name = ref("")
const initial_deposit = ref(0)
const description = ref("")
const ticker = ref()
const selected_portfolio = ref()
const CACHE_KEY = "PORTFOLIOS"
const dialogAssetVisible = ref(false)
const authStore = useAuthStore()
const quantity = ref()


onMounted(() => {
    getPortfolio()
    getAssets()
    dialogPortVisible.value = false
    dialogAssetVisible.value = false
    dialogVisible.value = false
})

async function getPortfolio(){
    try{
        if(!authStore.token){
            errorMessage.value = "NOT LOGGED IN"
            return
        }
        const cached = JSON.parse(localStorage.getItem(CACHE_KEY))
        if(cached){
            portfolios.value = cached
            console.log("Loaded from cache")
            return
        }
        const response = await axios.get("http://127.0.0.1:8000/api/portfolios/current",{
            headers:{
                'Authorization' : 'Bearer ' + authStore.token
            }
    })
    localStorage.setItem(CACHE_KEY,JSON.stringify(response.data))
    portfolios.value = response.data
    console.log("portfolios fetched successfully " + portfolios.value.length.toString())
    }
    catch(error){
        errorMessage.value = error
    }
}

async function createPortfolio(){
    try{
        if(!authStore.token){
            errorMessage.value = "NOT LOGGED IN"
            return
        }

        if(name.value==="" || initial_deposit.value===0){
            errorMessage.value = "One the fields is missing"
            return
        }

        const response = await axios.post("http://127.0.0.1:8000/api/portfolios/",{
            name : name.value,
            initial_deposit : initial_deposit.value,
            description : description.value
        },
        {headers:{
                'Authorization' : 'Bearer ' + authStore.token
            }
        })
        localStorage.removeItem(CACHE_KEY)
        successMessage.value = "Portfolio created successfully"
        dialogVisible.value = false
        await getPortfolio()
    }
    catch(error){
        errorMessage.value = error
    }
}



async function addAsset() {
    try {
        if (!authStore.token) {
            errorMessage.value = "NOT LOGGED IN"
            return
        }
        if (ticker.value === "" || !selected_portfolio.value || quantity.value=== 0) {
            errorMessage.value = "One of the fields is empty"
            return
        }
        
        const endpoint = "http://127.0.0.1:8000/api/portfolios/current/" 
            + selected_portfolio.value.id + "/" 
            + ticker.value + "/" 
            + quantity.value
        
        const response = await axios.put(endpoint, null, {
            headers: {
                'Authorization': `Bearer ${authStore.token}`
            }
        })
        localStorage.removeItem("PORTFOLIOS")
        await getPortfolio()
        successMessage.value = "Asset added successfully"
        dialogAssetVisible.value = false
        ticker.value = ""
        quantity.value = 0
    } catch (error) {
        errorMessage.value = error.response
    }
}


async function getAssets(){
    try{
        if(!authStore.token){
            errorMessage.value = "NOT LOGGED IN"
        }
        console.log("TEST LOGGED")
        const cached = JSON.parse(localStorage.getItem("ASSETS"))
        if(cached){
            console.log("Assets loaded from cache")
            allAssets.value = cached
            return
        }
        console.log("TEST DDD")
        console.log("API CALL")
        const response = await axios.get("http://127.0.0.1:8000/api/assets/",{
            headers:{
                "Authorization" : 'Bearer ' + authStore.token
            }
        })
        allAssets.value = response.data
        localStorage.setItem("ASSETS",JSON.stringify(response.data))
        successMessage.value = "Assets loaded successfully"
        }   
    catch(error){
        console.log(error.response)
        errorMessage.value = error
    }
}

</script>



<template>

<div>
    <div class="create">
        <Button class="button" label="Create Portfolio" @click="dialogVisible=true"></Button>
    </div>
    <Dialog v-model:visible="dialogVisible" modal header="New Portfolio" :style="{ width: '25rem'}">
        <span class="text-surface-500 dark:text-surface-400 block mb-8">Let's get more rich</span>
        <div class="flex items-center gap-4 mb-4">
            <label for="name" class="font-semibold w-24">Name</label>
            <InputText id="name" v-model="name" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4 mb-4">
            <label for="initial_deposit" class="font-semibold w-24">Initial Deposit</label>
            <InputText id="initial_deposit" v-model="initial_deposit" class="flex-auto" autocomplete="off" />
        </div>
        <div class="flex items-center gap-4 mb-8">
            <label for="description" class="font-semibold w-24">Description</label>
            <InputText id="description" v-model="description" class="flex-auto" autocomplete="off" />
        </div> 
        <div class="flex justify-end gap-2">
            <Button class="button" type="button" label="Cancel" severity="secondary" @click="dialogVisible = false"></Button>
            <Button class="button" type="button" label="Save" @click="createPortfolio"></Button>
        </div>
        <br>
        <Message v-if="errorMessage" severity="error" :life="3000" class="rounded-input">{{ errorMessage }}</Message>
        <Message v-if="successMessage" severity="success" :life="3000" class="rounded-input"> {{ successMessage }}</Message>
    </Dialog>

        
    <div class="container" style="text-align: center;" > 
       
    <Card v-for="portfolio in portfolios" :key="portfolio.id" class="card" style="width: 25rem; overflow: hidden">
        <template #header>
            <img alt="user header" src="https://primefaces.org/cdn/primevue/images/usercard.png" />
        </template>
        <template #title>
            <b>{{ portfolio.name }}</b>
        </template>
        <template #subtitle>
            <b>Amount: {{ portfolio.amount }}</b>
        </template>
        <template #content>
            <p class="m-0">
                {{ portfolio.description || 'No description available.' }}
            </p>
        </template>
        <template #footer>
            <div class="flex gap-4 mt-1">
                <Button label="Manage Portfolio" severity="secondary" variant="outlined" class="button w-full" @click="dialogPortVisible=true; selected_portfolio=portfolio" />
                <Button class="button w-full" label="Add Asset" @click="dialogAssetVisible=true; selected_portfolio=portfolio" />
            <Dialog v-model:visible="dialogAssetVisible" modal header="Add asset to portfolio" :style="{ width: '25rem'}">
                <span class="text-surface-500 dark:text-surface-400 block mb-8">Let's get more rich</span>
                <div class="flex items-center gap-4 mb-4">
                    <label for="ticker" class="font-semibold w-24">Asset Name</label> 
                    <Dropdown class="flex-auto" v-model="ticker" :options="allAssets" optionLabel="name" optionValue="ticker" placeholder="Select a ticker" :virtualScrollerOptions="{ itemSize : 38 }" showClear></Dropdown>
                    
                    <h1>{{ ticker }}</h1>
                </div>
                <div class="flex items-center gap-4 mb-8">
                    <label for="quantity" class="font-semibold w-24">Quantity</label>
                    <InputText id="quantity" v-model="quantity" class="flex-auto" autocomplete="off" />

                </div>
                <div class="flex justify-end gap-2">
                    <Button class="button" type="button" label="Cancel" severity="secondary" @click="dialogAssetVisible = false"></Button>
                    <Button class="button" type="button" label="Add" @click="addAsset"></Button>
                </div>
                <br>
                <Message v-if="errorMessage" severity="error" class="rounded-input">{{ errorMessage }}</Message>
                <Message v-if="successMessage" severity="success" class="rounded-input"> {{ successMessage }}</Message>
            </Dialog>


            <Dialog v-model:visible="dialogPortVisible" modal header="Add asset to portfolio" :style="{ width: '80rem', height: '80rem'}">
                <span class="text-surface-500 dark:text-surface-400 block mb-8">Let's get more rich</span>
                <div class="flex items-center gap-4 mb-4">
                    
                </div>
                <div class="flex items-center gap-4 mb-8">
                    <h1>{{ selected_portfolio }}</h1>
                </div>
                <div class="flex justify-end gap-2">
                    <Button class="button" type="button" label="Cancel" severity="secondary" @click="dialogPortVisible = false"></Button>
                </div>
                <br>
                <Message v-if="errorMessage" severity="error" class="rounded-input">{{ errorMessage }}</Message>
                <Message v-if="successMessage" severity="success" class="rounded-input"> {{ successMessage }}</Message>
            </Dialog>
            </div>
        </template>
    </Card>
    
    </div>
</div>

</template>


<style scoped>
.container {
    flex-wrap : wrap;
    display : flex;
    width: 100%;
    padding-top: 2vw;
    padding-bottom : 10vw;
    gap : 5vw;
    justify-content : center;
}


.button{
   border-radius : 40px; 
}

.card{
    width:60%;
}

.p-card{
    width:2%
}

.create{
    padding-top : 2vw;
    display : flex;
    justify-content : right;
    padding-right : 5vw;
}

</style>
