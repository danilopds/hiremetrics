<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />

    <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Recuperar Senha
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Digite seu email e enviaremos instruções para redefinir sua senha.
          </p>
        </div>
        <form
          class="mt-8 space-y-6"
          @submit.prevent="handleSubmit"
        >
          <div class="rounded-md shadow-sm -space-y-px">
            <div>
              <label
                for="email"
                class="sr-only"
              >Email address</label>
              <input
                id="email"
                v-model="formData.email"
                name="email"
                type="email"
                required
                class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="seu@email.com"
                :class="{ 'border-red-500': errors.email }"
              >
              <p
                v-if="errors.email"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.email }}
              </p>
            </div>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading">Enviando...</span>
              <span v-else>Enviar Instruções</span>
            </button>
          </div>

          <div class="text-sm text-center">
            <router-link
              to="/auth/login"
              class="font-medium text-blue-600 hover:text-blue-500"
            >
              Voltar ao login
            </router-link>
          </div>

          <!-- Success Message -->
          <div
            v-if="success"
            class="rounded-md bg-green-50 p-4"
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
                <p class="text-sm font-medium text-green-800">
                  {{ success }}
                </p>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div
            v-if="error"
            class="rounded-md bg-red-50 p-4"
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
                <p class="text-sm font-medium text-red-800">
                  {{ error }}
                </p>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, reactive } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useMessage } from 'naive-ui'
  import NavBar from '@/components/NavBar.vue'

  const authStore = useAuthStore()
  const message = useMessage()

  const formData = reactive({
    email: '',
  })

  const errors = reactive({
    email: '',
  })

  const loading = ref(false)
  const error = ref('')
  const success = ref('')

  const validateForm = () => {
    let isValid = true
    errors.email = ''

    if (!formData.email) {
      errors.email = 'Email é obrigatório'
      isValid = false
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      errors.email = 'Digite um email válido'
      isValid = false
    }

    return isValid
  }

  const handleSubmit = async () => {
    if (!validateForm()) {
      return
    }

    loading.value = true
    error.value = ''
    success.value = ''

    try {
      const result = await authStore.requestPasswordReset(formData.email)
      success.value = result.message
      message.success('Instruções de redefinição enviadas!')
    } catch (err) {
      console.error('Password reset request failed:', err)
      error.value = err.message || 'Falha ao enviar instruções. Tente novamente.'
      message.error('Falha ao enviar instruções')
    } finally {
      loading.value = false
    }
  }
</script>
