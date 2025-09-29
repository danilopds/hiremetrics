<template>
  <BasePageLayout
    title="Empresas Ranking"
    subtitle="Explore insights sobre as empresas que mais publicam vagas e suas características"
    icon="🏢"
    page-id="companies"
    :loading="loading"
    :error="error"
    default-period="last30days"
    :filters="filters"
    @period-change="onPeriodFilterChange"
  >
    <template #filter-bar>
      <!-- Filter Bar -->
      <CompaniesFilterBar
        :positions="companies.availablePositions"
        :companies="companies.availableCompanies"
        :seniority-levels="companies.availableSeniorityLevels"
        :initial-filters="companies.filters"
        :loading="loading"
        @update:filters="onFiltersUpdate"
        @position-change="onPositionChange"
      />
    </template>

    <template #kpi-cards>
      <KpiCardRow>
        <!-- Total Job Postings -->
        <KpiCard
          title="Total de Vagas Publicadas"
          :value="companies.kpis?.total_jobs?.toLocaleString() || '-'"
          :subtitle="
            companies.filters.employer_name && companies.filters.employer_name !== 'all'
              ? `de ${companies.filters.employer_name}`
              : 'todas as empresas'
          "
          icon="fas fa-briefcase"
          color="blue"
        />

        <!-- Remote Jobs Percentage -->
        <KpiCard
          title="% de Vagas Remotas"
          :value="`${companies.kpis?.remote_percentage || 0}%`"
          :subtitle="
            companies.filters.employer_name && companies.filters.employer_name !== 'all'
              ? `em ${companies.filters.employer_name}`
              : 'no mercado'
          "
          icon="fas fa-home"
          color="green"
        />

        <!-- Average Skills per Job -->
        <KpiCard
          title="Média de Skills por Vaga"
          :value="companies.kpis?.avg_skills_per_job || 0"
          subtitle="skills demandadas"
          icon="fas fa-code"
          color="purple"
        />

        <!-- Distinct Companies Count -->
        <KpiCard
          title="Empresas Ativas"
          :value="companies.kpis?.distinct_companies?.toLocaleString() || '-'"
          :subtitle="
            companies.filters.employer_name && companies.filters.employer_name !== 'all'
              ? `filtrada: ${companies.filters.employer_name}`
              : 'publicando vagas'
          "
          icon="fas fa-building"
          color="orange"
        />
      </KpiCardRow>
    </template>

    <!-- Top Companies -->
    <ChartCard
      title="Top 10 Empresas com Mais Vagas Publicadas"
      description="Ranking das empresas com maior número de vagas disponíveis"
      :loading="loading"
      :error="error"
      :has-data="companies.topCompanies.length > 0"
      content-class="h-80"
    >
      <BaseBarChart :data="topCompaniesChartData" />
    </ChartCard>

    <!-- Employment Type Distribution -->
    <ChartCard
      title="Vagas por Tipo de Contratação"
      description="Distribuição das vagas por modalidade de contrato"
      :loading="loading"
      :error="error"
      :has-data="companies.employmentTypeDistribution.length > 0"
      content-class="h-80"
    >
      <BasePieChart
        :data="companies.employmentTypeDistribution"
        title=""
      />
    </ChartCard>

    <!-- Seniority Distribution by Company -->
    <ChartCard
      title="Distribuição de Senioridade por Empresa"
      description="Níveis de senioridade requisitados por cada empresa"
      :loading="loading"
      :error="error"
      :has-data="companies.seniorityDistribution.length > 0"
      content-class="h-80"
    >
      <BaseBarChart :data="seniorityDistributionChartData" />
    </ChartCard>

    <!-- Remote Percentage by Company -->
    <ChartCard
      title="% de Vagas Remotas por Empresa"
      description="Percentual de trabalho remoto oferecido por cada empresa"
      :loading="loading"
      :error="error"
      :has-data="companies.remotePercentage.length > 0"
      content-class="h-80"
    >
      <BaseBarChart :data="remotePercentageChartData" />
    </ChartCard>

    <!-- Jobs Timeline -->
    <ChartCard
      title="Vagas Publicadas ao Longo do Tempo por Empresa"
      description="Evolução cumulativa das publicações de vagas por empresa"
      :loading="loading"
      :error="error"
      :has-data="companies.jobsTimeline.length > 0"
      content-class="h-80"
    >
      <BaseLineChart :data="jobsTimelineChartData" />
    </ChartCard>

    <!-- Top Skills by Company -->
    <ChartCard
      title="Top Skills Demandadas por Empresa"
      description="Habilidades mais requisitadas nas vagas publicadas"
      :loading="loading"
      :error="error"
      :has-data="companies.topSkills.length > 0"
      content-class="h-80"
    >
      <ImprovedWordCloud
        :key="'skills-cloud-' + topSkillsKey"
        :data="topSkillsWordCloudData"
        :loading="loading"
        :error="error"
      />
    </ChartCard>
  </BasePageLayout>
</template>

<script setup>
  import { computed, onMounted } from 'vue'
  import { useCompaniesStore } from '@/stores/companies'
  import CompaniesFilterBar from '@/components/filters/CompaniesFilterBar.vue'
  import BaseBarChart from '@/components/charts/BaseBarChart.vue'
  import BaseLineChart from '@/components/charts/BaseLineChart.vue'
  import BasePieChart from '@/components/charts/BasePieChart.vue'
  import ImprovedWordCloud from '@/components/charts/ImprovedWordCloud.vue'
  import { format, parseISO } from 'date-fns'

  // Import common components
  import BasePageLayout from '@/components/common/BasePageLayout.vue'
  import ChartCard from '@/components/common/ChartCard.vue'
  import KpiCard from '@/components/common/KpiCard.vue'
  import KpiCardRow from '@/components/common/KpiCardRow.vue'

  const companies = useCompaniesStore()

  const loading = computed(() => companies.loading)
  const error = computed(() => companies.error)
  const filters = computed(() => companies.filters)

  const topCompaniesChartData = computed(() => {
    const data = companies.topCompanies.slice(0, 10) // Top 10 for better visualization

    // Sort data by job count in descending order (highest to lowest)
    const sortedData = [...data].sort((a, b) => b.job_count - a.job_count)

    // Get top 3 job counts for coloring (highest values)
    const top3JobCounts = sortedData.slice(0, 3).map((item) => item.job_count)

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
        left: '1%', // Responsive space for company names (scales with screen)
        right: '10%', // Responsive space for value labels
        top: '15px', // Minimal top margin for tight spacing
        bottom: '10%', // Responsive bottom space for axis label
        containLabel: true, // Ensures labels stay within chart boundaries
      },
      xAxis: {
        type: 'value',
        name: 'Número de Vagas',
      },
      yAxis: {
        type: 'category',
        data: sortedData.map((item) => item.employer_name),
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
          name: 'Vagas Publicadas',
          type: 'bar',
          data: sortedData.map((item) => ({
            value: item.job_count,
            itemStyle: { color: getBarColor(item.job_count) },
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

  const seniorityDistributionChartData = computed(() => {
    const distribution = companies.seniorityDistribution
    const companies_names = [...new Set(distribution.map((item) => item.employer_name))]
    const seniorityLevels = [...new Set(distribution.map((item) => item.seniority))].filter(Boolean)

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

    const series = seniorityLevels.map((seniority, idx) => ({
      name: seniority,
      type: 'bar',
      stack: 'total',
      data: companies_names.map((company) => {
        const item = distribution.find(
          (d) => d.employer_name === company && d.seniority === seniority
        )
        return item ? item.job_count : 0
      }),
      itemStyle: { color: colorPalette[idx % colorPalette.length] },
    }))

    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
      },
      legend: {
        data: seniorityLevels,
        top: 0,
      },
      xAxis: {
        type: 'category',
        data: companies_names.slice(0, 10), // Top 10 companies
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

  const remotePercentageChartData = computed(() => {
    const data = companies.remotePercentage.slice(0, 15)

    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        formatter: function (params) {
          const param = params[0]
          return `${param.name}<br/>Vagas Remotas: ${param.value}%<br/>Total de Vagas: ${data[param.dataIndex]?.total_jobs || 0}`
        },
      },
      grid: {
        left: '1%', // Responsive space for company names (scales with screen)
        right: '10%', // Responsive space for value labels
        top: '15px', // Minimal top margin for tight spacing
        bottom: '10%', // Responsive bottom space for axis label
        containLabel: true, // Ensures labels stay within chart boundaries
      },
      xAxis: {
        type: 'value',
        name: 'Percentual de Vagas Remotas (%)',
        max: 100,
      },
      yAxis: {
        type: 'category',
        data: data.map((item) => item.employer_name),
        axisLabel: {
          interval: 0,
          overflow: 'truncate',
          fontSize: 11,
          margin: 8,
        },
      },
      series: [
        {
          name: '% Vagas Remotas',
          type: 'bar',
          data: data.map((item) => item.remote_percentage),
          itemStyle: { color: '#10b981' },
          label: {
            show: true,
            position: 'right',
            formatter: '{c}%',
          },
        },
      ],
    }
  })

  const jobsTimelineChartData = computed(() => {
    const timeline = companies.jobsTimeline
    const dates = [...new Set(timeline.map((item) => item.job_posted_at_date))].sort()
    const companies_names = [...new Set(timeline.map((item) => item.employer_name))]

    const series = companies_names.map((company) => {
      let cumulative = 0
      const data = dates.map((date) => {
        const item = timeline.find(
          (t) => t.job_posted_at_date === date && t.employer_name === company
        )
        if (item) {
          cumulative += item.job_count
        }
        return cumulative
      })

      return {
        name: company,
        type: 'line',
        data: data,
        smooth: true,
        showSymbol: true,
      }
    })

    // Format dates in the 'MMM d' format
    const formattedDates = dates.map((date) => format(parseISO(date), 'MMM d'))

    return {
      tooltip: {
        trigger: 'axis',
      },
      legend: {
        data: companies_names,
        type: 'scroll',
        bottom: 0,
      },
      xAxis: {
        type: 'category',
        data: formattedDates,
        axisLabel: { rotate: 45 },
      },
      yAxis: {
        type: 'value',
        name: 'Número de Vagas',
      },
      series: series,
    }
  })

  const topSkillsWordCloudData = computed(() => {
    // Transform data from the new API format (name/value) to the format expected by BaseWordCloud (skill/skill_count)
    if (!companies.topSkills || !Array.isArray(companies.topSkills)) {
      return []
    }

    // First transform the data to a consistent format
    const formattedData = companies.topSkills.map((item) => {
      const result = {
        skill: item.name || item.skill || '',
        skill_count: item.value || item.skill_count || 0,
      }
      return result
    })

    // Check for duplicates
    const skillCounts = {}
    formattedData.forEach((item) => {
      if (item.skill) {
        if (!skillCounts[item.skill]) {
          skillCounts[item.skill] = 0
        }
        skillCounts[item.skill]++
      }
    })

    // const duplicates = Object.entries(skillCounts)
    //   .filter(([_, count]) => count > 1)
    //   .map(([skill, count]) => ({ skill, count }))

    // Then deduplicate by skill name
    const uniqueSkillsMap = new Map()
    formattedData.forEach((item) => {
      if (
        item.skill &&
        (!uniqueSkillsMap.has(item.skill) ||
          uniqueSkillsMap.get(item.skill).skill_count < item.skill_count)
      ) {
        uniqueSkillsMap.set(item.skill, item)
      }
    })

    // Return array of unique skills
    const result = Array.from(uniqueSkillsMap.values())
    return result
  })

  const topSkillsKey = computed(() => {
    if (!topSkillsWordCloudData.value || topSkillsWordCloudData.value.length === 0) {
      return 'empty'
    }

    // Create a more reliable key that changes only when the actual data changes
    const sortedData = [...topSkillsWordCloudData.value].sort((a, b) =>
      a.skill.localeCompare(b.skill)
    )

    // Use data length and a hash of the first few items
    const dataLength = topSkillsWordCloudData.value.length
    const key = `len-${dataLength}-${Date.now()}-${sortedData
      .slice(0, 3)
      .map((item) => `${item.skill}`)
      .join('|')}`
    return key
  })

  const onPeriodFilterChange = (periodFilters) => {
    companies.setFilters(periodFilters)
    companies.refreshAll()
  }

  const onFiltersUpdate = (filters) => {
    companies.setFilters(filters)
    companies.refreshAll()
  }

  const onPositionChange = (newPosition) => {
    // Update position filter and reset other filters in the store
    companies.setFilters({
      ...companies.filters,
      search_position_query: newPosition,
      employer_name: undefined,
      job_is_remote: undefined,
      seniority: undefined,
    })
    // Refresh available companies and seniority levels for the new position
    companies.fetchAvailableCompanies()
    companies.fetchAvailableSeniorityLevels()
  }

  onMounted(async () => {
    await companies.initializeFilters()
    await companies.refreshAll()
  })
</script>
