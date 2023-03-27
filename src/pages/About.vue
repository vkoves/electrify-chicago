<template>
  <DefaultLayout>
    <div class="layout-constrained">
      <h1
        id="main-content"
        tabindex="-1"
      >
        About Us
      </h1>

      <p class="constrained">
        Electrify Chicago is an independent open-source project looking to shed light onto one of
        the biggest sources of Chicago's CO<sub>2</sub> emissions - buildings. By providing more
        information about some of the city's largest and most polluting buildings, we hope t
        encourage these buildings to electrify, particularly by mobilizing people related to the
        building - whether that be students and faculty for a college building or employees and
        patients at a hospital.
      </p>

      <p class="large-text bold">
        Our Goal: Get Large Buildings to <u>Electrify</u> & Use Less Energy
      </p>

      <h2>But Why Electrify?</h2>

      <p class="constrained">
        In simple terms, because we can scalably produce electricity without emitting CO<sub>2</sub>
        and exacerbating the climate crisis. In fact, <em>this decade</em> (the 2020s) is an
        especially crucial one for tackling climate change
        (<a href="https://www.nytimes.com/2023/03/20/climate/global-warming-ipcc-earth.html">&ldquo;World Has Less Than a Decade to Stop Catastrophic Warming&hellip;&rdquo;
          | The New York Times</a>), and shifting away from burning fossil fuels to using
        electricity
        <strong>today</strong> is a crucial step in that journey.
      </p>

      <p class="constrained">
        Even better, <strong>Illinois' grid in particular is already powered mostly by carbon-free
          energy</strong> and is improving every year!
      </p>

      <img
        alt="Pie chart showing that 67% of Illinois power is Carbon-Free, with 58% from Nuclear and
        9% from Wind. Then 18% comes from Coal and 14% from Natural Gas."
        class="-shadowed"
        src="/il-power-chart.png"
        width="500"
      >

      <p class="footnote -img">
        Source:
        <a
          href="https://decarbmystate.com/illinois#power"
          target="_blank"
          rel="noopener noreferrer"
        >
          Illinois Power | Decarb My State <NewTabIcon />
        </a>
      </p>

      <p>
        This means that buildings using only electricity cause less emissions every year as the
        power grid is moved to carbon-free sources, without any further changes to the building.
        On the other hand, fossil-fuel powered appliances will continue to emit as long as they are
        used.
      </p>

      <h2>Authors</h2>

      <p>
        Electrify Chicago is a project by <a href="https://viktorkoves.com/">Viktor Köves</a>, a
        Chicago native and climate developer who was part of the volunteer team behind
        <a href="https://decarbmystate.com/">DecarbMyState</a> and built
        <a href="https://carbonchallenge.io/">The Carbon Challenge</a>.
      </p>

      <p>
        Electrify Chicago is an independent project and not affiliated with or endorsed by the City
        of Chicago.
      </p>

      <h2>Sources</h2>

      <p>
        Data is primarily sourced from the publicly available
        <a
          href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c"
          target="_blank"
          rel="noopener noreferrer"
        >
          Chicago Energy Benchmarking Data <NewTabIcon />
        </a>, which is data collected and published under the
        <a href="https://www.chicago.gov/city/en/progs/env/building-energy-benchmarking---transparency.html">
          Chicago Energy Benchmarking Ordinance <NewTabIcon />
        </a>. This site shows data for the year 2020 (the latest available of March 2023) and
        filtered down to buildings with total emissions > 1,000 metric tons.
      </p>

      <h2>Contact Us</h2>

      <p>
        Found a bug or have a feature request?
        <a href="https://github.com/vkoves/electrify-chicago/issues/new">
          File an issue on the Electrify Chicago GitHub</a>!
      </p>
    </div>
  </DefaultLayout>
</template>

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
    return { title:  'About Us' };
  },
})
export default class About extends Vue {
}
</script>
