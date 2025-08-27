<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

/**
 * Redirect page for backwards compatibility
 *
 * This page was renamed to "All Electric Buildings" on Aug. 27th, 2025.
 * This redirect ensures old bookmarks and links continue to work.
 */
@Component<any>({
  metaInfo() {
    return {
      title: 'Redirecting to All Electric Buildings',
      meta: [{ 'http-equiv': 'refresh', content: '0; URL=/all-electric' }],
      link: [{ rel: 'canonical', href: '/all-electric' }],
    };
  },
})
export default class BiggestGasFreeBuildings extends Vue {}
</script>
