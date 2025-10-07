<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Scroll to Top Button -->
    <button
      v-show="showScrollTop"
      class="fixed bottom-8 right-8 bg-blue-600 text-white p-3 rounded-full shadow-lg hover:bg-blue-700 transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 z-50"
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
    <div class="relative bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto flex flex-col lg:flex-row items-center">
        <div
          class="w-full lg:w-1/2 z-10 pb-8 sm:pb-16 md:pb-20 lg:pb-28 xl:pb-32 flex flex-col justify-center"
        >
          <main
            class="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 md:mt-16 lg:mt-20 lg:px-8 xl:mt-28"
          >
            <div class="sm:text-center lg:text-left">
              <h1
                class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl"
              >
                <span class="block">Mercado de TI</span>
                <span class="block text-blue-600">em números</span>
              </h1>
              <p
                class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0"
              >
                Veja quais empresas mais contratam e as skills tech mais exigidas em tempo real.
                Entenda o mercado de tecnologia com dados atualizados e tendências do setor.
              </p>
              <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div class="rounded-md shadow">
                  <router-link
                    to="/auth/login"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10 transition-all duration-300"
                  >
                    👉 Acompanhe empresas em alta
                  </router-link>
                </div>
              </div>
            </div>
          </main>
        </div>
        <div class="w-full lg:w-1/2 flex justify-center items-center mt-8 lg:mt-0">
          <img
            class="w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-full h-auto object-contain"
            src="@/assets/img/hero.png"
            alt="Dashboard do mercado de tecnologia"
          >
        </div>
      </div>

      <!-- Scroll indicator -->
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div class="flex flex-col items-center text-gray-500">
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
      class="py-20 bg-gray-50 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Tendências do mercado TI
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            Por que acompanhar o mercado de tecnologia?
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Fique por dentro das tendências, skills mais buscadas e empresas que estão contratando
            em tempo real com dados reais do mercado.
          </p>
        </div>

        <div class="mt-20">
          <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
            <div class="relative group">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white transform transition-transform group-hover:scale-110"
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
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Skills tech mais buscadas
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Descubra quais habilidades estão em alta no mercado tech e quais empresas mais
                  valorizam cada competência.
                </p>
              </div>
            </div>

            <div class="relative group">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white transform transition-transform group-hover:scale-110"
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
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Empresas que contratam TI
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Acompanhe quais empresas estão mais ativas no mercado, suas demandas e
                  oportunidades de carreira.
                </p>
              </div>
            </div>

            <div class="relative group">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white transform transition-transform group-hover:scale-110"
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
                    d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Tendências do mercado tech
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Identifique as tecnologias emergentes e as mudanças no mercado de trabalho de
                  tecnologia.
                </p>
              </div>
            </div>

            <div class="relative group">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white transform transition-transform group-hover:scale-110"
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
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Dados em tempo real
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Acesse informações atualizadas diariamente sobre vagas e tendências do mercado de
                  TI.
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
      class="bg-white py-20 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center mb-10">
          <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Como Funciona
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            Análise do Mercado de Tecnologia
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Nossa plataforma monitora o mercado tech, analisa tendências e apresenta insights
            práticos para profissionais e empresas.
          </p>
        </div>

        <div class="mt-10">
          <div class="grid grid-cols-1 gap-10 lg:grid-cols-3">
            <!-- Step 1 -->
            <div class="relative">
              <div class="text-center">
                <div class="flex justify-center mb-0">
                  <img
                    src="@/assets/img/howto_1.svg"
                    alt="Monitoramento do mercado tech"
                    class="w-80 h-80 object-contain"
                  >
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-4">
                  1. Monitoramento do mercado tech
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Rastreamos milhares de vagas de tecnologia diariamente para capturar as tendências
                  mais recentes do mercado.
                </p>
              </div>
            </div>

            <!-- Step 2 -->
            <div class="relative">
              <div class="text-center">
                <div class="flex justify-center mb-0">
                  <img
                    src="@/assets/img/howto_2.svg"
                    alt="Análise de tendências"
                    class="w-80 h-80 object-contain"
                  >
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-4">
                  2. Análise de tendências
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Nossa IA identifica skills em alta, empresas que mais contratam e oportunidades
                  emergentes no mercado tech.
                </p>
              </div>
            </div>

            <!-- Step 3 -->
            <div class="relative">
              <div class="text-center">
                <div class="flex justify-center mb-0">
                  <img
                    src="@/assets/img/howto_3.svg"
                    alt="Insights acionáveis"
                    class="w-80 h-80 object-contain"
                  >
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-4">
                  3. Insights acionáveis
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Use os dados para planejar sua carreira, identificar oportunidades e entender o
                  que o mercado valoriza.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Demo Section -->
    <div
      id="demo"
      class="bg-gray-50 py-20 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center mb-10">
          <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Demonstração
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            Veja o mercado tech em ação
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Explore nossos dashboards com dados do mercado de tecnologia, tendências de skills e
            empresas que estão contratando.
          </p>
        </div>

        <div class="mt-10">
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
              title="HireMetrics - Mercado de Tecnologia"
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
      class="bg-gray-50 py-20 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center mb-10">
          <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Depoimentos
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            Profissionais já confiam no HireMetrics
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Veja como outros profissionais de TI estão usando dados reais para entender o mercado e
            planejar suas carreiras.
          </p>
        </div>

        <div class="mt-10">
          <div class="grid grid-cols-1 gap-8 md:grid-cols-2">
            <!-- Testimonial 1 -->
            <div
              class="bg-gray-50 p-6 rounded-lg shadow-lg transform transition-all duration-300 hover:scale-105"
            >
              <div class="flex items-center mb-4">
                <div class="flex-shrink-0">
                  <img
                    class="h-12 w-12 rounded-full"
                    src="https://i.pravatar.cc/150?img=8"
                    alt="Avatar da Ana"
                  >
                </div>
                <div class="ml-4">
                  <h4 class="text-lg font-medium text-gray-900">
                    João P.
                  </h4>
                  <p class="text-sm text-gray-500">
                    Desenvolvedor Full Stack
                  </p>
                </div>
              </div>
              <p class="text-gray-600 italic">
                "Com o HireMetrics, consegui identificar quais skills estão mais em alta no mercado.
                Isso me ajudou a focar nos estudos certos e conseguir uma promoção."
              </p>
            </div>

            <!-- Testimonial 2 -->
            <div
              class="bg-gray-50 p-6 rounded-lg shadow-lg transform transition-all duration-300 hover:scale-105"
            >
              <div class="flex items-center mb-4">
                <div class="flex-shrink-0">
                  <img
                    class="h-12 w-12 rounded-full"
                    src="https://i.pravatar.cc/150?img=15"
                    alt="Avatar do Pedro"
                  >
                </div>
                <div class="ml-4">
                  <h4 class="text-lg font-medium text-gray-900">
                    Pedro S.
                  </h4>
                  <p class="text-sm text-gray-500">
                    Tech Lead
                  </p>
                </div>
              </div>
              <p class="text-gray-600 italic">
                "Os dados do mercado nos ajudaram a entender quais empresas estão contratando mais e
                quais tecnologias estão em alta. É uma ferramenta essencial para planejar nossa
                estratégia."
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- FAQ Section -->
    <div
      id="faq"
      class="bg-white py-20 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center mb-10">
          <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
            FAQ
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            Perguntas Frequentes
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Respostas para as dúvidas mais comuns sobre nossa plataforma de análise do mercado de
            tecnologia.
          </p>
        </div>

        <div class="mt-10 max-w-3xl mx-auto">
          <dl class="space-y-6 divide-y divide-gray-200">
            <div class="pt-6">
              <dt class="text-lg">
                <button
                  class="text-left w-full flex justify-between items-start text-gray-400"
                  @click="toggleFaq(0)"
                >
                  <span class="font-medium text-gray-900">Como os dados ajudam a entender o mercado?</span>
                  <span class="ml-6 h-7 flex items-center">
                    <svg
                      class="h-6 w-6 transform transition-transform duration-200"
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
                <p class="text-base text-gray-500">
                  Nossos dados mostram as skills mais demandadas, empresas que mais contratam e
                  tendências salariais, permitindo entender melhor o mercado de tecnologia.
                </p>
              </dd>
            </div>

            <div class="pt-6">
              <dt class="text-lg">
                <button
                  class="text-left w-full flex justify-between items-start text-gray-400"
                  @click="toggleFaq(1)"
                >
                  <span class="font-medium text-gray-900">Os dados são atualizados com que frequência?</span>
                  <span class="ml-6 h-7 flex items-center">
                    <svg
                      class="h-6 w-6 transform transition-transform duration-200"
                      :class="{ 'rotate-0': !openFaqs[1], '-rotate-180': openFaqs[1] }"
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
                v-show="openFaqs[1]"
                class="mt-2 pr-12"
              >
                <p class="text-base text-gray-500">
                  Nossos dados são atualizados diariamente, garantindo que você sempre tenha acesso
                  às informações mais recentes do mercado de tecnologia.
                </p>
              </dd>
            </div>

            <div class="pt-6">
              <dt class="text-lg">
                <button
                  class="text-left w-full flex justify-between items-start text-gray-400"
                  @click="toggleFaq(2)"
                >
                  <span class="font-medium text-gray-900">Posso exportar os dados para análises?</span>
                  <span class="ml-6 h-7 flex items-center">
                    <svg
                      class="h-6 w-6 transform transition-transform duration-200"
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
                <p class="text-base text-gray-500">
                  Sim! Você pode exportar dados em CSV para análises mais profundas e relatórios
                  personalizados sobre o mercado tech.
                </p>
              </dd>
            </div>

            <div class="pt-6">
              <dt class="text-lg">
                <button
                  class="text-left w-full flex justify-between items-start text-gray-400"
                  @click="toggleFaq(3)"
                >
                  <span class="font-medium text-gray-900">Como posso usar os insights na prática?</span>
                  <span class="ml-6 h-7 flex items-center">
                    <svg
                      class="h-6 w-6 transform transition-transform duration-200"
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
                <p class="text-base text-gray-500">
                  Use os dados para planejar sua carreira, identificar skills em alta, escolher
                  empresas para trabalhar e entender as tendências do mercado tech.
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
      class="bg-blue-600 py-20 scroll-mt-16"
    >
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl leading-8 font-extrabold tracking-tight text-white sm:text-4xl">
          Pronto para entender o mercado tech?
        </h2>
        <p class="mt-4 text-xl text-blue-100">
          Junte-se a centenas de profissionais que já usam dados reais para entender o mercado de
          tecnologia e planejar suas carreiras.
        </p>
        <div class="mt-8">
          <router-link
            to="/auth/login"
            class="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-gray-50 transition-all duration-300"
          >
            👉 Comece sua análise agora
          </router-link>
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
