<template>
  <BasePageLayout
    title="Empresas & Vagas"
    subtitle="Explore e analise empresas e suas vagas com filtros avançados"
    icon="🏢"
    page-id="empresas"
    :loading="empresasStore.loading"
    :error="empresasStore.error"
    :filters="empresasStore.filters"
    @period-change="onPeriodFilterChange"
  >
    <template #filter-bar>
      <!-- Advanced Filters -->
      <div class="filter-bar">
        <div class="filter-group">
          <div class="filter-title">
            Cargo
          </div>
          <NSelect
            v-model:value="selectedPosition"
            :options="positionOptions"
            class="filter-select"
            placeholder="Selecione um cargo"
            filterable
            aria-label="Selecionar cargo"
            @update:value="onPositionChange"
          />
        </div>

        <div class="filter-group">
          <div class="filter-title">
            Empresa
          </div>
          <NSelect
            v-model:value="selectedCompany"
            :options="companyOptions"
            class="filter-select"
            placeholder="Todas as empresas"
            filterable
            aria-label="Selecionar empresa"
            @update:value="onCompanyChange"
          />
        </div>

        <div class="filter-group">
          <div class="filter-title">
            Remoto/Presencial
          </div>
          <NSelect
            v-model:value="selectedRemote"
            :options="remoteOptions"
            class="filter-select"
            placeholder="Todos"
            aria-label="Selecionar tipo de trabalho"
            @update:value="onRemoteChange"
          />
        </div>

        <div class="filter-group">
          <div class="filter-title">
            Cidade
          </div>
          <NSelect
            :key="`city-${selectedPosition}`"
            v-model:value="selectedCity"
            :options="cityOptions"
            class="filter-select"
            placeholder="Todas as cidades"
            filterable
            aria-label="Selecionar cidade"
            :disabled="selectedRemote === 'true'"
            @update:value="onCityChange"
          />
        </div>

        <div class="filter-group">
          <div class="filter-title">
            Senioridade
          </div>
          <NSelect
            v-model:value="selectedSeniority"
            :options="seniorityOptions"
            class="filter-select"
            placeholder="Todas"
            aria-label="Selecionar senioridade"
            @update:value="onSeniorityChange"
          />
        </div>

        <div class="filter-actions">
          <button
            class="apply-btn"
            :disabled="empresasStore.loading"
            @click="applyFilters"
          >
            <span
              v-if="empresasStore.loading"
              class="spinner"
            />
            Aplicar Filtros
          </button>
        </div>
      </div>
    </template>

    <!-- Companies Table -->
    <div class="bg-white shadow-lg border-2 border-gray-300 rounded-lg p-6">
      <div class="mb-4 flex justify-between items-center">
        <h3 class="text-xl font-semibold text-gray-900">
          🏢 Empresas Encontradas
        </h3>
        <span class="text-sm text-gray-500">
          Mostrando {{ paginatedCompanies.length }} de {{ totalCompanies }} empresas (top 50 de
          {{ totalUniqueCompanies }} total)
        </span>
      </div>

      <!-- Loading State -->
      <div
        v-if="empresasStore.loading"
        class="flex justify-center items-center py-8"
      >
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        <span class="ml-3 text-gray-600">Carregando empresas...</span>
      </div>

      <!-- Table -->
      <div
        v-else
        class="overflow-x-auto"
      >
        <div class="max-h-96 overflow-y-auto border border-gray-300 rounded-lg">
          <table class="min-w-full divide-y divide-gray-300">
            <thead class="bg-gray-100 sticky top-0">
              <tr>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border-r border-gray-300"
                >
                  Nome
                </th>
                <th
                  class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider text-center"
                >
                  Vagas
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-300">
              <tr
                v-for="company in paginatedCompanies"
                :key="company.employer_name"
                class="hover:bg-gray-50 cursor-pointer"
                :class="{
                  'bg-blue-50':
                    selectedCompanyData &&
                    selectedCompanyData.employer_name === company.employer_name,
                }"
                @click="selectCompany(company)"
              >
                <td class="px-4 py-4 text-sm text-gray-900 border-r border-gray-300">
                  {{ company.employer_name }}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
                  <span
                    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800"
                  >
                    {{ company.job_count }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Pagination -->
      <div
        v-if="totalPages > 1"
        class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
      >
        <div class="flex-1 flex justify-between sm:hidden">
          <button
            :disabled="currentPage === 1"
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            @click="previousPage"
          >
            Anterior
          </button>
          <button
            :disabled="currentPage === totalPages"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            @click="nextPage"
          >
            Próximo
          </button>
        </div>
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Mostrando <span class="font-medium">{{ startIndex + 1 }}</span> a
              <span class="font-medium">{{ endIndex }}</span> de
              <span class="font-medium">{{ totalCompanies }}</span> resultados
              <span class="text-xs text-gray-500 ml-2">(top 50 empresas)</span>
            </p>
          </div>
          <div>
            <nav
              class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
              aria-label="Pagination"
            >
              <button
                :disabled="currentPage === 1"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                @click="previousPage"
              >
                <span class="sr-only">Anterior</span>
                ←
              </button>

              <template
                v-for="page in visiblePages"
                :key="page"
              >
                <button
                  v-if="typeof page === 'number'"
                  :class="[
                    'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                    page === currentPage
                      ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                      : 'bg-white border-gray-300 text-gray-500 hover:bg-gray-50',
                  ]"
                  @click="goToPage(page)"
                >
                  {{ page }}
                </button>
                <span
                  v-else
                  class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700"
                >
                  ...
                </span>
              </template>

              <button
                :disabled="currentPage === totalPages"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
                @click="nextPage"
              >
                <span class="sr-only">Próximo</span>
                →
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Company Details Section -->
    <div
      v-if="selectedCompanyData"
      class="bg-white shadow-lg border-2 border-gray-300 rounded-lg p-6 mt-6"
    >
      <div class="mb-4">
        <h3 class="text-xl font-semibold text-gray-900">
          🏢 {{ selectedCompanyData.employer_name }}
        </h3>
        <p class="text-sm text-gray-600 mt-2">
          {{ companyJobs.length }}
          {{ companyJobs.length === 1 ? 'vaga disponível' : 'vagas disponíveis' }}
        </p>
      </div>

      <!-- Loading State for Details -->
      <div
        v-if="empresasStore.loadingDetails"
        class="flex justify-center items-center py-8"
      >
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        <span class="ml-3 text-gray-600">Carregando detalhes...</span>
      </div>

      <!-- Company Jobs Details -->
      <div
        v-else
        class="space-y-4"
      >
        <div
          v-for="job in companyJobs"
          :key="job.job_id"
          class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
        >
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <h4 class="text-lg font-medium text-gray-900 mb-2">
                {{ job.job_title }}
              </h4>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
                <div>
                  <span class="font-medium">Remoto:</span>
                  <span
                    class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="
                      job.job_is_remote
                        ? 'bg-green-100 text-green-800'
                        : 'bg-blue-100 text-blue-800'
                    "
                  >
                    {{ job.job_is_remote ? 'Sim' : 'Não' }}
                  </span>
                </div>
                <div>
                  <span class="font-medium">Senioridade:</span>
                  <span
                    class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getSeniorityBadgeClass(job.seniority)"
                  >
                    {{ job.seniority || 'N/A' }}
                  </span>
                </div>
                <div>
                  <span class="font-medium">Data de Publicação:</span>
                  <span class="ml-2">{{ formatDate(job.job_posted_at_date) }}</span>
                </div>
                <div>
                  <span class="font-medium">Tipo:</span>
                  <span class="ml-2">{{ job.job_employment_type }}</span>
                </div>
              </div>

              <!-- Apply Options -->
              <div
                v-if="parseApplyOptions(job.apply_options).length > 0"
                class="mt-3"
              >
                <span class="font-medium text-sm text-gray-700">Opções de Candidatura:</span>
                <div class="flex flex-wrap gap-2 mt-1">
                  <a
                    v-for="(option, optionIndex) in parseApplyOptions(job.apply_options)"
                    :key="optionIndex"
                    :href="option.apply_link"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-flex items-center px-3 py-1 rounded-md text-xs font-medium bg-blue-100 text-blue-800 hover:bg-blue-200 transition-colors duration-200"
                  >
                    🔗 {{ option.publisher }}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State for Details -->
    <div
      v-if="!selectedCompanyData && !empresasStore.loading"
      class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mt-6"
    >
      <div class="text-gray-400 text-6xl mb-4">
        🏢
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        Selecione uma empresa
      </h3>
      <p class="text-gray-600">
        Clique em uma empresa na tabela acima para ver os detalhes das vagas disponíveis.
      </p>
    </div>

    <!-- Welcome Popup -->
    <WelcomePopup />
  </BasePageLayout>
</template>

<script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import { NSelect } from 'naive-ui'
  import { useMessage } from 'naive-ui'
  import BasePageLayout from '@/components/common/BasePageLayout.vue'
  import WelcomePopup from '@/components/common/WelcomePopup.vue'
  import { useEmpresasStore } from '@/stores/empresas'
  import { format, parseISO } from 'date-fns'
  import { ptBR } from 'date-fns/locale'

  const empresasStore = useEmpresasStore()
  const message = useMessage()

  // Reactive data
  const selectedPosition = ref('')
  const selectedCompany = ref('')
  const selectedRemote = ref('')
  const selectedSeniority = ref('')
  const selectedCity = ref(null)

  // Use computed for selectedCompanyData to sync with store
  const selectedCompanyData = computed({
    get: () => empresasStore.selectedCompany,
    set: (value) => {
      empresasStore.setSelectedCompany(value)
    },
  })
  const currentPage = ref(1)
  const itemsPerPage = 15

  // Synchronize local reactive variables with store filters
  const syncFiltersFromStore = () => {
    const storeFilters = empresasStore.filters
    selectedPosition.value = storeFilters.search_position_query || ''
    selectedCompany.value = storeFilters.employer_name || ''
    selectedRemote.value = storeFilters.job_is_remote || ''
    selectedSeniority.value = storeFilters.seniority || ''
    selectedCity.value = storeFilters.job_city
  }

  // Computed properties
  const positionOptions = computed(() => {
    const positions = empresasStore.availablePositions || []
    return [
      { label: 'Todos os cargos', value: '' },
      ...positions.map((pos) => ({ label: pos, value: pos })),
    ]
  })

  const companyOptions = computed(() => {
    const companies = empresasStore.availableCompanies || []
    return [
      { label: 'Todas as empresas', value: '' },
      ...companies.map((company) => ({ label: company, value: company })),
    ]
  })

  const remoteOptions = ref([
    { label: 'Todos', value: '' },
    { label: 'Remoto', value: 'true' },
    { label: 'Presencial', value: 'false' },
  ])

  const seniorityOptions = computed(() => {
    const seniorities = empresasStore.availableSeniorities || []
    return [
      { label: 'Todas', value: '' },
      ...seniorities.map((seniority) => ({ label: seniority, value: seniority })),
    ]
  })

  const cityOptions = computed(() => {
    // If remote is true, only show N/A option
    if (selectedRemote.value === 'true') {
      return [{ label: 'N/A', value: 'N/A' }]
    }

    const options = [{ label: 'Todas as cidades', value: null }]

    // Add available cities from the store
    const locationData = empresasStore.locationData || []
    const cities = [...new Set(locationData.map((loc) => loc.title))]
      .filter(Boolean)
      .sort((a, b) => a.localeCompare(b))

    cities.forEach((city) => {
      options.push({ label: city, value: city })
    })

    return options
  })

  // Aggregate companies from jobs data
  const aggregatedCompanies = computed(() => {
    const companiesMap = new Map()

    empresasStore.jobs.forEach((job) => {
      const companyName = job.employer_name
      if (companiesMap.has(companyName)) {
        companiesMap.set(companyName, companiesMap.get(companyName) + 1)
      } else {
        companiesMap.set(companyName, 1)
      }
    })

    // Convert to array, sort by job count (highest to lowest), and limit to top 50 companies
    return Array.from(companiesMap.entries())
      .map(([employer_name, job_count]) => ({ employer_name, job_count }))
      .sort((a, b) => b.job_count - a.job_count)
      .slice(0, 50) // Limit to top 50 companies for display
  })

  // Total unique companies from all jobs (before limiting to 50)
  const totalUniqueCompanies = computed(() => {
    const uniqueCompanies = new Set(empresasStore.jobs.map((job) => job.employer_name))
    return uniqueCompanies.size
  })

  const totalCompanies = computed(() => aggregatedCompanies.value.length)
  const totalPages = computed(() => Math.ceil(totalCompanies.value / itemsPerPage))

  const paginatedCompanies = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage
    const end = start + itemsPerPage
    return aggregatedCompanies.value.slice(start, end)
  })

  const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage)
  const endIndex = computed(() => Math.min(startIndex.value + itemsPerPage, totalCompanies.value))

  const visiblePages = computed(() => {
    const total = totalPages.value
    const current = currentPage.value
    const delta = 2
    const range = []
    const rangeWithDots = []

    for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
      range.push(i)
    }

    if (current - delta > 2) {
      rangeWithDots.push(1, '...')
    } else {
      rangeWithDots.push(1)
    }

    rangeWithDots.push(...range)

    if (current + delta < total - 1) {
      rangeWithDots.push('...', total)
    } else if (total > 1) {
      rangeWithDots.push(total)
    }

    return total > 1 ? rangeWithDots : []
  })

  // Company jobs for selected company
  const companyJobs = computed(() => {
    if (!selectedCompanyData.value) {
      return []
    }
    return empresasStore.jobs.filter(
      (job) => job.employer_name === selectedCompanyData.value.employer_name
    )
  })

  // Helper functions
  const formatDate = (dateString) => {
    try {
      return format(parseISO(dateString), 'dd/MM/yyyy', { locale: ptBR })
    } catch (error) {
      console.error('Error formatting date:', error)
      return dateString
    }
  }

  const parseApplyOptions = (applyOptionsString) => {
    if (!applyOptionsString) {
      return []
    }

    try {
      // If it's already an array, return it
      if (Array.isArray(applyOptionsString)) {
        return applyOptionsString
      }

      // If it's a string, try to parse it as JSON
      if (typeof applyOptionsString === 'string') {
        const parsed = JSON.parse(applyOptionsString)
        return Array.isArray(parsed) ? parsed : []
      }

      return []
    } catch (error) {
      console.error('Error parsing apply options:', error)
      return []
    }
  }

  const getSeniorityBadgeClass = (seniority) => {
    const seniorityMap = {
      Junior: 'bg-green-100 text-green-800',
      Pleno: 'bg-yellow-100 text-yellow-800',
      Senior: 'bg-red-100 text-red-800',
      Lead: 'bg-purple-100 text-purple-800',
      Principal: 'bg-indigo-100 text-indigo-800',
    }
    return seniorityMap[seniority] || 'bg-gray-100 text-gray-800'
  }

  // Event handlers
  const onPositionChange = async (value) => {
    selectedPosition.value = value

    // Reset other filters when position changes (same as Empresas Ranking)
    selectedCompany.value = ''
    selectedRemote.value = ''
    selectedSeniority.value = ''
    selectedCity.value = null

    // Update store filters (but don't fetch data yet)
    empresasStore.setFilters({
      search_position_query: value,
      employer_name: '',
      job_is_remote: '',
      seniority: '',
      job_city: null,
    })

    // Only update available companies and seniority levels for the new position
    // Don't fetch table data - that should only happen when "Aplicar Filtros" is clicked
    try {
      // Fetch available companies, seniority levels, and locations for the new position (empty value means all positions)
      await Promise.all([
        empresasStore.fetchAvailableCompaniesForPosition(value || null),
        empresasStore.fetchAvailableSeniorityForPosition(value || null),
        empresasStore.fetchFilteredLocations(),
      ])

      console.log('Position changed, filter options updated:', value)
    } catch (error) {
      console.error('Error updating filter options after position change:', error)
    }
  }

  const onCompanyChange = (value) => {
    selectedCompany.value = value
  }

  const onRemoteChange = (value) => {
    selectedRemote.value = value

    // If remote is true, set city to N/A
    if (value === 'true') {
      selectedCity.value = 'N/A'
    } else if (selectedCity.value === 'N/A') {
      // Reset city if it was previously set to N/A
      selectedCity.value = null
    }
  }

  const onCityChange = (value) => {
    selectedCity.value = value
  }

  const onSeniorityChange = (value) => {
    selectedSeniority.value = value
  }

  const applyFilters = async () => {
    console.log('Applying filters:', {
      position: selectedPosition.value,
      company: selectedCompany.value,
      remote: selectedRemote.value,
      seniority: selectedSeniority.value,
      city: selectedCity.value,
    })

    empresasStore.setFilters({
      search_position_query: selectedPosition.value,
      employer_name: selectedCompany.value,
      job_is_remote: selectedRemote.value,
      seniority: selectedSeniority.value,
      job_city: selectedCity.value,
    })

    try {
      // Save current selected company if there is one
      const currentSelectedCompany = selectedCompanyData.value
        ? { ...selectedCompanyData.value }
        : null
      const currentSelectedCompanyName = currentSelectedCompany?.employer_name

      await empresasStore.fetchEmpresasData()
      currentPage.value = 1

      if (currentSelectedCompanyName && empresasStore.jobs.length > 0) {
        // Try to find the previously selected company in the new aggregated results
        const aggregatedCompaniesAfterFilter = aggregatedCompanies.value
        const previouslySelectedCompany = aggregatedCompaniesAfterFilter.find(
          (company) => company.employer_name === currentSelectedCompanyName
        )

        if (previouslySelectedCompany) {
          // If the same company exists in the new results, keep it selected
          selectedCompanyData.value = previouslySelectedCompany
          console.log('Preserved selection of company:', previouslySelectedCompany.employer_name)
        } else if (aggregatedCompaniesAfterFilter.length > 0) {
          // Company not found, but we have companies available
          selectedCompanyData.value = null
          console.log('Previously selected company not found in new results')
        } else {
          // No companies available
          selectedCompanyData.value = null
        }
      } else if (empresasStore.jobs.length === 0) {
        // No jobs found at all
        selectedCompanyData.value = null
      }

      message.success('Pesquisa realizada com sucesso!')
      console.log('Filters applied, data loaded:', empresasStore.jobs.length)
    } catch (error) {
      console.error('Error applying filters:', error)
      message.error(`Erro ao aplicar filtros: ${error.message || 'Erro desconhecido'}`)
    }
  }

  const onPeriodFilterChange = async (periodFilters) => {
    console.log('Period filter changed:', periodFilters)

    // Save current selected company if there is one for later comparison
    const currentSelectedCompany = selectedCompanyData.value
      ? { ...selectedCompanyData.value }
      : null
    const currentSelectedCompanyName = currentSelectedCompany?.employer_name

    empresasStore.setPeriod(periodFilters)
    console.log('Updated filters in store:', empresasStore.filters)

    try {
      // Fetch the data
      await empresasStore.fetchEmpresasData()
      currentPage.value = 1

      // Try to find the previously selected company in the new results
      let previouslySelectedCompany = null

      if (currentSelectedCompanyName && empresasStore.jobs.length > 0) {
        // Try to find the previously selected company in the new aggregated results
        const aggregatedCompaniesAfterFilter = aggregatedCompanies.value
        previouslySelectedCompany = aggregatedCompaniesAfterFilter.find(
          (company) => company.employer_name === currentSelectedCompanyName
        )
      }
      
      message.success('Período alterado com sucesso!')

      // Update the selection based on what we found earlier
      if (previouslySelectedCompany) {
        // If the same company exists in the new results, keep it selected
        selectedCompanyData.value = previouslySelectedCompany
        console.log('Preserved selection of company:', previouslySelectedCompany.employer_name)
      } else if (empresasStore.jobs.length > 0) {
        // Company not found, but we have companies available        
        selectedCompanyData.value = null
        console.log('Previously selected company not found in new results')
      } else {
        // No companies available
        selectedCompanyData.value = null
      }
    } catch (error) {
      console.error('Error during period filter change:', error)
      message.error(`Erro ao alterar período: ${error.message || 'Erro desconhecido'}`)
    }
  }

  const selectCompany = (company) => {
    selectedCompanyData.value = company
  }

  const previousPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--
    }
  }

  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++
    }
  }

  const goToPage = (page) => {
    currentPage.value = page
  }

  // Lifecycle
  onMounted(async () => {
    try {
      // Initialize with default filters
      empresasStore.initializeWithDefaults()

      // Synchronize local reactive variables with store filters
      syncFiltersFromStore()

      // Fetch available positions first
      await empresasStore.fetchAvailableOptions()

      // Fetch companies, seniority levels, and locations for current selection (empty means all)
      const currentPosition = selectedPosition.value || null
      await Promise.all([
        empresasStore.fetchAvailableCompaniesForPosition(currentPosition),
        empresasStore.fetchAvailableSeniorityForPosition(currentPosition),
        empresasStore.fetchFilteredLocations(),
      ])

      // Then fetch the initial data
      await empresasStore.fetchEmpresasData()

      console.log('EmpresasView mounted, data loaded:', empresasStore.jobs.length)
    } catch (error) {
      console.error('Error during EmpresasView initialization:', error)
      // Continue loading even if some APIs fail - the store handles graceful degradation
    }
  })

  // Watch for store filter changes and sync local variables
  watch(
    () => empresasStore.filters,
    () => {
      syncFiltersFromStore()
    },
    { deep: true }
  )
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
