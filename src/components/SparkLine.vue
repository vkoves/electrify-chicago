<template>
  <div class="bar-graph-cont">
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

export interface IGraphPoint {
  x: number | string;
  y: number;
}

/**
 * A component that can graph an arbitrary array of numeric data as a spark line, a simple line
 * graph (like might be used in a news chevron for a stock)
 */
@Component({})
export default class BarGraph extends Vue {
  @Prop({required: true}) graphTitle!: string;

  @Prop({required: true}) graphData!: Array<IGraphPoint>;

  @Watch('graphData')
  onDataChanged(): void {
    this.renderGraph();
  }

  readonly width = 800;
  readonly height = 400;

  readonly graphMargins = { top: 30, right: 30, bottom: 50, left: 60 };
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

    const xVals: Array<string> = this.graphData.map((d) => d.x.toString());
    const yVals: Array<number> = this.graphData.map((d) => d.y);

    const x = d3
      .scaleBand()
      .range([0, this.width])
      .domain(xVals)
      .padding(this.barMargin);

    const y = d3
      .scaleLinear()
      .domain([ d3.min(yVals) as number, d3.max(yVals) as number])
      .rangeRound([this.height, 0]);

    // Render X axis
    this.svg.append("g")
      .attr("transform", `translate(0, ${this.height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

    // Render Y axis
    this.svg.append("g")
      .call(d3.axisLeft(y));

    // Add the line
    this.svg.append("path")
      .datum(this.graphData)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 10)
      .attr("d", (d3.line() as any)
        .x((d: IGraphPoint) => { return x(d.x.toString()) })
        .y((d: IGraphPoint) => { return y(d.y) })
        )
  }
}
</script>

<style lang="scss">
.bar-graph-cont {
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
    max-width: 50rem;
  }

  .tick {
    font-weight: bold;
    font-size: 1rem;
  }
}
</style>
