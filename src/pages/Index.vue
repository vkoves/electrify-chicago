<script lang="ts">
// Gridsome doesn't have types, so can't import it properly
// eslint-disable-next-line @typescript-eslint/no-var-requires, no-undef
const Pager = require('gridsome').Pager;

import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import DataSourceFootnote from '../components/DataSourceFootnote.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    NewTabIcon,
    DataSourceFootnote,
    Pager,
  },
  metaInfo() {
    return { title: 'Home' };
  },
})
export default class Index extends Vue {
  /** Set by Gridsome to results of GraphQL query */
  $page: any;

  pageInput = 0;

  searchQuery = '';

  created(): void {
    this.pageInput = this.$page.allBuilding.pageInfo.currentPage;
  }

  jumpToPage(event: Event): void {
    event.preventDefault();

    window.location.href = `/${this.pageInput}`;
  }

  submitSearch(event?: Event): void {
    event?.preventDefault();

    document.location.href = `/search?q=${this.searchQuery}`;
  }
}
</script>

<page-query>
  query ($page: Int) {
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
  <DefaultLayout main-class="layout -full-width">
    <div class="homepage">
      <div class="skyline-hero">
        <div class="background"></div>
        <div class="page-constrained">
          <h1 id="main-content" tabindex="-1">
            Find Out How Much Chicago Buildings Pollute
          </h1>

          <form class="search-form">
            <div class="input-cont">
              <input
                id="search"
                v-model="searchQuery"
                type="text"
                name="search"
                aria-label="Search benchmarked buildings"
                placeholder="Search property name/address"
              />
              <button type="submit" @click="submitSearch">
                <img src="/search.svg" alt="" width="32" height="32" />
              </button>
            </div>
          </form>
        </div>
      </div>

      <div class="page-constrained">
        <h2>Our Research</h2>

        <div class="row">
          <div class="announcements">
            <div class="announce-panel -orange">
              <h3>
                <div class="regular-text-size">New Article</div>
                📰 $30 Million In Missed Fines
              </h3>

              <p>
                The City Of Chicago failed to collect $30 million in potential
                fines from the building benchmarking ordinance, reducing
                transparency and accountability.
              </p>

              <p>
                <a href="/blog/millions-in-missed-fines" class="bold"
                  >Read Our Full Blog Post On Millions in Missed Fines</a
                >.
              </p>
            </div>
          </div>
        </div>

        <h2>Chicago Buildings by Greenhouse Gas Intensity</h2>

        <DataDisclaimer />

        <BuildingsTable :buildings="$page.allBuilding.edges" />

        <div class="pager-cont">
          <div>
            <div class="page-number">
              Page {{ $page.allBuilding.pageInfo.currentPage }} of
              {{ $page.allBuilding.pageInfo.totalPages }}

              (Building #{ 1 + ($page.allBuilding.pageInfo.currentPage - 1) *
              $page.allBuilding.pageInfo.perPage }} to #{{
                ($page.allBuilding.pageInfo.currentPage - 1) *
                  $page.allBuilding.pageInfo.perPage +
                $page.allBuilding.edges.length
              }})
            </div>

            <Pager class="pager" :info="$page.allBuilding.pageInfo" />
          </div>

          <form class="page-form search-form">
            <label for="page-num">Go to Page</label>

            <div class="input-cont">
              <input id="page-num" v-model="pageInput" type="number" />
              <button type="submit" @click="jumpToPage">Jump</button>
            </div>
          </form>
        </div>

        <DataSourceFootnote />
      </div>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.homepage {
  .skyline-hero {
    display: flex;
    align-items: center;
    text-align: center;
    min-height: 28rem;
    padding: 5rem 1rem;
    color: $white;
    position: relative;

    // Apply the background on a separate element so we can apply filters to it
    .background {
      position: absolute;
      width: 100%;
      height: 100%;
      top: 0;
      left: 0;
      z-index: -1;
      background-image: url('/home/skyline-1920.webp');
      background-size: cover;
      background-repeat: no-repeat;
      background-position: center;
      filter: brightness(60%);
    }

    h1 {
      display: inline-block;
      font-size: 2.5rem;
      margin-top: 0;
      margin-bottom: 2rem;
    }

    form {
      margin: 0 auto 2rem auto;
      width: 80%;
      max-width: 50rem; // 800px

      .input-cont {
        height: 4rem;
        border-radius: 3rem;
        background: $white;

        &:focus-within {
          outline: solid $border-v-thick $blue-dark;

          input, button { outline: none; }
        }

        input, button { height: 100%; border: none; }

        input {
          padding: 1rem 0 1rem 2rem;
          font-size: 1.25rem;
        }

        button {
          padding: 0 1.5rem 0 1rem;
          background-color: $white;

          &:focus {
            background-color: $blue-dark;

            img { filter: invert(1); }
          }
        }
      }
    }
  }

  .row {
    display: flex;
    justify-content: space-between;
    gap: 2rem;

    p.main-paragraph {
      font-size: 1.125rem;
    }
  }

  .announcements {
    display: flex;
    gap: 1rem;
    align-items: flex-start;

    > * {
      flex-basis: 100%;
    }
  }

  .page-form {
    input,
    button {
      height: 2rem;
    }

    label {
      display: block;
      margin-bottom: 0.25rem;
      font-size: 0.825rem;
      font-weight: bold;
    }

    input {
      width: 3.5rem;
    }
  }

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
    .skyline-hero {
      // Switch to smaller size but taller skyline crop
      .background { background-image: url('/home/skyline-mobile.webp'); }

      h1 {
        line-height: 1.25;
        font-size: 1.8rem;
      }

      form {
        width: 100%;

        .input-cont {
          height: 3.5rem;

          input { font-size: 1rem; }
          button {
            padding-right: 1rem;

            img {
              width: 28px;
              height: 28px;
            }
          }
        }
      }
    }

    .announcements { flex-direction: column; }

    .row {
      display: block;

      p.main-paragraph {
        font-size: 0.825rem;
      }
    }

    .pager-cont {
      flex-direction: column;
      align-items: flex-start;
    }
  }
}
</style>
