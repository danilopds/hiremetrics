<template>
  <div
    ref="chartRef"
    class="w-full h-full"
  />
</template>

<script setup>
  import { ref, onMounted, onUnmounted, watch } from 'vue'
  import * as echarts from 'echarts'

  const props = defineProps({
    data: {
      type: Object,
      required: true,
    },
  })

  const chartRef = ref(null)
  let chart = null

  function initChart() {
    if (chartRef.value) {
      chart = echarts.init(chartRef.value)
      const options = {
        ...props.data,
        yAxis: {
          ...props.data.yAxis,
          minInterval: 1,
          splitNumber: 5,
          alignTicks: false,
        },
      }
      chart.setOption(options)
    }
  }

  function resizeChart() {
    if (chart) {
      chart.resize()
    }
  }

  watch(
    () => props.data,
    (newData) => {
      if (chart) {
        const options = {
          ...newData,
          yAxis: {
            ...newData.yAxis,
            minInterval: 1,
            splitNumber: 5,
            alignTicks: false,
          },
        }
        chart.setOption(options)
      }
    },
    { deep: true }
  )

  onMounted(() => {
    initChart()
    window.addEventListener('resize', resizeChart)
  })

  onUnmounted(() => {
    if (chart) {
      chart.dispose()
      chart = null
    }
    window.removeEventListener('resize', resizeChart)
  })
</script>

<style scoped>
  :host {
    display: block;
    height: 100%;
    width: 100%;
  }
</style>
