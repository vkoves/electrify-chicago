<script lang="ts">
// Gridsome doesn't have types, so can't import it properly
// eslint-disable-next-line @typescript-eslint/no-var-requires, no-undef
const Pager = require('gridsome').Pager;

import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { LatestDataYear } from '../constants/globals.vue';
import DataSourceFootnote from '../components/DataSourceFootnote.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    DataSourceFootnote,
    NewTabIcon,
    Pager,
  },
  metaInfo() {
    return { title: 'Highest Emissions Intensity Buildings' };
  },
})
export default class HighestEmissionsIntensity extends Vue {
  readonly LatestDataYear: number = LatestDataYear;

  /** Set by Gridsome to results of GraphQL query */
  $page: any;

  pageInput = 0;

  created(): void {
    this.pageInput = this.$page.allBuilding.pageInfo.currentPage;
  }

  jumpToPage(event: Event): void {
    event.preventDefault();

    window.location.href = `/${this.pageInput}`;
  }
}
</script>

<page-query>
  query($page: Int) {
    allBuilding(
      sortBy: "GHGIntensity", perPage: 15, page: $page
    ) @paginate {
      pageInfo {
        hasNextPage
        totalPages
        currentPage
        perPage
        hasPreviousPage
      }
      edges {
        node {
          slugSource
          ID
          DataYear
          PropertyName
          Address
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
        }
      }
    }
  }
</page-query>

<template>
  <DefaultLayout>
    <h1 id="main-content" tabindex="-1">
      All Buildings By Greenhouse Gas Intensity
    </h1>

    <p class="constrained -wide">
      These are the Chicago's benchmarked buildings that reported the highest
      greenhouse gas intensity i.e. emissions per square foot. Large, efficient,
      buildings can perform much better than very inefficient small buildings on
      this metric.
    </p>

    <DataDisclaimer />

    <BuildingsTable :buildings="$page.allBuilding.edges" />

    <div class="pager-cont">
      <div>
        <div class="page-number">
          Page {{ $page.allBuilding.pageInfo.currentPage }} of
          {{ $page.allBuilding.pageInfo.totalPages }}

          (Building #{{
            1 +
            ($page.allBuilding.pageInfo.currentPage - 1) *
              $page.allBuilding.pageInfo.perPage
          }}
          to #{{
            ($page.allBuilding.pageInfo.currentPage - 1) *
              $page.allBuilding.pageInfo.perPage +
            $page.allBuilding.edges.length
          }})
        </div>

        <Pager class="pager" :info="$page.allBuilding.pageInfo" />
      </div>
    </div>

    <DataSourceFootnote />
  </DefaultLayout>
</template>

<style lang="scss">
.pager-cont {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-top: 1rem;
  gap: 1rem;

  .pager {
    margin-top: 0;
  }

  .page-number {
    font-weight: bold;
    font-size: smaller;
    margin-bottom: 0.25rem;
  }
}

@media (max-width: $mobile-max-width) {
  .pager-cont {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
