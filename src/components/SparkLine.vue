<template>
  <div
    :id="svgContPrefix + randomId"
    class="spark-graph-cont"
  >
    <svg :id="svgIdPrefix + randomId"><!-- D3 inserts here --></svg>
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

  /** A unit to append to the min and max values (e.g. "tons") */
  @Prop({required: true}) unit?: string;

  readonly svgIdPrefix = 'spark-svg-';
  readonly svgContPrefix = 'spark-cont-';

  /* Strip HTML from the unit (just <sub> for CO2) and simplify by dropping 'metric' */
  get unitCleaned(): string {
    if (!this.unit) { return ''; }

    return this.unit
      .replace('<sub>', '<tspan class="sub" dy="0.5em">')
      .replace('</sub>', '</tspan><tspan dy="-0.5rem">')
      .replace('metric', '');
  }

  minAndMaxPoints?: Array<INumGraphPoint>;

  @Watch('graphData')
  onDataChanged(): void {
    this.renderGraph();
  }

  /** Underlying SVG size */
  readonly width = 320;
  readonly height = 60;

  /** The radius, in pixels, of the min and max dots and all the points on focus */
  readonly DotRadius = 8;

  /** The font-size of the label, in the <svg>'s internal space (so scaled as the SVG is scaled)' */
  readonly LabelFontSize = 28;

  // The amount to shift the x-axis down by
  readonly xAxisOffset = 60;

  readonly graphMargins = { top: 50, right: 15, bottom: 110, left: 15 };
  readonly barMargin = 0.2;

  randomId = Math.round(Math.random() * 1000);

  tooltip?: d3.Selection<HTMLDivElement, unknown, HTMLElement, any>;

  svg!: d3.Selection<SVGGElement, unknown, HTMLElement, any>;

  mounted(): void {
    const outerWidth = this.width + this.graphMargins.left + this.graphMargins.right;
    const outerHeight = this.height + this.graphMargins.top + this.graphMargins.bottom;

    this.svg = d3
      .select(`svg#${this.svgIdPrefix}${this.randomId}`)
      .attr("width", outerWidth)
      .attr("height", outerHeight)
      .attr("viewBox", `0 0 ${outerWidth} ${outerHeight}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .append("g")
        .attr("transform", `translate(${this.graphMargins.left},${this.graphMargins.top})`);

    this.calculateMinAndMaxPoints();
    this.setupTooltip();
    this.renderGraph();
  }

  /**
   * Get the global min and max points, which we show on the graph with their values to act as a
   * replacement for the y-axis
   */
   calculateMinAndMaxPoints(): void {
    const yVals: Array<number> = this.graphData.map((d) => d.y);
    const minAndMaxPoints: Array<INumGraphPoint> = [];

    const minPoint = this.graphData.find((datum) => datum.y === d3.min(yVals));
    const maxPoint = this.graphData.find((datum) => datum.y === d3.max(yVals));

    if (minPoint) {
      minAndMaxPoints.push(minPoint);
    }

    if (maxPoint) {
      minAndMaxPoints.push(maxPoint);
    }

    this.minAndMaxPoints = minAndMaxPoints;
  }

  renderGraph(): void {
    // Empty the SVG
    this.svg.html(null);

    // TODO: Fix passed years being strings and remove this conversion
    this.graphData.forEach((point: INumGraphPoint) => point.x = parseInt(point.x.toString()));

    const xVals: Array<number> = this.graphData.map((d) => d.x);
    const yVals: Array<number> = this.graphData.map((d) => d.y);

    const minYear = d3.min(xVals)!;
    const maxYear = d3.max(xVals)!;

    const x = d3
      .scaleLinear()
      .range([0, this.width])
      .domain(d3.extent(xVals) as [number, number]);

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
          .tickSizeOuter(0), // make the x-axis a flat line, with no tick marks at the ends
      )
      .selectAll("text")
        .attr("text-anchor", (d) =>  d === maxYear ? 'end' : 'start')
        // shift label a bit further from the axis line
        .attr("dy", "0.85em");

    // Render Y axis
    this.svg.append("g")
      .attr('class', 'y-axis')
      .call(
        d3.axisLeft(y)
          .tickValues(d3.extent(yVals) as [number, number]),
    );

    // Add the line
    this.svg.append("path")
      .datum(this.graphData)
      .attr("fill", "none")
      .attr("stroke", "black")
      .attr("stroke-width", 8)
      .attr("d", (d3.line() as any)
        .x((d: INumGraphPoint) => x(d.x))
        .y((d: INumGraphPoint) => y(d.y)),
        );

    if (this.minAndMaxPoints) {
      // Add all valid points, we'll then use CSS to hide all but the min and max unless hovered
      this.svg
        .append("g")
        .selectAll("dot")
        .data(this.graphData.filter((d) => !isNaN(d.y)))
        .enter()
        .append("circle")
          .attr('class', (d) => {
            const isMinMax = d.x === this.minAndMaxPoints![0].x
              || d.x === this.minAndMaxPoints![1].x;

            return isMinMax ? 'dot -min-max' : 'dot';
          })
          .attr("cx", (d) => x(d.x))
          .attr("cy", (d) => y(d.y))
          .attr("r", this.DotRadius)
          .attr("fill", "black")
          .attr('tabindex', '0')
          .on("mouseover", this.mouseover.bind(this))
          .on("focusin", (event: Event, d) => this.focus(event, d))
          .on("blur", this.mouseleave.bind(this))
          .on("mousemove", (event: MouseEvent, d) => this.mousemove(event, d))
          .on("mouseleave", this.mouseleave.bind(this));

      // Add the value labels for the min and max points
      this.svg
        .append("g")
        .selectAll("pointLabels")
        .data(this.minAndMaxPoints)
        .enter()
        .append("text")
          .attr("cx", (d) => x(d.x))
          .attr("cy", (d) => y(d.y))
          // Put the text at the position of the last point
          .attr("transform", (d) => {
            let xPos = x(d.x);
            let yPos = y(d.y);

            // The min point should have its label below
            if (d.x === this.minAndMaxPoints![0].x) {
              yPos += this.LabelFontSize * 1.5;

              return `translate(${xPos},${yPos})`;
            }
            // The max point has its label above
            else {
              yPos -= this.LabelFontSize * 0.5;

              return `translate(${xPos},${yPos})`;
            }
          })
          .attr("text-anchor", (d) => {
            // Points near the right edge of the graph should have text going left from the point,
            // otherwise go right (e.g. first year)
            // e.g. we have data from 2020 to 2024, the 3/4 year is 2023
            // (2020 + (0.75 * (2024 - 2020))
            const threeQuartersYear = Math.ceil(minYear + (0.75 * (maxYear - minYear)));
            const halfwayYear = Math.ceil(minYear + (0.5 * (maxYear - minYear)));

            // If the min point is more than 3/4 along in the graph, it's near enough to the end
            // that we align text to the left of the dot, otherwise to the start
            if (d.x >= threeQuartersYear) {
              return 'end';
            }
            // If it's say 2/3 along the graph, it may still hit the right edge, so center
            else if (d.x > halfwayYear) {
              return 'middle';
            }
            else {
              return 'start';
            }
          })
          .html((d) => `<tspan class="bold">${d.y.toLocaleString()}</tspan>`)
          .style("fill", "black")
          .style("font-size", this.LabelFontSize);
    }
  }

  /** Create the empty tooltip element we fill later */
  setupTooltip(): void {
    // create a tooltip
    this.tooltip = d3.select(`#${this.svgContPrefix}${this.randomId}`)
      .append("div")
        .style("opacity", 0)
        .attr("class", "tooltip");
  }

  focus(event: Event, datum: INumGraphPoint): void {
    this.mouseover();
    this.mousemove(event as MouseEvent, datum);
  }

  mouseover(): void {
    this.tooltip?.style("opacity", 1);
  }

  mousemove(event: Event, datum: INumGraphPoint): void {
    // Calculate a scale factor to match the internal SVG space to the rendered HTML space
    const outerWidth = this.width + this.graphMargins.left + this.graphMargins.right;
    const svgElem = document.getElementById(`${this.svgIdPrefix}${this.randomId}`);
    const scaleFactor = svgElem!.clientWidth / outerWidth;

    const tooltipX = d3.pointer(event)[0] * scaleFactor + 20;
    const tooltipY = d3.pointer(event)[1] * scaleFactor;

    this.tooltip!
      .html(
        `<div class="year">${datum.x}</div>` +
        `<div class="value-cont">` +
          `<span class="value">${datum.y.toLocaleString()}</span> ` +
          `<span class="unit">${this.unit}</span>` +
        `</div>`,
      )
      .style("left", `${tooltipX}px`)
      .style("top", `${tooltipY}px`);
    }

  mouseleave(): void {
    this.tooltip?.style("opacity", 0);
  }
}
</script>

<style lang="scss">
.spark-graph-cont {
  position: relative;

  .label {
    font-weight: bold;
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
  }

  .tooltip {
    position: absolute;
    background-color: $off-white;
    border: solid $border-medium $black;
    border-radius: $brd-rad-small;
    padding: 0.5rem 1rem;
    width: 10rem;
    pointer-events: none; // prevent interfering with hover
    transition: opacity 0.3s;
    font-size: 0.825rem;
    line-height: 1.25;

    .value {
      font-weight: bold;
      font-size: 1rem;
    }
    .unit { white-space: nowrap; }
    .year {
      font-weight: bold;
      margin-bottom: 0.25rem;
    }
  }

  svg {
    width: 100%;
    height: auto;
    max-width: 20rem; // 320px

    &:hover, &:focus-within {
      // Show all dots and make them thicker using a stroke
      circle.dot {
        opacity: 1;
        stroke-width: 0.5rem;
        stroke: $black;
      }
    }

    .dot {
      transition: opacity 0.3s, stroke-width 0.3s;

      // Hide all dots except the min max until hovered to keep the graph simple
      &:not(.-min-max) { opacity: 0; }
    }
    tspan.bold { font-weight: bold; }
    tspan.sub { font-size: 0.75em; }
  }

  // Hide tick lines on x-axis
  .tick line { display: none; }

  .x-axis .tick {
    font-size: 1.6rem;
    font-weight: normal
  }

  // Hide y-axis via CSS, we label points instead
  .y-axis { display: none; }
}
</style>
