<template>
  <div class="export-filter-section">
    <!-- Section Title -->
    <div class="filter-section-header">
      <h3 class="section-title">
        🔎 Filtros de Exportação
      </h3>
      <p class="section-description">
        Configure os filtros para personalizar sua exportação de dados
      </p>
    </div>

    <!-- Position Filter (Above Grid) -->
    <div class="position-filter-section">
      <div class="filter-group">
        <label class="filter-label">Cargo</label>
        <select
          v-model="filters.selectedPosition"
          class="single-select"
          @change="onPositionChange"
        >
          <option
            v-for="position in availablePositions"
            :key="position"
            :value="position"
          >
            {{ position }}
          </option>
        </select>
        <small class="filter-help">Selecione o cargo para filtrar os dados</small>
      </div>
    </div>

    <!-- Filter Grid -->
    <div class="filters-grid">
      <!-- Company Filter -->
      <div class="filter-group">
        <label class="filter-label">Empresa</label>
        <select
          v-model="filters.selectedCompanies"
          multiple
          class="multi-select"
          @change="emitFilters"
        >
          <option value="">
            Todas
          </option>
          <option
            v-for="company in availableCompanies"
            :key="company"
            :value="company"
          >
            {{ company }}
          </option>
        </select>
        <small class="filter-help">Use Ctrl+Click para múltiplas seleções</small>
      </div>

      <!-- Publisher Filter -->
      <div class="filter-group">
        <label class="filter-label">Portal de Empregos</label>
        <select
          v-model="filters.selectedPublishers"
          multiple
          class="multi-select"
          @change="emitFilters"
        >
          <option value="">
            Todas
          </option>
          <option
            v-for="publisher in availablePublishers"
            :key="publisher"
            :value="publisher"
          >
            {{ publisher }}
          </option>
        </select>
        <small class="filter-help">Use Ctrl+Click para múltiplas seleções</small>
      </div>

      <!-- Seniority Filter -->
      <div class="filter-group">
        <label class="filter-label">Nível de Senioridade</label>
        <select
          v-model="filters.selectedSeniority"
          multiple
          class="multi-select"
          @change="emitFilters"
        >
          <option value="">
            Todas
          </option>
          <option
            v-for="seniority in availableSeniority"
            :key="seniority"
            :value="seniority"
          >
            {{ seniority }}
          </option>
        </select>
        <small class="filter-help">Use Ctrl+Click para múltiplas seleções</small>
      </div>

      <!-- Employment Type Filter -->
      <div class="filter-group">
        <label class="filter-label">Tipo de Contratação</label>
        <select
          v-model="filters.selectedEmploymentTypes"
          multiple
          class="multi-select"
          @change="emitFilters"
        >
          <option value="">
            Todas
          </option>
          <option
            v-for="type in availableEmploymentTypes"
            :key="type"
            :value="type"
          >
            {{ type }}
          </option>
        </select>
        <small class="filter-help">Use Ctrl+Click para múltiplas seleções</small>
      </div>

      <!-- Location Filters - City -->
      <div class="filter-group">
        <label class="filter-label">Cidade</label>
        <select
          v-model="filters.selectedCities"
          multiple
          class="multi-select"
          @change="emitFilters"
        >
          <option value="">
            Todas
          </option>
          <option
            v-for="city in availableCities"
            :key="city"
            :value="city"
          >
            {{ city }}
          </option>
        </select>
        <small class="filter-help">Use Ctrl+Click para múltiplas seleções</small>
      </div>

      <!-- Location Filters - State -->
      <div class="filter-group">
        <label class="filter-label">Estado</label>
        <select
          v-model="filters.selectedStates"
          multiple
          class="multi-select"
          @change="emitFilters"
        >
          <option value="">
            Todas
          </option>
          <option
            v-for="state in availableStates"
            :key="state"
            :value="state"
          >
            {{ state }}
          </option>
        </select>
        <small class="filter-help">Use Ctrl+Click para múltiplas seleções</small>
      </div>

      <!-- Skills Filter -->
      <div class="filter-group">
        <label class="filter-label">Skills</label>
        <select
          v-model="filters.selectedSkills"
          multiple
          class="multi-select skills-select"
          @change="emitFilters"
        >
          <option value="">
            Todas
          </option>
          <option
            v-for="skill in availableSkills"
            :key="skill"
            :value="skill"
          >
            {{ skill }}
          </option>
        </select>
        <small class="filter-help">Use Ctrl+Click para múltiplas seleções</small>
      </div>

      <!-- Remote Filter -->
      <div class="filter-group">
        <label class="filter-label">Modalidade</label>
        <select
          v-model="filters.selectedRemoteTypes"
          multiple
          class="multi-select"
          @change="emitFilters"
        >
          <option value="">
            Todas
          </option>
          <option value="true">
            Remoto
          </option>
          <option value="false">
            Presencial
          </option>
        </select>
        <small class="filter-help">Use Ctrl+Click para múltiplas seleções</small>
      </div>

      <!-- Direct Application Filter -->
      <div class="filter-group">
        <label class="filter-label">Aplicação Direta</label>
        <select
          v-model="filters.selectedDirectTypes"
          multiple
          class="multi-select"
          @change="emitFilters"
        >
          <option value="">
            Todas
          </option>
          <option value="true">
            Direta
          </option>
          <option value="false">
            Indireta
          </option>
        </select>
        <small class="filter-help">Use Ctrl+Click para múltiplas seleções</small>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons">
      <button
        type="button"
        class="btn btn-secondary"
        :disabled="loadingStates.count || loadingStates.export"
        @click="clearFilters"
      >
        🗑️ Limpar Filtros
      </button>

      <button
        type="button"
        class="btn btn-primary"
        :disabled="loadingStates.count || loadingStates.export"
        @click="countRecords"
      >
        <span
          v-if="loadingStates.count"
          class="loading-spinner"
        />
        📊 Pré-visualizar
        <span
          v-if="recordCount !== null"
          class="record-badge"
        >
          {{ recordCount.toLocaleString() }}
        </span>
      </button>

      <button
        type="button"
        class="btn btn-success"
        :disabled="
          loadingStates.export || loadingStates.count || recordCount === null || recordCount === 0
        "
        @click="exportCSV"
      >
        <span
          v-if="loadingStates.export"
          class="loading-spinner"
        />
        📥 Exportar CSV
      </button>
    </div>
  </div>
</template>

<script setup>
  import { ref, reactive, onMounted } from 'vue'

  defineProps({
    availableCompanies: { type: Array, default: () => [] },
    availablePublishers: { type: Array, default: () => [] },
    availableSeniority: { type: Array, default: () => [] },
    availableEmploymentTypes: { type: Array, default: () => [] },
    availableCities: { type: Array, default: () => [] },
    availableStates: { type: Array, default: () => [] },
    availableSkills: { type: Array, default: () => [] },
    availablePositions: { type: Array, default: () => [] },
  })

  const emit = defineEmits(['filtersChanged', 'countRecords', 'exportCSV', 'positionChange'])

  const filters = ref({
    selectedPosition: 'Data Engineer',
    selectedCompanies: [],
    selectedPublishers: [],
    selectedSeniority: [],
    selectedEmploymentTypes: [],
    selectedCities: [],
    selectedStates: [],
    selectedSkills: [],
    selectedRemoteTypes: [],
    selectedDirectTypes: [],
  })

  const recordCount = ref(null)
  const loadingStates = reactive({
    count: false,
    export: false,
  })

  const emitFilters = () => {
    emit('filtersChanged', filters.value)
  }

  const clearFilters = () => {
    filters.value = {
      selectedPosition: 'Data Engineer',
      selectedCompanies: [],
      selectedPublishers: [],
      selectedSeniority: [],
      selectedEmploymentTypes: [],
      selectedCities: [],
      selectedStates: [],
      selectedSkills: [],
      selectedRemoteTypes: [],
      selectedDirectTypes: [],
    }
    recordCount.value = null
    emitFilters()
  }

  const countRecords = () => {
    emit('countRecords', filters.value)
  }

  const exportCSV = () => {
    emit('exportCSV', filters.value)
  }

  const setLoadingState = (type, state) => {
    loadingStates[type] = state
  }

  const updateRecordCount = (count) => {
    recordCount.value = count
  }

  const onPositionChange = () => {
    // Reset all other filters when position changes
    filters.value.selectedCompanies = []
    filters.value.selectedPublishers = []
    filters.value.selectedSeniority = []
    filters.value.selectedEmploymentTypes = []
    filters.value.selectedCities = []
    filters.value.selectedStates = []
    filters.value.selectedSkills = []
    filters.value.selectedRemoteTypes = []
    filters.value.selectedDirectTypes = []

    // Emit position change event for parent to handle
    emit('positionChange', filters.value.selectedPosition)

    // Also emit filters changed
    emitFilters()
  }

  // Expose methods to parent
  defineExpose({
    setLoadingState,
    updateRecordCount,
  })

  onMounted(() => {
    // Set default date range (last 30 days)
    const today = new Date()
    const thirtyDaysAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1000)

    filters.value.dateTo = today.toISOString().split('T')[0]
    filters.value.dateFrom = thirtyDaysAgo.toISOString().split('T')[0]

    emitFilters()
  })
</script>

<style scoped>
  .export-filter-section {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    margin-bottom: 24px;
    width: 100%;
    max-width: 100%;
    overflow-x: hidden;
  }

  .filter-section-header {
    margin-bottom: 24px;
    text-align: center;
  }

  .section-title {
    font-size: 24px;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 8px;
  }

  .section-description {
    font-size: 16px;
    color: #6b7280;
    margin: 0;
  }

  .position-filter-section {
    margin-bottom: 24px;
    padding-bottom: 24px;
    border-bottom: 1px solid #e5e7eb;
  }

  .position-filter-section .filter-group {
    max-width: 300px;
    width: 100%;
  }

  .filters-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
    margin-bottom: 32px;
    width: 100%;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    width: 100%;
    min-width: 0;
  }

  .filter-label {
    font-size: 14px;
    font-weight: 600;
    color: #374151;
    margin-bottom: 8px;
  }

  .date-range-container {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .date-input {
    flex: 1;
    padding: 10px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.2s;
    width: 100%;
  }

  .date-input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .date-separator {
    font-size: 14px;
    color: #6b7280;
    white-space: nowrap;
  }

  .multi-select {
    min-height: 120px;
    padding: 8px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.2s;
    width: 100%;
    box-sizing: border-box;
  }

  .multi-select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .single-select {
    padding: 10px 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-size: 14px;
    transition: border-color 0.2s;
    background-color: white;
    width: 100%;
    box-sizing: border-box;
  }

  .single-select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  .skills-select {
    min-height: 160px;
  }

  .filter-help {
    font-size: 12px;
    color: #6b7280;
    margin-top: 4px;
    font-style: italic;
  }

  .checkbox-container {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .checkbox-label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
    color: #374151;
    cursor: pointer;
  }

  .checkbox-label input[type='radio'] {
    margin: 0;
  }

  .action-buttons {
    display: flex;
    justify-content: center;
    gap: 16px;
    padding-top: 24px;
    border-top: 1px solid #e5e7eb;
    flex-wrap: wrap;
  }

  .btn {
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 8px;
    white-space: nowrap;
  }

  .btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .btn-secondary {
    background-color: #f3f4f6;
    color: #374151;
  }

  .btn-secondary:hover:not(:disabled) {
    background-color: #e5e7eb;
  }

  .btn-info {
    background-color: #3b82f6;
    color: white;
  }

  .btn-info:hover:not(:disabled) {
    background-color: #2563eb;
  }

  .btn-primary {
    background-color: #059669;
    color: white;
  }

  .btn-primary:hover:not(:disabled) {
    background-color: #047857;
  }

  .btn-success {
    background-color: #059669;
    color: white;
  }

  .btn-success:hover:not(:disabled) {
    background-color: #047857;
  }

  .loading-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid transparent;
    border-top: 2px solid currentColor;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  .results-info {
    background-color: #f0f9ff;
    border: 1px solid #bae6fd;
    border-radius: 8px;
    padding: 16px;
    margin-top: 16px;
  }

  .count-display {
    text-align: center;
  }

  .count-number {
    font-size: 24px;
    font-weight: 700;
    color: #0369a1;
  }

  .count-text {
    font-size: 16px;
    color: #374151;
    margin-left: 8px;
  }

  .count-warning {
    display: block;
    font-size: 14px;
    color: #dc2626;
    margin-top: 4px;
    font-weight: 500;
  }

  .record-badge {
    background-color: #059669;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    margin-left: 8px;
  }

  /* Mobile-first responsive design */
  @media (max-width: 768px) {
    .export-filter-section {
      padding: 16px;
      margin: 16px;
      border-radius: 8px;
    }

    .filters-grid {
      grid-template-columns: 1fr;
      gap: 16px;
    }

    .action-buttons {
      flex-direction: column;
      gap: 12px;
    }

    .btn {
      width: 100%;
      justify-content: center;
    }

    .date-range-container {
      flex-direction: column;
    }

    .date-separator {
      align-self: center;
    }

    .position-filter-section .filter-group {
      max-width: 100%;
    }

    .section-title {
      font-size: 20px;
    }

    .section-description {
      font-size: 14px;
    }
  }

  @media (max-width: 640px) {
    .export-filter-section {
      padding: 12px;
      margin: 12px;
    }

    .filters-grid {
      gap: 12px;
    }

    .filter-group {
      margin-bottom: 8px;
    }

    .multi-select {
      min-height: 100px;
    }

    .skills-select {
      min-height: 120px;
    }
  }

  @media (max-width: 480px) {
    .export-filter-section {
      padding: 8px;
      margin: 8px;
    }

    .filters-grid {
      gap: 8px;
    }

    .section-title {
      font-size: 18px;
    }

    .section-description {
      font-size: 13px;
    }
  }
</style>
