<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />

    <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Acessar Plataforma
          </h2>
        </div>

        <!-- Google OAuth Button - Now at the top -->
        <div class="mt-8">
          <button
            type="button"
            :disabled="googleLoading"
            class="group relative w-full flex justify-center py-3 px-4 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 shadow-md transition-all duration-200 hover:shadow-lg"
            @click="handleGoogleLogin"
          >
            <svg
              v-if="!googleLoading"
              class="w-6 h-6 mr-2"
              viewBox="0 0 24 24"
            >
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            <span
              v-if="googleLoading"
              class="text-base"
            >Entrando com Google...</span>
            <span
              v-else
              class="text-base font-medium"
            >Entrar com Google</span>
          </button>
        </div>

        <!-- Divider -->
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300" />
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-gray-50 text-gray-500">Ou entre com email</span>
          </div>
        </div>

        <form
          class="space-y-6"
          @submit.prevent="handleSubmit"
        >
          <div class="rounded-md shadow-sm -space-y-px">
            <div>
              <label
                for="email"
                class="sr-only"
              >Endereço de email</label>
              <input
                id="email"
                v-model="formData.email"
                name="email"
                type="email"
                required
                class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Endereço de email"
              >
            </div>
            <div>
              <label
                for="password"
                class="sr-only"
              >Senha</label>
              <input
                id="password"
                v-model="formData.password"
                name="password"
                type="password"
                required
                class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Senha"
              >
            </div>
          </div>

          <div class="flex items-center justify-end">
            <div class="text-sm">
              <router-link
                to="/auth/forgot-password"
                class="font-medium text-blue-600 hover:text-blue-500"
              >
                Esqueceu sua senha?
              </router-link>
            </div>
          </div>

          <div class="mt-4">
            <button
              type="submit"
              :disabled="loading"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              <span v-if="loading">Entrando...</span>
              <span v-else>Entrar</span>
            </button>
          </div>

          <div>
            <p class="mt-2 text-center text-sm text-gray-600">
              Ou
              <router-link
                to="/auth/register"
                class="font-medium text-indigo-600 hover:text-indigo-500"
              >
                crie uma nova conta
              </router-link>
            </p>
          </div>

          <div
            v-if="error"
            class="text-red-500 text-sm text-center"
          >
            <p>{{ error }}</p>
            <div
              v-if="showResendVerification"
              class="mt-3"
            >
              <p class="text-gray-600 text-xs mb-2">
                Não recebeu o email de verificação?
              </p>
              <button
                type="button"
                :disabled="resendLoading"
                class="text-blue-600 hover:text-blue-500 text-sm font-medium"
                @click="handleResendVerification"
              >
                <span v-if="resendLoading">Enviando...</span>
                <span v-else>Reenviar email de verificação</span>
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, reactive } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { useMessage } from 'naive-ui'
  import NavBar from '@/components/NavBar.vue'

  defineOptions({
    name: 'LoginPage',
  })

  const router = useRouter()
  const authStore = useAuthStore()
  const message = useMessage()

  const formData = reactive({
    email: '',
    password: '',
  })

  const loading = ref(false)
  const googleLoading = ref(false)
  const error = ref('')
  const showResendVerification = ref(false)
  const resendLoading = ref(false)
  const unverifiedEmail = ref('')

  const handleSubmit = async () => {
    try {
      loading.value = true
      error.value = ''
      showResendVerification.value = false
      unverifiedEmail.value = ''
      await authStore.login(formData.email, formData.password)
      message.success('Login realizado com sucesso!')
      router.push('/dashboard')
    } catch (err) {
      console.error('Login error:', err)
      if (err.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        if (
          err.response.status === 403 &&
          err.response.data.detail &&
          typeof err.response.data.detail === 'object'
        ) {
          // Handle unverified email error
          const errorDetail = err.response.data.detail
          if (errorDetail.code === 'EMAIL_NOT_VERIFIED') {
            error.value = errorDetail.message
            showResendVerification.value = true
            unverifiedEmail.value = errorDetail.email
          } else {
            error.value = errorDetail.message || 'Email ou senha inválidos'
          }
        } else {
          error.value = err.response.data.detail || 'Email ou senha inválidos'
        }
      } else if (err.request) {
        // The request was made but no response was received
        error.value = 'Não foi possível conectar ao servidor. Tente novamente mais tarde.'
      } else {
        // Something happened in setting up the request that triggered an Error
        error.value = err.message || 'Ocorreu um erro durante o login'
      }
    } finally {
      loading.value = false
    }
  }

  const handleResendVerification = async () => {
    try {
      resendLoading.value = true
      await authStore.resendVerification(unverifiedEmail.value)
      message.success('Email de verificação reenviado com sucesso!')
      showResendVerification.value = false
    } catch (err) {
      console.error('Resend verification error:', err)
      if (err.response) {
        error.value = err.response.data.detail || 'Erro ao reenviar email de verificação'
      } else {
        error.value = 'Erro ao reenviar email de verificação. Tente novamente mais tarde.'
      }
    } finally {
      resendLoading.value = false
    }
  }

  const handleGoogleLogin = async () => {
    try {
      googleLoading.value = true
      error.value = ''

      // Determine the API URL based on the current environment
      let apiBaseUrl

      if (window.location.hostname === 'localhost') {
        apiBaseUrl = 'http://localhost:8000'
      } else {
        // For production, use the API subdomain with the same protocol
        const protocol = window.location.protocol
        const domain = window.location.hostname.replace('www.', '')
        apiBaseUrl = `${protocol}//api.${domain}`
      }

      console.log('Using API base URL:', apiBaseUrl)

      // Make the request to the Google login endpoint
      const response = await fetch(`${apiBaseUrl}/api/auth/google/login`)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()

      if (data.auth_url) {
        console.log('Redirecting to Google OAuth:', data.auth_url)
        // Redirect to Google OAuth
        window.location.href = data.auth_url
      } else {
        error.value = data.detail || 'Erro ao iniciar login com Google'
      }
    } catch (err) {
      console.error('Google login error:', err)
      error.value = 'Erro ao conectar com Google. Tente novamente mais tarde.'
    } finally {
      googleLoading.value = false
    }
  }
</script>
