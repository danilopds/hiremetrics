<template>
  <div class="h-full relative">
    <!-- Loading overlay -->
    <div
      v-if="loading"
      class="flex items-center justify-center h-full bg-white bg-opacity-80 absolute inset-0 z-10"
    >
      <p class="text-gray-500">
        Loading map data...
      </p>
    </div>

    <!-- Error overlay -->
    <div
      v-if="error"
      class="flex items-center justify-center h-full bg-white bg-opacity-80 absolute inset-0 z-10"
    >
      <p class="text-red-500">
        {{ error }}
      </p>
    </div>

    <!-- Map container (always present) -->
    <div
      id="map-container"
      ref="mapContainer"
      class="maplibre-map absolute inset-0"
    />
  </div>
</template>

<script setup>
  import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
  import maplibregl from 'maplibre-gl'
  import 'maplibre-gl/dist/maplibre-gl.css'
  import { fetchJobLocationsGeo } from '@/api/dashboard'

  const props = defineProps({
    filters: {
      type: Object,
      default: () => ({}),
    },
  })

  const mapContainer = ref(null)
  let mapInstance = null
  const loading = ref(true)
  const error = ref(null)
  const locationData = ref([])

  // Function to initialize the map
  function initializeMap() {
    try {
      // Use getElementById as a fallback if ref is not available
      const container = document.getElementById('map-container')

      if (!container) {
        error.value = 'Map container not found'
        return false
      }

      // Check if map instance already exists
      if (mapInstance) {
        mapInstance.remove()
      }

      // Create new map instance
      mapInstance = new maplibregl.Map({
        container,
        style: 'https://demotiles.maplibre.org/style.json',
        center: [-55, -15], // Center on Brazil
        zoom: 3,
        attributionControl: true,
      })

      // Add map event handlers
      mapInstance.on('load', () => {
        mapInstance.resize()
        return true
      })

      mapInstance.on('error', (e) => {
        error.value = `Map error: ${e.error.message}`
        return false
      })

      return true
    } catch (e) {
      error.value = `Failed to initialize map: ${e.message}`
      loading.value = false
      return false
    }
  }

  // Function to fetch location data from API
  async function fetchLocationData() {
    loading.value = true
    error.value = null
    try {
      const {
        job_is_remote,
        dateFrom: job_posted_at_date_from,
        dateTo: job_posted_at_date_to,
        job_city,
        job_state,
        search_position_query,
      } = props.filters || {}

      const data = await fetchJobLocationsGeo({
        job_posted_at_date_from,
        job_posted_at_date_to,
        job_is_remote,
        job_city,
        job_state,
        search_position_query,
      })

      // Store the data
      locationData.value = data

      // Make sure map is initialized before adding markers
      if (!mapInstance) {
        const initialized = initializeMap()
        if (!initialized) {
          error.value = 'Failed to initialize map'
          loading.value = false
          return
        }

        // Give the map time to initialize before adding markers
        setTimeout(() => {
          if (mapInstance && data.length > 0) {
            addMarkersToMap(data)
          }
        }, 500)
      } else {
        // Map already initialized, add markers directly
        if (data.length > 0) {
          await addMarkersToMap(data)
        }
      }

      loading.value = false
    } catch (e) {
      console.error('MapLibreMap - Error loading data:', e)
      error.value = `Failed to load map data: ${e.message}`
      loading.value = false
    }
  }

  // Add markers to the map based on geocoded data
  async function addMarkersToMap(locations) {
    if (!mapInstance) {
      error.value = 'Map instance not available for adding markers'
      return
    }

    // Clear existing markers if any
    const existingMarkers = document.querySelectorAll('.maplibregl-marker')
    existingMarkers.forEach((marker) => marker.remove())

    // Create geocoder
    const geocoder = new SimpleGeocoder()
    const bounds = new maplibregl.LngLatBounds()
    let markersAdded = 0

    // Filter valid locations
    const validLocations = locations.filter((location) => location.job_city && location.job_state)

    if (validLocations.length === 0) {
      return
    }

    // Process all locations in sequence to avoid race conditions
    for (const location of validLocations) {
      try {
        const coords = await geocoder.geocode(`${location.job_city}, ${location.job_state}`)
        if (!coords) {
          continue
        }

        // Create popup content
        const popup = new maplibregl.Popup({ offset: 25 }).setHTML(`
          <div class="p-2">
            <strong>${location.job_city}, ${location.job_state}</strong><br>
            Job count: ${location.job_count}
          </div>
        `)

        // Create and add a marker
        const el = document.createElement('div')
        el.className = 'map-marker'
        el.style.width = '10px'
        el.style.height = '10px'
        el.style.borderRadius = '50%'
        el.style.backgroundColor = '#3b82f6'
        el.style.border = '2px solid #fff'
        el.style.boxShadow = '0 0 2px rgba(0,0,0,0.3)'

        // Make marker size proportional to job count (within limits)
        const markerSize = Math.min(20, Math.max(10, 10 + Math.log(location.job_count)))
        el.style.width = `${markerSize}px`
        el.style.height = `${markerSize}px`

        new maplibregl.Marker(el)
          .setLngLat([coords.longitude, coords.latitude])
          .setPopup(popup)
          .addTo(mapInstance)

        // Extend bounds to include this point
        bounds.extend([coords.longitude, coords.latitude])
        markersAdded++
      } catch (error) {
        // Silently continue on error
      }
    }

    // After all markers are added, fit the map to bounds
    if (markersAdded > 0) {
      mapInstance.fitBounds(bounds, { padding: 50, maxZoom: 9 })
    }
  }

  // Simple geocoder service using precomputed coordinates for Brazilian cities
  class SimpleGeocoder {
    constructor() {
      // Create a map of city-state pairs to coordinates
      this.cityStateMap = {
        // São Paulo state
        'São Paulo-SP': { latitude: -23.5505, longitude: -46.6333 },
        'Barueri-SP': { latitude: -23.5057, longitude: -46.8764 },
        'Campinas-SP': { latitude: -22.9071, longitude: -47.0633 },
        'São José dos Campos-SP': { latitude: -23.1791, longitude: -45.8872 },
        'Sumaré-SP': { latitude: -22.8204, longitude: -47.2728 },

        // Rio de Janeiro state
        'Rio de Janeiro-RJ': { latitude: -22.9068, longitude: -43.1729 },

        // Distrito Federal
        'Brasília-DF': { latitude: -15.7801, longitude: -47.9292 },

        // Bahia state
        'Salvador-BA': { latitude: -12.9714, longitude: -38.5014 },

        // Ceará state
        'Fortaleza-CE': { latitude: -3.7319, longitude: -38.5267 },
        'Croatá-CE': { latitude: -4.4085, longitude: -40.9022 },

        // Minas Gerais state
        'Belo Horizonte-MG': { latitude: -19.9167, longitude: -43.9345 },
        'Timóteo-MG': { latitude: -19.5811, longitude: -42.6471 },
        'Sete Lagoas-MG': { latitude: -19.4569, longitude: -44.2413 },
        'Itabira-MG': { latitude: -19.6186, longitude: -43.2269 },
        'Pouso Alegre-MG': { latitude: -22.2266, longitude: -45.9389 },
        'Lagoa Santa-MG': { latitude: -19.6333, longitude: -43.8833 },

        // Amazonas state
        'Manaus-AM': { latitude: -3.119, longitude: -60.0217 },

        // Paraná state
        'Curitiba-PR': { latitude: -25.4296, longitude: -49.2719 },

        // Pernambuco state
        'Recife-PE': { latitude: -8.0476, longitude: -34.877 },

        // Rio Grande do Sul state
        'Porto Alegre-RS': { latitude: -30.0368, longitude: -51.209 },
        'Passo Fundo-RS': { latitude: -28.2576, longitude: -52.4091 },

        // Pará state
        'Belém-PA': { latitude: -1.4558, longitude: -48.4902 },

        // Goiás state
        'Goiânia-GO': { latitude: -16.6799, longitude: -49.255 },

        // Santa Catarina state
        'Florianópolis-SC': { latitude: -27.5973, longitude: -48.5496 },
        'Joinville-SC': { latitude: -26.3032, longitude: -48.8461 },

        // Espírito Santo state
        'Vitória-ES': { latitude: -20.2976, longitude: -40.2958 },

        // Mato Grosso do Sul state
        'Campo Grande-MS': { latitude: -20.4697, longitude: -54.6201 },

        // Mato Grosso state
        'Cuiabá-MT': { latitude: -15.6014, longitude: -56.0979 },

        // Paraíba state
        'João Pessoa-PB': { latitude: -7.1195, longitude: -34.845 },

        // Maranhão state
        'Imperatriz-MA': { latitude: -5.5268, longitude: -47.4722 },

        // Tocantins state
        'Taguatinga-TO': { latitude: -12.4026, longitude: -46.4371 },
      }

      // Create a map of state abbreviations to coordinates for fallback
      this.stateMap = {
        SP: { latitude: -23.5505, longitude: -46.6333 }, // São Paulo state centered at São Paulo city
        RJ: { latitude: -22.9068, longitude: -43.1729 }, // Rio de Janeiro state centered at Rio city
        MG: { latitude: -19.9167, longitude: -43.9345 }, // Minas Gerais centered at Belo Horizonte
        ES: { latitude: -20.2976, longitude: -40.2958 }, // Espírito Santo centered at Vitória
        RS: { latitude: -30.0368, longitude: -51.209 }, // Rio Grande do Sul centered at Porto Alegre
        SC: { latitude: -27.5973, longitude: -48.5496 }, // Santa Catarina centered at Florianópolis
        PR: { latitude: -25.4296, longitude: -49.2719 }, // Paraná centered at Curitiba
        MS: { latitude: -20.4697, longitude: -54.6201 }, // Mato Grosso do Sul centered at Campo Grande
        MT: { latitude: -15.6014, longitude: -56.0979 }, // Mato Grosso centered at Cuiabá
        GO: { latitude: -16.6799, longitude: -49.255 }, // Goiás centered at Goiânia
        DF: { latitude: -15.7801, longitude: -47.9292 }, // Distrito Federal centered at Brasília
        BA: { latitude: -12.9714, longitude: -38.5014 }, // Bahia centered at Salvador
        SE: { latitude: -10.9472, longitude: -37.0731 }, // Sergipe centered at Aracaju
        AL: { latitude: -9.6498, longitude: -35.7089 }, // Alagoas centered at Maceió
        PE: { latitude: -8.0476, longitude: -34.877 }, // Pernambuco centered at Recife
        PB: { latitude: -7.1195, longitude: -34.845 }, // Paraíba centered at João Pessoa
        RN: { latitude: -5.7945, longitude: -35.212 }, // Rio Grande do Norte centered at Natal
        CE: { latitude: -3.7319, longitude: -38.5267 }, // Ceará centered at Fortaleza
        PI: { latitude: -5.092, longitude: -42.8038 }, // Piauí centered at Teresina
        MA: { latitude: -2.5307, longitude: -44.3068 }, // Maranhão centered at São Luís
        TO: { latitude: -10.1753, longitude: -48.3323 }, // Tocantins centered at Palmas
        PA: { latitude: -1.4558, longitude: -48.4902 }, // Pará centered at Belém
        AP: { latitude: 0.0356, longitude: -51.0705 }, // Amapá centered at Macapá
        RR: { latitude: 2.8196, longitude: -60.6714 }, // Roraima centered at Boa Vista
        AM: { latitude: -3.119, longitude: -60.0217 }, // Amazonas centered at Manaus
        AC: { latitude: -9.9754, longitude: -67.8249 }, // Acre centered at Rio Branco
        RO: { latitude: -8.7639, longitude: -63.9004 }, // Rondônia centered at Porto Velho
      }
    }

    async geocode(address) {
      try {
        // Parse city and state from the address
        const parts = address.split(',').map((part) => part.trim())
        const city = parts[0]
        const state = parts[1]

        // Map of full state names to abbreviations
        const stateNameToAbbrev = {
          'São Paulo': 'SP',
          'Rio de Janeiro': 'RJ',
          'Minas Gerais': 'MG',
          'Espírito Santo': 'ES',
          'Rio Grande do Sul': 'RS',
          'Santa Catarina': 'SC',
          Paraná: 'PR',
          'Mato Grosso do Sul': 'MS',
          'Mato Grosso': 'MT',
          Goiás: 'GO',
          'Distrito Federal': 'DF',
          Bahia: 'BA',
          Sergipe: 'SE',
          Alagoas: 'AL',
          Pernambuco: 'PE',
          Paraíba: 'PB',
          'Rio Grande do Norte': 'RN',
          Ceará: 'CE',
          Piauí: 'PI',
          Maranhão: 'MA',
          Tocantins: 'TO',
          Pará: 'PA',
          Amapá: 'AP',
          Roraima: 'RR',
          Amazonas: 'AM',
          Acre: 'AC',
          Rondônia: 'RO',
        }

        // Get state abbreviation
        const stateAbbrev = stateNameToAbbrev[state] || state

        // Try to match the city-state pair with abbreviation
        const key = `${city}-${stateAbbrev}`

        // First try exact city-state match
        if (this.cityStateMap[key]) {
          return this.cityStateMap[key]
        }

        // If no exact match, try the state abbreviation
        if (this.stateMap[stateAbbrev]) {
          return this.stateMap[stateAbbrev]
        }

        // Last resort: use hardcoded coordinates for common cities
        const cityCoordinates = {
          'São Paulo': { latitude: -23.5505, longitude: -46.6333 },
          Barueri: { latitude: -23.5057, longitude: -46.8764 },
          Croatá: { latitude: -4.4085, longitude: -40.9022 },
          Imperatriz: { latitude: -5.5268, longitude: -47.4722 },
          Florianópolis: { latitude: -27.5973, longitude: -48.5496 },
          'Porto Alegre': { latitude: -30.0368, longitude: -51.209 },
          Timóteo: { latitude: -19.5811, longitude: -42.6471 },
          Goiânia: { latitude: -16.6799, longitude: -49.255 },
          'Sete Lagoas': { latitude: -19.4569, longitude: -44.2413 },
          Itabira: { latitude: -19.6186, longitude: -43.2269 },
          Sumaré: { latitude: -22.8204, longitude: -47.2728 },
          'Passo Fundo': { latitude: -28.2576, longitude: -52.4091 },
          Taguatinga: { latitude: -12.4026, longitude: -46.4371 },
          'Pouso Alegre': { latitude: -22.2266, longitude: -45.9389 },
          'Lagoa Santa': { latitude: -19.6333, longitude: -43.8833 },
          'Belo Horizonte': { latitude: -19.9167, longitude: -43.9345 },
        }

        if (cityCoordinates[city]) {
          return cityCoordinates[city]
        }

        return null
      } catch (error) {
        return null
      }
    }
  }

  onMounted(() => {
    // Wait for DOM to be ready before fetching data
    // The fetchLocationData function will initialize the map if needed
    setTimeout(() => {
      fetchLocationData()
    }, 300)
  })

  onBeforeUnmount(() => {
    if (mapInstance) {
      console.log('Removing map instance')
      mapInstance.remove()
    }
  })

  // Watch for filter changes and reload data
  watch(
    () => props.filters,
    async (newFilters, oldFilters) => {
      if (!newFilters) {
        return
      }

      // Check if relevant filters changed (this helps avoid unnecessary reloads)
      const relevantPropsChanged = [
        'job_city',
        'job_state',
        'job_is_remote',
        'dateFrom',
        'dateTo',
        'search_position_query',
      ].some((key) => JSON.stringify(newFilters[key]) !== JSON.stringify(oldFilters?.[key]))

      if (relevantPropsChanged) {
        loading.value = true
        await fetchLocationData()
      }
    },
    { deep: true }
  )
</script>

<style scoped>
  .maplibre-map {
    width: 100%;
    height: 100%;
    min-height: 400px;
    border-radius: 0.5rem;
    overflow: hidden;
    position: relative;
    background-color: #f0f0f0;
  }

  /* Ensure the parent container has height */
  .h-full {
    height: 100%;
    min-height: 400px;
  }

  /* Style for map markers */
  .map-marker {
    cursor: pointer;
    transition: transform 0.2s;
  }

  .map-marker:hover {
    transform: scale(1.2);
  }
</style>
