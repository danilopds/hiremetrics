import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function fetchDashboardJobs({
  limit = 1000,
  offset = 0,
  job_posted_at_date,
  job_posted_at_date_from,
  job_posted_at_date_to,
  job_city,
  job_state,
  job_is_remote,
  search_position_query,
} = {}) {
  const params = { limit, offset }
  if (job_posted_at_date) {
    params.job_posted_at_date = job_posted_at_date
  }
  if (job_posted_at_date_from) {
    params.job_posted_at_date_from = job_posted_at_date_from
  }
  if (job_posted_at_date_to) {
    params.job_posted_at_date_to = job_posted_at_date_to
  }
  if (job_city) {
    params.job_city = job_city
  }
  if (job_state) {
    params.job_state = job_state
  }
  if (job_is_remote !== undefined && job_is_remote !== null) {
    params.job_is_remote = String(job_is_remote)
  }
  if (search_position_query) {
    params.search_position_query = search_position_query
  }
  const response = await axios.get(`${API_BASE_URL}/api/dashboard/jobs`, { params })
  return response.data
}

export const fetchJobLocationsGeo = async ({
  job_posted_at_date_from,
  job_posted_at_date_to,
  employer_name,
  job_is_remote,
  seniority,
  job_city,
  job_state,
  search_position_query,
}) => {
  try {
    const params = {}
    if (job_posted_at_date_from) {
      params.job_posted_at_date_from = job_posted_at_date_from
    }
    if (job_posted_at_date_to) {
      params.job_posted_at_date_to = job_posted_at_date_to
    }
    if (employer_name) {
      params.employer_name = employer_name
    }
    if (job_is_remote !== undefined && job_is_remote !== null) {
      params.job_is_remote = String(job_is_remote)
    }
    if (seniority) {
      params.seniority = seniority
    }
    if (job_city) {
      params.job_city = job_city
    }
    if (job_state) {
      params.job_state = job_state
    }
    if (search_position_query) {
      params.search_position_query = search_position_query
    }

    const response = await axios.get(`${API_BASE_URL}/api/dashboard/job-locations-geo`, { params })
    return response.data
  } catch (error) {
    console.error('Error fetching job locations geo data:', error)
    throw error
  }
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

export async function fetchFilteredLocations({
  search_position_query,
  job_posted_at_date_from,
  job_posted_at_date_to,
} = {}) {
  try {
    const params = {}
    if (search_position_query) {
      params.search_position_query = search_position_query
    }
    if (job_posted_at_date_from) {
      params.job_posted_at_date_from = job_posted_at_date_from
    }
    if (job_posted_at_date_to) {
      params.job_posted_at_date_to = job_posted_at_date_to
    }

    const response = await axios.get(`${API_BASE_URL}/api/dashboard/locations`, { params })
    return response.data
  } catch (error) {
    console.error('Error fetching filtered locations:', error)
    throw error
  }
}
