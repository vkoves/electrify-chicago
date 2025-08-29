interface MetaTag {
  name?: string;
  property?: string;
  content: string;
  key?: string;
}

interface PageSocialMetaResult {
  title: string;
  meta: MetaTag[];
}

/**
 * Utility function to generate social media meta tags for page social cards
 */
export default function generatePageSocialMeta(
  pageId: string,
  title: string,
  description: string,
): PageSocialMetaResult {
  const socialImageUrl = `/social-images/page-${pageId}.webp`;

  return {
    title: title,
    meta: [
      { name: 'description', content: description },
      { property: 'og:title', content: title },
      { property: 'og:description', content: description },
      { property: 'og:image', content: socialImageUrl, key: 'og:image' },
      { property: 'og:image:width', content: '1200' },
      { property: 'og:image:height', content: '630' },
      { property: 'og:type', content: 'website' },
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:title', content: title },
      { name: 'twitter:description', content: description },
      { name: 'twitter:image', content: socialImageUrl },
    ],
  };
}

// Also export as named export for backwards compatibility
export { generatePageSocialMeta };
