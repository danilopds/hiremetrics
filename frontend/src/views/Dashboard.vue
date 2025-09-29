<template>
  <BasePageLayout
    title="Dashboard do Mercado de Trabalho"
    subtitle="Visualize insights abrangentes sobre o mercado de trabalho atual"
    icon="🏠"
    page-id="dashboard"
    :loading="dashboardStore.loading"
    :error="dashboardStore.error"
    :filters="dashboardStore.filters"
    @period-change="onPeriodFilterChange"
  >
    <template #filter-bar>
      <!-- Filter Bar -->
      <FilterBar
        :positions="dashboardStore.availablePositions"
        :skills="dashboardStore.skillsDemand"
        :locations="dashboardStore.locationData"
        :initial-filters="dashboardStore.filters"
        :loading="dashboardStore.loading"
        @update:filters="onFiltersUpdate"
        @position-change="onPositionChange"
      />
    </template>

    <template #kpi-cards>
      <KpiCardRow>
        <!-- Total Jobs -->
        <KpiCard
          title="Total de Vagas"
          :value="dashboardStore.jobs.length"
          subtitle="anúncios"
          icon="fas fa-briefcase"
          color="blue"
        />

        <!-- Job Growth -->
        <KpiCard
          title="Crescimento de Vagas"
          :value="`${jobCountVariation.percent}%`"
          icon="fas fa-chart-line"
          :color="
            jobCountVariation.direction === 'up'
              ? 'green'
              : jobCountVariation.direction === 'down'
                ? 'red'
                : 'yellow'
          "
        >
          <template #trend>
            <div class="flex flex-col space-y-1">
              <div class="flex items-center">
                <span
                  :class="
                    jobCountVariation.direction === 'up'
                      ? 'text-green-600 font-semibold'
                      : jobCountVariation.direction === 'down'
                        ? 'text-red-600 font-semibold'
                        : 'text-gray-500'
                  "
                >
                  <i
                    :class="
                      jobCountVariation.direction === 'up'
                        ? 'fas fa-arrow-up'
                        : jobCountVariation.direction === 'down'
                          ? 'fas fa-arrow-down'
                          : 'fas fa-minus'
                    "
                  />
                  {{ jobCountVariation.message }}
                </span>
              </div>
              <div class="text-xs text-gray-400">
                {{ dashboardStore.currentPeriodJobsCount }} vs
                {{ dashboardStore.previousPeriodJobsCount }} vagas
              </div>
            </div>
          </template>
        </KpiCard>

        <!-- Active Companies -->
        <KpiCard
          title="Empresas Ativas"
          :value="activeCompanies"
          subtitle="empregadores"
          icon="fas fa-building"
          color="yellow"
        />
      </KpiCardRow>
    </template>

    <!-- Job Market Trends Chart -->
    <ChartCard
      title="Tendências do Mercado de Trabalho"
      description="Evolução das vagas publicadas ao longo do tempo"
      :loading="dashboardStore.loading"
      :error="dashboardStore.error"
      :has-data="dashboardStore.jobMarketTrends.length > 0"
      content-class="h-80"
    >
      <BaseLineChart :data="lineChartData" />
    </ChartCard>

    <!-- Remote vs On-site Jobs & Entities Overview Side by Side -->
    <div class="grid grid-cols-1 gap-8 lg:grid-cols-2">
      <ChartCard
        title="Vagas Remotas vs Presenciais"
        description="Distribuição de oportunidades de trabalho remotas e presenciais"
        :loading="dashboardStore.loading"
        :error="dashboardStore.error"
        :has-data="dashboardStore.jobs.length > 0"
        content-class="h-80"
      >
        <BasePieChart
          :data="remotePieChartData"
          :options="pieChartOptions"
        />
      </ChartCard>

      <ChartCard
        title="Visão Geral das Entidades"
        description="Comparação de empresas, canais de publicação e cargos no mercado"
        :loading="dashboardStore.loading"
        :error="dashboardStore.error"
        :has-data="dashboardStore.jobs.length > 0"
        content-class="h-80"
      >
        <BaseBarChart :data="entitiesBarChartData" />
      </ChartCard>
    </div>

    <!-- Top Cities -->
    <ChartCard
      title="Top 5 Cidades"
      description="Cidades com o maior número de oportunidades de trabalho"
      :loading="dashboardStore.loading"
      :error="dashboardStore.error"
      :has-data="dashboardStore.jobs.length > 0"
      content-class="h-80"
    >
      <BaseBarChart :data="topCitiesBarChartData" />
    </ChartCard>

    <!-- Job Distribution by Employment Type and Job Titles Side by Side -->
    <div class="grid grid-cols-1 gap-8 lg:grid-cols-2">
      <ChartCard
        title="Distribuição de Vagas por Tipo de Contrato"
        description="Divisão das vagas por tipo de contrato de trabalho"
        :loading="dashboardStore.loading"
        :error="dashboardStore.error"
        :has-data="dashboardStore.jobs.length > 0"
        content-class="h-80"
      >
        <BaseBarChart :data="employmentTypeBarChartData" />
      </ChartCard>

      <ChartCard
        title="Cargos"
        description="Cargos mais comuns nas vagas atuais"
        :loading="dashboardStore.loading"
        :error="dashboardStore.error"
        :has-data="dashboardStore.jobs.length > 0"
        content-class="h-80"
      >
        <div class="overflow-hidden rounded-lg border border-gray-200 h-full">
          <div class="overflow-y-auto h-full">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50 sticky top-0">
                <tr>
                  <th
                    class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider w-20"
                  >
                    Contagem
                  </th>
                  <th
                    class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                  >
                    Cargo
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr
                  v-for="item in sortedJobTitlesWithCount"
                  :key="item.title"
                >
                  <td class="px-4 py-4 text-sm text-gray-500 text-right w-20">
                    {{ item.count }}
                  </td>
                  <td
                    class="px-4 py-4 text-sm font-medium text-gray-900"
                    style="max-width: 70%"
                  >
                    <div
                      class="truncate"
                      :title="item.title"
                    >
                      {{ item.title }}
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </ChartCard>
    </div>

    <!-- Job Locations Map -->
    <ChartCard
      title="Mapa de Localizações das Vagas"
      description="Distribuição geográfica das oportunidades de trabalho"
      :loading="dashboardStore.loading"
      :error="dashboardStore.error"
      :has-data="dashboardStore.jobs.length > 0"
      content-class="h-96"
    >
      <MapLibreMap :filters="dashboardStore.filters" />
    </ChartCard>

    <!-- Welcome Popup -->
    <WelcomePopup />
  </BasePageLayout>
</template>

<script setup>
  import { computed, onMounted } from 'vue'

  defineOptions({
    name: 'DashboardPage',
  })
  import { useDashboardStore } from '@/stores/dashboard'
  import BaseLineChart from '@/components/charts/BaseLineChart.vue'
  import BaseBarChart from '@/components/charts/BaseBarChart.vue'
  import BasePieChart from '@/components/charts/BasePieChart.vue'
  import FilterBar from '@/components/filters/FilterBar.vue'
  import MapLibreMap from '@/components/maps/MapLibreMap.vue'
  import { format, parseISO } from 'date-fns'

  // Import new common components
  import BasePageLayout from '@/components/common/BasePageLayout.vue'
  import ChartCard from '@/components/common/ChartCard.vue'
  import KpiCard from '@/components/common/KpiCard.vue'
  import KpiCardRow from '@/components/common/KpiCardRow.vue'
  import WelcomePopup from '@/components/common/WelcomePopup.vue'
  import {
    formatRemotePieChartData,
    formatTopCitiesData,
    formatEmploymentTypeData,
    formatEntitiesOverviewData,
    createLineChartConfig,
  } from '@/utils/chartHelpers'

  const dashboardStore = useDashboardStore()
  // const user = authStore.user

  // ECharts data preparation
  const lineChartData = computed(() =>
    createLineChartConfig({
      dates: dashboardStore.jobMarketTrends.map((item) => format(parseISO(item.date), 'MMM d')),
      values: dashboardStore.jobMarketTrends.map((item) => item.count),
      seriesName: 'Vagas Publicadas',
      color: '#3b82f6',
    })
  )

  const topCitiesBarChartData = computed(() => formatTopCitiesData(dashboardStore.jobs))
  const employmentTypeBarChartData = computed(() => formatEmploymentTypeData(dashboardStore.jobs))
  const remotePieChartData = computed(() => formatRemotePieChartData(dashboardStore.jobs))
  const entitiesBarChartData = computed(() => formatEntitiesOverviewData(dashboardStore.jobs))

  const pieChartOptions = {
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
  }

  // Job titles aggregation
  const sortedJobTitlesWithCount = computed(() => {
    const titleCounts = {}
    dashboardStore.jobs.forEach((job) => {
      if (!job.job_title) {
        return
      }
      titleCounts[job.job_title] = (titleCounts[job.job_title] || 0) + 1
    })

    return Object.entries(titleCounts)
      .map(([title, count]) => ({ title, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 30) // Top 30 titles
  })

  const jobCountVariation = computed(() => {
    const current = dashboardStore.currentPeriodJobsCount
    const previous = dashboardStore.previousPeriodJobsCount

    // Always show comparison, even when previous period has no data
    if (previous === 0) {
      if (current === 0) {
        return {
          percent: '0.0',
          direction: 'neutral',
          rawPercent: 0,
          message: 'Sem alteração',
        }
      }
      return {
        percent: '+100.0',
        direction: 'up',
        rawPercent: 100,
        message: 'Crescimento vs período anterior',
      }
    }

    const percent = ((current - previous) / previous) * 100
    const direction = percent > 0 ? 'up' : percent < 0 ? 'down' : 'neutral'
    const sign = percent > 0 ? '+' : '' // negative sign is automatically included by toFixed for negative numbers

    return {
      percent: `${sign}${percent.toFixed(1)}`,
      direction,
      rawPercent: percent,
      message:
        direction === 'up'
          ? 'Crescimento vs período anterior'
          : direction === 'down'
            ? 'Declínio vs período anterior'
            : 'Sem alteração',
    }
  })

  // Active companies - moved to computed to maintain reactivity
  const activeCompanies = computed(() => {
    const employers = new Set()
    dashboardStore.jobs.forEach((job) => {
      if (job.employer_name) {
        employers.add(job.employer_name)
      }
    })
    return employers.size
  })

  const onPeriodFilterChange = (periodFilters) => {
    // Merge period filters with existing filters to avoid overwriting other filters
    const mergedFilters = {
      ...dashboardStore.filters,
      ...periodFilters,
    }
    dashboardStore.setFilters(mergedFilters)
    dashboardStore.fetchDashboardData()
  }

  const onFiltersUpdate = (newFilters) => {
    dashboardStore.setFilters(newFilters)
    dashboardStore.fetchDashboardData()
  }

  const onPositionChange = async (positionFilters) => {
    // Update position filter
    dashboardStore.setFilters({ ...dashboardStore.filters, ...positionFilters })

    // Fetch filtered locations based on new position
    await dashboardStore.fetchFilteredLocations()
  }

  onMounted(async () => {
    // Only initialize defaults if no date range is set
    if (!dashboardStore.filters.dateFrom || !dashboardStore.filters.dateTo) {
      dashboardStore.initializeWithDefaults()
    }

    // Initial load
    await dashboardStore.fetchAvailablePositions()
    await dashboardStore.fetchDashboardData()
  })
</script>
