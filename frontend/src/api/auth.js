import apiClient from './config'

// Use the centralized API client for all auth operations
const authApi = apiClient

export const login = async (email, password) => {
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)

  const response = await authApi.post('/api/auth/token', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const register = async (userData) => {
  const response = await authApi.post('/api/auth/register', userData)
  return response.data
}

export const getCurrentUser = async () => {
  const response = await authApi.get('/api/auth/me')
  return response.data
}

export const changePassword = async (passwordData) => {
  const response = await authApi.post('/api/auth/change-password', passwordData)
  return response.data
}

export const updateUserPreferences = async (preferences) => {
  const response = await authApi.put('/api/auth/preferences', preferences)
  return response.data
}

export const requestPasswordReset = async (email) => {
  const response = await authApi.post('/api/auth/forgot-password', { email })
  return response.data
}

export const resetPassword = async (token, newPassword) => {
  const response = await authApi.post('/api/auth/reset-password', {
    token,
    new_password: newPassword,
  })
  return response.data
}

export const validateResetToken = async (token) => {
  const response = await authApi.post('/api/auth/validate-reset-token', { token })
  return response.data
}

export const resendVerification = async (email) => {
  const response = await authApi.post('/api/auth/resend-verification', { email })
  return response.data
}

export default authApi
