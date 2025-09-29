<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />

    <!-- Hero Section -->
    <div class="relative bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="text-center">
          <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
            <span class="block">Entre em</span>
            <span class="block text-blue-600">Contato</span>
          </h1>
          <p
            class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl"
          >
            Tem alguma dúvida, sugestão ou precisa de ajuda? Estamos aqui para você.
          </p>
        </div>
      </div>
    </div>

    <!-- Contact Form Section -->
    <div class="py-16 bg-gray-50">
      <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-lg shadow-lg p-8">
          <div class="text-center mb-8">
            <h2 class="text-2xl font-bold text-gray-900">
              Envie sua mensagem
            </h2>
            <p class="mt-2 text-gray-600">
              Preencha o formulário abaixo e entraremos em contato em até 24 horas.
            </p>
          </div>

          <!-- Success Message -->
          <div
            v-if="showSuccess"
            class="mb-6 bg-green-50 border border-green-200 rounded-md p-4"
          >
            <div class="flex">
              <div class="flex-shrink-0">
                <svg
                  class="h-5 w-5 text-green-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
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
                  Mensagem enviada com sucesso!
                </p>
                <p class="mt-1 text-sm text-green-700">
                  Obrigado pelo contato. Retornaremos em breve.
                </p>
              </div>
            </div>
          </div>

          <!-- Error Message -->
          <div
            v-if="showError"
            class="mb-6 bg-red-50 border border-red-200 rounded-md p-4"
          >
            <div class="flex">
              <div class="flex-shrink-0">
                <svg
                  class="h-5 w-5 text-red-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
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
                  Erro ao enviar mensagem
                </p>
                <p class="mt-1 text-sm text-red-700">
                  {{ errorMessage }}
                </p>
              </div>
            </div>
          </div>

          <form
            class="space-y-6"
            @submit.prevent="submitForm"
          >
            <!-- Name Field -->
            <div>
              <label
                for="name"
                class="block text-sm font-medium text-gray-700"
              >
                Nome completo *
              </label>
              <input
                id="name"
                v-model="form.name"
                type="text"
                required
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-300': errors.name }"
                placeholder="Digite seu nome completo"
              >
              <p
                v-if="errors.name"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.name }}
              </p>
            </div>

            <!-- Email Field -->
            <div>
              <label
                for="email"
                class="block text-sm font-medium text-gray-700"
              > E-mail * </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-300': errors.email }"
                placeholder="seu@email.com"
              >
              <p
                v-if="errors.email"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.email }}
              </p>
            </div>

            <!-- Company Field -->
            <div>
              <label
                for="company"
                class="block text-sm font-medium text-gray-700"
              > Empresa </label>
              <input
                id="company"
                v-model="form.company"
                type="text"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                placeholder="Nome da sua empresa (opcional)"
              >
            </div>

            <!-- Subject Field -->
            <div>
              <label
                for="subject"
                class="block text-sm font-medium text-gray-700"
              >
                Assunto *
              </label>
              <select
                id="subject"
                v-model="form.subject"
                required
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-300': errors.subject }"
              >
                <option value="">
                  Selecione um assunto
                </option>
                <option value="Dúvida sobre funcionalidades">
                  Dúvida sobre funcionalidades
                </option>
                <option value="Solicitação de demonstração">
                  Solicitação de demonstração
                </option>
                <option value="Problema técnico">
                  Problema técnico
                </option>
                <option value="Sugestão de melhoria">
                  Sugestão de melhoria
                </option>
                <option value="Parceria comercial">
                  Parceria comercial
                </option>
                <option value="Outro">
                  Outro
                </option>
              </select>
              <p
                v-if="errors.subject"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.subject }}
              </p>
            </div>

            <!-- Message Field -->
            <div>
              <label
                for="message"
                class="block text-sm font-medium text-gray-700"
              >
                Mensagem *
              </label>
              <textarea
                id="message"
                v-model="form.message"
                rows="6"
                required
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                :class="{ 'border-red-300': errors.message }"
                placeholder="Descreva sua dúvida, sugestão ou solicitação..."
              />
              <p
                v-if="errors.message"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.message }}
              </p>
            </div>

            <!-- Submit Button -->
            <div class="flex justify-end">
              <button
                type="submit"
                :disabled="isSubmitting"
                class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
              >
                <svg
                  v-if="isSubmitting"
                  class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  />
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  />
                </svg>
                {{ isSubmitting ? 'Enviando...' : 'Enviar mensagem' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Contact Info Section -->
    <div class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Outras formas de contato
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            Estamos sempre disponíveis
          </p>
        </div>
        <div class="mt-10">
          <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10">
            <div class="relative">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white"
              >
                <svg
                  class="h-6 w-6"
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
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  E-mail
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  <a
                    href="mailto:hiremetrics.contato@gmail.com"
                    class="text-blue-600 hover:text-blue-500"
                  >
                    hiremetrics.contato@gmail.com
                  </a>
                </p>
                <p class="mt-1 text-sm text-gray-400">
                  Resposta em até 24 horas
                </p>
              </div>
            </div>

            <div class="relative">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white"
              >
                <svg
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Suporte
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Atendimento especializado
                </p>
                <p class="mt-1 text-sm text-gray-400">
                  Segunda a sexta, 9h às 18h
                </p>
              </div>
            </div>

            <div class="relative">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white"
              >
                <svg
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Segurança
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Dados protegidos e seguros
                </p>
                <p class="mt-1 text-sm text-gray-400">
                  Conformidade com LGPD
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script>
  import NavBar from '@/components/NavBar.vue'
  import AppFooter from '@/components/Footer.vue'
  import apiClient from '@/api/axios-config'
  import { useAuthStore } from '@/stores/auth'

  export default {
    name: 'ContatoPage',
    components: {
      NavBar,
      AppFooter,
    },
    data() {
      return {
        form: {
          name: '',
          email: '',
          company: '',
          subject: '',
          message: '',
        },
        errors: {},
        isSubmitting: false,
        showSuccess: false,
        showError: false,
        errorMessage: '',
      }
    },
    computed: {
      authStore() {
        return useAuthStore()
      },
    },
    mounted() {
      // Scroll to top when component mounts
      window.scrollTo(0, 0)

      // Pre-fill form with user data if logged in
      this.prefillFormWithUserData()
    },
    methods: {
      prefillFormWithUserData() {
        const user = this.authStore.user
        if (user) {
          // Pre-fill name (first_name + last_name)
          this.form.name = this.getUserFullName(user)

          // Pre-fill email
          if (user.email) {
            this.form.email = user.email
          }

          // Pre-fill company
          if (user.company) {
            this.form.company = user.company
          }
        }
      },

      validateForm() {
        this.errors = {}

        if (!this.form.name.trim()) {
          this.errors.name = 'Nome é obrigatório'
        }

        if (!this.form.email.trim()) {
          this.errors.email = 'E-mail é obrigatório'
        } else if (!this.isValidEmail(this.form.email)) {
          this.errors.email = 'E-mail inválido'
        }

        if (!this.form.subject) {
          this.errors.subject = 'Assunto é obrigatório'
        }

        if (!this.form.message.trim()) {
          this.errors.message = 'Mensagem é obrigatória'
        } else if (this.form.message.trim().length < 10) {
          this.errors.message = 'Mensagem deve ter pelo menos 10 caracteres'
        }

        return Object.keys(this.errors).length === 0
      },

      isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        return emailRegex.test(email)
      },

      async submitForm() {
        if (!this.validateForm()) {
          return
        }

        this.isSubmitting = true
        this.showSuccess = false
        this.showError = false

        try {
          // Send email using backend API
          const response = await apiClient.post('/api/contact', this.form)

          if (response.data.success) {
            this.showSuccess = true
            this.resetForm()

            // Hide success message after 5 seconds
            setTimeout(() => {
              this.showSuccess = false
            }, 5000)
          } else {
            throw new Error(response.data.message)
          }
        } catch (error) {
          console.error('Error sending email:', error)
          this.showError = true
          this.errorMessage =
            error.response?.data?.message ||
            'Erro ao enviar mensagem. Tente novamente ou entre em contato diretamente por e-mail.'
        } finally {
          this.isSubmitting = false
        }
      },

      resetForm() {
        // Reset form but preserve user data
        const user = this.authStore.user
        this.form = {
          name: user ? this.getUserFullName(user) : '',
          email: user?.email || '',
          company: user?.company || '',
          subject: '',
          message: '',
        }
        this.errors = {}
      },

      getUserFullName(user) {
        const nameParts = []
        if (user.first_name) {
          nameParts.push(user.first_name)
        }
        if (user.last_name) {
          nameParts.push(user.last_name)
        }
        return nameParts.join(' ')
      },
    },
  }
</script>
