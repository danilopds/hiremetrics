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
                <span class="block">Vagas de TI</span>
                <span class="block text-blue-600">mapeadas</span>
              </h1>
              <p
                class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0"
              >
                Veja empresas que estão contratando e as vagas tech mais buscadas hoje. Tenha
                visibilidade de vagas por cargo, stack, localidade e mais.
              </p>
              <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div class="rounded-md shadow">
                  <router-link
                    to="/auth/login"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 md:py-4 md:text-lg md:px-10 transition-all duration-300"
                  >
                    👉 Vagas tech em tempo real
                  </router-link>
                </div>
              </div>
            </div>
          </main>
        </div>
        <div class="w-full lg:w-1/2 flex justify-center items-center mt-8 lg:mt-0">
          <img
            class="w-full max-w-xs sm:max-w-sm md:max-w-md lg:max-w-full h-auto object-contain"
            src="@/assets/img/hero.svg"
            alt="Dashboard de vagas de TI"
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
            Vagas tech em tempo real
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            Por que acompanhar as oportunidades em TI?
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Descubra onde estão as vagas reais, quais empresas mais contratam e as oportunidades que
            fazem sentido para sua carreira tech.
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
                    d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0V6a2 2 0 012 2v6a2 2 0 01-2 2H8a2 2 0 01-2-2V8a2 2 0 012-2V6"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Onde estão contratando?
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Descubra quais empresas estão mais ativas no mercado e quais posições estão em
                  alta no momento.
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
                  Vagas para devs e techs
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Acompanhe oportunidades por stack, senioridade e localidade para encontrar a vaga
                  ideal.
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
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Estágios e vagas TI
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Encontre oportunidades desde estágios até posições sênior em diferentes áreas da
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
                    d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Empresas que mais contratam
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Identifique as empresas com maior volume de contratações e as que estão crescendo
                  no mercado tech.
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
            Quem busca programadores?
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Nossa plataforma monitora vagas tech em tempo real, analisa tendências e apresenta as
            melhores oportunidades para sua carreira.
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
                    alt="Monitoramento de vagas"
                    class="w-80 h-80 object-contain"
                  >
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-4">
                  1. Monitoramento de vagas
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Rastreamos milhares de vagas tech diariamente para capturar as oportunidades mais
                  recentes do mercado.
                </p>
              </div>
            </div>

            <!-- Step 2 -->
            <div class="relative">
              <div class="text-center">
                <div class="flex justify-center mb-0">
                  <img
                    src="@/assets/img/howto_2.svg"
                    alt="Análise de oportunidades"
                    class="w-80 h-80 object-contain"
                  >
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-4">
                  2. Análise de oportunidades
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Nossa IA identifica as vagas mais relevantes, empresas que mais contratam e
                  tendências do mercado.
                </p>
              </div>
            </div>

            <!-- Step 3 -->
            <div class="relative">
              <div class="text-center">
                <div class="flex justify-center mb-0">
                  <img
                    src="@/assets/img/howto_3.svg"
                    alt="Oportunidades mapeadas"
                    class="w-80 h-80 object-contain"
                  >
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-4">
                  3. Oportunidades mapeadas
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Use os dados para identificar as melhores oportunidades e empresas para sua
                  carreira tech.
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
            Veja as vagas em tempo real
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Explore nossos dashboards com dados sobre vagas tech, empresas contratando e
            oportunidades por stack e localidade.
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
              title="HireMetrics - Vagas de TI"
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
            Veja como outros profissionais de TI estão usando dados reais para encontrar as melhores
            oportunidades de carreira.
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
                    src="https://i.pravatar.cc/150?img=11"
                    alt="Avatar do Rafael"
                  >
                </div>
                <div class="ml-4">
                  <h4 class="text-lg font-medium text-gray-900">
                    Rafael M.
                  </h4>
                  <p class="text-sm text-gray-500">
                    Desenvolvedor Full Stack
                  </p>
                </div>
              </div>
              <p class="text-gray-600 italic">
                "Com o HireMetrics, consegui identificar quais empresas estavam contratando mais e
                quais stacks estavam em alta. Isso me ajudou a focar nos estudos certos e conseguir
                uma vaga melhor."
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
                    src="https://i.pravatar.cc/150?img=14"
                    alt="Avatar da Juliana"
                  >
                </div>
                <div class="ml-4">
                  <h4 class="text-lg font-medium text-gray-900">
                    Juliano S.
                  </h4>
                  <p class="text-sm text-gray-500">
                    Estagiário de TI
                  </p>
                </div>
              </div>
              <p class="text-gray-600 italic">
                "Os dados sobre vagas me ajudaram a entender onde estão as melhores oportunidades
                para estágio. Consegui encontrar uma vaga em uma empresa que realmente estava
                crescendo."
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
            Respostas para as dúvidas mais comuns sobre nossa plataforma de vagas de TI.
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
                  <span class="font-medium text-gray-900">Como os dados ajudam a encontrar vagas?</span>
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
                  Nossos dados mostram quais empresas estão contratando mais, quais stacks estão em
                  alta e as oportunidades por localidade, permitindo identificar as melhores vagas
                  para sua carreira.
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
                  às vagas mais recentes do mercado de TI.
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
                  personalizados sobre vagas de TI.
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
                  Use os dados para identificar quais empresas estão contratando mais, quais stacks
                  estão em alta e onde estão as melhores oportunidades para sua carreira tech.
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
          Pronto para encontrar as melhores vagas?
        </h2>
        <p class="mt-4 text-xl text-blue-100">
          Junte-se a centenas de profissionais de TI que já usam dados reais para identificar as
          melhores oportunidades de carreira no mercado tech.
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
