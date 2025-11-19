<template>
  <div><!-- No content, redirect page --></div>
</template>

<script>
export default {
  metaInfo() {
    return {
      title: `Redirecting to ${this.$page.building.path}`,
      meta: [
        {
          'http-equiv': 'refresh',
          content: `0; URL=${this.$page.building.path}`,
        },
      ],
      link: [
        {
          rel: 'canonical',
          href: `https://electrifychicago.net/${this.$page.building.path}`,
        },
      ],
    };
  },
};
</script>

<page-query>
query ($id: ID!) {
  building(id: $id) {
    path
  }
}
</page-query>
