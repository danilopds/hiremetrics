<template>
  <div class="min-h-screen bg-black">
    <NavBar />

    <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <!-- Background Grid Pattern -->
      <div class="absolute inset-0 bg-[linear-gradient(to_right,#1f2937_1px,transparent_1px),linear-gradient(to_bottom,#1f2937_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,#000_70%,transparent_110%)]" />
      
      <div class="relative max-w-md w-full space-y-8">
        <!-- Header -->
        <div class="text-center">
          <h2 class="mt-6 text-3xl font-extrabold text-white font-mono">
            <span class="text-cyan-400">$</span> Login
          </h2>
          <p class="mt-2 text-sm text-gray-400 font-mono">
            Acesse sua dashboard de desenvolvedor
          </p>
        </div>

        <!-- Card Container -->
        <div class="bg-gradient-to-br from-gray-900 to-gray-800 border border-gray-700 rounded-lg shadow-2xl p-8">
          <!-- Google OAuth Button -->
          <div>
            <button
              type="button"
              :disabled="googleLoading"
              class="group relative w-full flex items-center justify-center py-3 px-4 border border-gray-600 text-sm font-medium rounded-md text-gray-200 bg-gray-800 hover:bg-gray-700 hover:border-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 focus:ring-offset-gray-900 shadow-md transition-all duration-200 font-mono"
              @click="handleGoogleLogin"
            >
              <svg
                v-if="!googleLoading"
                class="w-5 h-5 mr-2"
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
              <span v-if="googleLoading">Entrando com Google...</span>
              <span v-else>Continuar com Google</span>
            </button>
          </div>

          <!-- Divider -->
          <div class="relative my-6">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-700" />
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-gray-800 text-gray-400 font-mono">
                <span class="text-cyan-500">//</span> ou use email
              </span>
            </div>
          </div>

          <!-- Login Form -->
          <form
            class="space-y-5"
            @submit.prevent="handleSubmit"
          >
            <div class="space-y-4">
              <div>
                <label
                  for="email"
                  class="block text-sm font-medium text-gray-300 mb-2 font-mono"
                >
                  <span class="text-cyan-400">&gt;</span> Email
                </label>
                <input
                  id="email"
                  v-model="formData.email"
                  name="email"
                  type="email"
                  required
                  class="appearance-none block w-full px-4 py-3 border border-gray-600 bg-gray-800 text-gray-200 placeholder-gray-500 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-colors font-mono"
                  placeholder="seu@email.com"
                >
              </div>
              <div>
                <label
                  for="password"
                  class="block text-sm font-medium text-gray-300 mb-2 font-mono"
                >
                  <span class="text-cyan-400">&gt;</span> Senha
                </label>
                <input
                  id="password"
                  v-model="formData.password"
                  name="password"
                  type="password"
                  required
                  class="appearance-none block w-full px-4 py-3 border border-gray-600 bg-gray-800 text-gray-200 placeholder-gray-500 rounded-md focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 transition-colors font-mono"
                  placeholder="••••••••"
                >
              </div>
            </div>

            <div class="flex items-center justify-end">
              <div class="text-sm">
                <router-link
                  to="/auth/forgot-password"
                  class="font-medium text-cyan-400 hover:text-cyan-300 transition-colors font-mono"
                >
                  Esqueceu sua senha?
                </router-link>
              </div>
            </div>

            <div>
              <button
                type="submit"
                :disabled="loading"
                class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 focus:ring-offset-gray-900 shadow-lg shadow-cyan-500/50 transition-all duration-200 font-mono disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="loading">Entrando...</span>
                <span v-else>Entrar →</span>
              </button>
            </div>

            <div class="text-center">
              <p class="text-sm text-gray-400 font-mono">
                Não tem uma conta?
                <router-link
                  to="/auth/register"
                  class="font-medium text-cyan-400 hover:text-cyan-300 transition-colors ml-1"
                >
                  Cadastre-se
                </router-link>
              </p>
            </div>

            <!-- Error Messages -->
            <div
              v-if="error"
              class="rounded-md bg-red-900/50 border border-red-700 p-4"
            >
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg
                    class="h-5 w-5 text-red-400"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                </div>
                <div class="ml-3">
                  <p class="text-sm text-red-300 font-mono">{{ error }}</p>
                  <div
                    v-if="showResendVerification"
                    class="mt-3"
                  >
                    <p class="text-gray-400 text-xs mb-2 font-mono">
                      Não recebeu o email de verificação?
                    </p>
                    <button
                      type="button"
                      :disabled="resendLoading"
                      class="text-cyan-400 hover:text-cyan-300 text-sm font-medium font-mono transition-colors"
                      @click="handleResendVerification"
                    >
                      <span v-if="resendLoading">Enviando...</span>
                      <span v-else>Reenviar email de verificação →</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </form>
        </div>
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
