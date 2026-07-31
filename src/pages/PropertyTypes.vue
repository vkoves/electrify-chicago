<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingsHero from '~/components/BuildingsHero.vue';
import DataSourceFootnote from '~/components/DataSourceFootnote.vue';
import {
  PropertyTypeStats,
  pluralizePropertyType,
} from '../common-functions.vue';
import {
  getPropertyTypeEmoji,
  slugifyPropertyType,
} from '../constants/property-type-helpers.vue';
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
  /**
   * All property types that have a generated page, sorted by building count
   * descending, since the largest categories are the most useful to browse
   */
  readonly propertyTypes: Array<IPropertyTypeSummary> =
    PropertyTypesConstant.propertyTypes
      .map((propertyType: string) => {
        const stats = (
          BuildingStatsByPropertyType as Record<string, PropertyTypeStats>
        )[propertyType] as PropertyTypeStats | undefined;

        const totalGHGEmissions = stats?.TotalGHGEmissions?.total ?? 0;

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
        };
      })
      .sort((a, b) => b.buildingCount - a.buildingCount);

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
              <span class="type-name">
                <span class="type-emoji" aria-hidden="true">{{
                  type.emoji
                }}</span>
                {{ type.propertyTypePlural }}
              </span>

              <span class="type-stats">
                <span class="type-stat">
                  <strong>{{ formatCount(type.buildingCount) }}</strong>
                  building{{ type.buildingCount === 1 ? '' : 's' }}
                </span>

                <span v-if="type.totalGHGEmissions" class="type-stat">
                  <strong>{{ formatEmissions(type.totalGHGEmissions) }}</strong>
                  metric tons CO<sub>2</sub>e
                  <span class="type-percent">
                    ({{ formatPercent(type.percentOfTotalEmissions) }} of
                    citywide)
                  </span>
                </span>

                <span v-if="type.avgGHGIntensity" class="type-stat">
                  <strong>{{ formatIntensity(type.avgGHGIntensity) }}</strong>
                  avg. kg CO<sub>2</sub>e/sqft
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
      gap: 0.5rem;
      height: 100%;
      box-sizing: border-box;
      padding: 1rem;
      background-color: $white;
      border: solid $border-thin $grey;
      border-bottom: solid $border-thick $chicago-blue;
      border-radius: $brd-rad-medium;
      text-decoration: none;
      color: $text-main;

      &:hover,
      &:focus {
        background-color: $grey-light;
      }

      .type-name {
        font-size: 1.125rem;
        font-weight: 600;

        .type-emoji {
          display: inline-block;
          margin-right: 0.25rem;
        }
      }

      .type-stats {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
        font-size: 0.875rem;
        color: $text-mid-light;

        .type-percent {
          font-size: 0.8rem;
        }
      }
    }
  }
}
</style>
