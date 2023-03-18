# Electrify Chicago

## Data Import

Sources:

- [Chicago Energy Benchmarking - Covered Buildings Data](https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking-Covered-Buildings/g5i5-yz37)

### Cleanup

Note that the column "# of Buildings" in the Chicago energy benchmarking data gets converted to
"__of_Buildings" by CSV Parse, which GraphQL does not like. Rename that column to
"Number of Buildings" and everything is happy!

## To-Do List

- [ ] Pick a framework - statically built VueJSS, maybe [VitePress](https://vitepress.dev/guide/getting-started)
- [ ] Setup landing page with SCSS working
- [ ] Get CSV data usable and on homepage
- [ ] Setup domain and build process
- [ ] Setup unit tests
- [ ] Setup linting
- [ ] Setup Typescript


## Running

Run `gridsome develop` to start a local dev server at `http://localhost:8080`

Happy coding 🎉🙌
