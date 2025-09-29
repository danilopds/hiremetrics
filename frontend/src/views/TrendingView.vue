<template>
  <BasePageLayout
    title="Tendências e Variações"
    subtitle="Explore as últimas tendências e variações do mercado de trabalho"
    icon="📈"
    page-id="trending"
    :loading="loading"
    :error="error"
    :filters="filters"

    @period-change="onPeriodFilterChange"
  >
    <template #filter-bar>
      <!-- Trending Filter Bar -->
      <TrendingFilterBar
        :positions="availablePositions"
        :skills="skills"
        :seniority-levels="seniorityLevels"
        :initial-filters="filters"
        :loading="loading"
        @update:filters="onFiltersUpdate"
        @position-change="onPositionChange"
      />
    </template>

    <template #kpi-cards>
      <KpiCardRow>
        <!-- Most Demanded Skill -->
        <KpiCard
          title="Skill Mais Demandada"
          :value="kpiMostDemanded?.skill || '-'"
          :subtitle="kpiMostDemanded ? kpiMostDemanded.skill_count + ' vagas' : ''"
          icon="fas fa-star"
          color="blue"
        />

        <!-- Highest Growth Skill -->
        <KpiCard
          title="Maior Crescimento"
          :value="kpiHighestGrowth?.skill || '-'"
          :subtitle="kpiHighestGrowth ? formatGrowthPercent(kpiHighestGrowth) : ''"
          icon="fas fa-arrow-up"
          :color="kpiHighestGrowth?.isLeastDeclining ? 'yellow' : 'green'"
        >
          <template
            v-if="kpiHighestGrowth"
            #trend
          >
            <div class="flex flex-col space-y-1">
              <div class="flex items-center">
                <span
                  :class="
                    kpiHighestGrowth.isLeastDeclining
                      ? 'text-yellow-600 font-semibold'
                      : 'text-green-600 font-semibold'
                  "
                >
                  <i
                    :class="
                      kpiHighestGrowth.isLeastDeclining ? 'fas fa-arrow-down' : 'fas fa-arrow-up'
                    "
                  />
                  {{
                    kpiHighestGrowth.isLeastDeclining
                      ? 'Skill com menor declínio'
                      : 'Crescimento vs período anterior'
                  }}
                </span>
              </div>
              <div class="text-xs text-gray-400">
                {{ kpiHighestGrowth.current }} vs {{ kpiHighestGrowth.prev }} menções
              </div>
              <div
                v-if="kpiHighestGrowth.isLeastDeclining"
                class="text-xs text-yellow-600"
              >
                Nenhuma skill mostrando crescimento neste período
              </div>
            </div>
          </template>
        </KpiCard>

        <!-- Biggest Drop Skill -->
        <KpiCard
          title="Skill em Queda"
          :value="kpiBiggestDrop?.skill || 'Nenhuma queda'"
          :subtitle="kpiBiggestDrop ? formatDeclinePercent(kpiBiggestDrop) : 'Todas crescendo'"
          icon="fas fa-arrow-down"
          :color="kpiBiggestDrop ? 'red' : 'green'"
        >
          <template
            v-if="kpiBiggestDrop"
            #trend
          >
            <div class="flex flex-col space-y-1">
              <div class="flex items-center">
                <span class="text-red-600 font-semibold">
                  <i class="fas fa-arrow-down" />
                  Declínio vs período anterior
                </span>
              </div>
              <div class="text-xs text-gray-400">
                {{ kpiBiggestDrop.current }} vs {{ kpiBiggestDrop.prev }} menções
              </div>
            </div>
          </template>
          <template
            v-else
            #trend
          >
            <div class="flex items-center">
              <span class="text-green-600 font-semibold">
                <i class="fas fa-smile" />
                Todas as skills estão crescendo
              </span>
            </div>
          </template>
        </KpiCard>
      </KpiCardRow>
    </template>

    <!-- Top Skills -->
    <ChartCard
      title="Top Skills"
      description="Skills mais demandadas nas vagas publicadas"
      :loading="loading"
      :error="error"
      :has-data="trending.topSkills.length > 0"
      content-class="h-80"
    >
      <BaseBarChart :data="topSkillsChartData" />
    </ChartCard>

    <!-- Skills Trend Over Time -->
    <ChartCard
      title="Tendência de Skills ao Longo do Tempo"
      description="Crescimento cumulativo das menções de skills ao longo do tempo"
      :loading="loading"
      :error="error"
      :has-data="trending.skillsTrend.length > 0"
      content-class="h-80"
    >
      <BaseLineChart :data="skillsTrendChartData" />
    </ChartCard>

    <!-- Word Cloud -->
    <ChartCard
      title="Nuvem de Palavras de Skills"
      description="Representação visual da frequência de skills nas vagas publicadas"
      :loading="loading"
      :error="error"
      :has-data="trending.wordCloudSkills.length > 0"
      content-class="h-80"
    >
      <ImprovedWordCloud
        :key="'skills-cloud-' + wordCloudSkillsKey"
        :data="trending.wordCloudSkills"
        :loading="loading"
        :error="error"
      />
    </ChartCard>

    <!-- Radar Skills by Seniority -->
    <ChartCard
      title="Radar de Skills por Senioridade"
      description="Requisitos de skills em diferentes níveis de senioridade"
      :loading="loading"
      :error="error"
      :has-data="radarBubbleSkills.data.length > 0"
      content-class="h-80"
    >
      <BaseRadarSeniority
        :skills="radarBubbleSkills.skills"
        :seniority-levels="radarBubbleSkills.seniorityLevels"
        :data="radarBubbleSkills.data"
      />
    </ChartCard>

    <!-- Bubble Chart: Skills x Seniority -->
    <ChartCard
      title="Gráfico de Bolhas: Skills x Senioridade"
      description="Relação entre skills e níveis de senioridade com contagem de vagas"
      :loading="loading"
      :error="error"
      :has-data="radarBubbleSkills.data.length > 0"
      content-class="h-80"
    >
      <BaseBubbleSeniority
        :skills="radarBubbleSkills.skills"
        :seniority-levels="radarBubbleSkills.seniorityLevels"
        :data="radarBubbleSkills.data"
        height="120%"
      />
    </ChartCard>
  </BasePageLayout>
</template>

<script setup>
  import { computed, onMounted } from 'vue'
  import { useTrendingStore } from '@/stores/trending'
  import TrendingFilterBar from '@/components/filters/TrendingFilterBar.vue'
  import BaseBarChart from '@/components/charts/BaseBarChart.vue'
  import BaseLineChart from '@/components/charts/BaseLineChart.vue'
  import ImprovedWordCloud from '@/components/charts/ImprovedWordCloud.vue'
  import BaseRadarSeniority from '@/components/charts/BaseRadarSeniority.vue'
  import BaseBubbleSeniority from '@/components/charts/BaseBubbleSeniority.vue'
  import { format, parseISO } from 'date-fns'

  // Import new common components
  import BasePageLayout from '@/components/common/BasePageLayout.vue'
  import ChartCard from '@/components/common/ChartCard.vue'
  import KpiCard from '@/components/common/KpiCard.vue'
  import KpiCardRow from '@/components/common/KpiCardRow.vue'

  const trending = useTrendingStore()

  const loading = computed(() => trending.loading)
  const error = computed(() => trending.error)
  const skills = computed(() => trending.skills)
  const seniorityLevels = computed(() => trending.seniorityLevels)
  const availablePositions = computed(() => trending.availablePositions)
  const filters = computed(() => trending.filters)
  const kpiMostDemanded = computed(() => trending.kpiMostDemanded)
  const kpiHighestGrowth = computed(() => trending.kpiHighestGrowth)
  const kpiBiggestDrop = computed(() => trending.kpiBiggestDrop)

  // Helper functions for KPI formatting
  const formatGrowthPercent = (kpi) => {
    if (!kpi) {
      return ''
    }
    if (kpi.isLeastDeclining) {
      return `${kpi.change.toFixed(1)}%` // Show negative percentage for least declining
    }
    const sign = kpi.change > 0 ? '+' : ''
    return `${sign}${kpi.change.toFixed(1)}%`
  }

  const formatDeclinePercent = (kpi) => {
    if (!kpi) {
      return ''
    }
    return `${kpi.change.toFixed(1)}%` // Already negative, no need for extra sign
  }

  const topSkillsChartData = computed(() => {
    const filters = trending.filters
    const topSkills = trending.topSkills
    const skillsTrend = trending.skillsTrend
    const colorPalette = [
      '#2563eb',
      '#10b981',
      '#f59e42',
      '#ef4444',
      '#a855f7',
      '#fbbf24',
      '#14b8a6',
      '#6366f1',
    ]

    if (!filters.selectedSeniority) {
      // Backend now returns breakdown by seniority when no seniority filter is applied
      // Create stacked chart showing individual seniority levels
      const skillData = {}
      const seniorityLevels = [...new Set(topSkills.map((item) => item.seniority))].filter(Boolean)

      // Debug logging
      console.log('Top Skills Chart - Raw data:', topSkills.length, 'records')
      console.log('Top Skills Chart - Seniority levels found:', seniorityLevels)

      // Group data by skill and seniority
      topSkills.forEach((item) => {
        if (!skillData[item.skill]) {
          skillData[item.skill] = {}
        }
        skillData[item.skill][item.seniority] = item.skill_count
      })

      // Debug logging for skill data
      console.log('Top Skills Chart - Skills found:', Object.keys(skillData).length)
      Object.entries(skillData)
        .slice(0, 5)
        .forEach(([skill, seniorities]) => {
          const total = Object.values(seniorities).reduce((sum, count) => sum + count, 0)
          console.log(
            `Skill '${skill}':`,
            Object.keys(seniorities).length,
            'seniority levels, total:',
            total
          )
          Object.entries(seniorities).forEach(([seniority, count]) => {
            console.log(`  - ${seniority}: ${count}`)
          })
        })

      // Get top 10 skills by total count across all seniority levels
      const sortedSkills = Object.keys(skillData)
        .map((skill) => ({
          skill,
          total: Object.values(skillData[skill]).reduce((sum, count) => sum + count, 0),
        }))
        .sort((a, b) => b.total - a.total)
        .slice(0, 10)
        .map((item) => item.skill)

      return {
        tooltip: {
          show: true,
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          formatter: function (params) {
            if (!Array.isArray(params)) {
              params = [params]
            }
            const skillName = params[0].name
            let total = 0
            let result = `${skillName}<br/>`
            params.forEach((param) => {
              const value = param.value || 0
              total += value
              result += `${param.seriesName}: ${value}<br/>`
            })
            result += `<br/>Total: ${total}`
            return result
          },
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: '#ccc',
          borderWidth: 1,
          textStyle: { color: '#333' },
        },
        legend: { data: seniorityLevels, top: 0 },
        xAxis: {
          type: 'category',
          data: sortedSkills,
          axisLabel: { interval: 0, rotate: 45, show: true },
        },
        yAxis: { type: 'value' },
        series: seniorityLevels.map((seniority, idx) => ({
          name: seniority,
          type: 'bar',
          stack: 'total',
          data: sortedSkills.map((skill) => skillData[skill][seniority] || 0),
          itemStyle: { color: colorPalette[idx % colorPalette.length] },
          label: {
            show: idx === seniorityLevels.length - 1,
            position: 'top',
            formatter: function (params) {
              const total = sortedSkills.map((skill) =>
                seniorityLevels.reduce((sum, level) => sum + (skillData[skill][level] || 0), 0)
              )[params.dataIndex]
              return total
            },
            color: '#333',
            fontWeight: 'bold',
          },
        })),
      }
    } else {
      // With seniority filter applied, use skillsTrend data for consistency
      const filteredSkills = skillsTrend
        .filter((item) => item.seniority === filters.selectedSeniority)
        .reduce((acc, item) => {
          if (!acc[item.skill]) {
            acc[item.skill] = { skill: item.skill, skill_count: 0 }
          }
          acc[item.skill].skill_count += item.skill_count
          return acc
        }, {})

      const sortedSkills = Object.values(filteredSkills)
        .sort((a, b) => b.skill_count - a.skill_count)
        .slice(0, 10)

      return {
        tooltip: {
          show: true,
          trigger: 'axis',
          axisPointer: { type: 'shadow' },
          formatter: function (params) {
            if (!Array.isArray(params)) {
              params = [params]
            }
            const param = params[0]
            return `${param.name}<br/>${filters.selectedSeniority}: ${param.value}`
          },
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: '#ccc',
          borderWidth: 1,
          textStyle: { color: '#333' },
        },
        xAxis: {
          type: 'category',
          data: sortedSkills.map((skill) => skill.skill),
          axisLabel: { interval: 0, rotate: 45, show: true },
        },
        yAxis: { type: 'value' },
        series: [
          {
            name: filters.selectedSeniority,
            type: 'bar',
            data: sortedSkills.map((skill) => skill.skill_count),
            itemStyle: { color: '#10b981' },
            label: {
              show: true,
              position: 'top',
              formatter: '{c}',
              color: '#333',
              fontWeight: 'bold',
            },
          },
        ],
      }
    }
  })

  const filteredSkillsTrend = computed(() => {
    if (!trending.filters.selectedSeniority) {
      return trending.skillsTrend
    }
    return trending.skillsTrend.filter(
      (item) => item.seniority === trending.filters.selectedSeniority
    )
  })

  const skillsTrendChartData = computed(() => {
    const dates = [
      ...new Set(filteredSkillsTrend.value.map((item) => item.job_posted_at_date)),
    ].sort()

    // If user has selected specific skills, use those
    // Otherwise, determine the top 10 skills by cumulative count
    let uniqueSkills = []

    if (trending.filters.selectedSkills?.length > 0) {
      uniqueSkills = trending.filters.selectedSkills
    } else {
      // Calculate total skill counts across all dates to find top 10
      const skillCounts = {}
      filteredSkillsTrend.value.forEach((item) => {
        if (!skillCounts[item.skill]) {
          skillCounts[item.skill] = 0
        }
        skillCounts[item.skill] += item.skill_count
      })

      // Sort by count and get top 10 skills
      uniqueSkills = Object.entries(skillCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([skill]) => skill)
    }

    // Initialize the skill-date map
    const skillDateMap = {}
    uniqueSkills.forEach((skill) => {
      skillDateMap[skill] = {}
      dates.forEach((date) => {
        skillDateMap[skill][date] = 0
      })
    })

    // Aggregate the data by skill and date (sum across all seniority levels)
    filteredSkillsTrend.value.forEach((item) => {
      if (
        skillDateMap[item.skill] &&
        skillDateMap[item.skill][item.job_posted_at_date] !== undefined
      ) {
        // Add to the existing value instead of overwriting
        skillDateMap[item.skill][item.job_posted_at_date] += item.skill_count
      }
    })

    // Calculate cumulative data for each skill
    const series = uniqueSkills.map((skill) => {
      let cumulative = 0
      const data = dates.map((date) => {
        cumulative += skillDateMap[skill][date] || 0
        return cumulative
      })
      return {
        name: skill,
        type: 'line',
        data: data,
        smooth: true,
        showSymbol: true,
      }
    })

    // Create a mapping between formatted dates and original dates for tooltip
    const formattedDates = dates.map((date) => format(parseISO(date), 'MMM d'))
    const dateMap = {}
    dates.forEach((date, index) => {
      dateMap[formattedDates[index]] = date
    })

    return {
      xAxis: {
        type: 'category',
        data: formattedDates,
        axisLabel: { rotate: 45 },
      },
      yAxis: { type: 'value', name: 'Contagem Cumulativa' },
      tooltip: {
        trigger: 'axis',
        formatter: function (params) {
          if (!Array.isArray(params)) {
            params = [params]
          }
          let result = `${params[0].axisValue}<br/>`
          params.forEach((param) => {
            result += `${param.seriesName}: ${param.value}<br/>`
          })
          return result
        },
      },
      legend: { type: 'scroll', bottom: 0 },
      series: series,
    }
  })

  const wordCloudSkillsKey = computed(() => {
    if (!trending.wordCloudSkills || trending.wordCloudSkills.length === 0) {
      return 'empty'
    }

    // Create a more reliable key that changes only when the actual data changes
    const dataLength = trending.wordCloudSkills.length
    const sortedData = [...trending.wordCloudSkills]
      .sort((a, b) => (a.skill || '').localeCompare(b.skill || ''))
      .slice(0, 3)

    const key = `len-${dataLength}-${Date.now()}-${sortedData.map((item) => item.skill).join('|')}`
    return key
  })

  const radarBubbleSkills = computed(() => {
    // CONSISTENCY FIX: This now uses the same aggregation logic as the KPI calculation
    // to ensure the radar chart and KPI show consistent numbers when seniority filters are applied

    // First, aggregate time-series data by skill to get total counts
    const skillCounts = {}
    filteredSkillsTrend.value.forEach((item) => {
      if (!skillCounts[item.skill]) {
        skillCounts[item.skill] = 0
      }
      skillCounts[item.skill] += item.skill_count
    })

    // Get top 10 skills based on total aggregated counts
    const topSkills = Object.entries(skillCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([skill]) => skill)

    let seniorityLevels = [
      ...new Set(filteredSkillsTrend.value.map((item) => item.seniority)),
    ].filter(Boolean)

    // Sort seniority levels in desired order for Y axis
    const desiredOrder = [
      'junior',
      'pleno',
      'senior',
      'especialista',
      'lider',
      'gerente',
      'diretor',
    ]
    const synonymMap = {
      júnior: 'junior',
      sênior: 'senior',
      lead: 'lider',
      líder: 'lider',
      principal: 'especialista',
      manager: 'gerente',
      director: 'diretor',
    }
    const normalize = (s) =>
      (s || '')
        .toString()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()
    const rank = (s) => {
      const n = normalize(s)
      const mapped = synonymMap[n] || n
      const idx = desiredOrder.indexOf(mapped)
      return idx !== -1 ? idx : desiredOrder.length + 1
    }
    seniorityLevels = seniorityLevels
      .sort((a, b) => {
        const ra = rank(a)
        const rb = rank(b)
        if (ra !== rb) {
          return ra - rb
        }
        return (a || '').localeCompare(b || '', 'pt-BR', { sensitivity: 'base' })
      })
      .reverse()

    // Create aggregated data by skill and seniority combination
    // This aggregation ensures totals match KPI calculations
    const aggregatedData = {}
    filteredSkillsTrend.value.forEach((item) => {
      if (topSkills.includes(item.skill)) {
        const key = `${item.skill}_${item.seniority}`
        if (!aggregatedData[key]) {
          aggregatedData[key] = {
            skill: item.skill,
            seniority: item.seniority,
            skill_count: 0,
          }
        }
        aggregatedData[key].skill_count += item.skill_count
      }
    })

    // Convert aggregated data back to array format
    const data = Object.values(aggregatedData)

    return { skills: topSkills, seniorityLevels, data }
  })

  function onPeriodFilterChange(periodFilters) {
    trending.setFilters({ ...trending.filters, ...periodFilters })
    const token = localStorage.getItem('token')
    if (token) {
      trending.refreshAll(token)
    }
  }

  function onFiltersUpdate(newFilters) {
    trending.setFilters({ ...trending.filters, ...newFilters })
    const token = localStorage.getItem('token')
    if (token) {
      trending.refreshAll(token)
    }
  }

  function onPositionChange(newPosition) {
    // Update position filter
    trending.setFilters({ ...trending.filters, search_position_query: newPosition })

    // Refresh available skills and seniority levels for the new position
    const token = localStorage.getItem('token')
    if (token) {
      trending.fetchAvailableSkills(token)
      trending.fetchAvailableSeniorityLevels(token)
    }
  }

  onMounted(async () => {
    const token = localStorage.getItem('token')
    if (token) {
      await trending.refreshAll(token)
    }
  })
</script>
