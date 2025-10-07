<template>
  <nav class="bg-black border-b border-gray-800 sticky top-0 z-50 backdrop-blur-sm bg-opacity-95">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo and Brand -->
        <div class="flex items-center">
          <router-link
            to="/"
            class="flex-shrink-0 flex items-center group"
          >
            <img
              v-if="!onLogoError"
              :src="logoSrc"
              alt="HireMetrics logo"
              class="h-8 w-auto mr-2"
              @error="onLogoError = true"
            >            
          </router-link>
        </div>

        <!-- Navigation Links -->
        <div class="hidden md:flex items-center space-x-1">
          <!-- Only show these links on the landing page -->
          <template v-if="isLandingPage">
            <a
              href="#benefits"
              class="text-gray-300 hover:text-cyan-400 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 font-mono"
            >
              Features
            </a>
            <a
              href="#how-it-works"
              class="text-gray-300 hover:text-cyan-400 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 font-mono"
            >
              Architecture
            </a>
            <a
              href="#community"
              class="text-gray-300 hover:text-cyan-400 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 font-mono"
            >
              Community
            </a>
            <a
              href="#demo"
              class="text-gray-300 hover:text-cyan-400 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 font-mono"
            >
              Demo
            </a>
            
            <!-- GitHub Link -->
            <a
              href="https://github.com/danilopds/hiremetrics"
              target="_blank"
              rel="noopener noreferrer"
              class="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 flex items-center space-x-1"
              title="View on GitHub"
            >
              <svg
                class="w-5 h-5"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  fill-rule="evenodd"
                  d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                  clip-rule="evenodd"
                />
              </svg>
            </a>
            
            <!-- Discord Link -->
            <a
              href="https://discord.gg/rr7TkzzR"
              target="_blank"
              rel="noopener noreferrer"
              class="text-gray-300 hover:text-indigo-400 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 flex items-center space-x-1"
              title="Join Discord"
            >
              <svg
                class="w-5 h-5"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M20.317 4.37a19.791 19.791 0 00-4.885-1.515.074.074 0 00-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 00-5.487 0 12.64 12.64 0 00-.617-1.25.077.077 0 00-.079-.037A19.736 19.736 0 003.677 4.37a.07.07 0 00-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 00.031.057 19.9 19.9 0 005.993 3.03.078.078 0 00.084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 00-.041-.106 13.107 13.107 0 01-1.872-.892.077.077 0 01-.008-.128 10.2 10.2 0 00.372-.292.074.074 0 01.077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 01.078.01c.12.098.246.198.373.292a.077.077 0 01-.006.127 12.299 12.299 0 01-1.873.892.077.077 0 00-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 00.084.028 19.839 19.839 0 006.002-3.03.077.077 0 00.032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 00-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z" />
              </svg>
            </a>
          </template>

          <!-- Auth Links -->
          <template v-if="!isAuthenticated">
            <router-link
              to="/auth/login"
              class="ml-4 border border-cyan-500 text-cyan-400 hover:bg-cyan-500 hover:text-white px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 font-mono"
              :class="{ 'bg-cyan-500 text-white': isLoginPage }"
            >
              Login
            </router-link>
            <router-link
              to="/auth/register"
              class="ml-2 bg-gradient-to-r from-cyan-500 to-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:from-cyan-600 hover:to-blue-700 transition-all duration-200 font-mono shadow-lg shadow-cyan-500/50"
              :class="{ 'from-cyan-600 to-blue-700': isRegisterPage }"
            >
              Sign Up
            </router-link>
          </template>

          <!-- User Menu (when authenticated) -->
          <template v-else>
            <router-link
              to="/dashboard"
              class="text-gray-300 hover:text-cyan-400 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 font-mono"
            >
              Dashboard
            </router-link>
            <button
              class="ml-4 text-gray-300 hover:text-red-400 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 font-mono"
              @click="logout"
            >
              Logout
            </button>
          </template>
        </div>

        <!-- Mobile menu button -->
        <div class="flex items-center md:hidden">
          <button
            class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-cyan-400 hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-cyan-500 transition-colors"
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
      class="md:hidden bg-gray-900 border-t border-gray-800"
      role="menu"
      aria-orientation="vertical"
      aria-labelledby="mobile-menu"
    >
      <div class="pt-2 pb-3 space-y-1">
        <template v-if="isLandingPage">
          <a
            href="#benefits"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-300 hover:bg-gray-800 hover:border-cyan-500 hover:text-cyan-400 transition-colors font-mono"
            @click="isMobileMenuOpen = false"
          >
            Features
          </a>
          <a
            href="#how-it-works"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-300 hover:bg-gray-800 hover:border-cyan-500 hover:text-cyan-400 transition-colors font-mono"
            @click="isMobileMenuOpen = false"
          >
            Architecture
          </a>
          <a
            href="#community"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-300 hover:bg-gray-800 hover:border-cyan-500 hover:text-cyan-400 transition-colors font-mono"
            @click="isMobileMenuOpen = false"
          >
            Community
          </a>
          <a
            href="#demo"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-300 hover:bg-gray-800 hover:border-cyan-500 hover:text-cyan-400 transition-colors font-mono"
            @click="isMobileMenuOpen = false"
          >
            Demo
          </a>
          
          <!-- Mobile GitHub Link -->
          <a
            href="https://github.com/danilopds/hiremetrics"
            target="_blank"
            rel="noopener noreferrer"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-300 hover:bg-gray-800 hover:border-gray-500 hover:text-white transition-colors flex items-center space-x-2"
            @click="isMobileMenuOpen = false"
          >
            <svg
              class="w-5 h-5"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                fill-rule="evenodd"
                d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                clip-rule="evenodd"
              />
            </svg>
            <span>GitHub</span>
          </a>
          
          <!-- Mobile Discord Link -->
          <a
            href="https://discord.gg/rr7TkzzR"
            target="_blank"
            rel="noopener noreferrer"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-300 hover:bg-gray-800 hover:border-indigo-500 hover:text-indigo-400 transition-colors flex items-center space-x-2"
            @click="isMobileMenuOpen = false"
          >
            <svg
              class="w-5 h-5"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M20.317 4.37a19.791 19.791 0 00-4.885-1.515.074.074 0 00-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 00-5.487 0 12.64 12.64 0 00-.617-1.25.077.077 0 00-.079-.037A19.736 19.736 0 003.677 4.37a.07.07 0 00-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 00.031.057 19.9 19.9 0 005.993 3.03.078.078 0 00.084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 00-.041-.106 13.107 13.107 0 01-1.872-.892.077.077 0 01-.008-.128 10.2 10.2 0 00.372-.292.074.074 0 01.077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 01.078.01c.12.098.246.198.373.292a.077.077 0 01-.006.127 12.299 12.299 0 01-1.873.892.077.077 0 00-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 00.084.028 19.839 19.839 0 006.002-3.03.077.077 0 00.032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 00-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z" />
            </svg>
            <span>Discord</span>
          </a>
        </template>

        <template v-if="!isAuthenticated">
          <router-link
            to="/auth/login"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-300 hover:bg-gray-800 hover:border-cyan-500 hover:text-cyan-400 transition-colors font-mono"
            @click="isMobileMenuOpen = false"
          >
            Login
          </router-link>
          <router-link
            to="/auth/register"
            class="block pl-3 pr-4 py-2 border-l-4 border-cyan-500 text-base font-medium text-cyan-400 hover:bg-gray-800 transition-colors font-mono"
            @click="isMobileMenuOpen = false"
          >
            Sign Up
          </router-link>
        </template>

        <template v-else>
          <router-link
            to="/dashboard"
            class="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-300 hover:bg-gray-800 hover:border-cyan-500 hover:text-cyan-400 transition-colors font-mono"
            @click="isMobileMenuOpen = false"
          >
            Dashboard
          </router-link>
          <button
            class="block w-full text-left pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-gray-300 hover:bg-gray-800 hover:border-red-500 hover:text-red-400 transition-colors font-mono"
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
