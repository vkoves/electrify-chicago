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
        <strong>
          <g-link to="/">
              <img src="/electrify-chicago-logo.svg"
                alt="Electrify Chicago Homepage" class="site-logo" />
          </g-link>
        </strong>
        <nav class="top-nav">
          <g-link class="nav-link" to="/">Home</g-link>
          <g-link class="nav-link" to="/about">About</g-link>
          <form class="header-search">
              <input type="text" name="search" id="search"
                aria-label="Search benchmarked buildings"
                placeholder="Search property name/address" v-model="searchQuery">
              <button v-on:click="submitSearch" type="submit">Search</button>
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
  height: 5rem;
  border-bottom: solid 0.0625rem $grey;

  .site-logo {
    height: 3rem;
    width: auto;
  }

  .top-nav {
    display: flex;
    gap: 1rem;
    align-items: center;
    flex-wrap: wrap;

    a { font-weight: bold; }
  }

  form.header-search {
    display: flex;
    white-space: nowrap;

    input, button {
      height: 2.5rem;
      box-sizing: border-box;
      // TODO: Move to colors
      border: solid 0.0625rem $grey;
      padding: 0 1rem;
    }

    input {
      border-radius: 1rem 0 0 1rem;
      width: 12.5rem;
      border-right: none;
      padding-right: 0;
      font-size: 0.75rem;
      flex-grow: 1;
    }

    button {
      border-radius: 0 1rem 1rem 0;
      border-left: none;
      font-weight: bold;
    }
  }

  @media (max-width: $mobile-max-width) {
    flex-wrap: wrap;
    margin-top: 0.5rem;
    height: auto;

    .site-logo {
      display: block;
      width: 100%;
      height: auto;
    }

    form.header-search { width: 100%; }

    nav { margin: 1rem 0; }
  }
}

footer {
  // Stick to bottom of screen on big displays
  position: fixed;
  bottom: 0;
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
