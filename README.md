# Electrify Chicago

[![Netlify Status](https://api.netlify.com/api/v1/badges/d777babe-6135-45a1-99dd-6377999b6127/deploy-status)](https://app.netlify.com/sites/radiant-cucurucho-d09bae/deploys)

A site to publicize some of the most polluting buildings based on the Chicago Energy Benchmarking data published in the City of Chicago Data Portal.

It's powered by [VueJS 2](https://v2.vuejs.org/) and [GridSome](https://gridsome.org/)

## Data Import

Sources:

- [Chicago Energy Benchmarking - Covered Buildings Data](https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking-Covered-Buildings/g5i5-yz37)

### Cleanup

GraphQL requires data key names to have no spaces or special characters, so there's a raw data file (only filtered by GHG emissions > 1,000 tons and year = 2020) and a cleaned file that just hast he headers renamed for GraphQL.

## General To-Do List

- [x] Pick a framework - statically built VueJSS, maybe [VitePress](https://vitepress.dev/guide/getting-started)
- [x] Setup landing page with SCSS working
- [x] Get CSV data usable and on homepage
- [x] Setup domain and build process
- [x] Setup Typescript
- [ ] Setup linting in CI (ESLin ✅️, Prettier, Stylelint)
- [ ] Setup unit tests


## Feature To-Do List

- [x] Show property owner (manually tagged)
- [x] Pre-process data to calculate things like averages for each property and rank of each
      building overall, in their class (TODO), and in their ward (TODO)
- [x] Add colors/emoji to table view to give more context (e.g. so people know Keating is super bad)
- [ ] Show % of energy use from the four sources (electric, gas, district chilled water, district steam)
- [ ] Create ward page that shows data by ward (needs new data source)
- [ ] Figure out a way to rank buildings by opportunity for improvement (perhaps higher than avg.
      in category, uses a lot of natural gas?)

## Development

## Setup

Make sure you have [Yarn](https://yarnpkg.com/) installed, `cd` into the project directory (after cloning it) and run:

```
yarn install
```

## Running

Run `yarn develop` to start a local dev server at `http://localhost:8080`

Happy coding 🎉🙌

## Run Linting

To run linting with auto-fix, run:

```
yarn lint-fix
```

## Deploys

This site deploys automatically via Netlify by running `gridsome build`.

## Tools

[python](https://www.python.org/) and [pandas](https://pandas.pydata.org/)
for data processing

### Run Data Processing

If you update the raw data CSVs or the data scripts that post-process them (like if you are adding
a new statistical analysis), you need to re-run the data processing.

This requires:

- Pip
- Python3

Run the following commands:

```
cd src/data
pip install --no-cache-dir -r requirements.txt
python3 scripts/process-data.py
```
