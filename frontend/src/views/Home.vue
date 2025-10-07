<template>
  <div class="min-h-screen bg-black">
    <!-- Scroll to Top Button -->
    <button
      v-show="showScrollTop"
      class="fixed bottom-8 right-8 bg-gradient-to-r from-cyan-500 to-blue-500 text-white p-3 rounded-full shadow-lg hover:from-cyan-600 hover:to-blue-600 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:ring-offset-2 focus:ring-offset-black z-50"
      aria-label="Voltar ao topo"
      @click="scrollToTop"
    >
      <svg
        class="h-6 w-6"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M5 10l7-7m0 0l7 7m-7-7v18"
        />
      </svg>
    </button>

    <NavBar />

    <!-- Hero Section -->
    <div class="relative bg-gradient-to-b from-black via-gray-900 to-black overflow-hidden">
      <!-- Grid background pattern -->
      <div class="absolute inset-0 bg-[linear-gradient(to_right,#1f2937_1px,transparent_1px),linear-gradient(to_bottom,#1f2937_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]" />
      
      <div class="relative max-w-7xl mx-auto flex flex-col lg:flex-row items-center">
        <div
          class="w-full lg:w-1/2 z-10 pb-8 sm:pb-16 md:pb-20 lg:pb-28 xl:pb-32 flex flex-col justify-center"
        >
          <main
            class="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28"
          >
            <div class="sm:text-center lg:text-left">
              <!-- Badge -->
              <div class="inline-flex items-center space-x-2 bg-gray-800 border border-gray-700 rounded-full px-4 py-2 mb-6">
                <span class="relative flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500" />
                </span>
                <span class="text-gray-300 text-sm font-mono">Now Open Source</span>
              </div>
              
              <h1
                class="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl"
              >
                <span class="block">Literalmente...</span>
                <span class="block bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">De Dev para Dev</span>
              </h1>
              <p
                class="mt-3 text-base text-gray-300 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0 font-mono"
              >
                <span class="text-cyan-400">&gt;</span> Descubra vagas de TI com dados atualizados e filtros avançados para o seu perfil.
                <br>
                <span class="text-cyan-400">&gt;</span> Skills extraídas com IA, rankings de empresas e insights acionáveis.
                <br>
                <span class="text-cyan-400">&gt;</span> Contribua com o projeto!
              </p>
              <div class="mt-8 sm:flex sm:justify-center lg:justify-start space-y-4 sm:space-y-0 sm:space-x-4">
                <router-link
                  to="/auth/login"
                  class="group relative inline-flex items-center justify-center px-8 py-3 overflow-hidden font-mono font-medium tracking-tighter text-white bg-gradient-to-r from-cyan-500 to-blue-600 rounded-lg hover:scale-105 transition-transform duration-300 shadow-lg shadow-cyan-500/50"
                >
                  <span class="absolute w-0 h-0 transition-all duration-500 ease-out bg-white rounded-full group-hover:w-56 group-hover:h-56 opacity-10" />
                  <span class="relative">Acessar plataforma →</span>
                </router-link>
                
                <a
                  href="https://github.com/danilopds/hiremetrics"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="inline-flex items-center justify-center px-8 py-3 border border-gray-600 text-base font-mono font-medium rounded-lg text-gray-300 bg-gray-800 hover:bg-gray-700 hover:border-gray-500 transition-all duration-300"
                >
                  <svg
                    class="w-5 h-5 mr-2"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  View Source
                </a>
              </div>
              
              <!-- GitHub Stars -->
              <div class="mt-8 flex items-center space-x-4 sm:justify-center lg:justify-start">
                <a 
                  href="https://github.com/danilopds/hiremetrics" 
                  target="_blank"
                  rel="noopener noreferrer"
                  class="flex items-center space-x-2 text-gray-400 hover:text-gray-200 transition-colors"
                >
                  <svg
                    class="w-4 h-4"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span class="text-sm font-mono">8 stars</span>
                </a>
                <span class="text-gray-600">•</span>
                <span class="text-sm font-mono text-gray-400">MIT License</span>
              </div>
            </div>
          </main>
        </div>
        <div class="w-full lg:w-1/2 flex justify-center items-center mt-8 lg:mt-0 px-4">
          <div class="relative">
            <div class="absolute inset-0 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg blur-3xl opacity-20" />
            <img
              class="relative w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-full h-auto object-contain"
              src="@/assets/img/hero.png"
              alt="Dashboard ilustrativo do HireMetrics"
            >
          </div>
        </div>
      </div>

      <!-- Scroll indicator -->
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div class="flex flex-col items-center text-cyan-500">
          <svg
            class="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 14l-7 7m0 0l-7-7m7 7V3"
            />
          </svg>
        </div>
      </div>
    </div>

    <!-- Data Preview Section -->
    <DataPreviewSection />

    <!-- Benefits Section -->
    <div
      id="benefits"
      class="py-12 bg-gradient-to-b from-black to-gray-900 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-cyan-400 font-semibold tracking-wide uppercase font-mono">
            <span class="text-cyan-500">//</span> Features
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl"
          >
            Built for Developers
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-300 lg:mx-auto font-mono">
            Analytics tools com dados reais do mercado tech brasileiro. Open source, grátis, e construído por devs para devs.
          </p>
        </div>

        <div class="mt-20">
          <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
            <div class="relative group">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-lg bg-gradient-to-br from-cyan-500 to-blue-600 text-white transform transition-transform group-hover:scale-110 shadow-lg shadow-cyan-500/50"
              >
                <svg
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-white font-mono">
                  AI-Powered Skills Extraction
                </h3>
                <p class="mt-2 text-base text-gray-400">
                  IA extrai skills de job descriptions automaticamente. Identifique tendências e mantenha seu stack atualizado com o mercado.
                </p>
              </div>
            </div>

            <div class="relative group">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-lg bg-gradient-to-br from-purple-500 to-pink-600 text-white transform transition-transform group-hover:scale-110 shadow-lg shadow-purple-500/50"
              >
                <svg
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-white font-mono">
                  ETL Pipeline
                </h3>
                <p class="mt-2 text-base text-gray-400">
                  Pipeline ETL roda diariamente. Dados frescos do mercado tech brasileiro, sempre atualizados.
                </p>
              </div>
            </div>

            <div class="relative group">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-lg bg-gradient-to-br from-green-500 to-emerald-600 text-white transform transition-transform group-hover:scale-110 shadow-lg shadow-green-500/50"
              >
                <svg
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-white font-mono">
                  100% Open Source
                </h3>
                <p class="mt-2 text-base text-gray-400">
                  Todo o código está no GitHub. Fork, contribua ou rode localmente. MIT License. Nenhuma string attached.
                </p>
              </div>
            </div>

            <div class="relative group">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-lg bg-gradient-to-br from-orange-500 to-red-600 text-white transform transition-transform group-hover:scale-110 shadow-lg shadow-orange-500/50"
              >
                <svg
                  class="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-white font-mono">
                  Exportações de Dados
                </h3>
                <p class="mt-2 text-base text-gray-400">
                  Exporte até 50k registros. Manipule dados como você quiser. Python, R, Excel - você decide.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- How It Works Section -->
    <div
      id="how-it-works"
      class="bg-gray-900 py-12 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center mb-10">
          <h2 class="text-base text-cyan-400 font-semibold tracking-wide uppercase font-mono">
            <span class="text-cyan-500">//</span> Architecture
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl"
          >
            Como funciona?
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-300 lg:mx-auto font-mono">
            Pipeline ETL automatizado. Coleta → Processa → Visualiza. Simple as that.
          </p>
        </div>

        <div class="mt-10">
          <div class="grid grid-cols-1 gap-10 lg:grid-cols-3">
            <!-- Step 1 -->
            <div class="relative">
              <div class="text-center bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-cyan-500 transition-colors">
                <div class="flex justify-center mb-4">
                  <div class="bg-gradient-to-br from-cyan-500 to-blue-600 rounded-lg p-4 shadow-lg shadow-cyan-500/50">
                    <svg
                      class="w-12 h-12 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                      />
                    </svg>
                  </div>
                </div>
                <h3 class="text-lg font-medium text-white mb-4 font-mono">
                  <span class="text-cyan-400">01.</span> Data Collection
                </h3>
                <p class="mt-2 text-base text-gray-400">
                  Scrapers automatizados coletam vagas de múltiplas fontes. Daily cron jobs mantém os dados frescos.
                </p>
              </div>
            </div>

            <!-- Step 2 -->
            <div class="relative">
              <div class="text-center bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-purple-500 transition-colors">
                <div class="flex justify-center mb-4">
                  <div class="bg-gradient-to-br from-purple-500 to-pink-600 rounded-lg p-4 shadow-lg shadow-purple-500/50">
                    <svg
                      class="w-12 h-12 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
                      />
                    </svg>
                  </div>
                </div>
                <h3 class="text-lg font-medium text-white mb-4 font-mono">
                  <span class="text-purple-400">02.</span> AI Processing
                </h3>
                <p class="mt-2 text-base text-gray-400">
                  LLMs extraem skills das descrições. dbt transforma raw data em analytics-ready datasets.
                </p>
              </div>
            </div>

            <!-- Step 3 -->
            <div class="relative">
              <div class="text-center bg-gray-800 rounded-lg p-6 border border-gray-700 hover:border-green-500 transition-colors">
                <div class="flex justify-center mb-4">
                  <div class="bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg p-4 shadow-lg shadow-green-500/50">
                    <svg
                      class="w-12 h-12 text-white"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                      />
                    </svg>
                  </div>
                </div>
                <h3 class="text-lg font-medium text-white mb-4 font-mono">
                  <span class="text-green-400">03.</span> Interactive Viz
                </h3>
                <p class="mt-2 text-base text-gray-400">
                  FastAPI + Vue.js servem dashboards interativos. ECharts renderiza gráficos. Export para CSV quando precisar.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Community Section -->
    <div
      id="community"
      class="bg-gradient-to-b from-gray-900 to-black py-12 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center mb-10">
          <h2 class="text-base text-cyan-400 font-semibold tracking-wide uppercase font-mono">
            <span class="text-cyan-500">//</span> Community
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl"
          >
            Join the Community
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-300 lg:mx-auto">
            Open source. Built in public. Contributors welcome.
          </p>
        </div>

        <div class="mt-10 grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          <!-- GitHub Card -->
          <a
            href="https://github.com/danilopds/hiremetrics"
            target="_blank"
            rel="noopener noreferrer"
            class="group relative bg-gradient-to-br from-gray-800 to-gray-900 rounded-lg p-8 border border-gray-700 hover:border-cyan-500 transition-all duration-300 hover:scale-105"
          >
            <div class="flex items-center mb-4">
              <div class="bg-gradient-to-br from-gray-700 to-gray-800 rounded-lg p-3">
                <svg
                  class="w-8 h-8 text-white"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    fill-rule="evenodd"
                    d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                    clip-rule="evenodd"
                  />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-xl font-bold text-white font-mono">GitHub</h3>
                <p class="text-sm text-gray-400 font-mono">Contribua com o código</p>
              </div>
            </div>
            <p class="text-gray-300 mb-4">
              Fork o repositório, abra issues, submeta PRs. Toda contribuição é bem-vinda - desde correções de bugs até novas features.
            </p>
            <div class="flex items-center space-x-4 text-sm text-gray-400">
              <span class="flex items-center">
                <svg
                  class="w-4 h-4 mr-1 text-yellow-400"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                8 stars
              </span>
              <span class="text-gray-600">•</span>
              <span>MIT License</span>
            </div>
            <div class="absolute top-4 right-4 text-gray-500 group-hover:text-cyan-400 transition-colors">
              <svg
                class="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                />
              </svg>
            </div>
          </a>

          <!-- Discord Card -->
          <a
            href="https://discord.gg/rr7TkzzR"
            target="_blank"
            rel="noopener noreferrer"
            class="group relative bg-gradient-to-br from-indigo-900/50 to-purple-900/50 rounded-lg p-8 border border-indigo-700 hover:border-indigo-500 transition-all duration-300 hover:scale-105"
          >
            <div class="flex items-center mb-4">
              <div class="bg-gradient-to-br from-indigo-600 to-purple-600 rounded-lg p-3">
                <svg
                  class="w-8 h-8 text-white"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path d="M20.317 4.37a19.791 19.791 0 00-4.885-1.515.074.074 0 00-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 00-5.487 0 12.64 12.64 0 00-.617-1.25.077.077 0 00-.079-.037A19.736 19.736 0 003.677 4.37a.07.07 0 00-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 00.031.057 19.9 19.9 0 005.993 3.03.078.078 0 00.084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 00-.041-.106 13.107 13.107 0 01-1.872-.892.077.077 0 01-.008-.128 10.2 10.2 0 00.372-.292.074.074 0 01.077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 01.078.01c.12.098.246.198.373.292a.077.077 0 01-.006.127 12.299 12.299 0 01-1.873.892.077.077 0 00-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 00.084.028 19.839 19.839 0 006.002-3.03.077.077 0 00.032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 00-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z" />
                </svg>
              </div>
              <div class="ml-4">
                <h3 class="text-xl font-bold text-white font-mono">Discord</h3>
                <p class="text-sm text-indigo-300 font-mono">Junte-se à comunidade</p>
              </div>
            </div>
            <p class="text-gray-200 mb-4">
              Discuta features, tire dúvidas, compartilhe insights sobre o mercado tech. A comunidade está crescendo!
            </p>
            <div class="inline-flex items-center space-x-2 bg-indigo-800/50 rounded-full px-4 py-2">
              <span class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
                <span class="relative inline-flex rounded-full h-2 w-2 bg-green-400" />
              </span>
              <span class="text-sm text-indigo-200 font-mono">Active community</span>
            </div>
            <div class="absolute top-4 right-4 text-indigo-400 group-hover:text-indigo-300 transition-colors">
              <svg
                class="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                />
              </svg>
            </div>
          </a>
        </div>
      </div>
    </div>

    <!-- Demo Section -->
    <div
      id="demo"
      class="bg-black py-12 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center mb-10">
          <h2 class="text-base text-cyan-400 font-semibold tracking-wide uppercase font-mono">
            <span class="text-cyan-500">//</span> Demo
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl"
          >
            Veja em ação
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-300 lg:mx-auto">
            Dashboards interativos, gráficos com ECharts, e dados atualizados diariamente.
          </p>
        </div>

        <div class="mt-10 rounded-lg overflow-hidden border border-gray-800 shadow-2xl">
          <!--ARCADE EMBED START-->
          <div
            style="
              position: relative;
              padding-bottom: calc(49.271451699946034% + 41px);
              height: 0;
              width: 100%;
            "
          >
            <iframe
              src="https://demo.arcade.software/l3ACeCcyhST8RRRB3z5j?embed&embed_mobile=tab&embed_desktop=inline&show_copy_link=true"
              title="HireMetrics - Dados que contratam"
              frameborder="0"
              loading="lazy"
              webkitallowfullscreen
              mozallowfullscreen
              allowfullscreen
              allow="clipboard-write"
              style="
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                color-scheme: light;
              "
            />
          </div>
          <!--ARCADE EMBED END-->
        </div>
      </div>
    </div>

    <!-- Social Proof Section -->
    <div
      id="testimonials"
      class="bg-gradient-to-b from-black to-gray-900 py-12 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center mb-10">
          <h2 class="text-base text-cyan-400 font-semibold tracking-wide uppercase font-mono">
            <span class="text-cyan-500">//</span> Testimonials
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl"
          >
            O que a galera diz
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-300 lg:mx-auto">
            Profissionais usando HireMetrics para tomar decisões baseadas em dados.
          </p>
        </div>

        <div class="mt-10">
          <div class="grid grid-cols-1 gap-8 md:grid-cols-2">
            <!-- Testimonial 1 -->
            <div
              class="bg-gradient-to-br from-gray-800 to-gray-900 p-6 rounded-lg border border-gray-700 shadow-lg transform transition-all duration-300 hover:scale-105 hover:border-cyan-500"
            >
              <div class="flex items-center mb-4">
                <div class="flex-shrink-0">
                  <img
                    class="h-12 w-12 rounded-full ring-2 ring-cyan-500"
                    src="https://i.pravatar.cc/150?img=5"
                    alt="Avatar da Carla"
                  >
                </div>
                <div class="ml-4">
                  <h4 class="text-lg font-medium text-white font-mono">
                    Carla A.
                  </h4>
                  <p class="text-sm text-gray-400">
                    Analista de RH
                  </p>
                </div>
              </div>
              <p class="text-gray-300 italic">
                "Graças ao HireMetrics com dados sempre atualizados, entendemos rapidamente as
                tendências do mercado e ajustamos nossa estratégia."
              </p>
            </div>

            <!-- Testimonial 2 -->
            <div
              class="bg-gradient-to-br from-gray-800 to-gray-900 p-6 rounded-lg border border-gray-700 shadow-lg transform transition-all duration-300 hover:scale-105 hover:border-purple-500"
            >
              <div class="flex items-center mb-4">
                <div class="flex-shrink-0">
                  <img
                    class="h-12 w-12 rounded-full ring-2 ring-purple-500"
                    src="https://i.pravatar.cc/150?img=12"
                    alt="Avatar do João"
                  >
                </div>
                <div class="ml-4">
                  <h4 class="text-lg font-medium text-white font-mono">
                    João M.
                  </h4>
                  <p class="text-sm text-gray-400">
                    Desenvolvedor Senior
                  </p>
                </div>
              </div>
              <p class="text-gray-300 italic">
                "Com o HireMetrics, consigo acompanhar quais skills estão em alta no mercado e me
                preparar melhor para as oportunidades."
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ Section -->
    <div
      id="faq"
      class="bg-gray-900 py-12 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center mb-10">
          <h2 class="text-base text-cyan-400 font-semibold tracking-wide uppercase font-mono">
            <span class="text-cyan-500">//</span> FAQ
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl"
          >
            Perguntas Frequentes
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-300 lg:mx-auto">
            Respostas para as dúvidas mais comuns sobre a plataforma.
          </p>
        </div>

        <div class="mt-10 max-w-3xl mx-auto">
          <dl class="space-y-6 divide-y divide-gray-700">
            <div class="pt-6">
              <dt class="text-lg">
                <button
                  class="text-left w-full flex justify-between items-start text-gray-400"
                  @click="toggleFaq(0)"
                >
                  <span class="font-medium text-white font-mono">A plataforma é realmente gratuita?</span>
                  <span class="ml-6 h-7 flex items-center">
                    <svg
                      class="h-6 w-6 transform transition-transform duration-200 text-cyan-400"
                      :class="{ 'rotate-0': !openFaqs[0], '-rotate-180': openFaqs[0] }"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </span>
                </button>
              </dt>
              <dd
                v-show="openFaqs[0]"
                class="mt-2 pr-12"
              >
                <p class="text-base text-gray-400">
                  Sim! A plataforma é 100% gratuita e open source. Código disponível no GitHub sob MIT License. Sem custos ocultos, sem limites artificiais.
                </p>
              </dd>
            </div>

            <div class="pt-6">
              <dt class="text-lg">
                <button
                  class="text-left w-full flex justify-between items-start text-gray-400"
                  @click="toggleFaq(2)"
                >
                  <span class="font-medium text-white font-mono">Com que frequência os dados são atualizados?</span>
                  <span class="ml-6 h-7 flex items-center">
                    <svg
                      class="h-6 w-6 transform transition-transform duration-200 text-cyan-400"
                      :class="{ 'rotate-0': !openFaqs[2], '-rotate-180': openFaqs[2] }"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </span>
                </button>
              </dt>
              <dd
                v-show="openFaqs[2]"
                class="mt-2 pr-12"
              >
                <p class="text-base text-gray-400">
                  Pipeline ETL roda diariamente. Coletamos milhares de vagas de múltiplas fontes, processamos com IA e disponibilizamos dados frescos todo dia.
                </p>
              </dd>
            </div>

            <div class="pt-6">
              <dt class="text-lg">
                <button
                  class="text-left w-full flex justify-between items-start text-gray-400"
                  @click="toggleFaq(3)"
                >
                  <span class="font-medium text-white font-mono">Posso contribuir com o projeto?</span>
                  <span class="ml-6 h-7 flex items-center">
                    <svg
                      class="h-6 w-6 transform transition-transform duration-200 text-cyan-400"
                      :class="{ 'rotate-0': !openFaqs[3], '-rotate-180': openFaqs[3] }"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </span>
                </button>
              </dt>
              <dd
                v-show="openFaqs[3]"
                class="mt-2 pr-12"
              >
                <p class="text-base text-gray-400">
                  Absolutamente! Fork o repo no GitHub, abra issues, submeta PRs. Join no Discord para discutir ideias. Toda contribuição é muito bem-vinda.
                </p>
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </div>

    <!-- Final CTA Section -->
    <div
      id="final-cta"
      class="bg-gradient-to-r from-cyan-600 via-blue-600 to-purple-600 py-12 scroll-mt-16 relative overflow-hidden"
    >
      <!-- Animated background pattern -->
      <div class="absolute inset-0 bg-[linear-gradient(to_right,#ffffff10_1px,transparent_1px),linear-gradient(to_bottom,#ffffff10_1px,transparent_1px)] bg-[size:4rem_4rem]" />
      
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl font-mono">
          $ ready to start?
        </h2>
        <p class="mt-4 text-xl text-blue-100">
          Join developers que já usam dados reais e open source para tomar decisões informadas.
        </p>
        <div class="mt-8 flex justify-center space-x-4">
          <router-link
            to="/auth/login"
            class="group relative inline-flex items-center px-8 py-3 overflow-hidden font-mono font-medium tracking-tighter text-white bg-black rounded-lg hover:scale-105 transition-transform duration-300 shadow-lg"
          >
            <span class="absolute w-0 h-0 transition-all duration-500 ease-out bg-white rounded-full group-hover:w-56 group-hover:h-56 opacity-10" />
            <span class="relative">Acessar plataforma →</span>
          </router-link>
          
          <a
            href="https://github.com/danilopds/hiremetrics"
            target="_blank"
            rel="noopener noreferrer"
            class="inline-flex items-center px-8 py-3 border-2 border-white text-base font-mono font-medium rounded-lg text-white hover:bg-white hover:text-blue-600 transition-all duration-300"
          >
            <svg
              class="w-5 h-5 mr-2"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                fill-rule="evenodd"
                d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
                clip-rule="evenodd"
              />
            </svg>
            GitHub
          </a>
        </div>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
  import { ref, onMounted, onUnmounted } from 'vue'
  import NavBar from '@/components/NavBar.vue'
  import AppFooter from '@/components/Footer.vue'
  import DataPreviewSection from '@/components/DataPreviewSection.vue'

  defineOptions({
    name: 'HomePage',
  })

  const showScrollTop = ref(false)
  const openFaqs = ref([false, false, false, false])

  const handleScroll = () => {
    showScrollTop.value = window.scrollY > 300
  }

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  }

  const toggleFaq = (index) => {
    openFaqs.value[index] = !openFaqs.value[index]
  }

  onMounted(() => {
    window.addEventListener('scroll', handleScroll)

    // Add smooth scroll behavior to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', function (e) {
        e.preventDefault()
        const targetId = this.getAttribute('href')
        const targetElement = document.querySelector(targetId)
        if (targetElement) {
          targetElement.scrollIntoView({
            behavior: 'smooth',
          })
        }
      })
    })
  })

  onUnmounted(() => {
    window.removeEventListener('scroll', handleScroll)
  })
</script>

<style>
  html {
    scroll-behavior: smooth;
  }
</style>
