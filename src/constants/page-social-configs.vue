<script lang="ts">
/**
 * TypeScript utilities for page social configs
 */
const pageSocialConfigsData = require('./page-social-configs.json');

export default {};

export interface IPageSocialConfig {
  id: string;
  title: string;
  description?: string;
  filter?: 'best' | 'worst' | 'largest';
}

export const pageSocialConfigs: Record<string, IPageSocialConfig> =
  pageSocialConfigsData as Record<string, IPageSocialConfig>;

/**
 * Get page config by ID
 */
export function getPageSocialConfig(pageId: string): IPageSocialConfig | null {
  return pageSocialConfigs[pageId] || null;
}

/**
 * Get all available page IDs
 */
export function getAvailablePageIds(): string[] {
  return Object.keys(pageSocialConfigs);
}
</script>
