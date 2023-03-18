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
      <header class="header">
        <strong>
          <g-link to="/">{{ $static.metadata.siteName }}</g-link>
        </strong>
        <nav class="top-nav">
          <g-link class="nav-link" to="/">Home</g-link>
          <g-link class="nav-link" to="/about/">About</g-link>
        </nav>
      </header>

      <!-- The main content -->
      <slot/>

    </div>

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
@import "@/scss/colors.scss";

body {
  font-family: -apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  margin:0;
  padding:0;
  line-height: 1.5;
}

.layout {
  max-width: 760px;
  margin: 0 auto;
  padding-left: 20px;
  padding-right: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  height: 80px;
}

footer {
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
    color: $link-blue;
    gap: 0.5rem;
  }
}
</style>
