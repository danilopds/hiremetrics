import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import {
  login as apiLogin,
  register as apiRegister,
  requestPasswordReset as apiRequestPasswordReset,
  resetPassword as apiResetPassword,
  validateResetToken as apiValidateResetToken,
  resendVerification as apiResendVerification,
} from '@/api/auth'
import apiClient, { API_BASE_URL } from '@/api/config'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user')) || null)
  const resetToken = ref(null)
  const tokenExpiration = ref(localStorage.getItem('tokenExpiration') || null)

  const isAuthenticated = computed(() => !!token.value)

  // Check if token is expired or about to expire
  const isTokenExpired = computed(() => {
    if (!tokenExpiration.value) {
      return false
    }

    const expirationTime = parseInt(tokenExpiration.value)
    const now = Date.now()

    // Return true if token is expired
    return now >= expirationTime
  })

  // Check if token will expire in the next 5 minutes
  const isTokenExpiringSoon = computed(() => {
    if (!tokenExpiration.value) {
      return false
    }

    const expirationTime = parseInt(tokenExpiration.value)
    const now = Date.now()
    const fiveMinutesMs = 5 * 60 * 1000

    // Return true if token will expire in less than 5 minutes
    return now >= expirationTime - fiveMinutesMs
  })

  const login = async (email, password) => {
    try {
      console.log('Auth store: Attempting login')

      // Clear any previously persisted selections to ensure clean state for new user
      localStorage.removeItem('vagas_selected_job')
      localStorage.removeItem('empresas_selected_company')
      localStorage.removeItem('skills_selected_skill')

      // Clear persisted filters to prevent stale data for new user
      localStorage.removeItem('vagas_filters')
      localStorage.removeItem('empresas_filters')
      localStorage.removeItem('skills_filters')

      const response = await apiLogin(email, password)

      // Calculate token expiration time (50 minutes from now)
      const expirationTime = Date.now() + 50 * 60 * 1000
      localStorage.setItem('tokenExpiration', expirationTime.toString())
      tokenExpiration.value = expirationTime.toString()

      // Save to localStorage
      localStorage.setItem('token', response.access_token)

      // Get user data
      const userData = await getCurrentUser()
      localStorage.setItem('user', JSON.stringify(userData))

      // Update store state
      token.value = response.access_token
      user.value = userData

      console.log('Auth store: Login successful')
      return true
    } catch (error) {
      console.error('Auth store: Login error:', error)
      throw error
    }
  }

  const register = async (userData) => {
    try {
      console.log('Auth store: Attempting registration')

      // Clear any previously persisted selections to ensure clean state for new user
      localStorage.removeItem('vagas_selected_job')
      localStorage.removeItem('empresas_selected_company')
      localStorage.removeItem('skills_selected_skill')

      // Clear persisted filters to prevent stale data for new user
      localStorage.removeItem('vagas_filters')
      localStorage.removeItem('empresas_filters')
      localStorage.removeItem('skills_filters')

      const response = await apiRegister(userData)

      // Calculate token expiration time (50 minutes from now)
      const expirationTime = Date.now() + 50 * 60 * 1000
      localStorage.setItem('tokenExpiration', expirationTime.toString())
      tokenExpiration.value = expirationTime.toString()

      // Save to localStorage
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response))

      // Update store state
      token.value = response.access_token
      user.value = response

      console.log('Auth store: Registration successful')
      return true
    } catch (error) {
      console.error('Auth store: Registration error:', error)
      throw error
    }
  }

  const logout = () => {
    console.log('Auth store: Logging out')
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('tokenExpiration')

    // Clear all sessionStorage items to reset alert banners and other session-based data
    sessionStorage.clear()

    // Clear persisted selections to ensure clean state on next login
    localStorage.removeItem('vagas_selected_job')
    localStorage.removeItem('empresas_selected_company')
    localStorage.removeItem('skills_selected_skill')

    // Clear persisted filters to prevent stale data on next login
    localStorage.removeItem('vagas_filters')
    localStorage.removeItem('empresas_filters')
    localStorage.removeItem('skills_filters')

    token.value = null
    user.value = null
    tokenExpiration.value = null
  }

  const setToken = (newToken) => {
    // Calculate token expiration time (50 minutes from now)
    const expirationTime = Date.now() + 50 * 60 * 1000
    localStorage.setItem('tokenExpiration', expirationTime.toString())
    tokenExpiration.value = expirationTime.toString()

    // Clear any previously persisted selections when setting a new token
    // This ensures clean state for new sessions
    localStorage.removeItem('vagas_selected_job')
    localStorage.removeItem('empresas_selected_company')
    localStorage.removeItem('skills_selected_skill')

    // Clear persisted filters to prevent stale data for new sessions
    localStorage.removeItem('vagas_filters')
    localStorage.removeItem('empresas_filters')
    localStorage.removeItem('skills_filters')

    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUser = (newUser) => {
    user.value = newUser
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  const requestPasswordReset = async (email) => {
    try {
      console.log('Auth store: Requesting password reset for:', email)
      const data = await apiRequestPasswordReset(email)
      return data
    } catch (error) {
      console.error('Auth store: Password reset request error:', error)
      throw error
    }
  }

  const resetPassword = async (token, newPassword) => {
    try {
      console.log('Auth store: Resetting password with token:', token)
      const data = await apiResetPassword(token, newPassword)
      return data
    } catch (error) {
      console.error('Auth store: Password reset error:', error)
      throw error
    }
  }

  const validateResetToken = async (token) => {
    try {
      console.log('Auth store: Validating reset token:', token)
      const data = await apiValidateResetToken(token)
      return data.success
    } catch (error) {
      console.error('Auth store: Token validation error:', error)
      throw error
    }
  }

  const resendVerification = async (email) => {
    try {
      console.log('Auth store: Resending verification email for:', email)
      const data = await apiResendVerification(email)
      return data
    } catch (error) {
      console.error('Auth store: Resend verification error:', error)
      throw error
    }
  }

  const getCurrentUser = async () => {
    try {
      // Use the apiClient from axios-config which has proper error handling
      const response = await apiClient.get(`${API_BASE_URL}/api/auth/me`, {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      })

      return response.data
    } catch (error) {
      console.error('Error getting current user:', error)

      // Check if token is invalid and clear auth if needed
      if (error.response && (error.response.status === 401 || error.response.status === 403)) {
        console.warn('Authentication token invalid or expired, logging out')
        logout() // Clear the invalid token
      }

      throw error
    }
  }

  const updateUserPreferences = async () => {
    try {
      // Refresh user data to get the latest preferences
      const updatedUser = await getCurrentUser()
      setUser(updatedUser)
      return updatedUser
    } catch (error) {
      console.error('Error updating user preferences:', error)
      throw error
    }
  }

  return {
    token,
    user,
    resetToken,
    tokenExpiration,
    isAuthenticated,
    isTokenExpired,
    isTokenExpiringSoon,
    login,
    register,
    logout,
    setToken,
    setUser,
    getCurrentUser,
    requestPasswordReset,
    resetPassword,
    validateResetToken,
    resendVerification,
    updateUserPreferences,
  }
})
