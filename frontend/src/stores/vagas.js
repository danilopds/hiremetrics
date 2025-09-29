import { defineStore } from 'pinia'
import { reportsApi } from '@/api/reports'
import { fetchFilteredLocations } from '@/api/dashboard'

export const useVagasStore = defineStore('vagas', {
  state: () => ({
    jobs: [],
    loading: false,
    error: null,
    selectedJob: null,
    availablePositions: [],
    availableEmploymentTypes: [],
    availableSeniorities: [],
    locationData: [], // Available locations for filtering
    filters: {
      search_position_query: '', // Start with no position filter
      employment_type: '', // Employment type filter
      job_is_remote: null, // Start with no remote filter (show all)
      seniority: '', // Seniority filter
      job_city: null, // City filter
      dateFrom: null,
      dateTo: null,
      period: 'last30days',
    },
  }),

  getters: {
    totalJobs: (state) => state.jobs.length,
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

      // Load saved filters from localStorage if available
      this.loadPersistedFilters()

      // Load saved selected job from localStorage if available
      // This preserves the user's selection when navigating between tabs
      this.loadPersistedSelectedJob()
    },

    async fetchVagasData() {
      this.loading = true
      this.error = null
      try {
        const {
          search_position_query,
          employment_type,
          job_is_remote,
          seniority,
          job_city,
          dateFrom,
          dateTo,
        } = this.filters

        // Build filters object for reports API
        const filters = {
          dateFrom: dateFrom,
          dateTo: dateTo,
          selectedPosition: search_position_query || '',
          selectedCompanies: [],
          selectedPublishers: [],
          selectedSeniority: seniority ? [seniority] : [],
          selectedEmploymentTypes: employment_type ? [employment_type] : [],
          selectedCities: job_city && job_city !== 'N/A' ? [job_city] : [],
          selectedStates: [],
          selectedSkills: [],
          selectedRemoteTypes:
            job_is_remote !== null && job_is_remote !== undefined && job_is_remote !== 'null'
              ? [job_is_remote === 'true' ? 'true' : 'false']
              : [],
          selectedDirectTypes: [],
        }

        console.log('Fetching vagas with filters:', filters)
        const jobs = await reportsApi.previewExport(filters, 50) // Max limit is 50
        console.log('Received jobs:', jobs.length)
        this.jobs = jobs || []
      } catch (error) {
        console.error('Error fetching vagas data:', error)
        this.error = error.message || 'Erro ao carregar vagas'
        this.jobs = []
      } finally {
        this.loading = false
      }
    },

    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      // Persist filters to localStorage
      this.persistFilters()
    },

    setPeriod(periodFilters) {
      // Handle both legacy period string and new period filters object
      if (typeof periodFilters === 'string') {
        // Legacy format - just period string
        this.filters.period = periodFilters
        this.updateDateFiltersFromPeriod(periodFilters)
      } else {
        // New format - object with dateFrom, dateTo, and period
        this.filters = { ...this.filters, ...periodFilters }
      }

      // Persist filters to localStorage
      this.persistFilters()
    },

    updateDateFiltersFromPeriod(period) {
      // Update date filters based on period
      const end = new Date()
      const start = new Date()

      switch (period) {
        case 'last7days':
          start.setDate(start.getDate() - 7)
          break
        case 'last30days':
          start.setDate(start.getDate() - 30)
          break
        case 'last90days':
          start.setDate(start.getDate() - 90)
          break
        case 'thisMonth':
          start.setDate(1) // First day of current month
          break
        case 'lastMonth':
          start.setMonth(start.getMonth() - 1) // Go to previous month
          start.setDate(1) // First day of previous month
          end.setDate(0) // Last day of previous month (by setting day 0 of current month)
          break
        case 'custom':
          // Keep existing date filters
          return
        default:
          start.setDate(start.getDate() - 30)
      }

      this.filters.dateFrom = start.toISOString().split('T')[0]
      this.filters.dateTo = end.toISOString().split('T')[0]
    },

    async refreshData() {
      await this.fetchVagasData()
    },

    async fetchAvailablePositions() {
      try {
        const positions = await reportsApi.getAvailablePositions()
        this.availablePositions = positions || []
      } catch (error) {
        console.error('Error fetching available positions:', error)
        // Fallback to default positions
        this.availablePositions = [
          'Data Engineering',
          'Frontend',
          'Fullstack',
          'DevOps',
          'Data Scientist',
          'Backend',
          'Mobile',
          'QA',
          'UX/UI',
          'Product Manager',
        ]
      }
    },

    async fetchAvailableSeniorities() {
      try {
        const seniorities = await reportsApi.getAvailableSeniority()
        this.availableSeniorities = seniorities || []
      } catch (error) {
        console.error('Error fetching available seniorities:', error)
        // Fallback to default seniorities
        this.availableSeniorities = ['Junior', 'Pleno', 'Senior', 'Lead', 'Principal']
      }
    },

    async fetchAvailableEmploymentTypes() {
      try {
        const employmentTypes = await reportsApi.getAvailableEmploymentTypes()
        this.availableEmploymentTypes = employmentTypes || []
      } catch (error) {
        console.error('Error fetching available employment types:', error)
        // Fallback to default employment types
        this.availableEmploymentTypes = [
          'CLT',
          'PJ',
          'Freelance',
          'Temporário',
          'Estágio',
          'Trainee',
          'Cooperado',
        ]
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
        this.locationData = []
        return []
      }
    },

    // Set selected job and persist it to localStorage
    setSelectedJob(job) {
      this.selectedJob = job
      this.persistSelectedJob()
    },

    // Persist filters to localStorage
    persistFilters() {
      try {
        localStorage.setItem('vagas_filters', JSON.stringify(this.filters))
      } catch (error) {
        console.error('Error persisting vagas filters to localStorage:', error)
      }
    },

    // Load persisted filters from localStorage
    loadPersistedFilters() {
      try {
        const savedFilters = localStorage.getItem('vagas_filters')
        if (savedFilters) {
          this.filters = { ...this.filters, ...JSON.parse(savedFilters) }
          console.log('Loaded persisted vagas filters:', this.filters)
        }
      } catch (error) {
        console.error('Error loading persisted vagas filters:', error)
      }
    },

    // Persist selected job to localStorage
    persistSelectedJob() {
      try {
        if (this.selectedJob) {
          localStorage.setItem('vagas_selected_job', JSON.stringify(this.selectedJob))
        } else {
          localStorage.removeItem('vagas_selected_job')
        }
      } catch (error) {
        console.error('Error persisting vagas selected job to localStorage:', error)
      }
    },

    // Load persisted selected job from localStorage
    loadPersistedSelectedJob() {
      try {
        const savedSelectedJob = localStorage.getItem('vagas_selected_job')
        if (savedSelectedJob) {
          this.selectedJob = JSON.parse(savedSelectedJob)
          console.log('Loaded persisted vagas selected job:', this.selectedJob)
        }
      } catch (error) {
        console.error('Error loading persisted vagas selected job:', error)
      }
    },
  },
})
