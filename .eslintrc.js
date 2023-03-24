module.exports = {
  'env': {
    'browser': true,
    'es2021': true,
  },
  'extends': [
    'eslint:recommended',
    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:vue/recommended',
  ],
  'parserOptions': {
    "parser": "@typescript-eslint/parser",
    "project": "./tsconfig.json",
    'extraFileExtensions': [ '.vue' ]
  },
  'plugins': [
    'vue',
  ],
  'rules': {
    'max-len': ['error', {
      'code': 100,
      // Fixes errors in HTML files with long links
      'ignoreUrls': true,
    }],
    'vue/multi-word-component-names': ['off'],
    // This rule is for Vue3, and Gridsome uses Vue2
    'vue/no-deprecated-filter': ['off'],
    '@typescript-eslint/indent': ['error', 2],
  },
  'overrides': [
    {
      'files': ['*.vue'],
      'rules': {
        'indent': 'off',
        '@typescript-eslint/indent': 'off'
      }
    }
  ]
};
