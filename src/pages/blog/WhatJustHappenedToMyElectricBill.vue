<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';
import LCOEBySource from '~/components/blog/electric-bill/LCOEBySource.vue';
import USElectricityConsumption from '~/components/blog/electric-bill/USElectricityConsumption.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    NewTabIcon,
    LCOEBySource,
    USElectricityConsumption,
  },
  metaInfo() {
    return {
      title: 'What Just Happened to My Electric Bill?',
      meta: [
        {
          key: 'description',
          name: 'description',
          content:
            'ComEd bills have shot up dramatically. Learn why PJM, the regional grid operator, ' +
            'is the real cause of rising electric rates and what you can do about it.',
        },
      ],
    };
  },
})
export default class WhatJustHappenedToMyElectricBill extends Vue {}
</script>

<template>
  <DefaultLayout>
    <article class="layout-constrained electric-bill-blog blog-post">
      <g-link to="/blog" class="back-link grey-link">
        <img src="/icons/arrow-back.svg" alt="" />
        Back to Blog
      </g-link>

      <h1 id="main-content" tabindex="-1">
        What just happened to my electric bill?
      </h1>
      <p class="sub-title">The root cause and what you can do about it</p>

      <p class="publish-time">
        Published <time datetime="2025-11-03">Nov. 3rd, 2025</time>
      </p>

      <p>
        If you're reading this, there's a good chance you saw your ComEd bill
        shoot up in the last few months.
      </p>

      <blockquote>
        <span class="quote">&ldquo;</span>Olivia Odendahl, 26, who shares a
        Lakeview two-bedroom walkup apartment with a roommate, saw her July 18
        ComEd bill <strong>more than double</strong> month-over-month to
        <strong>$120.83.</strong>
        <span class="quote">&rdquo;</span>
      </blockquote>

      <p class="footnote">
        Source:
        <a
          href="https://www.chicagotribune.com/2025/07/22/comed-supply-rate-bill-increases/"
          target="_blank"
          rel="noopener"
          >Chicago Tribune - ComEd supply rate bill increases
          <NewTabIcon />
        </a>
      </p>

      <p>
        It's been a hot few months, of course, and we're all used to electric
        bills being higher in the summer. But this year, that's only half the
        picture.
      </p>

      <p>
        The story behind the price increases is surprisingly complex, but much
        of it can be told with just three players:
      </p>

      <ul>
        <li>A costly coal plant</li>
        <li>A power-hungry data center</li>
        <li>PJM</li>
      </ul>

      <p>
        Never heard of PJM? That puts you firmly in the majority of people. In
        short, they're the largest electric grid operator in the US. And also,
        unfortunately, your grid operator, because as it turns out, PJM is the
        real cause of our electric rates going up.
      </p>

      <p>
        But we'll get to all that. Our story begins not with the mysterious PJM
        but with plain old, all-too-familiar coal.
      </p>

      <h2>Player one: the costly coal plant</h2>

      <p>
        The role of the coal plant in this story is a simple one: it's powering
        down.
      </p>

      <p>
        For half a century—from the 1950s to the 2000s—roughly half of all US
        electricity came from coal. The reason for this is just what you'd
        expect: it was cheap. (Cheap, that is, as long as you ignore its
        externalities.)
      </p>

      <p>
        It's for just those same economic reasons that coal plants across the
        country are shutting down. When it comes to cost, coal has become the
        expensive option. It isn't so much that coal itself has gotten more
        expensive, but that we now have substantially cheaper ways of producing
        electricity.
      </p>

      <p>
        As a result, the US has been in the process of replacing coal power
        plants with more cost-effective options. At first this generally meant
        natural gas plants. But today—believe it or not—the cheapest source of
        new generation is renewables, led by solar and wind.
      </p>

      <LCOEBySource />

      <p class="footnote">
        Source:
        <a
          href="https://ourworldindata.org/grapher/levelized-cost-of-energy"
          target="_blank"
          rel="noopener"
          >Our World In Data - Levelized Cost of Energy
          <NewTabIcon />
        </a>
      </p>

      <p>
        Ok, that's the rundown on the supply side. Now let's turn to demand.
      </p>

      <h2>Player two: the power-hungry data center</h2>

      <p>
        The data center in our story is here to play the role of electricity
        consumer, and not for no reason. Between 2023 and 2028, data centers are
        expected to account for close to half of all new demand on our power
        grid. <sup>*</sup>
      </p>

      <p class="footnote">
        <sup>*</sup> While that could amount to more like 12% of total
        electricity, the grid works on marginal demand—new and unexpected demand
        strains supply.
      </p>

      <p>
        So just as our oldest power plants are shutting down, data centers are
        ramping up—and fast.
      </p>

      <p>
        While it might seem easy to simply blame data centers, in many ways,
        they're simply revealing a problem that was already there. The US has
        just emerged from a slumbering two-decade period of basically flat
        demand growth on an aging grid. Even without data centers, we would
        still need to modernize our grid to support a future that will be
        increasingly electric as we transition to efficient and clean
        technologies like electric vehicles and heat pumps.
      </p>

      <USElectricityConsumption />

      <p class="footnote">
        Source:
        <a
          href="https://www.eia.gov/totalenergy/data/browser/index.php?tbl=T07.06#/?f=A&start=1949&end=2022&charted=1-2-3-4-5-6"
          target="_blank"
          rel="noopener"
        >
          U.S. Energy Information Administration - Electricity Retail Sales
          <NewTabIcon />
        </a>

        <br />

        See more:
        <a
          href="https://www.utilitydive.com/news/us-electricity-demand-will-grow-50-by-2050-electrical-manufacturer-study/744575/"
          target="_blank"
          rel="noopener"
        >
          US electricity demand will grow 50% by 2050... - Utility Dive
          <NewTabIcon />
        </a>
      </p>

      <p>
        Which brings us to who that "we" actually refers to. Who's responsible
        for keeping the two sides of this equation balanced, ensuring that we
        have enough electricity to meet our growing demand?
      </p>

      <p>That, in a nutshell, is the role of PJM.</p>

      <h2>Player three: PJM</h2>

      <p>
        Thought ComEd was in charge of our electricity? Well you're right. But
        that's not the whole picture.
      </p>

      <p>
        Where ComEd serves as a sort of local distributor of electricity here in
        Chicago, PJM coordinates the transmission of power across a vast,
        13-state region. If ComEd maintains city streets, PJM oversees the
        interstate highway system. They are what's known as a "grid operator."
      </p>

      <p>
        It's PJM's job to ensure that there is enough total generation capacity
        (think: power plants) to keep the lights on across the region. Not just
        for tonight, but three years from tonight.
      </p>

      <p>
        To make a guarantee like this in the face of all the uncertainties that
        "years out" entails, PJM and power generators make a deal. If generators
        promise to provide that electric capacity in three years, PJM will pay
        them a bounty for it.
      </p>

      <p>
        This brings us to the crux of the matter—the immediate reason our
        electric bills just went up. That bounty, known as the "capacity price,"
        has increased astronomically in the past two years—it's increased by
        over 1,000% (!!) This has a direct and visible impact on your electric
        bill—it shows up in the "supply" section of your ComEd bill.
      </p>

      <p>This leads to the natural question: Why is this happening?</p>

      <p>
        Part of the answer lies in the dynamics of the first two players: coal
        plants shutting down and data centers ramping up. But despite those
        dynamics, it 100% does not need to be this way.
      </p>

      <p>
        The fundamental challenge we're facing is insufficient supply for our
        rapidly growing demand. The obvious solution to this problem also
        happens to be the correct one: increase the supply!
      </p>

      <p>
        Unfortunately, it's here that PJM is falling disastrously short. PJM is
        the slowest of all grid operators in the US at getting new electricity
        generators onto the grid, with new energy sources waiting an average of
        5 years to connect.
      </p>

      <p>
        In a report on how the seven major grid operators in the US are handling
        this, PJM came in dead last. Its overall grade was a D-.
      </p>

      <aside class="highlight-box">
        <p>
          <strong
            >The highest scoring grids (ERCOT and CAISO), tended to have
            better:</strong
          >
        </p>
        <ul>
          <li>
            <strong>Grid study assumption clarity</strong> - helping power
            providers know the criteria for getting on the grid
          </li>
          <li>
            <strong>Interconnection alternatives</strong> - like letting new
            energy providers join the grid at certain times on a flexible basis
            instead of all-or-nothing
          </li>
          <li>
            <strong>Regional transmission planning</strong> - actually building
            out their network based on where they think the new power sources
            will be, including for renewables
          </li>
        </ul>

        <p>
          What's more, PJM has a tendency to significantly overestimate future
          electricity demand, which further compounds its other problems. By not
          planning for renewables—the cheapest source of new energy—PJM's
          inflated assumptions about demand then result in a fossil fuel bias.
        </p>

        <p>
          In December, PJM will submit new rules to FERC (the federal grid
          regulator) to allow some energy providers to "jump the line" and get
          quicker approval. As designed, the rule gives preference to projects
          over 500 megawatts and 3-year completion times, which would prioritize
          more costly (and polluting) gas plants.
        </p>
      </aside>

      <h2>How renewables can help with energy prices</h2>

      <p>
        Solar and wind are now cheaper than coal. They're cheaper than nuclear.
        They're even cheaper than natural gas.
      </p>

      <p>
        This shift has happened so quickly that very few people seem to
        appreciate it. Just 10 years ago, solar and wind were the Whole Foods of
        energy—nice if you can afford it, but you probably can't.
      </p>

      <p>
        In just the last few years they have, somewhat miraculously, transformed
        into the Costco of energy: cheap, abundant, and shockingly high quality.
      </p>

      <p>
        This is reflected by the makeup of the new generators waiting to get
        onto the grid. Fully 95% of them are solar, wind, and battery projects.
      </p>

      <p>
        Cheap renewable electricity generation is ready and waiting to connect
        to our homes and businesses. Our task now is to force open the
        floodgates.
      </p>

      <h2>How you can change the story</h2>

      <p>
        If you want to add your strength to this effort—to stop rising power
        bills and very literally save the planet at the same time—choose your
        weapon.
      </p>

      <p>
        All three of these actions are quickly done but calibrated to have
        maximum impact on the next chapter of this story.
      </p>

      <section class="action-section">
        <h3>
          A: Thank Governor Pritzker for putting pressure on PJM and tell him to
          turn up the heat
        </h3>
        <ul>
          <li>
            Governor Pritzker recently created a new group of governors to push
            PJM to improve, and Illinois is considering bills to require more
            transparency from PJM
          </li>
          <li>
            Also make sure to tell the governor if you're struggling with your
            bills! The struggle of constituents is what's motivating this fight
          </li>
          <li>
            In the meantime, though,
            <a
              href="https://www.citizensutilityboard.org/"
              target="_blank"
              rel="noopener"
              >Citizens Utility Board <NewTabIcon
            /></a>
            has resources for those burdened by utility costs
          </li>
        </ul>
      </section>

      <section class="action-section">
        <h3>
          B: Get the Clean and Reliable Grid Affordability Act (CRGA) passed
          here in Illinois
        </h3>
        <p>
          Designed as a follow-up to the 2021 Clean Energy & Jobs Act (CEJA),
          CRGA aims to level-up Illinois's portion of the grid. There are a lot
          of provisions in it, but here are a few key highlights that could help
          lower energy bills:
        </p>
        <ul>
          <li>
            Procuring 6 gigawatts (GW) of battery storage for Illinois, which
            could help deploy energy when prices are at their highest. Batteries
            would also provide "baseload" power for renewable energy, like using
            solar after the sun goes down
          </li>
          <li>
            Pushing for datacenters to have a clean energy plan before they
            build—and creating environmental standards for those plans
          </li>
          <li>
            Investing in grid enhancing technologies (GETs) and making it easier
            to build new transmission lines
          </li>
        </ul>
      </section>

      <section class="action-section">
        <h3>
          C: Tell the US Congress to put the bipartisan energy permitting reform
          bill up for a vote
        </h3>
        <p>
          If being on PJM's 13-state network has taught us anything, it's that
          the grid is bigger and more complicated than one state. It's a
          national issue.
        </p>
        <p>
          In 2024, a bipartisan bill to do national permitting reform nearly
          passed. It contained key provisions like:
        </p>
        <ul>
          <li>
            Streamlining federal review of permitting applications for all kinds
            of energy, including renewables
          </li>
          <li>
            Making it easier to build transmission lines and grid enhancement
            projects (like batteries) on "previously disturbed land" and in
            "rights of way" (like along highways)
          </li>
          <li>
            Seeking more reliability from transmission operators and protecting
            ratepayers from paying for grid upgrades that don't benefit them
          </li>
        </ul>
        <p>
          While some environmentalists oppose bipartisan reform on the basis
          that it could benefit fossil fuels, with 95% of the grid backlog being
          clean, an "all of the above" approach to permitting will still help
          with both affordability and climate change.
        </p>
      </section>
    </article>
  </DefaultLayout>
</template>

<style lang="scss">
.electric-bill-blog {
  h1 {
    margin-bottom: 0;
    line-height: 1.25;
  }

  .sub-title {
    margin: 0.25rem 0 0.5rem 0;
    font-size: 1.125rem;
    font-weight: 600;
    color: $text-light;
  }

  blockquote {
    margin: 1.5rem 0;
    padding: 1rem 1.5rem;
    background-color: $off-white;
    border-left: solid 0.25rem $blue-dark;
    font-style: italic;
    font-size: 1.125rem;
    line-height: 1.5;

    .quote {
      font-family: 'Times New Roman', serif;
      font-size: 1.5em;
      font-weight: bold;
      line-height: 0;
      vertical-align: -0.125rem;
    }
  }

  .footnote {
    font-size: 0.875rem;
    color: $text-light;
    margin-top: -0.5rem;
  }

  .highlight-box {
    margin: 2rem 0;
    padding: 1.5rem;
    background-color: $off-white;
    border: solid $border-thin $grey-dark;
    border-radius: 0.25rem;

    p:first-child {
      margin-top: 0;
    }

    p:last-child {
      margin-bottom: 0;
    }

    ul {
      margin-bottom: 1rem;
    }
  }

  .action-section {
    margin: 2rem 0;
    padding: 1.5rem;
    background-color: $blue-light;
    border-left: solid 0.25rem $blue-dark;
    border-radius: 0.25rem;

    h3 {
      margin-top: 0;
      color: $blue-dark;
    }

    p:last-child,
    ul:last-child {
      margin-bottom: 0;
    }
  }

  @media (max-width: $mobile-max-width) {
    .highlight-box,
    .action-section {
      padding: 1rem;
    }
  }
}
</style>
