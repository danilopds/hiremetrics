# Frontend Style Guide

This document outlines the styling and coding conventions for the HireMetrics frontend codebase.

## Component Structure

### Naming Conventions

- Use **PascalCase** for component filenames (e.g., `BaseButton.vue`, `FilterBar.vue`)
- Use **camelCase** for instance names, methods, and variables
- Use **kebab-case** for custom events and props in templates

### Component Organization

```vue
<script setup>
// 1. Imports - organized by type
import { ref, computed, onMounted } from 'vue'
import { useStore } from '@/stores/example'
import BaseComponent from '@/components/common/BaseComponent.vue'

// 2. Props
const props = defineProps({
  title: {
    type: String,
    required: true
  },
  items: {
    type: Array,
    default: () => []
  }
})

// 3. Emits
const emit = defineEmits(['update', 'select'])

// 4. State variables
const isLoading = ref(false)
const selectedItem = ref(null)

// 5. Computed properties
const filteredItems = computed(() => {
  return props.items.filter(item => item.active)
})

// 6. Methods
const handleSelect = (item) => {
  selectedItem.value = item
  emit('select', item)
}

// 7. Lifecycle hooks
onMounted(() => {
  // initialization logic
})
</script>

<template>
  <div class="component-container">
    <h2 class="title">{{ title }}</h2>
    <div v-if="isLoading" class="loading-indicator">Loading...</div>
    <ul v-else class="item-list">
      <li 
        v-for="item in filteredItems" 
        :key="item.id" 
        class="item"
        :class="{ 'item-selected': item === selectedItem }"
        @click="handleSelect(item)"
      >
        {{ item.name }}
      </li>
    </ul>
  </div>
</template>
```

## CSS/Styling Guidelines

### Using Tailwind CSS

- Prefer Tailwind utility classes for styling
- Use consistent spacing utilities (`p-4`, `m-2`, etc.)
- Extract common patterns to component classes when repeated

### Custom CSS

- When custom CSS is needed, use scoped styles
- Follow the BEM (Block Element Modifier) naming convention
- Use CSS variables for theme colors and consistent values

```vue
<style scoped>
.component-container {
  /* Component-specific styles */
}

.component-container__header {
  /* Element styles */
}

.component-container--highlighted {
  /* Modifier styles */
}
</style>
```

### Color System

Use our defined color palette through Tailwind classes:

- Primary: `text-primary-600`, `bg-primary-100`, etc.
- Neutral: `text-gray-800`, `bg-gray-100`, etc.
- Success: `text-green-600`, `bg-green-100`, etc.
- Warning: `text-yellow-600`, `bg-yellow-100`, etc.
- Error: `text-red-600`, `bg-red-100`, etc.

## Layout & Spacing

- Use consistent spacing with Tailwind's spacing scale
- Use responsive design utilities (`sm:`, `md:`, `lg:`, `xl:`)
- Follow a 4px/8px grid system for spacing

## Component Best Practices

1. Keep components focused on a single responsibility
2. Extract reusable logic to composables
3. Use props for data input and events for data output
4. Avoid direct DOM manipulation
5. Use slots for flexible content composition

## Chart Components

- Use consistent chart configuration
- Extract common chart options to utilities
- Use the same color palette across all charts
- Ensure responsive behavior for all chart types

## Form Components

- Use consistent validation patterns
- Provide clear error messages
- Use consistent input styling
- Support keyboard navigation

## Icons & Assets

- Use SVG icons when possible
- Follow naming conventions for assets
- Optimize images for web

## Accessibility

- Use semantic HTML elements
- Include proper ARIA attributes
- Ensure keyboard navigation works
- Maintain sufficient color contrast
