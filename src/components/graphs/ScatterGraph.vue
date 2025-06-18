<template>
  <div :id="containerId" ref="chartContainer" class="scatterplot-container" />
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount, ref, watch } from 'vue'
import * as d3 from 'd3'

export interface DataPoint {
  year: number
  value: number
}

const props = defineProps<{
  data: DataPoint[]
  yAxisLabel: string
  color: string
  containerId: string
}>()

const chartContainer = ref<HTMLElement | null>(null)
let resizeObserver: ResizeObserver | undefined

const renderScatterplot = () => {
  if (!chartContainer.value) return

  const container = d3.select(chartContainer.value)
  const containerWidth = parseInt(container.style('width'), 10) || 500
  const containerHeight = 300

  const margin = { top: 10, right: 30, bottom: 40, left: 80 }
  const width = containerWidth - margin.left - margin.right
  const height = containerHeight - margin.top - margin.bottom

  container.selectAll('*').remove()

  const svg = container
    .append('svg')
    .attr('width', '100%')
    .attr('height', containerHeight)
    .attr('viewBox', `0 0 ${containerWidth} ${containerHeight}`)
    .attr('preserveAspectRatio', 'xMidYMid meet')
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`)

  const xScale = d3
    .scaleLinear()
    .domain(d3.extent(props.data, (d) => d.year) as [number, number])
    .range([0, width])

  const yScale = d3
    .scaleLinear()
    .domain(d3.extent(props.data, (d) => d.value) as [number, number])
    .range([height, 0])

  svg.append('g')
    .attr('transform', `translate(0,${height})`)
    .call(d3.axisBottom(xScale).tickFormat(d3.format('d')))

  svg.append('g').call(d3.axisLeft(yScale))

  svg.append('text')
    .attr('transform', 'rotate(-90)')
    .attr('y', 0 - margin.left)
    .attr('x', 0 - height / 2)
    .attr('dy', '1em')
    .style('text-anchor', 'middle')
    .style('font-size', '12px')
    .text(props.yAxisLabel)

  svg.append('path')
    .datum(props.data)
    .attr('fill', 'none')
    .attr('stroke', props.color)
    .attr('stroke-width', 2)
    .attr('d', d3.line<DataPoint>()
      .x((d) => xScale(d.year))
      .y((d) => yScale(d.value))
    )

  const tooltip = container
    .append('div')
    .style('opacity', 0)
    .attr('class', 'tooltip')
    .style('position', 'absolute')
    .style('background-color', 'white')
    .style('border', '1px solid #ccc')
    .style('border-radius', '5px')
    .style('padding', '10px')
    .style('pointer-events', 'none')

  const mouseover = () => {
    tooltip.style('opacity', 1)
  }

  const mousemove = (event: MouseEvent, d: DataPoint) => {
    const [x, y] = d3.pointer(event, container.node())
    tooltip
      .html(`${d.year}: ${d.value.toLocaleString()}`)
      .style('left', `${x + 10}px`)
      .style('top', `${y + 10}px`)
  }

  const mouseleave = () => {
    tooltip.transition().duration(200).style('opacity', 0)
  }

  svg.append('g')
    .selectAll('circle')
    .data(props.data)
    .enter()
    .append('circle')
    .attr('cx', (d) => xScale(d.year))
    .attr('cy', (d) => yScale(d.value))
    .attr('r', 6)
    .attr('fill', props.color)
    .on('mouseover', mouseover)
    .on('mousemove', mousemove)
    .on('mouseout', mouseleave)
}

onMounted(() => {
  renderScatterplot()

  if (chartContainer.value) {
    resizeObserver = new ResizeObserver(() => {
      renderScatterplot()
    })
    resizeObserver.observe(chartContainer.value)
  }
})

onBeforeUnmount(() => {
  if (resizeObserver && chartContainer.value) {
    resizeObserver.unobserve(chartContainer.value)
  }
})

watch(() => props.data, () => {
  renderScatterplot()
}, { deep: true })
</script>

<style scoped>
.scatterplot-container {
  width: 100%;
  position: relative;
}
.tooltip {
  font-size: 12px;
}
</style>
