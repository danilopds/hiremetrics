<template>
  <div class="base-heatmap">
    <div
      v-if="loading"
      class="loading-state"
    >
      <div class="spinner" />
      <p>Carregando dados...</p>
    </div>

    <div
      v-else-if="error"
      class="error-state"
    >
      <p>{{ error }}</p>
    </div>

    <div
      v-else-if="
        !data || !data.length || !xAxisData || !xAxisData.length || !yAxisData || !yAxisData.length
      "
      class="empty-state"
    >
      <p>Nenhum dado disponível</p>
    </div>

    <div
      v-else
      ref="chartContainer"
      :style="{ height: chartHeight, width: '100%' }"
    />
  </div>
</template>

<script>
  import * as echarts from 'echarts'

  export default {
    name: 'BaseHeatmap',
    props: {
      data: {
        type: Array,
        default: () => [],
      },
      xAxisData: {
        type: Array,
        default: () => [],
      },
      yAxisData: {
        type: Array,
        default: () => [],
      },
      title: {
        type: String,
        default: '',
      },
      loading: {
        type: Boolean,
        default: false,
      },
      error: {
        type: String,
        default: null,
      },
      height: {
        type: String,
        default: '400px',
      },
      colorRange: {
        type: Array,
        default: () => [
          '#313695',
          '#4575b4',
          '#74add1',
          '#abd9e9',
          '#e0f3f8',
          '#ffffcc',
          '#fee090',
          '#fdae61',
          '#f46d43',
          '#d73027',
          '#a50026',
        ],
      },
    },

    data() {
      return {
        chart: null,
      }
    },

    computed: {
      chartHeight() {
        return this.height
      },

      chartOption() {
        if (!this.data.length || !this.xAxisData.length || !this.yAxisData.length) {
          return {}
        }

        // Find min/max values for color scale
        const values = this.data.map((item) => item[2])
        const minValue = Math.min(...values)
        const maxValue = Math.max(...values)

        return {
          title: {
            text: this.title,
            left: 'center',
            top: 10,
          },
          tooltip: {
            position: 'top',
            formatter: (params) => {
              const xLabel = this.xAxisData[params.data[0]]
              const yLabel = this.yAxisData[params.data[1]]
              const value = params.data[2]
              return `${yLabel}<br/>${xLabel}: <strong>${value}</strong> vagas`
            },
          },
          grid: {
            left: '15%',
            right: '10%',
            top: 60,
            bottom: '20%',
            containLabel: true,
          },
          xAxis: {
            type: 'category',
            data: this.xAxisData,
            splitArea: {
              show: true,
            },
            axisLabel: {
              rotate: 45,
              fontSize: 10,
              interval: 0,
              margin: 16,
              formatter: function (value) {
                return value.length > 12 ? `${value.substring(0, 10)}...` : value
              },
            },
          },
          yAxis: {
            type: 'category',
            data: this.yAxisData,
            splitArea: {
              show: true,
            },
            axisLabel: {
              fontSize: 10,
              formatter: function (value) {
                return value.length > 20 ? `${value.substring(0, 18)}...` : value
              },
            },
          },
          visualMap: {
            min: minValue,
            max: maxValue,
            calculable: true,
            orient: 'horizontal',
            left: 'center',
            bottom: '5%',
            inRange: {
              color: this.colorRange,
            },
            text: ['Alto', 'Baixo'],
            textStyle: {
              fontSize: 12,
            },
          },
          series: [
            {
              name: 'Heatmap',
              type: 'heatmap',
              data: this.data,
              label: {
                show: false,
              },
              emphasis: {
                itemStyle: {
                  shadowBlur: 10,
                  shadowColor: 'rgba(0, 0, 0, 0.5)',
                },
              },
            },
          ],
        }
      },
    },

    watch: {
      data: {
        handler() {
          this.$nextTick(() => {
            this.ensureChartAndUpdate()
          })
        },
        deep: true,
      },
      xAxisData: {
        handler() {
          this.$nextTick(() => {
            this.ensureChartAndUpdate()
          })
        },
      },
      yAxisData: {
        handler() {
          this.$nextTick(() => {
            this.ensureChartAndUpdate()
          })
        },
      },
    },

    mounted() {
      this.initChart()
    },

    beforeUnmount() {
      if (this.chart) {
        this.chart.dispose()
      }
    },

    methods: {
      initChart() {
        if (this.$refs.chartContainer) {
          try {
            this.chart = echarts.init(this.$refs.chartContainer)
            this.updateChart()

            // Handle window resize
            window.addEventListener('resize', this.handleResize)
          } catch (error) {
            console.error('Error initializing chart:', error)
          }
        }
      },

      updateChart() {
        if (this.chart && this.chartOption && Object.keys(this.chartOption).length > 0) {
          try {
            this.chart.setOption(this.chartOption, true)
          } catch (error) {
            console.error('Error updating heatmap chart:', error)
          }
        }
      },

      ensureChartAndUpdate() {
        // If we don't have a chart but we have data and a container, initialize it
        if (!this.chart && this.$refs.chartContainer && this.hasData()) {
          this.initChart()
        } else if (this.chart) {
          // Chart exists, just update it
          this.updateChart()
        }
      },

      hasData() {
        return (
          this.data &&
          this.data.length > 0 &&
          this.xAxisData &&
          this.xAxisData.length > 0 &&
          this.yAxisData &&
          this.yAxisData.length > 0
        )
      },

      handleResize() {
        if (this.chart) {
          this.chart.resize()
        }
      },
    },
  }
</script>

<style scoped>
  .base-heatmap {
    width: 100%;
    position: relative;
  }

  .loading-state,
  .error-state,
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: #666;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #007bff;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 10px;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .error-state {
    color: #dc3545;
  }

  .empty-state {
    color: #6c757d;
  }
</style>
