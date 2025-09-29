<template>
  <div
    ref="chartContainer"
    class="chart-container"
  />
</template>

<script setup>
  import { ref, onMounted, watch, onUnmounted } from 'vue'
  import * as echarts from 'echarts'

  const props = defineProps({
    data: {
      type: [Array, Object],
      required: true,
      default: () => [],
    },
    title: {
      type: String,
      default: '',
    },
  })

  const chartContainer = ref(null)
  let chartInstance = null

  const initChart = () => {
    if (chartInstance) {
      chartInstance.dispose()
    }

    if (chartContainer.value) {
      chartInstance = echarts.init(chartContainer.value)
      updateChart()
    } else {
      console.error('Chart container element is not available')
    }
  }

  const updateChart = () => {
    if (!chartInstance) {
      console.error('Chart instance is not initialized')
      return
    }

    // Handle different data formats
    let chartData = []
    let radius = '60%'

    try {
      if (Array.isArray(props.data)) {
        // Check if it's employment type distribution format (has job_employment_type and job_count)
        if (props.data.length > 0 && props.data[0].job_employment_type && props.data[0].job_count) {
          chartData = props.data.map((item) => ({
            value: item.job_count,
            name: item.job_employment_type,
          }))
        } else {
          // Assume it's already in the correct format with value and name
          chartData = props.data
        }
      } else if (props.data && props.data.data && Array.isArray(props.data.data)) {
        // If data is an object with a data property (like from Dashboard)
        chartData = props.data.data
        radius = props.data.radius || '60%'
      } else {
        // Special case for remote percentage data
        if (props.data && typeof props.data === 'object') {
          if (Array.isArray(props.data.data)) {
            chartData = props.data.data
            radius = props.data.radius || '60%'
          } else {
            console.error('Unable to extract chart data from provided object:', props.data)
          }
        } else {
          console.error('Unrecognized data format:', props.data)
        }
      }
    } catch (error) {
      console.error('Error processing chart data:', error)
      return
    }

    if (!chartData || !chartData.length) {
      return
    }

    const option = {
      title: {
        text: props.title,
        left: 'center',
        textStyle: {
          fontSize: 16,
          fontWeight: 'bold',
        },
      },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)',
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        top: 'middle',
      },
      series: [
        {
          name: 'Distribution',
          type: 'pie',
          radius: radius,
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
          data: chartData,
        },
      ],
    }

    chartInstance.setOption(option)
  }

  const resizeChart = () => {
    if (chartInstance) {
      chartInstance.resize()
    }
  }

  onMounted(() => {
    initChart()
    window.addEventListener('resize', resizeChart)
  })

  onUnmounted(() => {
    console.log('BasePieChart unmounted, disposing chart')
    if (chartInstance) {
      chartInstance.dispose()
    }
    window.removeEventListener('resize', resizeChart)
  })

  watch(
    () => props.data,
    () => {
      console.log('BasePieChart data changed, updating chart')
      updateChart()
    },
    { deep: true }
  )
</script>

<style scoped>
  .chart-container {
    width: 100%;
    height: 100%;
    min-height: 320px;
  }
</style>
