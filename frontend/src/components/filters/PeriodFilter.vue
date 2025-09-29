<template>
  <div class="period-filter">
    <div class="filter-group">
      <div class="filter-title">
        Período
      </div>
      <div class="period-buttons">
        <button
          v-for="option in periodOptions"
          :key="option.value"
          class="period-btn"
          :class="{ active: selectedPeriod === option.value }"
          @click="onPeriodClick(option.value)"
        >
          {{ option.label }}
        </button>
      </div>
    </div>
    <div class="filter-group">
      <div class="filter-title">
        Data Inicial
      </div>
      <input
        id="custom-date-from"
        v-model="customDateFrom"
        name="customDateFrom"
        type="date"
        class="date-input"
        :disabled="selectedPeriod !== 'custom'"
        @change="onCustomDateChange"
      >
    </div>
    <div class="filter-group">
      <div class="filter-title">
        Data Final
      </div>
      <input
        id="custom-date-to"
        v-model="customDateTo"
        name="customDateTo"
        type="date"
        class="date-input"
        :disabled="selectedPeriod !== 'custom'"
        @change="onCustomDateChange"
      >
    </div>
  </div>
</template>

<script setup>
  import { ref, watch, onMounted, nextTick } from 'vue'

  const props = defineProps({
    filters: { type: Object, default: () => ({}) },
    loading: { type: Boolean, default: false },
    defaultPeriod: { type: String, default: 'last30days' },
  })

  const emit = defineEmits(['period-change'])

  const periodOptions = [
    { label: 'Últimos 7 dias', value: 'last7days' },
    { label: 'Últimos 30 dias', value: 'last30days' },
    { label: 'Este mês', value: 'thisMonth' },
    { label: 'Mês passado', value: 'lastMonth' },
    { label: 'Período personalizado', value: 'custom' },
  ]

  const selectedPeriod = ref('')
  const customDateFrom = ref('')
  const customDateTo = ref('')
  const isInitialized = ref(false)

  function getDateRangeForPeriod(period) {
    const end = new Date()
    const start = new Date()

    switch (period) {
      case 'last7days':
        start.setDate(start.getDate() - 7)
        break
      case 'last30days':
        start.setDate(start.getDate() - 30)
        break
      case 'last90days':
        start.setDate(start.getDate() - 90)
        break
      case 'thisMonth':
        start.setDate(1)
        break
      case 'lastMonth':
        start.setMonth(start.getMonth() - 1)
        start.setDate(1)
        end.setDate(0)
        break
      default:
        return { dateFrom: null, dateTo: null }
    }

    return {
      dateFrom: start.toISOString().split('T')[0],
      dateTo: end.toISOString().split('T')[0],
    }
  }

  async function onPeriodClick(period) {
    // Force reactivity update
    selectedPeriod.value = period

    if (period !== 'custom') {
      const dates = getDateRangeForPeriod(period)
      customDateFrom.value = dates.dateFrom
      customDateTo.value = dates.dateTo
    }

    // Wait for DOM update before applying filters
    await nextTick()

    // Only apply filters if component is initialized
    if (isInitialized.value) {
      applyFilters()
    }
  }

  function onCustomDateChange() {
    if (selectedPeriod.value === 'custom' && isInitialized.value) {
      applyFilters()
    }
  }

  function applyFilters() {
    const dateFrom =
      selectedPeriod.value === 'custom'
        ? customDateFrom.value
        : getDateRangeForPeriod(selectedPeriod.value).dateFrom
    const dateTo =
      selectedPeriod.value === 'custom'
        ? customDateTo.value
        : getDateRangeForPeriod(selectedPeriod.value).dateTo

    const filters = {
      dateFrom,
      dateTo,
      period: selectedPeriod.value,
    }

    // Remove null/empty values
    Object.keys(filters).forEach((key) => {
      if (!filters[key]) {
        delete filters[key]
      }
    })

    emit('period-change', filters)
  }

  // Initialize component based on filters or default
  onMounted(() => {
    initializeFilter()
  })

  function initializeFilter() {
    // Check if we have period in filters, otherwise use default
    const periodToUse = props.filters?.period || props.defaultPeriod

    // Set the selected period
    selectedPeriod.value = periodToUse

    // Set the date range based on period or use existing dates from filters
    if (props.filters?.dateFrom && props.filters?.dateTo) {
      // Use existing dates
      customDateFrom.value = props.filters.dateFrom
      customDateTo.value = props.filters.dateTo

      // If no explicit period is provided but we have dates, try to match with a preset
      if (!props.filters.period) {
        const matchingPeriod = findMatchingPeriod(props.filters.dateFrom, props.filters.dateTo)
        if (matchingPeriod) {
          selectedPeriod.value = matchingPeriod
        } else {
          selectedPeriod.value = 'custom'
        }
      }
    } else {
      // Calculate dates based on period
      const dates = getDateRangeForPeriod(periodToUse)
      customDateFrom.value = dates.dateFrom
      customDateTo.value = dates.dateTo
    }

    // Mark component as initialized
    isInitialized.value = true
  }

  // Watch for changes in filters
  watch(
    () => props.filters,
    (newFilters, oldFilters) => {
      if (!newFilters || !isInitialized.value) {
        return
      }

      // Prevent processing identical filters
      if (oldFilters && JSON.stringify(newFilters) === JSON.stringify(oldFilters)) {
        return
      }

      if (newFilters.period && newFilters.period !== selectedPeriod.value) {
        // Direct period change from outside
        selectedPeriod.value = newFilters.period

        // Update dates if this is a preset period
        if (newFilters.period !== 'custom') {
          const dates = getDateRangeForPeriod(newFilters.period)
          customDateFrom.value = dates.dateFrom
          customDateTo.value = dates.dateTo
        }
      } else if (newFilters.dateFrom && newFilters.dateTo) {
        // Only date change, not period
        const datesChanged =
          customDateFrom.value !== newFilters.dateFrom || customDateTo.value !== newFilters.dateTo

        if (datesChanged) {
          customDateFrom.value = newFilters.dateFrom
          customDateTo.value = newFilters.dateTo

          // Check if dates match any preset period
          const matchingPeriod = findMatchingPeriod(newFilters.dateFrom, newFilters.dateTo)
          if (matchingPeriod && selectedPeriod.value !== matchingPeriod) {
            selectedPeriod.value = matchingPeriod
          } else if (!matchingPeriod && selectedPeriod.value !== 'custom') {
            selectedPeriod.value = 'custom'
          }
        }
      }
    },
    { deep: true, immediate: true }
  )

  // Helper function to find a period that matches date range
  function findMatchingPeriod(dateFrom, dateTo) {
    for (const option of periodOptions) {
      if (option.value === 'custom') {
        continue
      }

      const dates = getDateRangeForPeriod(option.value)
      if (dates.dateFrom === dateFrom && dates.dateTo === dateTo) {
        return option.value
      }
    }
    return null
  }
</script>

<style scoped>
  .period-filter {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 1rem;
    align-items: start;
    background: white;
    padding: 1rem;
    border-radius: 0.75rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    margin-bottom: 1.5rem;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    align-items: stretch;
  }

  .filter-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #555;
    margin-bottom: 0.5rem;
    letter-spacing: 0.01em;
  }

  .period-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .period-btn {
    padding: 0.5rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    background: white;
    color: #374151;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    white-space: nowrap;
  }

  .period-btn:hover {
    border-color: #3b82f6;
    background: #eff6ff;
    color: #1d4ed8;
  }

  .period-btn.active {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
  }

  .period-btn.active:hover {
    background: #2563eb;
    border-color: #2563eb;
  }

  .date-input {
    padding: 0.5rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    transition: border-color 0.2s;
    background-color: white;
  }

  .date-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .date-input:disabled {
    background-color: #f9fafb;
    color: #6b7280;
    cursor: not-allowed;
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .period-filter {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .period-buttons {
      justify-content: flex-start;
    }

    .period-btn {
      flex: 0 0 auto;
      min-width: fit-content;
    }
  }
</style>
