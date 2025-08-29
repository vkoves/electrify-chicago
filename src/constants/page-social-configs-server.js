/* eslint-env node */
/* eslint-disable @typescript-eslint/no-require-imports, no-undef -- CommonJS module for Gridsome server compatibility */
/**
 * CommonJS version for server-side usage (gridsome.server.js)
 */
const pageSocialConfigsData = require('./page-social-configs.json');

/**
 * Get all available page IDs
 */
function getAvailablePageIds() {
  return Object.keys(pageSocialConfigsData);
}

module.exports = {
  pageSocialConfigs: pageSocialConfigsData,
  getAvailablePageIds,
};