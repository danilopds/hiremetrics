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
        Skills
      </div>
      <NSelect
        v-model:value="selectedSkills"
        :options="skillOptions"
        label="Skills"
        class="filter-select"
        multiple
        filterable
        :loading="loading"
        placeholder="Buscar skills..."
        :filter="handleSkillFilter"
        aria-label="Selecionar skills"
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
        clearable
        placeholder="Todos"
        aria-label="Selecionar senioridade"
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
    skills: { type: Array, default: () => [] },
    seniorityLevels: { type: Array, default: () => [] },
    initialFilters: { type: Object, default: () => ({}) },
    loading: { type: Boolean, default: false },
  })

  const emit = defineEmits(['update:filters', 'position-change'])

  const positionOptions = computed(() => props.positions.map((pos) => ({ label: pos, value: pos })))

  const skillOptions = computed(() => props.skills.map((skill) => ({ label: skill, value: skill })))

  const seniorityOptions = computed(() =>
    props.seniorityLevels.map((sen) => ({ label: sen, value: sen }))
  )

  const selectedPosition = ref(props.initialFilters.search_position_query ?? 'Data Engineer')
  const selectedSkills = ref(props.initialFilters.selectedSkills || [])
  const selectedSeniority = ref(props.initialFilters.selectedSeniority || null)

  const lastAppliedFilters = ref({
    search_position_query: null,
    selectedSkills: [],
    selectedSeniority: null,
  })

  const filtersChanged = computed(() => {
    const currentFilters = {
      search_position_query: selectedPosition.value,
      selectedSkills: selectedSkills.value,
      selectedSeniority: selectedSeniority.value,
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

    // Check if seniority changed
    if (currentFilters.selectedSeniority !== lastFilters.selectedSeniority) {
      console.log(
        'Seniority changed:',
        currentFilters.selectedSeniority,
        'vs',
        lastFilters.selectedSeniority
      )
      return true
    }

    // Check if selected skills changed (deep comparison)
    if (currentFilters.selectedSkills.length !== lastFilters.selectedSkills.length) {
      console.log(
        'Skills length changed:',
        currentFilters.selectedSkills.length,
        'vs',
        lastFilters.selectedSkills.length
      )
      return true
    }

    // Check if skills arrays have different content
    const currentSkillsSet = new Set(currentFilters.selectedSkills)
    const lastSkillsSet = new Set(lastFilters.selectedSkills)

    for (const skill of currentSkillsSet) {
      if (!lastSkillsSet.has(skill)) {
        console.log('New skill added:', skill)
        return true
      }
    }

    for (const skill of lastSkillsSet) {
      if (!currentSkillsSet.has(skill)) {
        console.log('Skill removed:', skill)
        return true
      }
    }

    return false
  })

  function handleSkillFilter(pattern, option) {
    if (!pattern) {
      return true
    }
    return option.label.toLowerCase().includes(pattern.toLowerCase())
  }

  function onFilterChange() {
    // No auto-emit; just track changes
  }

  function onPositionChange() {
    // Reset skills and seniority when position changes
    selectedSkills.value = []
    selectedSeniority.value = null

    // Emit position change event for parent to handle
    emit('position-change', selectedPosition.value)
  }

  function applyFilters() {
    const newFilters = {
      search_position_query: selectedPosition.value,
      selectedSkills: [...selectedSkills.value], // Create a copy of the array
      selectedSeniority: selectedSeniority.value,
    }

    lastAppliedFilters.value = {
      search_position_query: selectedPosition.value,
      selectedSkills: [...selectedSkills.value], // Create a copy of the array
      selectedSeniority: selectedSeniority.value,
    }

    emit('update:filters', newFilters)
  }

  // Keep local filter state in sync with parent
  watch(
    () => props.initialFilters,
    (newFilters) => {
      if (newFilters) {
        if (newFilters.search_position_query !== undefined) {
          selectedPosition.value = newFilters.search_position_query
        }
        if (newFilters.selectedSkills !== undefined) {
          selectedSkills.value = [...(newFilters.selectedSkills || [])]
        }
        if (newFilters.selectedSeniority !== undefined) {
          selectedSeniority.value = newFilters.selectedSeniority
        }
      }
    },
    { deep: true, immediate: true }
  )

  // Set last applied filters only once on mount
  onMounted(() => {
    lastAppliedFilters.value = {
      search_position_query: selectedPosition.value,
      selectedSkills: [...selectedSkills.value],
      selectedSeniority: selectedSeniority.value,
    }
  })
</script>

<style scoped>
  .filter-bar {
    display: grid;
    grid-template-columns: repeat(3, 1fr) auto;
    gap: 1rem;
    align-items: end;
    background: white;
    padding: 1rem;
    border-radius: 0.75rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
    margin-bottom: 1.5rem;
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

  :deep(.n-select-menu) {
    max-height: 300px !important;
  }

  :deep(.n-select-option) {
    padding: 8px 12px !important;
  }

  :deep(.n-select-option--selected) {
    background-color: #e6f4ff !important;
  }

  :deep(.n-select-option--focus) {
    background-color: #f5f5f5 !important;
  }
</style>
