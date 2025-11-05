<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

/**
 * Site Wide Header
 */
@Component({
  name: 'AppHeader',
})
export default class AppHeader extends Vue {
  isHomepage = false;

  mobileMenuOpen = false;

  searchQuery = '';

  focusMain(): void {
    const mainHeading = document.getElementById('main-content');

    if (mainHeading) {
      mainHeading.focus();
    } else {
      throw new Error(
        "No main heading found matching selector '#main-content'!",
      );
    }
  }

  submitSearch(event?: Event): void {
    event?.preventDefault();

    document.location.href = `/search?q=${this.searchQuery}`;
  }

  toggleMobileMenu(): void {
    this.mobileMenuOpen = !this.mobileMenuOpen;
  }

  mounted(): void {
    this.isHomepage = document.location.pathname === '/';
  }
}
</script>

<template>
  <header class="header">
    <a href="#main-content" class="nav-link skip-to-main" @click="focusMain">
      Skip to Main Content
    </a>

    <!-- The main top container on mobil -->
    <div class="header-primary">
      <g-link to="/" class="logo-link">
        <img
          src="/electrify-chicago-logo.svg"
          alt="Electrify Chicago Homepage"
          width="270"
          height="48"
          class="site-logo"
        />
      </g-link>
    
      <button
        class="mobile-menu-toggle -grey mobile-only"
        :aria-expanded="mobileMenuOpen.toString()"
        @click="toggleMobileMenu"
      >
        <img src="/menu.svg" alt="Menu" width="25" height="25" />
      </button>
    </div>

    <nav class="top-nav" :class="{ '-hidden': !mobileMenuOpen }">
      <g-link class="nav-link" to="/"> Home </g-link>

      <g-link class="nav-link" to="/map"> Map </g-link>

      <g-link class="nav-link" to="/wards"> Wards </g-link>

      <g-link class="nav-link" to="/top-emitters"> Top Emitters </g-link>

      <g-link class="nav-link" to="/biggest-buildings">
        Biggest Buildings
      </g-link>

      <g-link class="nav-link" to="/large-owners"> Large Owners </g-link>

      <g-link class="nav-link" to="/cleanest-buildings">
        Cleanest Buildings
      </g-link>

      <g-link class="nav-link" to="/about"> About </g-link>

      <g-link class="nav-link" to="/blog"> Blog </g-link>

      <form v-if="!isHomepage" class="search-form">
        <div class="input-cont">
          <input
            id="search"
            v-model="searchQuery"
            type="text"
            name="search"
            aria-label="Search benchmarked buildings"
            placeholder="Search property name/address"
          />
          <button type="submit" @click="submitSearch">
            <img src="/search.svg" alt="" width="18" height="18" />
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
  padding: 1rem;
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

    &:focus {
      top: 0;
    }
  }

  .logo-link {
    display: inline-flex;
    flex-shrink: 0;
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

  .mobile-only {
    display: none;
  }

  /**
   * Mobile Styling
   */
  @media (max-width: $mobile-max-width) {
    position: relative;
    flex-wrap: wrap;
    height: auto;
    gap: 0;
    padding: 0;

    // Show mobile components
    .mobile-only {
      display: block;
    }

    .header-primary,
    .top-nav {
      padding: 0.5rem 0.75rem;
    }

    .header-primary {
      display: flex;
      justify-content: space-between;
      width: 100%;
    }

    .top-nav {
      position: absolute;
      top: 100%;
      z-index: 10;
      width: 100%;
      gap: 1rem 1.5rem;
      margin: 0;
      background-color: $off-white;

      // Hide until nav is opened on mobile
      &.-hidden {
        display: none;
      }
    }

    .logo-link {
      flex-shrink: initial;
      width: 60%;
      max-width: 22rem;

      .site-logo {
        display: block;
        height: auto;
      }
    }

    .mobile-menu-toggle {
      padding: 0.5rem;

      img {
        display: block;
      }
    }

    form.search-form {
      width: 100%;

      input,
      button {
        font-size: 0.75rem;
      }
    }

    nav {
      margin: 1rem 0;
    }
  }
}
</style>
