<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import NewTabIcon from '~/components/NewTabIcon.vue';
import BuildingTile from '../../components/BuildingTile.vue';

// TODO: Figure out a way to get metaInfo working without any
// https://github.com/xerebede/gridsome-starter-typescript/issues/37
@Component<any>({
  components: {
    BuildingTile,
    NewTabIcon,
  },
  metaInfo() {
    return {
      title: 'How We Grade Buildings, And Why',
      meta: [
        {
          // TODO: Make this work
          key: 'description',
          name: 'description',
          content:
            'Electrify Chicago gives buildings letter grades, but how are they calculated?',
        },
      ],
    };
  },
})
export default class HowWeGradeBuildings extends Vue {}
</script>
<template>
  <DefaultLayout>
    <div class="how-we-grade-page">
      <div class="layout-constrained">
        <h1 id="main-content" tabindex="-1">How We Grade Buildings, And Why</h1>

        <div class="table-of-contents">
          <h2>Table Of Contents</h2>

          <ul class="-spaced">
            <li><a href="#why-grade">Why Grade Buildings?</a></li>
            <li>
              <a href="#north-stars"
                >Our North Stars - Energy Use & Energy Mix</a
              >
            </li>
            <li><a href="#examples">Some Examples Of Each Grade</a></li>
            <li><a href="#formula">The Actual Formula</a></li>
            <li>
              <a href="#limitations">
                Limitations: We Don't Know What Goes On <em>Inside</em> A
                Building
              </a>
            </li>
            <li>
              <a href="#anomaly-detection"
                >The Last Piece - Anomaly Detection</a
              >
            </li>
          </ul>
        </div>

        <p>
          We've been working towards grading buildings at Electrify Chicago for
          a long time, and in March 2025 we rolled out our first version. Let's
          walk through how it works, and why!
        </p>

        <h2 id="why-grade">Why Grade Buildings?</h2>

        <p>
          <strong
            >We want to make it easy for folks to see, at-a-glance, whether a
            building is &ldquo;good&rdquo; or &ldquo;bad&rdquo; compared to
            other city buildings</strong
          >. But good and bad are relative, so let's explain what our team means
          by that.
        </p>

        <h2 id="north-stars">Our North Stars - Energy Use & Energy Mix</h2>

        <p>
          At Electrify Chicago, we're focused on the impact of buildings on
          climate change, and on encouraging buildings to reduce their
          emissions, so we have two primary criteria for what makes a building
          good:
        </p>

        <p class="bold">Our Highly Rated Buildings:</p>

        <ol class="-spaced">
          <li class="bold">Use As Little Energy As Possible Per Square Foot</li>
          <li class="bold">
            Use Primarily (Or Only) Electricity, Rather Than Burning Fuels For
            Energy
          </li>
        </ol>

        <p>
          The first point is easy to explain - the less energy a building uses
          per square foot, the lower emissions it has, and this metric is
          agnostic to building size. We considered grading by total emissions,
          but that would mean that incredibly efficient large buildings could
          never get an A grade.
        </p>

        <p>
          For the second point - electricity <em>can</em> be made without
          creating emissions. In Illinois, we have a large fleet of nuclear
          plants that create low-carbon electricity, and a growing numbers of
          solar and wind plants joining our grid. That means that two buildings
          with the same energy use, but one using electricity and one using
          fossil gas, are very different - in 10 years, without any internal
          changes, the all-electric building will have reduced its emissions as
          the grid gets cleaner year-by-year.
        </p>
      </div>

      <div class="layout-constrained">
        <h2 id="examples">Some Examples Of Each Grade</h2>

        <p>
          To demonstrate what some good and bad buildings look like, here's a
          set of buildings with each letter grade:
        </p>
      </div>

      <div class="buildings-scroll-cont">
        <ul class="building-tiles">
          <li
            v-for="building in $page.sampleBuildings.edges"
            :key="building.node.ID"
          >
            <BuildingTile
              :building="building.node"
              :path="building.node.path"
            />
          </li>
        </ul>
      </div>

      <div class="layout-constrained">
        <p>Here's a few tidbits about these buildings:</p>

        <ul class="-spaced">
          <li>
            <strong>Marina Towers</strong> are all-electric (giving them an A
            for Energy Mix) and a bit more energy efficient than the average
            benchmarked building (giving them a B for Emissions Intensity), and
            an overall A grade.
          </li>
          <li>
            <strong>The Monadnock Building</strong> uses mostly gas (giving it a
            D for Energy Mix) but is very energy efficient due to it's several
            foot thick brick walls (giving it an A for Emissions Intensity) and
            an overall B grade.
          </li>
          <li>
            <strong>The Art Institute of Chicago</strong> uses mostly gas
            (giving it a C for Energy Mix) and is a lot less energy efficient
            than the average benchmarked building (giving it an F for Emissions
            Intensity), and an overall D grade.
          </li>
        </ul>
      </div>

      <div class="layout-constrained">
        <h2 id="formula">The Actual Formula</h2>

        <ul class="-spaced">
          <li>
            <strong>50% GHG Intensity</strong> - this is a percentile compared
            to the other buildings in the data, so the highest score (an A) goes
            to a building with lower emissions intensity than 80% of buildings.
          </li>
          <li>
            <strong>40% Energy Mix</strong> - this is a percentile compared to
            the other buildings in the data in terms of how much electricity
            (including district chilling, where a central building cools water
            and then distributes it) the building uses. So the highest score
            (80%, an A) goes to a building with less gas use than 80% of
            buildings.
          </li>
          <li>
            <strong>10% Consistent Reporting</strong> - this is a simple share
            of how consistently a building reported. 80%+ reporting gets an A.
          </li>
        </ul>

        <h2 id="limitations">
          Limitations: We Don't Know What Goes On <em>Inside</em> A Building
        </h2>

        <p>
          One of the biggest limitations of the city benchmarking data is that,
          compared to a formal energy auditing process, no information is
          collected on how a building is used. The same energy use and emissions
          intensity is very different if a building:
        </p>

        <ul class="-spaced">
          <li>Is open 24/7 to the public</li>
          <li>Runs refrigerators and freezers to keep food safe</li>
          <li>
            Heats, cools, and filters millions of gallons of water for aquarium
            exhibits
          </li>
        </ul>

        <h3>What We Know From The Benchmarking Data</h3>

        <img
          class="what-we-know-diagram"
          src="/how-we-grade/what-we-know-diagram.svg"
          width="80%"
          alt="A diagram showing an arrow labelled 'Energy' going into a box with a question mark on
          it labelled 'The Building' and with an arrow coming out labelled 'Emissions'"
        />

        <p>
          Since we can't consistently get such information on the internals of
          each building, we grade all buildings compared to all other city
          buildings. This means that some buildings are marked as average that
          should be expected to perform better (say because they are an office
          building) while justified high energy intensity uses (like aquariums)
          will be penalized.
        </p>

        <h2 id="anomaly-detection">The Last Piece - Anomaly Detection</h2>

        <p>
          Looking purely at the latest data, some buildings <em>appear</em> to
          be incredibly efficient, and use very little energy. Some buildings,
          for example, report 0 natural gas use in their latest year. But does
          anything about the gas use of
          <g-link to="/building/1830-n-winchester-ave/"
            >1830 N Winchester Ave.</g-link
          >
          (from 2022) look suspicious to you?
        </p>

        <img
          class="-shadowed"
          src="/how-we-grade/fake-zero-gas-from-1830-n-winchester.webp"
          width="500"
          alt="A tile showing 'Fossil Gas Use' of 0 kBtu, but with a historical graph
          showing that in 2018 the natural gas use was 1.7 million kBTU"
        />

        <p>
          This building reported 0 gas use in 2021 to 2022, but had 1.7 million
          kBTUs of gas usage in 2018. We can pretty safely say,
          <strong>this building didn't actually use 0 fossil gas</strong>, but
          instead just failed to report their gas usage. Although it is possible
          buildings fully electrify, we'd expect to see a large increase in
          electricity use as gas heating moves over to electric. Physics
          dictates we still need energy to keep buildings warm, no matter the
          fuel type!
        </p>

        <p>
          To this end, we try to detect and flag such data anomalies - you'll
          see a warning at the top of the building's page, as well as on the
          report card, like so:
        </p>

        <img
          src="/how-we-grade/sample-flagged-building.webp"
          class="-shadowed"
          alt="1830 N Winchester Ave's building page, showing an 'Anomaly Detected' notice at the
            top and a warning obscuring the report card."
        />

        <h2>Have Feedback On Our Grading?</h2>

        <p>
          If you have suggestions on how we can make our grading better, from
          improved anomaly detection to new data sources we can integrate, let
          us know, by
          <a href="https://github.com/vkoves/electrify-chicago/issues/new"
            >filing an issue on our GitHub</a
          >!
        </p>
      </div>
    </div>
  </DefaultLayout>
</template>

<page-query>
  query {
    sampleBuildings: allBuilding(
      filter: {
        ID: {
          in: [
            # A - F buildings - Marina Towers, Monadnock Building, Core Site, Art Institute &
            # Crown Hall
            "239096", "131236", "101567", "160196", "256419"
          ]
        }
      }
      sortBy: "AvgPercentileLetterGrade"
      order: ASC
      limit: 10
    ) {
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
          TotalGHGEmissions
          ElectricityUse
          NaturalGasUse
          DistrictSteamUse
          AvgPercentileLetterGrade
        }
      }
    }
  }
</page-query>

<style lang="scss">
.how-we-grade-page {
  div.table-of-contents {
    background: $off-white;
    border-radius: $brd-rad-small;
    padding: 1rem 1.5rem;
    width: fit-content;
    margin-bottom: 1rem;

    h2 {
      margin-top: 0;
      font-size: 1.25rem;
    }

    a {
      display: block;
      font-weight: bold;
    }

    ul {
      padding-left: 1.25rem;
      margin: 0;
    }
  }

  ul.-spaced,
  ol.-spaced {
    li + li {
      margin-top: 0.5rem;
    }
  }

  // Center images
  img {
    display: block;
    margin-left: auto;
    margin-right: auto;
  }

  img.what-we-know-diagram {
    display: block;
    margin-top: 1rem;
    margin-bottom: 2rem;
    max-width: 30rem;
  }

  @media (max-width: $mobile-max-width) {
    img.what-we-know-diagram {
      width: 100%;
    }
  }
}
</style>
