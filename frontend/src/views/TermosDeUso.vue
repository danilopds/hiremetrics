<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />

    <!-- Hero Section -->
    <div class="relative bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="text-center">
          <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
            <span class="block">Termos de</span>
            <span class="block text-blue-600">Uso</span>
          </h1>
          <p
            class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl"
          >
            Última atualização: {{ lastUpdated }}
          </p>
        </div>
      </div>
    </div>

    <!-- Terms Content -->
    <div class="py-16 bg-gray-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-lg shadow-lg p-8">
          <div class="prose prose-lg max-w-none">
            <p class="text-gray-600 mb-8">
              Ao acessar e utilizar o HireMetrics, você concorda em cumprir e estar vinculado aos
              seguintes termos e condições de uso.
            </p>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                1. Aceitação dos Termos
              </h2>
              <p class="text-gray-700 mb-4">
                Ao criar uma conta ou utilizar nossos serviços, você confirma que leu, compreendeu e
                concorda com estes Termos de Uso. Se você não concordar com qualquer parte destes
                termos, não deve utilizar nossos serviços.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                2. Descrição do Serviço
              </h2>
              <p class="text-gray-700 mb-4">
                O HireMetrics é uma plataforma de análise de dados do mercado de trabalho que
                oferece:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li>Dashboard com insights sobre tendências de habilidades</li>
                <li>Análise de empresas e canais de publicação</li>
                <li>Relatórios e exportação de dados</li>
                <li>Visualizações geográficas e temporais</li>
                <li>Filtros avançados para análise específica</li>
              </ul>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                4. Uso Aceitável
              </h2>
              <p class="text-gray-700 mb-4">
                Você concorda em utilizar nossos serviços apenas para fins legais e de acordo com
                estes termos. É proibido:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li>Utilizar os serviços para atividades ilegais ou fraudulentas</li>
                <li>Tentar acessar ou modificar sistemas sem autorização</li>
                <li>Compartilhar credenciais de acesso com terceiros</li>
                <li>Utilizar os dados para spam ou marketing não autorizado</li>
                <li>Reproduzir, distribuir ou comercializar nossos dados sem permissão</li>
                <li>Interferir no funcionamento da plataforma</li>
              </ul>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                5. Privacidade e Dados
              </h2>
              <h3 class="text-xl font-semibold text-gray-900 mb-3">
                5.1 Coleta de Dados
              </h3>
              <p class="text-gray-700 mb-4">
                Coletamos e processamos dados pessoais conforme descrito em nossa Política de
                Privacidade. Ao utilizar nossos serviços, você consente com a coleta e uso de seus
                dados.
              </p>

              <h3 class="text-xl font-semibold text-gray-900 mb-3">
                5.2 Propriedade dos Dados
              </h3>
              <p class="text-gray-700 mb-4">
                Os dados do mercado de trabalho apresentados em nossa plataforma são coletados de
                fontes públicas e processados por nossa equipe. Você pode utilizar estes dados para
                fins de análise e tomada de decisão, mas não pode redistribuí-los comercialmente.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                6. Limitações de Responsabilidade
              </h2>
              <p class="text-gray-700 mb-4">
                O HireMetrics é fornecido "como está" e "conforme disponível". Não garantimos que:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li>Os serviços estarão sempre disponíveis ou livres de erros</li>
                <li>Os dados apresentados sejam 100% precisos ou completos</li>
                <li>Os resultados atendam às suas expectativas específicas</li>
                <li>Os serviços sejam compatíveis com todos os dispositivos ou navegadores</li>
              </ul>
              <p class="text-gray-700 mb-4">
                Em nenhuma circunstância seremos responsáveis por danos indiretos, incidentais,
                especiais ou consequenciais decorrentes do uso de nossos serviços.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                7. Propriedade Intelectual
              </h2>
              <p class="text-gray-700 mb-4">
                Todo o conteúdo, funcionalidades e tecnologia da plataforma HireMetrics são
                protegidos por direitos autorais, marcas registradas e outras leis de propriedade
                intelectual. Você não pode copiar, modificar, distribuir ou criar trabalhos
                derivados sem nossa permissão expressa.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                8. Rescisão
              </h2>
              <p class="text-gray-700 mb-4">
                Podemos suspender ou encerrar sua conta a qualquer momento, com ou sem aviso prévio,
                se você violar estes termos. Você também pode excluir sua conta a qualquer momento
                através das configurações de sua conta.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                9. Modificações dos Termos
              </h2>
              <p class="text-gray-700 mb-4">
                Reservamo-nos o direito de modificar estes termos a qualquer momento. As
                modificações entrarão em vigor imediatamente após sua publicação. O uso continuado
                dos serviços após as modificações constitui aceitação dos novos termos.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                10. Lei Aplicável
              </h2>
              <p class="text-gray-700 mb-4">
                Estes termos são regidos pelas leis brasileiras. Qualquer disputa será resolvida nos
                tribunais da comarca de São Paulo, SP, Brasil.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                11. Contato
              </h2>
              <p class="text-gray-700 mb-4">
                Se você tiver dúvidas sobre estes termos, entre em contato conosco através de:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li>E-mail: hiremetrics.contato@gmail.com</li>
                <li>Formulário de contato em nossa plataforma</li>
              </ul>
            </section>

            <div class="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-8">
              <h3 class="text-lg font-semibold text-blue-900 mb-2">
                Importante
              </h3>
              <p class="text-blue-800">
                Ao utilizar o HireMetrics, você confirma que leu e compreendeu estes Termos de Uso e
                concorda em cumpri-los. Se você não concordar com qualquer parte destes termos, não
                deve utilizar nossos serviços.
              </p>
            </div>
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
    name: 'TermosDeUsoPage',
    components: {
      NavBar,
      AppFooter,
    },
    data() {
      return {
        lastUpdated: '19 de Julho de 2025',
      }
    },
    mounted() {
      // Scroll to top when component mounts
      window.scrollTo(0, 0)
    },
  }
</script>
