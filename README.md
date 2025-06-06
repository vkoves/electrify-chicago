# Electrify Chicago

[![Netlify Status](https://api.netlify.com/api/v1/badges/d777babe-6135-45a1-99dd-6377999b6127/deploy-status)](https://app.netlify.com/sites/radiant-cucurucho-d09bae/deploys)

A site to publicize some of the most polluting buildings based on the Chicago Energy Benchmarking data published in the City of Chicago Data Portal.

Front-end in [VueJS 2](https://v2.vuejs.org/), statically built with [GridSome](https://gridsome.org/). Data processing with Python, and [Pandas](https://pandas.pydata.org/).

## Data Import

Our data is only sourced from the city's benchmarking data:

- [Chicago Energy Benchmarking Data](https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c/about_data)

### Cleanup

GraphQL requires data key names to have no spaces or special characters, so there's a raw data file (only filtered by GHG emissions > 1,000 tons and year = 2020) and a cleaned file that just hast he headers renamed for GraphQL.

## Tools

[python](https://www.python.org/) and [pandas](https://pandas.pydata.org/)
for data processing

[Leaflet](https://www.npmjs.com/package/leaflet) and [Leaflet Google mutant](https://www.npmjs.com/package/leaflet.gridlayer.googlemutant) for maps (e.g. the map page)

## Environment setup

### **1. Set up Docker**

Docker is the recommended approach to quickly getting started with local development. Docker helps create a version of the Electrify Chicago website on your computer so you can test out your code before submitting a pull request.

- The recommended installation method for your operating system can be found [here](https://docs.docker.com/install/).
- [Get started with Docker](https://docs.docker.com/get-started/)

### **2. Start Docker**

This command starts server locally. To start it, `cd` into the project directory in your terminal then run the following command:

```bash
 docker-compose up
```

**Tip:** Added a new dependency? Once you've updated the `package.json` run
`docker-compose up --build` to rebuild the image, which will re-run the setup steps in the
`Dockerfile`.

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

## Commands

### Run Front-End Linting

To run linting with auto-fixing (ESLint + Prettier), run the following command:

```bash
docker-compose run --rm electrify-chicago yarn lint-fix
```

### Run Data Processing

1. If you update the raw data CSVs or the data scripts that post-process them (like if you are adding
   a new statistical analysis), you need to re-run the data processing.

2. If you update the [Chicago Energy Benchmarking Data](https://data.cityofchicago.org/Environment-Sustainable-Development/Chicago-Energy-Benchmarking/xq83-jr8c/about_data)
   (`src/data/source/ChicagoEnergyBenchmarking.csv`), you need to update `src/data/source/CityGeocoder.xlsx` by following the
   instructions in `src/data/scripts/city-geocodes/README.md`.

3. To then process a new CSV file (at `src/data/source/ChicagoEnergyBenchmarking.csv`), you need to run the following command:

```bash
docker-compose run --rm electrify-chicago python3 run_all.py
```

### Run Data Processing Tests

1. Make sure test data is created/replaced before running tests by running the following script (it will overwrite the existing test data file if it exists):

```bash
docker-compose run --rm electrify-chicago bash create_test_data.sh
```

2. To run all tests in the project directory, enter the following command:

```bash
docker-compose run --rm electrify-chicago python -m pytest
```

3. Run the following command for individual unit test suite (where YOUR_FILE_NAME is something like
   `test_clean_all_years`):

```bash
docker-compose run --rm electrify-chicago python -m pytest tests/data/scripts/unit/YOUR_FILE_NAME.py
```

### Code Coverage

To run tests with coverage and generate coverage reports:

1. Run tests with coverage

```bash
docker-compose run --rm electrify-chicago coverage run --source=src/data/scripts -m pytest
```

2. View the coverage report in the terminal:

```bash
docker-compose run --rm electrify-chicago coverage report
```

3. Generate an HTML coverage report (results will be in the htmlcov/ directory):

```bash
docker-compose run --rm electrify-chicago coverage html
```

The `--source` parameter ensures that files without tests are still included in the coverage report, giving a more accurate picture of overall code coverage.

## Running Python Scripts Locally

If you want to run Python scripts or Jupyter notebooks locally outside of Docker, you should use a Python virtual environment. To see how to set up a Python virtual environment and manage Python dependencies, see our Python dev guide at [PythonDev.md](PythonDev.md).

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
];
```

**Note:** You'll have to restart your `yarn develop` after step 3 to see changes, since
`gridsome.server.js` just runs once.

### Adding Building Images

1. \*_Find A Suitable Image_ -- Building images can be sourced from Google Maps or a source that
   allows redistribution, like Wikimedia. Also see "Automatically Fetching Images from Streetview"

2 **Process the Image**

We should reasonably crop images if needed and then scale them to be EITHER:

- 1000px wide if it's a landscape image
- 600px wide if it's a portrait image

Make sure to export it as a `.webp` image at a **quality level of 70**, which should ensure a reasonable
file size under 200 kB.

**Store the image in `/static/building-imgs/`.**

3. **Tell The Site There's a Building Image** - Follow the pattern of other buildings in the
   `building-images.constant.vue`, providing an attribution URL, the image file name, and specify
   whether it's a tall (portrait) image and whether it's from Google Maps.

4. **Confirm the image is visible and looks good** - and that's all there is to it!

### Automatically Fetching Images from Streetview

We have a handy script, `fetch_streetview_imagery.py` that can be used to automatically fetch
Streetview building images by address. Unfortunately, Streetview imagery can be pretty hit or miss,
and so this is still a pretty manual process.

1. **Get a Google Maps API Key** - Ask Viktor for a key or setup your only Google Maps API key with
   Google

2. **Create An Addresses CSV** - create a CSV file of buildings addresses you want to fetch, with
   columns:

   - **ID** - the building ID (e.g "256424"), used so the output filename contains the ID
   - **address** - the full address (e.g "10 W 31st Street, Chicago IL, 60616")

   You can use `template_buildings_to_img.csv` as an example.

   **Tip!** If you're looking to check for images for a whole page, add `?debug` to the URL locally,
   and it'll show you the ID and address formatted for the CSV, right under the building name in any
   data table. You can then just copy paste each building you want to check into the CSV.

   You can also then pull all the addresses by running some simple JS:

   ```ts
   Array.from(document.querySelectorAll('.prop-address')).map(
     (elem) => elem.innerText,
   );
   ```

3. **Run The Script** - run the script to fetch images, passing in the API key and the path to your
   addresses CSV, like so:

   ```sh
   python3 -m src.data.scripts.fetch_streetview_imagery API_KEY ../addresses_to_img.csv
   ```

   This will save images to `/tmp_streetview_images`, which is git ignored so you can't accidentally
   commit building images without manually reviewing them.

4. **Copy Images You Like & Follow "Adding Building Images" Process** - a lot of the Google
   Streetview imagery might come back and not show the building well, so review the generated images,
   copy the ones you like over and follow our process above for adding building images.

   **Copy these images into `static/building-imgs/auto-streetview` specifically**, so that it's
   clear that these were automatically pulled and not hand-authored.

### Handling Duplicate Nodes Errors

When Gridsome builds, if you see an error like:

```sh
Building > Failed to add node: Duplicate key for property path: /building/salvation-army/
```

Add the building slug (the unique piece of the URL, e.g `salvation-army`) and add it to the
`duplicateSlugs` array in `gridsome.server.js`. By doing this, when the build process sees this
slug, it'll append the building ID to generate a unique URL. This happens when multiple buildings
have the same name, like "Salvation Army" in our example (which has multiple locations, and doesn't
specify their location in the title).

## Deploys

This site deploys automatically via Netlify by running `gridsome build`.
