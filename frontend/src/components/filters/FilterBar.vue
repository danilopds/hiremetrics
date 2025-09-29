<template>
  <div class="filter-bar">
    <div class="filter-group">
      <div class="filter-title">
        Cargo
      </div>
      <NSelect
        v-model:value="selectedPosition"
        :options="positionOptions"
        label="Cargo"
        class="filter-select"
        placeholder="Selecione um cargo"
        :render-label="customPlaceholder"
        filterable
        aria-label="Selecionar cargo"
        @update:value="onPositionChange"
      />
    </div>
    <div class="filter-group">
      <div class="filter-title">
        Cidade
      </div>
      <NSelect
        :key="`city-${selectedPosition.value}`"
        v-model:value="selectedCity"
        :options="cityOptions"
        label="Cidade"
        class="filter-select"
        :render-label="customPlaceholder"
        filterable
        aria-label="Selecionar cidade"
        @update:value="onFilterChange"
      />
    </div>
    <div class="filter-group">
      <div class="filter-title">
        Estado
      </div>
      <NSelect
        :key="`state-${selectedPosition.value}`"
        v-model:value="selectedState"
        :options="stateOptions"
        label="Estado"
        class="filter-select"
        :render-label="customPlaceholder"
        filterable
        aria-label="Selecionar estado"
        @update:value="onFilterChange"
      />
    </div>
    <div class="filter-group">
      <div class="filter-title">
        Remoto/Presencial
      </div>
      <NSelect
        v-model:value="selectedRemote"
        :options="remoteOptions"
        label="Remoto"
        class="filter-select"
        placeholder="Todos"
        aria-label="Selecionar tipo de trabalho"
        @update:value="onFilterChange"
      />
    </div>
    <div class="filter-actions">
      <button
        class="apply-btn"
        :disabled="!filtersChanged || loading"
        @click="applyFilters"
      >
        <span
          v-if="loading"
          class="spinner"
        />
        Aplicar Filtros
      </button>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch, computed, onMounted, nextTick } from 'vue'
  import { NSelect } from 'naive-ui'

  const props = defineProps({
    positions: { type: Array, default: () => [] },
    locations: { type: Array, default: () => [] },
    initialFilters: { type: Object, default: () => ({}) },
    loading: { type: Boolean, default: false },
  })

  const emit = defineEmits(['update:filters', 'position-change'])

  const positionOptions = computed(() =>
    props.positions
      .map((pos) => ({ label: pos, value: pos }))
      .filter((v, i, a) => v.value && a.findIndex((t) => t.value === v.value) === i)
      .sort((a, b) => a.label.localeCompare(b.label))
  )

  const cityOptions = computed(() => {
    const options = [
      { label: 'Todas', value: 'all' },
      ...props.locations
        .map((loc) => ({ label: loc.title, value: loc.title }))
        .filter((v, i, a) => v.value && a.findIndex((t) => t.value === v.value) === i)
        .sort((a, b) => a.label.localeCompare(b.label)),
    ]
    return options
  })

  const stateOptions = computed(() => {
    const options = [
      { label: 'Todos', value: 'all' },
      ...props.locations
        .map((loc) => ({ label: loc.state, value: loc.state }))
        .filter((v, i, a) => v.value && a.findIndex((t) => t.value === v.value) === i)
        .sort((a, b) => a.label.localeCompare(b.label)),
    ]
    return options
  })

  const remoteOptions = [
    { label: 'Todos', value: 'all' },
    { label: 'Remoto', value: 'true' },
    { label: 'Presencial', value: 'false' },
  ]

  const selectedPosition = ref(props.initialFilters.search_position_query ?? 'Data Engineer')
  const selectedCity = ref(props.initialFilters.job_city ?? 'all')
  const selectedState = ref(props.initialFilters.job_state ?? 'all')
  const selectedRemote = ref(props.initialFilters.job_is_remote ?? 'all')

  const lastAppliedFilters = ref({
    search_position_query: selectedPosition.value,
    job_city: selectedCity.value,
    job_state: selectedState.value,
    job_is_remote: selectedRemote.value,
  })

  const filtersChanged = computed(() => {
    return (
      selectedPosition.value !== lastAppliedFilters.value.search_position_query ||
      selectedCity.value !== lastAppliedFilters.value.job_city ||
      selectedState.value !== lastAppliedFilters.value.job_state ||
      selectedRemote.value !== lastAppliedFilters.value.job_is_remote
    )
  })

  async function onPositionChange() {
    // Emit position change to update city/state filters first
    emit('position-change', {
      search_position_query: selectedPosition.value,
    })

    // Wait for the next tick to ensure the options are updated
    await nextTick()

    // Reset city and state to 'All' after the options are updated
    selectedCity.value = 'all'
    selectedState.value = 'all'
  }

  function onFilterChange() {
    // No auto-emit; just track changes
  }

  function applyFilters() {
    lastAppliedFilters.value = {
      search_position_query: selectedPosition.value,
      job_city: selectedCity.value,
      job_state: selectedState.value,
      job_is_remote: selectedRemote.value,
    }
    emit('update:filters', {
      search_position_query: selectedPosition.value,
      job_city: selectedCity.value !== 'all' ? selectedCity.value : undefined,
      job_state: selectedState.value !== 'all' ? selectedState.value : undefined,
      job_is_remote: selectedRemote.value !== 'all' ? selectedRemote.value : undefined,
    })
  }

  // Keep local filter state in sync with parent
  watch(
    () => props.initialFilters,
    (newFilters) => {
      if (newFilters.search_position_query !== undefined) {
        selectedPosition.value = newFilters.search_position_query
      }
      if (newFilters.job_city !== undefined) {
        selectedCity.value = newFilters.job_city
      }
      if (newFilters.job_state !== undefined) {
        selectedState.value = newFilters.job_state
      }
      if (newFilters.job_is_remote !== undefined) {
        selectedRemote.value = newFilters.job_is_remote
      }
    },
    { deep: true }
  )

  // Set initial lastAppliedFilters on mount
  onMounted(() => {
    lastAppliedFilters.value = {
      search_position_query: selectedPosition.value,
      job_city: selectedCity.value,
      job_state: selectedState.value,
      job_is_remote: selectedRemote.value,
    }
  })

  // Add a custom placeholder renderer for better color
  function customPlaceholder(option) {
    return option.label
  }
</script>

<style scoped>
  .filter-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr) auto;
    gap: 1rem;
    align-items: end;
    background: white;
    padding: 1rem;
    border-radius: 0.75rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    margin-bottom: 1.5rem;
  }

  @media (max-width: 1200px) {
    .filter-bar {
      grid-template-columns: repeat(3, 1fr) auto;
    }
  }

  @media (max-width: 1024px) {
    .filter-bar {
      grid-template-columns: repeat(2, 1fr) auto;
    }
  }

  @media (max-width: 768px) {
    .filter-bar {
      grid-template-columns: 1fr;
      gap: 0.75rem;
    }

    .filter-actions {
      padding-top: 0.5rem;
    }

    .apply-btn {
      width: 100%;
      justify-content: center;
    }
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
    margin-bottom: 0.25rem;
    letter-spacing: 0.01em;
  }
  .filter-select {
    width: 100%;
    min-width: 0;
    max-width: 100%;
  }
  .filter-actions {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    height: 100%;
    padding-top: 1.5rem;
  }
  .apply-btn {
    background: #2563eb;
    color: #fff;
    border: none;
    border-radius: 0.375rem;
    padding: 0.5rem 1.25rem;
    font-weight: 600;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s;
    display: flex;
    align-items: center;
  }
  .apply-btn:disabled {
    background: #a5b4fc;
    cursor: not-allowed;
  }
  .spinner {
    border: 2px solid #fff;
    border-top: 2px solid #2563eb;
    border-radius: 50%;
    width: 1em;
    height: 1em;
    margin-right: 0.5em;
    animation: spin 1s linear infinite;
  }
  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
  :deep(.n-base-selection-placeholder) {
    color: #222 !important;
    opacity: 1 !important;
  }
</style>
