<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />

    <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Definir Nova Senha
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Digite sua nova senha abaixo.
          </p>
        </div>
        <form
          class="mt-8 space-y-6"
          @submit.prevent="handleSubmit"
        >
          <div class="rounded-md shadow-sm space-y-4">
            <div>
              <label
                for="password"
                class="sr-only"
              >New Password</label>
              <input
                id="password"
                v-model="formData.password"
                name="password"
                type="password"
                required
                class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Nova Senha"
                :class="{ 'border-red-500': errors.password }"
              >
              <p
                v-if="errors.password"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.password }}
              </p>
            </div>
            <div>
              <label
                for="confirmPassword"
                class="sr-only"
              >Confirm Password</label>
              <input
                id="confirmPassword"
                v-model="formData.confirmPassword"
                name="confirmPassword"
                type="password"
                required
                class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Confirmar Senha"
                :class="{ 'border-red-500': errors.confirmPassword }"
              >
              <p
                v-if="errors.confirmPassword"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.confirmPassword }}
              </p>
            </div>
          </div>

          <!-- Password Requirements -->
          <div class="bg-gray-50 p-4 rounded-md">
            <h3 class="text-sm font-medium text-gray-900 mb-2">
              Requisitos da Senha:
            </h3>
            <ul class="text-sm text-gray-600 space-y-1">
              <li :class="{ 'text-green-600': passwordLength }">
                • Pelo menos 6 caracteres
              </li>
            </ul>
          </div>

          <div>
            <button
              type="submit"
              :disabled="loading || !passwordLength"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading">Redefinindo...</span>
              <span v-else>Redefinir Senha</span>
            </button>
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
  import { ref, reactive, computed, onMounted } from 'vue'
  import { useRouter, useRoute } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { useMessage } from 'naive-ui'
  import NavBar from '@/components/NavBar.vue'

  const router = useRouter()
  const route = useRoute()
  const authStore = useAuthStore()
  const message = useMessage()

  const formData = reactive({
    password: '',
    confirmPassword: '',
  })

  const errors = reactive({
    password: '',
    confirmPassword: '',
  })

  const loading = ref(false)
  const error = ref('')
  const success = ref('')

  // Password validation - matching registration requirements
  const passwordLength = computed(() => formData.password.length >= 6)

  // const isPasswordValid = computed(() => {
  //   return passwordLength.value
  // })

  const validateForm = () => {
    let isValid = true
    errors.password = ''
    errors.confirmPassword = ''

    if (!formData.password) {
      errors.password = 'Senha é obrigatória'
      isValid = false
    } else if (formData.password.length < 6) {
      errors.password = 'A senha deve ter pelo menos 6 caracteres'
      isValid = false
    }

    if (!formData.confirmPassword) {
      errors.confirmPassword = 'Confirme sua senha'
      isValid = false
    } else if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'As senhas não coincidem'
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
      const token = route.params.token
      const result = await authStore.resetPassword(token, formData.password)
      success.value = result.message
      message.success('Senha redefinida com sucesso!')

      // Redirect to login after 2 seconds
      setTimeout(() => {
        router.push('/auth/login')
      }, 2000)
    } catch (err) {
      console.error('Password reset failed:', err)
      error.value = err.message || 'Falha ao redefinir senha. Tente novamente.'
      message.error('Falha ao redefinir senha')
    } finally {
      loading.value = false
    }
  }

  onMounted(async () => {
    try {
      const token = route.params.token
      const isValid = await authStore.validateResetToken(token)
      if (!isValid) {
        error.value = 'Token inválido ou expirado'
        message.error('Token inválido')
      }
    } catch (err) {
      console.error('Token validation failed:', err)
      error.value = 'Token inválido ou expirado'
      message.error('Token inválido')
    }
  })
</script>
