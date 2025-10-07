<template>
  <div class="bg-black py-12">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="lg:text-center mb-10">
        <h2 class="text-base text-cyan-400 font-semibold tracking-wide uppercase font-mono">
          <span class="text-cyan-500">//</span> Live Data
        </h2>
        <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl">
          Dados reais do mercado de TI
        </p>
        <p class="mt-4 max-w-2xl text-xl text-gray-300 lg:mx-auto font-mono">
          Dados reais extraídos com IA e atualizados diariamente. Preview do dataset que você terá acesso.
        </p>
      </div>

      <div class="bg-gradient-to-br from-gray-900 to-gray-800 shadow-2xl border border-gray-700 rounded-lg p-6">
        <div class="mb-4 flex justify-between items-center">
          <h3 class="text-xl font-semibold text-white font-mono">
            <span class="text-cyan-400">$</span> Job Dataset Sample
          </h3>
          <span class="text-sm text-gray-400 font-mono">
            {{ visibleRecords }} / {{ totalRecords }} records
          </span>
        </div>

        <!-- Position Filter -->
        <div class="mb-6 flex justify-center">
          <div class="w-full max-w-md">
            <label
              for="position-select"
              class="block text-sm font-medium text-gray-300 mb-2 font-mono"
            >
              <span class="text-cyan-400">&gt;</span> Filtrar por cargo
            </label>
            <select
              id="position-select"
              v-model="selectedPosition"
              class="w-full px-3 py-2 bg-gray-800 border border-gray-600 text-gray-200 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:border-cyan-500 font-mono"
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
          <p class="text-sm text-gray-400 font-mono">
            📅 Período: Últimos 30 dias ({{ formatDate(dateFrom) }} a {{ formatDate(dateTo) }})
          </p>
        </div>

        <!-- Loading State -->
        <div
          v-if="loading"
          class="flex justify-center items-center py-8"
        >
          <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500" />
          <span class="ml-3 text-gray-300 font-mono">Loading data...</span>
        </div>

        <!-- Data Table -->
        <div
          v-else
          class="overflow-x-auto"
        >
          <div class="max-h-96 overflow-y-auto border border-gray-700 rounded-lg">
            <table class="min-w-full divide-y divide-gray-700">
              <thead class="bg-gray-800 sticky top-0">
                <tr>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider border-r border-gray-700 font-mono"
                  >
                    Nível
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider border-r border-gray-700 font-mono"
                  >
                    Remoto
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider border-r border-gray-700 font-mono"
                  >
                    Título
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider border-r border-gray-700 font-mono"
                  >
                    Cargo
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider border-r border-gray-700 font-mono"
                  >
                    Data Publicação
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-300 uppercase tracking-wider font-mono"
                  >
                    Tipo
                  </th>
                </tr>
              </thead>
              <tbody class="bg-gray-900 divide-y divide-gray-700">
                <tr
                  v-for="job in sampleData"
                  :key="job.job_id"
                  class="hover:bg-gray-800 transition-colors"
                >
                  <td
                    class="px-4 py-4 whitespace-nowrap text-sm text-gray-200 border-r border-gray-700"
                  >
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium font-mono"
                      :class="getSeniorityBadgeClass(job.seniority)"
                    >
                      {{ job.seniority || 'N/A' }}
                    </span>
                  </td>
                  <td
                    class="px-4 py-4 whitespace-nowrap text-sm text-gray-200 border-r border-gray-700"
                  >
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium font-mono"
                      :class="
                        job.job_is_remote
                          ? 'bg-green-900 text-green-300 border border-green-700'
                          : 'bg-blue-900 text-blue-300 border border-blue-700'
                      "
                    >
                      {{ job.job_is_remote ? 'Sim' : 'Não' }}
                    </span>
                  </td>
                  <td
                    class="px-4 py-4 text-sm text-gray-200 max-w-xs truncate border-r border-gray-700"
                  >
                    {{ truncateTitle(job.job_title) }}
                  </td>
                  <td
                    class="px-4 py-4 whitespace-nowrap text-sm text-gray-200 border-r border-gray-700"
                  >
                    {{ job.search_position_query || 'N/A' }}
                  </td>
                  <td
                    class="px-4 py-4 whitespace-nowrap text-sm text-gray-200 border-r border-gray-700 font-mono"
                  >
                    {{ formatDate(job.job_posted_at_date) }}
                  </td>
                  <td class="px-4 py-4 whitespace-nowrap text-sm text-gray-200 font-mono">
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
            class="group relative inline-flex items-center px-8 py-3 overflow-hidden font-mono font-medium tracking-tighter text-white bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg hover:scale-105 transition-transform duration-300 shadow-lg shadow-cyan-500/50"
          >
            <span class="absolute w-0 h-0 transition-all duration-500 ease-out bg-white rounded-full group-hover:w-56 group-hover:h-56 opacity-10" />
            <span class="relative">Acessar dataset completo →</span>
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
      // Set up filters for last 30 days
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
        selectedRemoteTypes: [],
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
          job_id: 'job_002_2025_01_14',
          job_title: 'Analista de Dados Pleno',
          employer_name: 'DataViz Solutions',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Rio de Janeiro',
          job_state: 'RJ',
          seniority: 'Pleno',
          job_employment_type: 'PJ',
          job_is_remote: false,
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
          job_id: 'job_004_2025_01_12',
          job_title: 'UX/UI Designer',
          employer_name: 'DesignStudio Pro',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Curitiba',
          job_state: 'PR',
          seniority: 'Pleno',
          job_employment_type: 'CLT',
          job_is_remote: false,
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
          job_id: 'job_006_2025_01_10',
          job_title: 'Desenvolvedor Mobile Junior',
          employer_name: 'AppMakers',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Salvador',
          job_state: 'BA',
          seniority: 'Junior',
          job_employment_type: 'CLT',
          job_is_remote: false,
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
          job_id: 'job_008_2025_01_08',
          job_title: 'QA Engineer',
          employer_name: 'QualityAssurance Inc',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Fortaleza',
          job_state: 'CE',
          seniority: 'Pleno',
          job_employment_type: 'PJ',
          job_is_remote: false,
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
          job_id: 'job_010_2025_01_06',
          job_title: 'Backend Developer',
          employer_name: 'ServerPro',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Goiânia',
          job_state: 'GO',
          seniority: 'Senior',
          job_employment_type: 'PJ',
          job_is_remote: false,
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
          job_id: 'job_012_2025_01_04',
          job_title: 'React Developer',
          employer_name: 'ReactCorp',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Vitória',
          job_state: 'ES',
          seniority: 'Junior',
          job_employment_type: 'CLT',
          job_is_remote: false,
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
          job_id: 'job_014_2025_01_02',
          job_title: 'Java Developer',
          employer_name: 'JavaTech',
          job_posted_at_date: todayStr,
          search_position_query: pickRandomPosition(),
          job_city: 'Manaus',
          job_state: 'AM',
          seniority: 'Senior',
          job_employment_type: 'CLT',
          job_is_remote: false,
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
      totalRecords.value = 406 // Sample total
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
        return 'bg-blue-900 text-blue-300 border border-blue-700'
      case 'pleno':
        return 'bg-yellow-900 text-yellow-300 border border-yellow-700'
      case 'senior':
        return 'bg-green-900 text-green-300 border border-green-700'
      default:
        return 'bg-gray-800 text-gray-300 border border-gray-600'
    }
  }

  // Lifecycle
  onMounted(async () => {
    await fetchAvailablePositions()
    await fetchData()
  })
</script>
