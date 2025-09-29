import { defineStore } from 'pinia'
import { publishersAPI } from '@/api/publishers'

export const usePublishersStore = defineStore('publishers', {
  state: () => ({
    // KPIs data
    kpis: {
      totalPublishers: 0,
      avgPublishersPerJob: 0,
      biggestCoveragePublisher: null,
      biggestCoverageCount: 0,
      directPercentage: 0,
    },

    // Charts data
    topPublishers: [],
    seniorityDistribution: [],
    companiesMatrix: [],
    timeline: [],
    directVsIndirect: [],

    // Available filter options
    availablePublishers: [],
    availableSeniorityLevels: [],
    availableCompanies: [],
    availablePositions: [],

    // Loading states
    loading: {
      kpis: false,
      topPublishers: false,
      seniorityDistribution: false,
      companiesMatrix: false,
      timeline: false,
      directVsIndirect: false,
      availableOptions: false,
    },

    // Error states
    errors: {
      kpis: null,
      topPublishers: null,
      seniorityDistribution: null,
      companiesMatrix: null,
      timeline: null,
      directVsIndirect: null,
      availableOptions: null,
    },

    // Current filters
    filters: {
      dateFrom: null,
      dateTo: null,
      publisher: null,
      seniority: null,
      company: null,
      remote: null,
      search_position_query: 'Data Engineer',
      limit: 20,
      limitPublishers: 15,
      limitCompanies: 15,
      period: 'last30days',
    },
  }),

  getters: {
    // Transform seniority distribution for stacked bar chart
    seniorityChartData() {
      if (!this.seniorityDistribution.length) {
        return { publishers: [], seniorities: [], data: [] }
      }

      const publishers = [...new Set(this.seniorityDistribution.map((item) => item.publisher))]
      const seniorities = [...new Set(this.seniorityDistribution.map((item) => item.seniority))]

      const data = publishers.map((publisher) => {
        const publisherData = { publisher }
        seniorities.forEach((seniority) => {
          const item = this.seniorityDistribution.find(
            (d) => d.publisher === publisher && d.seniority === seniority
          )
          publisherData[seniority] = item ? item.job_count : 0
        })
        return publisherData
      })

      return { publishers, seniorities, data }
    },

    // Transform companies matrix for heatmap
    companiesMatrixData() {
      if (!this.companiesMatrix.length) {
        return { publishers: [], companies: [], data: [] }
      }

      const publishers = [...new Set(this.companiesMatrix.map((item) => item.publisher))]
      const companies = [...new Set(this.companiesMatrix.map((item) => item.employer_name))]

      const data = []
      publishers.forEach((publisher, pubIndex) => {
        companies.forEach((company, compIndex) => {
          const item = this.companiesMatrix.find(
            (d) => d.publisher === publisher && d.employer_name === company
          )
          data.push([pubIndex, compIndex, item ? item.job_count : 0])
        })
      })

      return { publishers, companies, data }
    },

    // Transform timeline data for line chart
    timelineChartData() {
      if (!this.timeline.length) {
        return { dates: [], series: [] }
      }

      const dates = [...new Set(this.timeline.map((item) => item.job_posted_at_date))].sort()
      const publishers = [...new Set(this.timeline.map((item) => item.publisher))]

      // Initialize publisher-date map for cumulative calculation
      const publisherDateMap = {}
      publishers.forEach((publisher) => {
        publisherDateMap[publisher] = {}
        dates.forEach((date) => {
          publisherDateMap[publisher][date] = 0
        })
      })

      // Populate the map with actual values
      this.timeline.forEach((item) => {
        if (
          publisherDateMap[item.publisher] &&
          publisherDateMap[item.publisher][item.job_posted_at_date] !== undefined
        ) {
          publisherDateMap[item.publisher][item.job_posted_at_date] = item.job_count
        }
      })

      // Calculate cumulative series
      const series = publishers.map((publisher) => {
        let cumulative = 0
        const data = dates.map((date) => {
          cumulative += publisherDateMap[publisher][date] || 0
          return cumulative
        })

        return {
          name: publisher,
          type: 'line',
          data: data,
          smooth: true,
        }
      })

      return { dates, series }
    },
  },

  actions: {
    // Set filters
    setFilters(newFilters) {
      // Ensure period is preserved properly
      if (newFilters.dateFrom && newFilters.dateTo && !newFilters.period) {
        // Try to match with preset periods if only dates are provided
        const end = new Date()
        const start = new Date()

        // Check for last30days (removed last90days check)
        start.setDate(start.getDate() - 30)
        if (
          newFilters.dateFrom === start.toISOString().split('T')[0] &&
          newFilters.dateTo === end.toISOString().split('T')[0]
        ) {
          newFilters.period = 'last30days'
        }

        // Check for last30days
        start.setDate(end.getDate() - 30)
        if (
          newFilters.dateFrom === start.toISOString().split('T')[0] &&
          newFilters.dateTo === end.toISOString().split('T')[0]
        ) {
          newFilters.period = 'last30days'
        }

        // Check for last7days
        start.setDate(end.getDate() - 7)
        if (
          newFilters.dateFrom === start.toISOString().split('T')[0] &&
          newFilters.dateTo === end.toISOString().split('T')[0]
        ) {
          newFilters.period = 'last7days'
        }

        // If no match, set as custom
        if (!newFilters.period) {
          newFilters.period = 'custom'
        }
      }

      this.filters = { ...this.filters, ...newFilters }
    },

    // Clear all errors
    clearErrors() {
      Object.keys(this.errors).forEach((key) => {
        this.errors[key] = null
      })
    },

    // Fetch KPIs
    async fetchKpis() {
      this.loading.kpis = true
      this.errors.kpis = null

      try {
        const response = await publishersAPI.getPublishersKpis({
          dateFrom: this.filters.dateFrom,
          dateTo: this.filters.dateTo,
          publisher: this.filters.publisher,
          seniority: this.filters.seniority,
          company: this.filters.company,
          remote: this.filters.remote,
          search_position_query: this.filters.search_position_query,
        })

        const data = response.data
        this.kpis = {
          totalPublishers: data.total_publishers,
          avgPublishersPerJob: data.avg_publishers_per_job,
          biggestCoveragePublisher: data.biggest_coverage_publisher,
          biggestCoverageCount: data.biggest_coverage_count,
          directPercentage: data.direct_percentage,
        }
      } catch (error) {
        this.errors.kpis = error.response?.data?.detail || 'Failed to fetch publishers KPIs'
        console.error('Error fetching publishers KPIs:', error)
      } finally {
        this.loading.kpis = false
      }
    },

    // Fetch top publishers
    async fetchTopPublishers() {
      this.loading.topPublishers = true
      this.errors.topPublishers = null

      try {
        const response = await publishersAPI.getTopPublishers({
          limit: this.filters.limit,
          dateFrom: this.filters.dateFrom,
          dateTo: this.filters.dateTo,
          publisher: this.filters.publisher,
          seniority: this.filters.seniority,
          company: this.filters.company,
          remote: this.filters.remote,
          search_position_query: this.filters.search_position_query,
        })

        this.topPublishers = response.data
      } catch (error) {
        this.errors.topPublishers = error.response?.data?.detail || 'Failed to fetch top publishers'
        console.error('Error fetching top publishers:', error)
      } finally {
        this.loading.topPublishers = false
      }
    },

    // Fetch seniority distribution
    async fetchSeniorityDistribution() {
      this.loading.seniorityDistribution = true
      this.errors.seniorityDistribution = null

      try {
        const response = await publishersAPI.getPublishersSeniorityDistribution({
          limit: this.filters.limit,
          dateFrom: this.filters.dateFrom,
          dateTo: this.filters.dateTo,
          publisher: this.filters.publisher,
          seniority: this.filters.seniority,
          company: this.filters.company,
          remote: this.filters.remote,
          search_position_query: this.filters.search_position_query,
        })

        this.seniorityDistribution = response.data
      } catch (error) {
        this.errors.seniorityDistribution =
          error.response?.data?.detail || 'Failed to fetch seniority distribution'
        console.error('Error fetching seniority distribution:', error)
      } finally {
        this.loading.seniorityDistribution = false
      }
    },

    // Fetch companies matrix
    async fetchCompaniesMatrix() {
      this.loading.companiesMatrix = true
      this.errors.companiesMatrix = null

      try {
        const response = await publishersAPI.getPublishersCompaniesMatrix({
          limitPublishers: this.filters.limitPublishers,
          limitCompanies: this.filters.limitCompanies,
          dateFrom: this.filters.dateFrom,
          dateTo: this.filters.dateTo,
          publisher: this.filters.publisher,
          seniority: this.filters.seniority,
          company: this.filters.company,
          remote: this.filters.remote,
          search_position_query: this.filters.search_position_query,
        })

        this.companiesMatrix = response.data
      } catch (error) {
        this.errors.companiesMatrix =
          error.response?.data?.detail || 'Failed to fetch companies matrix'
        console.error('Error fetching companies matrix:', error)
      } finally {
        this.loading.companiesMatrix = false
      }
    },

    // Fetch timeline
    async fetchTimeline() {
      this.loading.timeline = true
      this.errors.timeline = null

      try {
        const response = await publishersAPI.getPublishersTimeline({
          limit: this.filters.limit,
          dateFrom: this.filters.dateFrom,
          dateTo: this.filters.dateTo,
          publisher: this.filters.publisher,
          seniority: this.filters.seniority,
          company: this.filters.company,
          remote: this.filters.remote,
          search_position_query: this.filters.search_position_query,
        })

        this.timeline = response.data
      } catch (error) {
        this.errors.timeline = error.response?.data?.detail || 'Failed to fetch timeline'
        console.error('Error fetching timeline:', error)
      } finally {
        this.loading.timeline = false
      }
    },

    // Fetch direct vs indirect distribution
    async fetchDirectVsIndirect() {
      this.loading.directVsIndirect = true
      this.errors.directVsIndirect = null

      try {
        const response = await publishersAPI.getDirectVsIndirectDistribution({
          dateFrom: this.filters.dateFrom,
          dateTo: this.filters.dateTo,
          publisher: this.filters.publisher,
          seniority: this.filters.seniority,
          company: this.filters.company,
          remote: this.filters.remote,
          search_position_query: this.filters.search_position_query,
        })

        this.directVsIndirect = response.data
      } catch (error) {
        this.errors.directVsIndirect =
          error.response?.data?.detail || 'Failed to fetch direct vs indirect distribution'
        console.error('Error fetching direct vs indirect distribution:', error)
      } finally {
        this.loading.directVsIndirect = false
      }
    },

    // Fetch available options for filters
    async fetchAvailableOptions() {
      this.loading.availableOptions = true
      this.errors.availableOptions = null

      try {
        const [publishersResponse, seniorityResponse, companiesResponse, positionsResponse] =
          await Promise.all([
            publishersAPI.getAvailablePublishers({
              search_position_query: this.filters.search_position_query,
            }),
            publishersAPI.getAvailableSeniorityLevels({
              search_position_query: this.filters.search_position_query,
            }),
            publishersAPI.getAvailableCompanies({
              search_position_query: this.filters.search_position_query,
            }),
            publishersAPI.getAvailablePositions(),
          ])

        this.availablePublishers = publishersResponse.data
        this.availableSeniorityLevels = seniorityResponse.data
        this.availableCompanies = companiesResponse.data
        this.availablePositions = positionsResponse.data
      } catch (error) {
        this.errors.availableOptions =
          error.response?.data?.detail || 'Failed to fetch available options'
        console.error('Error fetching available options:', error)
      } finally {
        this.loading.availableOptions = false
      }
    },

    // Fetch available positions
    async fetchAvailablePositions() {
      try {
        const response = await publishersAPI.getAvailablePositions()
        this.availablePositions = response.data
        return response.data
      } catch (error) {
        console.error('Error fetching available positions:', error)
        return []
      }
    },

    // Fetch all data with parallel requests
    async fetchAllData() {
      await this.fetchAvailableOptions()
      await Promise.all([
        this.fetchKpis(),
        this.fetchTopPublishers(),
        this.fetchSeniorityDistribution(),
        this.fetchCompaniesMatrix(),
        this.fetchTimeline(),
        this.fetchDirectVsIndirect(),
      ])
    },

    // Initialize with default 30-day filter only if no filters exist
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
  },
})
