<template>
  <img
    class="new-tab-icon"
    :src="white ? '/new-tab-white.svg' : '/new-tab.svg'"
    alt="(opens in a new tab)"
  />
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

/**
 * A new tab icon for links
 */
@Component
export default class NewTabIcon extends Vue {
  /** Whether to use the white version of the icon (for dark backgrounds) */
  @Prop({ default: false })
  white!: boolean;
}
</script>

<style lang="scss">
.new-tab-icon {
  width: 1em;
  height: 1em;
}
</style>
