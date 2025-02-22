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
        >, with assistance and review by Viktor Köves
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
          >Chicago building benchmarking data</a
        >
        <!-- Add space between two links -->
        <span style="display: inline-block; width: 6px"></span>
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
            src="/blog/GHGIntensityPredictCompliance/distribution_of_GHG_intensity_mobile.png"
            alt="Distribution of GHG Intensity Values"
            style="width: 100%; height: auto"
          />
        </div>

        <div v-else>
          <iframe
            src="/blog/GHGIntensityPredictCompliance/distribution_of_GHG_intensity.html"
            frameborder="0"
            width="100%"
            height="400px"
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

      <div class="graph-caption">
        <b>Note:</b> Graphs above showing only most recent year of data.
        Buildings that didn't report data in both years are not represented in
        these scatter plots because we don't know what their emission levels
        were in the previous year. To see additional exploration of the data and
        graphs looking at different observation sets, refer to the code we used
        for this analysis by clicking the
        <a
          href="https://nbviewer.org/github/vkoves/electrify-chicago/blob/compliance-analysis/src/data/analysis/GHG_intensity_compliance_correlation.ipynb"
          target="_blank"
          rel="noopener noreferrer"
          >Jupyter notebook link</a
        >
        at the end of this blog.
      </div>

      <h2>Results: No meaningful difference between groups</h2>

      <p>
        As can be seen from both of the graphs above, it seems that there is no
        real pattern between emission intensities or emission trends when it
        comes to compliance. Instead, it seems that whether or not buildings
        report their emissions data seems pretty unrelated to a buildings
        emissions profile in the previous year.
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
      </section>

      <section class="-indented">
        <h3>2. Influence of Outliers</h3>
        <p>
          While most buildings have low emissions intensities and minimal
          changes, several outliers are present. Outliers in GHG intensity
          values distort mean values for groups (although median values should
          not be as affected).
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
      </section>

      <h3>Additional Analysis</h3>

      <p>
        To address questions #1 and #2 (COVID-19 and/or outliers) driving our
        results, we ran further analysis where we excluded both of these sets of
        data points and recalculated our mean and median values across groups.
        Ultimately, this simple descriptive analysis still found
        <b>no meaningful difference between groups.</b>
        This made it seem like these characteristics were not driving our
        results.
      </p>

      <p>
        If COVID-19 and outliers don't seem to be affecting our results, what
        about omitted predictive characteristics? Is it possible that there are
        strong connections between certain building characteristics (age of
        building, type of building, etc) and reporting rates? One building
        characteristic, for example, that likely affects reporting and emissions
        is the building type (office, school, etc). A quick visualization of
        reporting rates by building type in fact does show that there are some
        patterns across groups:
      </p>

      <h3>Variance in Reporting Across Building Type</h3>
      <div>
        <div v-if="isMobile">
          <img
            src="/blog/GHGIntensityPredictCompliance/reporting_rates_by_building_type_min_100.png"
            alt="GHG Last Year Compliance"
            style="width: 100%; height: auto"
          />
        </div>

        <div v-else>
          <iframe
            src="/blog/GHGIntensityPredictCompliance/reporting_rates_by_building_type_min_100.html"
            frameborder="0"
            width="100%"
            height="550px"
          ></iframe>
        </div>
      </div>
      <div class="graph-caption">
        <b>Note:</b> This graph only showing building categories with 100 or
        more observations. There are actually over 50 different building types,
        but most have less than a dozen buildings in the data. To see this graph
        with all the different building types, please view the
        <a
          href="https://nbviewer.org/github/vkoves/electrify-chicago/blob/compliance-analysis/src/data/analysis/GHG_intensity_compliance_correlation.ipynb"
          target="_blank"
          rel="noopener noreferrer"
          >Jupyter notebook link</a
        >
        at the end of this blog.
      </div>

      <p>
        In the graph above, it can be seen that two of the most common building
        categories, <b>"K-12 Schools"</b> and <b>"Multifamily Housing"</b> have
        very different reporting rates (<b>27%</b> and <b>17%</b>,
        respectfully). Is it possible that these trends, as well as their
        intersection with other patterns (like the drop off in COVID-19
        reporting), could be obscuring a relationship between emission levels
        and reporting compliance?
      </p>

      <h2>Regression Analysis</h2>
      <p>
        With these considerations in mind, we wanted to test the possibility
        that external factors might be obfuscating an underlying connection
        between emissions and reporting. To test this, we decided to run a
        linear regression analysis. Linear regression is a statistical technique
        that attempts to understand what the isolated effect of a variable is on
        a given outcome, while controlling for external factors. In our example,
        we are trying to rule out the possibility that some building
        characteristics (i.e. square footage, age of building, building type)
        and/or time trends could be obscuring a hidden pattern in the data of
        emissions being linked to reporting.
      </p>

      <p>
        Specifically, we fit a linear probability model where our outcome of
        interest is equal to 1 if a building failed to report in a given year.
        The analysis includes buildings that reported complete emissions data in
        the past two years, regardless of whether they reported in the current
        year. Thus, buildings that consistently fail to report are excluded, as
        we can't determine how their emissions affect reporting compliance if we
        don't have data on their emissions. Many buildings that consistently
        report appear multiple times in the dataset for different time periods.
      </p>

      <p>
        In the regression model, we controlled for
        <b>building characteristics</b> that we observe as well as the
        <b>time period</b> the data was collected in (to account for trends like
        COVID-19). The estimates of that model are reported below:
      </p>

      <!-- Regression Results Section -->
      <div>
        <h3>Regression Results: Linear Probability Model</h3>

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
                <tr>
                  <td class="cell-bordered">Building Type Dummy Variables:</td>
                  <td class="cell-bordered italic">
                    {{ results.building_type_dummy }}
                  </td>
                  <td class="cell-bordered"></td>
                  <td class="cell-bordered"></td>
                </tr>
                <tr>
                  <td class="cell-bordered">Year Dummy Variables:</td>
                  <td class="cell-bordered italic">
                    {{ results.year_fixed_effects }}
                  </td>
                  <td class="cell-bordered"></td>
                  <td class="cell-bordered"></td>
                </tr>
              </tbody>
            </table>
            <p class="regression-p">
              <strong>Dependent Variable:</strong>
              "{{ results.dependent_variable }}"<br />
              <strong>"Building Type" Categorical Dummy Variables:</strong>
              {{ results.building_type_dummy }}<br />
              <strong>"Year" Dummy Variables:</strong>
              {{ results.year_fixed_effects }}<br />
              <strong>Number of Observations:</strong>
              {{ results.number_of_observations }}<br />
              <strong
                >Number of Observations Dropped in Regression Due to Missing
                Independent Variables:</strong
              >
              {{ results.total_dropped_rows }} ({{
                results.total_dropped_rows_pct
              }}%)<br />
              <strong
                >Number of Observations Where Outcome was "{{
                  results.dependent_variable
                }}":</strong
              >
              {{ results.pct_obs_are_one }}% <br />
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
          As can be seen from the regression analysis above,
          <b
            >it doesn't seem like there is any meaningful relationship between
            the emission levels or trends of a building and whether or not it
            reports data.</b
          >
          The coefficient estimates for both of our emission related variables
          (GHG Intensity Last Year and Change in GHG Intensity) are essentially
          zero. In fact, most of our variables don't seem to have a very strong
          connection to reporting rates. The only variables that seem to explain
          some of the reporting patterns are those related to time (i.e. the
          COVID-19 data disruption) and those related to building type (a couple
          building categories have higher/lower reporting rates than average).
        </p>

        <h2>Conclusion: No pattern found</h2>

        <p>
          After looking at summary statistics and running regression analysis,
          it seems like there is no meaningful relationship between emission
          patterns of buildings and their reporting compliance. This contradicts
          our initial hypothesis that some buildings might withhold data to
          conceal poor emissions performance.
        </p>

        <p>
          This raises a key question: why do buildings choose to report or not?
          At Electrify Chicago, we’ve noticed that few politicians and
          policymakers are even aware of the existence of the Chicago Building
          Benchmarking Data. So, it’s not surprising that we see no pattern—why
          hide emissions if no one is paying attention?
        </p>

        <p>
          Electrify Chicago aims to change that reality by making the building
          benchmarking data more accessible. Still, nearly a third of buildings
          fail to report each year. Understanding why may require further
          quantitative and qualitative analysis.
        </p>

        <h3 class="italic">Explore our Analysis</h3>

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
    font-size: 1.1em;
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
    margin-bottom: 0;
    margin-top: 1rem;
  }

  .graph-caption {
    background-color: $blue-light;
    font-size: 0.7rem;
    border-radius: $brd-rad-small;
    padding: 0.5rem;
  }
  .regression-p {
    margin: 0.5rem 0 1rem 0;
    background-color: $blue-light;
    border-radius: $brd-rad-small;
    padding: 1rem;
    font-size: 0.9rem;
  }

  iframe {
    border: $border-medium solid $black;
    border-radius: 0.5rem;
  }

  .cell-bordered {
    border: solid $border-thin $black;
  }

  .italic {
    font-style: italic; // Corrected from "text: italics"
  }

  section.-indented {
    margin-left: 1rem;
  }

  h3 {
    margin-bottom: 0;

    + p {
      margin-top: 0.25rem;
    }
  }

  /**
   * Mobile Styling
   */
  @media (max-width: $mobile-max-width) {
    // Shrink table font size so it's more visible
    table {
      font-size: 0.75rem;
    }
  }
}
</style>
