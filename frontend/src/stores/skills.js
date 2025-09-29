import { defineStore } from 'pinia'
import { reportsApi } from '@/api/reports'

export const useSkillsStore = defineStore('skills', {
  state: () => ({
    jobs: [],
    loading: false,
    loadingDetails: false,
    error: null,
    availablePositions: [],
    availableSkills: [],
    availableSeniorities: [],
    selectedSkill: null,
    filters: {
      search_position_query: '', // No fixed default position
      skills: [], // Skills filter - now supports multiple values
      job_is_remote: '', // Remote filter
      seniority: '', // Seniority filter
      dateFrom: null,
      dateTo: null,
      period: 'last30days',
    },
  }),

  getters: {
    totalJobs: (state) => state.jobs.length,
    totalSkills: (state) => {
      const skills = new Set()
      state.jobs.forEach((job) => {
        if (job.extracted_skills) {
          try {
            const skillsArray = JSON.parse(job.extracted_skills)
            if (Array.isArray(skillsArray)) {
              skillsArray.forEach((skill) => skills.add(skill))
            }
          } catch (e) {
            // If parsing fails, treat as comma-separated string
            const skillsString = job.extracted_skills
            if (typeof skillsString === 'string') {
              skillsString.split(',').forEach((skill) => skills.add(skill.trim()))
            }
          }
        }
      })
      return skills.size
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
      this.loadPersistedSelectedSkill()
    },

    async fetchSkillsData() {
      this.loading = true
      this.error = null
      try {
        const { search_position_query, skills, job_is_remote, seniority, dateFrom, dateTo } =
          this.filters

        // Build filters object for skills API
        const filters = {
          dateFrom: dateFrom,
          dateTo: dateTo,
          selectedPosition: search_position_query || '',
          selectedCompanies: [],
          selectedPublishers: [],
          selectedSeniority: seniority ? [seniority] : [],
          selectedEmploymentTypes: [],
          selectedCities: [],
          selectedStates: [],
          selectedSkills: skills ? (Array.isArray(skills) ? skills : [skills]) : [],
          selectedRemoteTypes:
            job_is_remote !== null && job_is_remote !== undefined && job_is_remote !== ''
              ? [job_is_remote === 'true' ? 'true' : 'false']
              : [],
          selectedDirectTypes: [],
        }

        console.log('Fetching skills data with filters:', filters)

        // Use the dedicated skills API endpoint
        const jobs = await reportsApi.getJobsBySkills(filters) // Fetch up to 10000 records for complete skills analysis
        console.log('Received jobs for skills:', jobs.length)
        this.jobs = jobs || []
      } catch (error) {
        console.error('Error fetching skills data:', error)
        this.error = error.message || 'Erro ao carregar dados de skills'
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

        // Fetch available skills
        try {
          const skills = await reportsApi.getAvailableSkills()
          this.availableSkills = skills || []
        } catch (error) {
          console.warn('Failed to fetch skills, using empty array:', error)
          this.availableSkills = []
        }

        // Don't fetch seniority levels here - they will be fetched position-specifically
        this.availableSeniorities = ['Junior', 'Pleno', 'Senior', 'Lead', 'Principal']

        console.log('Available options loaded:', {
          positions: this.availablePositions.length,
          skills: this.availableSkills.length,
        })
      } catch (error) {
        console.error('Error fetching available options:', error)
        // Provide fallback empty arrays
        this.availablePositions = []
        this.availableSkills = []
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
        localStorage.setItem('skills_filters', JSON.stringify(this.filters))
      } catch (error) {
        console.error('Error persisting skills filters to localStorage:', error)
      }
    },

    // Load persisted filters from localStorage
    loadPersistedFilters() {
      try {
        const savedFilters = localStorage.getItem('skills_filters')
        if (savedFilters) {
          const parsedFilters = JSON.parse(savedFilters)

          // Handle migration from string to array for skills
          if (parsedFilters.skills && typeof parsedFilters.skills === 'string') {
            parsedFilters.skills = parsedFilters.skills ? [parsedFilters.skills] : []
          }

          this.filters = { ...this.filters, ...parsedFilters }
          console.log('Loaded persisted skills filters:', this.filters)
        }
      } catch (error) {
        console.error('Error loading persisted skills filters:', error)
      }
    },

    // Helper method to get jobs for a specific skill
    getJobsForSkill(skillName) {
      return this.jobs.filter((job) => {
        if (!job.extracted_skills) {
          return false
        }

        try {
          const skillsArray = JSON.parse(job.extracted_skills)
          if (Array.isArray(skillsArray)) {
            return skillsArray.some((skill) =>
              skill.toLowerCase().includes(skillName.toLowerCase())
            )
          }
        } catch (e) {
          // If parsing fails, treat as comma-separated string
          const skillsString = job.extracted_skills
          if (typeof skillsString === 'string') {
            return skillsString.toLowerCase().includes(skillName.toLowerCase())
          }
        }
        return false
      })
    },

    // Helper method to get skills aggregated data
    getAggregatedSkills() {
      const skillsMap = new Map()

      // If specific skills are filtered, only show those skills
      if (this.filters.skills && this.filters.skills.length > 0) {
        // Initialize the requested skills with 0 count
        this.filters.skills.forEach((skill) => {
          skillsMap.set(skill, 0)
        })

        // Count jobs for each requested skill
        this.jobs.forEach((job) => {
          if (job.extracted_skills) {
            try {
              const skillsArray = JSON.parse(job.extracted_skills)
              if (Array.isArray(skillsArray)) {
                skillsArray.forEach((skill) => {
                  const skillName = skill.trim()
                  if (skillName && this.filters.skills.includes(skillName)) {
                    skillsMap.set(skillName, skillsMap.get(skillName) + 1)
                  }
                })
              }
            } catch (e) {
              // If parsing fails, treat as comma-separated string
              const skillsString = job.extracted_skills
              if (typeof skillsString === 'string') {
                skillsString.split(',').forEach((skill) => {
                  const skillName = skill.trim()
                  if (skillName && this.filters.skills.includes(skillName)) {
                    skillsMap.set(skillName, skillsMap.get(skillName) + 1)
                  }
                })
              }
            }
          }
        })
      } else {
        // If no specific skills filter, show all skills (original behavior)
        this.jobs.forEach((job) => {
          if (job.extracted_skills) {
            try {
              const skillsArray = JSON.parse(job.extracted_skills)
              if (Array.isArray(skillsArray)) {
                skillsArray.forEach((skill) => {
                  const skillName = skill.trim()
                  if (skillName) {
                    if (skillsMap.has(skillName)) {
                      skillsMap.set(skillName, skillsMap.get(skillName) + 1)
                    } else {
                      skillsMap.set(skillName, 1)
                    }
                  }
                })
              }
            } catch (e) {
              // If parsing fails, treat as comma-separated string
              const skillsString = job.extracted_skills
              if (typeof skillsString === 'string') {
                skillsString.split(',').forEach((skill) => {
                  const skillName = skill.trim()
                  if (skillName) {
                    if (skillsMap.has(skillName)) {
                      skillsMap.set(skillName, skillsMap.get(skillName) + 1)
                    } else {
                      skillsMap.set(skillName, 1)
                    }
                  }
                })
              }
            }
          }
        })
      }

      // Convert to array and sort by job count (highest to lowest)
      return Array.from(skillsMap.entries())
        .map(([skill_name, job_count]) => ({ skill_name, job_count }))
        .sort((a, b) => b.job_count - a.job_count)
    },

    // Method to fetch available skills based on current position
    async fetchAvailableSkillsForPosition(position) {
      try {
        // Use the reports API to get available skills for the specific position
        const skills = await reportsApi.getAvailableSkills(position)
        this.availableSkills = skills || []
        console.log('Fetched available skills for position:', position, skills?.length)
      } catch (error) {
        console.error('Error fetching available skills for position:', error)
        // Fallback to extracting from jobs data
        this.updateAvailableSkillsFromJobs()
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

    // Helper method to extract unique skills from jobs data
    updateAvailableSkillsFromJobs() {
      if (this.availableSkills.length === 0 && this.jobs.length > 0) {
        const uniqueSkills = new Set()

        this.jobs.forEach((job) => {
          if (job.extracted_skills) {
            try {
              const skillsArray = JSON.parse(job.extracted_skills)
              if (Array.isArray(skillsArray)) {
                skillsArray.forEach((skill) => uniqueSkills.add(skill.trim()))
              }
            } catch (e) {
              // If parsing fails, treat as comma-separated string
              const skillsString = job.extracted_skills
              if (typeof skillsString === 'string') {
                skillsString.split(',').forEach((skill) => uniqueSkills.add(skill.trim()))
              }
            }
          }
        })

        this.availableSkills = Array.from(uniqueSkills).sort()
        console.log('Extracted skills from jobs data:', this.availableSkills.length)
      }
    },

    // Persist selected skill to localStorage
    persistSelectedSkill() {
      try {
        if (this.selectedSkill) {
          localStorage.setItem('skills_selected_skill', JSON.stringify(this.selectedSkill))
        } else {
          localStorage.removeItem('skills_selected_skill')
        }
      } catch (error) {
        console.error('Error persisting skills selected skill to localStorage:', error)
      }
    },

    // Load persisted selected skill from localStorage
    loadPersistedSelectedSkill() {
      try {
        const savedSelectedSkill = localStorage.getItem('skills_selected_skill')
        if (savedSelectedSkill) {
          this.selectedSkill = JSON.parse(savedSelectedSkill)
          console.log('Loaded persisted skills selected skill:', this.selectedSkill)
        }
      } catch (error) {
        console.error('Error loading persisted skills selected skill:', error)
      }
    },

    // Method to set the selected skill
    setSelectedSkill(skill) {
      this.selectedSkill = skill
      console.log('Selected skill set in store:', skill?.skill_name)
      // Persist selection to localStorage
      this.persistSelectedSkill()
    },
  },
})
