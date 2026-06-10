import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 1. Import your existing router file

// PrimeVue Imports
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import { definePreset } from '@primeuix/themes';
import Ripple from 'primevue/ripple';
import { createPinia } from 'pinia';

const app = createApp(App);

// 2. Define your Custom slate Theme
const MyPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{slate.50}',
            100: '{slate.100}',
            200: '{slate.200}',
            300: '{slate.300}',
            400: '{slate.400}',
            500: '{slate.500}',
            600: '{slate.600}',
            700: '{slate.700}',
            800: '{slate.800}',
            900: '{slate.900}',
            950: '{slate.950}'
        }
    }
});



// 3. Use PrimeVue with your theme and enable ripple
app.use(PrimeVue, {
    theme: {
        preset: MyPreset
    },
    ripple: true 
});

// 4. Register the Ripple directive
app.directive('ripple', Ripple);

// 5. Tell Vue to use your imported router
app.use(router); 

app.use(createPinia())

// 6. Finally, mount the app
app.mount('#app');