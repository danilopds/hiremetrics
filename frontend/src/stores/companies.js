import { defineStore } from 'pinia'
import {
  fetchTopCompanies,
  fetchCompaniesSeniorityDistribution,
  fetchEmploymentTypeDistribution,
  fetchCompaniesRemotePercentage,
  fetchCompaniesJobsTimeline,
  fetchCompaniesTopSkills,
  fetchCompaniesKpis,
  fetchAvailableCompanies as fetchAvailableCompaniesAPI,
  fetchAvailableSeniorityLevels as fetchAvailableSeniorityLevelsAPI,
  fetchAvailablePositions,
} from '@/api/companies'

export const useCompaniesStore = defineStore('companies', {
  state: () => ({
    topCompanies: [],
    seniorityDistribution: [],
    employmentTypeDistribution: [],
    remotePercentage: [],
    jobsTimeline: [],
    topSkills: [],
    kpis: {
      total_jobs: 0,
      remote_percentage: 0,
      avg_skills_per_job: 0,
      distinct_companies: 0,
    },
    availableCompanies: [],
    availableSeniorityLevels: [],
    availablePositions: [],
    filters: {
      search_position_query: 'Data Engineer',
      employer_name: null,
      job_is_remote: null,
      seniority: null,
      dateFrom: null,
      dateTo: null,
      period: 'last30days',
    },
    loading: false,
    error: null,
  }),
  actions: {
    async fetchTopCompanies() {
      this.loading = true
      try {
        const params = this._buildParams(20)
        this.topCompanies = await fetchTopCompanies(params)
      } catch (err) {
        this.error = 'Failed to fetch top companies'
        console.error('Error fetching top companies:', err)
      } finally {
        this.loading = false
      }
    },
    async fetchSeniorityDistribution() {
      this.loading = true
      try {
        const params = this._buildParams(10)
        const data = await fetchCompaniesSeniorityDistribution(params)
        this.seniorityDistribution = data
      } catch (err) {
        this.error = 'Failed to fetch seniority distribution'
        console.error('Error fetching seniority distribution:', err)
      } finally {
        this.loading = false
      }
    },
    async fetchEmploymentTypeDistribution() {
      this.loading = true
      try {
        const params = this._buildParams()
        this.employmentTypeDistribution = await fetchEmploymentTypeDistribution(params)
      } catch (err) {
        this.error = 'Failed to fetch employment type distribution'
        console.error('Error fetching employment type distribution:', err)
      } finally {
        this.loading = false
      }
    },
    async fetchRemotePercentage() {
      this.loading = true
      try {
        const params = this._buildParams(20)
        const data = await fetchCompaniesRemotePercentage(params)
        this.remotePercentage = data
      } catch (err) {
        this.error = 'Failed to fetch remote percentage'
        console.error('Error fetching remote percentage:', err)
      } finally {
        this.loading = false
      }
    },
    async fetchJobsTimeline() {
      this.loading = true
      try {
        const params = this._buildParams(5)
        this.jobsTimeline = await fetchCompaniesJobsTimeline(params)
      } catch (err) {
        this.error = 'Failed to fetch jobs timeline'
        console.error('Error fetching jobs timeline:', err)
      } finally {
        this.loading = false
      }
    },
    async fetchTopSkills() {
      this.loading = true
      try {
        const params = this._buildParams(10)
        params.skills_limit = 50
        const response = await fetchCompaniesTopSkills(params)

        // Check for duplicates in API response
        if (Array.isArray(response)) {
          const nameCounts = {}
          response.forEach((item) => {
            const name = item.name || item.skill || ''
            if (name) {
              if (!nameCounts[name]) {
                nameCounts[name] = 0
              }
              nameCounts[name]++
            }
          })
        }

        this.topSkills = response
      } catch (err) {
        this.error = 'Failed to fetch top skills'
        console.error('Error fetching top skills:', err)
      } finally {
        this.loading = false
      }
    },
    async fetchKpis() {
      this.loading = true
      try {
        const params = this._buildParams()
        this.kpis = await fetchCompaniesKpis(params)
      } catch (err) {
        this.error = 'Failed to fetch KPIs'
        console.error('Error fetching KPIs:', err)
      } finally {
        this.loading = false
      }
    },
    async fetchAvailableCompanies() {
      try {
        this.availableCompanies = await fetchAvailableCompaniesAPI(
          this.filters.search_position_query
        )
      } catch (err) {
        console.error('Error fetching available companies:', err)
      }
    },
    async fetchAvailableSeniorityLevels() {
      try {
        this.availableSeniorityLevels = await fetchAvailableSeniorityLevelsAPI(
          this.filters.search_position_query
        )
      } catch (err) {
        console.error('Error fetching available seniority levels:', err)
      }
    },
    async fetchAvailablePositions() {
      try {
        this.availablePositions = await fetchAvailablePositions()
        return this.availablePositions
      } catch (error) {
        console.error('Error fetching available positions:', error)
        this.availablePositions = []
        return []
      }
    },
    _buildParams(limit) {
      const params = {}
      if (limit) {
        params.limit = limit
      }

      // Add position filter
      if (this.filters.search_position_query) {
        params.search_position_query = this.filters.search_position_query
      }

      // Use period filters if available, otherwise default to 90 days
      if (this.filters.dateFrom && this.filters.dateTo) {
        // Ensure date format is YYYY-MM-DD
        const dateFromObj = new Date(this.filters.dateFrom)
        const dateToObj = new Date(this.filters.dateTo)

        // Format dates in YYYY-MM-DD format
        params.job_posted_at_date_from = dateFromObj.toISOString().split('T')[0]
        params.job_posted_at_date_to = dateToObj.toISOString().split('T')[0]
      } else {
        const endDate = new Date()
        const startDate = new Date()
        startDate.setDate(endDate.getDate() - 30)

        params.job_posted_at_date_from = startDate.toISOString().split('T')[0]
        params.job_posted_at_date_to = endDate.toISOString().split('T')[0]
      }

      if (this.filters.employer_name && this.filters.employer_name !== 'all') {
        params.employer_name = this.filters.employer_name
      }
      if (this.filters.job_is_remote && this.filters.job_is_remote !== 'all') {
        params.job_is_remote = this.filters.job_is_remote
      }
      if (this.filters.seniority && this.filters.seniority !== 'all') {
        params.seniority = this.filters.seniority
      }

      return params
    },
    async refreshAll() {
      this.error = null
      await Promise.all([
        this.fetchKpis(),
        this.fetchTopCompanies(),
        this.fetchSeniorityDistribution(),
        this.fetchEmploymentTypeDistribution(),
        this.fetchRemotePercentage(),
        this.fetchJobsTimeline(),
        this.fetchTopSkills(),
      ])
    },
    async initializeFilters() {
      await Promise.all([
        this.fetchAvailableCompanies(),
        this.fetchAvailableSeniorityLevels(),
        this.fetchAvailablePositions(),
      ])
    },
    setFilters(newFilters) {
      this.filters = { ...this.filters, ...newFilters }
    },
  },
})
