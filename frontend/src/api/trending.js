import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function fetchTopSkills(params = {}) {
  const response = await axios.get(`${API_BASE_URL}/api/dashboard/top-skills`, { params })
  return response.data
}

export async function fetchWordCloudSkills(params = {}) {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/top-skills`, { params })
    if (!response.data || !Array.isArray(response.data)) {
      throw new Error('Invalid response format')
    }
    return response.data
  } catch (error) {
    console.error('Error in fetchWordCloudSkills:', error)
    throw error
  }
}

export async function fetchSkillsTrend(params = {}) {
  const response = await axios.get(`${API_BASE_URL}/api/dashboard/skills-trend`, { params })
  return response.data
}

export async function fetchAvailableSkills(token, search_position_query = null) {
  const params = {}
  if (search_position_query) {
    params.search_position_query = search_position_query
  }
  const response = await axios.get(`${API_BASE_URL}/api/dashboard/available-skills`, {
    headers: { Authorization: `Bearer ${token}` },
    params,
  })
  return response.data
}

export async function fetchAvailableSeniorityLevels(token, search_position_query = null) {
  const params = {}
  if (search_position_query) {
    params.search_position_query = search_position_query
  }
  const response = await axios.get(`${API_BASE_URL}/api/dashboard/available-seniority-levels`, {
    headers: { Authorization: `Bearer ${token}` },
    params,
  })
  return response.data
}

export async function fetchAvailablePositions() {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/available-positions`)
    return response.data
  } catch (error) {
    console.error('Error fetching available positions:', error)
    throw error
  }
}
