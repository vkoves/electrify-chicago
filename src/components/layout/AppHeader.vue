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

    <button class="mobile-menu-toggle -grey mobile-only">
      <img src="/menu.svg" alt="Menu" width="30" height="30">
    </button>

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

<style lang="scss">
header.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: solid $border-thin $grey;
  padding: 1rem 0;
  gap: 2rem;

  // An off screen anchor link that goes on screen when focused
  .nav-link.skip-to-main {
    position: absolute;
    background: $chicago-blue;
    color: $white;
    border-top: none;
    border-radius: 0 0 $brd-rad-medium $brd-rad-medium;
    padding: 1rem;
    top: -10rem;
    outline-offset: 0.1rem;
    padding: 0.5rem 2rem;

    &:focus { top: 0; }
  }

  .logo-link {
    display: inline-flex;
    flex-shrink: 0;

    .site-logo {
      height: 3rem;
      width: auto;
    }
  }


  .top-nav {
    display: flex;
    gap: 1.5rem;
    align-items: center;
    flex-wrap: wrap;
    padding: 0.5rem 0;
  }

  .nav-link {
    font-weight: bold;
    color: $black;
    text-decoration: none;
    padding: 0.1rem 0.2rem;
    // Increase outline offset to prevent outline from intersecting the blue shadow
    outline-offset: 0.5rem;

    // Style current page link
    &.active--exact {
      box-shadow: 0 0.35rem $chicago-blue;
      text-decoration: none;
    }
  }

  .mobile-only { display: none; }

  @media (max-width: $mobile-max-width) {
    flex-wrap: wrap;
    margin-top: 0.5rem;
    height: auto;
    gap: 0;

    .mobile-only { display: block; }

    .logo-link {
      flex-shrink: initial;
      width: 70%;
      max-width: 22rem;

      .site-logo {
        display: block;
        height: auto;
      }
    }

    // Tighten vertical gap
    .top-nav { gap: 1.25rem 1.5rem; }

    form.search-form { width: 100%; }

    nav { margin: 1rem 0; }
  }
}
</style>