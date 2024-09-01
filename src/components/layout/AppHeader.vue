<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

/**
 * Site Wide Header
 */
@Component({
  name: 'AppHeader',
})
export default class AppHeader extends Vue {
  searchQuery = '';

  focusMain(): void {
    const mainHeading = document.getElementById('main-content');

    mainHeading!.focus();
  }

  submitSearch(event?: Event): void {
    if (event) {
      event.preventDefault();
    }

    document.location.href = `/search?q=${this.searchQuery}`;
  }
}
</script>

<template>
  <header class="header">
    <a
      href="#main-content"
      class="nav-link skip-to-main"
      @click="focusMain"
    >
      Skip to Main Content
    </a>

    <g-link
      to="/"
      class="logo-link"
    >
      <img
        src="/electrify-chicago-logo.svg"
        alt="Electrify Chicago Homepage"
        width="334"
        height="48"
        class="site-logo"
      >
    </g-link>

    <nav class="top-nav">
      <g-link
        class="nav-link"
        to="/"
      >
        Home
      </g-link>

      <g-link
        class="nav-link"
        to="/map"
      >
        Map
      </g-link>

      <g-link
        class="nav-link"
        to="/top-gas-users"
      >
        Top Gas Users
      </g-link>

      <g-link
        class="nav-link"
        to="/top-emitters"
      >
        Top Emitters
      </g-link>

      <g-link
        class="nav-link"
        to="/biggest-buildings"
      >
        Biggest Buildings
      </g-link>

      <g-link
        class="nav-link"
        to="/large-owners"
      >
        Large Owners
      </g-link>

      <g-link
        class="nav-link"
        to="/cleanest-buildings"
      >
        Cleanest Buildings
      </g-link>

      <g-link
        class="nav-link"
        to="/about"
      >
        About
      </g-link>

      <g-link
        class="nav-link"
        to="/blog"
      >
        Blog
      </g-link>

      <form class="search-form">
        <div class="input-cont">
          <input
            id="search"
            v-model="searchQuery"
            type="text"
            name="search"
            aria-label="Search benchmarked buildings"
            placeholder="Search property name/address"
          >
          <button
            type="submit"
            @click="submitSearch"
          >
            Search
          </button>
        </div>
      </form>
    </nav>
  </header>
</template>