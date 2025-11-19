// This is the main.js file. Import global CSS and scripts here.
// The Client API can be used here. Learn more: gridsome.org/docs/client-api

import DefaultLayout from '~/layouts/Default.vue';

export default function (Vue, { head, isClient }) {
  // Set default layout as a global component
  Vue.component('DefaultLayout', DefaultLayout);

  Vue.config.errorHandler = function (err, vm, info) {
    // handle error
    // `info` is a Vue-specific error info, e.g. which lifecycle hook
    // the error was found in. Only available in 2.2.0+
    console.error('Vue error', err, info, vm);
  };

  // Preload the most critical font (Regular) for faster initial render
  head.link.push({
    rel: 'preload',
    href: '/fonts/Roboto-Regular.woff2',
    as: 'font',
    type: 'font/woff2',
    crossorigin: 'anonymous',
  });

  // Add default social images (will be overridden by page-specific meta)
  head.meta.push({
    property: 'og:image',
    content: 'https://electrifychicago.net/social-image.png',
    key: 'og:image',
  });

  head.script.push({
    src: 'https://www.googletagmanager.com/gtag/js?id=G-D4F03H5C02',
    async: true,
  });

  // Google analytics code
  if (isClient) {
    window.dataLayer = window.dataLayer || [];

    function gtag() {
      window.dataLayer.push(arguments);
    }

    gtag('js', new Date());

    gtag('config', 'G-D4F03H5C02');
  }
}
