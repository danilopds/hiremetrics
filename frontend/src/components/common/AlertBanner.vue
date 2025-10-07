<template>
  <div
    v-if="!isDismissed"
    class="alert-banner"
    :class="bannerClasses"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between py-2.5">
        <!-- Banner Content -->
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <i
              :class="iconClass"
              class="text-base"
            />
          </div>
          <div class="ml-2.5">
            <!-- eslint-disable vue/no-v-html -->
            <p
              class="text-xs font-medium"
              :class="textClass"
              v-html="message"
            />
            <!-- eslint-enable vue/no-v-html -->
            <!-- Note: v-html is used here for controlled HTML content from parent components -->
          </div>
        </div>

        <!-- Close Button (only shown if dismissible) -->
        <div
          v-if="dismissible"
          class="flex-shrink-0"
        >
          <button
            class="close-btn"
            :class="closeButtonClass"
            aria-label="Fechar banner"
            @click="dismissBanner"
          >
            <i class="fas fa-times" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, computed } from 'vue'

  const props = defineProps({
    message: {
      type: String,
      default: 'Esta é uma mensagem de exemplo. Você pode personalizá-la conforme necessário.',
    },
    type: {
      type: String,
      default: 'info', // info, success, warning, error
      validator: (value) => ['info', 'success', 'warning', 'error'].includes(value),
    },
    dismissible: {
      type: Boolean,
      default: true,
    },
    persistDismissal: {
      type: Boolean,
      default: false, // Don't persist dismissal - show again on next login
    },
    storageKey: {
      type: String,
      default: 'alert-banner-dismissed',
    },
  })

  const emit = defineEmits(['dismissed'])

  // Check if banner was previously dismissed
  // Use sessionStorage for session-based dismissal, localStorage for persistent dismissal
  const isDismissed = ref(
    props.persistDismissal
      ? localStorage.getItem(props.storageKey) === 'true'
      : sessionStorage.getItem(props.storageKey) === 'true'
  )

  // Computed classes based on banner type
  const bannerClasses = computed(() => {
    const baseClasses = 'alert-banner border-t border-b'
    const typeClasses = {
      info: 'bg-blue-50 border-blue-200',
      success: 'bg-green-50 border-green-200',
      warning: 'bg-yellow-50 border-yellow-200',
      error: 'bg-red-50 border-red-200',
    }
    return `${baseClasses} ${typeClasses[props.type]}`
  })

  const iconClass = computed(() => {
    const iconMap = {
      info: 'fas fa-info-circle text-blue-500',
      success: 'fas fa-check-circle text-green-500',
      warning: 'fas fa-exclamation-triangle text-yellow-500',
      error: 'fas fa-exclamation-circle text-red-500',
    }
    return iconMap[props.type]
  })

  const textClass = computed(() => {
    const textMap = {
      info: 'text-blue-800',
      success: 'text-green-800',
      warning: 'text-yellow-800',
      error: 'text-red-800',
    }
    return textMap[props.type]
  })

  const closeButtonClass = computed(() => {
    const buttonMap = {
      info: 'text-blue-400 hover:text-blue-600',
      success: 'text-green-400 hover:text-green-600',
      warning: 'text-yellow-400 hover:text-yellow-600',
      error: 'text-red-400 hover:text-red-600',
    }
    return buttonMap[props.type]
  })

  // Dismiss banner
  const dismissBanner = () => {
    isDismissed.value = true

    // Store dismissal based on persistence setting
    if (props.persistDismissal) {
      localStorage.setItem(props.storageKey, 'true')
    } else {
      // Use sessionStorage for session-based dismissal
      sessionStorage.setItem(props.storageKey, 'true')
    }

    emit('dismissed')
  }

  // Method to show banner again (useful for programmatic control)
  const showBanner = () => {
    isDismissed.value = false
    if (props.persistDismissal) {
      localStorage.removeItem(props.storageKey)
    } else {
      sessionStorage.removeItem(props.storageKey)
    }
  }

  // Expose methods for parent components
  defineExpose({
    showBanner,
    dismissBanner,
  })
</script>

<style scoped>
  .alert-banner {
    position: sticky;
    top: 64px; /* Height of navbar (h-16 = 64px) */
    left: 0;
    right: 0;
    z-index: 40; /* Below navigation but above page content */
    transition: all 0.3s ease-in-out;
  }

  .close-btn {
    padding: 0.125rem;
    border-radius: 0.25rem;
    background: transparent;
    border: none;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 1.25rem;
    height: 1.25rem;
    font-size: 0.75rem;
  }

  .close-btn:hover {
    background: rgba(0, 0, 0, 0.1);
  }

  .close-btn:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5);
  }

  /* Smooth slide down animation */
  .alert-banner {
    animation: slideDown 0.3s ease-out;
  }

  @keyframes slideDown {
    from {
      transform: translateY(-100%);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  /* Responsive design */
  @media (max-width: 640px) {
    .alert-banner {
      padding-left: 0.75rem;
      padding-right: 0.75rem;
    }

    .close-btn {
      margin-left: 0.375rem;
    }
  }
</style>
