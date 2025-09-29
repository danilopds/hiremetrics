<template>
  <BasePageLayout
    title="Meu Perfil"
    subtitle="Gerencie suas informações pessoais e configurações de conta"
    icon="👤"
    page-id="profile"
    :loading="false"
    :error="null"
    :show-period-filter="false"
    :show-alert-banner="false"
  >
    <div class="max-w-4xl mx-auto">
      <div class="bg-white shadow rounded-lg">
        <!-- Tabs -->
        <div class="border-b border-gray-200">
          <nav class="-mb-px flex space-x-8 px-6">
            <button
              class="py-4 px-1 border-b-2 font-medium text-sm"
              :class="
                activeTab === 'account'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              "
              @click="activeTab = 'account'"
            >
              Informações da Conta
            </button>
            <button
              class="py-4 px-1 border-b-2 font-medium text-sm"
              :class="
                activeTab === 'password'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              "
              @click="activeTab = 'password'"
            >
              Alterar Senha
            </button>
            <button
              class="py-4 px-1 border-b-2 font-medium text-sm"
              :class="
                activeTab === 'preferences'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              "
              @click="activeTab = 'preferences'"
            >
              Preferências
            </button>
          </nav>
        </div>

        <div class="p-6">
          <!-- Account Information Tab -->
          <div v-if="activeTab === 'account'">
            <h2 class="text-lg font-medium text-gray-900 mb-4">
              Informações da Conta
            </h2>

            <!-- Personal Information -->
            <div class="mb-8">
              <h3 class="text-md font-medium text-gray-800 mb-4">
                Informações Pessoais
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Nome</label>
                  <p class="mt-1 text-sm text-gray-900">
                    {{ getUserFullName() }}
                  </p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Email</label>
                  <p class="mt-1 text-sm text-gray-900">
                    {{ user?.email }}
                  </p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Membro desde</label>
                  <p class="mt-1 text-sm text-gray-900">
                    {{ formatDate(user?.created_at) }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Professional Information -->
            <div>
              <h3 class="text-md font-medium text-gray-800 mb-4">
                Informações Profissionais
              </h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700">Empresa</label>
                  <p class="mt-1 text-sm text-gray-900">
                    {{ user?.company || 'Não informado' }}
                  </p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Cargo</label>
                  <p class="mt-1 text-sm text-gray-900">
                    {{ user?.job_title || 'Não informado' }}
                  </p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Setor</label>
                  <p class="mt-1 text-sm text-gray-900">
                    {{ user?.industry || 'Não informado' }}
                  </p>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700">Tamanho da Empresa</label>
                  <p class="mt-1 text-sm text-gray-900">
                    {{ user?.company_size || 'Não informado' }}
                  </p>
                </div>
                <div class="md:col-span-2">
                  <label class="block text-sm font-medium text-gray-700">Seu Papel/Interesse</label>
                  <p class="mt-1 text-sm text-gray-900">
                    {{ user?.role_in_company || 'Não informado' }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Change Password Tab -->
          <div v-if="activeTab === 'password'">
            <h2 class="text-lg font-medium text-gray-900 mb-4">
              Alterar Senha
            </h2>

            <!-- Success Message -->
            <div
              v-if="successMessage"
              class="mb-4 bg-green-50 border border-green-200 rounded-md p-4"
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

            <!-- Error Message -->
            <div
              v-if="errorMessage"
              class="mb-4 bg-red-50 border border-red-200 rounded-md p-4"
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
                    {{ errorMessage }}
                  </p>
                </div>
              </div>
            </div>

            <form
              class="space-y-4 max-w-md"
              @submit.prevent="changePassword"
            >
              <div>
                <label
                  for="currentPassword"
                  class="block text-sm font-medium text-gray-700"
                >Senha Atual</label>
                <input
                  id="currentPassword"
                  v-model="passwordForm.currentPassword"
                  type="password"
                  required
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  :class="{ 'border-red-500': errors.currentPassword }"
                >
                <p
                  v-if="errors.currentPassword"
                  class="mt-1 text-sm text-red-600"
                >
                  {{ errors.currentPassword }}
                </p>
              </div>
              <div>
                <label
                  for="newPassword"
                  class="block text-sm font-medium text-gray-700"
                >Nova Senha</label>
                <input
                  id="newPassword"
                  v-model="passwordForm.newPassword"
                  type="password"
                  required
                  class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  :class="{ 'border-red-500': errors.newPassword }"
                >
                <p
                  v-if="errors.newPassword"
                  class="mt-1 text-sm text-red-600"
                >
                  {{ errors.newPassword }}
                </p>
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
                  :disabled="isChangingPassword || !passwordLength"
                  class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {{ isChangingPassword ? 'Alterando...' : 'Alterar Senha' }}
                </button>
              </div>
            </form>
          </div>

          <!-- Preferences Tab -->
          <div v-if="activeTab === 'preferences'">
            <h2 class="text-lg font-medium text-gray-900 mb-4">
              Preferências
            </h2>

            <!-- Success Message -->
            <div
              v-if="preferencesSuccessMessage"
              class="mb-4 bg-green-50 border border-green-200 rounded-md p-4"
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
                    {{ preferencesSuccessMessage }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Error Message -->
            <div
              v-if="preferencesErrorMessage"
              class="mb-4 bg-red-50 border border-red-200 rounded-md p-4"
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
                    {{ preferencesErrorMessage }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Marketing Emails Preference -->
            <div class="space-y-6">
              <div class="bg-white p-6 border border-gray-200 rounded-lg">
                <h3 class="text-md font-medium text-gray-800 mb-4">
                  Preferências de Email
                </h3>

                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="text-sm font-medium text-gray-900">
                      Emails de Marketing
                    </h4>
                    <p class="text-sm text-gray-600 mt-1">
                      Receber emails sobre novidades, atualizações e ofertas especiais
                    </p>
                  </div>
                  <div class="flex items-center">
                    <button
                      :disabled="isUpdatingPreferences"
                      class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                      :class="user?.marketing_emails ? 'bg-blue-600' : 'bg-gray-200'"
                      @click="toggleMarketingEmails"
                    >
                      <span
                        class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
                        :class="user?.marketing_emails ? 'translate-x-5' : 'translate-x-0'"
                      />
                    </button>
                    <span class="ml-3 text-sm text-gray-900">
                      {{ user?.marketing_emails ? 'Ativado' : 'Desativado' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </BasePageLayout>
</template>

<script setup>
  import { ref, onMounted, computed, watch } from 'vue'
  import BasePageLayout from '@/components/common/BasePageLayout.vue'
  import { useAuthStore } from '@/stores/auth'
  import { changePassword as apiChangePassword } from '@/api/auth'
  import { updateUserPreferences } from '@/api/auth'
  import { format, parseISO } from 'date-fns'
  import { ptBR } from 'date-fns/locale'

  defineOptions({
    name: 'ProfilePage',
  })

  const authStore = useAuthStore()

  const user = ref(authStore.user)
  const activeTab = ref('account')

  // Watch for changes in the store's user and update local ref
  watch(
    () => authStore.user,
    (newUser) => {
      if (newUser) {
        user.value = newUser
      }
    },
    { immediate: true }
  )

  const isChangingPassword = ref(false)
  const successMessage = ref('')
  const errorMessage = ref('')
  const passwordForm = ref({
    currentPassword: '',
    newPassword: '',
  })

  const errors = ref({
    currentPassword: '',
    newPassword: '',
  })

  // Preferences variables
  const isUpdatingPreferences = ref(false)
  const preferencesSuccessMessage = ref('')
  const preferencesErrorMessage = ref('')

  // Password validation - matching registration requirements
  const passwordLength = computed(() => passwordForm.value.newPassword.length >= 6)

  const getUserFullName = () => {
    if (!user.value) {
      return 'Não informado'
    }

    const parts = []
    if (user.value.first_name) {
      parts.push(user.value.first_name)
    }
    if (user.value.last_name) {
      parts.push(user.value.last_name)
    }

    return parts.length > 0 ? parts.join(' ') : 'Não informado'
  }

  const formatDate = (dateString) => {
    if (!dateString) {
      return 'Não informado'
    }
    try {
      return format(parseISO(dateString), "d 'de' MMMM 'de' yyyy", { locale: ptBR })
    } catch {
      return 'Não informado'
    }
  }

  const validatePasswordForm = () => {
    let isValid = true
    errors.value.currentPassword = ''
    errors.value.newPassword = ''

    if (!passwordForm.value.currentPassword) {
      errors.value.currentPassword = 'Senha atual é obrigatória'
      isValid = false
    }

    if (!passwordForm.value.newPassword) {
      errors.value.newPassword = 'Nova senha é obrigatória'
      isValid = false
    } else if (passwordForm.value.newPassword.length < 6) {
      errors.value.newPassword = 'A senha deve ter pelo menos 6 caracteres'
      isValid = false
    }

    return isValid
  }

  const changePassword = async () => {
    if (!validatePasswordForm()) {
      return
    }

    isChangingPassword.value = true
    successMessage.value = ''
    errorMessage.value = ''

    try {
      await apiChangePassword({
        current_password: passwordForm.value.currentPassword,
        new_password: passwordForm.value.newPassword,
      })

      successMessage.value = 'Senha alterada com sucesso!'
      passwordForm.value.currentPassword = ''
      passwordForm.value.newPassword = ''
      // Clear errors
      errors.value.currentPassword = ''
      errors.value.newPassword = ''
    } catch (error) {
      console.error('Error changing password:', error)
      if (error.response?.data?.detail) {
        errorMessage.value = error.response.data.detail
      } else {
        errorMessage.value = 'Erro ao alterar senha. Tente novamente.'
      }
    } finally {
      isChangingPassword.value = false
    }
  }

  const toggleMarketingEmails = async () => {
    if (!user.value) {
      return
    }

    isUpdatingPreferences.value = true
    preferencesSuccessMessage.value = ''
    preferencesErrorMessage.value = ''

    try {
      await updateUserPreferences({
        marketing_emails: !user.value.marketing_emails,
      })

      // Update user preferences in the store
      const updatedUser = await authStore.updateUserPreferences()

      // Update the local user ref to reflect the changes immediately
      if (updatedUser) {
        user.value = updatedUser
      }

      preferencesSuccessMessage.value = 'Preferências de email atualizadas com sucesso!'
    } catch (error) {
      console.error('Error updating marketing emails preference:', error)
      if (error.response?.data?.detail) {
        preferencesErrorMessage.value = error.response.data.detail
      } else {
        preferencesErrorMessage.value = 'Erro ao atualizar preferências de email. Tente novamente.'
      }
    } finally {
      isUpdatingPreferences.value = false
    }
  }

  onMounted(() => {
    // Load any necessary data
  })
</script>
