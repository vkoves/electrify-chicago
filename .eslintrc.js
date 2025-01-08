module.exports = {
  env: {
    browser: true,
    node: true,
    es2021: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/eslint-recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:vue/recommended",
  ],
  parserOptions: {
    parser: "@typescript-eslint/parser",
    project: "./tsconfig.json",
    extraFileExtensions: [".vue"],
  },
  plugins: ["vue"],
  rules: {
    "max-len": [
      "error",
      {
        code: 100,
        // Fixes errors in HTML files with long links
        ignoreUrls: true,
      },
    ],

    // Disable stylistic rules that interfere with Prettier
    "vue/html-self-closing": "off",
    "vue/singleline-html-element-content-newline": "off",
    "vue/max-attributes-per-line": "off",

    "vue/multi-word-component-names": ["off"],
    // This rule is for Vue3, and Gridsome uses Vue2
    "vue/no-deprecated-filter": ["off"],
    // Don't make <g-link> multiline, it adds spaces
    "vue/multiline-html-element-content-newline": [
      "error",
      {
        ignores: [
          "g-link",
          // Original inline elements from: https://github.com/vuejs/eslint-plugin-vue/blob/master/lib/utils/inline-non-void-elements.json
          "a",
          "abbr",
          "audio",
          "b",
          "bdi",
          "bdo",
          "canvas",
          "cite",
          "code",
          "data",
          "del",
          "dfn",
          "em",
          "i",
          "iframe",
          "ins",
          "kbd",
          "label",
          "map",
          "mark",
          "noscript",
          "object",
          "output",
          "picture",
          "q",
          "ruby",
          "s",
          "samp",
          "small",
          "span",
          "strong",
          "sub",
          "sup",
          "svg",
          "time",
          "u",
          "var",
          "video",
        ],
      },
    ],
    "vue/singleline-html-element-content-newline": [
      "error",
      {
        externalIgnores: ["g-link"],
      },
    ],

    "@typescript-eslint/indent": ["error", 2],
    semi: ["error", "always"],
    "arrow-parens": ["error", "always"],
    "comma-dangle": ["error", "always-multiline"],

    "@typescript-eslint/explicit-function-return-type": [
      "error",
      {
        allowExpressions: true,
        allowHigherOrderFunctions: true,
        allowTypedFunctionExpressions: true,
      },
    ],
  },
  overrides: [
    {
      files: ["*.vue", "declarations/*.ts"],
      rules: {
        indent: "off",
        "@typescript-eslint/indent": "off",
        "@typescript-eslint/no-var-requires": 0,
      },
    },
  ],
};
