// Server API makes it possible to hook into various parts of Gridsome
// on server-side and add custom data to the GraphQL data layer.
// Learn more: https://gridsome.org/docs/server-api/

// Changes here require a server restart.
// To restart press CTRL + C in terminal and run `gridsome develop`

module.exports = function(api) {
  api.loadSource(({addCollection}) => {
    // Use the Data Store API here: https://gridsome.org/docs/data-store-api/
  });

  api.createPages(({createPage}) => {
    // Use the Pages API here: https://gridsome.org/docs/pages-api/
  });
};

/**
 * From fetching CSV data:
 * https://gridsome.org/docs/fetching-data/#csv
 */
const {readFileSync} = require('fs');
const parse = require('csv-parse/sync').parse;

const DataDirectory = './src/data/dist/';

const BuildingEmissionsDataFile = 'building-benchmarks.csv';

module.exports = function(api) {
  api.loadSource(async (actions) => {
    loadBuildingBenchmarkData(actions);
  });
};

/**
 * Load in the building benchmark data
 *
 * @param {unknown} actions The actions class?
 */
function loadBuildingBenchmarkData(actions) {
  const input = readFileSync(`${DataDirectory}${BuildingEmissionsDataFile}`, 'utf8');

  /**
   * Load in building benchmarks and expose as Buildings collection
   */
  const BuildingsData = parse(input, {
    columns: true,
    skip_empty_lines: true,
  });

  const collection = actions.addCollection({typeName: 'Building'});

  for (const building of BuildingsData) {
    // Make a slugSource that is the property name or the address as a fallback
    building.slugSource = building.PropertyName || building.Address;

    collection.addNode(building);
  }
}
