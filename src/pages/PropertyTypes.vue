<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsHero from '~/components/BuildingsHero.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import {
  IBuilding,
  IBuildingNode,
  PropertyTypeStats,
  pluralizePropertyType,
} from '../common-functions.vue';
import {
  getPropertyTypeEmoji,
  slugifyPropertyType,
} from '../constants/property-type-helpers.vue';
import { getBuildingImage } from '../constants/building-images.constant.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';
import BuildingStatsByPropertyType from '../data/dist/building-statistics-by-property-type.json';
import PropertyTypesConstant from '../data/dist/property-types.json';

/** A property type with the summary stats we show in the index list */
interface IPropertyTypeSummary {
  propertyType: string;
  propertyTypePlural: string;
  slug: string;
  emoji: string;
  buildingCount: number;
  totalGHGEmissions: number;
  /** Share of all benchmarked emissions, as a percent (e.g. 12.4) */
  percentOfTotalEmissions: number;
  avgGHGIntensity: number;
  /** The largest building of this type that has a photo, if any */
  featuredBuilding: IBuilding | null;
  /** The photo URL for featuredBuilding, or null if no building has one */
  imgUrl: string | null;
}

/**
 * Total emissions across every property type we have stats for, used as the
 * denominator for each type's share. This covers a few types that don't have
 * their own page, so the listed shares add up to slightly under 100%.
 */
const CitywideTotalEmissions = Object.values(
  BuildingStatsByPropertyType as Record<string, PropertyTypeStats>,
).reduce((sum, stats) => sum + (stats.TotalGHGEmissions?.total ?? 0), 0);

/**
 * Note: @Component<any> is required for metaInfo to work with TypeScript
 * This is a known limitation of vue-property-decorator + vue-meta integration
 * See: https://github.com/xerebede/gridsome-starter-typescript/issues/37
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  components: {
    BuildingsHero,
    DataSourceFootnote,
  },
  metaInfo() {
    return generatePageMeta(
      'Buildings By Property Type',
      'Browse Chicago buildings by property type - see how offices, schools, ' +
        'hospitals, and more compare on energy use and emissions.',
    );
  },
})
export default class PropertyTypes extends Vue {
  /** Set by Gridsome to results of the static GraphQL query */
  readonly $static!: { allBuilding: { edges: Array<IBuildingNode> } };

  /**
   * All property types that have a generated page, sorted by building count
   * descending, since the largest categories are the most useful to browse
   */
  propertyTypes: Array<IPropertyTypeSummary> = [];

  created(): void {
    const featuredBuildings = this.buildFeaturedBuildingMap();

    this.propertyTypes = PropertyTypesConstant.propertyTypes
      .map((propertyType: string) => {
        const stats = (
          BuildingStatsByPropertyType as Record<string, PropertyTypeStats>
        )[propertyType] as PropertyTypeStats | undefined;

        const totalGHGEmissions = stats?.TotalGHGEmissions?.total ?? 0;
        const featuredBuilding = featuredBuildings[propertyType] ?? null;

        return {
          propertyType,
          propertyTypePlural: pluralizePropertyType(propertyType),
          slug: slugifyPropertyType(propertyType),
          emoji: getPropertyTypeEmoji(propertyType),
          buildingCount: stats?.GHGIntensity?.count ?? 0,
          totalGHGEmissions,
          percentOfTotalEmissions: CitywideTotalEmissions
            ? (totalGHGEmissions / CitywideTotalEmissions) * 100
            : 0,
          avgGHGIntensity: stats?.GHGIntensity?.mean ?? 0,
          featuredBuilding,
          imgUrl: featuredBuilding
            ? (getBuildingImage(featuredBuilding)?.imgUrl ?? null)
            : null,
        };
      })
      .sort((a, b) => b.buildingCount - a.buildingCount);
  }

  /**
   * Finds the largest building with a photo for each property type. The query
   * is sorted by GrossFloorArea descending, so the first building we see with
   * an image for a given type is the largest one we can show.
   */
  private buildFeaturedBuildingMap(): Record<string, IBuilding> {
    const featuredBuildings: Record<string, IBuilding> = {};

    this.$static.allBuilding.edges.forEach(({ node }) => {
      const propertyType = node.PrimaryPropertyType;

      if (
        !propertyType ||
        featuredBuildings[propertyType] ||
        !getBuildingImage(node)
      ) {
        return;
      }

      featuredBuildings[propertyType] = node;
    });

    return featuredBuildings;
  }

  get totalBuildingCount(): number {
    return this.propertyTypes.reduce(
      (sum, type) => sum + type.buildingCount,
      0,
    );
  }

  formatCount(count: number): string {
    return count.toLocaleString();
  }

  formatEmissions(emissions: number): string {
    return Math.round(emissions).toLocaleString();
  }

  /** Show a floor of "<0.1%" so tiny categories don't all read as 0% */
  formatPercent(percent: number): string {
    if (percent > 0 && percent < 0.1) {
      return '<0.1%';
    }

    return `${percent.toFixed(1)}%`;
  }

  formatIntensity(intensity: number): string {
    return intensity.toFixed(1);
  }
}
</script>

<!--
  Sorted by GrossFloorArea descending so we can pick the largest building with
  a photo for each property type in a single pass
-->
<static-query>
  query {
    allBuilding(sortBy: "GrossFloorArea") {
      edges {
        node {
          ID
          PropertyName
          Address
          PrimaryPropertyType
          GrossFloorArea
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout main-class="layout -full-width">
    <div class="property-types-page">
      <BuildingsHero :buildings="[]" :short="true">
        <div class="layout-constrained">
          <h1 id="main-content" tabindex="-1">Buildings By Property Type</h1>

          <p class="subtitle">
            Curious how Chicago's offices, schools, or hospitals stack up? Pick
            a property type below to see its buildings, energy use, and
            emissions.
          </p>
        </div>
      </BuildingsHero>

      <div class="layout-constrained -padded">
        <p>
          {{ formatCount(propertyTypes.length) }} property types covering
          {{ formatCount(totalBuildingCount) }} benchmarked buildings. Emissions
          shares are of <em>all benchmarked emissions citywide</em>. See our
          <g-link to="/citywide-stats">Citywide Stats</g-link> page for how the
          city as a whole is trending.
        </p>

        <ul class="property-type-list">
          <li v-for="type in propertyTypes" :key="type.slug">
            <g-link
              class="property-type-tile"
              :to="`/property-type/${type.slug}`"
            >
              <span class="type-image-cont">
                <img
                  v-if="type.imgUrl"
                  :src="type.imgUrl"
                  :alt="`${
                    type.featuredBuilding.PropertyName ||
                    type.featuredBuilding.Address
                  }, the largest ${type.propertyType} we have a photo of`"
                  loading="lazy"
                />
                <img
                  v-else
                  src="/home/skyline-mobile.webp"
                  alt=""
                  loading="lazy"
                />

                <span class="type-name">
                  <span class="type-emoji" aria-hidden="true">{{
                    type.emoji
                  }}</span>

                  <span class="type-name-text">
                    <span class="type-title">
                      {{ type.propertyTypePlural }}
                    </span>

                    <span class="type-building-count">
                      <strong>{{ formatCount(type.buildingCount) }}</strong>
                      building{{ type.buildingCount === 1 ? '' : 's' }}
                    </span>
                  </span>
                </span>
              </span>

              <span class="type-stats">
                <span v-if="type.totalGHGEmissions" class="type-stat">
                  <span class="type-stat-title">Total Emissions</span>

                  <strong>{{ formatEmissions(type.totalGHGEmissions) }}</strong>
                  metric tons CO<sub>2</sub>e

                  <span class="type-percent">
                    {{ formatPercent(type.percentOfTotalEmissions) }} of total
                    benchmarked
                  </span>
                </span>

                <span v-if="type.avgGHGIntensity" class="type-stat">
                  <span class="type-stat-title">
                    Average Emissions Intensity
                  </span>

                  <strong>{{ formatIntensity(type.avgGHGIntensity) }}</strong>
                  kg CO<sub>2</sub>e/sqft
                </span>
              </span>
            </g-link>
          </li>
        </ul>

        <DataSourceFootnote />
      </div>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.property-types-page {
  h1 {
    margin-bottom: 0;
  }

  .subtitle {
    margin-top: 0;
  }

  ul.property-type-list {
    display: grid;
    gap: 1rem;
    grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr));
    list-style: none;
    margin: 1.5rem 0;
    padding: 0;

    .property-type-tile {
      display: flex;
      flex-direction: column;
      height: 100%;
      box-sizing: border-box;
      overflow: hidden;
      background-color: $white;
      border: solid $border-thin $grey;
      border-bottom: solid $border-thick $chicago-blue;
      border-radius: $brd-rad-medium;
      text-decoration: none;
      color: $text-main;

      &:hover,
      &:focus {
        background-color: $grey-light;

        .type-image-cont img {
          transform: scale(1.05);
        }
      }

      // The building photo, with the property type name overlaid on top of it
      .type-image-cont {
        display: block;
        position: relative;
        overflow: hidden;
        height: 13rem;
        background-color: $off-black;

        img {
          width: 100%;
          height: 100%;
          object-fit: cover;
          // Darkened so the white title stays readable over any photo
          filter: brightness(65%);
          transition: transform 0.2s ease;
        }
      }

      .type-name {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 0.5rem;
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 2rem 0.75rem 0.5rem;
        background: linear-gradient(
          to top,
          rgba(0, 0, 0, 0.8) 0%,
          transparent 100%
        );
        color: $white;
        text-shadow: 0 0.125rem 0.25rem $box-shadow-main;

        .type-emoji {
          flex-shrink: 0;
          font-size: 1.75rem;
          line-height: 1;
        }

        .type-name-text {
          display: flex;
          flex-direction: column;
          gap: 0.125rem;
        }

        .type-title {
          font-size: 1.125rem;
          font-weight: 600;
        }

        .type-building-count {
          font-size: 0.875rem;
        }
      }

      .type-stats {
        display: flex;
        flex-direction: column;
        flex: 1;
        gap: 0.75rem;
        padding: 0.75rem;
        font-size: 0.875rem;
        color: $text-mid-light;

        .type-stat-title {
          display: block;
          font-size: 0.75rem;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.03em;
          color: $off-black;
        }

        .type-percent {
          display: block;
          font-size: 0.875rem;
          font-weight: 600;
        }
      }
    }
  }
}
</style>
