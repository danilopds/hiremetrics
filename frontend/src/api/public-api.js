import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create a public axios instance without auth interceptors
const publicApiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Simple response interceptor that doesn't redirect on 401
publicApiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // For public endpoints, we don't redirect on 401, just return the error
    return Promise.reject(error)
  }
)

export default publicApiClient
