<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

import BuildingImage from '~/components/BuildingImage.vue';
import { IBuilding } from '../common-functions.vue';
import { generatePageMeta } from '../constants/meta-helpers.vue';

interface QuizPair {
  /** Label describing what the buildings have in common */
  category: string;
  /** Explainer shown after the user picks */
  explainer: string;
  /** Index into the buildings array for building A */
  buildingAIndex: number;
  /** Index into the buildings array for building B */
  buildingBIndex: number;
}

/**
 * Note: @Component<any> is required for metaInfo to work with TypeScript
 * This is a known limitation of vue-property-decorator + vue-meta integration
 * See: https://github.com/xerebede/gridsome-starter-typescript/issues/37
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
@Component<any>({
  components: {
    BuildingImage,
  },
  metaInfo() {
    return generatePageMeta(
      'Which Building Is Greener?',
      'Test your knowledge! Guess which famous Chicago building has lower ' +
        'greenhouse gas emissions intensity in this interactive quiz.',
    );
  },
})
export default class Quiz extends Vue {
  quizStarted = false;
  currentRound = 0;
  selectedBuildingId: string | number | null = null;
  score = 0;
  quizComplete = false;

  /**
   * Maps building IDs from the static query to array indices for easy lookup.
   * Order matches the static-query result sorted by ID ASC:
   * 0: 100429 (Hancock), 1: 101567 (Monadnock), 2: 101713 (Aon Center),
   * 3: 102460 (MSI), 4: 103606 (Willis), 5: 103638 (Field Museum),
   * 6: 231019 (Aqua), 7: 239096 (Marina Towers)
   */
  readonly quizPairs: QuizPair[] = [
    {
      category: 'Loop Office Buildings',
      explainer:
        'The Monadnock Building has less than half the Aon Center\'s greenhouse gas ' +
        'intensity, despite being nearly 90 years older! The Monadnock\'s 6-foot-thick ' +
        'brick walls act as incredible insulation, making its efficiency surprisingly good.',
      buildingAIndex: 2, // Aon Center (GHG 5.9)
      buildingBIndex: 1, // Monadnock (GHG 2.6)
    },
    {
      category: 'Residential Towers',
      explainer:
        'Marina Towers edges out the much newer Aqua despite being built nearly 50 years ' +
        "earlier. Both are efficient for residential buildings, but Marina Towers' compact " +
        'design gives it a slight advantage.',
      buildingAIndex: 7, // Marina Towers (GHG 5.3)
      buildingBIndex: 6, // Aqua (GHG 5.8)
    },
    {
      category: 'Iconic Skyscrapers',
      explainer:
        'The Hancock Center has significantly lower greenhouse gas intensity than Willis ' +
        "Tower, despite both being massive 1970s skyscrapers. Willis Tower's enormous " +
        'floor area makes efficiency a bigger challenge.',
      buildingAIndex: 4, // Willis Tower (GHG 13.9)
      buildingBIndex: 0, // Hancock (GHG 10.0)
    },
    {
      category: 'Chicago Museums',
      explainer:
        'The Museum of Science and Industry has less than half the greenhouse gas ' +
        'intensity of the Field Museum, despite similar square footage. Museum climate ' +
        'control needs can vary a lot based on collections and building design.',
      buildingAIndex: 3, // MSI (GHG 4.9)
      buildingBIndex: 5, // Field Museum (GHG 11.3)
    },
  ];

  get buildings(): IBuilding[] {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return (this as any).$static.allBuilding.edges.map(
      (edge: { node: IBuilding }) => edge.node,
    );
  }

  readonly galleryRows: string[][] = [
    [
      'willis-tower.webp',
      'art-institute.webp',
      'marina-towers.webp',
      'field-museum.webp',
      'merchandise-mart.webp',
      'navy-pier.webp',
    ],
    [
      'john-hancock.webp',
      'aon-center.webp',
      'aqua.webp',
      'shedd-aquarium.webp',
      'museum-of-science-and-industry.webp',
      'chicago-theatre.webp',
    ],
    [
      'monadnock-building.webp',
      'tribune-tower.webp',
      'mccormick-place.webp',
      'wrigley-building.webp',
      'thompson-center.webp',
      'aon-center.webp',
    ],
  ];

  get currentPair(): QuizPair {
    return this.quizPairs[this.currentRound];
  }

  get buildingA(): IBuilding {
    return this.buildings[this.currentPair.buildingAIndex];
  }

  get buildingB(): IBuilding {
    return this.buildings[this.currentPair.buildingBIndex];
  }

  /** The building with lower GHG intensity wins */
  get winnerId(): string | number {
    return this.buildingA.GHGIntensity <= this.buildingB.GHGIntensity
      ? this.buildingA.ID
      : this.buildingB.ID;
  }

  get hasSelected(): boolean {
    return this.selectedBuildingId !== null;
  }

  get isCorrect(): boolean {
    return String(this.selectedBuildingId) === String(this.winnerId);
  }

  startQuiz(): void {
    this.quizStarted = true;
  }

  formatNumber(value: number): string {
    if (!value) return '—';
    return Math.round(value).toLocaleString();
  }

  selectBuilding(buildingId: string | number): void {
    if (this.hasSelected) return;

    this.selectedBuildingId = buildingId;

    if (String(buildingId) === String(this.winnerId)) {
      this.score++;
    }
  }

  nextRound(): void {
    if (this.currentRound < this.quizPairs.length - 1) {
      this.currentRound++;
      this.selectedBuildingId = null;
    } else {
      this.quizComplete = true;
    }
  }

  playAgain(): void {
    this.currentRound = 0;
    this.selectedBuildingId = null;
    this.score = 0;
    this.quizComplete = false;
    this.quizStarted = true;
  }

  getCardClass(building: IBuilding): Record<string, boolean> {
    return {
      'quiz-card': true,
      '-winner':
        this.hasSelected && String(building.ID) === String(this.winnerId),
      '-loser':
        this.hasSelected && String(building.ID) !== String(this.winnerId),
    };
  }
}
</script>

<static-query>
  query {
    allBuilding(
      filter: {
        DataYear: { eq: "2023" },
        ID: { in: ["100429", "101567", "101713", "102460", "103606", "103638", "231019", "239096"] }
      },
      sortBy: "ID", order: ASC
    ) {
      edges {
        node {
          slugSource
          ID
          DataYear
          PropertyName
          Address
          path
          PrimaryPropertyType
          GrossFloorArea
          YearBuilt
          GHGIntensity
          TotalGHGEmissions
          GHGIntensityLetterGrade
        }
      }
    }
  }
</static-query>

<template>
  <DefaultLayout main-class="layout -full-width">
    <!-- Intro screen - full viewport -->
    <div v-if="!quizStarted" class="quiz-intro">
      <div class="gallery" aria-hidden="true">
        <div
          v-for="(row, rowIndex) in galleryRows"
          :key="rowIndex"
          class="gallery-track"
          :class="{ '-reverse': rowIndex % 2 === 1 }"
        >
          <img
            v-for="img in row"
            :key="'a-' + img"
            :src="'/building-imgs/' + img"
            alt=""
          />
          <img
            v-for="img in row"
            :key="'b-' + img"
            :src="'/building-imgs/' + img"
            alt=""
          />
        </div>
      </div>

      <div class="intro-overlay">
        <div class="intro-inner">
          <h1 id="main-content" tabindex="-1">Which Building Is Greener?</h1>

          <p>
            We'll show you pairs of famous Chicago buildings. Your job: guess
            which one has <strong>lower greenhouse gas intensity</strong> (less
            CO<sub>2</sub> per square foot).
          </p>

          <p>{{ quizPairs.length }} rounds. Can you get them all right?</p>

          <button class="action-btn start-btn" @click="startQuiz">
            Start Quiz
          </button>
        </div>
      </div>
    </div>

    <div class="quiz-page page-constrained">
      <!-- Quiz round -->
      <div v-if="quizStarted && !quizComplete">
        <h1 id="main-content" tabindex="-1" class="sr-only">
          Which Building Is Greener?
        </h1>

        <div class="round-header">
          <p class="round-indicator">
            Round {{ currentRound + 1 }}/{{ quizPairs.length }}
          </p>
          <p class="round-category">{{ currentPair.category }}</p>
        </div>

        <p class="quiz-prompt">
          Which building emits less CO<sub>2</sub> per square foot?
        </p>

        <div class="quiz-pair">
          <div
            v-for="building in [buildingA, buildingB]"
            :key="building.ID"
            :class="getCardClass(building)"
          >
            <BuildingImage :building="building" :hide-attribution="true" />

            <h2 class="building-name">{{ building.PropertyName }}</h2>

            <ul class="building-stats">
              <li>{{ building.PrimaryPropertyType }}</li>
              <li>Built {{ Math.round(building.YearBuilt) }}</li>
              <li>{{ formatNumber(building.GrossFloorArea) }} sq ft</li>
            </ul>

            <button
              v-if="!hasSelected"
              class="action-btn pick-btn"
              @click="selectBuilding(building.ID)"
            >
              Pick
            </button>

            <div v-if="hasSelected" class="result-stats">
              <p class="ghg-value">
                {{ building.GHGIntensity }}
                <span class="ghg-unit">kg CO<sub>2</sub>/ft<sup>2</sup></span>
              </p>
            </div>
          </div>
        </div>

        <!-- Feedback after selection -->
        <div v-if="hasSelected" class="round-feedback">
          <p v-if="isCorrect" class="feedback-msg -correct">Correct!</p>
          <p v-else class="feedback-msg -wrong">Not quite!</p>

          <p class="explainer">{{ currentPair.explainer }}</p>

          <button class="action-btn" @click="nextRound">
            {{
              currentRound < quizPairs.length - 1 ? 'Next Round' : 'See Results'
            }}
          </button>
        </div>
      </div>

      <!-- Final score -->
      <div v-if="quizComplete" class="quiz-results">
        <h1 id="main-content" tabindex="-1" class="sr-only">
          Which Building Is Greener?
        </h1>

        <div class="announce-panel -blue">
          <h2>Quiz Complete!</h2>
          <p class="final-score">
            <strong>{{ score }}</strong> / {{ quizPairs.length }}
          </p>
          <p v-if="score === quizPairs.length" class="score-msg">
            Perfect score! You really know Chicago's buildings.
          </p>
          <p v-else-if="score >= quizPairs.length / 2" class="score-msg">
            Good job! Building efficiency can be tricky to guess.
          </p>
          <p v-else class="score-msg">
            Building efficiency is full of surprises! Explore the site to learn
            more.
          </p>
        </div>

        <button class="action-btn play-again-btn" @click="playAgain">
          Play Again
        </button>

        <h3 class="view-more-heading">View More About These Buildings</h3>
        <ul class="view-more-links">
          <li v-for="building in buildings" :key="building.ID">
            <g-link :to="building.path">{{ building.PropertyName }}</g-link>
          </li>
        </ul>
      </div>
    </div>
  </DefaultLayout>
</template>

<style lang="scss" scoped>
.quiz-page {
  padding: 1rem 0;
}

// --- Intro screen ---

.quiz-intro {
  position: relative;
  overflow: hidden;
  height: 100vh;
  height: 100dvh;
}

.gallery {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  height: 100%;
  justify-content: center;
}

.gallery-track {
  display: flex;
  gap: 0.5rem;
  animation: gallery-scroll-left 25s linear infinite;

  &.-reverse {
    animation: gallery-scroll-right 30s linear infinite;
  }


  img {
    height: calc(100vh / 3 - 1rem);
    height: calc(100dvh / 3 - 1rem);
    width: auto;
    flex-shrink: 0;
    border-radius: $brd-rad-medium;
  }
}

@keyframes gallery-scroll-left {
  0% {
    transform: translateX(0);
  }

  100% {
    transform: translateX(-50%);
  }
}

@keyframes gallery-scroll-right {
  0% {
    transform: translateX(-50%);
  }

  100% {
    transform: translateX(0);
  }
}

.intro-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: rgba(0, 0, 0, 0.6);
  padding: 1.5rem;

  .intro-inner {
    background: rgba(0, 0, 0,0.3);
    border-radius: 0.5rem;
    padding: 1.5rem 0.5rem;
    backdrop-filter: blur(0.5rem);
  }

  h1,
  p {
    color: $white;
    max-width: 30rem;
  }

  h1 {
    margin: 0 0 0.5rem 0;
  }

  p {
    margin-top: 0.25rem;
    margin-bottom: 0.25rem;
  }
}

.start-btn {
  font-size: 1.5rem;
  padding: 0.75rem 2.5rem;
  margin-top: 0.75rem;
}

// --- Round header ---

.round-header {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  margin-bottom: 0.25rem;
  padding: 1rem;
}

.round-indicator {
  font-weight: bold;
  color: $text-mid-light;
  margin: 0;
  white-space: nowrap;
}

.round-category {
  font-weight: bold;
  font-size: 1.125rem;
  margin: 0;
}

.quiz-prompt {
  font-size: 1.125rem;
  font-weight: bold;
  margin-top: 0.25rem;
  padding: 0 1rem;
}

// --- Quiz pair grid ---

.quiz-pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin: 1rem 0;

  @media (max-width: $mobile-max-width) {
    gap: 0;

    .quiz-card:first-child {
      padding: 1rem;
      border-right: $border-medium solid $grey;
    }

    .quiz-card:last-child {
      padding: 1rem;
    }
  }
}

.quiz-card {
  border: $border-medium solid $grey;
  border-radius: $brd-rad-medium;
  padding: 0.75rem;
  text-align: center;

  &.-winner {
    border-color: $green;
    background-color: $concern-great-background;
  }

  &.-loser {
    border-color: $red;
    background-color: $concern-very-bad-background;
  }

  // Override BuildingImage max-height to fit within quiz cards
  ::v-deep .building-img-cont {
    text-align: center;

    img {
      max-height: 12rem;
    }
  }

  @media (max-width: $mobile-max-width) {
    border: none;
    border-radius: 0;
    padding: 0;
    text-align: left;

    &.-winner,
    &.-loser {
      border: none;
    }

    &.-winner {
      background-color: $concern-great-background;
    }

    &.-loser {
      background-color: $concern-very-bad-background;
    }
  }
}

.building-name {
  font-size: 1.125rem;
  margin: 0.5rem 0 0.25rem;
}

.building-stats {
  list-style: none;
  padding: 0;
  margin: 0.25rem 0 0.75rem;
  font-size: 0.875rem;
  color: $text-mid-light;

  li {
    display: block;
    font-size: 0.9375rem;
    color: $text-main;
    margin-bottom: 0.125rem;
  }
}

.pick-btn {
  width: 100%;
}

.action-btn {
  margin-left: auto;
  margin-right: auto;
}

.result-stats {
  margin-top: 0.5rem;
}

.ghg-value {
  font-size: 1.5rem;
  font-weight: bold;
  margin: 0;
}

.ghg-unit {
  font-size: 0.8125rem;
  font-weight: normal;
  color: $text-mid-light;
}

// --- Feedback ---

.round-feedback {
  text-align: center;
  margin: 1rem 0;
}

.feedback-msg {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.25rem;

  &.-correct {
    color: $green;
  }

  &.-wrong {
    color: $red;
  }
}

.explainer {
  max-width: 36rem;
  margin: 0 auto 1rem;
  font-size: 0.9375rem;
  color: $text-mid-light;
}

// --- Results ---

.quiz-results {
  text-align: center;
  margin-top: 2rem;

  .announce-panel {
    display: inline-block;
    text-align: center;
  }

  .final-score {
    font-size: 2rem;
  }

  .score-msg {
    font-size: 1rem;
  }
}

.play-again-btn {
  margin-top: 1.5rem;
}

.view-more-heading {
  margin-top: 2rem;
}

.view-more-links {
  list-style: none;
  padding: 0;
  text-align: left;
  max-width: 24rem;
  margin: 0.5rem auto;

  li {
    margin-bottom: 0.5rem;
    font-size: 1.125rem;
    font-weight: bold;
  }
}

// --- Accessibility ---

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

// --- Mobile tightening ---

@media (max-width: $mobile-max-width) {
  .quiz-intro {
    .start-btn {
      font-size: 1.25rem;
    }

    .intro-overlay {
      padding: 1rem;
    }
  }

  .round-header {
    flex-direction: column;
    gap: 0;
  }

  .building-name {
    font-size: 1.25rem;
    line-height: 1.25;
  }

  .building-stats {
    font-size: 0.8125rem;
  }
}
</style>
