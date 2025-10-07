<template>
  <div
    v-if="showPopup"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    @click="closePopup"
  >
    <div
      class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 transform transition-all duration-300 scale-100"
      @click.stop
    >
      <!-- Header -->
      <div class="bg-gradient-to-r from-blue-600 to-blue-700 rounded-t-lg p-3 text-center">
        <div class="text-2xl mb-1">
          🎉
        </div>
        <h2 class="text-lg font-bold text-white mb-1">
          Bem-vindo ao HireMetrics!
        </h2>
        <p class="text-blue-100 text-xs">
          Sua plataforma de análise do mercado de trabalho
        </p>
      </div>

      <!-- Content -->
      <div class="p-3 text-center">
        <div class="mb-3">
          <div class="text-3xl text-green-500 mb-1">
            💎
          </div>
          <h3 class="text-lg font-semibold text-gray-900 mb-1">
            Bem-vindo ao HireMetrics!
          </h3>
          <p class="text-gray-600 text-xs leading-relaxed">
            Explore livremente todas as funcionalidades disponíveis na plataforma. Descubra
            insights valiosos sobre o mercado de tecnologia brasileiro.
          </p>
        </div>

        <!-- Features List -->
        <div class="text-left mb-3">
          <h4 class="font-semibold text-gray-900 mb-2 text-center text-sm">
            O que você pode fazer:
          </h4>
          <div class="space-y-1 text-xs text-gray-600">
            <div class="flex items-center">
              <span class="text-green-500 mr-1">✓</span>
              Explorar vagas com filtros avançados
            </div>
            <div class="flex items-center">
              <span class="text-green-500 mr-1">✓</span>
              Descobrir vagas por empresas com filtros avançados
            </div>
            <div class="flex items-center">
              <span class="text-green-500 mr-1">✓</span>
              Visualizar detalhes completos das vagas
            </div>
            <div class="flex items-center">
              <span class="text-green-500 mr-1">✓</span>
              Gerar relatórios personalizados
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="bg-gray-50 rounded-b-lg px-3 py-2 flex justify-center">
        <button
          class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 text-sm"
          @click="closePopup"
        >
          Começar a Explorar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'

  const showPopup = ref(false)

  const closePopup = () => {
    showPopup.value = false
    // Store in sessionStorage so it doesn't show again in this session
    sessionStorage.setItem('welcome-popup-shown', 'true')
  }

  onMounted(async () => {
    // Check if popup was already shown in this session
    const alreadyShown = sessionStorage.getItem('welcome-popup-shown')
    if (!alreadyShown) {
      // Show popup after a short delay for better UX
      setTimeout(() => {
        showPopup.value = true
      }, 1000)
    }
  })

  // Expose method to show popup programmatically if needed
  defineExpose({
    showPopup: () => {
      showPopup.value = true
    },
  })
</script>

<style scoped>
  /* Animation classes */
  .scale-100 {
    transform: scale(1);
  }

  /* Ensure popup is above everything */
  .z-50 {
    z-index: 9999;
  }
</style>
