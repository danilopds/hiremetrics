import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useProfileStore = defineStore('profile', () => {
  // State
  const profile = ref({
    name: '',
    email: '',
    jobTitle: '',
    company: '',
    industry: '',
    location: '',
  })

  const preferences = ref({
    emailNotifications: true,
    reportNotifications: true,
    defaultTimeRange: '30d',
    chartType: 'line',
    timezone: 'UTC',
  })

  const activeSessions = ref([])
  const loading = ref(false)
  const error = ref('')

  // Getters
  const isProfileComplete = computed(() => {
    return profile.value.name && profile.value.email
  })

  const hasActiveSessions = computed(() => {
    return activeSessions.value.length > 0
  })

  // Actions
  const fetchProfile = async () => {
    loading.value = true
    error.value = ''
    try {
      // TODO: Replace with actual API call
      const response = await new Promise((resolve) =>
        setTimeout(
          () =>
            resolve({
              name: 'John Doe',
              email: 'john@example.com',
              jobTitle: 'Software Engineer',
              company: 'Tech Corp',
              industry: 'Technology',
              location: 'New York',
            }),
          1000
        )
      )
      profile.value = response
    } catch (e) {
      error.value = 'Failed to fetch profile'
      console.error('Profile fetch error:', e)
    } finally {
      loading.value = false
    }
  }

  const updateProfile = async (profileData) => {
    loading.value = true
    error.value = ''
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      profile.value = { ...profile.value, ...profileData }
      return true
    } catch (e) {
      error.value = 'Failed to update profile'
      console.error('Profile update error:', e)
      return false
    } finally {
      loading.value = false
    }
  }

  const updatePassword = async () => {
    loading.value = true
    error.value = ''
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      return true
    } catch (e) {
      error.value = 'Failed to update password'
      console.error('Password update error:', e)
      return false
    } finally {
      loading.value = false
    }
  }

  const fetchActiveSessions = async () => {
    loading.value = true
    error.value = ''
    try {
      // TODO: Replace with actual API call
      const response = await new Promise((resolve) =>
        setTimeout(
          () =>
            resolve([
              {
                id: 1,
                device: 'Chrome on Windows',
                location: 'New York, USA',
                lastActive: '2 minutes ago',
              },
              {
                id: 2,
                device: 'Safari on iPhone',
                location: 'San Francisco, USA',
                lastActive: '1 hour ago',
              },
            ]),
          1000
        )
      )
      activeSessions.value = response
    } catch (e) {
      error.value = 'Failed to fetch active sessions'
      console.error('Sessions fetch error:', e)
    } finally {
      loading.value = false
    }
  }

  const terminateSession = async (sessionId) => {
    loading.value = true
    error.value = ''
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 500))
      activeSessions.value = activeSessions.value.filter((session) => session.id !== sessionId)
      return true
    } catch (e) {
      error.value = 'Failed to terminate session'
      console.error('Session termination error:', e)
      return false
    } finally {
      loading.value = false
    }
  }

  const updatePreferences = async (preferencesData) => {
    loading.value = true
    error.value = ''
    try {
      // TODO: Replace with actual API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      preferences.value = { ...preferences.value, ...preferencesData }
      return true
    } catch (e) {
      error.value = 'Failed to update preferences'
      console.error('Preferences update error:', e)
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    // State
    profile,
    preferences,
    activeSessions,
    loading,
    error,
    // Getters
    isProfileComplete,
    hasActiveSessions,
    // Actions
    fetchProfile,
    updateProfile,
    updatePassword,
    fetchActiveSessions,
    terminateSession,
    updatePreferences,
  }
})
