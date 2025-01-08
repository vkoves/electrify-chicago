<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import NewTabIcon from "~/components/NewTabIcon.vue";

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
  },
  metaInfo() {
    return { title: "Take Action" };
  },
})
export default class TakeActionTips extends Vue {}
</script>

<template>
  <DefaultLayout>
    <div class="take-act-page layout-constrained">
      <h1 id="main-content" and tabindex="-1">Take Action</h1>
      <p class="subtitle">How Can Our Buildings Improve?</p>

      <p class="constrained">
        Practically every building has room to improve with energy efficiency
        upgrades like insulation, switching to ENERGY STAR rated appliances, and
        more, but for any buildings with large fossil gas use, we recommend one
        thing: <strong>electrify!</strong>
      </p>

      <p class="constrained">
        In other words,
        <strong>
          buildings should look to move all on-site uses of fossil fuels
          (including space heating, water heating, and cooking) to electrically
          powered systems
        </strong>
        like industrial grade heat pumps, heat pump water heaters, and induction
        stoves. With Illinois' current electric supply, just using the same
        amount of energy from electricity, rather than fossil gas (aka methane)
        will dramatically reduce greenhouse gas emissions. This is because
        Illinois' grid in 2020 was already 67% carbon-free (see
        <a
          href="https://decarbmystate.com/illinois#power"
          target="_blank"
          rel="noopener"
        >
          Illinois - Power | DecarbMyState <NewTabIcon /> </a
        >). This has already been done across the country with a variety of
        buildings, large and small, like the
        <a
          href="https://www.youtube.com/watch?v=J4aTcU6Fzoc"
          target="_blank"
          rel="noopener"
        >
          Hotel Marcel
          <NewTabIcon /> </a
        >.
      </p>

      <p class="constrained">
        You can help make this a reality by talking to building owners and
        letting them know that a building's emissions are important to you, and
        that you want to see their building become fully electric and stop
        emitting greenhouse gases. Particularly for buildings you have a
        financial stake in (like your university, work, condo building, or
        apartment building) your voice
        <em>in concert with your fellow building users</em> can have a huge
        impact.
      </p>

      <h3>Additional Resources</h3>

      <p>
        See some additional resources on improving energy efficiency and
        understanding this data:
      </p>

      <ul>
        <li>
          <a
            href="https://www.chicago.gov/city/en/depts/mayor/supp_info/chicago-energy-benchmarking/Chicago_Energy_Benchmarking_Beyond_Benchmarking.html"
            target="_blank"
            rel="noopener"
          >
            Chicago Energy Benchmarking: Taking Action to Improve Energy
            Efficiency | City of Chicago <NewTabIcon />
          </a>
        </li>

        <li>
          <a
            href="https://www.chicagobuilding.gov/content/dam/city/progs/env/EnergyBenchmark/2018_Chicago_Energy_Benchmarking_Results_By_Sector.pdf"
            target="_blank"
            rel="noopener"
          >
            Chicago Average EUIs and ENERGY STAR scores by property type [PDF]
            <NewTabIcon />
          </a>
        </li>

        <li>
          <a
            href="https://portfoliomanager.energystar.gov/pdf/reference/US%20National%20Median%20Table.pdf"
            target="_blank"
            rel="noopener"
          >
            U.S. Energy Use Intensity by Property Type | ENERGY STAR [PDF]
            <NewTabIcon />
          </a>
        </li>
      </ul>
    </div>
  </DefaultLayout>
</template>

<style lang="scss">
.take-act-page {
  h1 {
    margin-bottom: 0;
  }

  .subtitle {
    font-size: 1.25rem;
    font-weight: 500;
    margin-top: 0;
  }
}
</style>
