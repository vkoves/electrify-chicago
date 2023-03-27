<script lang="ts">
// Gridsome doesn't have types, so can't import it properly
// eslint-disable-next-line @typescript-eslint/no-var-requires, no-undef
const Pager = require('gridsome').Pager;

import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import EmissionsBreakdownGraph from '~/components/EmissionsBreakdownGraph.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    EmissionsBreakdownGraph,
    BuildingsTable,
    DataDisclaimer,
    NewTabIcon,
    Pager,
  },
  metaInfo() {
    return { title:  'Biggest Buildings' };
  },
})
export default class BiggestBuildings extends Vue {
}
</script>

<page-query>
  query ($page: Int) {
    allBuilding(sortBy: "GHGIntensity", perPage: 15, page: $page) @paginate {
      pageInfo {
        totalPages
        currentPage
      }
      edges {
        node {
          slugSource
          PropertyName
          Address
          path
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
        }
      }
    }
  }
</page-query>

<template>
  <DefaultLayout>
    <div class="homepage">
      <h1 id="main-content" tabindex="-1">
        Electrify Chicago
      </h1>

      <div class="row">
        <div>
          <p class="constrained -wide">
            <!-- TODO: Move to consolidated sources object-->
            According to the
            <a
              ref="noopener noreferrer"
              href="https://www.chicago.gov/city/en/sites/climate-action-plan/home.html"
              target="_blank"
            >
              2022 Chicago Climate Action Plan<NewTabIcon />
            </a>,
            a whopping <strong>69% of Chicago's emissions come from buildings</strong>, making it
            our biggest challenge and <em>our biggest opportunity</em> as a city to tackle
            change. At Electrify Chicago we want to showcase some of the best and worst performing
            buildings in the city using publicly available data and manual annotations to add
            building photographs and label multi-building owners like universities.
          </p>

          <EmissionsBreakdownGraph class="-mobile" />

          <p class="constrained -wide">
            You can start by looking at Chicago's buildings with the highest greenhouse gas
            intensity - this means that they use the most energy when adjusted per unit of square
            foot, so big buildings could actually perform much better than very inefficient small
            buildings on this metric.
          </p>

          <h2>Chicago Buildings by Greenhouse Gas Intensity</h2>

          <DataDisclaimer />
        </div>

        <EmissionsBreakdownGraph class="-desktop" />
      </div>

      <BuildingsTable :buildings="$page.allBuilding.edges" />

      <Pager
        class="pager"
        :info="$page.allBuilding.pageInfo"
      />

      <p class="footnote">
        Data Source:
        <a
          href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
          target="_blank"
          rel="noopener noreferrer"
        >
          Chicago Energy Benchmarking Data <NewTabIcon />
        </a>
      </p>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.homepage {
  .row {
    display: flex;
    justify-content: space-between;
    gap: 2rem;

    p.constrained { font-size: 1.25rem; }
  }

  .emissions-breakdown {
    text-align: right;
    margin-bottom: 1rem;
    flex-shrink: 0;

    &.-mobile { display: none; }
    > img { height: 25rem; }
    p { margin: 0; }
  }

  @media (max-width: $mobile-max-width) {
    .row { display: block; }

    .emissions-breakdown {
      width: 100%;
      text-align: center;

      &.-mobile { display: block; }
      &.-desktop { display: none; }
    }
  }
}
</style>
