<template>
  <VChart
    :option="option"
    autoresize
    style="height: 350px; width: 100%"
  />
</template>

<script setup>
  import { computed } from 'vue'
  import VChart from 'vue-echarts'
  import { use } from 'echarts/core'
  import { CanvasRenderer } from 'echarts/renderers'
  import 'echarts-wordcloud'

  // Register necessary ECharts components
  use([CanvasRenderer])

  const props = defineProps({
    data: { type: Array, required: true },
  })

  const option = computed(() => ({
    series: [
      {
        type: 'wordCloud',
        shape: 'circle',
        left: 'center',
        top: 'center',
        width: '100%',
        height: '100%',
        sizeRange: [12, 60],
        rotationRange: [-45, 90],
        gridSize: 8,
        drawOutOfBound: false,
        textStyle: {
          fontFamily: 'sans-serif',
          fontWeight: 'bold',
          color: () => `hsl(${Math.round(Math.random() * 360)}, 70%, 50%)`,
        },
        data: props.data.map((item) => ({
          name: item.skill,
          value: item.skill_count,
        })),
      },
    ],
  }))
</script>
