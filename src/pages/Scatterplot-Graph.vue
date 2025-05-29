<template>
  <DefaultLayout>
    <h1 id="main-content" tabindex="-1">Release Notes</h1>
    <div id="my_dataviz"></div>
  </DefaultLayout>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import * as d3 from 'd3';
import NewTabIcon from '~/components/NewTabIcon.vue';

interface DataPoint {
  year: number;
  value: number;
}

@Component({
  components: {
    NewTabIcon,
  },
})
export default class ScatterplotGraph extends Vue {
  mounted() {
    const margin = { top: 10, right: 30, bottom: 30, left: 60 };
    const width = 500 - margin.left - margin.right;
    const height = 440 - margin.top - margin.bottom;

    const emissionsData: DataPoint[] = [
      { year: 2010, value: 8140.71 },
      { year: 2011, value: 8338.42 },
      { year: 2012, value: 8371.15 },
      { year: 2013, value: 8285.96 },
      { year: 2014, value: 8197.8 },
      { year: 2015, value: 8298.69 },
      { year: 2016, value: 8880.23 },
      { year: 2017, value: 8997.57 },
      { year: 2018, value: 9001.64 },
      { year: 2019, value: 10000 },
    ];

    const svg = d3
      .select('#my_dataviz')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)

      // <g> is the <svg> without the margins - so the margin is the space in between the <svg> and the <g>
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // extent() -- returns the minimum and maximum values in an array from the given array.
    // in this case, the first and last year (2010, 2019)
    // Domain is the input. Range is the output. This is one way to do it.

    // I want a line - so grab scaleLinear
    // what do I want to put on the line? My emissions values. So chuck that into the domain.
    // how do I want to spread this data across my line? Put that distance into the range.
    // naturally, you'll likely always keep this [height, 0] and [0, width] situation
    const topAndBottomEmissionsValues = d3.extent(
      emissionsData,
      (d: DataPoint) => d.value,
    ) as [number, number];
    const yAxisLinearlyScaledLineWeMade = d3
      .scaleLinear()
      .domain(topAndBottomEmissionsValues)
      .range([height, 0]);

    // or you can see here, it's less explicit but shorter code
    const topAndBottomYears = d3.extent(
      emissionsData,
      (d: DataPoint) => d.year,
    ) as [number, number];
    const xAxisLinearlyScaledLineWeMade = d3.scaleLinear(topAndBottomYears, [
      0,
      width,
    ]);

    // the x axis <g>
    svg
      .append('g')
      .attr('transform', `translate(0,${height})`)
      .call(
        // remember the x axis we made? It's time to put it somewhere! But where do we put it?..
        //.. at the bottom of course (thats what axiBottom does)
        d3
          .axisBottom(xAxisLinearlyScaledLineWeMade) // draws the x line axis at the bottom
          .tickFormat(d3.format('d')), // format the tick labels as regular integers
      );

    // the y axis <g>
    // axisLeft draws the leftAxis
    svg.append('g').call(d3.axisLeft(yAxisLinearlyScaledLineWeMade));

    // now we're putting the line on here
    svg
      .append('path')
      .datum(emissionsData) // binds the whole array to only the single element <path>
      .attr('fill', 'none')
      .attr('stroke', '#69b3a2')
      .attr('stroke-width', 2)

      // this is the crazy letters and numbers that you always see in the <path> of svgs
      .attr(
        'd',
        d3
          .line<DataPoint>()
          .x((d: DataPoint) => xAxisLinearlyScaledLineWeMade(d.year))
          .y((d: DataPoint) => yAxisLinearlyScaledLineWeMade(d.value)),
      );

    const tooltip = d3
      .select('#my_dataviz')
      .append('div')
      .style('opacity', 0)
      .attr('class', 'tooltip')
      .style('border', 'solid')
      .style('border-width', '1px')
      .style('border-radiux', '5px')
      .style('padding', '10px');

    // a function that changes this tooltip when the user hovers over a point.
    // Its opacity is set to 1: we can now see it. Plus it sets the text and
    // position of the tooltip depending on the datapoint (d)

    const mouseover = (event: MouseEvent, d: DataPoint) => {
      tooltip.style('opacity', 1);
    };

    const mouseMove = function (event: MouseEvent, d: DataPoint) {
      const [x, y] = d3.pointer(event);
      tooltip
        .html(d.year + ' Annual Emissions: ' + d.value)
        .style('position', 'absolute')
        .style('background-color', 'white')
        .style('pointer-events', 'auto')
        .style('left', `${x + 80}px`)
        .style('top', `${y + 140}px`)
        .style('position', 'absolute');
    };

    const mouseleave = (d: DataPoint) => {
      tooltip
        .transition()
        .duration(200)
        .style('opacity', 0)
        .style('pointer-events', 'none');
    };

    // render circles
    svg
      .append('g')
      .selectAll('circle') // Try to select existing <circle> elements
      .data(emissionsData) // Bind your data array
      .enter() // For each data item that doesn't have a matching <circle>...
      .append('circle') // ...create one!
      .attr('cx', (d: DataPoint) => xAxisLinearlyScaledLineWeMade(d.year)) // the center point of the x axis of the circle
      .attr('cy', (d: DataPoint) => yAxisLinearlyScaledLineWeMade(d.value)) // the center point of the y axis of the circle
      .attr('r', 9)
      .attr('fill', '#69b3a2')
      .on('mouseover', mouseover)
      .on('mousemove', mouseMove)
      .on('mouseout', mouseleave);
  }
}
</script>

<style lang="scss" scoped>
#my_dataviz {
  margin-top: 2rem;
}
</style>
