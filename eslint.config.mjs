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

      semi: ['error', 'always'],
      'arrow-parens': ['error', 'always'],
      'comma-dangle': ['error', 'always-multiline'],

      '@typescript-eslint/explicit-function-return-type': [
        'error',
        {
          allowExpressions: true,
          allowHigherOrderFunctions: true,
          allowTypedFunctionExpressions: true,
        },
      ],

      // We have to use `require` in some cases
      '@typescript-eslint/no-require-imports': 'warn',

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
