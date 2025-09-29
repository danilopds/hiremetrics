// Mock data generator functions
const generateTimeSeriesData = (startDate, days, baseValue, variance) => {
  const data = []
  const date = new Date(startDate)

  for (let i = 0; i < days; i++) {
    const value = baseValue + (Math.random() * variance * 2 - variance)
    data.push({
      date: new Date(date),
      value: Math.round(value),
    })
    date.setDate(date.getDate() + 1)
  }

  return data
}

const generateSkillsData = () => {
  const skills = [
    'JavaScript',
    'Python',
    'Java',
    'React',
    'Node.js',
    'TypeScript',
    'AWS',
    'Docker',
    'Kubernetes',
    'Machine Learning',
    'Data Science',
    'DevOps',
    'Cloud Computing',
    'Mobile Development',
    'UI/UX Design',
  ]

  return skills.map((skill) => ({
    name: skill,
    value: Math.round(Math.random() * 100),
    trend: Math.random() > 0.5 ? 'up' : 'down',
    change: Math.round(Math.random() * 20),
  }))
}

const generateLocationData = () => {
  return [
    {
      id: 1,
      position: [40.7128, -74.006],
      title: 'New York',
      description: 'Tech Hub',
      jobCount: 1250,
      avgSalary: 120000,
    },
    {
      id: 2,
      position: [37.7749, -122.4194],
      title: 'San Francisco',
      description: 'Silicon Valley',
      jobCount: 1500,
      avgSalary: 140000,
    },
    {
      id: 3,
      position: [51.5074, -0.1278],
      title: 'London',
      description: 'Tech Hub',
      jobCount: 950,
      avgSalary: 85000,
    },
    {
      id: 4,
      position: [52.52, 13.405],
      title: 'Berlin',
      description: 'Tech Hub',
      jobCount: 800,
      avgSalary: 75000,
    },
  ]
}

const generateCompanyData = () => {
  const companies = [
    'Google',
    'Microsoft',
    'Amazon',
    'Apple',
    'Meta',
    'Netflix',
    'Twitter',
    'LinkedIn',
    'Salesforce',
    'Adobe',
  ]

  return companies.map((company) => ({
    name: company,
    jobCount: Math.round(Math.random() * 500),
    avgSalary: Math.round(80000 + Math.random() * 70000),
    growth: Math.round(Math.random() * 30),
  }))
}

// Mock API endpoints
export const mockApi = {
  // Dashboard data
  getDashboardData: (config = {}) => {
    // Handle timeRange
    let days = 30
    if (config.timeRange) {
      switch (config.timeRange) {
        case '7d':
          days = 7
          break
        case '30d':
          days = 30
          break
        case '90d':
          days = 90
          break
        case '1y':
          days = 365
          break
      }
    }
    const startDate = new Date()
    startDate.setDate(startDate.getDate() - days)

    // Generate data
    const jobMarketTrends = generateTimeSeriesData(startDate, days, 1000, 200)
    let skillsDemand = generateSkillsData()
    let locationData = generateLocationData()
    const companyData = generateCompanyData()

    // Filter by skill
    if (config.skill) {
      skillsDemand = skillsDemand.filter((skill) => skill.name === config.skill)
    }

    // Filter by location
    if (config.location) {
      locationData = locationData.filter((loc) => loc.title === config.location)
    }

    // Optionally, filter companyData by location or skill if needed

    return {
      jobMarketTrends,
      skillsDemand,
      locationData,
      companyData,
    }
  },

  // Report data
  getReportData: (config) => {
    const { timeRange, filters } = config
    const startDate = new Date()

    // Adjust start date based on timeRange
    switch (timeRange) {
      case '7d':
        startDate.setDate(startDate.getDate() - 7)
        break
      case '30d':
        startDate.setDate(startDate.getDate() - 30)
        break
      case '90d':
        startDate.setDate(startDate.getDate() - 90)
        break
      case '1y':
        startDate.setFullYear(startDate.getFullYear() - 1)
        break
    }

    const data = {
      timeSeries: generateTimeSeriesData(startDate, 30, 1000, 200),
      skills: generateSkillsData(),
      locations: generateLocationData(),
      companies: generateCompanyData(),
    }

    // Apply filters if provided
    if (filters) {
      // Implement filtering logic here
    }

    return data
  },

  // User profile data
  getUserProfile: () => ({
    name: 'John Doe',
    email: 'john.doe@example.com',
    jobTitle: 'HR Manager',
    company: 'Tech Corp',
    avatar: 'https://i.pravatar.cc/150',
    preferences: {
      defaultView: 'overview',
      notifications: {
        weeklyReport: true,
        marketUpdates: true,
        newFeatures: false,
      },
      timezone: 'UTC',
    },
  }),

  // Saved reports
  getSavedReports: () => [
    {
      id: 1,
      name: 'Monthly Tech Hiring Trends',
      created: '2025-01-15',
      updated: '2025-02-01',
      config: {
        metrics: ['jobPostings', 'avgSalary'],
        timeRange: '30d',
        chartType: 'line',
      },
    },
    {
      id: 2,
      name: 'Salary Analysis Q1 2025',
      created: '2025-01-01',
      updated: '2025-01-31',
      config: {
        metrics: ['avgSalary', 'skillsDemand'],
        timeRange: '90d',
        chartType: 'bar',
      },
    },
  ],
}

// Export mock data for direct use in components
export const mockData = {
  jobMarketTrends: generateTimeSeriesData(new Date(), 30, 1000, 200),
  skillsDemand: generateSkillsData(),
  locationData: generateLocationData(),
  companyData: generateCompanyData(),
}
