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
import { DataPoint, DataSeries, RegressionLine } from '../../common-functions.vue';

interface SeriesElements {
  circles: d3.Selection<SVGCircleElement, DataPoint, SVGGElement, unknown>;
  path: d3.Selection<SVGPathElement, DataPoint[], null, undefined>;
  trendLine: d3.Selection<SVGLineElement, unknown, null, undefined> | null;
}

interface ChartElements {
  container: d3.Selection<HTMLElement, unknown, null, undefined>;
  chartGroup: d3.Selection<SVGGElement, unknown, null, undefined>;
  tooltip: d3.Selection<HTMLDivElement, unknown, null, undefined>;
  seriesElements: SeriesElements[];
}

/**
 * ScatterGraph - A flexible D3-based scatter plot component with line graphs
 *
 * TODOS For Future:
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

  // Legacy single-series props (for backward compatibility)
  /** Single data series (use `series` prop for multiple lines) */
  @Prop() data?: DataPoint[];
  /** CSS class for line stroke color (e.g., 'chart-stroke-blue') */
  @Prop() strokeColor?: string;
  /** CSS class for data point fill color (e.g., 'chart-fill-blue') */
  @Prop() fillColor?: string;

  // New multi-series prop
  /** Array of data series for multi-line charts with legend support */
  @Prop() series?: DataSeries[];

  // Common props
  /** Label displayed on the y-axis */
  @Prop({ required: true }) yAxisLabel!: string;
  /** Unique ID for the chart container (must be unique across page) */
  @Prop({ required: true }) containerId!: string;
  /** Chart title displayed at the top */
  @Prop({ required: true }) title!: string;

  /** Show horizontal and vertical grid lines */
  @Prop({ default: true }) showGrid!: boolean;
  /** Show linear regression trend line for each series */
  @Prop({ default: true }) showTrendLine!: boolean;
  /** Duration of chart animations in milliseconds */
  @Prop({ default: 800 }) animationDuration!: number;
  /** Show color-coded legend (useful for multi-series charts) */
  @Prop({ default: false }) showLegend!: boolean;
  /** Hide data point circles, showing only lines */
  @Prop({ default: false }) hidePoints!: boolean;
  /** Custom formatter function for y-axis tick values */
  @Prop() yAxisFormatter?: (value: number) => string;

  /**
   * Y-axis padding as a fraction of the maximum value.
   * Controls how much extra space appears above the highest data point.
   *
   * @example
   * 0.1 = 10% padding (default, tight spacing for efficient use of space)
   * 0.5 = 50% padding (more spacious, better for sparse data)
   */
  @Prop({ default: 0.1 }) yAxisPadding!: number;

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

  // Computed properties for handling both single and multi-series modes
  get dataSeries(): DataSeries[] {
    if (this.series && this.series.length > 0) {
      return this.series;
    }
    // Backward compatibility: convert old single-series props to new format
    if (this.data && this.strokeColor && this.fillColor) {
      return [
        {
          name: this.title,
          data: this.data,
          strokeColor: this.strokeColor,
          fillColor: this.fillColor,
        },
      ];
    }
    return [];
  }

  get allDataPoints(): DataPoint[] {
    return this.dataSeries.flatMap((s) => s.data);
  }

  get sortedData(): DataPoint[] {
    return [...this.allDataPoints].sort((a, b) => a.year - b.year);
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

  @Watch('series', { deep: true })
  onSeriesChange(): void {
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
    // Add extra right margin when showing legend with multiple series
    const rightMargin =
      this.showLegend && this.dataSeries.length > 1 ? 150 : 40;
    const margin = { top: 50, right: rightMargin, bottom: 60, left: 80 };
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
    const yPaddingTop = yExtent[1] * this.yAxisPadding;

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
    const years = [...new Set(this.sortedData.map((d: DataPoint) => d.year))];
    const yearRange = years[years.length - 1] - years[0];
    // Show ~8-10 ticks for readability
    const tickInterval = yearRange > 50 ? 10 : yearRange > 20 ? 5 : 1;
    const tickYears = years.filter((year) => year % tickInterval === 0);

    chartGroup
      .append('g')
      .attr('class', 'x-axis')
      .attr('transform', `translate(0,${height})`)
      .call(
        d3
          .axisBottom(this.xScale)
          .tickValues(tickYears)
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
          .tickFormat((d: d3.NumberValue) => {
            const value = +d;
            if (value === 0) return '';
            if (this.yAxisFormatter) {
              return this.yAxisFormatter(value);
            }
            // Default: use regular decimal notation
            return value.toLocaleString();
          }),
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

    // Legend
    if (this.showLegend && this.dataSeries.length > 1) {
      const legendX = width + margin.left + 10;
      const legendGroup = svg
        .append('g')
        .attr('transform', `translate(${legendX}, ${margin.top})`);

      this.dataSeries.forEach((series, i) => {
        const legendItem = legendGroup
          .append('g')
          .attr('transform', `translate(0, ${i * 25})`);

        legendItem
          .append('line')
          .attr('x1', 0)
          .attr('x2', 20)
          .attr('y1', 10)
          .attr('y2', 10)
          .attr('class', series.strokeColor)
          .attr('stroke-width', 3);

        legendItem
          .append('circle')
          .attr('cx', 10)
          .attr('cy', 10)
          .attr('r', 4)
          .attr('class', series.fillColor);

        legendItem
          .append('text')
          .attr('x', 30)
          .attr('y', 10)
          .attr('dy', '0.35em')
          .style('font-size', '12px')
          .text(series.name);
      });
    }

    // Render each data series
    const seriesElements: SeriesElements[] = [];
    const line = d3
      .line<DataPoint>()
      .x((d: DataPoint) => this.xScale(d.year))
      .y((d: DataPoint) => this.yScale(d.value))
      .curve(d3.curveMonotoneX);

    this.dataSeries.forEach((series) => {
      const sortedSeriesData = [...series.data].sort((a, b) => a.year - b.year);

      // Trend line (drawn first to appear behind data)
      let trendLine: d3.Selection<
        SVGLineElement,
        unknown,
        null,
        undefined
      > | null = null;

      if (this.showTrendLine && sortedSeriesData.length > 1) {
        const regression = this.calculateLinearRegression(sortedSeriesData);
        trendLine = chartGroup
          .append('line')
          .attr('x1', this.xScale(regression.x1))
          .attr('y1', this.yScale(regression.y1))
          .attr('x2', this.xScale(regression.x1)) // collapsed start
          .attr('y2', this.yScale(regression.y1))
          .style('stroke', '#8b5cf6')
          .style('stroke-width', 2)
          .style('stroke-dasharray', '5,5')
          .style('opacity', 0);
      }

      // Line
      const path = chartGroup
        .append('path')
        .datum(sortedSeriesData)
        .attr('fill', 'none')
        .attr('class', series.strokeColor)
        .attr('stroke-width', 3)
        .attr('d', line)
        .style('filter', 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1))')
        .style('opacity', 0);

      // Circles (optional based on hidePoints prop)
      const circlesGroup = chartGroup.append('g');
      const circles = circlesGroup
        .selectAll('circle')
        .data(this.hidePoints ? [] : sortedSeriesData)
        .enter()
        .append('circle')
        .attr('cx', (d: DataPoint) => this.xScale(d.year))
        .attr('cy', (d: DataPoint) => this.yScale(d.value))
        .attr('r', 0)
        .attr('class', series.fillColor)
        .style('cursor', 'pointer')
        .style('opacity', 0)
        .on('mouseover', function () {
          tooltip.style('opacity', 1);
        })
        .on('mousemove', (event: MouseEvent, d: DataPoint) => {
          const [x, y] = d3.pointer(event, container.node());
          const containerWidth = parseInt(container.style('width'), 10) || 500;

          const shouldLeftAlign =
            x + this.TooltipEstimatedWidth >
            containerWidth - this.TooltipEdgeBuffer;

          const tooltipContent = `<div><strong>${series.name}</strong></div><div>Year: ${d.year}</div><div>${this.yAxisLabel}: ${d.value}</div>`;
          tooltip
            .html(tooltipContent)
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

      seriesElements.push({ circles, path, trendLine });
    });

    this.chartElements = {
      container,
      chartGroup,
      tooltip,
      seriesElements,
    };

    this.loading = false;
    this.chartRendered = true;
  }

  private animateDataElements(): void {
    if (!this.chartElements || this.hasAnimated) return;

    this.chartElements.seriesElements.forEach((seriesElement, seriesIndex) => {
      const { circles, path, trendLine } = seriesElement;
      const seriesData = this.dataSeries[seriesIndex].data;
      const sortedSeriesData = [...seriesData].sort((a, b) => a.year - b.year);

      if (trendLine) {
        const regression = this.calculateLinearRegression(sortedSeriesData);
        trendLine
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

      // Animate circles (will be empty if hidePoints is true)
      circles
        .style('opacity', 1)
        .transition()
        .duration(this.animationDuration)
        .delay((_d: DataPoint, i: number) => i * 100)
        .attr('r', 6)
        .ease(d3.easeBackOut);
    });

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
