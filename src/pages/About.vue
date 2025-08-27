<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';
import { LatestDataYear } from '../constants/globals.vue';
import EmissionsBreakdownGraph from '../components/EmissionsBreakdownGraph.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    EmissionsBreakdownGraph,
    NewTabIcon,
  },
  metaInfo() {
    return { title: 'About Us' };
  },
})
export default class About extends Vue {
  readonly LatestDataYear: number = LatestDataYear;
}
</script>
<template>
  <DefaultLayout>
    <div class="about-page layout-constrained">
      <h1 id="main-content" tabindex="-1">About Us</h1>

      <div class="flex-row">
        <div>
          <p class="constrained">
            Electrify Chicago is an independent open-source project looking to
            shed light onto one of the biggest sources of Chicago's CO<sub
              >2</sub
            >
            emissions - buildings. By providing more information about some of
            the city's largest and most polluting buildings, we hope to
            encourage these buildings to electrify, particularly by mobilizing
            people related to the building - whether that be students and
            faculty for a college building or employees and patients at a
            hospital.
          </p>

          <h2>Why Buildings?</h2>

          <p class="constrained -wide main-paragraph">
            <!-- TODO: Move to consolidated sources object-->
            According to the
            <a
              ref="noopener"
              href="https://www.chicago.gov/city/en/sites/climate-action-plan/home.html"
              target="_blank"
            >
              2022 Chicago Climate Action Plan<NewTabIcon /> </a
            >, <strong>69% of Chicago's emissions come from buildings</strong>,
            making building emissions our biggest challenge and
            <em>our biggest opportunity</em> as a city to tackle climate change.
            At Electrify Chicago, we showcase building performance using
            publicly available data supplemented by community-submitted
            photographs and building owners.
          </p>

          <p class="our-why large-text">
            <strong>Our Goal?</strong> Get Large Buildings to
            <em>Electrify</em> And Use Less Energy
          </p>
        </div>

        <EmissionsBreakdownGraph class="-desktop" />
      </div>

      <h2>But Why Electrify?</h2>

      <div class="power-chart">
        <img
          alt="Pie chart showing that 67% of Illinois power is Carbon-Free, with 58% from Nuclear
            and 9% from Wind. Then 18% comes from Coal and 14% from Fossil Gas."
          class="-shadowed"
          src="/il-power-chart.webp"
          width="300"
        />

        <p class="footnote -img">
          Source:
          <a
            href="https://decarbmystate.com/illinois#power"
            target="_blank"
            rel="noopener"
          >
            Illinois Power | Decarb My State <NewTabIcon />
          </a>
        </p>
      </div>

      <p class="constrained">
        In simple terms, because we can scalably produce electricity without
        emitting CO<sub>2</sub> and exacerbating the climate crisis. In fact,
        <em>this decade</em> (the 2020s) is an especially crucial one for
        tackling climate change (<a
          href="https://www.nytimes.com/2023/03/20/climate/global-warming-ipcc-earth.html"
        >
          &ldquo;World Has Less Than a Decade to Stop Catastrophic
          Warming&hellip;&rdquo; | The New York Times </a
        >), and shifting away from burning fossil fuels to using electricity
        <strong>today</strong> is a crucial step in that journey.
      </p>

      <p class="constrained">
        Even better,
        <strong>
          Illinois' grid in particular is already powered mostly by carbon-free
          energy
        </strong>
        and is improving every year!
      </p>

      <p>
        This means that buildings using only electricity cause less emissions
        every year as the power grid is moved to carbon-free sources, without
        any further changes to the building. On the other hand, fossil-fuel
        powered appliances will continue to emit as long as they are used.
      </p>

      <h2>Updates</h2>

      <p>
        See our
        <g-link to="/release-notes" class="bold">Release Notes</g-link> page to
        see data updates and other changes, or check activity on our
        <a href="https://github.com/vkoves/electrify-chicago">
          GitHub repository </a
        >!
      </p>

      <h2>Other Interesting Pages</h2>

      <p>
        There are a lot of interesting ways to view this data, here are a few
        pages that aren't featured in our header but could be useful:
      </p>

      <ul class="other-pages">
        <li>
          <g-link to="/citywide-stats"> City Wide Statistics </g-link>
        </li>
        <li>
          <g-link to="/top-gas-users"> Top Gas Users </g-link>
        </li>
        <li>
          <g-link to="/top-electricity-users"> Top Electricity Users </g-link>
        </li>
        <li>
          <g-link to="/all-electric"> All Electric Buildings </g-link>
        </li>
        <li>
          <g-link to="/retrofit-chicago-participants">
            Retrofit Chicago Case Studies
          </g-link>
        </li>
      </ul>

      <h2>Authors</h2>

      <p>
        Electrify Chicago is a volunteer project led by
        <a href="https://viktorkoves.com/"> Viktor Köves </a>, a Chicago native
        and climate developer part of the volunteer team behind
        <a href="https://decarbmystate.com/"> DecarbMyState </a>.
      </p>

      <p>
        Electrify Chicago is an independent project and not affiliated with or
        endorsed by the City of Chicago.
      </p>

      <h2>Sources</h2>

      <p>
        Data is primarily sourced from the publicly available
        <a
          href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
          target="_blank"
          rel="noopener"
        >
          Chicago Energy Benchmarking Data <NewTabIcon /> </a
        >, which is data collected and published under the
        <a
          href="https://www.chicago.gov/city/en/progs/env/building-energy-benchmarking---transparency.html"
        >
          Chicago Energy Benchmarking Ordinance <NewTabIcon /> </a
        >. This site shows data for the year {{ LatestDataYear }} (the latest
        available of March 2023) and filtered down to buildings with total
        emissions > 1,000 metric tons CO<sub>2</sub>
        equivalent.
      </p>

      <h2>Contact Us</h2>

      <p>
        Found a bug or have a feature request?
        <a href="https://github.com/vkoves/electrify-chicago/issues/new">
          File an issue on the Electrify Chicago GitHub </a
        >!
      </p>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.about-page {
  h2 {
    margin-top: 1.75rem;
  }

  .flex-row {
    display: flex;
    gap: 2rem;

    .emissions-breakdown {
      flex-shrink: 0;

      img {
        margin: 0;
      }
    }
  }

  p.our-why {
    display: inline-block;
    line-height: 1.25;
    border-bottom: solid 0.5rem $chicago-blue;
  }

  .power-chart {
    float: right;
    margin-left: 2rem;
    margin-bottom: 3rem;

    img {
      margin: 0;
    }
  }

  .other-pages {
    li {
      font-size: 1.25rem;
      margin-top: 1rem;
      font-weight: bold;
    }
  }

  @media (max-width: $mobile-max-width) {
    .emissions-breakdown {
      display: none;
    }

    .power-chart {
      float: none;
      margin-left: 0;
    }
  }
}
</style>
