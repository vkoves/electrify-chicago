<template>
  <div class="spark-graph-cont">
    <div
      class="label"
      v-html="graphTitle"
    />

    <svg :id="'spark' + randomId"><!-- D3 inserts here --></svg>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import * as d3 from 'd3';

export interface INumGraphPoint {
  x: number;
  y: number;
}

/**
 * A component that can graph an arbitrary array of numeric data as a spark line, a simple line
 * graph (like might be used in a news chevron for a stock)
 */
@Component({})
export default class BarGraph extends Vue {
  @Prop({required: true}) graphTitle!: string;

  @Prop({required: true}) graphData!: Array<INumGraphPoint>;

  @Watch('graphData')
  onDataChanged(): void {
    this.renderGraph();
  }

  /** Underlying size */
  readonly width = 400;
  readonly height = 150;

  // The amount to shift the x-axis down by
  readonly xAxisOffset = 20;

  readonly graphMargins = { top: 30, right: 0, bottom: 80, left: 60 };
  readonly barMargin = 0.2;

  randomId = Math.round(Math.random() * 1000);

  svg!: d3.Selection<SVGGElement, unknown, HTMLElement, any>;

  mounted(): void {
    const outerWidth = this.width + this.graphMargins.left + this.graphMargins.right;
    const outerHeight = this.height + this.graphMargins.top + this.graphMargins.bottom;

    this.svg = d3
      .select("svg#spark" + this.randomId)
      .attr("width", outerWidth)
      .attr("height", outerHeight)
      .attr("viewBox", `0 0 ${outerWidth} ${outerHeight}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .append("g")
        .attr("transform", `translate(${this.graphMargins.left},${this.graphMargins.top})`);

    this.renderGraph();
  }

  renderGraph(): void {
    // Empty the SVG
    this.svg.html(null);

    // TODO: Fix passed years being strings and remove this conversion
    this.graphData.forEach((point: INumGraphPoint) => point.x = parseInt(point.x.toString()));

    const xVals: Array<number> = this.graphData.map((d) => d.x);
    const yVals: Array<number> = this.graphData.map((d) => d.y);

    const x = d3
      .scaleLinear()
      .range([0, this.width])
      .domain(d3.extent(xVals) as [number, number])

    const y = d3
      .scaleLinear()
      .domain([ d3.min(yVals) as number, d3.max(yVals) as number])
      .rangeRound([this.height, 0]);

    // Render X axis
    this.svg.append("g")
      .attr('class', 'x-axis')
      .attr("transform", `translate(0, ${this.height + this.xAxisOffset})`)
      .call(
        d3.axisBottom(x)
          .tickFormat(d3.format('d'))
          // For spark line, only show first and last year (e.g. 2018 and 2022)
          .tickValues(d3.extent(xVals) as [number, number])
      )
      .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

    // Render Y axis
    this.svg.append("g")
      .attr('class', 'y-axis')
      .call(
        d3.axisLeft(y)
          .tickValues(d3.extent(yVals) as [number, number])
    );

    // Add the line
    this.svg.append("path")
      .datum(this.graphData)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 10)
      .attr("d", (d3.line() as any)
        .x((d: INumGraphPoint) => { return x(d.x as number) })
        .y((d: INumGraphPoint) => { return y(d.y) })
        )
  }
}
</script>

<style lang="scss">
.spark-graph-cont {
  margin: 1rem 0;

  .label {
    font-weight: bold;
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
  }

  svg {
    width: 100%;
    border: solid $border-thin $grey-light;
    aspect-ratio: 2;
    height: auto;
    max-width: 20rem; // 320px
  }

  .tick {
    font-weight: bold;
    font-size: 1.25rem;
  }

  // Hide tick lines on x-axis
  .tick line { display: none; }

  // Hide main y-axis line
  .y-axis .domain { display: none; }
}
</style>
