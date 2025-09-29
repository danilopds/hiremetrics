<template>
  <div class="chart-container">
    <VChart
      v-if="!loading"
      :option="chartOptions"
      :autoresize="true"
    />
    <div
      v-else
      class="flex items-center justify-center h-64 bg-gray-50 rounded-md"
    >
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600" />
    </div>
  </div>
</template>

<script setup>
  import { computed } from 'vue'
  import VChart from 'vue-echarts'
  import { createLineChartConfig, formatChartDate } from '@/utils/chartConfig'

  /**
   * Standardized line chart component using the chart configuration utilities
   * @displayName StandardLineChart
   */

  const props = defineProps({
    /**
     * Chart title
     */
    title: {
      type: String,
      default: '',
    },
    /**
     * Chart subtitle
     */
    subtitle: {
      type: String,
      default: '',
    },
    /**
     * X-axis data (categories)
     */
    xAxisData: {
      type: Array,
      default: () => [],
    },
    /**
     * Series data for the chart
     * Format: [{ name: 'Series Name', data: [1, 2, 3] }]
     */
    seriesData: {
      type: Array,
      default: () => [],
    },
    /**
     * Whether to format x-axis labels as dates
     */
    formatDates: {
      type: Boolean,
      default: false,
    },
    /**
     * Date format to use ('short', 'medium', 'long')
     */
    dateFormat: {
      type: String,
      default: 'medium',
    },
    /**
     * Whether the chart is loading
     */
    loading: {
      type: Boolean,
      default: false,
    },
    /**
     * Custom chart options to merge with defaults
     */
    customOptions: {
      type: Object,
      default: () => ({}),
    },
  })

  // Format x-axis data if needed
  const formattedXAxisData = computed(() => {
    if (props.formatDates) {
      return props.xAxisData.map((date) => formatChartDate(date, props.dateFormat))
    }
    return props.xAxisData
  })

  // Create series data in the format expected by ECharts
  const formattedSeriesData = computed(() => {
    return props.seriesData.map((series) => ({
      name: series.name,
      type: 'line',
      data: series.data,
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      emphasis: {
        focus: 'series',
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.3)',
        },
      },
    }))
  })

  // Generate chart options using our utility function
  const chartOptions = computed(() => {
    return createLineChartConfig({
      title: {
        text: props.title,
        subtext: props.subtitle,
        left: 'center',
      },
      xAxis: {
        type: 'category',
        data: formattedXAxisData.value,
        boundaryGap: false,
      },
      series: formattedSeriesData.value,
      ...props.customOptions,
    })
  })
</script>

<style scoped>
  .chart-container {
    width: 100%;
    height: 100%;
    min-height: 300px;
  }
</style>
