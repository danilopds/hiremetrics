/**
 * @deprecated Use the apiClient from '@/api/config.js' instead
 * This file is kept for backward compatibility and will be removed in future versions
 */
import apiClient, { API_BASE_URL } from './config'

// Log for debugging during transition period
console.log('API Base URL:', API_BASE_URL)

export default apiClient
