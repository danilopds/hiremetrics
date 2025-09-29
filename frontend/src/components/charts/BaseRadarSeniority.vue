<template>
  <VChart
    :option="option"
    autoresize
    style="height: 400px; width: 100%"
  />
</template>

<script setup>
  import { computed } from 'vue'
  import VChart from 'vue-echarts'

  const props = defineProps({
    skills: { type: Array, required: true }, // array of skill names
    seniorityLevels: { type: Array, required: true }, // array of seniority names
    data: { type: Array, required: true }, // array of { skill, seniority, skill_count }
  })

  const colorPalette = [
    '#2563eb',
    '#10b981',
    '#f59e42',
    '#ef4444',
    '#a855f7',
    '#fbbf24',
    '#14b8a6',
    '#6366f1',
  ]

  const option = computed(() => {
    // Prepare radar indicators (skills) with minimum scale to avoid ECharts warnings
    const indicators = props.skills.map((skill) => {
      const skillCounts = props.data.filter((d) => d.skill === skill).map((d) => d.skill_count)
      const maxCount = Math.max(...skillCounts, 1)
      // Ensure minimum scale of 4 to avoid ECharts alignment warnings for small values
      const adjustedMax = Math.max(maxCount, 4)
      return {
        name: skill,
        max: adjustedMax,
      }
    })

    // Prepare series for each seniority
    const series = props.seniorityLevels.map((seniority, idx) => {
      const values = props.skills.map((skill) => {
        const found = props.data.find((d) => d.skill === skill && d.seniority === seniority)
        return found ? found.skill_count : 0
      })
      return {
        value: values,
        name: seniority,
        lineStyle: { color: colorPalette[idx % colorPalette.length] },
        itemStyle: { color: colorPalette[idx % colorPalette.length] },
        areaStyle: { opacity: 0.08, color: colorPalette[idx % colorPalette.length] },
      }
    })

    return {
      tooltip: {},
      legend: { data: props.seniorityLevels, top: 0 },
      radar: {
        indicator: indicators,
        radius: '65%',
        splitNumber: 4,
        // Disable alignTicks to avoid the warning
        alignTicks: false,
        // Explicitly set scale configuration to prevent alignment warnings
        scale: false,
        // Set consistent start angle
        startAngle: 90,
        axisName: {
          fontSize: 12,
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(0, 0, 0, 0.1)',
          },
        },
        splitArea: {
          show: true,
          areaStyle: {
            color: ['rgba(255, 255, 255, 0.5)'],
          },
        },
        axisLine: {
          lineStyle: {
            color: 'rgba(0, 0, 0, 0.2)',
          },
        },
      },
      series: [
        {
          type: 'radar',
          data: series,
        },
      ],
    }
  })
</script>
