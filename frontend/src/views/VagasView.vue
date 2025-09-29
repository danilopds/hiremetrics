<template>
  <BasePageLayout
    title="Vagas"
    subtitle="Explore e analise vagas de tecnologia com filtros avançados"
    icon="💼"
    page-id="vagas"
    :loading="vagasStore.loading"
    :error="vagasStore.error"
    :filters="vagasStore.filters"
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
            placeholder="Todos os cargos"
            filterable
            aria-label="Selecionar cargo"
            @update:value="onPositionChange"
          />
        </div>

        <div class="filter-group">
          <div class="filter-title">
            Tipo de Contrato
          </div>
          <NSelect
            v-model:value="selectedEmploymentType"
            :options="employmentTypeOptions"
            class="filter-select"
            placeholder="Todos os tipos"
            aria-label="Selecionar tipo de contrato"
            @update:value="onEmploymentTypeChange"
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
            placeholder="Todas as senioridades"
            aria-label="Selecionar senioridade"
            @update:value="onSeniorityChange"
          />
        </div>

        <div class="filter-actions">
          <button
            class="apply-btn"
            :disabled="vagasStore.loading"
            @click="applyFilters"
          >
            <span
              v-if="vagasStore.loading"
              class="spinner"
            />
            Aplicar Filtros
          </button>
        </div>
      </div>
    </template>

    <!-- Jobs Table -->
    <div class="bg-white shadow-lg border-2 border-gray-300 rounded-lg p-6">
      <div class="mb-4 flex justify-between items-center">
        <h3 class="text-xl font-semibold text-gray-900">
          📋 Vagas Encontradas
        </h3>
        <span class="text-sm text-gray-500">
          Mostrando {{ paginatedJobs.length }} de {{ totalJobs }} vagas (máximo 50 por consulta)
        </span>
      </div>

      <!-- Loading State -->
      <div
        v-if="vagasStore.loading"
        class="flex justify-center items-center py-8"
      >
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        <span class="ml-3 text-gray-600">Carregando vagas...</span>
      </div>

      <!-- Table -->
      <div
        v-else
        class="overflow-x-auto"
      >
        <!-- Empty State for No Jobs -->
        <div
          v-if="vagasStore.jobs.length === 0"
          class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center"
        >
          <div class="text-gray-400 text-6xl mb-4">
            🔍
          </div>
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            Nenhuma vaga encontrada
          </h3>
          <p class="text-gray-600">
            Tente ajustar os filtros ou alterar o período de busca para encontrar mais vagas.
          </p>
        </div>

        <!-- Jobs Table -->
        <div
          v-else
          class="border border-gray-300 rounded-lg"
        >
          <div class="max-h-96 overflow-y-auto">
            <table class="min-w-full divide-y divide-gray-300">
              <thead class="bg-gray-100 sticky top-0">
                <tr>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border-r border-gray-300"
                  >
                    Nível
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border-r border-gray-300"
                  >
                    Remoto
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border-r border-gray-300"
                  >
                    Título
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border-r border-gray-300"
                  >
                    Cargo
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border-r border-gray-300"
                  >
                    Data Publicação
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider border-r border-gray-300"
                  >
                    Localização
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider"
                  >
                    Tipo
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-300">
                <tr
                  v-for="job in paginatedJobs"
                  :key="job.job_id"
                  class="hover:bg-gray-50 cursor-pointer"
                  :class="{
                    'bg-blue-50':
                      vagasStore.selectedJob && vagasStore.selectedJob.job_id === job.job_id,
                  }"
                  @click="selectJob(job)"
                >
                  <td
                    class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 border-r border-gray-300"
                  >
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getSeniorityBadgeClass(job.seniority)"
                    >
                      {{ job.seniority || 'N/A' }}
                    </span>
                  </td>
                  <td
                    class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 border-r border-gray-300"
                  >
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
                  <td
                    class="px-4 py-4 text-sm text-gray-900 max-w-xs truncate border-r border-gray-300"
                  >
                    {{ truncateTitle(job.job_title) }}
                  </td>
                  <td
                    class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 border-r border-gray-300"
                  >
                    {{ job.search_position_query || 'N/A' }}
                  </td>
                  <td
                    class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 border-r border-gray-300"
                  >
                    {{ formatDate(job.job_posted_at_date) }}
                  </td>
                  <td
                    class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 border-r border-gray-300"
                  >
                    {{ formatLocation(job.job_city, job.job_state) }}
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-900">
                    {{ job.job_employment_type }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div
        v-if="totalPages > 1 && vagasStore.jobs.length > 0"
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
              <span class="font-medium">{{ totalJobs }}</span> resultados
              <span class="text-xs text-gray-500 ml-2">(máximo 50 por consulta)</span>
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
                <i class="fas fa-chevron-left" />
              </button>

              <template
                v-for="page in visiblePages"
                :key="page"
              >
                <button
                  v-if="page !== '...'"
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
                <i class="fas fa-chevron-right" />
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State for Job Details -->
    <div
      v-if="!vagasStore.selectedJob && !vagasStore.loading"
      class="mt-8 bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center"
    >
      <div class="text-gray-400 text-6xl mb-4">
        💼
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        Selecione uma vaga
      </h3>
      <p class="text-gray-600">
        Clique em uma vaga na tabela acima para ver os detalhes da vaga.
      </p>
    </div>

    <!-- Job Details Modal -->
    <div
      v-if="vagasStore.selectedJob"
      class="mt-8 bg-white shadow-lg rounded-lg overflow-hidden relative"
    >
      <div class="px-6 py-4 border-b border-gray-200">
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-semibold text-gray-900">
            Detalhes da Vaga
          </h3>
          <button
            class="text-gray-400 hover:text-gray-600"
            @click="clearSelectedJob"
          >
            <i class="fas fa-times" />
          </button>
        </div>
      </div>

      <div class="px-6 py-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <!-- Job Information -->
          <div>
            <h4 class="text-lg font-medium text-gray-900 mb-4">
              {{ vagasStore.selectedJob.job_title }}
            </h4>

            <div class="space-y-3">
              <div>
                <span class="text-sm font-medium text-gray-500">Empresa:</span>
                <span class="ml-2 text-sm text-gray-900">{{
                  vagasStore.selectedJob.employer_name
                }}</span>
              </div>

              <div>
                <span class="text-sm font-medium text-gray-500">Localização:</span>
                <span class="ml-2 text-sm text-gray-900">
                  {{
                    formatLocation(
                      vagasStore.selectedJob.job_city,
                      vagasStore.selectedJob.job_state
                    )
                  }}
                </span>
              </div>

              <div>
                <span class="text-sm font-medium text-gray-500">Remoto:</span>
                <span
                  class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="
                    vagasStore.selectedJob.job_is_remote
                      ? 'bg-green-100 text-green-800'
                      : 'bg-blue-100 text-blue-800'
                  "
                >
                  {{ vagasStore.selectedJob.job_is_remote ? 'Sim' : 'Não' }}
                </span>
              </div>

              <div v-if="vagasStore.selectedJob.seniority">
                <span class="text-sm font-medium text-gray-500">Senioridade:</span>
                <span class="ml-2 text-sm text-gray-900">{{
                  vagasStore.selectedJob.seniority
                }}</span>
              </div>

              <div>
                <span class="text-sm font-medium text-gray-500">Tipo de Contrato:</span>
                <span class="ml-2 text-sm text-gray-900">{{
                  vagasStore.selectedJob.job_employment_type
                }}</span>
              </div>

              <div>
                <span class="text-sm font-medium text-gray-500">Data de Publicação:</span>
                <span class="ml-2 text-sm text-gray-900">{{
                  formatDate(vagasStore.selectedJob.job_posted_at_date)
                }}</span>
              </div>

              <div v-if="vagasStore.selectedJob.job_publisher">
                <span class="text-sm font-medium text-gray-500">Canal:</span>
                <span class="ml-2 text-sm text-gray-900">{{
                  vagasStore.selectedJob.job_publisher
                }}</span>
              </div>
            </div>
          </div>

          <!-- Skills and Additional Info -->
          <div>
            <h5 class="text-md font-medium text-gray-900 mb-3">
              Skills Identificadas
            </h5>

            <div
              v-if="parseSkills(vagasStore.selectedJob.extracted_skills).length > 0"
              class="mb-4"
            >
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="skill in parseSkills(vagasStore.selectedJob.extracted_skills)"
                  :key="skill"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                >
                  {{ skill }}
                </span>
              </div>
            </div>
            <div
              v-else
              class="text-sm text-gray-500 mb-4"
            >
              Nenhuma skill identificada
            </div>

            <!-- Apply Options -->
            <div v-if="parseApplyOptions(vagasStore.selectedJob.apply_options).length > 0">
              <h5 class="text-md font-medium text-gray-900 mb-2">
                Opções de Candidatura
              </h5>
              <div class="space-y-2">
                <div
                  v-for="(option, index) in parseApplyOptions(vagasStore.selectedJob.apply_options)"
                  :key="index"
                  class="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div class="flex items-center space-x-3">
                    <span class="text-sm font-medium text-gray-700">{{ option.publisher }}</span>
                    <span
                      class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                      :class="
                        option.is_direct
                          ? 'bg-green-100 text-green-800'
                          : 'bg-blue-100 text-blue-800'
                      "
                    >
                      {{ option.is_direct ? 'Candidatura Direta' : 'Candidatura Externa' }}
                    </span>
                  </div>
                  <a
                    v-if="option.apply_link"
                    :href="option.apply_link"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-colors"
                  >
                    <i class="fas fa-external-link-alt mr-1" />
                    Candidatar
                  </a>
                </div>
              </div>
            </div>

            <!-- External Link -->
            <div class="mt-4">
              <a
                v-if="vagasStore.selectedJob.job_url"
                :href="vagasStore.selectedJob.job_url"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
              >
                <i class="fas fa-external-link-alt mr-2" />
                Ver vaga original
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- Welcome Popup -->
    <WelcomePopup />
  </BasePageLayout>
</template>

<script setup>
  import { ref, computed, onMounted, watch } from 'vue'
  import { useVagasStore } from '@/stores/vagas'
  import { NSelect, useMessage } from 'naive-ui'
  import { format, parseISO } from 'date-fns'
  import { ptBR } from 'date-fns/locale'
  import BasePageLayout from '@/components/common/BasePageLayout.vue'
  import WelcomePopup from '@/components/common/WelcomePopup.vue'

  // Store
  const vagasStore = useVagasStore()
  const message = useMessage()

  // Reactive data
  const selectedPosition = ref('') // Will be updated from store
  const selectedEmploymentType = ref('') // Will be updated from store
  const selectedRemote = ref(null) // Will be updated from store
  const selectedSeniority = ref('') // Will be updated from store
  const selectedCity = ref(null) // Will be updated from store
  const currentPage = ref(1)
  const itemsPerPage = 10 // Reduced since we only get 50 records max

  // Watch for jobs changes - removed auto-selection of first job
  watch(
    () => vagasStore.jobs,
    (newJobs) => {
      // We don't auto-select the first job anymore
      // Users need to explicitly click on a job to see its details
      console.log('Jobs updated, count:', newJobs?.length || 0)
    },
    { immediate: true }
  )

  // Computed properties
  const positionOptions = computed(() => {
    const options = [{ label: 'Todos os cargos', value: '' }]

    // Add available positions from the store or use defaults
    const availablePositions = vagasStore.availablePositions || [
      'Data Engineering',
      'Frontend',
      'Fullstack',
      'DevOps',
      'Data Scientist',
      'Backend',
      'Mobile',
      'QA',
      'UX/UI',
      'Product Manager',
    ]

    availablePositions.forEach((position) => {
      options.push({ label: position, value: position })
    })

    return options
  })

  const remoteOptions = computed(() => [
    { label: 'Todos', value: null },
    { label: 'Remoto', value: 'true' },
    { label: 'Presencial', value: 'false' },
  ])

  const employmentTypeOptions = computed(() => {
    const options = [{ label: 'Todos os tipos', value: '' }]

    // Add available employment types from the store or use defaults
    const availableEmploymentTypes = vagasStore.availableEmploymentTypes || [
      'CLT',
      'PJ',
      'Freelance',
      'Temporário',
      'Estágio',
      'Trainee',
      'Cooperado',
    ]

    availableEmploymentTypes.forEach((type) => {
      options.push({ label: type, value: type })
    })

    return options
  })

  const seniorityOptions = computed(() => {
    const options = [{ label: 'Todas as senioridades', value: '' }]

    // Add available seniorities from the store or use defaults
    const availableSeniorities = vagasStore.availableSeniorities || [
      'Junior',
      'Pleno',
      'Senior',
      'Lead',
      'Principal',
    ]

    availableSeniorities.forEach((seniority) => {
      options.push({ label: seniority, value: seniority })
    })

    return options
  })

  const cityOptions = computed(() => {
    // If remote is true, only show N/A option
    if (selectedRemote.value === 'true') {
      return [{ label: 'N/A', value: 'N/A' }]
    }

    const options = [{ label: 'Todas as cidades', value: null }]

    // Add available cities from the store
    const locationData = vagasStore.locationData || []
    const cities = [...new Set(locationData.map((loc) => loc.title))]
      .filter(Boolean)
      .sort((a, b) => a.localeCompare(b))

    cities.forEach((city) => {
      options.push({ label: city, value: city })
    })

    return options
  })

  // const filtersChanged = computed(() => {
  //   return (
  //     selectedPosition.value !== vagasStore.filters.search_position_query ||
  //     selectedEmploymentType.value !== vagasStore.filters.employment_type ||
  //     selectedRemote.value !== vagasStore.filters.job_is_remote ||
  //     selectedSeniority.value !== vagasStore.filters.seniority ||
  //     selectedCity.value !== vagasStore.filters.job_city
  //   )
  // })

  const totalJobs = computed(() => vagasStore.jobs.length)
  const totalPages = computed(() => Math.ceil(totalJobs.value / itemsPerPage))
  const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage)
  const endIndex = computed(() => Math.min(startIndex.value + itemsPerPage, totalJobs.value))

  const paginatedJobs = computed(() => {
    const start = startIndex.value
    const end = endIndex.value
    return vagasStore.jobs.slice(start, end)
  })

  const visiblePages = computed(() => {
    const pages = []
    const maxVisible = 5

    if (totalPages.value <= maxVisible) {
      for (let i = 1; i <= totalPages.value; i++) {
        pages.push(i)
      }
    } else {
      if (currentPage.value <= 3) {
        for (let i = 1; i <= 4; i++) {
          pages.push(i)
        }
        pages.push('...')
        pages.push(totalPages.value)
      } else if (currentPage.value >= totalPages.value - 2) {
        pages.push(1)
        pages.push('...')
        for (let i = totalPages.value - 3; i <= totalPages.value; i++) {
          pages.push(i)
        }
      } else {
        pages.push(1)
        pages.push('...')
        for (let i = currentPage.value - 1; i <= currentPage.value + 1; i++) {
          pages.push(i)
        }
        pages.push('...')
        pages.push(totalPages.value)
      }
    }

    return pages
  })

  // Methods
  const formatDate = (dateString) => {
    if (!dateString) {
      return 'N/A'
    }
    try {
      return format(parseISO(dateString), 'dd/MM/yyyy', { locale: ptBR })
    } catch {
      return dateString
    }
  }

  const formatLocation = (city, state) => {
    if (!city && !state) {
      return 'N/A'
    }
    if (city && state) {
      return `${city}, ${state}`
    }
    return city || state || 'N/A'
  }

  const truncateTitle = (title) => {
    if (!title) {
      return 'N/A'
    }
    const maxLength = Math.min(Math.floor(title.length * 0.7), 30)
    return title.length > maxLength ? `${title.substring(0, maxLength)}...` : title
  }

  const getSeniorityBadgeClass = (seniority) => {
    if (!seniority) {
      return 'bg-gray-100 text-gray-800'
    }

    const seniorityLower = seniority.toLowerCase()
    if (seniorityLower.includes('junior') || seniorityLower.includes('júnior')) {
      return 'bg-green-100 text-green-800'
    } else if (seniorityLower.includes('pleno') || seniorityLower.includes('mid')) {
      return 'bg-yellow-100 text-yellow-800'
    } else if (seniorityLower.includes('senior') || seniorityLower.includes('sênior')) {
      return 'bg-red-100 text-red-800'
    } else {
      return 'bg-gray-100 text-gray-800'
    }
  }

  const parseSkills = (skillsString) => {
    if (!skillsString) {
      return []
    }

    try {
      // If it's already an array, return it
      if (Array.isArray(skillsString)) {
        return skillsString
      }

      // If it's a string, try to parse it as JSON
      if (typeof skillsString === 'string') {
        const parsed = JSON.parse(skillsString)
        return Array.isArray(parsed) ? parsed : []
      }

      return []
    } catch (error) {
      console.error('Error parsing skills:', error)
      return []
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

  const onPositionChange = async (value) => {
    selectedPosition.value = value

    // When position changes, fetch updated locations and reset city filter
    await vagasStore.fetchFilteredLocations()
    selectedCity.value = null
  }

  const onCityChange = (value) => {
    selectedCity.value = value
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

  const onSeniorityChange = (value) => {
    selectedSeniority.value = value
  }

  const onEmploymentTypeChange = (value) => {
    selectedEmploymentType.value = value
  }

  const applyFilters = async () => {
    console.log('Applying filters:', {
      position: selectedPosition.value,
      employmentType: selectedEmploymentType.value,
      remote: selectedRemote.value,
      seniority: selectedSeniority.value,
      city: selectedCity.value,
    })

    vagasStore.setFilters({
      search_position_query: selectedPosition.value,
      employment_type: selectedEmploymentType.value,
      job_is_remote: selectedRemote.value,
      seniority: selectedSeniority.value,
      job_city: selectedCity.value,
    })

    try {
      await vagasStore.fetchVagasData()
      currentPage.value = 1

      console.log('Filters applied, data loaded:', vagasStore.jobs.length)
      message.success('Pesquisa realizada com sucesso!')
    } catch (error) {
      console.error('Error applying filters:', error)
      message.error(`Erro ao aplicar filtros: ${error.message || 'Erro desconhecido'}`)
    }
  }

  const onPeriodFilterChange = async (periodFilters) => {
    console.log('Period filter changed:', periodFilters)

    // Save current selected job if there is one for later comparison
    const currentSelectedJob = vagasStore.selectedJob ? { ...vagasStore.selectedJob } : null
    const currentSelectedJobId = currentSelectedJob?.job_id

    vagasStore.setPeriod(periodFilters)
    console.log('Updated filters in store:', vagasStore.filters)

    try {
      // Fetch the data 
      await vagasStore.fetchVagasData()
      currentPage.value = 1

      if (currentSelectedJobId && vagasStore.jobs.length > 0) {
        // Try to find the previously selected job in the new results
        const previouslySelectedJob = vagasStore.jobs.find(
          (job) => job.job_id === currentSelectedJobId
        )

        if (previouslySelectedJob) {
          // If the same job exists in the new results, keep it selected
          vagasStore.setSelectedJob(previouslySelectedJob)
          console.log('Preserved selection of job:', previouslySelectedJob.job_title)
        } else {
          // Job not found in new results, but we have jobs available
          // Try to find a similar job (same title and company) as a fallback
          const similarJob = vagasStore.jobs.find(
            (job) =>
              job.job_title === currentSelectedJob.job_title &&
              job.employer_name === currentSelectedJob.employer_name
          )

          if (similarJob) {
            // Found a similar job, select it
            vagasStore.setSelectedJob(similarJob)
            console.log('Found similar job, selected:', similarJob.job_title)
          } else {
            // No similar job found, clear selection
            vagasStore.setSelectedJob(null)
            console.log('Previously selected job not found in new results')
          }
        }
      } else if (vagasStore.jobs.length === 0) {
        // No jobs available
        vagasStore.setSelectedJob(null)
      }

      message.success('Período alterado com sucesso!')
    } catch (error) {
      console.error('Error during period filter change:', error)
      message.error(`Erro ao alterar período: ${error.message || 'Erro desconhecido'}`)
    }
  }

  const selectJob = (job) => {
    // If already selected, toggle off
    if (vagasStore.selectedJob && vagasStore.selectedJob.job_id === job.job_id) {
      vagasStore.setSelectedJob(null)
      return
    }

    vagasStore.setSelectedJob(job)
  }

  // Clear selected job
  const clearSelectedJob = () => {
    vagasStore.setSelectedJob(null)
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

  // Synchronize local reactive variables with store filters
  const syncFiltersFromStore = () => {
    const storeFilters = vagasStore.filters
    selectedPosition.value = storeFilters.search_position_query || ''
    selectedEmploymentType.value = storeFilters.employment_type || ''
    selectedRemote.value = storeFilters.job_is_remote
    selectedSeniority.value = storeFilters.seniority || ''
    selectedCity.value = storeFilters.job_city
  }

  // Lifecycle
  onMounted(async () => {
    // Initialize with default filters and load saved filters if available
    vagasStore.initializeWithDefaults()

    // Synchronize local reactive variables with store filters
    syncFiltersFromStore()

    // Fetch available positions, employment types, seniorities, and locations
    await Promise.all([
      vagasStore.fetchAvailablePositions(),
      vagasStore.fetchAvailableEmploymentTypes(),
      vagasStore.fetchAvailableSeniorities(),
      vagasStore.fetchFilteredLocations(),
    ])

    // Fetch data 
    await vagasStore.fetchVagasData()

    // The store now automatically clears selectedJob on initialization
    // Users need to explicitly click on a job to see its details
  })

  // Watch for filter changes
  watch(
    [selectedPosition, selectedEmploymentType, selectedRemote, selectedSeniority, selectedCity],
    () => {
      // Reset to first page when filters change
      currentPage.value = 1
    }
  )

  // Watch for store filter changes and sync local variables
  watch(
    () => vagasStore.filters,
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
