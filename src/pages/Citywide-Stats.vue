<template>
  <DefaultLayout>
    <h1 id="main-content" tabindex="-1">Citywide Stats</h1>
    <!-- <p class="constrained">
      Electrify Chicago is an independent open-source project looking to
      shed light onto one of the biggest sources of Chicago's CO<sub
        >2</sub
      >
      emissions - buildings. By providing more information about some of
      the city's largest and most polluting buildings, we hope to
      encourage these buildings to electrify, particularly by mobilizing
      people related to the building - whether that be students and
      faculty for a college building or employees and patients at a
      hospital.
    </p> -->
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

      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const topAndBottomEmissionsValues = d3.extent(
      emissionsData,
      (d: DataPoint) => d.value,
    ) as [number, number];
    const yAxisLinearlyScaledLineWeMade = d3
      .scaleLinear()
      .domain(topAndBottomEmissionsValues)
      .range([height, 0]);

    const topAndBottomYears = d3.extent(
      emissionsData,
      (d: DataPoint) => d.year,
    ) as [number, number];
    const xAxisLinearlyScaledLineWeMade = d3.scaleLinear(topAndBottomYears, [
      0,
      width,
    ]);

    svg
      .append('g')
      .attr('transform', `translate(0,${height})`)
      .call(
        d3
          .axisBottom(xAxisLinearlyScaledLineWeMade) 
          .tickFormat(d3.format('d')), 
      );

    svg.append('g').call(d3.axisLeft(yAxisLinearlyScaledLineWeMade));

    svg
      .append('path')
      .datum(emissionsData) 
      .attr('fill', 'none')
      .attr('stroke', '#69b3a2')
      .attr('stroke-width', 2)

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

    svg
      .append('g')
      .selectAll('circle') 
      .data(emissionsData) 
      .enter() 
      .append('circle') 
      .attr('cx', (d: DataPoint) => xAxisLinearlyScaledLineWeMade(d.year)) 
      .attr('cy', (d: DataPoint) => yAxisLinearlyScaledLineWeMade(d.value)) 
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
