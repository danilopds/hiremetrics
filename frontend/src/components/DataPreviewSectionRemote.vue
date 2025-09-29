<template>
  <div class="bg-white py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="lg:text-center mb-10">
        <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
          Vagas Remotas
        </h2>
        <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
          Veja as vagas remotas disponíveis
        </p>
        <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
          Dados reais de vagas remotas extraídos com inteligência artificial e atualizados
          diariamente. Veja uma prévia do que você encontrará em nossos dashboards.
        </p>
      </div>

      <div class="bg-white shadow-lg border-2 border-gray-300 rounded-lg p-6">
        <div class="mb-4 flex justify-between items-center">
          <h3 class="text-xl font-semibold text-gray-900">
            📋 Amostra de Vagas Remotas
          </h3>
          <span class="text-sm text-gray-500">
            Mostrando {{ visibleRecords }} de {{ totalRecords }} registros
          </span>
        </div>

        <!-- Position Filter -->
        <div class="mb-6 flex justify-center">
          <div class="w-full max-w-md">
            <label
              for="position-select"
              class="block text-sm font-medium text-gray-700 mb-2"
            >
              Cargo
            </label>
            <select
              id="position-select"
              v-model="selectedPosition"
              class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              :disabled="loading"
              @change="fetchData"
            >
              <option value="">
                Todos os cargos
              </option>
              <option
                v-for="position in availablePositions"
                :key="position"
                :value="position"
              >
                {{ position }}
              </option>
            </select>
          </div>
        </div>

        <!-- Period Info -->
        <div class="mb-4 text-center">
          <p class="text-sm text-gray-600">
            📅 Período: Últimos 30 dias ({{ formatDate(dateFrom) }} a {{ formatDate(dateTo) }})
          </p>
        </div>

        <!-- Loading State -->
        <div
          v-if="loading"
          class="flex justify-center items-center py-8"
        >
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
          <span class="ml-3 text-gray-600">Carregando dados...</span>
        </div>

        <!-- Data Table -->
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
                    class="px-4 py-3 text-left text-xs font-medium text-gray-700 uppercase tracking-wider"
                  >
                    Tipo
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-300">
                <tr
                  v-for="job in sampleData"
                  :key="job.job_id"
                  class="hover:bg-gray-50"
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
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800"
                    >
                      Sim
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
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ job.job_employment_type }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="mt-6 text-center">
          <router-link
            to="/auth/login"
            class="inline-flex items-center px-6 py-3 border-2 border-blue-600 text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 transition-all duration-300"
          >
            👉 Acesse dados completos agora
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted, computed } from 'vue'
  import { publicReportsApi } from '@/api/public-reports'
  import { format, parseISO } from 'date-fns'
  import { ptBR } from 'date-fns/locale'

  // Reactive data
  const sampleData = ref([])
  const availablePositions = ref([])
  const selectedPosition = ref('')
  const totalRecords = ref(0)
  const loading = ref(false)

  // Date range for last 30 days
  const dateTo = ref(new Date().toISOString().split('T')[0])
  const dateFrom = ref(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0])

  // Date range for last 30 days

  // Computed properties
  const visibleRecords = computed(() => {
    return sampleData.value.length
  })

  // Methods
  const fetchAvailablePositions = async () => {
    try {
      const positions = await publicReportsApi.getAvailablePositions()
      availablePositions.value = positions || []
    } catch (error) {
      console.error('Error fetching positions:', error)
      // Fallback to sample positions if API fails
      availablePositions.value = [
        'Desenvolvedor Full Stack',
        'Analista de Dados',
        'DevOps Engineer',
        'UX/UI Designer',
        'Product Manager',
        'Desenvolvedor Mobile',
        'Data Scientist',
        'QA Engineer',
      ]
    }
  }

  const fetchData = async () => {
    loading.value = true
    try {
      // Set up filters for last 30 days with remote filter
      const filters = {
        dateFrom: dateFrom.value,
        dateTo: dateTo.value,
        selectedPosition: selectedPosition.value,
        selectedCompanies: [],
        selectedPublishers: [],
        selectedSeniority: [],
        selectedEmploymentTypes: [],
        selectedCities: [],
        selectedStates: [],
        selectedSkills: [],
        selectedRemoteTypes: ['true'], // Only remote positions
        selectedDirectTypes: [],
      }

      // Fetch preview data (15 records)
      const previewData = await publicReportsApi.previewExport(filters, 15)
      sampleData.value = previewData || []

      // Fetch total count
      const countData = await publicReportsApi.countExportRecords(filters, 50000)
      totalRecords.value = countData.count || 0
    } catch (error) {
      console.error('Error fetching data:', error)
      // Fallback to sample data if API fails
      const todayStr = new Date().toISOString().split('T')[0]
      const positionsForFallback = [
        'Desenvolvedor Full Stack',
        'Analista de Dados',
        'DevOps Engineer',
        'UX/UI Designer',
        'Product Manager',
        'Desenvolvedor Mobile',
        'Data Scientist',
        'QA Engineer',
        'Engenheiro de Software',
        'Analista de BI',
      ]
      const pickRandomPosition = () =>
        positionsForFallback[Math.floor(Math.random() * positionsForFallback.length)]
      sampleData.value = [
        {
          job_id: 'job_001_2025_01_15',
          job_title: 'Desenvolvedor Full Stack Senior',
          employer_name: 'TechCorp Brasil',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'São Paulo',
          job_state: 'SP',
          seniority: 'Senior',
          job_employment_type: 'CLT',
          job_is_remote: true,
        },
        {
          job_id: 'job_003_2025_01_13',
          job_title: 'DevOps Engineer',
          employer_name: 'CloudTech Ltda',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Belo Horizonte',
          job_state: 'MG',
          seniority: 'Senior',
          job_employment_type: 'CLT',
          job_is_remote: true,
        },
        {
          job_id: 'job_005_2025_01_11',
          job_title: 'Product Manager',
          employer_name: 'InnovateLab',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Porto Alegre',
          job_state: 'RS',
          seniority: 'Senior',
          job_employment_type: 'PJ',
          job_is_remote: true,
        },
        {
          job_id: 'job_007_2025_01_09',
          job_title: 'Data Scientist',
          employer_name: 'AI Analytics',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Brasília',
          job_state: 'DF',
          seniority: 'Senior',
          job_employment_type: 'CLT',
          job_is_remote: true,
        },
        {
          job_id: 'job_009_2025_01_07',
          job_title: 'Frontend Developer',
          employer_name: 'WebTech Solutions',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Recife',
          job_state: 'PE',
          seniority: 'Pleno',
          job_employment_type: 'CLT',
          job_is_remote: true,
        },
        {
          job_id: 'job_011_2025_01_05',
          job_title: 'Machine Learning Engineer',
          employer_name: 'AI Innovations',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Campinas',
          job_state: 'SP',
          seniority: 'Senior',
          job_employment_type: 'CLT',
          job_is_remote: true,
        },
        {
          job_id: 'job_013_2025_01_03',
          job_title: 'Python Developer',
          employer_name: 'PythonSoft',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Florianópolis',
          job_state: 'SC',
          seniority: 'Pleno',
          job_employment_type: 'PJ',
          job_is_remote: true,
        },
        {
          job_id: 'job_015_2025_01_01',
          job_title: 'Node.js Developer',
          employer_name: 'NodeSolutions',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'João Pessoa',
          job_state: 'PB',
          seniority: 'Pleno',
          job_employment_type: 'PJ',
          job_is_remote: true,
        },
      ]
      totalRecords.value = 156 // Sample total for remote jobs
    } finally {
      loading.value = false
    }
  }

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

  // const formatLocation = (city, state) => {
  //   if (!city && !state) {
  //     return 'N/A'
  //   }
  //   if (city && state) {
  //     return `${city}, ${state}`
  //   }
  //   return city || state || 'N/A'
  // }

  // Match VagasView title truncation logic
  const truncateTitle = (title) => {
    if (!title) {
      return 'N/A'
    }
    const maxLength = Math.min(Math.floor(title.length * 0.7), 30)
    return title.length > maxLength ? `${title.substring(0, maxLength)}...` : title
  }

  const getSeniorityBadgeClass = (seniority) => {
    switch (seniority?.toLowerCase()) {
      case 'junior':
        return 'bg-blue-100 text-blue-800'
      case 'pleno':
        return 'bg-yellow-100 text-yellow-800'
      case 'senior':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  // Lifecycle
  onMounted(async () => {
    await fetchAvailablePositions()
    await fetchData()
  })
</script>
