<template>
  <NConfigProvider>
    <NMessageProvider>
      <NNotificationProvider>
        <NDialogProvider>
          <div class="app-container">
            <router-view v-slot="{ Component }">
              <component :is="Component" />
            </router-view>
          </div>
        </NDialogProvider>
      </NNotificationProvider>
    </NMessageProvider>
  </NConfigProvider>
</template>

<script setup>
  import {
    NConfigProvider,
    NMessageProvider,
    NNotificationProvider,
    NDialogProvider,
  } from 'naive-ui'
  import { onMounted } from 'vue'
  import { useRouter } from 'vue-router'

  const router = useRouter()

  onMounted(() => {
    console.log('App mounted')
    console.log('Current route:', router.currentRoute.value.path)
  })
</script>

<style>
  @tailwind base;
  @tailwind components;
  @tailwind utilities;

  .app-container {
    min-height: 100vh;
    background-color: rgb(249 250 251);
  }
</style>
