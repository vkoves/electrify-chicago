import * as d3 from 'd3';

export interface DataPoint {
  year: number;
  value: number;
}

export interface GraphConfig {
  data: DataPoint[];
  containerId: string;
  yAxisLabel: string;
  color: string;
}

export function renderScatterplot(config: GraphConfig): void {
  const container = d3.select(`#${config.containerId}`);
  const containerWidth = parseInt(container.style('width'), 10) || 500;
  const containerHeight = 300;

  const margin = { top: 10, right: 30, bottom: 40, left: 80 };
  const width = containerWidth - margin.left - margin.right;
  const height = containerHeight - margin.top - margin.bottom;

  // Clear previous content
  container.selectAll("*").remove();

  // Create SVG with responsive viewBox
  const svg = container
    .append('svg')
    .attr('width', '100%')
    .attr('height', containerHeight)
    .attr('viewBox', `0 0 ${containerWidth} ${containerHeight}`)
    .attr('preserveAspectRatio', 'xMidYMid meet')
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  // Scales
  const xScale = d3.scaleLinear()
    .domain(d3.extent(config.data, (d: DataPoint) => d.year) as [number, number])
    .range([0, width]);

  const yScale = d3.scaleLinear()
    .domain(d3.extent(config.data, (d: DataPoint) => d.value) as [number, number])
    .range([height, 0]);

  // Axes
  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(xScale).tickFormat(d3.format('d')));

  svg.append('g')
    .call(d3.axisLeft(yScale));

  // Y axis label
  svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 0 - margin.left)
    .attr("x", 0 - height / 2)
    .attr("dy", "1em")
    .style("text-anchor", "middle")
    .style("font-size", "12px")
    .text(config.yAxisLabel);

  // Line path
  svg.append('path')
    .datum(config.data)
    .attr('fill', 'none')
    .attr('stroke', config.color)
    .attr('stroke-width', 2)
    .attr(
      'd',
      d3.line<DataPoint>()
        .x((d: DataPoint) => xScale(d.year))
        .y((d: DataPoint) => yScale(d.value))
    );

  // Tooltip div (absolute, outside svg)
  const tooltip = container
    .append('div')
    .style('opacity', 0)
    .attr('class', 'tooltip')
    .style('position', 'absolute')
    .style('background-color', 'white')
    .style('border', 'solid 1px #ccc')
    .style('border-radius', '5px')
    .style('padding', '10px')
    .style('pointer-events', 'none');

  // Tooltip event handlers
  const mouseover = (_event: MouseEvent, _d: DataPoint) => {
    tooltip.style('opacity', 1);
  };

  const mousemove = (event: MouseEvent, d: DataPoint) => {
    const [x, y] = d3.pointer(event, container.node());
    tooltip
      .html(`${d.year}: ${d.value.toLocaleString()}`)
      .style('left', `${x + 10}px`)
      .style('top', `${y + 10}px`);
  };

  const mouseleave = () => {
    tooltip.transition().duration(200).style('opacity', 0);
  };

  // Draw circles and bind tooltip events
  svg.append('g')
    .selectAll('circle')
    .data(config.data)
    .enter()
    .append('circle')
    .attr('cx', (d: DataPoint) => xScale(d.year))
    .attr('cy', (d: DataPoint) => yScale(d.value))
    .attr('r', 6)
    .attr('fill', config.color)
    .on('mouseover', mouseover)
    .on('mousemove', mousemove)
    .on('mouseout', mouseleave);
}
