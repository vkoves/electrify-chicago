<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import NewTabIcon from '~/components/NewTabIcon.vue';

// Extend Vue options with metaInfo
@Component({
  components: {
    NewTabIcon,
  },
})
export default class MillionsInMissedFine extends Vue {
  readonly NotifLetterUrl =
    'https://www.chicago.gov/content/dam/city/progs/env/EnergyBenchmark/sample_notification_letter.pdf';

  readonly NonReportingBuildingsDataUrl =
    'https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c/explore/query/...';

  results: Record<string, unknown> | unknown[] | null = null;
  loading = true;
  isMobile = false; // Add mobile detection flag

  async mounted(): Promise<void> {
    this.checkScreenSize();
    window.addEventListener('resize', this.checkScreenSize);

    const jsonFilePath =
      '/blog/GHGIntensityPredictCompliance/regression_results_w_covid.json';

    console.log('Fetching JSON from:', jsonFilePath);

    try {
      const response = await fetch(jsonFilePath);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      this.results = await response.json();
      console.log('Loaded regression results:', this.results);
    } catch (error) {
      console.error('Error loading regression results:', error);
    } finally {
      this.loading = false;
    }
  }

  beforeDestroy(): void {
    window.removeEventListener('resize', this.checkScreenSize);
  }

  checkScreenSize(): void {
    this.isMobile = window.innerWidth <= 768;
  }

  metaInfo(): Record<string, unknown> {
    return {
      title: 'Do High Emitting Buildings Fail to Report?',
    };
  }
}
</script>

<template>
  <DefaultLayout>
    <article class="layout-constrained compliance-analysis blog-post">
      <g-link to="/blog" class="back-link grey-link"> Back to Blog </g-link>

      <h1 id="main-content" tabindex="-1">
        Do High Emitters Stop Reporting Emissions Data in the Future?
      </h1>
      <p class="sub-title constrained">
        Analyzing Patterns in Greenhouse Gas Emissions Reporting
      </p>
      <p class="author">
        Analysis by
        <a href="https://github.com/colton-lapp" class="author-link"
          >Colton Lapp</a
        >, with assistance and review by Viktor Koves
      </p>

      <p class="publish-time">
        <!-- TODO: Update publish time when PR is about to get merged -->
        Published <time datetime="2025-02-10">Feb. 10th, 2025</time>
      </p>

      <p class="constrained">
        Many buildings in the
        <a
          href="https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c/about_data"
          target="_blank"
          rel="noopener noreferrer"
          >Chicago building benchmarking</a
        >
        data
        <a
          href="https://electrifychicago.net/blog/millions-in-missed-fines"
          target="_blank"
          rel="noopener noreferrer"
          >don't report their emissions.</a
        >
        Is there a pattern to which buildings fail to report? Our team has
        noticed that some high emissions buildings stop reporting, while more
        efficient buildings tend to keep reporting year after year. In this
        blog, we investigate if there is a broader pattern at play - are
        buildings emission levels linked to a building's reporting compliance?
      </p>

      <h2>Analyzing the Emissions Data</h2>

      <p>
        To understand if there was a link between reporting compliance and
        emissions, we analyzed Chicago's building benchmarking data. As a first
        step, we wanted to investigate the overall landscape of emissions
        reporting. We started by computing some general statistics about
        emissions reporting.
      </p>

      <p class="constrained bold">Historical Patterns of Non-Reporting</p>

      <p>
        The graph below depicts the count of buildings that did and did not
        report emissions data each year.
      </p>

      <div>
        <div v-if="isMobile">
          <img
            src="/blog/GHGIntensityPredictCompliance/reporting_counts_over_time.png"
            alt="Reporting Counts Over Time"
            style="width: 100%; height: auto"
          />
        </div>

        <div v-else>
          <iframe
            src="/blog/GHGIntensityPredictCompliance/reporting_counts_over_time.html"
            frameborder="1"
            width="100%"
            height="500px"
          ></iframe>
        </div>
      </div>

      <p>Several things can be seen from the time series analysis above.</p>

      <ul>
        <li>
          The pool of covered buildings grew from a <b>few hundred</b> to a
          <b>few thousand</b> buildings during the ramp up period of the program
          from 2014 to 2016
        </li>
        <li>
          There was a sharp <b>drop in emissions</b> reporting during the
          <b>COVID-19 pandemic</b>. Buildings report emissions for the previous
          year in the spring, so emissions for 2019 were not reported in the
          spring of 2020.
        </li>
        <li>
          Outside of the disruption from COVID-19, between <b>a third</b> to
          <b>a fourth</b> of covered buildings
          <b>fail to report every year</b> (starting in 2018)
        </li>
      </ul>

      <h2>Understanding Emissions Intensities</h2>

      <p>
        Our goal was to understand if 'bad' levels of emissions are related to
        buildings failing to report in subsequent years. To answer this, we need
        to choose a metric to measure what constitutes 'bad' levels of
        emissions. Our preferred metric is <b>Green House Gas Intensity</b> (GHG
        Intensity), the amount of greenhouse gas released <em>per</em>
        square foot. Buildings with GHG Intensity levels that are abnormally
        high or trending in a bad direction may strategically choose not to
        report data the next year.
      </p>

      <p class="constrained bold">What are normal emissions intensities?</p>

      <div>
        <div v-if="isMobile">
          <img
            src="/blog/GHGIntensityPredictCompliance/distribution_of_GHG_intensity.png"
            alt="Distribution of GHG Intensity Values"
            style="width: 100%; height: auto"
          />
        </div>

        <div v-else>
          <iframe
            src="/blog/GHGIntensityPredictCompliance/distribution_of_GHG_intensity.html"
            frameborder="0"
            width="100%"
            height="450px"
          ></iframe>
        </div>
      </div>

      <p>
        As can be seen above, most buildings have
        <b>GHG intensities between 0 and 20</b>, but some outliers have GHG
        intensities <b>well above 200</b>.
      </p>

      <h2>
        Analysis: Do levels/trends in emissions predict reporting compliance?
      </h2>

      <p>
        To understand whether or not emissions patterns were related to
        reporting compliance, we looked at two different emissions
        characteristics:
      </p>

      <ol>
        <li>The <b>GHG Intensity</b> level <b>a year prior</b></li>
        <li>
          The <b>change in GHG intensity</b> levels between <b>last year</b> and
          <b> two years ago</b>
        </li>
      </ol>

      <p>For both of these values, we were curious to know:</p>

      <ol>
        <li>
          Does last years <b>GHG intensity level</b> predict this year's
          <b>reporting compliance?</b>
        </li>
        <li>
          Does the <b>change in GHG intensity</b> in the last two years predict
          this year's <b>reporting compliance?</b>
        </li>
      </ol>

      <p>
        We computed the mean and median of the level and trend of GHG intensity
        for both groups of buildings: Reporting and Non-Reporting. In the graphs
        below, we show these statistics only for the most recent year of data.
        When we expand the analysis for all years of data, the findings do not
        meaningfully change. As can be seen, there are no real group differences
        in emission characteristics between the two groups:
      </p>

      <div>
        <div v-if="isMobile">
          <img
            src="/blog/GHGIntensityPredictCompliance/GHG_last_year_by_compliance_recent_data_only.png"
            alt="GHG Last Year Compliance"
            style="width: 100%; height: auto"
          />

          <img
            src="/blog/GHGIntensityPredictCompliance/change_GHG_trend_by_compliance_recent_data_only.png"
            alt="Change GHG Trend Compliance"
            style="width: 100%; height: auto"
          />
        </div>

        <div v-else>
          <iframe
            src="/blog/GHGIntensityPredictCompliance/GHG_last_year_by_compliance_recent_data_only.html"
            frameborder="0"
            width="100%"
            height="400px"
          ></iframe>

          <iframe
            src="/blog/GHGIntensityPredictCompliance/change_GHG_trend_by_compliance_recent_data_only.html"
            frameborder="1"
            width="100%"
            height="400px"
          ></iframe>
        </div>
      </div>

      <h2>Results: No meaningful difference between groups</h2>

      <p>
        As can be seen from both of the graphs above, it seems that there is no
        real pattern between emission intensities or emission trends when it
        comes to compliance. Instead, it seems that whether or not buildings
        report their emissions data seems pretty unrelated to a buildings
        emissions profile.
      </p>

      <h2>Investigating Further</h2>

      <p>
        Although the graphs above suggest that the average values between
        compliant and non-compliant buildings are similar, several factors could
        be driving this (lack of a) finding. These considerations are grouped
        into three key areas:
      </p>

      <section class="-indented">
        <h3>1. Impact of COVID-19 on Reporting Rates</h3>
        <p>
          Most of the buildings that did not report data coincided with the
          COVID-19 drop in reporting rates.
        </p>
        <p>
          <strong>Question:</strong> If we omit the year of data from COVID-19,
          do the results change?
        </p>
      </section>

      <section class="-indented">
        <h3>2. Influence of Outliers</h3>
        <p>
          While most buildings have low emissions intensities and minimal
          changes, several outliers are present. Outliers in GHG intensitity
          values distort mean values for groups (although median values should
          not be as affected).
        </p>
        <p>
          <strong>Question:</strong> If we omitted the outliers, do the results
          change?
        </p>
      </section>

      <section class="-indented">
        <h3>3. Omitted Predictive Characteristics</h3>
        <p>
          Emissions intensity and trends are not the only factors that might
          predict compliance with reporting laws. The building type, for
          example, likely matters a great deal when it comes to GHG intensity
          (i.e. data centers, gyms and aquariums have different energy needs and
          operating hours). Some of these characteristics might also correlate
          with reporting compliance in a way that could be obscuring underlying
          trends.
        </p>
        <p>
          <strong>Question:</strong> What other characteristics might be
          predictive of GHG intensity, and if we control for them, will the
          results change?
        </p>
      </section>

      <h2>Investigating Further: Analysis</h2>

      <p>
        To address questions #1 and #2 (COVID-19 and/or outliers) driving our
        results, we ran further analysyis where we excluded both of these sets
        of data points and recalculated our mean and median values across
        groups. Ultimately, we found that
        <b>the results still showed no meaningful difference between groups.</b>
        This leads us to believe that these factors were not driving our
        results.
      </p>

      <p>
        What about other predictive factors that might be masking a
        relationship? To try to address this question, we ran a regression
        analysis and included square footage as a control variable. Linear
        regression is a tool that can try to control for external factors to
        understand what a variables isolated effect is on our outcome of
        interest. A limitation in our regression model is that we have very few
        variables to add as control variables. An area of future work could be
        to merge other data sources into our buildings dataset to try to control
        for a broader array of building characteristics. In this model, the only
        control we added was square footage. The results are below:
      </p>

      <!-- Regression Results Section -->
      <div>
        <h2>Regression Results: Linear Probability Model</h2>

        <!-- Check if results exist -->
        <div id="regression-container">
          <template v-if="results">
            <table>
              <thead>
                <tr>
                  <th class="cell-bordered">Variable</th>
                  <th class="cell-bordered">Coefficient</th>
                  <th class="cell-bordered">P-Value</th>
                  <th class="cell-bordered">
                    Confidence Interval (0.025, 0.975)
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(coef, variable) in results.coefficients"
                  :key="variable"
                >
                  <td class="cell-bordered">{{ variable }}</td>
                  <td class="cell-bordered">{{ coef.toFixed(3) }}</td>
                  <td class="cell-bordered">
                    {{ results.p_values[variable].toFixed(3) }}
                  </td>
                  <td class="cell-bordered">
                    [{{ results.confidence_intervals[variable][0].toFixed(3) }},
                    {{ results.confidence_intervals[variable][1].toFixed(3) }}]
                  </td>
                </tr>
              </tbody>
            </table>
            <p>
              <strong>Dependent Variable:</strong>
              {{ results.dependent_variable }}<br />
              <strong>Number of Observations:</strong>
              {{ results.number_of_observations }}<br />
              <strong>R-Squared:</strong> {{ results.r_squared.toFixed(3)
              }}<br />
              <strong>Adjusted R-Squared:</strong>
              {{ results.adj_r_squared.toFixed(3) }}<br />
              <strong>Covariance Type:</strong> {{ results.covariance_type }}
            </p>
          </template>
          <!-- Loading and error handling -->
          <p v-else-if="loading">Loading regression results...</p>
          <p v-else>
            Error loading regression results. Please try again later.
          </p>
        </div>

        <p>
          <br />
          It doesn't seem like the level of GHG intensity or the trend of GHG
          intensity help predict compliance at all. Building size does help
          predict compliance a tiny bit though. For every million additional
          square feet, the building is roughly 1.5% less likely to be NON
          compliant. In general, this is a very weak finding and the variables
          we currently do have don't seem to predict reporting compliance much
          at all. We ran these regressions with the dataset of no outliers and
          no covid data as well and found similar results - details can be seen
          in the linked Jupyter notebook below.
        </p>

        <h2>Explore our Analysis</h2>

        <p>
          Interested in diving deeper into our analysis? You can view the code
          and interactive data exploration
          <a
            href="https://nbviewer.org/github/vkoves/electrify-chicago/blob/compliance-analysis/src/data/analysis/GHG_intensity_compliance_correlation.ipynb"
            target="_blank"
            rel="noopener noreferrer"
            >in the linked Jupyter Notebook.</a
          >
        </p>
      </div>

      <h2>Questions?</h2>

      <p>
        Contact the lead developer on this site, Viktor Köves, by emailing
        <a href="mailto:contact@viktorkoves.com">contact@viktorkoves.com</a>
      </p>
    </article>
  </DefaultLayout>
</template>
<style lang="scss">
.compliance-analysis {
  h1 {
    margin-bottom: 0;
    line-height: 1.25;

    + p {
      margin: 0.25rem 0 0.5rem 0;
    }
  }
  .author {
    font-size: 0.9em; /* Slightly smaller */
    font-style: italic; /* Makes text italic */
    font-weight: normal;
    margin-top: 0.2rem;
    margin-bottom: 0.2rem;
    line-height: 1.2;
  }

  h3 {
    font-size: 1em;
    font-weight: bold;
  }

  a.back-link {
    margin: 1rem 0 0 0;
    display: inline-block;
    font-weight: 600;
  }

  table {
    border-collapse: collapse;
    width: 100%;
    border: $border-thin solid $black;
  }

  iframe {
    border: $border-medium solid $black;
    border-radius: 0.5rem;
  }

  .cell-bordered {
    border: solid $border-thin $black;
  }

  section.-indented {
    margin-left: 1rem;
  }
}
</style>
