<template>
  <footer class="bg-black border-t border-gray-800">
    <div class="max-w-7xl mx-auto py-12 px-4 overflow-hidden sm:px-6 lg:px-8">
      <!-- Social Links -->
      <div class="flex justify-center space-x-6 mb-8">
        <a
          href="https://github.com/danilopds/hiremetrics"
          target="_blank"
          rel="noopener noreferrer"
          class="text-gray-400 hover:text-white transition-colors duration-300"
          title="GitHub"
        >
          <span class="sr-only">GitHub</span>
          <svg
            class="h-6 w-6"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              fill-rule="evenodd"
              d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
              clip-rule="evenodd"
            />
          </svg>
        </a>
        <a
          href="https://discord.gg/rr7TkzzR"
          target="_blank"
          rel="noopener noreferrer"
          class="text-gray-400 hover:text-indigo-400 transition-colors duration-300"
          title="Discord"
        >
          <span class="sr-only">Discord</span>
          <svg
            class="h-6 w-6"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M20.317 4.37a19.791 19.791 0 00-4.885-1.515.074.074 0 00-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 00-5.487 0 12.64 12.64 0 00-.617-1.25.077.077 0 00-.079-.037A19.736 19.736 0 003.677 4.37a.07.07 0 00-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 00.031.057 19.9 19.9 0 005.993 3.03.078.078 0 00.084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 00-.041-.106 13.107 13.107 0 01-1.872-.892.077.077 0 01-.008-.128 10.2 10.2 0 00.372-.292.074.074 0 01.077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 01.078.01c.12.098.246.198.373.292a.077.077 0 01-.006.127 12.299 12.299 0 01-1.873.892.077.077 0 00-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 00.084.028 19.839 19.839 0 006.002-3.03.077.077 0 00.032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 00-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z" />
          </svg>
        </a>
      </div>

      <!-- Navigation Links -->
      <nav
        class="-mx-5 -my-2 flex flex-wrap justify-center"
        aria-label="Footer"
      >
        <div class="px-5 py-2">
          <router-link
            to="/"
            class="text-base text-gray-400 hover:text-cyan-400 transition-colors duration-300 font-mono"
          >
            Home
          </router-link>
        </div>
        <div class="px-5 py-2">
          <router-link
            to="/sobre"
            class="text-base text-gray-400 hover:text-cyan-400 transition-colors duration-300 font-mono"
          >
            About
          </router-link>
        </div>
        <div class="px-5 py-2">
          <router-link
            to="/contato"
            class="text-base text-gray-400 hover:text-cyan-400 transition-colors duration-300 font-mono"
          >
            Contact
          </router-link>
        </div>
        <div class="px-5 py-2">
          <router-link
            to="/termos-de-uso"
            class="text-base text-gray-400 hover:text-cyan-400 transition-colors duration-300 font-mono"
          >
            Terms
          </router-link>
        </div>
        <div class="px-5 py-2">
          <router-link
            to="/politica-privacidade"
            class="text-base text-gray-400 hover:text-cyan-400 transition-colors duration-300 font-mono"
          >
            Privacy
          </router-link>
        </div>
      </nav>

      <!-- Copyright and Open Source Badge -->
      <div class="mt-8 text-center">
        <div class="flex items-center justify-center space-x-2 mb-2">
          <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-800 text-gray-300 border border-gray-700 font-mono">
            <svg
              class="w-3 h-3 mr-1 text-green-400"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                clip-rule="evenodd"
              />
            </svg>
            Open Source • MIT License
          </span>
        </div>
        <p class="text-base text-gray-500 font-mono">
          <span class="text-cyan-500">&copy;</span> 2025 HireMetrics. Built by devs, for devs.
        </p>
      </div>
    </div>
  </footer>
</template>

<script>
  export default {
    name: 'AppFooter',
  }
</script>
