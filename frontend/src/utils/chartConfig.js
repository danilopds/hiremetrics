/**
 * Chart Configuration Utilities
 *
 * This file provides standardized chart configurations and helper functions
 * to maintain consistent styling and behavior across all charts.
 */

import { chartColors } from '@/styles/tokens'

/**
 * Default chart theme settings
 * These settings are applied to all charts for consistent styling
 */
export const defaultChartTheme = {
  // Text styling
  textStyle: {
    fontFamily: 'Inter, sans-serif',
    color: '#374151', // gray-700
  },

  // Title styling
  title: {
    textStyle: {
      fontSize: 16,
      fontWeight: 'bold',
      color: '#1f2937', // gray-800
    },
    subtextStyle: {
      color: '#6b7280', // gray-500
    },
  },

  // Legend styling
  legend: {
    textStyle: {
      color: '#4b5563', // gray-600
    },
  },

  // Tooltip styling
  tooltip: {
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    borderColor: '#e5e7eb', // gray-200
    textStyle: {
      color: '#1f2937', // gray-800
    },
    axisPointer: {
      lineStyle: {
        color: '#9ca3af', // gray-400
      },
      crossStyle: {
        color: '#9ca3af', // gray-400
      },
      shadowStyle: {
        color: 'rgba(156, 163, 175, 0.3)', // gray-400 with opacity
      },
    },
  },

  // Axis styling
  xAxis: {
    axisLine: {
      lineStyle: {
        color: '#d1d5db', // gray-300
      },
    },
    axisTick: {
      lineStyle: {
        color: '#d1d5db', // gray-300
      },
    },
    axisLabel: {
      color: '#4b5563', // gray-600
    },
    splitLine: {
      lineStyle: {
        color: '#e5e7eb', // gray-200
      },
    },
  },

  yAxis: {
    axisLine: {
      lineStyle: {
        color: '#d1d5db', // gray-300
      },
    },
    axisTick: {
      lineStyle: {
        color: '#d1d5db', // gray-300
      },
    },
    axisLabel: {
      color: '#4b5563', // gray-600
    },
    splitLine: {
      lineStyle: {
        color: '#e5e7eb', // gray-200
      },
    },
  },
}

/**
 * Creates a color palette for charts based on the number of data points
 * @param {number} count - Number of colors needed
 * @param {string} type - Type of palette ('primary', 'secondary', 'categorical')
 * @returns {string[]} Array of color hex codes
 */
export const getChartColorPalette = (count, type = 'primary') => {
  const palette = chartColors[type] || chartColors.primary

  // If we need more colors than in our palette, cycle through them
  if (count <= palette.length) {
    return palette.slice(0, count)
  } else {
    const result = []
    for (let i = 0; i < count; i++) {
      result.push(palette[i % palette.length])
    }
    return result
  }
}

/**
 * Generates a consistent line chart configuration
 * @param {Object} options - Custom options to override defaults
 * @returns {Object} ECharts options object
 */
export const createLineChartConfig = (options = {}) => {
  const defaultOptions = {
    color: chartColors.primary,
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985',
        },
      },
    },
    legend: {
      type: 'scroll',
      orient: 'horizontal',
      bottom: 0,
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
    },
    yAxis: {
      type: 'value',
    },
  }

  return mergeChartOptions(defaultOptions, options)
}

/**
 * Generates a consistent bar chart configuration
 * @param {Object} options - Custom options to override defaults
 * @returns {Object} ECharts options object
 */
export const createBarChartConfig = (options = {}) => {
  const defaultOptions = {
    color: chartColors.primary,
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
    },
    legend: {
      type: 'scroll',
      orient: 'horizontal',
      bottom: 0,
    },
    xAxis: {
      type: 'category',
      axisLabel: {
        interval: 0,
        rotate: 30,
      },
    },
    yAxis: {
      type: 'value',
    },
  }

  return mergeChartOptions(defaultOptions, options)
}

/**
 * Generates a consistent pie chart configuration
 * @param {Object} options - Custom options to override defaults
 * @returns {Object} ECharts options object
 */
export const createPieChartConfig = (options = {}) => {
  const defaultOptions = {
    color: chartColors.categorical,
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)',
    },
    legend: {
      type: 'scroll',
      orient: 'horizontal',
      bottom: 0,
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: false,
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
      },
    ],
  }

  return mergeChartOptions(defaultOptions, options)
}

/**
 * Generates a consistent bubble chart configuration
 * @param {Object} options - Custom options to override defaults
 * @returns {Object} ECharts options object
 */
export const createBubbleChartConfig = (options = {}) => {
  const defaultOptions = {
    color: chartColors.categorical,
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      containLabel: true,
    },
    tooltip: {
      trigger: 'item',
      formatter: function (params) {
        return `${params.seriesName}<br/>${params.name}: ${params.value[2]}`
      },
    },
    legend: {
      right: '10%',
      top: '3%',
      type: 'scroll',
    },
    xAxis: {
      type: 'category',
      splitLine: {
        show: true,
      },
    },
    yAxis: {
      type: 'category',
      splitLine: {
        show: true,
      },
    },
    series: [],
  }

  return mergeChartOptions(defaultOptions, options)
}

/**
 * Generates a consistent heatmap chart configuration
 * @param {Object} options - Custom options to override defaults
 * @returns {Object} ECharts options object
 */
export const createHeatmapConfig = (options = {}) => {
  const defaultOptions = {
    tooltip: {
      position: 'top',
      formatter: function (params) {
        return `${params.name}: ${params.value[2]}`
      },
    },
    grid: {
      left: '3%',
      right: '7%',
      bottom: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      splitArea: {
        show: true,
      },
    },
    yAxis: {
      type: 'category',
      splitArea: {
        show: true,
      },
    },
    visualMap: {
      min: 0,
      max: 10,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: [
          '#e0f2fe', // primary-100
          '#7dd3fc', // primary-300
          '#0ea5e9', // primary-500
          '#0369a1', // primary-700
        ],
      },
    },
    series: [
      {
        type: 'heatmap',
        label: {
          show: true,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  }

  return mergeChartOptions(defaultOptions, options)
}

/**
 * Formats date strings consistently across all charts
 * @param {string} dateStr - Date string to format
 * @param {string} format - Format type ('short', 'medium', 'long')
 * @returns {string} Formatted date string
 */
export const formatChartDate = (dateStr, format = 'medium') => {
  if (!dateStr) {
    return ''
  }

  const date = new Date(dateStr)

  // Check if date is valid
  if (isNaN(date.getTime())) {
    return dateStr
  }

  // Format options
  const options = {
    short: { day: '2-digit', month: '2-digit' },
    medium: { day: '2-digit', month: '2-digit', year: 'numeric' },
    long: { day: '2-digit', month: 'long', year: 'numeric' },
  }

  return date.toLocaleDateString('pt-BR', options[format] || options.medium)
}

/**
 * Merges custom chart options with default options
 * @param {Object} defaultOptions - Default chart options
 * @param {Object} customOptions - Custom options to override defaults
 * @returns {Object} Merged options object
 */
export const mergeChartOptions = (defaultOptions, customOptions) => {
  const result = { ...defaultOptions }

  // Handle special case for series which is an array
  if (customOptions.series && defaultOptions.series) {
    result.series = customOptions.series.map((customSeries, index) => {
      const defaultSeries = defaultOptions.series[index] || {}
      return { ...defaultSeries, ...customSeries }
    })
  }

  // Merge all other properties
  Object.keys(customOptions).forEach((key) => {
    if (key !== 'series') {
      if (
        typeof customOptions[key] === 'object' &&
        !Array.isArray(customOptions[key]) &&
        defaultOptions[key] &&
        typeof defaultOptions[key] === 'object'
      ) {
        result[key] = { ...defaultOptions[key], ...customOptions[key] }
      } else {
        result[key] = customOptions[key]
      }
    }
  })

  return result
}
