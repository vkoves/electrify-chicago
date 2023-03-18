# Electrify Chicago

A site to publicize some of the most polluting buildings based on the Chicago Energy Benchmarking data published in the City of Chicago Data Portal.

## Data Import

Sources:

- [Chicago Energy Benchmarking - Covered Buildings Data](https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking-Covered-Buildings/g5i5-yz37)

### Cleanup

GraphQL requires data key names to have no spaces or special characters, so there's a raw data file (only filtered by GHG emissions > 1,000 tons and year = 2020) and a cleaned file that just hast he headers renamed for GraphQL.

## To-Do List

- [x] Pick a framework - statically built VueJSS, maybe [VitePress](https://vitepress.dev/guide/getting-started)
- [x] Setup landing page with SCSS working
- [x] Get CSV data usable and on homepage
- [x] Setup domain and build process
- [ ] Setup unit tests
- [ ] Setup linting
- [ ] Setup Typescript


## Running

Run `gridsome develop` to start a local dev server at `http://localhost:8080`

Happy coding 🎉🙌

## Deploys

This site deploys automatically via Netlify by running `gridsome build`.
