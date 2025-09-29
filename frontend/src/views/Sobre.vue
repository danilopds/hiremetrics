<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />

    <!-- Hero Section -->
    <div class="relative bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="text-center">
          <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
            <span class="block">Sobre o</span>
            <span class="block text-blue-600">HireMetrics</span>
          </h1>
          <p
            class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl"
          >
            Conheça nossa missão, visão e a equipe por trás da plataforma que está democratizando o
            acesso a dados do mercado de trabalho no Brasil.
          </p>
        </div>
      </div>
    </div>

    <!-- Nossa Missão Section -->
    <div class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Nossa Missão
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            Democratizar o acesso a dados do mercado
          </p>
        </div>
        <div class="mt-10 max-w-3xl mx-auto">
          <div class="bg-gray-50 rounded-lg p-8">
            <p class="text-lg text-gray-700 leading-relaxed">
              Nossa missão é democratizar o acesso a dados do mercado de trabalho, fornecendo
              insights valiosos para que profissionais, empresas e pesquisadores possam tomar
              decisões mais informadas e estratégicas sobre suas carreiras e negócios.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Nossa História Section -->
    <div class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Nossa História
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            Como tudo começou
          </p>
        </div>
        <div class="mt-10 max-w-4xl mx-auto">
          <div class="bg-white rounded-lg p-8 shadow-sm">
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
              O HireMetrics nasceu da necessidade de ter dados reais e atualizados sobre o mercado
              de trabalho brasileiro. Identificamos que muitos profissionais e empresas tomavam
              decisões baseadas em intuição ou dados desatualizados.
            </p>
            <p class="text-lg text-gray-700 leading-relaxed">
              Com anos de experiência em tecnologia e análise de dados, desenvolvemos uma plataforma
              que coleta, processa e apresenta informações do mercado de forma clara e acionável
              para todos os tipos de usuários.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Nossos Valores Section -->
    <div class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Nossos Valores
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            O que nos move
          </p>
        </div>
        <div class="mt-10">
          <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10">
            <div class="relative">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white"
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
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Transparência
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Acreditamos que dados transparentes e acessíveis são fundamentais para um mercado
                  de trabalho mais justo, eficiente e informado.
                </p>
              </div>
            </div>

            <div class="relative">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white"
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
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Inovação
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Buscamos constantemente novas formas de coletar, processar e apresentar dados para
                  oferecer insights cada vez mais valiosos e acessíveis.
                </p>
              </div>
            </div>

            <div class="relative">
              <div
                class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white"
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
                    d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                  />
                </svg>
              </div>
              <div class="ml-16">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  Colaboração
                </h3>
                <p class="mt-2 text-base text-gray-500">
                  Trabalhamos em parceria com profissionais, empresas e pesquisadores para entender
                  suas necessidades e desenvolver soluções cada vez melhores.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Equipe Section -->
    <div class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-blue-600 font-semibold tracking-wide uppercase">
            Nossa Equipe
          </h2>
          <p
            class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl"
          >
            Conheça quem faz acontecer
          </p>
        </div>
        <div class="mt-10">
          <div class="grid grid-cols-1 md:grid-cols-1 gap-8">
            <!-- Team Member 1 - Your Position -->
            <div class="bg-white rounded-lg shadow-lg p-6 text-center">
              <div class="w-48 h-48 mx-auto mb-4 bg-gray-200 flex items-center justify-center">
                <!-- Placeholder for your photo -->
                <img
                  src="@/assets/img/danilo_silva.jpeg"
                  alt="Danilo Silva"
                  class="w-48 h-48 rounded-lg"
                >
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">
                Danilo Silva
              </h3>
              <p class="text-blue-600 font-medium mb-3">
                CEO & Fundador
              </p>
              <p class="text-gray-600 text-sm leading-relaxed">
                Especialista em tecnologia e análise de dados com mais de 10 anos de experiência no
                mercado brasileiro. Apaixonado por transformar dados em insights acionáveis para
                profissionais e empresas nos mais diversos setores.
              </p>
            </div>

            <!-- Team Member 2 - Placeholder -->
            <!--<div class="bg-white rounded-lg shadow-lg p-6 text-center">
              <div class="w-32 h-32 mx-auto mb-4 rounded-full bg-gray-200 flex items-center justify-center">
                <svg class="w-16 h-16 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">Nome do Colaborador</h3>
              <p class="text-blue-600 font-medium mb-3">Cargo</p>
              <p class="text-gray-600 text-sm leading-relaxed">
                Descrição do perfil profissional, experiência e contribuições
                para o projeto HireMetrics.
              </p>
            </div>-->

            <!-- Team Member 3 - Placeholder -->
            <!--<div class="bg-white rounded-lg shadow-lg p-6 text-center">
              <div class="w-32 h-32 mx-auto mb-4 rounded-full bg-gray-200 flex items-center justify-center">
                <svg class="w-16 h-16 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-900 mb-2">Nome do Colaborador</h3>
              <p class="text-blue-600 font-medium mb-3">Cargo</p>
              <p class="text-gray-600 text-sm leading-relaxed">
                Descrição do perfil profissional, experiência e contribuições
                para o projeto HireMetrics.
              </p>
            </div>-->
          </div>
        </div>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="py-16 bg-blue-600">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 class="text-3xl font-extrabold text-white sm:text-4xl">
          <span class="block">Pronto para começar?</span>
          <span class="block">Junte-se a nós hoje mesmo</span>
        </h2>
        <p class="mt-4 text-lg leading-6 text-blue-200">
          Descubra como o HireMetrics pode transformar sua compreensão do mercado de trabalho.
        </p>
        <div class="mt-8 flex justify-center">
          <div class="rounded-md shadow">
            <router-link
              to="/auth/login"
              class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-blue-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10 transition-all duration-300"
            >
              Começar agora
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script>
  import NavBar from '@/components/NavBar.vue'
  import AppFooter from '@/components/Footer.vue'

  export default {
    name: 'SobrePage',
    components: {
      NavBar,
      AppFooter,
    },
    mounted() {
      // Scroll to top when component mounts
      window.scrollTo(0, 0)
    },
  }
</script>
