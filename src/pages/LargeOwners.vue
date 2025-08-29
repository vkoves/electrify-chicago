<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsTable from '~/components/BuildingsTable.vue';
import DataDisclaimer from '~/components/DataDisclaimer.vue';
import NewTabIcon from '~/components/NewTabIcon.vue';
import { BuildingOwners } from '../constants/buildings-custom-info.constant.vue';
import generatePageSocialMeta from '../constants/page-social-meta';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingsTable,
    DataDisclaimer,
    NewTabIcon,
  },
  metaInfo() {
    return generatePageSocialMeta(
      'Large Owners',
      'Explore buildings by major property owners in Chicago - ' +
      'universities, the city, and other large organizations',
    );
  },
})
export default class LargeOwners extends Vue {
  BuildingOwners = BuildingOwners;
}
</script>

<static-query>
  query {
    allBuilding(sortBy: "GHGIntensity", limit: 50) {
      edges {
        node {
          slugSource
          ID
          DataYear
          PropertyName
          Address
          ZIPCode
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
          AvgPercentileLetterGrade
          DataAnomalies
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout>
    <div class="building-owners">
      <h1 id="main-content" tabindex="-1">Large Building Owners</h1>

      <p class="constrained -wide">
        These building owners own multiple properties in the City of Chicago
        benchmarked Buildings data set, making them responsible for a larger
        total of emissions than individual building owners.
      </p>

      <p class="constrained -wide">
        <strong>Note:</strong> All building owners are manually tagged through
        public data, like university building directories, and are thus may be
        an incomplete list.
      </p>

      <p class="constrained -wide">
        Notice a problem or have a suggestion?
        <a
          ref="noopener"
          href="https://github.com/vkoves/electrify-chicago/issues/new"
          target="_blank"
          >File an issue on our GitHub! <NewTabIcon />
        </a>
      </p>

      <!-- Loop through building owners -->
      <ul class="owners-list">
        <li v-for="owner in BuildingOwners" :key="owner.key">
          <g-link :to="'/owner/' + owner.key" class="owner-tile">
            <img :src="owner.logoLarge" :alt="owner.name" />
          </g-link>
        </li>
      </ul>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.building-owners {
  ul.owners-list {
    display: flex;
    flex-wrap: wrap;
    gap: 2rem;
    max-width: 60rem;
    padding: 0;
    margin-top: 2rem;
    list-style: none;

    a {
      text-decoration: none;
    }

    .owner-tile {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      background-color: $white;
      padding: 1.5rem 2rem;
      border-radius: 0.5rem;
      height: 100%;
      box-sizing: border-box;
      border: solid $border-thin $grey;
      border-bottom: solid 1.5rem $chicago-blue;
      transition: background-color 0.2s;

      img {
        display: block;
        width: 24rem;
      }

      .name {
        display: none;
        margin-top: 1rem;
        color: $text-main;
        font-size: 1.25rem;
        text-decoration: none;
      }

      &:hover,
      &:focus {
        background-color: $grey-light;
      }
    }
  }
}
</style>
