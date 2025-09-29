import publicApiClient from './public-api'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Transform filter object to API format
const transformFilters = (filters) => {
  // Handle remote filter properly
  let jobIsRemote = null
  if (filters.selectedRemoteTypes && filters.selectedRemoteTypes.length > 0) {
    // Check if the array contains both "true" and "false" or empty string (means "Todas")
    if (
      filters.selectedRemoteTypes.includes('') ||
      (filters.selectedRemoteTypes.includes('true') &&
        filters.selectedRemoteTypes.includes('false'))
    ) {
      // If "Todas" is selected or both options are selected, don't filter by remote
      jobIsRemote = null
    } else if (filters.selectedRemoteTypes.includes('true')) {
      jobIsRemote = true
    } else if (filters.selectedRemoteTypes.includes('false')) {
      jobIsRemote = false
    }
  }

  // Handle direct application filter
  let isDirect = null
  if (filters.selectedDirectTypes && filters.selectedDirectTypes.length > 0) {
    // Check if the array contains both "true" and "false" or empty string (means "Todas")
    if (
      filters.selectedDirectTypes.includes('') ||
      (filters.selectedDirectTypes.includes('true') &&
        filters.selectedDirectTypes.includes('false'))
    ) {
      // If "Todas" is selected or both options are selected, don't filter by direct application
      isDirect = null
    } else if (filters.selectedDirectTypes.includes('true')) {
      isDirect = true
    } else if (filters.selectedDirectTypes.includes('false')) {
      isDirect = false
    }
  }

  return {
    job_posted_at_date_from: filters.dateFrom || null,
    job_posted_at_date_to: filters.dateTo || null,
    search_position_query: filters.selectedPosition || null,
    employer_names: filters.selectedCompanies?.filter((c) => c !== '') || [],
    publishers: filters.selectedPublishers?.filter((p) => p !== '') || [],
    seniority_levels: filters.selectedSeniority?.filter((s) => s !== '') || [],
    employment_types: filters.selectedEmploymentTypes?.filter((t) => t !== '') || [],
    cities: filters.selectedCities?.filter((c) => c !== '') || [],
    states: filters.selectedStates?.filter((s) => s !== '') || [],
    skills: filters.selectedSkills?.filter((s) => s !== '') || [],
    job_is_remote: jobIsRemote,
    is_direct: isDirect,
  }
}

export const publicReportsApi = {
  // Preview export data (public endpoint)
  async previewExport(filters, limit = 15) {
    try {
      const transformed = transformFilters(filters)
      const queryParams = new URLSearchParams()
      for (const key in transformed) {
        if (transformed[key] !== null && transformed[key] !== undefined) {
          queryParams.append(key, transformed[key])
        }
      }
      queryParams.append('limit', limit)

      const response = await publicApiClient.get(
        `${API_BASE_URL}/api/public/preview-export?${queryParams.toString()}`
      )
      return response.data
    } catch (error) {
      console.error('Error fetching preview export:', error)
      throw error
    }
  },

  // Count records (public endpoint)
  async countExportRecords(filters, maxRecords = 50000) {
    try {
      const response = await publicApiClient.post(
        `${API_BASE_URL}/api/public/count-export-records`,
        {
          filters: transformFilters(filters),
          max_records: maxRecords,
        }
      )
      return response.data
    } catch (error) {
      console.error('Error counting export records:', error)
      throw new Error(error.response?.data?.detail || 'Failed to count records')
    }
  },

  // Get available positions (public endpoint)
  async getAvailablePositions() {
    try {
      const response = await publicApiClient.get(`${API_BASE_URL}/api/public/available-positions`)
      return response.data
    } catch (error) {
      console.error('Error fetching positions:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch positions')
    }
  },
}
