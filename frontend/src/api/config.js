/**
 * API Configuration Module
 *
 * Centralizes API configuration and provides utility functions for API requests.
 * This eliminates duplicate code across the application.
 */

import axios from 'axios'

/**
 * Determines the API base URL based on the environment
 * @returns {string} The API base URL
 */
export const getApiBaseUrl = () => {
  if (window.location.hostname === 'localhost') {
    // Local development
    return import.meta.env.VITE_API_URL || 'http://localhost:8000'
  } else {
    // Production environment - use the API subdomain with the same protocol
    const protocol = window.location.protocol
    const domain = window.location.hostname.replace('www.', '')
    return `${protocol}//api.${domain}`
  }
}

// API base URL
export const API_BASE_URL = getApiBaseUrl()

// Flag to prevent multiple expiration messages
let isExpiredMessageShown = false

/**
 * Creates a configured axios instance with proper interceptors
 * @returns {import('axios').AxiosInstance} Configured axios instance
 */
export const createApiClient = () => {
  // Create a centralized axios instance
  const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  // Request interceptor to add auth token
  apiClient.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  // Response interceptor to handle token expiration globally
  apiClient.interceptors.response.use(
    (response) => {
      return response
    },
    (error) => {
      if (error.response?.status === 401 && !isExpiredMessageShown) {
        isExpiredMessageShown = true

        // Token expired or invalid, show message
        const message = 'Sua sessão expirou. Você será redirecionado para a página de login.'
        alert(message)

        // Clear auth data
        localStorage.removeItem('token')
        localStorage.removeItem('user')

        // Redirect after a short delay to allow user to see the message
        setTimeout(() => {
          window.location.href = '/auth/login'
          isExpiredMessageShown = false
        }, 2000)

        return Promise.reject(new Error('Authentication expired'))
      }
      return Promise.reject(error)
    }
  )

  return apiClient
}

// Create and export the default API client
const apiClient = createApiClient()
export default apiClient

/**
 * Handles API errors consistently
 * @param {Error} error - The error object from axios
 * @param {string} fallbackMessage - Fallback message if error details aren't available
 * @returns {string} Formatted error message
 */
export const handleApiError = (error, fallbackMessage = 'Ocorreu um erro na operação') => {
  // Check for specific error response format
  if (error.response?.data?.detail) {
    return error.response.data.detail
  }

  // Check for message in response data
  if (error.response?.data?.message) {
    return error.response.data.message
  }

  // Check for error message
  if (error.message && error.message !== 'Authentication expired') {
    return error.message
  }

  // Return fallback message
  return fallbackMessage
}
