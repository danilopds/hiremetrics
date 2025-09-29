<template>
  <div class="min-h-screen bg-gray-100">
    <DashboardNav />

    <!-- Alert Banner -->
    <AlertBanner
      v-if="showAlertBanner"
      :message="bannerMessage"
      :type="bannerType"
      :dismissible="false"
      :persist-dismissal="false"
      storage-key="dashboard-alert-banner"
    />

    <div class="py-6 mt-14">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Page Header -->
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">
            {{ icon }} {{ title }}
          </h1>
          <p class="text-lg text-gray-600">
            {{ subtitle }}
          </p>
        </div>
      </div>
      <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
        <!-- Period Filter - Only show if enabled -->
        <PeriodFilter
          v-if="showPeriodFilter"
          :key="`${pageId}-period-filter`"
          :loading="loading"
          :default-period="defaultPeriod"
          :filters="filters"
          @period-change="onPeriodFilterChange"
        />

        <!-- Advanced Filter Bar -->
        <slot name="filter-bar" />

        <!-- Loading State -->
        <div
          v-if="loading"
          class="py-4"
        >
          <div class="bg-white shadow rounded-lg p-6">
            <p class="text-center text-gray-500">
              Loading {{ pageId }} data...
            </p>
          </div>
        </div>

        <!-- Error State -->
        <div
          v-else-if="error"
          class="py-4"
        >
          <div class="bg-red-50 shadow rounded-lg p-6">
            <p class="text-center text-red-500">
              {{ error }}
            </p>
          </div>
        </div>

        <!-- Content -->
        <template v-else>
          <!-- KPI Cards -->
          <slot name="kpi-cards" />

          <!-- Charts and Other Content -->
          <slot />
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { defineProps, defineEmits } from 'vue'
  import DashboardNav from '@/components/DashboardNav.vue'
  import PeriodFilter from '@/components/filters/PeriodFilter.vue'
  import AlertBanner from '@/components/common/AlertBanner.vue'

  defineProps({
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      default: '',
    },
    icon: {
      type: String,
      default: '📊',
    },
    pageId: {
      type: String,
      required: true,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    error: {
      type: [String, null],
      default: null,
    },
    showPeriodFilter: {
      type: Boolean,
      default: true,
    },
    defaultPeriod: {
      type: String,
      default: 'last30days',
    },
    filters: {
      type: Object,
      default: () => ({}),
    },
    bannerMessage: {
      type: String,
      default:
        '🎉 Bem-vindo ao HireMetrics! Explore as vagas e descubra insights do mercado de tecnologia.',
    },
    bannerType: {
      type: String,
      default: 'info',
      validator: (value) => ['info', 'success', 'warning', 'error'].includes(value),
    },
    showAlertBanner: {
      type: Boolean,
      default: true,
    },
  })

  const emit = defineEmits(['period-change'])

  const onPeriodFilterChange = (periodFilters) => {
    emit('period-change', periodFilters)
  }
</script>
