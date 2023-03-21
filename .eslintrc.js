module.exports = {
  'env': {
    'browser': true,
    'es2021': true,
  },
  'extends': [
    'plugin:vue/vue3-essential',
    'google',
  ],
  'overrides': [
  ],
  'parserOptions': {
    'ecmaVersion': 'latest',
    'sourceType': 'module',
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
  },
};
