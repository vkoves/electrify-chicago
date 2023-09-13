<script lang="ts">
// Gridsome doesn't have types, so can't import it properly
// eslint-disable-next-line @typescript-eslint/no-var-requires, no-undef
const Pager = require('gridsome').Pager;

import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
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
    return { title:  'Home' };
  },
})
export default class BiggestBuildings extends Vue {
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
  query ($page: Int) {
    allBuilding(
      filter: { DataYear: { eq: "2021" } }, sortBy: "GHGIntensity", perPage: 15, page: $page
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
      <h1
        id="main-content"
        tabindex="-1"
      >
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

      <div class="pager-cont">
        <div>
          <div class="page-number">
            Page {{ $page.allBuilding.pageInfo.currentPage }} of
            {{ $page.allBuilding.pageInfo.totalPages }}

            (Building
            #{{ 1 + ($page.allBuilding.pageInfo.currentPage - 1)
              * $page.allBuilding.pageInfo.perPage }}
            to #{{ ($page.allBuilding.pageInfo.currentPage - 1)
              * $page.allBuilding.pageInfo.perPage + $page.allBuilding.edges.length }})
          </div>

          <Pager
            class="pager"
            :info="$page.allBuilding.pageInfo"
          />
        </div>

        <form class="page-form search-form">
          <label for="page-num">Go to Page</label>

          <div class="input-cont">
            <input
              id="page-num"
              v-model="pageInput"
              type="number"
            >
            <button
              type="submit"
              @click="jumpToPage"
            >
              Jump
            </button>
          </div>
        </form>
      </div>

      <DataSourceFootnote />
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

  .page-form {
    input, button { height: 2rem; }

    label {
      display: block;
      margin-bottom: 0.25rem;
      font-size: 0.825rem;
      font-weight: bold;
    }

    input { width: 3.5rem;}
  }

  .pager-cont {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-top: 1rem;
    gap: 1rem;

    .pager { margin-top: 0; }

    .page-number {
      font-weight: bold;
      font-size: smaller;
      margin-bottom: 0.25rem;
    }
  }

  @media (max-width: $mobile-max-width) {
    .row { display: block; }

    .emissions-breakdown {
      width: 100%;
      text-align: center;

      &.-mobile { display: block; }
      &.-desktop { display: none; }
    }

    .pager-cont {
      flex-direction: column;
      align-items: flex-start;
    }
  }
}
</style>
