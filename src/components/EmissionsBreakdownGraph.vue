<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import NewTabIcon from "~/components/NewTabIcon.vue";

@Component<any>({
  components: {
    NewTabIcon,
  },
})
export default class EmissionsBreakdownGraph extends Vue {}
</script>

<template>
  <div class="emissions-breakdown">
    <img
      src="/chicago-2017-ghg-emissions.png"
      width="167"
      height="400"
      class="-shadowed"
      alt="2017 GHG Emissions -
        31M metric tons CO2 equivalent
        69% buildings
        24% transportation
        7% waste"
    />

    <p class="footnote">
      <a
        ref="noopener"
        href="https://www.chicago.gov/city/en/sites/climate-action-plan/home.html"
        target="_blank"
      >
        Chicago 2022 CAP <NewTabIcon />
      </a>
    </p>
  </div>
</template>

<style lang="scss"></style>
