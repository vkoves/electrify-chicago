<template>
  <div class="pie-chart-cont">
    <svg :id="idPrefix + '-pie-chart'"><!-- D3 inserts here --></svg>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import * as d3 from 'd3';

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

  /** A unique ID prefix for this pie chart */
  @Prop({ required: true }) idPrefix!: Array<IPieSlice>;

  /** Whether we want to show labels */
  @Prop({ default: true }) showLabels!: boolean;

  @Watch('graphData')
  onDataChanged(): void {
    this.renderGraph();
  }

  width = 400;
  height = 320;

  readonly graphMargins = { top: 0, right: 0, bottom: 0, left: 0 };

  svg!: d3.Selection<SVGGElement, unknown, HTMLElement, null>;

  mounted(): void {
    // If no labels, make the graph square (400x400)
    if (!this.showLabels) {
      this.height = this.width;
    }

    const outerWidth =
      this.width + this.graphMargins.left + this.graphMargins.right;
    const outerHeight =
      this.height + this.graphMargins.top + this.graphMargins.bottom;

    this.svg = d3
      .select(`svg#${this.idPrefix}-pie-chart`)
      .attr('width', outerWidth)
      .attr('height', outerHeight)
      .attr('viewBox', `0 0 ${outerWidth} ${outerHeight}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .append('g')
      .attr('transform', `translate(${this.width / 2},${this.height / 2})`);

    this.renderGraph();
  }

  renderGraph(): void {
    // Empty the SVG
    this.svg.html(null);

    let pieRadius = 100;
    let labelRadius = 150;

    if (!this.showLabels) {
      pieRadius = 200;
    }

    // Compute the position of each group on the pie:
    var pie = d3.pie().value((d: any) => d.value);
    var dataReady = pie(this.graphData as any);

    // shape helper to build arcs:
    var arcGenerator = d3.arc().innerRadius(0).outerRadius(pieRadius);

    var labelArcGenerator = d3
      .arc()
      .innerRadius(pieRadius)
      .outerRadius(labelRadius);

    // Build the pie chart: Basically, each part of the pie is a path that we build using the
    // arc function.
    this.svg
      .selectAll('mySlices')
      .data(dataReady)
      .enter()
      .append('path')
      .attr('d', arcGenerator as any)
      .attr('fill', (d) => (d.data as any as IPieSlice).color);

    // Calculate total value for % calculation
    let totalValue = 0;
    this.graphData.forEach((d) => (totalValue += d.value));

    if (this.showLabels) {
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

  // When printing, scale up text and thicken borders
  @media print {
    svg {
      font-size: 2rem;

      path {
        stroke-width: 0.6125rem;
      }
    }
  }
}
</style>
