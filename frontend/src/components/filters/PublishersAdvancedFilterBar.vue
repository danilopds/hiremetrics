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
        filterable
        aria-label="Selecionar cargo"
        @update:value="onPositionChange"
      />
    </div>
    <div class="filter-group">
      <div class="filter-title">
        Canal de Publicação
      </div>
      <NSelect
        v-model:value="selectedPublisher"
        :options="publisherOptions"
        label="Canal de Publicação"
        class="filter-select"
        placeholder="Selecione um canal"
        :render-label="customPlaceholder"
        filterable
        clearable
        aria-label="Selecionar canal de publicação"
        @update:value="onFilterChange"
      />
    </div>
    <div class="filter-group">
      <div class="filter-title">
        Senioridade
      </div>
      <NSelect
        v-model:value="selectedSeniority"
        :options="seniorityOptions"
        label="Senioridade"
        class="filter-select"
        placeholder="Selecionar senioridade"
        :render-label="customPlaceholder"
        filterable
        clearable
        aria-label="Selecionar senioridade"
        @update:value="onFilterChange"
      />
    </div>
    <div class="filter-group">
      <div class="filter-title">
        Empresa
      </div>
      <NSelect
        v-model:value="selectedCompany"
        :options="companyOptions"
        label="Empresa"
        class="filter-select"
        placeholder="Selecione uma empresa"
        :render-label="customPlaceholder"
        filterable
        clearable
        aria-label="Selecionar empresa"
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
        placeholder="Remoto/Presencial"
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
  import { ref, watch, computed, onMounted } from 'vue'
  import { NSelect } from 'naive-ui'

  const props = defineProps({
    positions: { type: Array, default: () => [] },
    publishers: { type: Array, default: () => [] },
    seniorityLevels: { type: Array, default: () => [] },
    companies: { type: Array, default: () => [] },
    initialFilters: { type: Object, default: () => ({}) },
    loading: { type: Boolean, default: false },
  })

  const emit = defineEmits(['update:filters', 'position-change'])

  const positionOptions = computed(() => props.positions.map((pos) => ({ label: pos, value: pos })))

  const publisherOptions = computed(() => [
    { label: 'Todos', value: 'all' },
    ...props.publishers
      .map((publisher) => ({ label: publisher, value: publisher }))
      .filter((v, i, a) => v.value && a.findIndex((t) => t.value === v.value) === i)
      .sort((a, b) => a.label.localeCompare(b.label)),
  ])

  const seniorityOptions = computed(() => [
    { label: 'Todas', value: 'all' },
    ...props.seniorityLevels
      .map((level) => ({ label: level, value: level }))
      .filter((v, i, a) => v.value && a.findIndex((t) => t.value === v.value) === i),
  ])

  const companyOptions = computed(() => [
    { label: 'Todas', value: 'all' },
    ...props.companies
      .map((company) => ({ label: company, value: company }))
      .filter((v, i, a) => v.value && a.findIndex((t) => t.value === v.value) === i)
      .sort((a, b) => a.label.localeCompare(b.label)),
  ])

  const remoteOptions = [
    { label: 'Todos', value: 'all' },
    { label: 'Remoto', value: 'true' },
    { label: 'Presencial', value: 'false' },
  ]

  const selectedPosition = ref(props.initialFilters.search_position_query ?? 'Data Engineer')
  const selectedPublisher = ref(props.initialFilters.publisher ?? 'all')
  const selectedSeniority = ref(props.initialFilters.seniority ?? 'all')
  const selectedCompany = ref(props.initialFilters.company ?? 'all')
  const selectedRemote = ref(props.initialFilters.remote ?? 'all')

  const lastAppliedFilters = ref({
    search_position_query: selectedPosition.value,
    publisher: selectedPublisher.value,
    seniority: selectedSeniority.value,
    company: selectedCompany.value,
    remote: selectedRemote.value,
  })

  const filtersChanged = computed(() => {
    const currentFilters = {
      search_position_query: selectedPosition.value,
      publisher: selectedPublisher.value,
      seniority: selectedSeniority.value,
      company: selectedCompany.value,
      remote: selectedRemote.value,
    }

    const lastFilters = lastAppliedFilters.value

    // Check if position changed
    if (currentFilters.search_position_query !== lastFilters.search_position_query) {
      console.log(
        'Position changed:',
        currentFilters.search_position_query,
        'vs',
        lastFilters.search_position_query
      )
      return true
    }

    // Check if publisher changed
    if (currentFilters.publisher !== lastFilters.publisher) {
      console.log('Publisher changed:', currentFilters.publisher, 'vs', lastFilters.publisher)
      return true
    }

    // Check if seniority changed
    if (currentFilters.seniority !== lastFilters.seniority) {
      console.log('Seniority changed:', currentFilters.seniority, 'vs', lastFilters.seniority)
      return true
    }

    // Check if company changed
    if (currentFilters.company !== lastFilters.company) {
      console.log('Company changed:', currentFilters.company, 'vs', lastFilters.company)
      return true
    }

    // Check if remote changed
    if (currentFilters.remote !== lastFilters.remote) {
      console.log('Remote changed:', currentFilters.remote, 'vs', lastFilters.remote)
      return true
    }

    return false
  })

  function onFilterChange() {
    // No auto-emit; just track changes
  }

  function onPositionChange() {
    // Reset publisher, seniority, company, and remote when position changes
    selectedPublisher.value = 'all'
    selectedSeniority.value = 'all'
    selectedCompany.value = 'all'
    selectedRemote.value = 'all'

    // Don't update lastAppliedFilters here - let the user click Apply Filters
    // This ensures the Apply button remains enabled

    // Emit position change event for parent to handle
    emit('position-change', selectedPosition.value)
  }

  function applyFilters() {
    lastAppliedFilters.value = {
      search_position_query: selectedPosition.value,
      publisher: selectedPublisher.value,
      seniority: selectedSeniority.value,
      company: selectedCompany.value,
      remote: selectedRemote.value,
    }
    emit('update:filters', {
      search_position_query: selectedPosition.value,
      publisher: selectedPublisher.value !== 'all' ? selectedPublisher.value : undefined,
      seniority: selectedSeniority.value !== 'all' ? selectedSeniority.value : undefined,
      company: selectedCompany.value !== 'all' ? selectedCompany.value : undefined,
      remote: selectedRemote.value !== 'all' ? selectedRemote.value : undefined,
    })
  }

  // Keep local filter state in sync with parent
  watch(
    () => props.initialFilters,
    (newFilters) => {
      if (newFilters.search_position_query !== undefined) {
        selectedPosition.value = newFilters.search_position_query
      }
      if (newFilters.publisher !== undefined) {
        selectedPublisher.value = newFilters.publisher
      }
      if (newFilters.seniority !== undefined) {
        selectedSeniority.value = newFilters.seniority
      }
      if (newFilters.company !== undefined) {
        selectedCompany.value = newFilters.company
      }
      if (newFilters.remote !== undefined) {
        selectedRemote.value = newFilters.remote
      }

      // Handle undefined values (when filters are reset)
      if (newFilters.publisher === undefined) {
        selectedPublisher.value = 'all'
      }
      if (newFilters.seniority === undefined) {
        selectedSeniority.value = 'all'
      }
      if (newFilters.company === undefined) {
        selectedCompany.value = 'all'
      }
      if (newFilters.remote === undefined) {
        selectedRemote.value = 'all'
      }

      // Only update lastAppliedFilters if this is not a position change
      // (position changes should keep the Apply button enabled)
      if (newFilters.search_position_query === lastAppliedFilters.value.search_position_query) {
        lastAppliedFilters.value = {
          search_position_query: selectedPosition.value,
          publisher: selectedPublisher.value,
          seniority: selectedSeniority.value,
          company: selectedCompany.value,
          remote: selectedRemote.value,
        }
      }
    },
    { deep: true }
  )

  // Set last applied filters only once on mount
  onMounted(() => {
    lastAppliedFilters.value = {
      search_position_query: selectedPosition.value,
      publisher: selectedPublisher.value,
      seniority: selectedSeniority.value,
      company: selectedCompany.value,
      remote: selectedRemote.value,
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
    grid-template-columns: repeat(5, 1fr) auto;
    gap: 1rem;
    align-items: end;
    background: white;
    padding: 1rem;
    border-radius: 0.75rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    margin-bottom: 1.5rem;
  }

  @media (max-width: 1400px) {
    .filter-bar {
      grid-template-columns: repeat(4, 1fr) auto;
    }
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
</style>
