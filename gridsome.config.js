// This is where project configuration and plugin options are located.
// Learn more: https://gridsome.org/docs/config

// Changes here require a server restart.
// To restart press CTRL + C in terminal and run `gridsome develop`

const path = require('path');

/**
 * A function that loads in all our global SCSS files
 *
 * @param {string} rule A rule?
 */
function addStyleResource(rule) {
  rule.use('style-resource')
      .loader('style-resources-loader')
      .options({
        patterns: [
          path.resolve(__dirname, './src/scss/*.scss'),
        ],
      });
}


module.exports = {
  siteName: 'Electrify Chicago',
  plugins: [
    {
      use: 'gridsome-plugin-typescript',
    },
  ],

  templates: {
    // Register building details path
    Building: [
      {
        path: '/building/:slugSource',
        component: './src/templates/BuildingDetails.vue',
      },
      {
        name: 'building-by-id',
        path: '/building-id/:ID',
        component: './src/templates/BuildingDetails.vue',
      },
    ],
  },

  // Ensure /scss folder is globally available
  chainWebpack(config) {
    // Load variables for all vue-files
    const types = ['vue-modules', 'vue', 'normal-modules', 'normal'];

    // or if you use scss
    types.forEach((type) => {
      addStyleResource(config.module.rule('scss').oneOf(type));
    });
  },
};
