/**
 * Standardized chart formatting utilities for consistent charts across all pages
 */

export const DEFAULT_COLOR_PALETTE = [
  '#2563eb',
  '#10b981',
  '#f59e42',
  '#ef4444',
  '#a855f7',
  '#fbbf24',
  '#14b8a6',
  '#6366f1',
]

/**
 * Creates a standard bar chart configuration
 * @param {Object} options - Chart options
 * @param {Array} options.categories - X-axis categories
 * @param {Array} options.values - Y-axis values
 * @param {string} options.seriesName - Name for the series
 * @param {string} options.color - Color for bars (defaults to blue)
 * @param {boolean} options.showLabels - Whether to show data labels
 * @param {string} options.xAxisType - X-axis type ('category' or 'value')
 * @param {string} options.yAxisType - Y-axis type ('category' or 'value')
 * @param {Object} options.tooltip - Custom tooltip configuration
 * @returns {Object} ECharts configuration object
 */
export function createBarChartConfig({
  categories,
  values,
  seriesName = 'Count',
  color = '#3b82f6',
  showLabels = true,
  xAxisType = 'category',
  yAxisType = 'value',
  tooltip = {},
}) {
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      ...tooltip,
    },
    xAxis: {
      type: xAxisType,
      data: xAxisType === 'category' ? categories : undefined,
      axisLabel: {
        interval: 0,
        rotate: 45,
        overflow: 'break',
        fontSize: 12,
        color: '#333',
      },
    },
    yAxis: {
      type: yAxisType,
      data: yAxisType === 'category' ? categories : undefined,
      name: yAxisType === 'value' ? seriesName : undefined,
    },
    series: [
      {
        name: seriesName,
        type: 'bar',
        data: values,
        itemStyle: { color },
        label: showLabels
          ? {
              show: true,
              position: 'top',
              color: '#222',
              fontWeight: 'bold',
              formatter: '{c}',
            }
          : undefined,
      },
    ],
  }
}

/**
 * Creates a standard line chart configuration
 * @param {Object} options - Chart options
 * @param {Array} options.dates - X-axis dates
 * @param {Array} options.values - Y-axis values
 * @param {string} options.seriesName - Name for the series
 * @param {string} options.color - Line color
 * @param {boolean} options.smooth - Whether to smooth the line
 * @param {boolean} options.showArea - Whether to show area under the line
 * @param {boolean} options.showLabels - Whether to show data labels
 * @param {Object} options.tooltip - Custom tooltip configuration
 * @returns {Object} ECharts configuration object
 */
export function createLineChartConfig({
  dates,
  values,
  seriesName = 'Value',
  color = '#3b82f6',
  smooth = true,
  showArea = true,
  showLabels = true,
  tooltip = {},
}) {
  return {
    tooltip: {
      trigger: 'axis',
      ...tooltip,
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLabel: { rotate: 45 },
    },
    yAxis: {
      type: 'value',
      minInterval: 1,
      splitNumber: 5,
    },
    series: [
      {
        name: seriesName,
        type: 'line',
        data: values,
        smooth,
        lineStyle: { color },
        areaStyle: showArea ? { color: `${color}15` } : undefined,
        label: showLabels
          ? {
              show: true,
              position: 'top',
              color: '#222',
              fontWeight: 'bold',
              formatter: '{c}',
            }
          : undefined,
      },
    ],
  }
}

/**
 * Creates a standard pie chart configuration
 * @param {Object} options - Chart options
 * @param {Array} options.data - Array of { name, value } objects
 * @param {string} options.title - Chart title
 * @param {string} options.radius - Pie chart radius (e.g., '60%')
 * @param {boolean} options.showLegend - Whether to show the legend
 * @returns {Object} ECharts configuration object
 */
export function createPieChartConfig({ data, title = '', radius = '60%', showLegend = true }) {
  return {
    title: title
      ? {
          text: title,
          left: 'center',
          textStyle: {
            fontSize: 16,
            fontWeight: 'bold',
          },
        }
      : undefined,
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)',
    },
    legend: showLegend
      ? {
          orient: 'vertical',
          left: 'left',
          top: 'middle',
        }
      : undefined,
    series: [
      {
        name: 'Distribution',
        type: 'pie',
        radius,
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
        data,
      },
    ],
  }
}

/**
 * Creates a standard stacked bar chart configuration
 * @param {Object} options - Chart options
 * @param {Array} options.categories - X-axis categories
 * @param {Array} options.series - Series data for stacking
 * @param {Array} options.colorPalette - Array of colors for series
 * @param {boolean} options.showLabels - Whether to show data labels
 * @returns {Object} ECharts configuration object
 */
export function createStackedBarChartConfig({
  categories,
  series,
  colorPalette = DEFAULT_COLOR_PALETTE,
  showLabels = true,
}) {
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
    },
    legend: {
      data: series.map((s) => s.name),
      top: 0,
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        interval: 0,
        rotate: 45,
        fontSize: 12,
      },
    },
    yAxis: {
      type: 'value',
    },
    series: series.map((s, idx) => ({
      name: s.name,
      type: 'bar',
      stack: 'total',
      data: s.data,
      itemStyle: { color: colorPalette[idx % colorPalette.length] },
      label:
        showLabels && idx === series.length - 1
          ? {
              show: true,
              position: 'top',
              formatter: (params) => {
                // Calculate total of the stack at this position
                let total = 0
                series.forEach((s) => {
                  total += s.data[params.dataIndex] || 0
                })
                return total
              },
              color: '#333',
              fontWeight: 'bold',
            }
          : undefined,
    })),
  }
}

/**
 * Formats job data for Remote vs On-site pie chart
 * @param {Array} jobs - Array of job objects
 * @returns {Object} Formatted data for pie chart
 */
export function formatRemotePieChartData(jobs) {
  const remoteCounts = { Remoto: 0, Presencial: 0 }

  jobs.forEach((job) => {
    if (job.job_is_remote === true || job.job_is_remote === 'true' || job.job_is_remote === 1) {
      remoteCounts['Remoto']++
    } else {
      remoteCounts['Presencial']++
    }
  })

  return {
    radius: '60%',
    data: [
      { value: remoteCounts['Remoto'], name: 'Remoto' },
      { value: remoteCounts['Presencial'], name: 'Presencial' },
    ],
  }
}

/**
 * Formats job data for Top Cities bar chart
 * @param {Array} jobs - Array of job objects
 * @param {number} limit - Maximum number of cities to include
 * @returns {Object} Formatted data for bar chart
 */
export function formatTopCitiesData(jobs, limit = 5) {
  // Aggregate job counts by city
  const cityCounts = {}
  jobs.forEach((job) => {
    if (!job.job_city) {
      return
    }
    cityCounts[job.job_city] = (cityCounts[job.job_city] || 0) + 1
  })

  // Sort cities by count descending and take top N
  const sortedCities = Object.entries(cityCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)

  return createBarChartConfig({
    categories: sortedCities.map(([city]) => city),
    values: sortedCities.map(([, count]) => count),
    seriesName: 'Contagem de Vagas',
    color: '#3b82f6',
    showLabels: true,
  })
}

/**
 * Formats job data for Employment Type bar chart
 * @param {Array} jobs - Array of job objects
 * @returns {Object} Formatted data for bar chart
 */
export function formatEmploymentTypeData(jobs) {
  // Aggregate job counts by employment type
  const typeCounts = {}
  jobs.forEach((job) => {
    if (!job.job_employment_type) {
      return
    }
    typeCounts[job.job_employment_type] = (typeCounts[job.job_employment_type] || 0) + 1
  })

  // Sort types by count descending
  const sortedTypes = Object.entries(typeCounts).sort((a, b) => b[1] - a[1])

  return createBarChartConfig({
    categories: sortedTypes.map(([type]) => type),
    values: sortedTypes.map(([, count]) => count),
    seriesName: 'Contagem de Vagas',
  })
}

/**
 * Calculate entity metrics (unique cities, publishers, companies)
 * @param {Array} jobs - Array of job objects
 * @returns {Object} Formatted data for entities bar chart
 */
export function formatEntitiesOverviewData(jobs) {
  // Unique cities
  const citySet = new Set()
  jobs.forEach((job) => {
    if (job.job_city) {
      citySet.add(job.job_city)
    }
  })

  // Unique publishers (from apply_options - same logic as Publishers page)
  const publisherSet = new Set()
  jobs.forEach((job) => {
    if (job.apply_options) {
      try {
        const applyOptions = JSON.parse(job.apply_options)
        if (Array.isArray(applyOptions)) {
          applyOptions.forEach((option) => {
            if (option.publisher && option.publisher.trim()) {
              publisherSet.add(option.publisher.trim())
            }
          })
        }
      } catch (error) {
        // If JSON parsing fails, fallback to job_publisher
        console.warn('Failed to parse apply_options JSON:', error)
        if (job.job_publisher) {
          publisherSet.add(job.job_publisher)
        }
      }
    } else if (job.job_publisher) {
      // Fallback to job_publisher if apply_options is not available
      publisherSet.add(job.job_publisher)
    }
  })

  // Unique companies
  const companySet = new Set()
  jobs.forEach((job) => {
    if (job.employer_name) {
      companySet.add(job.employer_name)
    }
  })

  return createBarChartConfig({
    categories: ['Cidades', 'Canais', 'Empresas'],
    values: [citySet.size, publisherSet.size, companySet.size],
    seriesName: 'Contagem',
    color: '#6366f1',
  })
}
