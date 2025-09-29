<template>
  <BasePageLayout
    title="Skills & Vagas"
    subtitle="Explore e analise vagas por skills específicos com filtros avançados"
    icon="💻"
    page-id="skills"
    :loading="skillsStore.loading"
    :error="skillsStore.error"
    :filters="skillsStore.filters"
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
            Skill
          </div>
          <NSelect
            v-model:value="selectedSkills"
            :options="skillOptions"
            class="filter-select"
            placeholder="Selecione skills"
            filterable
            multiple
            aria-label="Selecionar skills"
            @update:value="onSkillsChange"
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
            :disabled="skillsStore.loading"
            @click="applyFilters"
          >
            <span
              v-if="skillsStore.loading"
              class="spinner"
            />
            Aplicar Filtros
          </button>
        </div>
      </div>
    </template>

    <!-- Skills Table -->
    <div class="bg-white shadow-lg border-2 border-gray-300 rounded-lg p-6">
      <div class="mb-4 flex justify-between items-center">
        <h3 class="text-xl font-semibold text-gray-900">
          💻 Skills Encontradas
        </h3>
        <span class="text-sm text-gray-500">
          <span v-if="selectedSkills.length > 0">
            Mostrando {{ paginatedSkills.length }} de {{ totalSkills }} skills filtradas
          </span>
          <span v-else>
            Mostrando {{ paginatedSkills.length }} de {{ totalSkills }} skills (top 50 de
            {{ totalUniqueSkills }} total)
          </span>
        </span>
      </div>

      <!-- Loading State -->
      <div
        v-if="skillsStore.loading"
        class="flex justify-center items-center py-8"
      >
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        <span class="ml-3 text-gray-600">Carregando skills...</span>
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
                  Skill
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
                v-for="skill in paginatedSkills"
                :key="skill.skill_name"
                class="hover:bg-gray-50 cursor-pointer"
                :class="{
                  'bg-blue-50':
                    selectedSkillData && selectedSkillData.skill_name === skill.skill_name,
                }"
                @click="selectSkill(skill)"
              >
                <td class="px-4 py-4 text-sm text-gray-900 border-r border-gray-300">
                  {{ skill.skill_name }}
                </td>
                <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900 text-center">
                  <span
                    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800"
                  >
                    {{ skill.job_count }}
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
              <span class="font-medium">{{ totalSkills }}</span> resultados
              <span
                v-if="selectedSkills.length === 0"
                class="text-xs text-gray-500 ml-2"
              >(top 50 skills)</span>
              <span
                v-else
                class="text-xs text-gray-500 ml-2"
              >(skills filtradas)</span>
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

    <!-- Skill Details Section -->
    <div
      v-if="selectedSkillData"
      class="bg-white shadow-lg border-2 border-gray-300 rounded-lg p-6 mt-6"
    >
      <div class="mb-4">
        <h3 class="text-xl font-semibold text-gray-900">
          💻 {{ selectedSkillData.skill_name }}
        </h3>
        <p class="text-sm text-gray-600 mt-2">
          {{ skillJobs.length }}
          {{ skillJobs.length === 1 ? 'vaga disponível' : 'vagas disponíveis' }}
        </p>
      </div>

      <!-- Loading State for Details -->
      <div
        v-if="skillsStore.loadingDetails"
        class="flex justify-center items-center py-8"
      >
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
        <span class="ml-3 text-gray-600">Carregando detalhes...</span>
      </div>

      <!-- Skill Jobs Details -->
      <div
        v-else
        class="space-y-4"
      >
        <div
          v-for="job in skillJobs"
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
                  <span class="font-medium">Empresa:</span>
                  <span class="ml-2">{{ job.employer_name }}</span>
                </div>
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
              </div>

              <!-- Skills -->
              <div
                v-if="parseSkills(job.extracted_skills).length > 0"
                class="mt-3"
              >
                <span class="font-medium text-sm text-gray-700">Skills:</span>
                <div class="flex flex-wrap gap-2 mt-1">
                  <span
                    v-for="(skill, skillIndex) in parseSkills(job.extracted_skills)"
                    :key="skillIndex"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium"
                    :class="
                      skill.toLowerCase() === selectedSkillData.skill_name.toLowerCase()
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-gray-100 text-gray-800'
                    "
                  >
                    {{ skill }}
                  </span>
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
      v-if="!selectedSkillData && !skillsStore.loading"
      class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mt-6"
    >
      <div class="text-gray-400 text-6xl mb-4">
        💻
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        Selecione uma skill
      </h3>
      <p class="text-gray-600">
        Clique em uma skill na tabela acima para ver os detalhes das vagas disponíveis.
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
  import { useSkillsStore } from '@/stores/skills'
  import { format, parseISO } from 'date-fns'
  import { ptBR } from 'date-fns/locale'

  const skillsStore = useSkillsStore()
  const message = useMessage()

  // Reactive data
  const selectedPosition = ref('')
  const selectedSkills = ref([])
  const selectedRemote = ref('')
  const selectedSeniority = ref('')

  // Use computed for selectedSkillData to sync with store
  const selectedSkillData = computed({
    get: () => skillsStore.selectedSkill,
    set: (value) => {
      skillsStore.setSelectedSkill(value)
    },
  })
  const currentPage = ref(1)
  const itemsPerPage = 15

  // Synchronize local reactive variables with store filters
  const syncFiltersFromStore = () => {
    const storeFilters = skillsStore.filters
    selectedPosition.value = storeFilters.search_position_query || ''
    selectedSkills.value = storeFilters.skills || []
    selectedRemote.value = storeFilters.job_is_remote || ''
    selectedSeniority.value = storeFilters.seniority || ''
  }

  // Computed properties
  const positionOptions = computed(() => {
    const positions = skillsStore.availablePositions || []
    return [
      { label: 'Todos os cargos', value: '' },
      ...positions.map((pos) => ({ label: pos, value: pos })),
    ]
  })

  const skillOptions = computed(() => {
    const skills = skillsStore.availableSkills || []
    return skills.map((skill) => ({ label: skill, value: skill }))
  })

  const remoteOptions = ref([
    { label: 'Todos', value: '' },
    { label: 'Remoto', value: 'true' },
    { label: 'Presencial', value: 'false' },
  ])

  const seniorityOptions = computed(() => {
    const seniorities = skillsStore.availableSeniorities || []
    return [
      { label: 'Todas', value: '' },
      ...seniorities.map((seniority) => ({ label: seniority, value: seniority })),
    ]
  })

  // Aggregate skills from jobs data (limit top 50 for display)
  const aggregatedSkills = computed(() => skillsStore.getAggregatedSkills().slice(0, 50))

  // Total unique skills from available options (cheap) or selected list
  const totalUniqueSkills = computed(() => {
    if (selectedSkills.value && selectedSkills.value.length > 0) {
      return selectedSkills.value.length
    }
    return Array.isArray(skillsStore.availableSkills)
      ? skillsStore.availableSkills.length
      : aggregatedSkills.value.length
  })

  const totalSkills = computed(() => aggregatedSkills.value.length)
  const totalPages = computed(() => Math.ceil(totalSkills.value / itemsPerPage))

  const paginatedSkills = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage
    const end = start + itemsPerPage
    return aggregatedSkills.value.slice(start, end)
  })

  const startIndex = computed(() => (currentPage.value - 1) * itemsPerPage)
  const endIndex = computed(() => Math.min(startIndex.value + itemsPerPage, totalSkills.value))

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

  // Skill jobs for selected skill
  const skillJobs = computed(() => {
    if (!selectedSkillData.value) {
      return []
    }
    return skillsStore.getJobsForSkill(selectedSkillData.value.skill_name)
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

  // Lightweight memoization to avoid repeated JSON.parse per render
  const parsedSkillsCache = new Map()
  const parsedApplyOptionsCache = new Map()

  const parseSkills = (skillsString, cacheKey) => {
    const key = cacheKey ?? skillsString
    if (parsedSkillsCache.has(key)) {
      return parsedSkillsCache.get(key)
    }
    if (!skillsString) {
      return []
    }

    try {
      // If it's already an array, return it
      if (Array.isArray(skillsString)) {
        parsedSkillsCache.set(key, skillsString)
        return skillsString
      }

      // If it's a string, try to parse it as JSON
      if (typeof skillsString === 'string') {
        const parsed = JSON.parse(skillsString)
        const value = Array.isArray(parsed) ? parsed : []
        parsedSkillsCache.set(key, value)
        return value
      }

      return []
    } catch (error) {
      return []
    }
  }

  const parseApplyOptions = (applyOptionsString, cacheKey) => {
    const key = cacheKey ?? applyOptionsString
    if (parsedApplyOptionsCache.has(key)) {
      return parsedApplyOptionsCache.get(key)
    }
    if (!applyOptionsString) {
      return []
    }

    try {
      // If it's already an array, return it
      if (Array.isArray(applyOptionsString)) {
        parsedApplyOptionsCache.set(key, applyOptionsString)
        return applyOptionsString
      }

      // If it's a string, try to parse it as JSON
      if (typeof applyOptionsString === 'string') {
        const parsed = JSON.parse(applyOptionsString)
        const value = Array.isArray(parsed) ? parsed : []
        parsedApplyOptionsCache.set(key, value)
        return value
      }

      return []
    } catch (error) {
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

    // Reset other filters when position changes
    selectedSkills.value = []
    selectedRemote.value = ''
    selectedSeniority.value = ''

    // Do not update store filters here to avoid refreshing the table.
    // Store filters are only updated when the user clicks "Aplicar Filtros".

    // Only update available skills and seniority levels for the new position
    // Don't fetch table data - that should only happen when "Aplicar Filtros" is clicked
    try {
      await Promise.all([
        skillsStore.fetchAvailableSkillsForPosition(value || null),
        skillsStore.fetchAvailableSeniorityForPosition(value || null),
      ])
    } catch (error) {
      console.error('Error fetching position data:', error)
    }
  }

  const onSkillsChange = (value) => {
    // Update only local selection; table refresh happens on "Aplicar Filtros"
    selectedSkills.value = value
  }

  const onRemoteChange = (value) => {
    // Update only local selection; table refresh happens on "Aplicar Filtros"
    selectedRemote.value = value
  }

  const onSeniorityChange = (value) => {
    // Update only local selection; table refresh happens on "Aplicar Filtros"
    selectedSeniority.value = value
  }

  // Simple debounce helper
  let applyFiltersTimeout = null
  const applyFilters = async () => {
    if (applyFiltersTimeout) {
      clearTimeout(applyFiltersTimeout)
    }
    applyFiltersTimeout = setTimeout(async () => {
      skillsStore.setFilters({
        search_position_query: selectedPosition.value,
        skills: selectedSkills.value,
        job_is_remote: selectedRemote.value,
        seniority: selectedSeniority.value,
      })

      try {
        await skillsStore.fetchSkillsData()
        currentPage.value = 1
        selectedSkillData.value = null

        message.success('Pesquisa realizada com sucesso!')
      } catch (error) {
        message.error(`Erro ao aplicar filtros: ${error.message || 'Erro desconhecido'}`)
      }
    }, 300)
  }

  const onPeriodFilterChange = async (periodFilters) => {
    skillsStore.setPeriod(periodFilters)

    try {
      await skillsStore.fetchSkillsData()
      currentPage.value = 1
      selectedSkillData.value = null
      message.success('Período alterado com sucesso!')
    } catch (error) {
      message.error(`Erro ao alterar período: ${error.message || 'Erro desconhecido'}`)
    }
  }

  const selectSkill = async (skill) => {
    selectedSkillData.value = skill
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
      skillsStore.initializeWithDefaults()

      // Synchronize local reactive variables with store filters
      syncFiltersFromStore()

      // Fetch available positions first
      await skillsStore.fetchAvailableOptions()

      // Fetch skills and seniority levels for current selection (empty means all)
      const currentPosition = selectedPosition.value || null
      await Promise.all([
        skillsStore.fetchAvailableSkillsForPosition(currentPosition),
        skillsStore.fetchAvailableSeniorityForPosition(currentPosition),
      ])

      // Then fetch the initial data
      await skillsStore.fetchSkillsData()
    } catch (error) {
      // Continue loading even if some APIs fail - the store handles graceful degradation
    }
  })

  // Watch for store filter changes and sync local variables
  watch(
    () => skillsStore.filters,
    () => {
      syncFiltersFromStore()
    },
    { deep: true }
  )
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
</style>
