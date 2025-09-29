<template>
  <nav class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo and Brand -->
        <div class="flex">
          <router-link
            to="/"
            class="flex-shrink-0 flex items-center"
          >
            <img
              v-if="!onLogoError"
              :src="logoSrc"
              alt="HireMetrics logo"
              class="h-8 w-auto mr-2"
              @error="onLogoError = true"
            >
            <h1
              v-else
              class="text-xl font-bold text-gray-900"
            >
              HireMetrics
            </h1>
          </router-link>
        </div>

        <!-- Navigation Links -->
        <div class="hidden md:flex items-center space-x-4">
          <!-- Only show these links on the landing page -->
          <template v-if="isLandingPage">
            <a
              href="#benefits"
              class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            >
              Benefícios
            </a>
            <a
              href="#how-it-works"
              class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            >
              Como Funciona
            </a>
            <a
              href="#demo"
              class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            >
              Demonstração
            </a>
            <a
              href="#testimonials"
              class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            >
              Depoimentos
            </a>
            <a
              href="#faq"
              class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            >
              FAQ
            </a>
          </template>

          <!-- Auth Links -->
          <template v-if="!isAuthenticated">
            <router-link
              to="/auth/login"
              class="ml-4 bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors duration-200"
              :class="{ 'bg-blue-700': isLoginPage }"
            >
              Login
            </router-link>
            <router-link
              to="/auth/register"
              class="ml-4 bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors duration-200"
              :class="{ 'bg-blue-700': isRegisterPage }"
            >
              Cadastrar
            </router-link>
          </template>

          <!-- User Menu (when authenticated) -->
          <template v-else>
            <router-link
              to="/dashboard"
              class="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            >
              Dashboard
            </router-link>
            <button
              class="ml-4 text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
              @click="logout"
            >
              Logout
            </button>
          </template>
        </div>

        <!-- Mobile menu button -->
        <div class="flex items-center md:hidden">
          <button
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500"
            aria-expanded="false"
            @click="isMobileMenuOpen = !isMobileMenuOpen"
          >
            <span class="sr-only">Open main menu</span>
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
      </div>
    </div>

    <!-- Mobile menu -->
    <div
      v-if="isMobileMenuOpen"
      class="md:hidden"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="mobile-menu"
    >
      <div class="pt-2 pb-3 space-y-1">
        <template v-if="isLandingPage">
          <a
            href="#benefits"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800"
            @click="isMobileMenuOpen = false"
          >
            Benefícios
          </a>
          <a
            href="#how-it-works"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800"
            @click="isMobileMenuOpen = false"
          >
            Como Funciona
          </a>
          <a
            href="#demo"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800"
            @click="isMobileMenuOpen = false"
          >
            Demonstração
          </a>
          <a
            href="#testimonials"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800"
            @click="isMobileMenuOpen = false"
          >
            Depoimentos
          </a>
          <a
            href="#faq"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800"
            @click="isMobileMenuOpen = false"
          >
            FAQ
          </a>
        </template>

        <template v-if="!isAuthenticated">
          <router-link
            to="/auth/login"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800"
            @click="isMobileMenuOpen = false"
          >
            Login
          </router-link>
          <router-link
            to="/auth/register"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800"
            @click="isMobileMenuOpen = false"
          >
            Cadastrar
          </router-link>
        </template>

        <template v-else>
          <router-link
            to="/dashboard"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800"
            @click="isMobileMenuOpen = false"
          >
            Dashboard
          </router-link>
          <button
            class="block w-full text-left pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-600 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-800"
            @click="logout"
          >
            Logout
          </button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
  import { ref, computed } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import logoSrc from '@/assets/img/hire-metrics-logo-transparent.png'

  const route = useRoute()
  const router = useRouter()
  const authStore = useAuthStore()
  const isMobileMenuOpen = ref(false)

  const onLogoError = ref(false)

  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const isLandingPage = computed(() => {
    const landingPaths = [
      '/',
      '/home',
      '/recrutamento',
      '/mercado',
      '/rh-analytics',
      '/vagas',
      '/remotas',
    ]
    return landingPaths.includes(route.path)
  })
  const isLoginPage = computed(() => route.path === '/auth/login')
  const isRegisterPage = computed(() => route.path === '/auth/register')

  const logout = async () => {
    await authStore.logout()
    router.push('/')
  }
</script>
