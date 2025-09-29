import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const publishersAPI = {
  // Get publishers KPIs
  getPublishersKpis: (filters = {}) => {
    const params = new URLSearchParams()

    if (filters.dateFrom) {
      params.append('job_posted_at_date_from', filters.dateFrom)
    }
    if (filters.dateTo) {
      params.append('job_posted_at_date_to', filters.dateTo)
    }
    if (filters.publisher) {
      params.append('publisher', filters.publisher)
    }
    if (filters.seniority) {
      params.append('seniority', filters.seniority)
    }
    if (filters.company) {
      params.append('employer_name', filters.company)
    }
    if (filters.remote) {
      params.append('job_is_remote', filters.remote)
    }
    if (filters.search_position_query) {
      params.append('search_position_query', filters.search_position_query)
    }

    const queryString = params.toString()
    const url = `${API_BASE_URL}/api/dashboard/publishers-kpis${queryString ? `?${queryString}` : ''}`

    return axios.get(url)
  },

  // Get top publishers by volume
  getTopPublishers: (filters = {}) => {
    const params = new URLSearchParams()

    if (filters.limit) {
      params.append('limit', filters.limit)
    }
    if (filters.dateFrom) {
      params.append('job_posted_at_date_from', filters.dateFrom)
    }
    if (filters.dateTo) {
      params.append('job_posted_at_date_to', filters.dateTo)
    }
    if (filters.publisher) {
      params.append('publisher', filters.publisher)
    }
    if (filters.seniority) {
      params.append('seniority', filters.seniority)
    }
    if (filters.company) {
      params.append('employer_name', filters.company)
    }
    if (filters.remote) {
      params.append('job_is_remote', filters.remote)
    }
    if (filters.search_position_query) {
      params.append('search_position_query', filters.search_position_query)
    }

    const queryString = params.toString()
    const url = `${API_BASE_URL}/api/dashboard/top-publishers${queryString ? `?${queryString}` : ''}`

    return axios.get(url)
  },

  // Get publishers seniority distribution
  getPublishersSeniorityDistribution: (filters = {}) => {
    const params = new URLSearchParams()

    if (filters.limit) {
      params.append('limit', filters.limit)
    }
    if (filters.dateFrom) {
      params.append('job_posted_at_date_from', filters.dateFrom)
    }
    if (filters.dateTo) {
      params.append('job_posted_at_date_to', filters.dateTo)
    }
    if (filters.publisher) {
      params.append('publisher', filters.publisher)
    }
    if (filters.seniority) {
      params.append('seniority', filters.seniority)
    }
    if (filters.company) {
      params.append('employer_name', filters.company)
    }
    if (filters.remote) {
      params.append('job_is_remote', filters.remote)
    }
    if (filters.search_position_query) {
      params.append('search_position_query', filters.search_position_query)
    }

    const queryString = params.toString()
    const url = `${API_BASE_URL}/api/dashboard/publishers-seniority-distribution${queryString ? `?${queryString}` : ''}`

    return axios.get(url)
  },

  // Get publishers companies matrix
  getPublishersCompaniesMatrix: (filters = {}) => {
    const params = new URLSearchParams()

    if (filters.limitPublishers) {
      params.append('limit_publishers', filters.limitPublishers)
    }
    if (filters.limitCompanies) {
      params.append('limit_companies', filters.limitCompanies)
    }
    if (filters.dateFrom) {
      params.append('job_posted_at_date_from', filters.dateFrom)
    }
    if (filters.dateTo) {
      params.append('job_posted_at_date_to', filters.dateTo)
    }
    if (filters.publisher) {
      params.append('publisher', filters.publisher)
    }
    if (filters.seniority) {
      params.append('seniority', filters.seniority)
    }
    if (filters.company) {
      params.append('employer_name', filters.company)
    }
    if (filters.remote) {
      params.append('job_is_remote', filters.remote)
    }
    if (filters.search_position_query) {
      params.append('search_position_query', filters.search_position_query)
    }

    const queryString = params.toString()
    const url = `${API_BASE_URL}/api/dashboard/publishers-companies-matrix${queryString ? `?${queryString}` : ''}`

    return axios.get(url)
  },

  // Get publishers timeline
  getPublishersTimeline: (filters = {}) => {
    const params = new URLSearchParams()

    if (filters.limit) {
      params.append('limit', filters.limit)
    }
    if (filters.dateFrom) {
      params.append('job_posted_at_date_from', filters.dateFrom)
    }
    if (filters.dateTo) {
      params.append('job_posted_at_date_to', filters.dateTo)
    }
    if (filters.publisher) {
      params.append('publisher', filters.publisher)
    }
    if (filters.seniority) {
      params.append('seniority', filters.seniority)
    }
    if (filters.company) {
      params.append('employer_name', filters.company)
    }
    if (filters.remote) {
      params.append('job_is_remote', filters.remote)
    }
    if (filters.search_position_query) {
      params.append('search_position_query', filters.search_position_query)
    }

    const queryString = params.toString()
    const url = `${API_BASE_URL}/api/dashboard/publishers-timeline${queryString ? `?${queryString}` : ''}`

    return axios.get(url)
  },

  // Get direct vs indirect distribution
  getDirectVsIndirectDistribution: (filters = {}) => {
    const params = new URLSearchParams()

    if (filters.dateFrom) {
      params.append('job_posted_at_date_from', filters.dateFrom)
    }
    if (filters.dateTo) {
      params.append('job_posted_at_date_to', filters.dateTo)
    }
    if (filters.publisher) {
      params.append('publisher', filters.publisher)
    }
    if (filters.seniority) {
      params.append('seniority', filters.seniority)
    }
    if (filters.company) {
      params.append('employer_name', filters.company)
    }
    if (filters.remote) {
      params.append('job_is_remote', filters.remote)
    }
    if (filters.search_position_query) {
      params.append('search_position_query', filters.search_position_query)
    }

    const queryString = params.toString()
    const url = `${API_BASE_URL}/api/dashboard/direct-vs-indirect-distribution${queryString ? `?${queryString}` : ''}`

    return axios.get(url)
  },

  // Get available publishers (for filter options)
  getAvailablePublishers: (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.search_position_query) {
      params.append('search_position_query', filters.search_position_query)
    }

    const queryString = params.toString()
    const url = `${API_BASE_URL}/api/dashboard/available-publishers${queryString ? `?${queryString}` : ''}`

    return axios.get(url)
  },

  // Get available seniority levels (for filter options)
  getAvailableSeniorityLevels: (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.search_position_query) {
      params.append('search_position_query', filters.search_position_query)
    }

    const queryString = params.toString()
    const url = `${API_BASE_URL}/api/dashboard/available-seniority-levels${queryString ? `?${queryString}` : ''}`

    return axios.get(url)
  },

  // Get available companies (for filter options)
  getAvailableCompanies: (filters = {}) => {
    const params = new URLSearchParams()
    if (filters.search_position_query) {
      params.append('search_position_query', filters.search_position_query)
    }

    const queryString = params.toString()
    const url = `${API_BASE_URL}/api/dashboard/available-companies${queryString ? `?${queryString}` : ''}`

    return axios.get(url)
  },

  // Get available positions (for filter options)
  getAvailablePositions: () => {
    return axios.get(`${API_BASE_URL}/api/dashboard/available-positions`)
  },
}
