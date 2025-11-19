<template>
  <div :id="containerId" ref="chartContainer" class="scatterplot-container">
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Watch } from 'vue-property-decorator';
import * as d3 from 'd3';
import { DataPoint, RegressionLine } from '../../common-functions.vue';

interface ChartElements {
  container: d3.Selection<HTMLElement, unknown, null, undefined>;
  chartGroup: d3.Selection<SVGGElement, unknown, null, undefined>;
  tooltip: d3.Selection<HTMLDivElement, unknown, null, undefined>;
  circles: d3.Selection<SVGCircleElement, DataPoint, SVGGElement, unknown>;
  path: d3.Selection<SVGPathElement, DataPoint[], null, undefined>;
  trendLine: d3.Selection<SVGLineElement, unknown, null, undefined> | null;
}

/**
 * TODOS For Future:
 *
 *  - Add doc block to this component, including an example perhaps
 *  - Migrate duplicate CSS to styling
 *  - Ensure all colors come from colors.scss
 *  - Avoid magic numbers
 *  - Make tooltips consistent with SparkGraph, and ideally consolidate functionality
 */
@Component
export default class ScatterPlot extends Vue {
  $refs!: {
    chartContainer: HTMLElement;
  };
  @Prop({ required: true }) data!: DataPoint[];
  @Prop({ required: true }) yAxisLabel!: string;
  @Prop({ required: true }) strokeColor!: string;
  @Prop({ required: true }) fillColor!: string;
  @Prop({ required: true }) containerId!: string;
  @Prop({ required: true }) title!: string;

  @Prop({ default: true }) showGrid!: boolean;
  @Prop({ default: true }) showTrendLine!: boolean;
  @Prop({ default: 800 }) animationDuration!: number;

  private chartContainer: HTMLElement | null = null;
  private loading: boolean = true;
  private hasAnimated: boolean = false;
  private chartRendered: boolean = false;
  private xScale: d3.ScaleLinear<number, number> = d3.scaleLinear();
  private yScale: d3.ScaleLinear<number, number> = d3.scaleLinear();
  private chartElements: ChartElements | null = null;
  private intersectionObserver: IntersectionObserver | undefined;

  // Tooltip positioning constants
  private readonly TooltipOffset = 15; // Distance from cursor to tooltip
  private readonly TooltipEstimatedWidth = 150; // Estimated tooltip width for positioning
  private readonly TooltipEdgeBuffer = 30; // Buffer from container edge

  get sortedData(): DataPoint[] {
    return [...this.data].sort((a, b) => a.year - b.year);
  }

  mounted(): void {
    this.chartContainer = this.$refs.chartContainer as HTMLElement;
    this.renderChartStructure();
    this.setupIntersectionObserver();
  }

  beforeDestroy(): void {
    if (this.intersectionObserver && this.chartContainer) {
      this.intersectionObserver.unobserve(this.chartContainer);
      this.intersectionObserver.disconnect();
    }
  }

  @Watch('data', { deep: true })
  onDataChange(): void {
    this.loading = true;
    this.hasAnimated = false;
    this.chartRendered = false;
    this.renderChartStructure();
    this.animateDataElements();
  }

  private setupIntersectionObserver(): void {
    if (!this.chartContainer) return;

    const threshold = 0.5;
    this.intersectionObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (
            entry.isIntersecting &&
            !this.hasAnimated &&
            entry.intersectionRatio >= threshold &&
            this.chartRendered
          ) {
            this.animateDataElements();
          }
        });
      },
      { threshold },
    );

    requestAnimationFrame(() => {
      if (this.intersectionObserver && this.chartContainer) {
        this.intersectionObserver.observe(this.chartContainer);
      }
    });
  }

  // TODO: Break apart this massive function
  private renderChartStructure(): void {
    if (!this.chartContainer || !this.sortedData.length) return;

    const container = d3.select(this.chartContainer);
    const containerWidth = parseInt(container.style('width'), 10) || 500;
    const containerHeight = 400;
    const margin = { top: 50, right: 40, bottom: 60, left: 80 };
    const width = containerWidth - margin.left - margin.right;
    const height = containerHeight - margin.top - margin.bottom;

    container.selectAll('svg').remove();

    const svg = container
      .append('svg')
      .attr('viewBox', `0 0 ${containerWidth} ${containerHeight}`)
      // TODO: Move to CSS standardize
      .style('background', 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)')
      .style('box-shadow', '0 4px 20px rgba(0, 0, 0, 0.1)');

    const chartGroup = svg
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Title
    svg
      .append('text')
      .attr('x', containerWidth / 2)
      .attr('y', 30)
      .attr('text-anchor', 'middle')
      .style('font-size', '18px')
      .style('font-weight', '600')
      .style('fill', '#1e293b')
      .text(this.title);

    // Scales
    this.xScale = d3
      .scaleLinear()
      .domain(
        d3.extent(this.sortedData, (d: DataPoint) => d.year) as [
          number,
          number,
        ],
      )
      .range([0, width]);

    const yExtent = d3.extent(this.sortedData, (d: DataPoint) => d.value) as [
      number,
      number,
    ];
    const yPaddingTop = yExtent[1] * 0.5; // 10% padding above max

    this.yScale = d3
      .scaleLinear()
      .domain([0, yExtent[1] + yPaddingTop]) // always start at 0
      .range([height, 0]);

    // Grid
    if (this.showGrid) {
      const gridGroup = chartGroup.append('g').attr('class', 'grid');

      gridGroup
        .selectAll('.grid-line-horizontal')
        .data(this.yScale.ticks(6))
        .enter()
        .append('line')
        .attr('x1', 0)
        .attr('x2', width)
        .attr('y1', (d: number) => this.yScale(d))
        .attr('y2', (d: number) => this.yScale(d))
        .style('stroke', '#e2e8f0')
        .style('stroke-width', 1)
        .style('opacity', 0.5);

      gridGroup
        .selectAll('.grid-line-vertical')
        .data(this.xScale.ticks(Math.min(8, this.sortedData.length)))
        .enter()
        .append('line')
        .attr('x1', (d: number) => this.xScale(d))
        .attr('x2', (d: number) => this.xScale(d))
        .attr('y1', 0)
        .attr('y2', height)
        .style('stroke', '#e2e8f0')
        .style('stroke-width', 1)
        .style('opacity', 0.5);
    }

    // Axes
    chartGroup
      .append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0,${height})`)
      .call(
        d3
          .axisBottom(this.xScale)
          .tickValues(this.sortedData.map((d: DataPoint) => d.year))
          .tickFormat((d: d3.NumberValue) => String(d.valueOf()))
          .tickSize(-10),
      );

    chartGroup
      .append('g')
      .attr('class', 'y-axis')
      .call(
        d3
          .axisLeft(this.yScale)
          .tickSize(-10)
          .tickFormat((d: d3.NumberValue) =>
            +d === 0 ? '' : d3.format('~s')(d),
          ),
      );

    // Axis labels
    chartGroup
      .append('text')
      .attr('transform', 'rotate(-90)')
      .attr('y', 0 - margin.left)
      .attr('x', 0 - height / 2)
      .attr('dy', '2.5em')
      .style('text-anchor', 'middle')
      .style('font-size', '14px')
      .style('font-weight', '600')
      .style('fill', 'black')
      .text(this.yAxisLabel);

    chartGroup
      .append('text')
      .attr('transform', `translate(${width / 2}, ${height + 45})`)
      .style('text-anchor', 'middle')
      .style('font-size', '14px')
      .style('font-weight', '600')
      .style('fill', 'black')
      .text('Year');

    // Trend line (drawn first to appear behind data)
    let trendLine: d3.Selection<
      SVGLineElement,
      unknown,
      null,
      undefined
    > | null = null;

    if (this.showTrendLine && this.sortedData.length > 1) {
      const regression = this.calculateLinearRegression(this.sortedData);
      trendLine = chartGroup
        .append('line')
        .attr('x1', this.xScale(regression.x1))
        .attr('y1', this.yScale(regression.y1))
        .attr('x2', this.xScale(regression.x1)) // collapsed start
        .attr('y2', this.yScale(regression.y1))
        .style('stroke', '#8b5cf6')
        .style('stroke-width', 3)
        .style('stroke-dasharray', '20,5')
        .style('opacity', 0);
    }

    // Tooltip
    const tooltip = container
      .append('div')
      .style('opacity', 0)
      .style('position', 'absolute')
      .style('background', 'rgba(255, 255, 255, 0.95)')
      .style('backdrop-filter', 'blur(10px)')
      .style('border', '1px solid #e2e8f0')
      .style('border-radius', '8px')
      .style('padding', '12px')
      .style('pointer-events', 'none')
      .style('font-size', '13px')
      .style('font-weight', '500')
      .style('box-shadow', '0 4px 20px rgba(0, 0, 0, 0.15)')
      .style('z-index', '1000');

    // Line
    const line = d3
      .line<DataPoint>()
      .x((d: DataPoint) => this.xScale(d.year))
      .y((d: DataPoint) => this.yScale(d.value))
      .curve(d3.curveMonotoneX);

    const path = chartGroup
      .append('path')
      .datum(this.sortedData)
      .attr('fill', 'none')
      .attr('class', this.strokeColor)
      .attr('stroke-width', 3)
      .attr('d', line)
      .style('filter', 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1))')
      .style('opacity', 0);

    // Circles
    const circles = chartGroup
      .append('g')
      .selectAll('circle')
      .data(this.sortedData)
      .enter()
      .append('circle')
      .attr('cx', (d: DataPoint) => this.xScale(d.year))
      .attr('cy', (d: DataPoint) => this.yScale(d.value))
      .attr('r', 0)
      .attr('class', this.fillColor)
      .style('cursor', 'pointer')
      .style('opacity', 0)
      .on('mouseover', function () {
        tooltip.style('opacity', 1);
      })
      .on('mousemove', (event: MouseEvent, d: DataPoint) => {
        const [x, y] = d3.pointer(event, container.node());
        const containerWidth = parseInt(container.style('width'), 10) || 500;

        // Check if tooltip would extend beyond right edge of container
        const shouldLeftAlign =
          x + this.TooltipEstimatedWidth >
          containerWidth - this.TooltipEdgeBuffer;

        tooltip
          .html(
            `<div>Year: ${d.year}</div><div>${this.yAxisLabel}: ${d.value}</div>`,
          )
          .style(
            'left',
            shouldLeftAlign
              ? `${x - this.TooltipEstimatedWidth - this.TooltipOffset}px`
              : `${x + this.TooltipOffset}px`,
          )
          .style('top', `${y - this.TooltipOffset}px`);
      })
      .on('mouseout', function () {
        tooltip.style('opacity', 0);
      });

    this.chartElements = {
      container,
      chartGroup,
      tooltip,
      circles,
      path,
      trendLine,
    };

    this.loading = false;
    this.chartRendered = true;
  }

  private animateDataElements(): void {
    if (!this.chartElements || this.hasAnimated) return;
    const { circles, path } = this.chartElements;

    if (this.chartElements.trendLine) {
      const regression = this.calculateLinearRegression(this.sortedData);
      this.chartElements.trendLine
        .style('opacity', 0.7)
        .transition()
        .duration(this.animationDuration)
        .delay(this.animationDuration * 0.2)
        .ease(d3.easeQuadOut)
        .attr('x2', this.xScale(regression.x2))
        .attr('y2', this.yScale(regression.y2));
    }

    // Animate line
    const totalLength = path.node()?.getTotalLength() || 0;
    path
      .attr('stroke-dasharray', `${totalLength} ${totalLength}`)
      .attr('stroke-dashoffset', totalLength)
      .style('opacity', 1)
      .transition()
      .duration(this.animationDuration)
      .ease(d3.easeLinear)
      .attr('stroke-dashoffset', 0);

    // Animate circles
    circles
      .style('opacity', 1)
      .transition()
      .duration(this.animationDuration)
      .delay((d: DataPoint, i: number) => i * 100)
      .attr('r', 6)
      .ease(d3.easeBackOut);

    this.hasAnimated = true;
  }

  private calculateLinearRegression(data: DataPoint[]): RegressionLine {
    const n = data.length;
    const sumX = data.reduce((s, d) => s + d.year, 0);
    const sumY = data.reduce((s, d) => s + d.value, 0);
    const sumXY = data.reduce((s, d) => s + d.year * d.value, 0);
    const sumXX = data.reduce((s, d) => s + d.year * d.year, 0);

    const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    const intercept = (sumY - slope * sumX) / n;

    const xMin = Math.min(...data.map((d) => d.year));
    const xMax = Math.max(...data.map((d) => d.year));

    return {
      x1: xMin,
      y1: slope * xMin + intercept,
      x2: xMax,
      y2: slope * xMax + intercept,
    };
  }
}
</script>

<style scoped>
.scatterplot-container {
  position: relative;
  display: grid;
  width: 100%;
  margin: auto 0;
  padding: 0 1rem;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  z-index: 1000;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@media (max-width: 768px) {
  .scatterplot-container {
    font-size: 12px;
  }
}
</style>
