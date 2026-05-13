<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import BuildingsHero from '~/components/BuildingsHero.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import BuildingsMap from '~/components/BuildingsMap.vue';
import { IBuilding, isMostlyElectric } from '../common-functions.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';

interface IBuildingEdge {
  node: IBuilding;
}

/**
 * Mostly Electric Buildings page — buildings whose energy mix is >80% but <100% electricity.
 *
 * We can't filter on a computed percent-electric ratio inside the GraphQL query, so we fetch
 * a broad pool of 2023 buildings sorted by floor area and filter client-side via
 * `isMostlyElectric`. The pool is capped at 1000 buildings, which comfortably covers the
 * largest candidates without slowing the build.
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  components: {
    BuildingsTable,
    BuildingsHero,
    BuildingsMap,
    DataDisclaimer,
    DataSourceFootnote,
    NewTabIcon,
  },
  metaInfo() {
    const description =
      'Chicago buildings that are over 80% electric — close to fully electrified but ' +
      'still burning some fossil gas or relying on district steam. Prime candidates ' +
      'for full electrification.';

    return {
      ...generatePageMeta(
        'mostly-electric',
        'Mostly Electric Buildings',
        description,
      ),
      link: [
        {
          // Leaflet CSS - required for map tiles to render
          href: 'https://unpkg.com/leaflet@1.9.3/dist/leaflet.css',
          rel: 'stylesheet',
        },
      ],
    };
  },
})
export default class MostlyElectric extends Vue {
  get mostlyElectricEdges(): Array<IBuildingEdge> {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const edges: Array<IBuildingEdge> = (this as any).$static.allBuilding.edges;
    return edges.filter((edge) => isMostlyElectric(edge.node));
  }
}
</script>

<!-- If this query is updated, make sure to update PageSocialCard as well -->
<static-query>
  query {
    allBuilding(
      filter: {
        DataYear: { eq: "2023" },
        ElectricityUse: { gt: 0 },
        # Exclude buildings that previously used gas but now report zero, see DataAnomalies in
        # common-functions
        DataAnomalies: { nin: ["gas:zero-with-prev-use"] }
      },
      sortBy: "GrossFloorArea", limit: 1000
    ) {
      edges {
        node {
          slugSource
          ID
          DataYear
          PropertyName
          Address
          ZIPCode
          path
          GrossFloorArea
          GrossFloorAreaRank
          GrossFloorAreaPercentileRank
          Latitude
          Longitude
          PrimaryPropertyType
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
          DistrictSteamUse
          AvgPercentileLetterGrade
          DataAnomalies
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout main-class="layout -full-width">
    <BuildingsHero :buildings="mostlyElectricEdges.map((edge) => edge.node)">
      <h1 id="main-content" tabindex="-1">
        Chicago's {{ mostlyElectricEdges.length }} Mostly Electric Buildings
      </h1>
    </BuildingsHero>

    <div class="page-constrained">
      <p class="constrained -wide">
        These buildings are more than <strong>80% electric</strong> by energy
        mix, but still burn a bit of fossil gas or rely on district steam. They
        are the closest buildings to fully electric in the city — small
        retrofits (heat pumps, electric water heating, kitchen electrification)
        would push them across the line.
      </p>

      <p class="constrained -wide">
        <strong>Note:</strong> Percent electric is calculated from a building's
        reported electricity, natural gas, and district steam use (all in kBtu).
        Buildings that report zero current gas use but used gas in prior years
        are excluded, since the current reading is suspect. Fully all-electric
        buildings live on
        <g-link to="/all-electric">our All Electric page</g-link>.
      </p>

      <DataDisclaimer />

      <BuildingsMap
        :buildings="mostlyElectricEdges"
        filter-label="mostly electric"
      />

      <BuildingsTable
        :buildings="mostlyElectricEdges"
        :show-square-footage="true"
      />

      <DataSourceFootnote />
    </div>
  </DefaultLayout>
</template>

<style lang="scss"></style>
