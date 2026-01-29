import eslint from '@eslint/js';
import globals from 'globals';
import js from '@eslint/js';
import pluginVue from 'eslint-plugin-vue';
import tseslint from 'typescript-eslint';
import vue from 'eslint-plugin-vue';

export default tseslint.config(
  {
    // config with just ignores is the replacement for `.eslintignore`
    ignores: ['src/.temp/**', '**/.venv/**', '**/dist/**', '**/htmlcov/**', '*.js'],
  },
  js.configs.recommended,
  eslint.configs.recommended,
  tseslint.configs.recommended,
  ...pluginVue.configs['flat/recommended'],
  {
    files: ['src/**/*.ts', 'src/**/*.vue'],

    plugins: {
      vue,
    },

    languageOptions: {
      globals: {
        ...globals.browser,
        require: 'readonly',
      },

      ecmaVersion: 5,
      sourceType: 'script',

      parserOptions: {
        parser: '@typescript-eslint/parser',
        project: './tsconfig.json',
        extraFileExtensions: ['.vue'],
      },
    },

    rules: {
      'max-len': [
        'error',
        {
          code: 100,
          ignoreUrls: true,
          // Ignore long lines that are just 'src="longurl"'
          ignorePattern: '^\\s*src=".*"$',
        },
      ],

      'vue/html-closing-bracket-newline': 'off',
      'vue/html-self-closing': 'off',
      'vue/max-attributes-per-line': 'off',
      'vue/singleline-html-element-content-newline': 'off',
      'vue/html-indent': 'off',
      'vue/multi-word-component-names': ['off'],
      'vue/no-deprecated-filter': ['off'],
      // This is a FE only site, so there's no real HTML security risks
      'vue/no-v-html': 'off',

      'vue/multiline-html-element-content-newline': [
        'error',
        {
          ignores: [
            'g-link',
            'a',
            'abbr',
            'audio',
            'b',
            'bdi',
            'bdo',
            'canvas',
            'cite',
            'code',
            'data',
            'del',
            'dfn',
            'em',
            'i',
            'iframe',
            'ins',
            'kbd',
            'label',
            'map',
            'mark',
            'noscript',
            'object',
            'output',
            'picture',
            'q',
            'ruby',
            's',
            'samp',
            'small',
            'span',
            'strong',
            'sub',
            'sup',
            'svg',
            'time',
            'u',
            'var',
            'video',
          ],
        },
      ],
      'arrow-parens': ['error', 'always'],
      'comma-dangle': ['error', 'always-multiline'],

      // Prevent console.log usage (but allow console.error)
      'no-console': ['error', { allow: ['error'] }],
      'semi': ['error', 'always'],


      '@typescript-eslint/explicit-function-return-type': [
        'error',
        {
          allowExpressions: true,
          allowHigherOrderFunctions: true,
          allowTypedFunctionExpressions: true,
        },
      ],

      // Disallow require() imports - use ES6 imports instead
      // Note: require() is sometimes needed for SSR compatibility (Gridsome) or webpack asset bundling
      // Use eslint-disable comments with clear explanations when require() is necessary
      '@typescript-eslint/no-require-imports': 'error',

      '@typescript-eslint/no-explicit-any': 'warn',
    },
  },
  {
    files: ['**/*.vue', 'declarations/*.ts'],

    rules: {
      indent: 'off',
      '@typescript-eslint/indent': 'off',
      '@typescript-eslint/no-var-requires': 0,
    },
  },
);
