import apiClient from './axios-config'

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

export const reportsApi = {
  // Count records that would be exported
  async countExportRecords(filters, maxRecords = 50000) {
    try {
      const response = await apiClient.post(`${API_BASE_URL}/api/reports/count-export-records`, {
        filters: transformFilters(filters),
        max_records: maxRecords,
      })
      return response.data
    } catch (error) {
      console.error('Error counting export records:', error)
      throw new Error(error.response?.data?.detail || 'Failed to count records')
    }
  },

  // Export CSV data
  async exportCSV(filters, maxRecords = 50000) {
    try {
      const response = await apiClient.post(
        `${API_BASE_URL}/api/reports/export-csv`,
        {
          filters: transformFilters(filters),
          max_records: maxRecords,
        },
        {
          responseType: 'blob',
        }
      )

      // Create blob and download
      const blob = new Blob([response.data], { type: 'text/csv;charset=utf-8' })
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url

      // Get filename from Content-Disposition header or use default
      const contentDisposition = response.headers['content-disposition']
      let filename = 'jobs_export.csv'
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/)
        if (filenameMatch) {
          filename = filenameMatch[1]
        }
      }

      link.setAttribute('download', filename)
      document.body.appendChild(link)
      link.click()
      link.remove()
      window.URL.revokeObjectURL(url)

      return { success: true, filename }
    } catch (error) {
      console.error('Error exporting CSV:', error)
      throw new Error(error.response?.data?.detail || 'Failed to export CSV')
    }
  },

  // Preview export data
  async previewExport(filters, limit = 10) {
    try {
      const queryParams = new URLSearchParams()

      if (filters.dateFrom) {
        queryParams.append('job_posted_at_date_from', filters.dateFrom)
      }
      if (filters.dateTo) {
        queryParams.append('job_posted_at_date_to', filters.dateTo)
      }
      if (filters.selectedPosition) {
        queryParams.append('search_position_query', filters.selectedPosition)
      }

      // Filter out empty string values (which represent "Todas")
      const nonEmptyCompanies = filters.selectedCompanies?.filter((c) => c !== '') || []
      const nonEmptyPublishers = filters.selectedPublishers?.filter((p) => p !== '') || []
      const nonEmptySeniority = filters.selectedSeniority?.filter((s) => s !== '') || []
      const nonEmptyEmploymentTypes = filters.selectedEmploymentTypes?.filter((t) => t !== '') || []
      const nonEmptyCities = filters.selectedCities?.filter((c) => c !== '') || []
      const nonEmptyStates = filters.selectedStates?.filter((s) => s !== '') || []
      const nonEmptySkills = filters.selectedSkills?.filter((s) => s !== '') || []

      if (nonEmptyCompanies.length) {
        queryParams.append('employer_names', nonEmptyCompanies.join(','))
      }
      if (nonEmptyPublishers.length) {
        queryParams.append('publishers', nonEmptyPublishers.join(','))
      }
      if (nonEmptySeniority.length) {
        queryParams.append('seniority_levels', nonEmptySeniority.join(','))
      }
      if (nonEmptyEmploymentTypes.length) {
        queryParams.append('employment_types', nonEmptyEmploymentTypes.join(','))
      }
      if (nonEmptyCities.length) {
        queryParams.append('cities', nonEmptyCities.join(','))
      }
      if (nonEmptyStates.length) {
        queryParams.append('states', nonEmptyStates.join(','))
      }
      if (nonEmptySkills.length) {
        queryParams.append('skills', nonEmptySkills.join(','))
      }

      // Handle remote filter
      if (filters.selectedRemoteTypes && filters.selectedRemoteTypes.length > 0) {
        // If "Todas" is selected or both options are selected, don't filter by remote
        if (
          !filters.selectedRemoteTypes.includes('') &&
          !(
            filters.selectedRemoteTypes.includes('true') &&
            filters.selectedRemoteTypes.includes('false')
          )
        ) {
          if (filters.selectedRemoteTypes.includes('true')) {
            queryParams.append('job_is_remote', 'true')
          } else if (filters.selectedRemoteTypes.includes('false')) {
            queryParams.append('job_is_remote', 'false')
          }
        }
      }

      // Handle direct application filter
      if (filters.selectedDirectTypes && filters.selectedDirectTypes.length > 0) {
        // If "Todas" is selected or both options are selected, don't filter by direct application
        if (
          !filters.selectedDirectTypes.includes('') &&
          !(
            filters.selectedDirectTypes.includes('true') &&
            filters.selectedDirectTypes.includes('false')
          )
        ) {
          if (filters.selectedDirectTypes.includes('true')) {
            queryParams.append('is_direct', 'true')
          } else if (filters.selectedDirectTypes.includes('false')) {
            queryParams.append('is_direct', 'false')
          }
        }
      }

      queryParams.append('limit', limit)

      const response = await apiClient.get(
        `${API_BASE_URL}/api/reports/preview-export?${queryParams.toString()}`
      )
      return response.data
    } catch (error) {
      console.error('Error previewing export:', error)
      throw new Error(error.response?.data?.detail || 'Failed to preview export')
    }
  },

  // Get available filter options
  async getAvailableLocations(position = null) {
    try {
      const params = {}
      if (position) {
        params.search_position_query = position
      }

      const response = await apiClient.get(`${API_BASE_URL}/api/dashboard/locations`, { params })
      return response.data
    } catch (error) {
      console.error('Error fetching locations:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch locations')
    }
  },

  async getAvailableEmploymentTypes() {
    try {
      const response = await apiClient.get(`${API_BASE_URL}/api/reports/available-employment-types`)
      return response.data
    } catch (error) {
      console.error('Error fetching employment types:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch employment types')
    }
  },

  // Get available positions
  async getAvailablePositions() {
    try {
      const response = await apiClient.get(`${API_BASE_URL}/api/dashboard/available-positions`)
      return response.data
    } catch (error) {
      console.error('Error fetching positions:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch positions')
    }
  },

  // Use existing dashboard endpoints for other filter options
  async getAvailableCompanies(position = null) {
    try {
      const params = {}
      if (position) {
        params.search_position_query = position
      }

      const response = await apiClient.get(`${API_BASE_URL}/api/dashboard/available-companies`, {
        params,
      })
      return response.data
    } catch (error) {
      console.error('Error fetching companies:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch companies')
    }
  },

  async getAvailablePublishers(position = null) {
    try {
      const params = {}
      if (position) {
        params.search_position_query = position
      }

      const response = await apiClient.get(`${API_BASE_URL}/api/dashboard/available-publishers`, {
        params,
      })
      return response.data
    } catch (error) {
      console.error('Error fetching publishers:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch publishers')
    }
  },

  async getAvailableSeniority(position = null) {
    try {
      const params = {}
      if (position) {
        params.search_position_query = position
      }

      const response = await apiClient.get(
        `${API_BASE_URL}/api/dashboard/available-seniority-levels`,
        { params }
      )
      return response.data
    } catch (error) {
      console.error('Error fetching seniority levels:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch seniority levels')
    }
  },

  async getAvailableSkills(position = null) {
    try {
      const params = {}
      if (position) {
        params.search_position_query = position
      }

      const response = await apiClient.get(`${API_BASE_URL}/api/dashboard/available-skills`, {
        params,
      })
      return response.data
    } catch (error) {
      console.error('Error fetching skills:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch skills')
    }
  },

  // Get jobs filtered by skills using the dedicated skills endpoint
  async getJobsBySkills(filters) {
    try {
      const params = {
        skills: filters.selectedSkills?.join(',') || '',
        limit: 10000,
      }

      // Add optional filters if they exist
      if (filters.dateFrom) {
        params.job_posted_at_date_from = filters.dateFrom
      }
      if (filters.dateTo) {
        params.job_posted_at_date_to = filters.dateTo
      }
      if (filters.selectedPosition) {
        params.search_position_query = filters.selectedPosition
      }
      if (filters.selectedCompanies?.length > 0) {
        params.employer_names = filters.selectedCompanies.join(',')
      }
      if (filters.selectedPublishers?.length > 0) {
        params.publishers = filters.selectedPublishers.join(',')
      }
      if (filters.selectedSeniority?.length > 0) {
        params.seniority_levels = filters.selectedSeniority.join(',')
      }
      if (filters.selectedEmploymentTypes?.length > 0) {
        params.employment_types = filters.selectedEmploymentTypes.join(',')
      }
      if (filters.selectedCities?.length > 0) {
        params.cities = filters.selectedCities.join(',')
      }
      if (filters.selectedStates?.length > 0) {
        params.states = filters.selectedStates.join(',')
      }
      if (filters.selectedRemoteTypes?.length === 1 && filters.selectedRemoteTypes[0] !== '') {
        params.job_is_remote = filters.selectedRemoteTypes[0] === 'true'
      }
      if (filters.selectedDirectTypes?.length === 1 && filters.selectedDirectTypes[0] !== '') {
        params.is_direct = filters.selectedDirectTypes[0] === 'true'
      }

      const response = await apiClient.get(`${API_BASE_URL}/api/skills/jobs`, { params })
      return response.data
    } catch (error) {
      console.error('Error fetching jobs by skills:', error)
      throw new Error(error.response?.data?.detail || 'Failed to fetch jobs by skills')
    }
  },
}
