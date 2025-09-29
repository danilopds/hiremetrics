import { defineStore } from 'pinia'
import { reportsApi } from '@/api/reports'
import { fetchFilteredLocations } from '@/api/dashboard'

export const useEmpresasStore = defineStore('empresas', {
  state: () => ({
    jobs: [],
    loading: false,
    loadingDetails: false,
    error: null,
    availablePositions: [],
    availableCompanies: [],
    availableSeniorities: [],
    locationData: [], // Available locations for filtering
    selectedCompany: null,
    filters: {
      search_position_query: '', // No fixed default position
      employer_name: '', // Company filter
      job_is_remote: '', // Remote filter
      seniority: '', // Seniority filter
      job_city: null, // City filter
      dateFrom: null,
      dateTo: null,
      period: 'last30days',
    },
  }),

  getters: {
    totalJobs: (state) => state.jobs.length,
    totalCompanies: (state) => {
      const companies = new Set(state.jobs.map((job) => job.employer_name))
      return companies.size
    },
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

      // Load saved filters and selection from localStorage if available
      this.loadPersistedFilters()
      this.loadPersistedSelectedCompany()
    },

    async fetchEmpresasData() {
      this.loading = true
      this.error = null
      try {
        const {
          search_position_query,
          employer_name,
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
          selectedCompanies: employer_name ? [employer_name] : [],
          selectedPublishers: [],
          selectedSeniority: seniority ? [seniority] : [],
          selectedEmploymentTypes: [],
          selectedCities: job_city && job_city !== 'N/A' ? [job_city] : [],
          selectedStates: [],
          selectedSkills: [],
          selectedRemoteTypes:
            job_is_remote !== null && job_is_remote !== undefined && job_is_remote !== ''
              ? [job_is_remote === 'true' ? 'true' : 'false']
              : [],
          selectedDirectTypes: [],
        }

        console.log('Fetching empresas with filters:', filters)
        const jobs = await reportsApi.previewExport(filters, 1000) // Fetch up to 1000 records for complete company analysis
        console.log('Received jobs for empresas:', jobs.length)
        this.jobs = jobs || []

        // Update available companies from jobs data if not already loaded
        this.updateAvailableCompaniesFromJobs()
      } catch (error) {
        console.error('Error fetching empresas data:', error)
        this.error = error.message || 'Erro ao carregar empresas'
        this.jobs = []
      } finally {
        this.loading = false
      }
    },

    async fetchAvailableOptions() {
      try {
        // Fetch available positions for the position filter
        try {
          const positions = await reportsApi.getAvailablePositions()
          this.availablePositions = positions || []
        } catch (error) {
          console.warn('Failed to fetch positions, using empty array:', error)
          this.availablePositions = []
        }

        // Don't fetch companies here - they will be fetched position-specifically
        this.availableCompanies = []

        // Don't fetch seniority levels here - they will be fetched position-specifically
        this.availableSeniorities = ['Junior', 'Pleno', 'Senior', 'Lead', 'Principal']

        console.log('Available positions loaded:', {
          positions: this.availablePositions.length,
        })
      } catch (error) {
        console.error('Error fetching available options:', error)
        // Provide fallback empty arrays
        this.availablePositions = []
        this.availableCompanies = []
        this.availableSeniorities = ['Junior', 'Pleno', 'Senior', 'Lead', 'Principal']
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
      let end = new Date()
      let start = new Date()

      switch (period) {
        case 'last7days':
          start.setDate(start.getDate() - 7)
          break
        case 'last30days':
          start.setDate(start.getDate() - 30)
          break
        case 'last60days':
          start.setDate(start.getDate() - 60)
          break
        case 'last90days':
          start.setDate(start.getDate() - 90)
          break
        case 'thisMonth':
          start = new Date(end.getFullYear(), end.getMonth(), 1)
          break
        case 'lastMonth': {
          const lastMonth = new Date(end.getFullYear(), end.getMonth() - 1, 1)
          const lastDayOfPrevMonth = new Date(end.getFullYear(), end.getMonth(), 0) // Last day of previous month
          start = lastMonth
          end = lastDayOfPrevMonth
          break
        }
        default:
          start.setDate(start.getDate() - 30)
      }

      this.filters.dateFrom = start.toISOString().split('T')[0]
      this.filters.dateTo = end.toISOString().split('T')[0]
    },

    // Persist filters to localStorage
    persistFilters() {
      try {
        localStorage.setItem('empresas_filters', JSON.stringify(this.filters))
      } catch (error) {
        console.error('Error persisting empresas filters to localStorage:', error)
      }
    },

    // Load persisted filters from localStorage
    loadPersistedFilters() {
      try {
        const savedFilters = localStorage.getItem('empresas_filters')
        if (savedFilters) {
          this.filters = { ...this.filters, ...JSON.parse(savedFilters) }
          console.log('Loaded persisted empresas filters:', this.filters)
        }
      } catch (error) {
        console.error('Error loading persisted empresas filters:', error)
      }
    },

    // Helper method to get jobs for a specific company
    getJobsForCompany(companyName) {
      return this.jobs.filter((job) => job.employer_name === companyName)
    },

    // Helper method to get companies aggregated data
    getAggregatedCompanies() {
      const companiesMap = new Map()

      this.jobs.forEach((job) => {
        const companyName = job.employer_name
        if (companiesMap.has(companyName)) {
          companiesMap.set(companyName, companiesMap.get(companyName) + 1)
        } else {
          companiesMap.set(companyName, 1)
        }
      })

      // Convert to array and sort by job count (highest to lowest)
      return Array.from(companiesMap.entries())
        .map(([employer_name, job_count]) => ({ employer_name, job_count }))
        .sort((a, b) => b.job_count - a.job_count)
    },

    // Helper method to extract unique companies from jobs data
    updateAvailableCompaniesFromJobs() {
      if (this.availableCompanies.length === 0 && this.jobs.length > 0) {
        const uniqueCompanies = [...new Set(this.jobs.map((job) => job.employer_name))]
          .filter((company) => company && company.trim() !== '')
          .sort()
        this.availableCompanies = uniqueCompanies
        console.log('Extracted companies from jobs data:', uniqueCompanies.length)
      }
    },

    // Persist selected company to localStorage
    persistSelectedCompany() {
      try {
        if (this.selectedCompany) {
          localStorage.setItem('empresas_selected_company', JSON.stringify(this.selectedCompany))
        } else {
          localStorage.removeItem('empresas_selected_company')
        }
      } catch (error) {
        console.error('Error persisting empresas selected company to localStorage:', error)
      }
    },

    // Load persisted selected company from localStorage
    loadPersistedSelectedCompany() {
      try {
        const savedSelectedCompany = localStorage.getItem('empresas_selected_company')
        if (savedSelectedCompany) {
          this.selectedCompany = JSON.parse(savedSelectedCompany)
          console.log('Loaded persisted empresas selected company:', this.selectedCompany)
        }
      } catch (error) {
        console.error('Error loading persisted empresas selected company:', error)
      }
    },

    // Method to fetch available companies based on current position (similar to companies store)
    async fetchAvailableCompaniesForPosition(position) {
      try {
        // Use the reports API to get available companies for the specific position
        const companies = await reportsApi.getAvailableCompanies(position)
        this.availableCompanies = companies || []
        console.log('Fetched available companies for position:', position, companies?.length)
      } catch (error) {
        console.error('Error fetching available companies for position:', error)
        // Fallback to extracting from jobs data
        this.updateAvailableCompaniesFromJobs()
      }
    },

    // Method to fetch available seniority levels based on current position
    async fetchAvailableSeniorityForPosition(position) {
      try {
        // Use the reports API to get available seniority levels for the specific position
        const seniorities = await reportsApi.getAvailableSeniority(position)
        this.availableSeniorities = seniorities || [
          'Junior',
          'Pleno',
          'Senior',
          'Lead',
          'Principal',
        ]
        console.log(
          'Fetched available seniority levels for position:',
          position,
          seniorities?.length
        )
      } catch (error) {
        console.error('Error fetching available seniority levels for position:', error)
        // Fallback to default seniority levels
        this.availableSeniorities = ['Junior', 'Pleno', 'Senior', 'Lead', 'Principal']
      }
    },

    // Method to set the selected company
    setSelectedCompany(company) {
      this.selectedCompany = company
      console.log('Selected company set in store:', company?.employer_name)
      // Persist selection to localStorage
      this.persistSelectedCompany()
    },

    // Method to fetch filtered locations
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
  },
})
