import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Helper function for error handling
function handleApiError(error, functionName) {
  const errorMessage = error.response?.data?.detail
    ? typeof error.response.data.detail === 'string'
      ? error.response.data.detail
      : Array.isArray(error.response.data.detail)
        ? error.response.data.detail.map((err) => err.msg).join(', ')
        : 'Unknown error'
    : 'Failed to fetch data'

  console.error(`Error in ${functionName}:`, errorMessage)
  throw new Error(errorMessage)
}

export async function fetchTopCompanies(params = {}) {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/top-companies`, { params })
    return response.data
  } catch (error) {
    handleApiError(error, 'fetchTopCompanies')
  }
}

export async function fetchCompaniesSeniorityDistribution(params = {}) {
  try {
    const response = await axios.get(
      `${API_BASE_URL}/api/dashboard/companies-seniority-distribution`,
      { params }
    )
    return response.data
  } catch (error) {
    handleApiError(error, 'fetchCompaniesSeniorityDistribution')
  }
}

export async function fetchEmploymentTypeDistribution(params = {}) {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/employment-type-distribution`, {
      params,
    })
    return response.data
  } catch (error) {
    handleApiError(error, 'fetchEmploymentTypeDistribution')
  }
}

export async function fetchCompaniesRemotePercentage(params = {}) {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/companies-remote-percentage`, {
      params,
    })
    return response.data
  } catch (error) {
    handleApiError(error, 'fetchCompaniesRemotePercentage')
  }
}

export async function fetchCompaniesJobsTimeline(params = {}) {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/companies-jobs-timeline`, {
      params,
    })
    return response.data
  } catch (error) {
    handleApiError(error, 'fetchCompaniesJobsTimeline')
  }
}

export async function fetchCompaniesTopSkills(params = {}) {
  try {
    // Ensure skills_limit is within allowed range
    if (params.skills_limit && params.skills_limit > 50) {
      params.skills_limit = 50
    }

    const response = await axios.get(`${API_BASE_URL}/api/dashboard/companies-top-skills`, {
      params,
    })

    return response.data
  } catch (error) {
    handleApiError(error, 'fetchCompaniesTopSkills')
  }
}

export async function fetchCompaniesKpis(params = {}) {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/companies-kpis`, { params })
    return response.data
  } catch (error) {
    handleApiError(error, 'fetchCompaniesKpis')
  }
}

export async function fetchAvailableCompanies(search_position_query = null) {
  try {
    const params = {}
    if (search_position_query) {
      params.search_position_query = search_position_query
    }
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/available-companies`, {
      params,
    })
    return response.data
  } catch (error) {
    handleApiError(error, 'fetchAvailableCompanies')
  }
}

export async function fetchAvailableSeniorityLevels(search_position_query = null) {
  try {
    const params = {}
    if (search_position_query) {
      params.search_position_query = search_position_query
    }
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/available-seniority-levels`, {
      params,
    })
    return response.data
  } catch (error) {
    handleApiError(error, 'fetchAvailableSeniorityLevels')
  }
}

export async function fetchAvailablePositions() {
  try {
    const response = await axios.get(`${API_BASE_URL}/api/dashboard/available-positions`)
    return response.data
  } catch (error) {
    handleApiError(error, 'fetchAvailablePositions')
  }
}
