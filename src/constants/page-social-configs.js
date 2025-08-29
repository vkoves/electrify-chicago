/**
 * Configuration for page social cards
 * Each config defines how to generate a social card for a major page
 */
const pageSocialConfigs = {
  'top-emitters': {
    id: 'top-emitters',
    title: 'Top Emitters',
    description: 'Chicago\'s highest greenhouse gas emitting buildings',
    filter: 'worst',
  },
  'biggest-buildings': {
    id: 'biggest-buildings', 
    title: 'Biggest Buildings',
    description: 'Chicago\'s largest buildings by floor area',
    filter: 'largest',
  },
  'all-electric': {
    id: 'all-electric',
    title: 'All Electric Buildings',
    description: 'Buildings powered entirely by electricity',
    filter: 'best',
  },
  'cleanest-buildings': {
    id: 'cleanest-buildings',
    title: 'Cleanest Buildings',
    description: 'Chicago\'s most environmentally friendly buildings',
    filter: 'best',
  },
  'top-gas-users': {
    id: 'top-gas-users',
    title: 'Top Fossil Gas Users',
    description: 'Chicago\'s biggest consumers of fossil gas',
    filter: 'worst',
  },
  'top-electricity-users': {
    id: 'top-electricity-users',
    title: 'Top Electricity Users',
    description: 'Chicago\'s biggest consumers of electricity',
    filter: 'largest',
  },
};

/**
 * Get page config by ID
 */
function getPageSocialConfig(pageId) {
  return pageSocialConfigs[pageId] || null;
}

/**
 * Get all available page IDs
 */
function getAvailablePageIds() {
  return Object.keys(pageSocialConfigs);
}

// Export for CommonJS (gridsome.server.js)
module.exports = {
  pageSocialConfigs,
  getPageSocialConfig,
  getAvailablePageIds
};