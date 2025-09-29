<template>
  <VChart
    :option="option"
    autoresize
    :style="{ height: height, width: '100%' }"
  />
</template>

<script setup>
  import { computed } from 'vue'
  import VChart from 'vue-echarts'

  const props = defineProps({
    skills: { type: Array, required: true }, // array of skill names
    seniorityLevels: { type: Array, required: true }, // array of seniority names
    data: { type: Array, required: true }, // array of { skill, seniority, skill_count }
    height: { type: String, default: '500px' }, // Increased default height
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
    // Prepare data for scatter
    const scatterData = props.data.map((d) => [
      props.skills.indexOf(d.skill),
      props.seniorityLevels.indexOf(d.seniority),
      d.skill_count,
      d.skill,
      d.seniority,
    ])

    // Calculate statistics for better scaling
    // const counts = props.data.map((d) => d.skill_count)
    // const maxCount = Math.max(...counts)
    // const minCount = Math.min(...counts)
    // const avgCount = counts.reduce((a, b) => a + b, 0) / counts.length

    // Smart scaling function to prevent overflow
    const calculateBubbleSize = (count) => {
      if (count === 0) {
        return 2
      } // Minimum size for zero values

      // Apply logarithmic scaling to reduce impact of very large values
      const logScaled = Math.log(count + 1) * 10

      // Cap the maximum size to prevent overflow
      const maxSize = 500
      const cappedSize = Math.min(logScaled, maxSize)

      // Ensure minimum size for visibility
      return Math.max(2, cappedSize)
    }

    return {
      tooltip: {
        formatter: function (params) {
          return `<b>${params.data[3]}</b><br>Seniority: ${params.data[4]}<br>Count: ${params.data[2]}`
        },
      },
      grid: {
        left: '5%',
        right: '5%',
        top: '10%',
        bottom: '15%',
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: props.skills,
        name: 'Skill',
        axisLabel: {
          rotate: 45,
          interval: 0,
          fontSize: 11,
          margin: 16,
        },
      },
      yAxis: {
        type: 'category',
        data: props.seniorityLevels,
        name: 'Seniority',
      },
      series: [
        {
          type: 'scatter',
          symbolSize: function (val) {
            return calculateBubbleSize(val[2])
          },
          data: scatterData,
          itemStyle: {
            color: function (params) {
              return colorPalette[params.dataIndex % colorPalette.length]
            },
            opacity: 0.7,
          },
        },
      ],
    }
  })
</script>
