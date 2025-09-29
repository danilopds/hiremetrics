<template>
  <div class="flex-1 bg-white shadow rounded-lg p-6 flex items-center">
    <div class="flex-shrink-0">
      <span
        class="inline-flex items-center justify-center h-12 w-12 rounded-full"
        :class="bgColorClass"
      >
        <slot name="icon">
          <i :class="[icon, 'text-2xl', iconColorClass]" />
        </slot>
      </span>
    </div>
    <div class="ml-4">
      <div class="text-gray-500 text-sm font-medium">
        {{ title }}
      </div>
      <div class="text-2xl font-bold">
        {{ value }}
      </div>
      <div
        v-if="subtitle"
        :class="['text-lg', textColorClass]"
      >
        {{ subtitle }}
      </div>
      <slot name="trend" />
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
    value: {
      type: [String, Number],
      required: true,
    },
    subtitle: {
      type: String,
      default: '',
    },
    icon: {
      type: String,
      default: 'fas fa-chart-bar',
    },
    color: {
      type: String,
      default: 'blue', // blue, green, yellow, red, purple
    },
  })

  const colorMap = {
    blue: {
      bg: 'bg-blue-100',
      text: 'text-blue-700',
      icon: 'text-blue-600',
    },
    green: {
      bg: 'bg-green-100',
      text: 'text-green-700',
      icon: 'text-green-600',
    },
    yellow: {
      bg: 'bg-yellow-100',
      text: 'text-yellow-700',
      icon: 'text-yellow-600',
    },
    red: {
      bg: 'bg-red-100',
      text: 'text-red-700',
      icon: 'text-red-600',
    },
    purple: {
      bg: 'bg-purple-100',
      text: 'text-purple-700',
      icon: 'text-purple-600',
    },
  }

  const bgColorClass = computed(() => colorMap[props.color]?.bg || 'bg-blue-100')
  const textColorClass = computed(() => colorMap[props.color]?.text || 'text-blue-700')
  const iconColorClass = computed(() => colorMap[props.color]?.icon || 'text-blue-600')
</script>
