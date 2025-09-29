<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />

    <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div class="text-center">
          <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100">
            <svg
              class="h-6 w-6 text-blue-600"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
          </div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Verificação de Email
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Verificando seu email...
          </p>
        </div>

        <!-- Loading State -->
        <div
          v-if="loading"
          class="text-center"
        >
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto" />
          <p class="mt-4 text-sm text-gray-600">
            Verificando seu email...
          </p>
        </div>

        <!-- Success State -->
        <div
          v-if="success"
          class="bg-green-50 border border-green-200 rounded-md p-6"
        >
          <div class="flex">
            <div class="flex-shrink-0">
              <svg
                class="h-5 w-5 text-green-400"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-green-800">
                Email verificado com sucesso!
              </h3>
              <div class="mt-2 text-sm text-green-700">
                <p>{{ successMessage }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Error State -->
        <div
          v-if="error"
          class="bg-red-50 border border-red-200 rounded-md p-6"
        >
          <div class="flex">
            <div class="flex-shrink-0">
              <svg
                class="h-5 w-5 text-red-400"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd"
                />
              </svg>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">
                Erro na verificação
              </h3>
              <div class="mt-2 text-sm text-red-700">
                <p>{{ errorMessage }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Actions -->
        <div
          v-if="error || success"
          class="space-y-4"
        >
          <NButton
            v-if="error"
            type="primary"
            class="w-full"
            :loading="resendLoading"
            @click="resendVerification"
          >
            Reenviar Email de Verificação
          </NButton>

          <NButton
            type="primary"
            class="w-full"
            @click="goToLogin"
          >
            Fazer Login
          </NButton>
        </div>

        <!-- Help Text -->
        <div
          v-if="error"
          class="text-center"
        >
          <p class="text-sm text-gray-600">
            Não recebeu o email? Verifique sua caixa de spam ou
            <button
              class="text-indigo-600 hover:text-indigo-500 font-medium"
              :disabled="resendLoading"
              @click="resendVerification"
            >
              solicite um novo email de verificação
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import NavBar from '@/components/NavBar.vue'
  import { NButton } from 'naive-ui'
  import apiClient from '@/api/axios-config'

  const route = useRoute()
  const router = useRouter()

  const loading = ref(true)
  const success = ref(false)
  const error = ref(false)
  const successMessage = ref('')
  const errorMessage = ref('')
  const resendLoading = ref(false)

  const verifyEmail = async (token) => {
    try {
      const response = await apiClient.post('/api/auth/verify-email', { token })

      if (response.data.success) {
        success.value = true
        successMessage.value = response.data.message
      } else {
        throw new Error(response.data.message)
      }
    } catch (err) {
      error.value = true
      if (err.response?.data?.detail) {
        errorMessage.value = err.response.data.detail
      } else {
        errorMessage.value = 'Erro ao verificar email. Tente novamente.'
      }
    } finally {
      loading.value = false
    }
  }

  const resendVerification = async () => {
    resendLoading.value = true
    try {
      // Get email from route query or prompt user
      const email = route.query.email || prompt('Digite seu email:')

      if (!email) {
        errorMessage.value = 'Email é obrigatório'
        return
      }

      const response = await apiClient.post('/api/auth/resend-verification', { email })

      if (response.data.success) {
        successMessage.value = 'Novo email de verificação enviado!'
        error.value = false
        success.value = true
      } else {
        throw new Error(response.data.message)
      }
    } catch (err) {
      if (err.response?.data?.detail) {
        errorMessage.value = err.response.data.detail
      } else {
        errorMessage.value = 'Erro ao reenviar email. Tente novamente.'
      }
    } finally {
      resendLoading.value = false
    }
  }

  const goToLogin = () => {
    router.push('/auth/login')
  }

  onMounted(() => {
    const token = route.query.token

    if (!token) {
      error.value = true
      errorMessage.value = 'Token de verificação não encontrado.'
      loading.value = false
      return
    }

    verifyEmail(token)
  })
</script>
