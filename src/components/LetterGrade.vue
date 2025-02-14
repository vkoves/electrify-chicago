<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

/**
 * A component that shows a letter grade
 */
@Component({
  filters: {
    lowercase(value: string) {
      return value.toLowerCase();
    },
  },
})
export default class LetterGrade extends Vue {
  @Prop({ required: true }) grade!: string;
}
</script>
<template>
  <span class="grade-letter" :class="`-${grade}` | lowercase">
    {{ grade }}
  </span>
</template>
<style lang="scss">
</style>
