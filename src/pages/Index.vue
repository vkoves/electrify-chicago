<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import DataSourceFootnote from '../components/DataSourceFootnote.vue';
import BuildingTile from '../components/BuildingTile.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    BuildingTile,
    DataDisclaimer,
    NewTabIcon,
    DataSourceFootnote,
  },
  metaInfo() {
    return { title: 'Home' };
  },
})
export default class Index extends Vue {
  searchQuery = '';

  submitSearch(event?: Event): void {
    event?.preventDefault();

    document.location.href = `/search?q=${this.searchQuery}`;
  }
}
</script>

<page-query>
  query ($page: Int) {
    worstBuildings: allBuilding(
      sortBy: "GHGIntensity", perPage: 10, page: $page
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
          TotalGHGEmissions
          ElectricityUse
          NaturalGasUse
          DistrictSteamUse
        }
      }
    }
    featuredBuildings: allBuilding(
      filter: {
        ID: {
          in: [
            # Marina Towers, Willis, Shedd Aquarium, Monadnock Building, Art Institute of Chicago,
            # Merch Mart, The John Hancock, and Aqua
            "103606", "239096", "166134", "101567", "160196", "103656", "100429", "231019"
          ]
        }
      }
      sortBy: "ID"
      order: DESC
      limit: 10
    ) {
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
          TotalGHGEmissions
          ElectricityUse
          NaturalGasUse
          DistrictSteamUse
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
                <img src="/search.svg" alt="Search" width="32" height="32" />
              </button>
            </div>
          </form>
        </div>
      </div>

      <div class="page-constrained">
        <div class="list-title">
          <h2>
            Chicago&apos;s Most Emissions Intense Buildings
          </h2>
          <g-link class="bold" to="/highest-emissions-intensity"
            >View More</g-link
          >
        </div>
        <p class="list-desc">
          The buildings that reported the highest greenhouse gas emissions per
          square foot
        </p>

        <div class="buildings-scroll-cont">
          <ul class="building-tiles">
            <li
              v-for="building in $page.worstBuildings.edges"
              :key="building.node.ID"
            >
              <BuildingTile
                :building="building.node"
                :path="building.node.path"
              />
            </li>
          </ul>
        </div>

        <div class="list-title"><h2>Featured Chicago Buildings</h2></div>
        <p class="list-desc">
          Check out some of Chicago’s most famous buildings, and learn how they
          use energy
        </p>

        <div class="buildings-scroll-cont">
          <ul class="building-tiles">
            <li
              v-for="building in $page.featuredBuildings.edges"
              :key="building.node.ID"
            >
              <BuildingTile
                :building="building.node"
                :path="building.node.path"
              />
            </li>
          </ul>
        </div>

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

        <DataDisclaimer />

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

          input,
          button {
            outline: none;
          }
        }

        input,
        button {
          height: 100%;
          border: none;
        }

        input {
          padding: 1rem 0 1rem 2rem;
          font-size: 1.25rem;
        }

        button {
          padding: 0 1.5rem 0 1rem;
          background-color: $white;

          &:focus {
            background-color: $blue-dark;

            img {
              filter: invert(1);
            }
          }
        }
      }
    }
  }

  .list-title {
    display: block;
    margin: 2rem 1rem 0 0;

    h2 {
      display: inline;
      margin: 0 0.5rem 0 0;
    }
  }
  .list-desc {
    margin: 0;
  }

  .buildings-scroll-cont {
    position: relative;
    $card-padding: 0.75rem;
    // Grow to account for inner padding
    margin: 1rem (-$card-padding) 2rem (-$card-padding);
    overflow: scroll hidden;

    // Create a fake partial right border to make clear it's scrollable
    &::after {
      content: '';
      width: 60px;
      height: 4px;
      background: gray;
      position: absolute;
      bottom: -4px;
    }

    // Set scrollbar width
    &::-webkit-scrollbar {
      width: 0.75rem;
    }
    // Scrollbar track
    &::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: $brd-rad-medium;
      margin: $card-padding;
    }

    // Scrollbar Handle
    &::-webkit-scrollbar-thumb {
      background: #888;
      border-radius: $brd-rad-medium;
      cursor: pointer;

      // Scroll handle on hover
      &:hover {
        background: #555;
      }
    }

    ul.building-tiles {
      list-style: none;
      display: flex;
      gap: 1rem;
      margin: 0;
      padding: 0;

      li {
        padding: 0.5rem $card-padding 1.5rem $card-padding;
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

  @media (max-width: $mobile-max-width) {
    .skyline-hero {
      min-height: unset;

      // Switch to smaller size but taller skyline crop
      .background {
        background-image: url('/home/skyline-mobile.webp');
      }

      h1 {
        line-height: 1.25;
        font-size: 1.8rem;
      }

      form {
        width: 100%;

        .input-cont {
          height: 3.5rem;

          input {
            font-size: 1rem;
          }
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

    // Undo padding on mobile to make scroll full width
    .buildings-scroll-cont {
      margin-left: -1rem;
      margin-right: -1rem;

      ul.building-tiles {
        li {
          padding-left: 1rem;
          padding-right: 1rem;
        }
      }
    }

    .announcements {
      flex-direction: column;
    }

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
