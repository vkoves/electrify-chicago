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
- [ ] Setup linting in CI (ESLint ✅️, Prettier, Stylelint)
- [ ] Setup unit tests


## Feature To-Do List

- [x] Show property owner (manually tagged)
- [x] Pre-process data to calculate things like averages for each property and rank of each building overall, in their class (TODO), and in their ward (TODO)
- [x] Add colors/emoji to table view to give more context (e.g. so people know Keating is super bad)
- [ ] Show % of energy use from the four sources (electric, gas, district chilled water, district steam)
- [ ] Create ward page that shows data by ward (needs new data source)
- [ ] Figure out a way to rank buildings by opportunity for improvement (perhaps higher than avg. in category, uses a lot of natural gas?)


## Development

### Front-End Setup

Make sure you have [Yarn](https://yarnpkg.com/) installed, `cd` into the project directory (after cloning it) and run:

```bash
yarn install
```

### Running The Front-End

Run `yarn develop` to start a local dev server at `http://localhost:8080`

Happy coding 🎉🙌

### Run Front-End Linting

To run linting with auto-fix, run:

```bash
yarn lint-fix
```

## Deploys

This site deploys automatically via Netlify by running `gridsome build`.


## Tools

[python](https://www.python.org/) and [pandas](https://pandas.pydata.org/)
for data processing

Leaflet and Leaflet Google mutant https://www.npmjs.com/package/leaflet.gridlayer.googlemutant


## Data Processing

### Python Setup (For Data Processing & tests)

This project's Python data pipeline requires:

- pip
- python 3.9

To install our Python dependencies, from the root of the project, run:

```bash
pip install --no-cache-dir -r requirements.txt
```

### Run Data Processing

If you update the raw data CSVs or the data scripts that post-process them (like if you are adding
a new statistical analysis), you need to re-run the data processing. Make sure to follow the "Python
Setup" steps first.

To then process a new CSV file (at `src/data/source/ChicagoEnergyBenchmarking.csv`), from the project
directory run:

```bash
bash run_all.sh
```

### Run Data Processing Tests

Make sure test data is created/replaced before running tests by running the following script from
the main project directory (it will overwrite the existing test data file if it exists):

```bash
bash create_test_data.sh
```

To run all tests simply in the project directory run:

```bash
pytest
```

This assumes that `pytest` has been installed, see setup.

Run the following command for individual unit test suite (where XXX is something like
`test_clean_all_years`):

```bash
python3 -m pytest test/data/scripts/unit/XXX.py
```


## Known Development Issues

#### macOS libvips Error

If you encounter an error on macOS such as `sharp Prebuilt libvips 8.10.5 binaries are not yet available for darwin-arm64v8`, you'll need to install these dependencies separately. Install the [Brew package manager](https://brew.sh/), then run the following commands:

```
brew install --build-from-source gcc
xcode-select install
brew install vips
```
=======
**Important!** When you update the data, make sure to update the `LatestDataYear` in
`globals.vue`, as well as the filter year in all page queries.
