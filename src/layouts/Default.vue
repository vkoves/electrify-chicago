<static-query>
  query {
    metadata {
      siteName
    }
  }
</static-query>

<template>
  <div>
    <div class="layout">
      <!-- TODO: Split to a component-->
      <header class="header">
        <strong>
          <g-link to="/">
              <g-image src="~/images/electrify-chicago-logo.svg"
                alt="Electrify Chicago Homepage" class="site-logo" />
          </g-link>
        </strong>
        <nav class="top-nav">
          <g-link class="nav-link" to="/">Home</g-link>
          <g-link class="nav-link" to="/about/">About</g-link>
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
          <g-image alt="" src="~/images/github-mark.svg" width="16" />
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

  nav a {
    font-weight: bold;

    + a { margin-left: 1rem; }
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
