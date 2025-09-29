<template>
  <div class="mt-8">
    <div class="bg-white shadow rounded-lg p-6">
      <div class="mb-3">
        <h3 class="text-lg font-medium text-gray-900">
          {{ title }}
        </h3>
        <p
          v-if="description"
          class="text-sm text-gray-500 mt-1"
        >
          {{ description }}
        </p>
      </div>
      <div
        v-if="loading"
        class="h-80 flex items-center justify-center"
      >
        <p class="text-center text-gray-500">
          Loading chart data...
        </p>
      </div>
      <div
        v-else-if="error"
        class="h-80 flex items-center justify-center"
      >
        <p class="text-center text-red-500">
          {{ error }}
        </p>
      </div>
      <div
        v-else-if="!hasData"
        class="h-80 flex items-center justify-center"
      >
        <p class="text-center text-gray-500">
          No data available for the selected filters
        </p>
      </div>
      <div
        v-else
        :class="contentClass"
        :style="contentStyle"
      >
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
  import { computed } from 'vue'

  const props = defineProps({
    title: {
      type: String,
      required: true,
    },
    description: {
      type: String,
      default: '',
    },
    loading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: [String, null],
      default: null,
    },
    hasData: {
      type: Boolean,
      default: true,
    },
    height: {
      type: String,
      default: 'h-80',
    },
    contentClass: {
      type: String,
      default: 'h-80',
    },
    minHeight: {
      type: String,
      default: '320px',
    },
    overflow: {
      type: String,
      default: 'visible',
    },
  })

  const contentStyle = computed(() => {
    return {
      minHeight: props.minHeight,
      overflow: props.overflow,
      marginBottom: '0px',
    }
  })
</script>
