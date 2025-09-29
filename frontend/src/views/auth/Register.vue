<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />

    <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Crie sua conta
          </h2>
          <p class="mt-2 text-center text-sm text-gray-600">
            Ou
            <router-link
              to="/auth/login"
              class="font-medium text-indigo-600 hover:text-indigo-500"
            >
              entre na sua conta
            </router-link>
          </p>
        </div>

        <!-- Registration Success State -->
        <div
          v-if="registrationCompleted"
          class="text-center space-y-6"
        >
          <div class="bg-green-50 border border-green-200 rounded-md p-6">
            <div class="flex justify-center mb-4">
              <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
                <svg
                  class="w-8 h-8 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
              </div>
            </div>
            <h3 class="text-lg font-medium text-green-900 mb-2">
              Conta criada com sucesso!
            </h3>
            <p class="text-sm text-green-700 mb-4">
              Enviamos um email de verificação para <strong>{{ registeredEmail }}</strong>
            </p>
            <p class="text-sm text-green-600">
              Clique no link no email para ativar sua conta e começar a usar o HireMetrics.
            </p>
          </div>

          <!-- Action Buttons -->
          <div class="space-y-3">
            <NButton
              type="primary"
              :loading="resendLoading"
              class="w-full"
              @click="resendVerificationEmail"
            >
              Reenviar Email de Verificação
            </NButton>

            <div class="text-sm text-gray-600">
              Não recebeu o email? Verifique sua caixa de spam.
            </div>

            <div class="pt-4 border-t border-gray-200">
              <p class="text-sm text-gray-600 mb-3">
                Já verificou seu email?
              </p>
              <NButton
                type="default"
                class="w-full"
                @click="goToLogin"
              >
                Fazer Login
              </NButton>
            </div>
          </div>
        </div>

        <!-- Success Message (for resend) -->
        <div
          v-if="successMessage"
          class="bg-green-50 border border-green-200 rounded-md p-4"
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
                {{ successMessage }}
              </p>
            </div>
          </div>
        </div>

        <!-- General Error Message -->
        <div
          v-if="generalError"
          class="bg-red-50 border border-red-200 rounded-md p-4"
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
                {{ generalError }}
              </p>
              <div
                v-if="generalError.includes('já está registrado')"
                class="mt-2"
              >
                <router-link
                  to="/auth/login"
                  class="text-sm text-indigo-600 hover:text-indigo-500 font-medium"
                >
                  → Fazer login com este email
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <form
          v-if="!registrationCompleted"
          class="mt-8 space-y-6"
          @submit.prevent="handleSubmit"
        >
          <!-- Step 1: Basic Information -->
          <div
            v-if="currentStep === 1"
            class="space-y-4"
          >
            <h3 class="text-lg font-medium text-gray-900">
              Informações Básicas
            </h3>

            <div>
              <label
                for="name"
                class="block text-sm font-medium text-gray-700"
              >Nome Completo *</label>
              <NInput
                id="name"
                v-model:value="form.name"
                type="text"
                placeholder="Digite seu nome completo"
                :status="errors.name ? 'error' : undefined"
              />
              <p
                v-if="errors.name"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.name }}
              </p>
            </div>

            <div>
              <label
                for="email"
                class="block text-sm font-medium text-gray-700"
              >E-mail *</label>
              <NInput
                id="email"
                v-model:value="form.email"
                type="email"
                placeholder="seu@email.com"
                :status="errors.email ? 'error' : undefined"
              />
              <p
                v-if="errors.email"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.email }}
              </p>
            </div>

            <div>
              <label
                for="password"
                class="block text-sm font-medium text-gray-700"
              >Senha *</label>
              <NInput
                id="password"
                v-model:value="form.password"
                type="password"
                placeholder="Mínimo 6 caracteres"
                :status="errors.password ? 'error' : undefined"
              />
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
                class="block text-sm font-medium text-gray-700"
              >Confirmar Senha *</label>
              <NInput
                id="confirmPassword"
                v-model:value="form.confirmPassword"
                type="password"
                placeholder="Confirme sua senha"
                :status="errors.confirmPassword ? 'error' : undefined"
              />
              <p
                v-if="errors.confirmPassword"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.confirmPassword }}
              </p>
            </div>
          </div>

          <!-- Step 2: Profile Information -->
          <div
            v-if="currentStep === 2"
            class="space-y-4"
          >
            <h3 class="text-lg font-medium text-gray-900">
              Perfil Profissional
            </h3>
            <p class="text-sm text-gray-600">
              Essas informações nos ajudam a personalizar sua experiência.
            </p>

            <div>
              <label
                for="company"
                class="block text-sm font-medium text-gray-700"
              >Empresa *</label>
              <NInput
                id="company"
                v-model:value="form.company"
                type="text"
                placeholder="Nome da sua empresa"
                :status="errors.company ? 'error' : undefined"
              />
              <p
                v-if="errors.company"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.company }}
              </p>
            </div>

            <div>
              <label
                for="jobTitle"
                class="block text-sm font-medium text-gray-700"
              >Cargo *</label>
              <NInput
                id="jobTitle"
                v-model:value="form.jobTitle"
                type="text"
                placeholder="Seu cargo atual"
                :status="errors.jobTitle ? 'error' : undefined"
              />
              <p
                v-if="errors.jobTitle"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.jobTitle }}
              </p>
            </div>

            <div>
              <label
                for="industry"
                class="block text-sm font-medium text-gray-700"
              >Setor *</label>
              <NSelect
                v-model:value="form.industry"
                :options="industryOptions"
                placeholder="Selecione o setor"
                :status="errors.industry ? 'error' : undefined"
              />
              <p
                v-if="errors.industry"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.industry }}
              </p>
            </div>

            <div>
              <label
                for="companySize"
                class="block text-sm font-medium text-gray-700"
              >Tamanho da Empresa *</label>
              <NSelect
                v-model:value="form.companySize"
                :options="companySizeOptions"
                placeholder="Selecione o tamanho"
                :status="errors.companySize ? 'error' : undefined"
              />
              <p
                v-if="errors.companySize"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.companySize }}
              </p>
            </div>

            <div>
              <label
                for="roleInCompany"
                class="block text-sm font-medium text-gray-700"
              >Seu Papel/Interesse *</label>
              <NSelect
                v-model:value="form.roleInCompany"
                :options="roleOptions"
                placeholder="Selecione seu papel ou interesse"
                :status="errors.roleInCompany ? 'error' : undefined"
              />
              <p
                v-if="errors.roleInCompany"
                class="mt-1 text-sm text-red-600"
              >
                {{ errors.roleInCompany }}
              </p>
            </div>
          </div>

          <!-- Step 3: Terms and Conditions -->
          <div
            v-if="currentStep === 3"
            class="space-y-4"
          >
            <h3 class="text-lg font-medium text-gray-900">
              Termos e Condições
            </h3>

            <div class="bg-gray-50 p-4 rounded-md">
              <p class="text-sm text-gray-700 mb-4">
                Ao criar uma conta, você concorda com nossos Termos de Uso e Política de
                Privacidade. As preferências de emails podem ser alteradas em seu perfil.
              </p>
              <div class="space-y-2">
                <div class="flex items-start">
                  <NCheckbox
                    v-model:checked="form.terms"
                    class="mt-1"
                  />
                  <label class="ml-2 text-sm text-gray-700">
                    Concordo com os
                    <router-link
                      to="/termos-de-uso"
                      class="text-indigo-600 hover:text-indigo-500"
                    >Termos de Uso</router-link>
                    e
                    <router-link
                      to="/politica-privacidade"
                      class="text-indigo-600 hover:text-indigo-500"
                    >Política de Privacidade</router-link>
                  </label>
                </div>
                <div class="flex items-start">
                  <NCheckbox
                    v-model:checked="form.marketing"
                    class="mt-1"
                  />
                  <label class="ml-2 text-sm text-gray-700">
                    Aceito receber emails sobre novidades
                  </label>
                </div>
              </div>
            </div>

            <p
              v-if="errors.terms"
              class="text-sm text-red-600"
            >
              {{ errors.terms }}
            </p>
          </div>

          <!-- Navigation Buttons -->
          <div class="flex justify-between">
            <NButton
              v-if="currentStep > 1"
              type="default"
              :disabled="loading"
              @click="previousStep"
            >
              Voltar
            </NButton>
            <div v-else />

            <NButton
              v-if="currentStep < 3"
              type="primary"
              :disabled="loading || !canProceedToNextStep"
              @click="nextStep"
            >
              Próximo
            </NButton>
            <NButton
              v-else
              type="primary"
              attr-type="submit"
              :loading="loading"
            >
              Criar Conta
            </NButton>
          </div>

          <!-- Progress Indicator -->
          <div class="flex justify-center space-x-2">
            <div
              v-for="step in 3"
              :key="step"
              class="w-3 h-3 rounded-full"
              :class="step <= currentStep ? 'bg-indigo-600' : 'bg-gray-300'"
            />
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, reactive, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import NavBar from '@/components/NavBar.vue'
  import { NInput, NButton, NCheckbox, NSelect } from 'naive-ui'
  import apiClient from '@/api/axios-config'

  defineOptions({
    name: 'RegisterPage',
  })

  const router = useRouter()
  const loading = ref(false)
  const currentStep = ref(1)
  const successMessage = ref('')
  const generalError = ref('')
  const registrationCompleted = ref(false)
  const registeredEmail = ref('')
  const resendLoading = ref(false)

  const form = reactive({
    // Step 1
    name: '',
    email: '',
    password: '',
    confirmPassword: '',

    // Step 2
    company: '',
    jobTitle: '',
    industry: '',
    companySize: '',
    roleInCompany: '',

    // Step 3
    terms: true,
    marketing: true,
  })

  const errors = reactive({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    company: '',
    jobTitle: '',
    industry: '',
    companySize: '',
    roleInCompany: '',
    terms: '',
  })

  // Options for select fields
  const industryOptions = [
    { label: 'Tecnologia', value: 'tecnologia' },
    { label: 'Saúde', value: 'saude' },
    { label: 'Educação', value: 'educacao' },
    { label: 'Financeiro', value: 'financeiro' },
    { label: 'Varejo', value: 'varejo' },
    { label: 'Manufatura', value: 'manufatura' },
    { label: 'Consultoria', value: 'consultoria' },
    { label: 'Outro', value: 'outro' },
  ]

  const companySizeOptions = [
    { label: '1-10 funcionários', value: '1-10' },
    { label: '11-50 funcionários', value: '11-50' },
    { label: '51-200 funcionários', value: '51-200' },
    { label: '201-1000 funcionários', value: '201-1000' },
    { label: '1000+ funcionários', value: '1000+' },
  ]

  const roleOptions = [
    { label: 'Desenvolvedor/Programador', value: 'desenvolvedor' },
    { label: 'Recursos Humanos', value: 'rh' },
    { label: 'Recrutamento', value: 'recrutamento' },
    { label: 'Gestor/Diretor', value: 'gestor' },
    { label: 'CEO/Founder', value: 'ceo' },
    { label: 'Consultor', value: 'consultor' },
    { label: 'Pesquisador/Analista', value: 'pesquisador' },
    { label: 'Estudante', value: 'estudante' },
    { label: 'Candidato/Job Seeker', value: 'candidato' },
    { label: 'Outro', value: 'outro' },
  ]

  const clearMessages = () => {
    successMessage.value = ''
    generalError.value = ''
    Object.keys(errors).forEach((key) => {
      errors[key] = ''
    })
  }

  const resendVerificationEmail = async () => {
    resendLoading.value = true
    try {
      const response = await apiClient.post('/api/auth/resend-verification', {
        email: registeredEmail.value,
      })

      if (response.data.success) {
        successMessage.value = 'Email de verificação reenviado com sucesso!'
        setTimeout(() => {
          successMessage.value = ''
        }, 5000)
      } else {
        throw new Error(response.data.message)
      }
    } catch (error) {
      console.error('Error resending verification email:', error)
      if (error.response) {
        generalError.value = error.response.data.detail || 'Erro ao reenviar email de verificação.'
      } else {
        generalError.value = 'Erro ao reenviar email de verificação. Tente novamente.'
      }
    } finally {
      resendLoading.value = false
    }
  }

  const goToLogin = () => {
    router.push('/auth/login')
  }

  const validateStep1 = () => {
    clearMessages()
    let isValid = true

    if (!form.name.trim()) {
      errors.name = 'Nome é obrigatório'
      isValid = false
    }

    if (!form.email.trim()) {
      errors.email = 'Email é obrigatório'
      isValid = false
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      errors.email = 'Digite um email válido'
      isValid = false
    }

    if (!form.password) {
      errors.password = 'Senha é obrigatória'
      isValid = false
    } else if (form.password.length < 6) {
      errors.password = 'A senha deve ter pelo menos 6 caracteres'
      isValid = false
    }

    if (!form.confirmPassword) {
      errors.confirmPassword = 'Confirme sua senha'
      isValid = false
    } else if (form.password !== form.confirmPassword) {
      errors.confirmPassword = 'As senhas não coincidem'
      isValid = false
    }

    return isValid
  }

  const validateStep2 = () => {
    clearMessages()
    let isValid = true

    if (!form.company.trim()) {
      errors.company = 'Empresa é obrigatória'
      isValid = false
    }

    if (!form.jobTitle.trim()) {
      errors.jobTitle = 'Cargo é obrigatório'
      isValid = false
    }

    if (!form.industry) {
      errors.industry = 'Setor é obrigatório'
      isValid = false
    }

    if (!form.companySize) {
      errors.companySize = 'Tamanho da empresa é obrigatório'
      isValid = false
    }

    if (!form.roleInCompany) {
      errors.roleInCompany = 'Seu papel ou interesse é obrigatório'
      isValid = false
    }

    return isValid
  }

  const validateStep3 = () => {
    clearMessages()
    let isValid = true

    if (!form.terms) {
      errors.terms = 'Você deve aceitar os Termos e Condições para continuar'
      isValid = false
    }

    return isValid
  }

  const canProceedToNextStep = computed(() => {
    if (currentStep.value === 1) {
      return (
        form.name &&
        form.email &&
        form.password &&
        form.confirmPassword &&
        form.password === form.confirmPassword &&
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email) &&
        form.password.length >= 6
      )
    }
    if (currentStep.value === 2) {
      return (
        form.company && form.jobTitle && form.industry && form.companySize && form.roleInCompany
      )
    }
    return true
  })

  const nextStep = () => {
    if (currentStep.value === 1 && !validateStep1()) {
      return
    }
    if (currentStep.value === 2 && !validateStep2()) {
      return
    }
    if (currentStep.value < 3) {
      currentStep.value++
    }
  }

  const previousStep = () => {
    if (currentStep.value > 1) {
      currentStep.value--
    }
  }

  const handleSubmit = async () => {
    if (!validateStep3()) {
      return
    }

    loading.value = true
    try {
      // Split name into first and last name
      const [firstName, ...lastNameParts] = form.name.split(' ')
      const lastName = lastNameParts.join(' ')

      const response = await apiClient.post('/api/auth/register', {
        email: form.email,
        password: form.password,
        first_name: firstName,
        last_name: lastName,
        company: form.company,
        job_title: form.jobTitle,
        industry: form.industry,
        company_size: form.companySize,
        role_in_company: form.roleInCompany,
      })

      if (response.data.success) {
        // Set registration completed state
        registrationCompleted.value = true
        registeredEmail.value = form.email

        // Don't redirect automatically - let user verify email first
        // The success state will guide them to check their email
      } else {
        throw new Error(response.data.message)
      }
    } catch (error) {
      console.error('Registration failed:', error)
      if (error.response) {
        if (error.response.data.detail === 'Email already registered') {
          // Handle duplicate email error
          generalError.value =
            'Este email já está registrado. Tente usar um email diferente ou faça login se você já tem uma conta.'
          // Clear the email field and go back to step 1
          form.email = ''
          currentStep.value = 1
          // Clear other error messages
          Object.keys(errors).forEach((key) => {
            errors[key] = ''
          })
        } else {
          generalError.value = error.response.data.detail || 'Falha no registro. Tente novamente.'
        }
      } else if (error.request) {
        generalError.value = 'Não foi possível conectar ao servidor. Tente novamente mais tarde.'
      } else {
        generalError.value = error.message || 'Ocorreu um erro durante o registro'
      }
    } finally {
      loading.value = false
    }
  }
</script>
