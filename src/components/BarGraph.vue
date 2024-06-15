<template>
  <div class="bar-graph-cont">
    <div class="label"></div>

    <svg><!-- D3 inserts here --></svg>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import * as d3 from 'd3';

/**
 * A component that can graph an arbitrary array of numeric data
 */
@Component({
  components: {
  },
})
export default class BarGraph extends Vue {
  @Prop({required: true}) data/*!*/: Array<{ x: number | string, y: number }> = [
    { x: 2018, y: 50 },
    { x: 2019, y: 55 },
    { x: 2020, y: 40 },
    { x: 2021, y: 60 },
    { x: 2022, y: 65 },
    { x: 2023, y: 68 },
  ];

  mounted(): void {
    const width = 800;
    const height = 500;

    const margin = {top: 30, right: 30, bottom: 70, left: 60};
    const barMargin = 0.2;

    const outerWidth = width + margin.left + margin.right;
    const outerHeight = height + margin.top + margin.bottom;

    const svg = d3
      .select("svg")
      .attr("width", outerWidth)
      .attr("height", outerHeight)
      .attr("viewBox", `0 0 ${outerWidth} ${outerHeight}`)
      .attr("preserveAspectRatio", "xMidYMid meet")
      .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const g = svg.append("g");

    const xVals: Array<string> = this.data.map((d) => d.x.toString());
    const yVals: Array<number> = this.data.map((d) => d.y);


    const x = d3
      .scaleBand()
      .range([0, width])
      .domain(xVals)
      .padding(barMargin);

    const y = d3
      .scaleLinear()
      .domain([ 0, d3.max(yVals) as number])
      .rangeRound([height, 0]);

    // Render X axis
    svg.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

    // Render Y axis
    svg.append("g")
      .call(d3.axisLeft(y));

    svg.selectAll("mybar")
      .data(this.data)
      .enter()
      .append("rect")
        .attr("x", (d) => {
          return x(d.x.toString() as string) as number;
        })
        .attr("y", (d) => y(d.y))
        .attr("width", x.bandwidth())
        .attr("height", (d) => height - y(d.y))
        .attr("fill", "#69b3a2");
  }
}
</script>

<style lang="scss">
.bar-graph-cont {
  svg {
    width: 100%;
    border: solid $border-thin $grey-light;
    aspect-ratio: 1.5;
    height: auto;
    max-width: 50rem;
  }
}
</style>
