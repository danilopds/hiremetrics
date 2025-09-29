<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
        <h2 class="text-2xl font-bold text-gray-900 mb-2">
          {{ loading ? 'Entrando...' : error ? 'Erro no Login' : 'Login Realizado!' }}
        </h2>
        <p class="text-gray-600">
          {{
            loading
              ? 'Processando seu login com Google...'
              : error || 'Redirecionando para o dashboard...'
          }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { useMessage } from 'naive-ui'

  const router = useRouter()
  const route = useRoute()
  const authStore = useAuthStore()
  const message = useMessage()

  const loading = ref(true)
  const error = ref('')

  onMounted(async () => {
    try {
      // Check for error in the URL
      if (route.query.error) {
        error.value = `Erro na autenticação Google: ${route.query.error}`
        loading.value = false

        // Redirect to login page after error
        setTimeout(() => {
          router.push('/auth/login')
        }, 3000)
        return
      }

      const token = route.query.token

      if (!token) {
        error.value = 'Token de autenticação não encontrado'
        loading.value = false

        // Redirect to login page after error
        setTimeout(() => {
          router.push('/auth/login')
        }, 3000)
        return
      }

      // Set the token in the auth store
      authStore.setToken(token)

      // Check if the token is valid by checking authentication status
      if (!authStore.isAuthenticated) {
        error.value = 'Token de autenticação inválido'
        loading.value = false

        // Redirect to login page after error
        setTimeout(() => {
          router.push('/auth/login')
        }, 3000)
        return
      }

      try {
        // Get user data
        const userData = await authStore.getCurrentUser()
        authStore.setUser(userData)

        message.success('Login com Google realizado com sucesso!')

        // Redirect to dashboard
        setTimeout(() => {
          router.push('/dashboard')
        }, 1000)
      } catch (userError) {
        console.error('Error getting user data:', userError)

        // If we can't get user data but have a valid token, still redirect to dashboard
        // The app will try to get user data again when needed
        message.warning('Login realizado, mas não foi possível obter dados do usuário')

        setTimeout(() => {
          router.push('/dashboard')
        }, 1000)
      }
    } catch (err) {
      console.error('Google callback error:', err)

      // Try to parse error message if it's JSON
      if (err.response && err.response.data) {
        error.value =
          err.response.data.detail || 'Erro ao processar login com Google. Tente novamente.'
      } else if (err.message && err.message.includes('detail')) {
        try {
          const errorJson = JSON.parse(err.message.substring(err.message.indexOf('{')))
          error.value = errorJson.detail || 'Erro ao processar login com Google. Tente novamente.'
        } catch (e) {
          error.value = 'Erro ao processar login com Google. Tente novamente.'
        }
      } else {
        error.value = err.message || 'Erro ao processar login com Google. Tente novamente.'
      }

      loading.value = false

      // Redirect to login page after error
      setTimeout(() => {
        router.push('/auth/login')
      }, 5000)
    }
  })
</script>
