import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import naive from 'naive-ui'
import { useAuthStore } from './stores/auth'

// Import Tailwind CSS
import './assets/tailwind.css'

// Create Vue app instance
const app = createApp(App)

// Create Pinia instance
const pinia = createPinia()

// Use plugins
app.use(pinia)
app.use(router)
app.use(naive)

// Initialize 
const authStore = useAuthStore(pinia)

if (authStore.isAuthenticated) {
  console.log('App: User is authenticated...')
}

// Error handling
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue Error:', err)
  console.error('Error Info:', info)
}

// Mount app
app.mount('#app')
