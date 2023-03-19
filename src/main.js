// This is the main.js file. Import global CSS and scripts here.
// The Client API can be used here. Learn more: gridsome.org/docs/client-api

import DefaultLayout from '~/layouts/Default.vue';

// eslint-disable-next-line require-jsdoc
export default function(Vue, {router, head, isClient}) {
  // Set default layout as a global component
  Vue.component('DefaultLayout', DefaultLayout);

  Vue.config.errorHandler = function(err, vm, info) {
    // handle error
    // `info` is a Vue-specific error info, e.g. which lifecycle hook
    // the error was found in. Only available in 2.2.0+
    console.error('Vue error', error, info, vm);
  };
}
