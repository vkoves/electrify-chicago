<template>
  <div :id="containerId" ref="chartContainer" class="scatterplot-container">
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch, computed } from 'vue';
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

const props = withDefaults(
  defineProps<{
    data: DataPoint[];
    yAxisLabel: string;
    color?: string;
    containerId: string;
    title: string;
    showGrid: boolean;
    showTrendLine?: boolean;
    animationDuration?: number;
  }>(),
  {
    color: '#3B82F6',
    showGrid: true,
    showTrendLine: true,
    animationDuration: 800,
  },
);

const tooltipAnimationDuration = 300;
const chartContainer = ref<HTMLElement | null>(null);
const loading = ref(true);
const hasAnimated = ref(false);
const chartRendered = ref(false);
let xScale: d3.ScaleLinear<number, number> = d3.scaleLinear().range([0, 0]);
let yScale: d3.ScaleLinear<number, number> = d3.scaleLinear().range([0, 0]);

// Store references to chart elements for later animation
let chartElements: ChartElements | null = null;

const sortedData = computed(() => {
  return [...props.data].sort((a, b) => a.year - b.year);
});

const renderChartStructure = (): void => {
  if (!chartContainer.value || !sortedData.value.length) return;

  // Grab Height and Width from the DOM
  const container = d3.select(chartContainer.value);
  const containerWidth = parseInt(container.style('width'), 10) || 500;
  const containerHeight = 400;

  // Customize SVG widths and heights
  const margin = { top: 50, right: 40, bottom: 60, left: 80 };
  const width = containerWidth - margin.left - margin.right;
  const height = containerHeight - margin.top - margin.bottom;

  // avoid duplicate charts
  container.selectAll('svg').remove();

  // Create and Style SVG
  const svg = container
    .append('svg')
    .attr('viewBox', `0 0 ${containerWidth} ${containerHeight}`)
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
    .text(props.title);

  // Scales
  xScale = d3
    .scaleLinear()
    .domain(
      d3.extent(sortedData.value, (d: DataPoint) => d.year) as [number, number],
    )
    .range([0, width]);

  const yExtent = d3.extent(sortedData.value, (d: DataPoint) => d.value) as [
    number,
    number,
  ];
  const yPadding = (yExtent[1] - yExtent[0]) * 0.1;
  yScale = d3
    .scaleLinear()
    .domain([Math.max(0, yExtent[0] - yPadding), yExtent[1] + yPadding])
    .range([height, 0]);

  // Grid
  const gridGroup = chartGroup.append('g').attr('class', 'grid');

  gridGroup
    .selectAll('.grid-line-horizontal')
    .data(yScale.ticks(6))
    .enter()
    .append('line')
    .attr('class', 'grid-line-horizontal')
    .attr('x1', 0)
    .attr('x2', width)
    .attr('y1', (d) => yScale(d))
    .attr('y2', (d) => yScale(d))
    .style('stroke', '#e2e8f0')
    .style('stroke-width', 1)
    .style('opacity', 0.5);

  gridGroup
    .selectAll('.grid-line-vertical')
    .data(xScale.ticks(Math.min(8, sortedData.value.length)))
    .enter()
    .append('line')
    .attr('class', 'grid-line-vertical')
    .attr('x1', (d) => xScale(d))
    .attr('x2', (d) => xScale(d))
    .attr('y1', 0)
    .attr('y2', height)
    .style('stroke', '#e2e8f0')
    .style('stroke-width', 1)
    .style('opacity', 0.5);

  // Axes
  chartGroup
    .append('g')
    .attr('class', 'x-axis')
    .attr('transform', `translate(0,${height})`)
    .call(
      d3
        .axisBottom(xScale)
        .tickValues(sortedData.value.map((d) => d.year))
        .tickFormat((d) => {
          return containerWidth < 400 ? `'${String(d).slice(2)}` : String(d);
        })
        .tickSize(-10),
    );

  chartGroup
    .append('g')
    .attr('class', 'y-axis')
    .call(d3.axisLeft(yScale).tickFormat(d3.format('.2s')).tickSize(-10));

  // Style axes
  svg
    .selectAll('.x-axis, .y-axis')
    .selectAll('path, line')
    .style('stroke', '#64748b')
    .style('stroke-width', 2);

  svg
    .selectAll('.x-axis, .y-axis')
    .selectAll('text')
    .style('fill', '#475569')
    .style('font-size', '12px');

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
    .style('fill', '#374151')
    .text(props.yAxisLabel);

  chartGroup
    .append('text')
    .attr('transform', `translate(${width / 2}, ${height + 45})`)
    .style('text-anchor', 'middle')
    .style('font-size', '14px')
    .style('font-weight', '600')
    .style('fill', '#374151')
    .text('Year');

  // Create tooltip (but don't show it yet)
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

  // Prepare data elements (but don't show them yet)
  const line = d3
    .line<DataPoint>()
    .x((d: DataPoint) => xScale(d.year))
    .y((d: DataPoint) => yScale(d.value))
    .curve(d3.curveMonotoneX);

  // Create path but make it invisible
  const path = chartGroup
    .append('path')
    .datum(sortedData.value)
    .attr('class', 'line')
    .attr('fill', 'none')
    .attr('stroke', props.color)
    .attr('stroke-width', 3)
    .attr('d', line)
    .style('filter', 'drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1))')
    .style('opacity', 0); // Start invisible

  // Create trend line but make it invisible
  let trendLine = null;
  if (props.showTrendLine && sortedData.value.length > 1) {
    const regression = calculateLinearRegression(sortedData.value);
    trendLine = chartGroup
      .append('line')
      .attr('x1', xScale(regression.x1))
      .attr('x2', xScale(regression.x2))
      .attr('y1', yScale(regression.y1))
      .attr('y2', yScale(regression.y2))
      .style('stroke', '#8b5cf6')
      .style('stroke-width', 3)
      .style('stroke-dasharray', '20,5')
      .style('opacity', 0); // Start invisible
  }

  // Create circles but make them invisible
  const circles = chartGroup
    .append('g')
    .selectAll('circle')
    .data(sortedData.value)
    .enter()
    .append('circle')
    .attr('cx', (d: DataPoint) => xScale(d.year))
    .attr('cy', (d: DataPoint) => yScale(d.value))
    .attr('r', 0) // Start with 0 radius
    .attr('fill', props.color)
    .style('cursor', 'pointer')
    .style('opacity', 0) // Start invisible
    .on('mouseover', function () {
      if (hasAnimated.value) {
        // Only show tooltip after animation
        tooltip.style('opacity', 1);
        d3.select(this)
          .transition()
          .duration(tooltipAnimationDuration)
          .attr('r', 8);
      }
    })
    .on('mousemove', function (event, d) {
      if (hasAnimated.value) {
        const [x, y] = d3.pointer(event, container.node());
        tooltip
          .html(
            `
            <div style="color: #1e293b; font-weight: 600; margin-bottom: 4px;">
              Year: ${d.year}
            </div>
            <div style="color: ${props.color}; font-weight: 600;">
              ${props.yAxisLabel}: ${d.value.toLocaleString()}
            </div>
          `,
          )
          .style('left', `${x + 15}px`)
          .style('top', `${y - 10}px`);
      }
    })
    .on('mouseout', function () {
      if (hasAnimated.value) {
        tooltip
          .transition()
          .duration(tooltipAnimationDuration)
          .style('opacity', 0);
        d3.select(this)
          .transition()
          .duration(tooltipAnimationDuration)
          .attr('r', 6);
      }
    });

  if (props.showTrendLine && sortedData.value.length > 1) {
    const regression = calculateLinearRegression(sortedData.value);
    trendLine = chartGroup
      .append('line')
      .attr('x1', xScale(regression.x1))
      .attr('y1', yScale(regression.y1))
      // Start collapsed at (x1, y1)
      .attr('x2', xScale(regression.x1))
      .attr('y2', yScale(regression.y1))
      .style('stroke', '#8b5cf6')
      .style('stroke-width', 3)
      .style('stroke-dasharray', '20,5')
      .style('opacity', 0); // Start invisible
  }

  // Store references for later animation
  chartElements = {
    container,
    chartGroup,
    tooltip,
    circles,
    path,
    trendLine,
  };

  loading.value = false;
  chartRendered.value = true;
};

const animateDataElements = (): void => {
  if (!chartElements || hasAnimated.value) return;

  const { circles, path, trendLine } = chartElements;

  // Animate the line
  const totalLength = path.node()?.getTotalLength() || 0;
  path
    .attr('stroke-dasharray', totalLength + ' ' + totalLength)
    .attr('stroke-dashoffset', totalLength)
    .style('opacity', 1)
    .transition()
    .duration(props.animationDuration)
    .ease(d3.easeLinear)
    .attr('stroke-dashoffset', 0);

  // Animate circles
  circles
    .style('opacity', 1)
    .transition()
    .duration(props.animationDuration)
    .delay((d: DataPoint, i: number) => i * 100)
    .attr('r', 6)
    .ease(d3.easeBackOut);

  // Animate trend line
  if (trendLine) {
    const regression = calculateLinearRegression(sortedData.value);
    trendLine
      .style('opacity', 0.7)
      .transition()
      .duration(props.animationDuration)
      .delay(props.animationDuration * 0.2)
      .ease(d3.easeQuadOut)
      .attr('x2', xScale(regression.x2))
      .attr('y2', yScale(regression.y2));
  }

  hasAnimated.value = true;
};

const calculateLinearRegression = (data: DataPoint[]): RegressionLine => {
  const n = data.length;
  const sumX = data.reduce((sum, d) => sum + d.year, 0);
  const sumY = data.reduce((sum, d) => sum + d.value, 0);
  const sumXY = data.reduce((sum, d) => sum + d.year * d.value, 0);
  const sumXX = data.reduce((sum, d) => sum + d.year * d.year, 0);

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
};

let intersectionObserver: IntersectionObserver | undefined;

onMounted(() => {
  // Render chart structure immediately
  renderChartStructure();

  // Set up intersection observer for data animation
  intersectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (
          entry.isIntersecting &&
          !hasAnimated.value &&
          entry.intersectionRatio >= 0.5 &&
          chartRendered.value
        ) {
          console.log('Animating chart data for:', props.containerId);
          animateDataElements();
        }
      });
    },
    {
      threshold: 0.5,
    },
  );

  requestAnimationFrame(() => {
    if (intersectionObserver && chartContainer.value) {
      intersectionObserver.observe(chartContainer.value);
    }
  });
});

onBeforeUnmount(() => {
  if (intersectionObserver && chartContainer.value) {
    intersectionObserver.unobserve(chartContainer.value);
    intersectionObserver.disconnect();
  }
});

watch(
  () => props.data,
  () => {
    loading.value = true;
    hasAnimated.value = false;
    chartRendered.value = false;
    renderChartStructure();
    animateDataElements();
  },
  { deep: true },
);
</script>

<style scoped>
.scatterplot-container {
  width: 100%;
  position: relative;
}

@media screen and (min-width: 500px) {
  .scatterplot-container {
    max-width: 62.5rem;
  }
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
