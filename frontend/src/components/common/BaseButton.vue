<template>
  <button
    :type="type"
    :class="buttonClasses"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <span
      v-if="loading"
      class="inline-block mr-2"
    >
      <svg
        class="animate-spin h-4 w-4"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        />
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
    </span>
    <slot />
  </button>
</template>

<script setup>
  import { computed } from 'vue'

  /**
   * Button component with different variants and states
   * @displayName BaseButton
   */

  const props = defineProps({
    /**
     * Button type attribute
     */
    type: {
      type: String,
      default: 'button',
      validator: (value) => ['button', 'submit', 'reset'].includes(value),
    },
    /**
     * Button variant
     */
    variant: {
      type: String,
      default: 'primary',
      validator: (value) => ['primary', 'secondary', 'outline', 'danger', 'text'].includes(value),
    },
    /**
     * Button size
     */
    size: {
      type: String,
      default: 'md',
      validator: (value) => ['sm', 'md', 'lg'].includes(value),
    },
    /**
     * Whether the button is disabled
     */
    disabled: {
      type: Boolean,
      default: false,
    },
    /**
     * Whether the button is in loading state
     */
    loading: {
      type: Boolean,
      default: false,
    },
    /**
     * Whether the button should take full width
     */
    block: {
      type: Boolean,
      default: false,
    },
    /**
     * Whether the button should have rounded corners
     */
    rounded: {
      type: Boolean,
      default: false,
    },
  })

  const emit = defineEmits(['click'])

  /**
   * Computed classes based on props
   */
  const buttonClasses = computed(() => {
    const baseClasses =
      'inline-flex items-center justify-center font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2'

    // Size classes
    const sizeClasses = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
    }

    // Variant classes
    const variantClasses = {
      primary: 'bg-primary-600 hover:bg-primary-700 text-white focus:ring-primary-500',
      secondary: 'bg-gray-600 hover:bg-gray-700 text-white focus:ring-gray-500',
      outline:
        'border border-primary-600 text-primary-600 hover:bg-primary-50 focus:ring-primary-500',
      danger: 'bg-red-600 hover:bg-red-700 text-white focus:ring-red-500',
      text: 'text-primary-600 hover:text-primary-700 hover:bg-primary-50 focus:ring-primary-500',
    }

    // Disabled classes
    const disabledClasses =
      props.disabled || props.loading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'

    // Block class
    const blockClass = props.block ? 'w-full' : ''

    // Rounded class
    const roundedClass = props.rounded ? 'rounded-full' : 'rounded-md'

    return [
      baseClasses,
      sizeClasses[props.size],
      variantClasses[props.variant],
      disabledClasses,
      blockClass,
      roundedClass,
    ]
  })

  /**
   * Handle click event
   */
  const handleClick = (event) => {
    if (!props.disabled && !props.loading) {
      emit('click', event)
    }
  }
</script>
