<static-query>
  query {
    metadata {
      siteName
    }
  }
</static-query>

<script>
export default {
  data() {
    return {
      searchQuery: '',
    };
  },
  methods: {
    submitSearch(event) {
      if (event) {
        event.preventDefault();
      }

      document.location.href = `/search?q=${this.searchQuery}`;
    },
  },
};
</script>

<template>
  <div>
    <div class="layout">
      <!-- TODO: Split to a component-->
      <header class="header">
        <g-link to="/" class="logo-link">
          <img src="/electrify-chicago-logo.svg"
              alt="Electrify Chicago Homepage" class="site-logo" />
        </g-link>
        <nav class="top-nav">
          <g-link class="nav-link" to="/">Home</g-link>
          <g-link class="nav-link" to="/about">About</g-link>
          <g-link class="nav-link" to="/top-gas-users">Top Gas Users</g-link>
          <g-link class="nav-link" to="/top-emitters">Top Emitters</g-link>
          <g-link class="nav-link" to="/biggest-buildings">Biggest Buildings</g-link>
          <!--
            <g-link class="nav-link" to="/top-electricity-users">Top Electricity Users</g-link>
          -->

          <form class="search-form">
            <div class="input-cont">
              <input type="text" name="search" id="search"
                aria-label="Search benchmarked buildings"
                placeholder="Search property name/address" v-model="searchQuery">
              <button v-on:click="submitSearch" type="submit">Search</button>
            </div>
          </form>
        </nav>
      </header>

      <!-- The main content -->
      <slot/>

    </div>

    <!-- TODO: Split to a component -->
    <footer>
      <div>
        Created by <a href="https://viktorkoves.com/">Viktor Köves</a>
      </div>
      <div>
        <a href="https://github.com/vkoves/electrify-chicago">
          <img alt="" src="/github-mark.svg" width="16" />
          Contribute to Electrify Chicago on GitHub
        </a>
      </div>
    </footer>
  </div>
</template>

<style lang="scss">
.layout {
  // Make sure footer is always at the bottom
  min-height: calc(100vh - 10rem);
  max-width: 75rem; // 1200px
  margin: 0 auto;
  padding-left: 1rem;
  padding-right: 1rem;
  // Account for <footer> for mobile
  padding-bottom: 5rem;
}

header.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: solid $border-thin $grey;
  padding: 1rem 0;
  gap: 2rem;

  .logo-link {
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

    a {
      font-weight: bold;
      color: $black;
      text-decoration: none;
      padding: 0.2rem 0;

      // Style current page link
      &.active--exact {
        box-shadow: 0 0.5rem $chicago-blue;
        text-decoration: none;
      }
    }
  }

  @media (max-width: $mobile-max-width) {
    flex-wrap: wrap;
    margin-top: 0.5rem;
    height: auto;
    gap: 0;

    .logo-link {
      flex-shrink: initial;

      .site-logo {
        display: block;
        width: 100%;
        height: auto;
      }
    }

    // Tighten vertical gap
    .top-nav { gap: 1.25rem 1.5rem; }

    form.search-form { width: 100%; }

    nav { margin: 1rem 0; }
  }
}

footer {
  width: 100%;
  text-align: center;
  padding: 1rem 0;
  background-color: $grey;
  font-size: 0.75rem;

  > div + div { margin-top: 0.5rem; }

  a {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
  }

  @media (max-width: $mobile-max-width) {
    position: static;
  }
}
</style>
