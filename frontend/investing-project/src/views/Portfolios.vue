<script setup>
import Panel from 'primevue/panel';
import axios from 'axios'
import { ref } from 'vue'
import { useAuthStore } from '@/stores/login'
import InputText from 'primevue/inputtext';
import Listbox from 'primevue/listbox';
import DataView from 'primevue/dataview';
import 'primeflex/primeflex.css'
import 'primeicons/primeicons.css'
import Tag from 'primevue/tag';
import Button from 'primevue/button';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';  
import Row from 'primevue/row';                   

const errorMessage = ref("")
const successMessage = ref("")
const portfolios = ref([])
const name = ref("")
const initial_deposit = ref(0)
const description = ref("")
const ticker = ref("")
const selected_portfolio = ref()


const authStore = useAuthStore()

async function getPortfolio(){
    try{
        if(!authStore.token){
            errorMessage.value = "NOT LOGGED IN"
            return
        }

        const response = await axios.get("http://127.0.0.1:8000/api/portfolios/current",{
            headers:{
                'Authorization' : 'Bearer ' + authStore.token
            }
    })
    successMessage.value = "portfolios fetched successfully " + portfolios.value.length.toString()
    portfolios.value = response.data
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

        const response = axios.post("http://127.0.0.1:8000/api/portfolios/",{
            name : name.value,
            initial_deposit : initial_deposit.value,
            description : description.value
        },
        {headers:{
                'Authorization' : 'Bearer ' + authStore.token
            }
        })
    }
    catch(error){
        errorMessage.value = error
    }
}




async function addAsset(){
    try{
        if(!authStore.token){
            errorMessage.value = "NOT LOGGED IN "
            return
        }
        if(ticker.value==="" || portfolio_id.value===0){
            errorMessage.value = "One of the fields is empty"
        }
        const endpoint = "http://127.0.0.1:8000/api/portfolios/" + portfolio_id + "/" + ticker.value 
        const response = axios.get(endpoint,{
            portfolio_id : portfolio_id.value,
            ticker : ticker.value
        },
        {
            headers:{
                'Authorization' : 'Bearer ' + authStore.token
            }
        })
        successMessage.value = "Asset added successfully"
    }
    catch(error){
        errorMessage.value = error
    }
}

</script>



<template>

<div>
    <h1>{{ errorMessage }}</h1>
    <h1>{{ successMessage }}</h1>
    <button @click="getPortfolio">TEST</button>
    

    <InputText v-model="name">NAME</InputText>
    <InputText v-model="initial_deposit">INITIAL DEPOSIT</InputText>
    <InputText v-model="description">DESCRIPTION</InputText>
    <button @click="createPortfolio">CREATE</button>
        
        
    <Listbox v-model=selected_portfolio :options="portfolios" optionLabel="name"></Listbox>
        

    <DataTable v-if="selected_portfolio" :value="[selected_portfolio]" >
        <Column field="name" header="Name">{{ selected_portfolio.name }}</Column>
        <Column field="amount" header = "Amount"></Column>
        <Column field="initial_deposit" header="Initial Deposit"></Column>
        <Column v-if="description != ''" field="description" header="Description"></Column>
    </DataTable>
        



<div class="container" style="text-align: center;">
    <Panel class="panel", style="text-align: center ;"><h1><b>Portfolios</b></h1>

    <DataView :value="portfolios" layout="list" class="data">
       <template #list="slotProps">
                <div v-for="(item, index) in slotProps.items" :key="index">
                    <div class="flex flex-col sm:flex-row sm:items-center p-6 gap-4" :class="{ 'border-t border-surface-200 dark:border-surface-700': index !== 0 }">
                            <div class="absolute bg-black/70 rounded-border" style="left: 4px; top: 4px">
                            </div>
                        </div>
                        <div class="flex flex-col md:flex-row justify-between md:items-center flex-1 gap-6">
                            <div class="flex flex-row md:flex-col justify-between items-start gap-2">
                                <div>
                                    <span class="font-medium text-surface-500 dark:text-surface-400 text-sm"><h1><b>{{ item.name }}</b></h1></span>
                                </div>
                                <div class="bg-surface-100 p-1" style="border-radius: 30px">
                                    <div class="bg-surface-0 flex items-center gap-2 justify-center py-1 px-2" style="border-radius: 30px; box-shadow: 0px 1px 2px 0px rgba(0, 0, 0, 0.04), 0px 1px 2px 0px rgba(0, 0, 0, 0.06)">
                                        <span class="text-surface-900 font-medium text-sm">{{ item.initial_deposit }}</span>
                                        <i class="pi pi-star-fill text-yellow-500"></i>
                                </div>
                            </div>
                            <div class="flex flex-col md:items-end gap-8">
                                <span class="text-xl font-semibold">${{ item.amount }}</span>
                                <div class="flex flex-row-reverse md:flex-row gap-2">
                                    <Button icon="pi pi-heart" variant="outlined"></Button>
                                    <Button icon="pi pi-shopping-cart" label="Buy Now"  class="flex-auto md:flex-initial whitespace-nowrap"></Button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        </template>
    </DataView>
</Panel>

</div>
</div>

</template>



<style scoped>


.container {
    display: flex;
    justify-content: flex-start;  /* Align to left */
    width: 50%;
    padding-top : 5vw;

}

.panel {
    width: 100%;
    max-width: 500px;
    border-radius : 30px;
}

/* Use :deep() to style DataView internals */
:deep(.p-dataview) {
    width: 100%;
}

:deep(.p-dataview-list) {
    display: flex !important;
    flex-direction: column !important;
}

</style>
