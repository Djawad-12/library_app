import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 1. Import your existing router file

// Styles
import './assets/main.css';
import 'primeicons/primeicons.css';

// PrimeVue Imports
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import { definePreset } from '@primevue/themes';
import Ripple from 'primevue/ripple';
import { createPinia } from 'pinia';

const app = createApp(App);

// 2. Define your Custom slate Theme
const MyPreset = definePreset(Aura, {
    semantic: {
        primary: {
            50: '{green.50}',
            100: '{green.100}',
            200: '{green.200}',
            300: '{green.300}',
            400: '{green.400}',
            500: '{green.500}',
            600: '{green.600}',
            700: '{green.700}',
            800: '{green.800}',
            900: '{green.900}',
            950: '{green.950}'
        },
        colorScheme: {
            dark: {
                surface: {
                    0: '#000000',
                    50: '#020202',
                    100: '#050505',
                    200: '#080808',
                    300: '#0a0a0a',
                    400: '#0d0d0d',
                    500: '#111111',
                    600: '#141414',
                    700: '#171717',
                    800: '#1a1a1a',
                    900: '#1d1d1d',
                    950: '#202020'
                },
                primary: {
                    color: '{primary.500}',
                    inverseColor: '#000000',
                    hoverColor: '{primary.400}',
                    activeColor: '{primary.300}'
                }
            }
        }
    },
    components: {
        button: {
            colorScheme: {
                dark: {
                    root: {
                        background: 'transparent',
                        color: '{primary.color}',
                        border: {
                            color: '{primary.color}'
                        }
                    },
                    outlined: {
                        color: '{primary.color}',
                        border: {
                            color: '{primary.color}'
                        }
                    },
                    secondary: {
                        background: 'transparent',
                        color: '{primary.color}',
                        border: {
                            color: '{primary.color}'
                        }
                    }
                }
            }
        },
        menubar: {
            colorScheme: {
                dark: {
                    root: {
                        background: '#000000',
                        border: {
                            color: '{primary.color}'
                        }
                    },
                    item: {
                        color: '{primary.color}',
                        focus: {
                            background: '{primary.color}',
                            color: '#000000'
                        }
                    }
                }
            }
        },
        inputtext: {
            colorScheme: {
                dark: {
                    root: {
                        background: '#000000',
                        color: '{primary.color}',
                        border: {
                            color: '{primary.color}'
                        }
                    }
                }
            }
        }
    }
});



// 3. Use PrimeVue with your theme and enable ripple
app.use(PrimeVue, {
    theme: {
        preset: MyPreset,
        options: {
            darkModeSelector: '.my-app-dark'
        }
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
