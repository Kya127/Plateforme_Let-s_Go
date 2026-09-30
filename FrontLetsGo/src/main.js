import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './assets/styles/main.css'
import { useAuthentificationStore } from './stores/authentification'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialisation de la session JWT persistante
const storeAuth = useAuthentificationStore()
storeAuth.initialiserSession()

app.mount('#app')
