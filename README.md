# Electrify Chicago

[![Netlify Status](https://api.netlify.com/api/v1/badges/d777babe-6135-45a1-99dd-6377999b6127/deploy-status)](https://app.netlify.com/sites/radiant-cucurucho-d09bae/deploys)

A site to publicize some of the most polluting buildings based on the Chicago Energy Benchmarking data published in the City of Chicago Data Portal.

It's powered by [VueJS 2](https://v2.vuejs.org/) and [GridSome](https://gridsome.org/)

## Data Import

Sources:

- [Chicago Energy Benchmarking - Covered Buildings Data](https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking-Covered-Buildings/g5i5-yz37)

### Cleanup

GraphQL requires data key names to have no spaces or special characters, so there's a raw data file (only filtered by GHG emissions > 1,000 tons and year = 2020) and a cleaned file that just hast he headers renamed for GraphQL.

## Tools

[python](https://www.python.org/) and [pandas](https://pandas.pydata.org/)
for data processing

Leaflet and Leaflet Google mutant https://www.npmjs.com/package/leaflet.gridlayer.googlemutant

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

## Environment setup

### **1. Set up Docker**

Docker is the recommended approach to quickly getting started with local development. Docker helps create a version of the Electrify Chicago website on your computer so you can test out your code before submitting a pull request.

- The recommended installation method for your operating system can be found [here](https://docs.docker.com/install/). 
- [Get started with Docker](https://docs.docker.com/get-started/)

### **2. Start Docker**

> [!IMPORTANT]
> Please make sure the `Docker Desktop` application is **running on your computer** before you run the bash commands below.

This command starts server locally. To start it, `cd` into the project directory in your terminal then run the following command: 

```bash
 docker-compose up
```

Running the above command will result in the following output in your terminal

<details>
  <summary><strong>Click here</strong> to see an example terminal output</summary>
  <img width="662" alt="Screenshot 2024-04-05 at 7 23 04 PM" src="https://github.com/gaylem/electrify-chicago/assets/76500899/ad25d216-d58d-48f1-9f7c-16473db50537">
</details>

When you see the above output, it means the site is now running and now you can browse to http://localhost:8080

### **3. Stop Docker**

- To stop and completely remove the server (i.e. the running Docker container), run `docker-compose down`
- To stop the server, but not destroy it (often sufficient for day-to-day work), run `docker-compose stop`
- Bring the same server back up later with `docker-compose up`

## Open Bash Shell

> [!IMPORTANT]
> To run any of the commands below, you'll need to do the following:
> 1. Open a new terminal and `cd` into the root project directory after spinning up your Docker container
> 2. Open up a bash shell inside the Docker container with the following command:

```bash
docker-compose exec electrify-chicago bash
```
### Run Front-End Linting

To run linting with auto-fix, run the following command inside the Docker bash shell:

```bash
yarn lint-fix
```

### Run Data Processing

1. If you update the raw data CSVs or the data scripts that post-process them (like if you are adding
a new statistical analysis), you need to re-run the data processing. 

2. To then process a new CSV file (at `src/data/source/ChicagoEnergyBenchmarking.csv`), you need to run the following command inside the Docker bash shell:

```bash
bash run_all.sh
```

### Run Data Processing Tests

1. Make sure test data is created/replaced before running tests by running the following script from
the Docker bash shell (it will overwrite the existing test data file if it exists):

```bash
bash create_test_data.sh
```

2. To run all tests in the project directory, enter the following command inside the Docker bash shell:

```bash
python -m pytest
```
3. Run the following command for individual unit test suite (where XXX is something like
`test_clean_all_years`) in the Docker bash shell:

```bash
python -m pytest tests/data/scripts/unit/YOUR_FILE_NAME_HERE.py
```

## Managing The Data

### Adding a Building Owner

If there's a new large building owner to add, simply:

1. **Add the building owner in the `BuildingOwners` constant** in `buildings-custom-info.constant.vue` -
this defines metadata about the owner like their name and logo URLs

Example:

```ts
iit: {
  key: 'iit',
  name: 'Illinois Institute of Technology',
  nameShort: 'Illinois Tech',
  logoSmall: '/building-owners/iit/logo-small.png',
  logoLarge: '/building-owners/iit/logo-large.svg',
}
```

2. **Tag buildings they own in the `BuildingsCustomInfo` constant** (in the same
`buildings-custom-info.constant.vue` file) - this associates a given building (by its numeric unique
ID, found under its address on its details page), with a given owner.

Example:

```ts
// Keating Hall
'256434': {owner: BuildingOwners.iit.key},
```

3. **Setup their route by adding the new owner's ID (key) to `BuildingOwnerIds`** (in
`gridsome.server.js`) - this tells Gridsome to create a route for this given slug

Example:

```ts
const BuildingOwnerIds = [
  'iit',
  // ...
]
```

**Note:** You'll have to restart your `yarn develop` after step 3 to see changes, since
`gridsome.server.js` just runs once.

## Deploys

This site deploys automatically via Netlify by running `gridsome build`.

