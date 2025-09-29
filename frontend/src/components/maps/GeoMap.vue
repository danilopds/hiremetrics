<template>
  <LMap
    ref="mapRef"
    :zoom="zoom"
    :center="center"
    style="height: 100%; width: 100%"
    :use-global-leaflet="false"
    @ready="handleMapReady"
  >
    <LTileLayer
      :url="tileUrl"
      :attribution="attribution"
    />
    <LMarker
      v-for="loc in locations"
      :key="loc.id"
      :lat-lng="loc.position"
    >
      <LPopup>
        <div class="text-sm">
          <div class="font-bold">
            {{ loc.title }}
          </div>
          <div>{{ loc.description }}</div>
          <div>
            Jobs: <span class="font-semibold">{{ loc.jobCount }}</span>
          </div>
          <div>Avg Salary: ${{ loc.avgSalary.toLocaleString() }}</div>
        </div>
      </LPopup>
    </LMarker>
  </LMap>
</template>

<script setup>
  import { computed, ref, watch, nextTick } from 'vue'
  import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'

  const props = defineProps({
    locations: { type: Array, required: true },
  })

  const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
  const attribution =
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

  const center = computed(() => {
    if (props.locations.length > 0) {
      return props.locations[0].position
    }
    return [0, 0]
  })
  const zoom = 2

  const mapRef = ref(null)

  function handleMapReady(mapObject) {
    nextTick(() => {
      mapObject.invalidateSize()
    })
  }

  watch(
    () => props.locations,
    () => {
      if (mapRef.value) {
        nextTick(() => {
          mapRef.value.leafletObject.invalidateSize()
        })
      }
    }
  )
</script>

<style scoped>
  .leaflet-container {
    display: block;
    height: 100% !important;
    width: 100% !important;
    max-width: 100%;
    max-height: 100%;
    min-height: 300px;
    overflow: hidden;
  }
</style>
