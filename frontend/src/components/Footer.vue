<template>
  <footer class="bg-gray-50">
    <div class="max-w-7xl mx-auto py-12 px-4 overflow-hidden sm:px-6 lg:px-8">
      <nav
        class="-mx-5 -my-2 flex flex-wrap justify-center"
        aria-label="Footer"
      >
        <div class="px-5 py-2">
          <router-link
            to="/"
            class="text-base text-gray-500 hover:text-gray-900 transition-colors duration-300"
          >
            Início
          </router-link>
        </div>
        <div class="px-5 py-2">
          <router-link
            to="/sobre"
            class="text-base text-gray-500 hover:text-gray-900 transition-colors duration-300"
          >
            Sobre Nós
          </router-link>
        </div>
        <div class="px-5 py-2">
          <router-link
            to="/contato"
            class="text-base text-gray-500 hover:text-gray-900 transition-colors duration-300"
          >
            Contato
          </router-link>
        </div>
        <div class="px-5 py-2">
          <router-link
            to="/termos-de-uso"
            class="text-base text-gray-500 hover:text-gray-900 transition-colors duration-300"
          >
            Termos de Uso
          </router-link>
        </div>
        <div class="px-5 py-2">
          <router-link
            to="/politica-privacidade"
            class="text-base text-gray-500 hover:text-gray-900 transition-colors duration-300"
          >
            Política de Privacidade
          </router-link>
        </div>
      </nav>
      <p class="mt-8 text-center text-base text-gray-400">
        &copy; 2025 HireMetrics. Todos os direitos reservados.
      </p>
    </div>
  </footer>
</template>

<script>
  export default {
    name: 'AppFooter',
  }
</script>
