module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2021: true,
  },
  extends: [
    'plugin:vue/vue3-recommended',
    'eslint:recommended',
  ],
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: 'module',
  },
  rules: {
    // Vue specific rules (only code quality, no formatting)
    'vue/multi-word-component-names': 'error',
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/no-v-html': 'warn',
    'vue/require-default-prop': 'error',
    'vue/require-explicit-emits': 'error',
    'vue/no-unused-components': 'error',
    // All Vue formatting rules removed - handled by Prettier

    // JavaScript rules (only code quality, no formatting)
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    // All JavaScript formatting rules removed - handled by Prettier

    // Best practices
    'curly': ['error', 'all'],
    'eqeqeq': ['error', 'always'],
    'no-var': 'error',
    'prefer-const': 'error',
    'prefer-template': 'error',
  },
  overrides: [
    {
      files: ['*.vue'],
      rules: {
        // Vue-specific overrides can go here
      }
    }
  ]
}
