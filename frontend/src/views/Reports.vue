<template>
  <BasePageLayout
    title="Exportação de Dados"
    subtitle="Gere extrações personalizadas de dados de vagas com filtros avançados"
    icon="📄"
    page-id="reports"
    :loading="false"
    :error="null"
    :filters="{}"
    @period-change="onPeriodFilterChange"
  >
    <!-- Filters Section -->
    <ReportFilterBar
      ref="filterBar"
      :available-positions="filterOptions.positions"
      :available-companies="filterOptions.companies"
      :available-publishers="filterOptions.publishers"
      :available-seniority="filterOptions.seniority"
      :available-employment-types="filterOptions.employmentTypes"
      :available-cities="filterOptions.cities"
      :available-states="filterOptions.states"
      :available-skills="filterOptions.skills"
      @filters-changed="onFiltersChanged"
      @position-change="onPositionChange"
      @count-records="handleCountRecords"
      @export-c-s-v="handleExportCSV"
    />

    <!-- Preview Section -->
    <div
      v-if="showPreview && previewData.length > 0"
      class="mt-8"
    >
      <div class="bg-white shadow rounded-lg p-6">
        <div class="mb-4 flex justify-between items-center">
          <h2 class="text-xl font-semibold text-gray-900">
            📋 Pré-visualização da Exportação
          </h2>
          <span class="text-sm text-gray-500">
            Mostrando {{ previewData.length }} de {{ recordCount?.toLocaleString() || 0 }} registros
            (máximo 5 para pré-visualização)
          </span>
        </div>

        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  ID
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Título
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Empresa
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Data Publicação
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Localização
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Senioridade
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Tipo
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Remoto
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="job in previewData"
                :key="job.job_id"
                class="hover:bg-gray-50"
              >
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 font-mono">
                  {{ job.job_id.substring(0, 8) }}...
                </td>
                <td class="px-4 py-4 text-sm text-gray-900 max-w-xs truncate">
                  {{ truncateTitle(job.job_title) }}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ job.employer_name }}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatDate(job.job_posted_at_date) }}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ formatLocation(job.job_city, job.job_state) }}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getSeniorityBadgeClass(job.seniority)"
                  >
                    {{ job.seniority || 'N/A' }}
                  </span>
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ job.job_employment_type }}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="
                      job.job_is_remote
                        ? 'bg-green-100 text-green-800'
                        : 'bg-blue-100 text-blue-800'
                    "
                  >
                    {{ job.job_is_remote ? 'Sim' : 'Não' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>


  </BasePageLayout>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useMessage } from 'naive-ui'
  import BasePageLayout from '@/components/common/BasePageLayout.vue'
  import ReportFilterBar from '@/components/filters/ReportFilterBar.vue'

  import { reportsApi } from '@/api/reports'
  import { format, parseISO } from 'date-fns'
  import { ptBR } from 'date-fns/locale'

  defineOptions({
    name: 'ReportsPage',
  })

  const router = useRouter()
  const message = useMessage()

  // State
  const filterBar = ref(null)
  const currentFilters = ref({})
  const periodFilters = ref({
    dateFrom: null,
    dateTo: null,
    period: 'last30days',
  })
  const recordCount = ref(null)
  const previewData = ref([])
  const showPreview = ref(false)

  // Filter options
  const filterOptions = ref({
    positions: [],
    companies: [],
    publishers: [],
    seniority: [],
    employmentTypes: [],
    cities: [],
    states: [],
    skills: [],
  })



  // Methods
  const onPeriodFilterChange = (filters) => {
    periodFilters.value = filters
    showPreview.value = false
    recordCount.value = null
  }

  const onFiltersChanged = (filters) => {
    currentFilters.value = filters
    showPreview.value = false
    recordCount.value = null
  }

  const onPositionChange = async (newPosition) => {
    // Clear preview and count when position changes
    showPreview.value = false
    recordCount.value = null

    // Refresh all filter options for the new position
    await loadFilterOptions(newPosition)
  }

  const handleCountRecords = async (filters) => {
    try {
      filterBar.value?.setLoadingState('count', true)

      // Merge period filters with advanced filters
      const combinedFilters = {
        ...filters,
        ...periodFilters.value,
      }

      const result = await reportsApi.countExportRecords(combinedFilters)
      recordCount.value = result.count
      filterBar.value?.updateRecordCount(result.count)

      // Load preview data
      if (result.count > 0) {
        previewData.value = await reportsApi.previewExport(combinedFilters, 5)
        showPreview.value = true
        message.success(`Encontrados ${result.count.toLocaleString()} registros!`)
      } else {
        showPreview.value = false
        message.info('Nenhum registro encontrado com os filtros aplicados.')
      }
    } catch (error) {
      message.error(`Erro ao contar registros: ${error.message || 'Erro desconhecido'}`)
      showPreview.value = false
    } finally {
      filterBar.value?.setLoadingState('count', false)
    }
  }

  const handleExportCSV = async (filters) => {
    try {
      filterBar.value?.setLoadingState('export', true)

      // Merge period filters with advanced filters
      const combinedFilters = {
        ...filters,
        ...periodFilters.value,
      }

      await reportsApi.exportCSV(combinedFilters)
      message.success('Exportação realizada com sucesso!')
    } catch (error) {
      message.error(`Erro ao exportar dados: ${error.message || 'Erro desconhecido'}`)
    } finally {
      filterBar.value?.setLoadingState('export', false)
    }
  }

  const loadFilterOptions = async (position = 'Data Engineer') => {
    try {
      const [positions, companies, publishers, seniority, employmentTypes, locations, skills] =
        await Promise.all([
          reportsApi.getAvailablePositions(),
          reportsApi.getAvailableCompanies(position),
          reportsApi.getAvailablePublishers(position),
          reportsApi.getAvailableSeniority(position),
          reportsApi.getAvailableEmploymentTypes(),
          reportsApi.getAvailableLocations(position),
          reportsApi.getAvailableSkills(position),
        ])

      // Extract cities and states from the locations response
      const cities = locations
        .map((loc) => loc.title)
        .filter((v, i, a) => v && a.indexOf(v) === i)
        .sort()
      const states = locations
        .map((loc) => loc.state)
        .filter((v, i, a) => v && a.indexOf(v) === i)
        .sort()

      filterOptions.value = {
        positions,
        companies,
        publishers,
        seniority,
        employmentTypes,
        cities,
        states,
        skills,
      }
    } catch (error) {
      console.error('Error loading filter options:', error)
      message.error('Erro ao carregar opções de filtro. Tente recarregar a página.')
    }
  }

  // Utility functions
  const truncateTitle = (title) => {
    if (!title) {
      return 'N/A'
    }
    const maxLength = Math.min(Math.floor(title.length * 0.7), 30)
    return title.length > maxLength ? `${title.substring(0, maxLength)}...` : title
  }

  const formatDate = (dateStr) => {
    if (!dateStr) {
      return 'N/A'
    }
    try {
      return format(parseISO(dateStr), 'dd/MM/yyyy', { locale: ptBR })
    } catch {
      return dateStr
    }
  }

  const formatLocation = (city, state) => {
    if (!city && !state) {
      return 'N/A'
    }
    if (!city) {
      return state
    }
    if (!state) {
      return city
    }
    return `${city}, ${state}`
  }

  const getSeniorityBadgeClass = (seniority) => {
    if (!seniority) {
      return 'bg-gray-100 text-gray-800'
    }

    const level = seniority.toLowerCase()
    if (level.includes('junior') || level.includes('trainee')) {
      return 'bg-green-100 text-green-800'
    }
    if (level.includes('pleno') || level.includes('mid')) {
      return 'bg-blue-100 text-blue-800'
    }
    if (level.includes('senior') || level.includes('lead')) {
      return 'bg-purple-100 text-purple-800'
    }

    return 'bg-gray-100 text-gray-800'
  }

  // Initialize period filters with default values
  const initializePeriodFilters = () => {
    const end = new Date()
    const start = new Date()
    start.setDate(start.getDate() - 30)

    periodFilters.value = {
      dateFrom: start.toISOString().split('T')[0],
      dateTo: end.toISOString().split('T')[0],
      period: 'last30days',
    }
  }

  // Lifecycle
  onMounted(async () => {
    initializePeriodFilters()
    await loadFilterOptions()
  })
</script>

<style scoped>
  .truncate {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .max-w-xs {
    max-width: 20rem;
  }

  /* Custom scrollbar for table */
  .overflow-x-auto::-webkit-scrollbar {
    height: 8px;
  }

  .overflow-x-auto::-webkit-scrollbar-track {
    background: #f1f5f9;
    border-radius: 4px;
  }

  .overflow-x-auto::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 4px;
  }

  .overflow-x-auto::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
  }

  /* Mobile responsiveness for Reports view */
  @media (max-width: 768px) {
    .overflow-x-auto {
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }

    /* Ensure table fits on mobile */
    table {
      min-width: 600px; /* Minimum width to prevent squashing */
    }

    /* Adjust preview section padding on mobile */
    .bg-white.shadow.rounded-lg.p-6 {
      padding: 16px;
      margin: 16px;
    }

    /* Make table headers and cells more mobile-friendly */
    th,
    td {
      padding: 8px 4px;
      font-size: 12px;
    }

    /* Ensure text doesn't overflow on mobile */
    .max-w-xs {
      max-width: 12rem;
    }
  }

  @media (max-width: 640px) {
    .bg-white.shadow.rounded-lg.p-6 {
      padding: 12px;
      margin: 12px;
    }

    th,
    td {
      padding: 6px 3px;
      font-size: 11px;
    }

    .max-w-xs {
      max-width: 10rem;
    }
  }

  @media (max-width: 480px) {
    .bg-white.shadow.rounded-lg.p-6 {
      padding: 8px;
      margin: 8px;
    }

    th,
    td {
      padding: 4px 2px;
      font-size: 10px;
    }

    .max-w-xs {
      max-width: 8rem;
    }
  }
</style>
