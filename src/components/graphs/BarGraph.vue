<template>
  <div class="bar-graph-cont">
    <div class="label" v-html="graphTitle" />

    <svg id="bar-graph"><!-- D3 inserts here --></svg>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import * as d3 from "d3";

export interface IGraphPoint {
  x: number | string;
  y: number;
}

/**
 * A component that can graph an arbitrary array of numeric data
 */
@Component({})
export default class BarGraph extends Vue {
  @Prop({ required: true }) graphTitle!: string;

  @Prop({ required: true }) graphData!: Array<IGraphPoint>;

  @Watch("graphData")
  onDataChanged(): void {
    this.renderGraph();
  }

  readonly width = 800;
  readonly height = 400;

  readonly graphMargins = { top: 30, right: 30, bottom: 50, left: 60 };
  readonly barMargin = 0.2;

  svg!: d3.Selection<SVGGElement, unknown, HTMLElement, any>;

  mounted(): void {
    const outerWidth =
      this.width + this.graphMargins.left + this.graphMargins.right;
    const outerHeight =
      this.height + this.graphMargins.top + this.graphMargins.bottom;

    this.svg = d3
      .select("svg#bar-graph")
      .attr("width", outerWidth)
      .attr("height", outerHeight)
      .attr("viewBox", `0 0 ${outerWidth} ${outerHeight}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .append("g")
      .attr(
        "transform",
        `translate(${this.graphMargins.left},${this.graphMargins.top})`,
      );

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
      .domain([0, d3.max(yVals) as number])
      .rangeRound([this.height, 0]);

    // Render X axis
    this.svg
      .append("g")
      .attr("transform", `translate(0, ${this.height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .attr("transform", "translate(-10,0)rotate(-45)")
      .style("text-anchor", "end");

    // Render Y axis
    this.svg.append("g").call(d3.axisLeft(y));

    this.svg
      .selectAll("mybar")
      .data(this.graphData)
      .enter()
      .append("rect")
      .attr("x", (d) => {
        return x(d.x.toString() as string) as number;
      })
      .attr("y", (d) => y(d.y))
      .attr("width", x.bandwidth())
      .attr("height", (d) => this.height - y(d.y))
      .attr("fill", "#69b3a2");
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
