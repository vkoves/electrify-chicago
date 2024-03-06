<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
  },
  metaInfo() {
    return { title:  'Chicago Failed to Collect Potentially $30 Million in Fines' };
  },
})
export default class MillionsInMissedFine extends Vue {
  readonly NotifLetterUrl = 'https://www.chicago.gov/content/dam/city/progs/env/EnergyBenchmark/sample_notification_letter.pdf';

  /** Buildings from 2018 - 2022 that didn't report */
  readonly NonReportingBuildingsDataUrl = 'https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c/explore/query/SELECT%0A%20%20%60data_year%60%2C%0A%20%20%60id%60%2C%0A%20%20%60property_name%60%2C%0A%20%20%60reporting_status%60%2C%0A%20%20%60address%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60chicago_energy_rating%60%2C%0A%20%20%60exempt_from_chicago_energy_rating%60%2C%0A%20%20%60community_area%60%2C%0A%20%20%60primary_property_type%60%2C%0A%20%20%60gross_floor_area_buildings_sq_ft%60%2C%0A%20%20%60year_built%60%2C%0A%20%20%60of_buildings%60%2C%0A%20%20%60water_use_kgal%60%2C%0A%20%20%60energy_star_score%60%2C%0A%20%20%60electricity_use_kbtu%60%2C%0A%20%20%60natural_gas_use_kbtu%60%2C%0A%20%20%60district_steam_use_kbtu%60%2C%0A%20%20%60district_chilled_water_use_kbtu%60%2C%0A%20%20%60all_other_fuel_use_kbtu%60%2C%0A%20%20%60site_eui_kbtu_sq_ft%60%2C%0A%20%20%60source_eui_kbtu_sq_ft%60%2C%0A%20%20%60weather_normalized_site_eui_kbtu_sq_ft%60%2C%0A%20%20%60weather_normalized_source_eui_kbtu_sq_ft%60%2C%0A%20%20%60total_ghg_emissions_metric_tons_co2e%60%2C%0A%20%20%60ghg_intensity_kg_co2e_sq_ft%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%2C%0A%20%20%60row_id%60%2C%0A%20%20%60%3A%40computed_region_43wa_7qmu%60%2C%0A%20%20%60%3A%40computed_region_vrxf_vc4k%60%2C%0A%20%20%60%3A%40computed_region_6mkv_f3dw%60%2C%0A%20%20%60%3A%40computed_region_bdys_3d7i%60%2C%0A%20%20%60%3A%40computed_region_awaf_s7ux%60%0AWHERE%0A%20%20%28%60data_year%60%20IN%20%28%222019%22%2C%20%222020%22%2C%20%222021%22%2C%20%222022%22%2C%20%222018%22%29%29%0A%20%20AND%20caseless_one_of%28%60reporting_status%60%2C%20%22Not%20Submitted%22%29/page/filter';
}
</script>
<template>
  <DefaultLayout>
    <div class="layout-constrained millions-in-fines">
      <g-link
        to="/blog"
        class="back-link grey-link"
      >
        Back to Blog
      </g-link>

      <h1
        id="main-content"
        tabindex="-1"
      >
        City Of Chicago Failed to Collect $30 Million In Potential Fines from Building Benchmarking
        Ordinance
      </h1>
      <p class="constrained bold">
        Not Enforcing The Benchmarking Ordinance&apos;s Fines From 2018 - 2022 Reduced
        Accountability & Transparency
      </p>

      <p class="constrained">
        Electrify Chicago has analyzed the last five years of city benchmark data, and found
        3,325 instances of building owners not submitting data. Based on the
        <a
          :href="NotifLetterUrl"
          target="_blank"
          rel="noopener"
        >
          latest (2024) official notification letter <NewTabIcon />
        </a> fines for non-compliance could total up to $9,200 per year.
      </p>

      <img
        src="/blog/millions-in-missed-fines/max-fine-quote.webp"
        class="blog-img"
        alt="A selection of text with a title 'Failure to comply is more expensive than you
          think', with details of fines and a highlight saying 'These fines could total $9,200 /
          year'"
      >

      <p class="caption">
        A screenshot of the energy benchmarking notification letter&apos;s section on fines, as of
        Feb. 2024 (<a
          :href="NotifLetterUrl"
          target="_blank"
          rel="noopener"
        >source <NewTabIcon /></a>)
      </p>

      <p>
        With a maximum of $9,200 of fines multiplied by 3,325 instances of non-compliance
        (<a
          :href="NonReportingBuildingsDataUrl"
          target="_blank"
          rel="noopener"
        >source - City of Chicago data portal <NewTabIcon /></a>), that
        means a whopping <strong>$30,590,000 dollars of fines could have been collected</strong>
        by the city&apos;s commissioner of business affairs and consumer protection (who is given
        this responsibility in the
        <a href="https://www.chicago.gov/content/dam/city/progs/env/EnergyBenchmark/BenchmarkingOrdinance11SEP2013.pdf">original ordinance</a>).
      </p>

      <img
        src="/blog/millions-in-missed-fines/non-reporting-buildings-query.webp"
        class="blog-img"
        alt="A screenshot of the city data portal showing a view of buildings filtered by the
          years 2018, 2019, 2020, 2021, and 2022, and a reporting status of 'Not Reporting',
          with the total results returned of 3,325 underlined in red"
      >

      <img
        src="/blog/millions-in-missed-fines/zoomed-non-reporting-count.webp"
        class="blog-img"
        width="400"
        alt="A screenshot of text that reads &apos;Showing rows 1-100 of 3325'"
      >

      <p class="caption">
        The full data portal screenshot, and a zoomed in view of the query result count (<a
          :href="NonReportingBuildingsDataUrl"
          target="_blank"
          rel="noopener"
        >source <NewTabIcon /></a>)
      </p>

      <p>
        A Freedom of Information Act (FOIA) request submitted to the city&apos;s Department of
        Business Affairs and Consumer Protections, which is charged with enforcing the benchmarking
        ordinance, returned no recorded instances of the ordinance being enforced.
      </p>

      <h2>Why This Matters</h2>

      <p>
        Without consequences for non-reporting, building owners who perform poorly can simply opt
        out of reporting their data. Some owners of very large and culturally significant buildings
        have consistently not submitted. As an example, view
        <a
          href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c/explore/query/SELECT%0A%20%20%60data_year%60%2C%0A%20%20%60id%60%2C%0A%20%20%60property_name%60%2C%0A%20%20%60reporting_status%60%2C%0A%20%20%60address%60%2C%0A%20%20%60zip_code%60%2C%0A%20%20%60chicago_energy_rating%60%2C%0A%20%20%60exempt_from_chicago_energy_rating%60%2C%0A%20%20%60community_area%60%2C%0A%20%20%60primary_property_type%60%2C%0A%20%20%60gross_floor_area_buildings_sq_ft%60%2C%0A%20%20%60year_built%60%2C%0A%20%20%60of_buildings%60%2C%0A%20%20%60water_use_kgal%60%2C%0A%20%20%60energy_star_score%60%2C%0A%20%20%60electricity_use_kbtu%60%2C%0A%20%20%60natural_gas_use_kbtu%60%2C%0A%20%20%60district_steam_use_kbtu%60%2C%0A%20%20%60district_chilled_water_use_kbtu%60%2C%0A%20%20%60all_other_fuel_use_kbtu%60%2C%0A%20%20%60site_eui_kbtu_sq_ft%60%2C%0A%20%20%60source_eui_kbtu_sq_ft%60%2C%0A%20%20%60weather_normalized_site_eui_kbtu_sq_ft%60%2C%0A%20%20%60weather_normalized_source_eui_kbtu_sq_ft%60%2C%0A%20%20%60total_ghg_emissions_metric_tons_co2e%60%2C%0A%20%20%60ghg_intensity_kg_co2e_sq_ft%60%2C%0A%20%20%60latitude%60%2C%0A%20%20%60longitude%60%2C%0A%20%20%60location%60%2C%0A%20%20%60row_id%60%2C%0A%20%20%60%3A%40computed_region_43wa_7qmu%60%2C%0A%20%20%60%3A%40computed_region_vrxf_vc4k%60%2C%0A%20%20%60%3A%40computed_region_6mkv_f3dw%60%2C%0A%20%20%60%3A%40computed_region_bdys_3d7i%60%2C%0A%20%20%60%3A%40computed_region_awaf_s7ux%60%0AWHERE%0A%20%20caseless_one_of%28%60reporting_status%60%2C%20%22Not%20Submitted%22%29%0A%20%20AND%20%28%60data_year%60%20IN%20%28%222022%22%29%29%0AORDER%20BY%20%60gross_floor_area_buildings_sq_ft%60%20DESC%20NULL%20LAST/page/filter"
          target="_blank"
          rel="noopener"
        >
          2023&apos;s largest non reporting buildings in the data portal <NewTabIcon />
        </a>. Not having all building owners report means the goals of the ordinance aren't being
        met, and the public loses out on valuable information for buildings that could be emitting
        the most or be the least efficient. The city may also believe that it is on track with its
        climate goals, when there are still large buildings that are emitting but have their
        emissions not reported or not reported accurately, like if a building reports their
        electricity use but not their natural gas use.
      </p>

      <p>
        To put this $30 million in potential fines into context, zin the 2024 budget, $25.3 million
        was suggested to be put towards lead line replacement, meaning these potential fines could
        have fully funded that program in 2024
        (<a href="https://www.chicago.gov/content/dam/city/sites/committeeonthebudget/2024/FY2024/2024-Budget-Overview.pdf"
        target="_blank"
          rel="noopener"
        >source - City of Chicago 2024 Budget Overview <NewTabIcon /></a>).
      </p>

      <h2>Next Steps</h2>

      <p>
        An older version of the energy benchmarking notification (<a
          href="https://web.archive.org/web/20221214211117/https://www.chicago.gov/content/dam/city/progs/env/EnergyBenchmark/2020_Sample_Notification_Letter.pdf"
          target="_blank"
          rel="noopener"
        >source - WayBackMachine <NewTabIcon /></a>)
        did not contain any information about potential fines, and merely by updating the
        notification letter to make sure that building owners are aware of the consequences for not
        reporting, the reporting rate is likely to improve. However, we believe it is crucial the
        city then follow through and fine any owners who choose to ignore repeated requests to
        report their energy use, in keeping with the original ordinance. We also believe that
        larger fines may be necessary to get the owners of very large and inefficient buildings
        to report their emissions, rather than to obscure their pollution from the public.
      </p>

      <p>
        Additionally, we recommend the city consider adding more granular data requirements to the
        data portal to help building emissions data be more clear and helpful. This includes
        ensuring that all electric buildings are clearly reported, distinct from buildings that
        reported electric but not gas use, and considering requesting information about a building's
        HVAC system, since that can be the driving factor in a buildings emissions profile, and a
        building that uses gas only for cooking should be identifiable from a building using gas for
        heating and cooling as well.
      </p>


      <h2>Questions?</h2>

      <p>
        Contact the lead developer on this site, Viktor Köves, by emailing
        <a href="mailto:contact@viktorkoves.com">contact@viktorkoves.com</a>
      </p>
    </div>
  </DefaultLayout>
</template>
<style lang="scss">
.millions-in-fines {
  h1 {
    margin-bottom: 0;
    line-height: 1.25;

    + p { margin: 0.25rem 0 0.5rem 0; }
  }

  a.back-link {
    margin: 1rem 0 0 0;
    display: inline-block;
    font-weight: 600;
  }

  img.blog-img {
    margin-top: 1rem;
    box-shadow: 0.1rem 0.1rem 0.25rem $box-shadow-main;
    border: solid $border-thin $grey-dark;
  }

  p.caption {
    font-size: 0.825rem;
    margin-top: 0.25rem;
    color: $text-light;
  }
}
</style>
