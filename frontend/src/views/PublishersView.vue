<template>
  <BasePageLayout
    title="Canais de Publicação"
    subtitle="Análise dos canais onde as vagas são publicadas e suas características"
    icon="🔗"
    page-id="publishers"
    :loading="publishersStore.loading.kpis"
    :error="publishersStore.errors.kpis"
    :filters="publishersStore.filters"
    @period-change="onFilterChange"
  >
    <template #filter-bar>
      <!-- Advanced Filter Bar -->
      <PublishersAdvancedFilterBar
        :positions="publishersStore.availablePositions"
        :publishers="publishersStore.availablePublishers"
        :seniority-levels="publishersStore.availableSeniorityLevels"
        :companies="publishersStore.availableCompanies"
        :initial-filters="publishersStore.filters"
        :loading="publishersStore.loading.availableOptions"
        @update:filters="onAdvancedFiltersUpdate"
        @position-change="onPositionChange"
      />
    </template>

    <template #kpi-cards>
      <KpiCardRow>
        <!-- Total Publishers -->
        <KpiCard
          title="Publishers Únicos"
          :value="publishersStore.kpis.totalPublishers"
          subtitle="canais de divulgação"
          icon="fas fa-broadcast-tower"
          color="blue"
        />

        <!-- Average Publishers per Job -->
        <KpiCard
          title="Média de Publishers por Vaga"
          :value="publishersStore.kpis.avgPublishersPerJob"
          subtitle="canais por vaga"
          icon="fas fa-chart-line"
          color="green"
        />

        <!-- Biggest Coverage -->
        <KpiCard
          title="Maior Cobertura"
          :value="publishersStore.kpis.biggestCoveragePublisher || 'N/A'"
          :subtitle="`(${publishersStore.kpis.biggestCoverageCount} vagas)`"
          icon="fas fa-trophy"
          color="yellow"
        />

        <!-- Direct Application Percentage -->
        <KpiCard
          title="Aplicação Direta"
          :value="`${publishersStore.kpis.directPercentage}%`"
          subtitle="das vagas"
          icon="fas fa-percentage"
          color="purple"
        />
      </KpiCardRow>
    </template>

    <!-- Top Publishers Chart -->
    <ChartCard
      title="Top 15 Publishers por Volume"
      description="Publishers com maior número de vagas únicas"
      :loading="publishersStore.loading.topPublishers"
      :error="publishersStore.errors.topPublishers"
      :has-data="topPublishersChartData.series && topPublishersChartData.series.length > 0"
      content-class="h-80"
    >
      <BaseBarChart :data="topPublishersChartData" />
    </ChartCard>

    <!-- Direct vs Indirect Distribution -->
    <ChartCard
      title="Distribuição por Tipo de Aplicação"
      description="Proporção de aplicações diretas vs indiretas"
      :loading="publishersStore.loading.directVsIndirect"
      :error="publishersStore.errors.directVsIndirect"
      :has-data="directVsIndirectChartData.length > 0"
      content-class="h-80"
    >
      <BasePieChart :data="directVsIndirectChartData" />
    </ChartCard>

    <!-- Seniority Distribution Chart -->
    <ChartCard
      title="Distribuição de Senioridade por Publisher"
      description="Como cada publisher distribui vagas por nível de senioridade"
      :loading="publishersStore.loading.seniorityDistribution"
      :error="publishersStore.errors.seniorityDistribution"
      :has-data="
        seniorityDistributionChartData.series && seniorityDistributionChartData.series.length > 0
      "
      content-class="h-80"
    >
      <BaseBarChart :data="seniorityDistributionChartData" />
    </ChartCard>

    <!-- Publishers Timeline Chart -->
    <ChartCard
      title="Vagas Publicadas por Publisher (Cumulativo)"
      description="Evolução cumulativa das publicações dos top 5 publishers ao longo do tempo"
      :loading="publishersStore.loading.timeline"
      :error="publishersStore.errors.timeline"
      :has-data="timelineChartData.series && timelineChartData.series.length > 0"
      content-class="h-80"
    >
      <BaseLineChart :data="timelineChartData" />
    </ChartCard>

    <!-- Companies-Publishers Matrix -->
    <ChartCard
      title="Publishers mais Usados por Empresas"
      description="Mapa de calor mostrando quais publishers cada empresa utiliza mais"
      :loading="publishersStore.loading.companiesMatrix"
      :error="publishersStore.errors.companiesMatrix"
      :has-data="companiesMatrixData.data && companiesMatrixData.data.length > 0"
      content-class="h-96"
      min-height="400px"
      overflow="auto"
    >
      <BaseHeatmap
        :data="companiesMatrixData.data"
        :x-axis-data="companiesMatrixData.publishers"
        :y-axis-data="companiesMatrixData.companies"
        height="400px"
      />
    </ChartCard>
  </BasePageLayout>
</template>

<script setup>
  import { computed, onMounted } from 'vue'
  import { usePublishersStore } from '@/stores/publishers'
  import PublishersAdvancedFilterBar from '@/components/filters/PublishersAdvancedFilterBar.vue'
  import BaseBarChart from '@/components/charts/BaseBarChart.vue'
  import BaseLineChart from '@/components/charts/BaseLineChart.vue'
  import BasePieChart from '@/components/charts/BasePieChart.vue'
  import BaseHeatmap from '@/components/charts/BaseHeatmap.vue'
  import { format, parseISO } from 'date-fns'

  // Import new common components
  import BasePageLayout from '@/components/common/BasePageLayout.vue'
  import ChartCard from '@/components/common/ChartCard.vue'
  import KpiCard from '@/components/common/KpiCard.vue'
  import KpiCardRow from '@/components/common/KpiCardRow.vue'

  const publishersStore = usePublishersStore()

  // Initialize only if no date filters exist yet
  onMounted(async () => {
    // Only initialize defaults if no date range is set
    if (!publishersStore.filters.dateFrom || !publishersStore.filters.dateTo) {
      publishersStore.initializeWithDefaults()
    }
    publishersStore.fetchAvailableOptions()
    publishersStore.fetchAllData()
  })

  const topPublishersChartData = computed(() => {
    const data = publishersStore.topPublishers.slice(0, 15) // Top 15 for better visualization

    // Sort data by unique jobs count in descending order (highest to lowest)
    const sortedData = [...data].sort((a, b) => b.unique_jobs_count - a.unique_jobs_count)

    // Get top 3 job counts for coloring (highest values)
    const top3JobCounts = sortedData.slice(0, 3).map((item) => item.unique_jobs_count)

    // Function to get color based on job count ranking
    const getBarColor = (jobCount) => {
      const rank = top3JobCounts.indexOf(jobCount)
      if (rank === 0) {
        return '#FFD700'
      } // Gold for 1st
      if (rank === 1) {
        return '#C0C0C0'
      } // Silver for 2nd
      if (rank === 2) {
        return '#CD7F32'
      } // Bronze for 3rd
      return '#3b82f6' // Blue for others
    }

    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
      },
      grid: {
        left: '1%', // Responsive space for publisher names (scales with screen)
        right: '10%', // Responsive space for value labels
        top: '15px', // Minimal top margin for tight spacing
        bottom: '10%', // Responsive bottom space for axis label
        containLabel: true, // Ensures labels stay within chart boundaries
      },
      xAxis: {
        type: 'value',
        name: 'Número de Vagas Únicas',
      },
      yAxis: {
        type: 'category',
        data: sortedData.map((item) => item.publisher),
        inverse: true, // Reverse the axis order to show highest at top
        axisLabel: {
          interval: 0,
          overflow: 'truncate',
          fontSize: 11,
          margin: 8,
        },
      },
      series: [
        {
          name: 'Vagas Únicas',
          type: 'bar',
          data: sortedData.map((item) => ({
            value: item.unique_jobs_count,
            itemStyle: { color: getBarColor(item.unique_jobs_count) },
          })),
          label: {
            show: true,
            position: 'right',
            formatter: '{c}',
          },
        },
      ],
    }
  })

  const directVsIndirectChartData = computed(() => {
    return publishersStore.directVsIndirect.map((item) => ({
      name: item.application_type,
      value: item.count,
    }))
  })

  const seniorityDistributionChartData = computed(() => {
    const { seniorities, data } = publishersStore.seniorityChartData

    // Get top 10 publishers by volume from topPublishers data
    const topPublishers = publishersStore.topPublishers.slice(0, 10).map((item) => item.publisher)

    // Filter data to only include top publishers
    const filteredData = data.filter((item) => topPublishers.includes(item.publisher))

    const colorPalette = [
      '#3b82f6',
      '#10b981',
      '#f59e0b',
      '#ef4444',
      '#8b5cf6',
      '#06b6d4',
      '#84cc16',
      '#f97316',
    ]

    const series = seniorities.map((seniority, idx) => ({
      name: seniority,
      type: 'bar',
      stack: 'total',
      data: filteredData.map((item) => item[seniority] || 0),
      itemStyle: { color: colorPalette[idx % colorPalette.length] },
    }))

    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
      },
      legend: {
        data: seniorities,
        top: 0,
      },
      xAxis: {
        type: 'category',
        data: topPublishers, // Use top 10 publishers by volume
        axisLabel: {
          interval: 0,
          rotate: 45,
          overflow: 'truncate',
        },
      },
      yAxis: {
        type: 'value',
        name: 'Número de Vagas',
      },
      series: series,
    }
  })

  const timelineChartData = computed(() => {
    const { dates, series } = publishersStore.timelineChartData

    // Get top 5 publishers by volume from topPublishers data
    const topPublishers = publishersStore.topPublishers.slice(0, 5).map((item) => item.publisher)

    // Filter series to only include top 5 publishers
    const filteredSeries = series.filter((s) => topPublishers.includes(s.name))

    // Format dates in the 'MMM d' format
    const formattedDates = dates.map((date) => format(parseISO(date), 'MMM d'))

    return {
      tooltip: {
        trigger: 'axis',
      },
      legend: {
        data: filteredSeries.map((s) => s.name),
        top: 0,
      },
      xAxis: {
        type: 'category',
        data: formattedDates,
        axisLabel: {
          rotate: 45,
        },
      },
      yAxis: {
        type: 'value',
        name: 'Vagas Acumuladas',
      },
      series: filteredSeries.map((s) => ({
        ...s,
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
      })),
    }
  })

  const companiesMatrixData = computed(() => publishersStore.companiesMatrixData)

  function onFilterChange(newFilters) {
    // Period filters update - merge with existing advanced filters
    const mergedFilters = {
      ...publishersStore.filters,
      ...newFilters,
    }
    publishersStore.setFilters(mergedFilters)
    publishersStore.fetchAllData()
  }

  function onAdvancedFiltersUpdate(newFilters) {
    // Advanced filters update - merge with existing period filters
    const mergedFilters = {
      ...publishersStore.filters,
      ...newFilters,
    }
    publishersStore.setFilters(mergedFilters)
    publishersStore.fetchAllData()
  }

  function onPositionChange(newPosition) {
    // Update position filter and reset other filters in the store
    publishersStore.setFilters({
      ...publishersStore.filters,
      search_position_query: newPosition,
      publisher: undefined,
      seniority: undefined,
      company: undefined,
      remote: undefined,
    })
    // Refresh available options for the new position (but don't refresh data yet)
    publishersStore.fetchAvailableOptions()
  }
</script>

<style scoped>
  .publishers-filter-bar {
    background: white;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .quick-filter-btn.active {
    background-color: #0056b3;
    border-color: #0056b3;
  }

  .clear-filters-btn {
    padding: 8px 16px;
    border: 1px solid #ced4da;
    border-radius: 4px;
    background: white;
    color: #495057;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.15s ease-in-out;
    align-self: flex-end;
    margin-left: auto; /* Push to the right */
  }

  .clear-filters-btn:hover {
    background-color: #f1f3f5;
  }

  .clear-filters-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
</style>
