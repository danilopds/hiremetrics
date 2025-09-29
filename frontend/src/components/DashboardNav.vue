<template>
  <nav class="bg-white shadow fixed top-0 left-0 right-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex">
          <div class="flex-shrink-0 flex items-center">
            <router-link
              to="/dashboard/vagas"
              class="flex items-center"
            >
              <img
                v-if="!onLogoError"
                :src="logoSrc"
                alt="HireMetrics logo"
                class="h-8 w-auto mr-2"
                @error="onLogoError = true"
              >
              <span
                v-else
                class="text-xl font-bold text-gray-900"
              >HireMetrics</span>
            </router-link>
          </div>
          <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
            <router-link
              to="/dashboard/vagas"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="{ 'border-blue-500 text-gray-900': $route.path === '/dashboard/vagas' }"
            >
              Vagas
            </router-link>
            <router-link
              to="/dashboard/empresas"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="{ 'border-blue-500 text-gray-900': $route.path === '/dashboard/empresas' }"
            >
              Empresas & Vagas
            </router-link>
            <router-link
              to="/dashboard/skills"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="{ 'border-blue-500 text-gray-900': $route.path === '/dashboard/skills' }"
            >
              Skills & Vagas
            </router-link>
            <router-link
              to="/dashboard/trending"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="{ 'border-blue-500 text-gray-900': $route.path === '/dashboard/trending' }"
            >
              Top Skills
            </router-link>
            <router-link
              to="/dashboard/companies"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="{ 'border-blue-500 text-gray-900': $route.path === '/dashboard/companies' }"
            >
              Empresas Ranking
            </router-link>
            <router-link
              to="/dashboard/overview"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="{ 'border-blue-500 text-gray-900': $route.path === '/dashboard/overview' }"
            >
              Overview
            </router-link>
            <router-link
              to="/dashboard/publishers"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="{ 'border-blue-500 text-gray-900': $route.path === '/dashboard/publishers' }"
            >
              Canais
            </router-link>
            <router-link
              to="/reports"
              class="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
              :class="{ 'border-blue-500 text-gray-900': $route.path === '/reports' }"
            >
              Relatórios
            </router-link>
          </div>
        </div>
        <div class="flex items-center sm:hidden">
          <button
            class="text-base font-semibold text-blue-600 px-2 py-1 bg-blue-50 rounded-l-md border-r border-blue-200 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            @click="isMobileMenuOpen = !isMobileMenuOpen"
          >
            {{ currentPageName }}
          </button>
          <button
            class="inline-flex items-center justify-center p-2 rounded-r-md text-blue-600 hover:text-blue-700 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 bg-blue-50"
            aria-expanded="false"
            @click="isMobileMenuOpen = !isMobileMenuOpen"
          >
            <span class="sr-only">Abrir menu principal</span>
            <svg
              class="h-6 w-6"
              :class="{ hidden: isMobileMenuOpen, block: !isMobileMenuOpen }"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
            <svg
              class="h-6 w-6"
              :class="{ block: isMobileMenuOpen, hidden: !isMobileMenuOpen }"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
        <div class="hidden sm:ml-6 sm:flex sm:items-center">
          <div class="ml-3 relative">
            <div>
              <button
                id="user-menu-button"
                class="bg-white rounded-full flex text-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                aria-expanded="false"
                aria-haspopup="true"
                @click="isProfileMenuOpen = !isProfileMenuOpen"
              >
                <span class="sr-only">Abrir menu do usuário</span>
                <div
                  class="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white"
                >
                  {{ userInitials }}
                </div>
              </button>
            </div>
            <div
              v-if="isProfileMenuOpen"
              class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none"
              role="menu"
              aria-orientation="vertical"
              aria-labelledby="user-menu-button"
              tabindex="-1"
            >
              <router-link
                to="/profile"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                role="menuitem"
                @click="isProfileMenuOpen = false"
              >
                Meu Perfil
              </router-link>
              <router-link
                to="/contato"
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                role="menuitem"
                @click="isProfileMenuOpen = false"
              >
                Contato
              </router-link>
              <button
                class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                role="menuitem"
                @click="handleLogout"
              >
                Sair
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="isMobileMenuOpen"
      class="sm:hidden"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="mobile-menu"
    >
      <div class="pt-2 pb-3 space-y-1">
        <router-link
          to="/dashboard/vagas"
          class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
          :class="[
            $route.path === '/dashboard/vagas'
              ? 'border-blue-500 text-blue-700 bg-blue-50'
              : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700',
          ]"
          @click="isMobileMenuOpen = false"
        >
          Vagas
        </router-link>
        <router-link
          to="/dashboard/empresas"
          class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
          :class="[
            $route.path === '/dashboard/empresas'
              ? 'border-blue-500 text-blue-700 bg-blue-50'
              : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700',
          ]"
          @click="isMobileMenuOpen = false"
        >
          Empresas & Vagas
        </router-link>
        <router-link
          to="/dashboard/skills"
          class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
          :class="[
            $route.path === '/dashboard/skills'
              ? 'border-blue-500 text-blue-700 bg-blue-50'
              : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700',
          ]"
          @click="isMobileMenuOpen = false"
        >
          Skills & Vagas
        </router-link>
        <router-link
          to="/dashboard/trending"
          class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
          :class="[
            $route.path === '/dashboard/trending'
              ? 'border-blue-500 text-blue-700 bg-blue-50'
              : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700',
          ]"
          @click="isMobileMenuOpen = false"
        >
          Top Skills
        </router-link>
        <router-link
          to="/dashboard/companies"
          class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
          :class="[
            $route.path === '/dashboard/companies'
              ? 'border-blue-500 text-blue-700 bg-blue-50'
              : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700',
          ]"
          @click="isMobileMenuOpen = false"
        >
          Empresas Ranking
        </router-link>
        <router-link
          to="/dashboard/overview"
          class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
          :class="[
            $route.path === '/dashboard/overview'
              ? 'border-blue-500 text-blue-700 bg-blue-50'
              : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700',
          ]"
          @click="isMobileMenuOpen = false"
        >
          Overview
        </router-link>
        <router-link
          to="/dashboard/publishers"
          class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
          :class="[
            $route.path === '/dashboard/publishers'
              ? 'border-blue-500 text-blue-700 bg-blue-50'
              : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700',
          ]"
          @click="isMobileMenuOpen = false"
        >
          Canais
        </router-link>
        <router-link
          to="/reports"
          class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
          :class="[
            $route.path === '/reports'
              ? 'border-blue-500 text-blue-700 bg-blue-50'
              : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700',
          ]"
          @click="isMobileMenuOpen = false"
        >
          Relatórios
        </router-link>
      </div>
      <div class="pt-4 pb-3 border-t border-gray-200">
        <div class="flex items-center px-4">
          <div class="flex-shrink-0">
            <div
              class="h-10 w-10 rounded-full bg-blue-600 flex items-center justify-center text-white"
            >
              {{ userInitials }}
            </div>
          </div>
          <div class="ml-3">
            <div class="text-base font-medium text-gray-800">
              {{ getUserDisplayName() }}
            </div>
            <div class="text-sm font-medium text-gray-500">
              {{ authStore.user?.email }}
            </div>
          </div>
        </div>
        <div class="mt-3 space-y-1">
          <router-link
            to="/profile"
            class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
            @click="isMobileMenuOpen = false"
          >
            Meu Perfil
          </router-link>
          <router-link
            to="/contato"
            class="block px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
            @click="isMobileMenuOpen = false"
          >
            Contato
          </router-link>
          <button
            class="block w-full text-left px-4 py-2 text-base font-medium text-gray-500 hover:text-gray-800 hover:bg-gray-100"
            @click="handleLogout"
          >
            Sair
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
  import { ref, computed } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import logoSrc from '@/assets/img/hire-metrics-logo-transparent.png'

  const router = useRouter()
  const authStore = useAuthStore()
  const isProfileMenuOpen = ref(false)
  const isMobileMenuOpen = ref(false)
  const onLogoError = ref(false)

  const userInitials = computed(() => {
    const user = authStore.user
    if (!user) {
      return 'U'
    }

    const initials = []

    // Get initials from first_name and last_name
    if (user.first_name) {
      initials.push(user.first_name.charAt(0))
    }
    if (user.last_name) {
      initials.push(user.last_name.charAt(0))
    }

    // If we have initials, return them; otherwise fallback to first char of email or 'U'
    if (initials.length > 0) {
      return initials.join('').toUpperCase()
    } else if (user.email) {
      return user.email.charAt(0).toUpperCase()
    } else {
      return 'U'
    }
  })

  const currentPageName = computed(() => {
    const route = router.currentRoute.value
    const path = route.path

    // Map routes to display names
    const pageNames = {
      '/dashboard/vagas': 'Vagas',
      '/dashboard/empresas': 'Empresas & Vagas',
      '/dashboard/skills': 'Skills & Vagas',
      '/dashboard/trending': 'Top Skills',
      '/dashboard/companies': 'Empresas Ranking',
      '/dashboard/overview': 'Overview',
      '/dashboard/publishers': 'Canais',
      '/reports': 'Relatórios',
      '/profile': 'Meu Perfil',
    }

    return pageNames[path] || 'Dashboard'
  })

  const getUserDisplayName = () => {
    const user = authStore.user
    if (!user) {
      return 'User'
    }

    const parts = []
    if (user.first_name) {
      parts.push(user.first_name)
    }
    if (user.last_name) {
      parts.push(user.last_name)
    }

    return parts.length > 0 ? parts.join(' ') : user.email || 'User'
  }

  const handleLogout = () => {
    isProfileMenuOpen.value = false
    isMobileMenuOpen.value = false
    authStore.logout()
    router.push('/auth/login')
  }
</script>

<style scoped>
  /* Mobile responsiveness improvements */
  @media (max-width: 768px) {
    .max-w-7xl {
      max-width: 100%;
      padding-left: 1rem;
      padding-right: 1rem;
    }

    /* Ensure mobile menu fits properly */
    .sm\\:hidden {
      width: 100%;
      max-width: 100vw;
      overflow-x: hidden;
    }

    /* Mobile menu items */
    .pt-2.pb-3.space-y-1 {
      padding-left: 1rem;
      padding-right: 1rem;
    }

    /* Ensure logo and text fit on mobile */
    .h-8.w-auto.mr-2 {
      height: 2rem;
      width: auto;
    }

    .text-xl.font-bold.text-gray-900 {
      font-size: 1.125rem;
    }
  }

  @media (max-width: 640px) {
    .max-w-7xl {
      padding-left: 0.75rem;
      padding-right: 0.75rem;
    }

    .pt-2.pb-3.space-y-1 {
      padding-left: 0.75rem;
      padding-right: 0.75rem;
    }

    .text-xl.font-bold.text-gray-900 {
      font-size: 1rem;
    }
  }

  @media (max-width: 480px) {
    .max-w-7xl {
      padding-left: 0.5rem;
      padding-right: 0.5rem;
    }

    .pt-2.pb-3.space-y-1 {
      padding-left: 0.5rem;
      padding-right: 0.5rem;
    }

    /* Ensure very small screens don't overflow */
    .h-16 {
      min-height: 4rem;
    }
  }
</style>
