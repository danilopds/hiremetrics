import { defineStore } from 'pinia'
import {
  fetchDashboardJobs,
  fetchAvailablePositions,
  fetchFilteredLocations,
} from '@/api/dashboard'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    jobs: [],
    jobMarketTrends: [], // Placeholder for future trend extraction
    skillsDemand: [], // Placeholder for future skill extraction
    locationData: [], // Placeholder for future location extraction
    companyData: [], // Placeholder for future company extraction
    availablePositions: [], // Available positions for filtering
    loading: false,
    error: null,
    selectedView: 'table',
    marketData: [],
    filters: {
      search_position_query: 'Data Engineer',
      job_city: null,
      job_state: null,
      job_is_remote: null,
      dateFrom: null,
      dateTo: null,
      period: 'last30days',
    },
    currentPeriodJobsCount: 0,
    previousPeriodJobsCount: 0,
  }),

  getters: {
    totalJobs: (state) => state.jobs.length,
    // Placeholders for future real data extraction
    averageSalary: () => 0,
    activeCompanies: (state) => {
      const employers = new Set()
      state.jobs.forEach((job) => {
        if (job.employer_name) {
          employers.add(job.employer_name)
        }
      })
      return employers.size
    },
    topSkills: () => [],
  },

  actions: {
    // Initialize with default 30-day period only if no filters exist
    initializeWithDefaults() {
      // Only initialize if we don't have date filters set
      if (!this.filters.dateFrom || !this.filters.dateTo) {
        const end = new Date()
        const start = new Date()
        start.setDate(start.getDate() - 30)

        this.filters.dateFrom = start.toISOString().split('T')[0]
        this.filters.dateTo = end.toISOString().split('T')[0]
        this.filters.period = 'last30days'
      }
    },

    async fetchDashboardData() {
      this.loading = true
      this.error = null
      try {
        const { search_position_query, job_city, job_state, job_is_remote, dateFrom, dateTo } =
          this.filters

        // Use period filters if available, otherwise default to 90 days
        const currentParams = {
          limit: 1000, // Request all records
          search_position_query,
          job_city,
          job_state,
          job_is_remote,
        }

        if (dateFrom && dateTo) {
          currentParams.job_posted_at_date_from = dateFrom
          currentParams.job_posted_at_date_to = dateTo

          // Calculate previous period dates for comparison
          const fromDate = new Date(dateFrom)
          const toDate = new Date(dateTo)
          const daysDiff = Math.ceil((toDate - fromDate) / (1000 * 60 * 60 * 24))

          const prevToDate = new Date(fromDate)
          prevToDate.setDate(prevToDate.getDate() - 1)
          const prevFromDate = new Date(prevToDate)
          prevFromDate.setDate(prevFromDate.getDate() - daysDiff)

          // Previous period params
          const previousParams = {
            limit: 1000, // Request all records
            job_posted_at_date_from: prevFromDate.toISOString().split('T')[0],
            job_posted_at_date_to: prevToDate.toISOString().split('T')[0],
            search_position_query,
            job_city,
            job_state,
            job_is_remote,
          }

          // Fetch jobs for both periods
          const [jobs, prevJobs] = await Promise.all([
            fetchDashboardJobs(currentParams),
            fetchDashboardJobs(previousParams),
          ])

          this.jobs = jobs
          this.currentPeriodJobsCount = jobs.length
          this.previousPeriodJobsCount = prevJobs.length
        } else {
          // Fallback to default 30-day period
          const days = 30
          const today = new Date()
          const toDate = today
          const fromDate = new Date(today)
          fromDate.setDate(fromDate.getDate() - days + 1)

          const formatDate = (d) => d.toISOString().slice(0, 10)

          currentParams.job_posted_at_date_from = formatDate(fromDate)
          currentParams.job_posted_at_date_to = formatDate(toDate)

          const jobs = await fetchDashboardJobs(currentParams)
          this.jobs = jobs
          this.currentPeriodJobsCount = jobs.length
          this.previousPeriodJobsCount = 0
        }

        // Compute jobMarketTrends: group jobs by job_posted_at_date and count
        const trendsMap = {}
        for (const job of this.jobs) {
          const date = job.job_posted_at_date
          if (!date) {
            continue
          }
          if (!trendsMap[date]) {
            trendsMap[date] = 0
          }
          trendsMap[date]++
        }
        this.jobMarketTrends = Object.entries(trendsMap)
          .map(([date, count]) => ({ date, count }))
          .sort((a, b) => new Date(a.date) - new Date(b.date))
        // Extract unique city/state pairs for locationData
        const locMap = {}
        this.jobs.forEach((job) => {
          if (job.job_city && job.job_state) {
            const key = `${job.job_city}|${job.job_state}`
            if (!locMap[key]) {
              locMap[key] = { title: job.job_city, state: job.job_state }
            }
          }
        })
        this.locationData = Object.values(locMap)
        // TODO: Extract skillsDemand, companyData from jobs if needed
        this.marketData = this.jobs.map((job) => ({
          category: job.job_title,
          count: 1,
          change: '',
          trend: '',
        }))
      } catch (error) {
        this.error = error.message
        console.error('Error fetching dashboard data:', error)
      } finally {
        this.loading = false
      }
    },

    setSelectedView(view) {
      this.selectedView = view
    },

    async refreshData() {
      await this.fetchDashboardData()
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
    },

    async fetchAvailablePositions() {
      try {
        const positions = await fetchAvailablePositions()
        this.availablePositions = positions
        return positions
      } catch (error) {
        console.error('Error fetching available positions:', error)
        this.availablePositions = []
        return []
      }
    },

    async fetchFilteredLocations() {
      try {
        const { search_position_query, dateFrom, dateTo } = this.filters
        const locations = await fetchFilteredLocations({
          search_position_query,
          job_posted_at_date_from: dateFrom,
          job_posted_at_date_to: dateTo,
        })
        this.locationData = locations
        return locations
      } catch (error) {
        console.error('Error fetching filtered locations:', error)
        return []
      }
    },
  },
})
