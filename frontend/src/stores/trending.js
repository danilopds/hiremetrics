import { defineStore } from 'pinia'
import {
  fetchTopSkills,
  fetchWordCloudSkills,
  fetchSkillsTrend,
  fetchAvailableSkills,
  fetchAvailableSeniorityLevels,
  fetchAvailablePositions,
} from '@/api/trending'

export const useTrendingStore = defineStore('trending', {
  state: () => ({
    skills: [],
    seniorityLevels: [],
    availablePositions: [],
    topSkills: [],
    skillsTrend: [],
    wordCloudSkills: [],
    prevPeriodSkills: [],
    kpiMostDemanded: null,
    kpiHighestGrowth: null,
    kpiBiggestDrop: null,
    filters: {
      search_position_query: 'Data Engineer',
      selectedSkills: [],
      selectedSeniority: null,
      dateFrom: null,
      dateTo: null,
      period: 'last30days',
    },
    loading: false,
    error: null,
  }),
  actions: {
    async fetchAvailableSkills(token) {
      try {
        this.skills = await fetchAvailableSkills(token, this.filters.search_position_query)
      } catch (err) {
        this.error = 'Failed to fetch available skills'
      }
    },
    async fetchAvailableSeniorityLevels(token) {
      try {
        this.seniorityLevels = await fetchAvailableSeniorityLevels(
          token,
          this.filters.search_position_query
        )
      } catch (err) {
        this.error = 'Failed to fetch available seniority levels'
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
    async fetchTopSkills() {
      this.loading = true
      try {
        const params = this._buildParams(50) // Increased from 10 to 50 to ensure we get enough skills for top 10
        this.topSkills = await fetchTopSkills(params)
      } catch (err) {
        this.error = 'Failed to fetch top skills data'
      } finally {
        this.loading = false
      }
    },
    async fetchSkillsTrend() {
      this.loading = true
      try {
        const params = this._buildParams(this.filters.selectedSkills?.length || 50) // Increased from 5 to 50 to get more skills for chart
        if (this.filters.selectedSkills?.length > 0) {
          params.skills = this.filters.selectedSkills
        }
        this.skillsTrend = await fetchSkillsTrend(params)
      } catch (err) {
        this.error = 'Failed to fetch skills trend data'
      } finally {
        this.loading = false
      }
    },
    async fetchWordCloudSkills() {
      this.loading = true
      try {
        const params = this._buildParams(100)
        const response = await fetchWordCloudSkills(params)
        if (!Array.isArray(response)) {
          throw new Error('Invalid response format for word cloud skills')
        }
        this.wordCloudSkills = response
      } catch (err) {
        this.error = 'Failed to fetch skills for word cloud'
        this.wordCloudSkills = []
      } finally {
        this.loading = false
      }
    },
    async fetchPrevPeriodSkills() {
      try {
        const params = this._buildPrevPeriodParams(1000)
        this.prevPeriodSkills = await fetchTopSkills(params)
      } catch (err) {
        this.error = 'Failed to fetch previous period skills'
      }
    },
    _buildParams(limit = 10) {
      const params = { limit }

      // Add position filter
      if (this.filters.search_position_query) {
        params.search_position_query = this.filters.search_position_query
      }

      // Use period filters if available, otherwise default to 90 days
      if (this.filters.dateFrom && this.filters.dateTo) {
        params.job_posted_at_date_from = this.filters.dateFrom
        params.job_posted_at_date_to = this.filters.dateTo
      } else {
        const endDate = new Date()
        const startDate = new Date()
        startDate.setDate(endDate.getDate() - 30)

        params.job_posted_at_date_from = startDate.toISOString().split('T')[0]
        params.job_posted_at_date_to = endDate.toISOString().split('T')[0]
      }

      if (this.filters.selectedSeniority && this.filters.selectedSeniority !== 'Todos') {
        params.seniority = this.filters.selectedSeniority
      }

      return params
    },
    _buildPrevPeriodParams(limit = 1000) {
      const params = { limit }

      // Add position filter
      if (this.filters.search_position_query) {
        params.search_position_query = this.filters.search_position_query
      }

      // Calculate previous period based on current period
      if (this.filters.dateFrom && this.filters.dateTo) {
        const fromDate = new Date(this.filters.dateFrom)
        const toDate = new Date(this.filters.dateTo)
        const daysDiff = Math.ceil((toDate - fromDate) / (1000 * 60 * 60 * 24))

        const prevToDate = new Date(fromDate)
        prevToDate.setDate(prevToDate.getDate() - 1)
        const prevFromDate = new Date(prevToDate)
        prevFromDate.setDate(prevFromDate.getDate() - daysDiff)

        params.job_posted_at_date_from = prevFromDate.toISOString().split('T')[0]
        params.job_posted_at_date_to = prevToDate.toISOString().split('T')[0]
      } else {
        // Use fixed 30-day period for previous period (30-60 days ago)
        const endDate = new Date()
        const days = 30

        const prevToDate = new Date(endDate)
        prevToDate.setDate(endDate.getDate() - days)
        const prevFromDate = new Date(endDate)
        prevFromDate.setDate(endDate.getDate() - 2 * days + 1)

        params.job_posted_at_date_from = prevFromDate.toISOString().split('T')[0]
        params.job_posted_at_date_to = prevToDate.toISOString().split('T')[0]
      }

      if (this.filters.selectedSeniority && this.filters.selectedSeniority !== 'Todos') {
        params.seniority = this.filters.selectedSeniority
      }
      return params
    },
    computeKPIs() {
      // Always use consistent aggregation logic regardless of filter state
      const aggregate = (arr) => {
        const map = {}
        arr.forEach((item) => {
          if (!map[item.skill]) {
            map[item.skill] = 0
          }
          map[item.skill] += item.skill_count
        })
        return Object.entries(map).map(([skill, skill_count]) => ({ skill, skill_count }))
      }

      // Use skillsTrend (time-series data) for current skills to match radar chart
      // Filter skills trend by seniority if applicable
      const filteredCurrentSkills =
        this.filters.selectedSeniority && this.filters.selectedSeniority !== 'Todos'
          ? this.skillsTrend.filter((item) => item.seniority === this.filters.selectedSeniority)
          : this.skillsTrend

      // For previous period, handle both data formats from top-skills endpoint
      let filteredPrevSkills
      if (this.filters.selectedSeniority && this.filters.selectedSeniority !== 'Todos') {
        // When seniority filter is applied, top-skills returns { skill, skill_count }
        // No need to filter further as API already filtered by seniority
        filteredPrevSkills = this.prevPeriodSkills
      } else {
        // When no seniority filter, top-skills returns { skill, seniority, skill_count, total_count }
        // Filter by seniority if needed, or aggregate across all seniority levels
        filteredPrevSkills = this.prevPeriodSkills
      }

      // Aggregate the time-series data by skill (current period)
      const currentSkills = aggregate(filteredCurrentSkills)

      // Handle previous period data format - may already be aggregated or need aggregation
      const prevSkills =
        filteredPrevSkills.length > 0 && Object.prototype.hasOwnProperty.call(filteredPrevSkills[0], 'seniority')
          ? aggregate(filteredPrevSkills) // Time-series format, needs aggregation
          : filteredPrevSkills // Already aggregated format from top-skills with seniority filter

      if (currentSkills.length > 0) {
        this.kpiMostDemanded = currentSkills.reduce((a, b) =>
          a.skill_count > b.skill_count ? a : b
        )
      } else {
        this.kpiMostDemanded = null
      }

      // Calculate growth and decline KPIs even when there's no previous period data
      if (currentSkills.length > 0) {
        const prevMap = {}
        prevSkills.forEach((item) => {
          prevMap[item.skill] = item.skill_count
        })
        const changes = currentSkills.map((item) => {
          const prev = prevMap[item.skill] || 0
          let change
          if (prev === 0) {
            // New skill - set to 100% growth
            change = 100
          } else {
            // Existing skill - calculate percentage change
            change = ((item.skill_count - prev) / prev) * 100
          }

          return {
            skill: item.skill,
            current: item.skill_count,
            prev,
            change,
          }
        })

        // Find highest growth (all skills now have percentage values)
        const growthCandidates = changes.filter((c) => c.change > 0)

        let bestPerformer = null
        if (growthCandidates.length > 0) {
          // Show highest growth
          bestPerformer = growthCandidates.reduce((a, b) => (a.change > b.change ? a : b))
        } else if (changes.length > 0) {
          // No growth exists, but show the least declining skill with special marking
          bestPerformer = changes.reduce((a, b) => (a.change > b.change ? a : b))
          bestPerformer.isLeastDeclining = true // Special flag to indicate this is "least bad" not actual growth
        }

        this.kpiHighestGrowth = bestPerformer

        // Find biggest drop (only skills that existed before and declined)
        const declineCandidates = changes.filter((c) => c.prev > 0 && c.change < 0)
        this.kpiBiggestDrop =
          declineCandidates.length > 0
            ? declineCandidates.reduce((a, b) => (a.change < b.change ? a : b))
            : null
      } else {
        this.kpiHighestGrowth = null
        this.kpiBiggestDrop = null
      }
    },
    async refreshAll(token) {
      await this.fetchAvailableSkills(token)
      await this.fetchAvailableSeniorityLevels(token)
      await this.fetchAvailablePositions()
      await this.fetchTopSkills()
      await this.fetchSkillsTrend()
      await this.fetchWordCloudSkills()
      await this.fetchPrevPeriodSkills()
      this.computeKPIs()
    },
    setFilters(newFilters) {
      this.filters = { ...this.filters, ...newFilters }
    },
  },
})
