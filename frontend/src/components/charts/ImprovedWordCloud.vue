<template>
  <div
    ref="wordCloudContainer"
    class="word-cloud-container"
    style="height: 350px; width: 100%"
  >
    <div
      v-if="loading"
      class="flex items-center justify-center h-full"
    >
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
    </div>
    <div
      v-else-if="error"
      class="flex items-center justify-center h-full"
    >
      <p class="text-red-500">
        {{ error }}
      </p>
    </div>
    <div
      v-else-if="!processedData.length"
      class="flex items-center justify-center h-full"
    >
      <p class="text-gray-500">
        No data available for word cloud
      </p>
    </div>
    <div
      v-else
      class="word-cloud h-full w-full"
    >
      <VChart
        :option="option"
        autoresize
      />
    </div>
  </div>
</template>

<script setup>
  import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
  import VChart from 'vue-echarts'
  import { use } from 'echarts/core'
  import { CanvasRenderer } from 'echarts/renderers'
  import 'echarts-wordcloud'

  // Register necessary ECharts components
  use([CanvasRenderer])

  const props = defineProps({
    data: { type: Array, required: true },
    loading: { type: Boolean, default: false },
    error: { type: String, default: null },
    maxWords: { type: Number, default: 100 },
    colorScheme: {
      type: Array,
      default: () => [
        '#3b82f6',
        '#10b981',
        '#f59e0b',
        '#ef4444',
        '#8b5cf6',
        '#06b6d4',
        '#84cc16',
        '#f97316',
      ],
    },
  })

  // Define refs first to avoid "Cannot access before initialization" error
  const wordCloudContainer = ref(null)
  const containerWidth = ref(0)
  const containerHeight = ref(0)

  // Process data to ensure consistent format and remove duplicates
  const processedData = computed(() => {
    if (!props.data || !Array.isArray(props.data) || props.data.length === 0) {
      return []
    }

    try {
      // Handle different data formats
      const formattedData = props.data
        .map((item) => {
          if (!item) {
            return null
          }

          // Handle format { skill: "...", skill_count: ... }
          if (item.skill !== undefined && item.skill_count !== undefined) {
            return {
              name: String(item.skill || ''),
              value: Number(item.skill_count || 0),
            }
          }
          // Handle format { name: "...", value: ... }
          else if (item.name !== undefined && item.value !== undefined) {
            return {
              name: String(item.name || ''),
              value: Number(item.value || 0),
            }
          }
          // Return null for invalid items
          return null
        })
        .filter(Boolean) // Remove null entries

      // Remove duplicates by creating a map with name as key
      // Keep the entry with the highest value when duplicates exist
      const uniqueDataMap = new Map()
      formattedData.forEach((item) => {
        if (
          item.name &&
          (!uniqueDataMap.has(item.name) || uniqueDataMap.get(item.name).value < item.value)
        ) {
          uniqueDataMap.set(item.name, item)
        }
      })

      // Convert map back to array, sort by value (descending) and limit to maxWords
      const result = Array.from(uniqueDataMap.values())
        .filter((item) => item.value > 0) // Only include items with positive values
        .sort((a, b) => b.value - a.value)
        .slice(0, props.maxWords)

      return result
    } catch (error) {
      console.error('Error processing word cloud data:', error)
      return []
    }
  })

  // Generate word cloud options
  const option = computed(() => {
    // Ensure data is unique before rendering
    const uniqueData = processedData.value

    return {
      series: [
        {
          type: 'wordCloud',
          shape: 'circle',
          left: 'center',
          top: 'center',
          width: '90%',
          height: '90%',
          right: null,
          bottom: null,
          sizeRange: [12, 60],
          rotationRange: [-45, 90],
          rotationStep: 15,
          gridSize: 8,
          drawOutOfBound: false,
          layoutAnimation: true,
          textStyle: {
            fontFamily: 'sans-serif',
            fontWeight: 'bold',
            color: function () {
              // Use the provided color scheme
              return props.colorScheme[Math.floor(Math.random() * props.colorScheme.length)]
            },
          },
          emphasis: {
            textStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.3)',
            },
          },
          data: uniqueData,
        },
      ],
    }
  })

  function updateContainerSize() {
    if (wordCloudContainer.value) {
      containerWidth.value = wordCloudContainer.value.clientWidth
      containerHeight.value = wordCloudContainer.value.clientHeight
    }
  }

  // Watch for key changes in parent component - AFTER ref definition
  watch(
    () => props.data,
    () => {
      // Force chart update when data changes
      if (wordCloudContainer.value) {
        updateContainerSize()
      }
    },
    { deep: true, immediate: true }
  )

  // Update container dimensions on mount and resize
  onMounted(() => {
    if (wordCloudContainer.value) {
      containerWidth.value = wordCloudContainer.value.clientWidth
      containerHeight.value = wordCloudContainer.value.clientHeight
    }

    window.addEventListener('resize', updateContainerSize)

    // Force a refresh after mounting
    setTimeout(() => {
      updateContainerSize()
    }, 100)
  })

  // Clean up event listener
  onUnmounted(() => {
    window.removeEventListener('resize', updateContainerSize)
  })
</script>

<style scoped>
  .word-cloud-container {
    position: relative;
  }
</style>
