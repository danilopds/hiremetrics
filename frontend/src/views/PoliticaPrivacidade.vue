<template>
  <div class="min-h-screen bg-gray-50">
    <NavBar />

    <!-- Hero Section -->
    <div class="relative bg-white overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div class="text-center">
          <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
            <span class="block">Política de</span>
            <span class="block text-blue-600">Privacidade</span>
          </h1>
          <p
            class="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl"
          >
            Última atualização: {{ lastUpdated }}
          </p>
        </div>
      </div>
    </div>

    <!-- Privacy Content -->
    <div class="py-16 bg-gray-50">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="bg-white rounded-lg shadow-lg p-8">
          <div class="prose prose-lg max-w-none">
            <p class="text-gray-600 mb-8">
              Esta Política de Privacidade descreve como o HireMetrics coleta, utiliza e protege
              suas informações pessoais. Estamos comprometidos em proteger sua privacidade e
              garantir a segurança de seus dados.
            </p>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                1. Informações que Coletamos
              </h2>

              <h3 class="text-xl font-semibold text-gray-900 mb-3">
                1.1 Informações Pessoais
              </h3>
              <p class="text-gray-700 mb-4">
                Coletamos as seguintes informações pessoais quando você se registra ou utiliza
                nossos serviços:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li>Nome completo</li>
                <li>Endereço de e-mail</li>
                <li>Histórico de uso da plataforma</li>
                <li>Preferências e configurações</li>
              </ul>

              <h3 class="text-xl font-semibold text-gray-900 mb-3">
                1.2 Informações Técnicas
              </h3>
              <p class="text-gray-700 mb-4">
                Coletamos automaticamente informações técnicas sobre seu dispositivo e uso:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li>Endereço IP</li>
                <li>Tipo de navegador e sistema operacional</li>
                <li>Páginas visitadas e tempo de permanência</li>
                <li>Cookies e tecnologias similares</li>
                <li>Dados de localização (quando permitido)</li>
              </ul>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                2. Como Utilizamos suas Informações
              </h2>
              <p class="text-gray-700 mb-4">
                Utilizamos suas informações pessoais para:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li>Fornecer e manter nossos serviços</li>
                <li>Gerenciar conta e acesso à plataforma</li>
                <li>Enviar comunicações importantes sobre sua conta</li>
                <li>Melhorar e personalizar sua experiência</li>
                <li>Fornecer suporte ao cliente</li>
                <li>Detectar e prevenir fraudes</li>
                <li>Cumprir obrigações legais</li>
              </ul>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                3. Compartilhamento de Informações
              </h2>
              <p class="text-gray-700 mb-4">
                Não vendemos, alugamos ou compartilhamos suas informações pessoais com terceiros,
                exceto:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">                
                <li>
                  <strong>Provedores de Serviços:</strong> Empresas que nos ajudam a operar a
                  plataforma
                </li>
                <li>
                  <strong>Obrigações Legais:</strong> Quando exigido por lei ou ordem judicial
                </li>
                <li>
                  <strong>Proteção de Direitos:</strong> Para proteger nossos direitos e segurança
                </li>
              </ul>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                4. Cookies e Tecnologias Similares
              </h2>
              <p class="text-gray-700 mb-4">
                Utilizamos cookies e tecnologias similares para:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li>Manter você logado em sua conta</li>
                <li>Lembrar suas preferências</li>
                <li>Analisar o uso da plataforma</li>
                <li>Melhorar a performance e segurança</li>
              </ul>
              <p class="text-gray-700 mb-4">
                Você pode controlar o uso de cookies através das configurações do seu navegador.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                5. Segurança dos Dados
              </h2>
              <p class="text-gray-700 mb-4">
                Implementamos medidas de segurança técnicas e organizacionais para proteger suas
                informações:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li>Criptografia de dados em trânsito e em repouso</li>
                <li>Controle de acesso rigoroso</li>
                <li>Monitoramento contínuo de segurança</li>
                <li>Backups regulares e seguros</li>
                <li>Treinamento da equipe em práticas de segurança</li>
              </ul>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                6. Seus Direitos (LGPD)
              </h2>
              <p class="text-gray-700 mb-4">
                Conforme a Lei Geral de Proteção de Dados (LGPD), você tem os seguintes direitos:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li><strong>Acesso:</strong> Solicitar informações sobre seus dados pessoais</li>
                <li><strong>Correção:</strong> Solicitar correção de dados incorretos</li>
                <li><strong>Exclusão:</strong> Solicitar a exclusão de seus dados</li>
                <li><strong>Portabilidade:</strong> Receber seus dados em formato estruturado</li>
                <li><strong>Revogação:</strong> Revogar consentimento a qualquer momento</li>
                <li><strong>Oposição:</strong> Opor-se ao processamento de seus dados</li>
              </ul>
              <p class="text-gray-700 mb-4">
                Para exercer seus direitos, entre em contato conosco através do e-mail:
                hiremetrics.contato@gmail.com
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                7. Retenção de Dados
              </h2>
              <p class="text-gray-700 mb-4">
                Mantemos suas informações pessoais apenas pelo tempo necessário para:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li>Fornecer nossos serviços</li>
                <li>Cumprir obrigações legais</li>
                <li>Resolver disputas</li>
                <li>Fazer cumprir nossos acordos</li>
              </ul>
              <p class="text-gray-700 mb-4">
                Quando você cancela sua conta, excluímos ou anonimizamos seus dados pessoais, exceto
                quando necessário para fins legais ou de segurança.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                8. Transferências Internacionais
              </h2>
              <p class="text-gray-700 mb-4">
                Seus dados podem ser processados em países diferentes do Brasil. Quando isso
                ocorrer, garantimos que as transferências sejam feitas de acordo com as leis de
                proteção de dados aplicáveis e que medidas de segurança adequadas sejam
                implementadas.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                9. Menores de Idade
              </h2>
              <p class="text-gray-700 mb-4">
                Nossos serviços não são destinados a menores de 18 anos. Não coletamos
                intencionalmente informações pessoais de menores de idade. Se você é pai ou
                responsável e acredita que seu filho nos forneceu informações pessoais, entre em
                contato conosco imediatamente.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                10. Alterações nesta Política
              </h2>
              <p class="text-gray-700 mb-4">
                Podemos atualizar esta Política de Privacidade periodicamente. Quando fizermos
                alterações significativas, notificaremos você por e-mail ou através de um aviso em
                nossa plataforma. O uso continuado de nossos serviços após as alterações constitui
                aceitação da nova política.
              </p>
            </section>

            <section class="mb-8">
              <h2 class="text-2xl font-bold text-gray-900 mb-4">
                11. Contato
              </h2>
              <p class="text-gray-700 mb-4">
                Se você tiver dúvidas sobre esta Política de Privacidade ou sobre como tratamos seus
                dados, entre em contato conosco:
              </p>
              <ul class="list-disc pl-6 text-gray-700 mb-4">
                <li><strong>E-mail:</strong> hiremetrics.contato@gmail.com</li>
                <li><strong>Formulário de contato:</strong> Disponível em nossa plataforma</li>
                <li><strong>Endereço:</strong> São Paulo, SP, Brasil</li>
              </ul>
            </section>

            <div class="bg-green-50 border border-green-200 rounded-lg p-6 mt-8">
              <h3 class="text-lg font-semibold text-green-900 mb-2">
                Compromisso com a Privacidade
              </h3>
              <p class="text-green-800">
                Sua privacidade é importante para nós. Estamos comprometidos em proteger suas
                informações pessoais e em ser transparentes sobre como as utilizamos. Se você tiver
                qualquer dúvida ou preocupação, não hesite em entrar em contato.
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
    name: 'PoliticaPrivacidadePage',
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
