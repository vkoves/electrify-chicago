// Server API makes it possible to hook into various parts of Gridsome
// on server-side and add custom data to the GraphQL data layer.
// Learn more: https://gridsome.org/docs/server-api/

// Changes here require a server restart.
// To restart press CTRL + C in terminal and run `gridsome develop`

/**
 * From fetching CSV data:
 * https://gridsome.org/docs/fetching-data/#csv
 */
const { readFileSync } = require('fs');
const build = require('gridsome/lib/build');
const parse = require('csv-parse/sync').parse;

const DataDirectory = './src/data/dist/';

const BuildingEmissionsDataFile = 'building-benchmarks.csv';
const HistoricBenchmarkingDataFile = 'benchmarking-all-years.csv';

// This is an array equivalent of Object.keys(BuildingOwners) but this file can't use Typescript and
// import that file
const BuildingOwnerIds = [
  'depaul',
  'uchicago',
  'uic',
  'iit',
  'northwestern',
  'loyola',
  'cps',
  'cha',
  'cityofchicago',
  'columbia',
  'ccc',
  'moody',
  'saic',
  'npu',
];

module.exports = function (api) {
  // Use the Data Store API here: https://gridsome.org/docs/data-store-api/
  api.loadSource(async (actions) => {
    loadBuildingBenchmarkData(actions);
    loadHistoricBenchmarkDat(actions);
  });

  // Use the Pages API here: https://gridsome.org/docs/pages-api/
  api.createPages(({ createPage }) => {
    // Create pages for building owners. This could be a dynamic route, but making it this way
    // should let them get statically built as expected
    BuildingOwnerIds.forEach((ownerId) => {
      createPage({
        path: `/owner/${ownerId}`,
        component: './src/templates/BuildingOwner.vue',
        context: { ownerId },
      });
    });
  });
};

/**
 * Load in the building benchmark data
 *
 * @param {unknown} actions The actions class?
 */
function loadBuildingBenchmarkData(actions) {
  const latestBenchmarksRaw = readFileSync(
    `${DataDirectory}${BuildingEmissionsDataFile}`,
    'utf8',
  );

  /**
   * Load in building benchmarks and expose as Buildings collection
   */
  const LatestBenchmarksData = parse(latestBenchmarksRaw, {
    columns: true,
    skip_empty_lines: true,
  });

  const collection = actions.addCollection({ typeName: 'Building' });

  for (const building of LatestBenchmarksData) {
    // Make a slugSource that is the property name or the address as a fallback (skip one letter
    // names, e.g. '-)
    building.slugSource =
      building.PropertyName.length > 1
        ? building.PropertyName
        : building.Address;

    // The csv parse returns everything as strings, so explicitly parse float columns so GraphQL
    // loads them properly and can apply filters (like `TotalGHGEmissions: { gt: 1000.0 }`)
    // TODO: Parse all our float and int columns so GraphQL can then filter them
    const buildingFloatCols = [
      'DistrictChilledWaterUse',
      'DistrictSteamUse',
      'ElectricityUse',
      'GHGIntensity',
      'GrossFloorArea',
      'NaturalGasUse',
      'TotalGHGEmissions',
    ];

    buildingFloatCols.forEach((col) => {
      building[col] = parseFloat(building[col]);
    });

    if (!building.slugSource || typeof building.slugSource !== 'string') {
      throw new Error('No building slug source (name or address)!', building);
    }

    // If we get a duplicate node warning, notate the name, and then we tack on the ID to the URL
    // so '/building/salvation-army` becomes `/building/salvation-army-1234`
    const duplicateSlugs = [
      'illinois-institute-of-technology',
      'bricktown-square',
      'the-woodlands-of-bronzeville-condominium-association',
      'west-side-realty-corporation',
      'gateway-centre',
      'salvation-army',
      'left-bank-at-k-station',
      'tech-business-center',
      'iit-research-tower',
      'oakwood-shores-2d',
    ]

    try {
      if (duplicateSlugs.includes(building.slugSource.toLowerCase().replaceAll(' ', '-'))) {
        building.slugSource =   building.slugSource + building.ID;
      }

      collection.addNode(building);
    }
    catch (error) {
      console.log('error', error);
    }
  }
}

/**
 * Load in the historic benchmark data
 *
 * @param {unknown} actions The actions class?
 */
function loadHistoricBenchmarkDat(actions) {
  const historicBenchmarksRaw = readFileSync(
    `${DataDirectory}${HistoricBenchmarkingDataFile}`,
    'utf8',
  );

  /**
   * Load in building benchmarks and expose as Buildings collection
   */
  const HistoricBenchmarksData = parse(historicBenchmarksRaw, {
    columns: true,
    skip_empty_lines: true,
  });

  const collection = actions.addCollection({ typeName: 'Benchmark' });

  for (const benchmark of HistoricBenchmarksData) {
    // The csv parse returns everything as strings, so explicitly parse float columns so GraphQL
    // loads them properly and can apply filters (like `TotalGHGEmissions: { gt: 1000.0 }`)
    // TODO: Parse all our float and int columns so GraphQL can then filter them
    const historicFloatCols = [
      'DistrictChilledWaterUse',
      'DistrictSteamUse',
      'ElectricityUse',
      'GHGIntensity',
      'GrossFloorArea',
      'NaturalGasUse',
      'SourceEUI',
      'TotalGHGEmissions',
    ];

    historicFloatCols.forEach((col) => {
      benchmark[col] = parseFloat(benchmark[col]);
    });

    collection.addNode(benchmark);
  }
}
