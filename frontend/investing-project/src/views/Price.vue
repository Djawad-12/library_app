<script setup>

import axios from "axios";
import { ref } from 'vue'
import Button from 'primevue/button';
import InputText from 'primevue/inputtext';
import Chart from 'primevue/chart';


const price = ref(0)
const ticker = ref('')
const annual_returns = ref()
const monthly_returns = ref()
const chartDataYearly = ref(null)
const chartDataMonthly = ref(null)

async function handleClick(){
    await getPrice()
    await getAnnualReturns()
    await getMonthlyReturns()
    transformChartData(annual_returns,chartDataYearly)
    transformChartData(monthly_returns,chartDataMonthly)
}

async function getPrice(){
    const response = await axios.get(
        'http://127.0.0.1:8000/api/assets/price/' + ticker.value
    );
    price.value = response.data
}

async function getAnnualReturns(){
        const response = await axios.get(
        'http://127.0.0.1:8000/api/assets/annual_returns/' + ticker.value
    );
    annual_returns.value = response.data
}

async function getMonthlyReturns(){
        const response = await axios.get(
        'http://127.0.0.1:8000/api/assets/monthly_returns/' + ticker.value
    );
    monthly_returns.value = response.data
}

function transformChartData(returns,chartData){
    const years = []
    const values = []
    for (const [key,value] of Object.entries(returns.value)){
        years.push(key)
        values.push(value)
    }
    chartData.value = {
        "labels" : years,
        "datasets" : [{
            label : "Annual returns",
            data : values
        }]
    }

}


</script>




<template>

    <br><br>

    <div id="left">
        <InputText type="text" v-model="ticker" />
        <Button label="Get Price of an asset" variant="outlined" @click="handleClick"/>
    </div>

    <div id="left">
        {{ price }}
    </div>

    {{ returns }}

    <div class="chart_container">
        <Chart class="chart1" type="bar" :data="chartDataMonthly" />
        <Chart class = "chart2" type="bar" :data="chartDataYearly" />
    </div>

 



</template>



<style scoped>


.chart_container{
    display: flex;
    width: 100%;
    gap : 5vw;
}

.chart1, .chart2{
    flex: 1;
    height: 40vh;  /* 50% of viewport height - much better than vw */
}
</style>