<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import RankText from '~/components/RankText.vue';
import OverallRankEmoji from '~/components/OverallRankEmoji.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import BuildingsMap from '~/components/BuildingsMap.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';
import BuildingImage from '../components/BuildingImage.vue';

/**
 * Note: @Component<any> is required for metaInfo to work with TypeScript
 * This is a known limitation of vue-property-decorator + vue-meta integration
 * See: https://github.com/xerebede/gridsome-starter-typescript/issues/37
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  components: {
    BuildingImage,
    BuildingsMap,
    DataDisclaimer,
    DataSourceFootnote,
    NewTabIcon,
    OverallRankEmoji,
    RankText,
  },
  metaInfo() {
    return {
      ...generatePageMeta(
        'Map',
        'Interactive map of Chicago buildings showing energy performance and emissions data',
      ),
      link: [
        {
          // Leaflet CSS
          href: 'https://unpkg.com/leaflet@1.9.3/dist/leaflet.css',
          rel: 'stylesheet',
        },
      ],
    };
  },
})
export default class MapPage extends Vue {}
</script>

<page-query>
  query {
    allBuilding(sortBy: "GHGIntensity") {
      edges {
        node {
          slugSource
          ID
          DataYear
          PropertyName
          Address
          ZIPCode
          ZIPCode
          Latitude
          Longitude
          path
          PrimaryPropertyType
          GrossFloorArea
          GrossFloorAreaRank
          GrossFloorAreaPercentileRank
          GHGIntensity
          GHGIntensityRank
          GHGIntensityPercentileRank
          TotalGHGEmissions
          TotalGHGEmissionsRank
          TotalGHGEmissionsPercentileRank
          ElectricityUse
          ElectricityUseRank
          ElectricityUsePercentileRank
          NaturalGasUse
          NaturalGasUseRank
          NaturalGasUsePercentileRank
          AvgPercentileLetterGrade
          DataAnomalies
        }
      }
    }
  }
</page-query>

<template>
  <DefaultLayout>
    <div class="map-page">
      <h1 id="main-content" tabindex="-1">Map</h1>

      <DataDisclaimer />

      <BuildingsMap
        :buildings="$page.allBuilding.edges"
        filter-label="highest GHG intensity"
      />

      <!--
        <BuildingsTable :buildings="$page.allBuilding.edges" />
      -->

      <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss"></style>
