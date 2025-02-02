<template>
  <div id="app" class="pie-chart-cont">
    <svg id="pie-chart"><!-- D3 inserts here --></svg>
    <img
      v-tooltip.bottom="tooltipMessage"
      class="tooltip"
      src="/help.svg"
      alt="Help icon. Hover to reveal additional text."
    >
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import * as d3 from 'd3';
import vToolTip from 'v-tooltip';

export interface IPieSlice {
  value: number;
  label: string;
  color: string;
}

/**
 * A component that can graph an arbitrary array of numeric data as a pie chart
 *
 * E.g. Votes for favorite pies:
 * [ { label: 'Cherry', value: 30 }, { label: 'Chocolate', value: 12 }]
 */
@Component({})
export default class PieChart extends Vue {
  @Prop({ required: true }) graphData!: Array<IPieSlice>;

  @Watch('graphData')
  onDataChanged(): void {
    this.renderGraph();
  }

  readonly width = 400;
  readonly height = 320;

  readonly graphMargins = { top: 0, right: 0, bottom: 0, left: 0 };

  svg!: d3.Selection<SVGGElement, unknown, HTMLElement, any>;
  tooltipMessage = `
    <h6>Why does this matter?</h6>
    <p>
      Although reducing energy use overall is important, not all energy is created equal -
      electricity can be created without emissions (via solar, wind, nuclear, etc.) but burning
      natural gas always creates emissions.
    </p>
  `;

  mounted(): void {
    const outerWidth =
      this.width + this.graphMargins.left + this.graphMargins.right;
    const outerHeight =
      this.height + this.graphMargins.top + this.graphMargins.bottom;

    this.svg = d3
      .select('svg#pie-chart')
      .attr('width', outerWidth)
      .attr('height', outerHeight)
      .attr('viewBox', `0 0 ${outerWidth} ${outerHeight}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .append('g')
      .attr('transform', `translate(${this.width / 2},${this.height / 2})`);

    this.renderGraph();
    this.renderTooltips();
  }

  renderGraph(): void {
    // Empty the SVG
    this.svg.html(null);

    const radius = 100;
    const labelRadius = 150;

    // Compute the position of each group on the pie:
    var pie = d3.pie().value((d: any) => d.value);
    var dataReady = pie(this.graphData as any);

    // shape helper to build arcs:
    var arcGenerator = d3.arc().innerRadius(0).outerRadius(radius);

    var labelArcGenerator = d3
      .arc()
      .innerRadius(radius)
      .outerRadius(labelRadius);

    // Build the pie chart: Basically, each part of the pie is a path that we build using the
    // arc function.
    this.svg
      .selectAll('mySlices')
      .data(dataReady)
      .enter()
      .append('path')
      .attr('d', arcGenerator as any)
      .attr('fill', (d) => (d.data as unknown as IPieSlice).color);

    // Calculate total value for % calculation
    let totalValue = 0;
    this.graphData.forEach((d) => (totalValue += d.value));

    /** Add pie chart labels */
    this.svg
      .selectAll('mySlices')
      .data(dataReady)
      .enter()
      .append('text')
      .html((d) => {
        // Convert degrees to rads
        const thresholdRadians = (5 / 360) * 2 * Math.PI;

        // If we have a lot of small slices, we skip those labels so they don't collide
        if (
          this.graphData.length > 2 &&
          d.endAngle - d.startAngle < thresholdRadians
        ) {
          return '';
        }

        let data = d.data as any as IPieSlice;

        const label =
          `<tspan class="percent">${this.calculatePercentage(
            data.value,
            totalValue,
          )}%</tspan>` +
          `<tspan class="label" x="0" dy="1.5em">${data.label}</tspan>`;

        return label;
      })
      .attr('class', () => (this.graphData.length === 1 ? '-only-slice' : ''))
      .attr('transform', (d) => {
        // If we have only 1 slice (e.g. 100% electric, like Marina Towers), place dead center,
        // otherwise use secondary arc centroid
        if (this.graphData.length === 1) {
          return '';
        }

        return `translate(${labelArcGenerator.centroid(
          d as unknown as d3.DefaultArcObject,
        )})`;
      })
      .style('text-anchor', (d) => {
        // Center single slice label
        if (this.graphData.length === 1) {
          return 'middle';
        }

        // are we past the center?
        return (d.endAngle + d.startAngle) / 2 > Math.PI ? 'end' : 'start';
      });
  }

  renderTooltips(): void {
    Vue.use(vToolTip); // Mounts v-tooltips library
  }

  calculatePercentage(value: number, total: number): string {
    const percentage = (value / total) * 100;

    if (percentage < 1) {
      return '< 1';
    }
    // If > 99%, we don't want to round to 100% so we can show there's other slices
    else if (percentage > 99 && percentage < 100) {
      return Math.floor(percentage).toString();
    } else {
      return Math.round(percentage).toString();
    }
  }
}
</script>

<style lang="scss">
.pie-chart-cont {
  display: flex;
  flex-direction: column;

  svg {
    width: 100%;
    height: auto;
    max-width: 50rem;

    path {
      stroke: $white;
      stroke-width: 0.25rem;
    }

    text.-only-slice {
      font-size: 1.5rem;
    }
  }

  tspan.percent {
    font-weight: bold;
    font-size: 1.3em;
  }
  tspan.label {
    font-size: 0.65em;
  }
}

.tooltip {
  align-self: flex-end;
  z-index: 10000;
  margin: 0rem 2rem 1rem 0rem;

  .tooltip-inner {
    background: $white;
    color: $black;
    border-radius: 4px;
    border: 1px solid $blue-dark;
    box-shadow: 4px 4px 4px $grey;
    padding: 5px 10px 4px;
    width: 22rem;
    padding: 1rem;

    h6 {
      font-size: 1rem;
      color: $blue-dark;
      margin: 0;
      margin-bottom: 0.75rem;
    }
  }

  .tooltip-arrow {
    width: 0;
    height: 0;
    border-style: solid;
    position: absolute;
    margin: 5px;
    border-color: $blue-dark;
    z-index: 1;
  }

  &[x-placement^="top"] {
    margin-bottom: 5px;

    .tooltip-arrow {
      border-width: 5px 5px 0 5px;
      border-left-color: transparent !important;
      border-right-color: transparent !important;
      border-bottom-color: transparent !important;
      bottom: -5px;
      left: calc(50% - 5px);
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  &[x-placement^="bottom"] {
    margin-top: 5px;

    .tooltip-arrow {
      border-width: 0 5px 5px 5px;
      border-left-color: transparent !important;
      border-right-color: transparent !important;
      border-top-color: transparent !important;
      top: -5px;
      left: calc(50% - 5px);
      margin-top: 0;
      margin-bottom: 0;
    }
  }

  &[x-placement^="right"] {
    margin-left: 5px;

    .tooltip-arrow {
      border-width: 5px 5px 5px 0;
      border-left-color: transparent !important;
      border-top-color: transparent !important;
      border-bottom-color: transparent !important;
      left: -5px;
      top: calc(50% - 5px);
      margin-left: 0;
      margin-right: 0;
    }
  }

  &[x-placement^="left"] {
    margin-right: 5px;

    .tooltip-arrow {
      border-width: 5px 0 5px 5px;
      border-top-color: transparent !important;
      border-right-color: transparent !important;
      border-bottom-color: transparent !important;
      right: -5px;
      top: calc(50% - 5px);
      margin-left: 0;
      margin-right: 0;
    }
  }

  &.popover {
    $color: #f9f9f9;

    .popover-inner {
      background: $color;
      color: black;
      padding: 24px;
      border-radius: 5px;
      box-shadow: 0 5px 30px rgba(black, .1);
    }

    .popover-arrow {
      border-color: $color;
    }
  }

  &[aria-hidden='true'] {
    visibility: hidden;
    opacity: 0;
    transition: opacity .15s, visibility .15s;
  }

  &[aria-hidden='false'] {
    visibility: visible;
    opacity: 1;
    transition: opacity .15s;
  }
}
</style>
