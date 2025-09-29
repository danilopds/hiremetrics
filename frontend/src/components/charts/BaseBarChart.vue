<template>
  <VChart
    :option="chartOptions"
    autoresize
    style="height: 100%; width: 100%"
  />
</template>

<script setup>
  import { computed } from 'vue'
  import VChart from 'vue-echarts'
  import { use } from 'echarts/core'
  import { CanvasRenderer } from 'echarts/renderers'
  import { BarChart } from 'echarts/charts'
  import {
    GridComponent,
    TooltipComponent,
    LegendComponent,
    TitleComponent,
  } from 'echarts/components'

  use([CanvasRenderer, BarChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent])

  const props = defineProps({
    options: { type: Object, default: () => ({}) },
    data: { type: Object, required: true },
  })

  const chartOptions = computed(() => ({
    ...props.options,
    tooltip: props.data.tooltip,
    grid: props.data.grid, // Ensure grid configuration is passed through
    xAxis: props.data.xAxis,
    yAxis: {
      ...props.data.yAxis,
      minInterval: 1,
      splitNumber: 5,
      alignTicks: false,
    },
    series: props.data.series,
    legend: props.data.legend,
  }))
</script>

<style scoped>
  :host {
    display: block;
    height: 100%;
    width: 100%;
  }
</style>
