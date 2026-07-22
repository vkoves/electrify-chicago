<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import {
  IBuildingSearchIndexItem,
  normalizeForSearch,
} from '../common-functions.vue';

/** A search index item with its normalized fields precomputed for matching */
interface INormalizedIndexItem {
  item: IBuildingSearchIndexItem;
  name: string;
  address: string;
  type: string;
}

/**
 * Search input with a building-name/address autocomplete dropdown, shared by
 * the homepage hero and the site header.
 *
 * The autocomplete index (~3.5k buildings) is fetched lazily on first focus
 * from /building-search-index.json (generated at build time by
 * gridsome.server.js), so it's ready by the time the user types but never
 * bloats the initial page load.
 *
 * Selecting a suggestion navigates straight to that building's page; submitting
 * without a selection falls back to the full search page (/search?q=...).
 */
@Component({ name: 'BuildingSearchAutocomplete' })
export default class BuildingSearchAutocomplete extends Vue {
  /** Unique id for the input, used to wire up label/listbox ARIA attributes */
  @Prop({ default: 'building-search' }) readonly inputId!: string;

  @Prop({ default: 'Search benchmarked buildings' })
  readonly ariaLabel!: string;

  @Prop({ default: 'Search property name or address' })
  readonly placeholder!: string;

  /** Optional visible button text; when empty the button is icon-only */
  @Prop({ default: '' }) readonly buttonLabel!: string;

  /** Pixel size of the search icon in the submit button */
  @Prop({ default: 32 }) readonly iconSize!: number;

  /** Max number of suggestions shown in the dropdown */
  readonly MaxSuggestions = 8;

  searchQuery = '';
  suggestions: Array<IBuildingSearchIndexItem> = [];

  /** Index of the keyboard-highlighted suggestion, or -1 for none */
  activeIndex = -1;

  /** Whether the dropdown should be shown (input focused and typing) */
  open = false;

  /** Normalized index, populated once on first focus */
  private normalizedIndex: Array<INormalizedIndexItem> | null = null;
  private loading = false;

  get isOpen(): boolean {
    return this.open && this.suggestions.length > 0;
  }

  get listboxId(): string {
    return `${this.inputId}-suggestions`;
  }

  /** ARIA id of the active option for aria-activedescendant */
  get activeDescendant(): string {
    return this.activeIndex >= 0
      ? `${this.listboxId}-option-${this.activeIndex}`
      : '';
  }

  /** Fetch and normalize the search index once, on first focus */
  async loadIndex(): Promise<void> {
    if (this.normalizedIndex || this.loading) {
      return;
    }

    this.loading = true;

    try {
      const response = await fetch('/building-search-index.json');
      const items: Array<IBuildingSearchIndexItem> = await response.json();

      this.normalizedIndex = items.map((item) => ({
        item,
        name: normalizeForSearch(item.name),
        address: normalizeForSearch(item.address),
        type: normalizeForSearch(item.type),
      }));
    } catch (error) {
      console.error('Failed to load building search index:', error);
      this.normalizedIndex = [];
    } finally {
      this.loading = false;
      this.updateSuggestions();
    }
  }

  onFocus(): void {
    this.open = true;
    this.loadIndex();
    this.updateSuggestions();
  }

  onInput(): void {
    this.open = true;
    this.updateSuggestions();
  }

  /**
   * Rank a normalized building entry against the query. Higher is better; 0
   * means no match. Name matches outrank address matches, which outrank
   * property type matches, and prefix matches outrank mid-string matches.
   */
  private rank(entry: INormalizedIndexItem, query: string): number {
    if (entry.name.startsWith(query)) return 5;
    if (entry.name.includes(query)) return 4;
    if (entry.address.startsWith(query)) return 3;
    if (entry.address.includes(query)) return 2;
    if (entry.type.includes(query)) return 1;
    return 0;
  }

  updateSuggestions(): void {
    const query = normalizeForSearch(this.searchQuery);

    if (!query || !this.normalizedIndex) {
      this.suggestions = [];
      this.activeIndex = -1;
      return;
    }

    const matches: Array<{ entry: INormalizedIndexItem; score: number }> = [];

    for (const entry of this.normalizedIndex) {
      const score = this.rank(entry, query);
      if (score > 0) {
        matches.push({ entry, score });
      }
    }

    matches.sort((a, b) => b.score - a.score);

    this.suggestions = matches
      .slice(0, this.MaxSuggestions)
      .map((match) => match.entry.item);
    this.activeIndex = -1;
  }

  /** Move the keyboard highlight up or down, wrapping around the list */
  moveActive(delta: number): void {
    if (!this.isOpen) {
      return;
    }

    const count = this.suggestions.length;
    this.activeIndex = (this.activeIndex + delta + count) % count;
  }

  onEnter(event: Event): void {
    // If a suggestion is highlighted, go to it instead of submitting the form
    if (this.isOpen && this.activeIndex >= 0) {
      event.preventDefault();
      this.selectSuggestion(this.suggestions[this.activeIndex]);
    }
  }

  selectSuggestion(suggestion: IBuildingSearchIndexItem): void {
    this.close();
    window.location.href = suggestion.path;
  }

  /**
   * Secondary line shown under the name: the address (unless it's already
   * being used as the name) plus the property type.
   */
  detailText(suggestion: IBuildingSearchIndexItem): string {
    const parts: Array<string> = [];

    if (suggestion.name && suggestion.address) {
      parts.push(suggestion.address);
    }

    if (suggestion.type) {
      parts.push(suggestion.type);
    }

    return parts.join(' · ');
  }

  /** Fall back to the full search page when submitting without a selection */
  submitSearch(event?: Event): void {
    event?.preventDefault();

    const query = this.searchQuery.trim();
    window.location.href = `/search?q=${encodeURIComponent(query)}`;
  }

  close(): void {
    this.open = false;
    this.activeIndex = -1;
  }
}
</script>

<template>
  <form
    class="search-form building-search-autocomplete"
    role="search"
    @submit="submitSearch"
  >
    <div class="input-cont">
      <input
        :id="inputId"
        v-model="searchQuery"
        type="text"
        name="search"
        autocomplete="off"
        role="combobox"
        aria-autocomplete="list"
        :aria-label="ariaLabel"
        :aria-expanded="isOpen.toString()"
        :aria-controls="listboxId"
        :aria-activedescendant="activeDescendant"
        :placeholder="placeholder"
        @focus="onFocus"
        @input="onInput"
        @keydown.down.prevent="moveActive(1)"
        @keydown.up.prevent="moveActive(-1)"
        @keydown.enter="onEnter"
        @keydown.esc="close"
        @blur="close"
      />
      <button type="submit">
        <img
          src="/search.svg"
          :alt="buttonLabel ? '' : 'Search'"
          :width="iconSize"
          :height="iconSize"
        />
        <template v-if="buttonLabel">{{ buttonLabel }}</template>
      </button>

      <ul
        v-if="isOpen"
        :id="listboxId"
        class="search-suggestions"
        role="listbox"
      >
        <li
          v-for="(suggestion, index) in suggestions"
          :id="`${listboxId}-option-${index}`"
          :key="suggestion.path"
          role="option"
          :aria-selected="(index === activeIndex).toString()"
          :class="{ '-active': index === activeIndex }"
          @mousedown.prevent="selectSuggestion(suggestion)"
          @mouseenter="activeIndex = index"
        >
          <span class="name">{{ suggestion.name || suggestion.address }}</span>
          <span v-if="detailText(suggestion)" class="details">
            {{ detailText(suggestion) }}
          </span>
        </li>
      </ul>
    </div>
  </form>
</template>

<style lang="scss">
.building-search-autocomplete {
  .input-cont {
    position: relative;
  }

  .search-suggestions {
    position: absolute;
    top: calc(100% + 0.25rem);
    left: 0;
    right: 0;
    z-index: 20;
    margin: 0;
    padding: 0;
    list-style: none;
    background-color: $white;
    border: solid $border-thin $grey;
    border-radius: $brd-rad-small;
    box-shadow: 0 0.25rem 0.5rem $box-shadow-main;
    max-height: 20rem;
    overflow-y: auto;
    text-align: left;
    white-space: normal;

    li {
      display: flex;
      flex-direction: column;
      gap: 0.125rem;
      padding: 0.5rem 0.75rem;
      cursor: pointer;
      // Set explicitly so we don't inherit the homepage hero's white text
      color: $text-main;
      // Transparent by default so activating an option doesn't shift content
      border-left: solid 0.25rem transparent;
      border-bottom: solid $border-thin $grey-light;

      &:last-child {
        border-bottom: none;
      }

      &.-active {
        border-left-color: $blue-dark;
        background-color: $off-white;

        // Darken the secondary text so it stays legible on the active bg
        .details {
          color: $text-main;
        }
      }

      .name {
        font-weight: 600;
        font-size: 0.875rem;
      }

      .details {
        font-size: 0.75rem;
        color: $text-light;
      }
    }
  }
}
</style>
