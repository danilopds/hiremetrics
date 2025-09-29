import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Root',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/recrutamento',
    name: 'Recrutamento',
    component: () => import('../views/LandingRecrutamento.vue'),
  },
  {
    path: '/mercado',
    name: 'Mercado',
    component: () => import('../views/LandingMercado.vue'),
  },
  {
    path: '/rh-analytics',
    name: 'RHAnalytics',
    component: () => import('../views/LandingRHAnalytics.vue'),
  },
  {
    path: '/vagas',
    name: 'Vagas',
    component: () => import('../views/LandingVagas.vue'),
  },
  {
    path: '/remotas',
    name: 'Remotas',
    component: () => import('../views/LandingRemotas.vue'),
  },
  {
    path: '/auth/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
  },
  {
    path: '/auth/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue'),
  },
  {
    path: '/auth/forgot-password',
    name: 'ForgotPassword',
    component: () => import('../views/auth/ForgotPassword.vue'),
  },
  {
    path: '/auth/reset-password/:token',
    name: 'ResetPassword',
    component: () => import('../views/auth/ResetPassword.vue'),
  },
  {
    path: '/auth/verify-email',
    name: 'VerifyEmail',
    component: () => import('../views/auth/VerifyEmail.vue'),
  },
  {
    path: '/auth/google-callback',
    name: 'GoogleCallback',
    component: () => import('../views/auth/GoogleCallback.vue'),
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    redirect: '/dashboard/vagas',
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/overview',
    name: 'Overview',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/trending',
    component: () => import('../views/TrendingView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/companies',
    component: () => import('../views/CompaniesView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/publishers',
    component: () => import('../views/PublishersView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/vagas',
    component: () => import('../views/VagasView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/empresas',
    component: () => import('../views/EmpresasView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/skills',
    component: () => import('../views/SkillsView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('../views/Reports.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true },
  },

  {
    path: '/sobre',
    name: 'Sobre',
    component: () => import('../views/Sobre.vue'),
  },
  {
    path: '/contato',
    name: 'Contato',
    component: () => import('../views/Contato.vue'),
  },
  {
    path: '/termos-de-uso',
    name: 'TermosDeUso',
    component: () => import('../views/TermosDeUso.vue'),
  },
  {
    path: '/politica-privacidade',
    name: 'PoliticaPrivacidade',
    component: () => import('../views/PoliticaPrivacidade.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Flag to prevent showing multiple expiration warnings
let expirationWarningShown = false

// Add navigation debugging and token expiration check
router.beforeEach(async (to, from, next) => {
  console.log('Navigating to:', to.path)
  const authStore = useAuthStore()
  console.log('Auth status:', authStore.isAuthenticated)

  // Handle authentication requirements
  if (to.meta.requiresAuth) {
    if (!authStore.isAuthenticated) {
      console.log('Auth required, redirecting to login')
      next('/auth/login')
      return
    }

    // Check if token is expired
    if (authStore.isTokenExpired) {
      console.log('Token expired, logging out')
      authStore.logout()

      // Show expiration message
      alert('Sua sessão expirou. Por favor, faça login novamente.')
      next('/auth/login')
      return
    }

    // Check if token will expire soon
    if (authStore.isTokenExpiringSoon && !expirationWarningShown) {
      expirationWarningShown = true

      // Show warning about imminent expiration
      alert('Sua sessão expirará em breve. Salve seu trabalho e faça login novamente.')

      // Reset the warning flag after some time
      setTimeout(() => {
        expirationWarningShown = false
      }, 60000) // Only show warning once per minute
    }

    // All dashboard features are accessible to authenticated users
  }

  next()
})

export default router
