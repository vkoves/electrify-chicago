interface MetaTag {
  name?: string;
  property?: string;
  content: string;
  key: string;
}

interface PageSocialMetaResult {
  title: string;
  meta: MetaTag[];
}

/**
 * Utility function to generate social media meta tags for page social cards
 *
 * Overload 1: With pageId for custom social images
 */
export default function generatePageSocialMeta(
  pageId: string,
  title: string,
  description: string,
): PageSocialMetaResult;

/**
 * Overload 2: Without pageId for pages with just meta descriptions
 */
export default function generatePageSocialMeta(
  title: string,
  description: string,
): PageSocialMetaResult;

/**
 * Implementation
 */
export default function generatePageSocialMeta(
  pageIdOrTitle: string,
  titleOrDescription?: string,
  descriptionOnly?: string,
): PageSocialMetaResult {
  // Handle both signatures: (pageId, title, description) and (title, description)
  let title: string;
  let description: string;
  let socialImageUrl: string | undefined;

  if (descriptionOnly !== undefined) {
    // Three params: (pageId, title, description)
    const pageId = pageIdOrTitle;
    title = titleOrDescription!;
    description = descriptionOnly;
    socialImageUrl = `/social-images/page-${pageId}.webp`;
  } else {
    // Two params: (title, description)
    title = pageIdOrTitle;
    description = titleOrDescription || '';
    socialImageUrl = undefined;
  }

  const baseMeta = [
    { name: 'description', content: description, key: 'description' },
    { property: 'og:title', content: title, key: 'og:title' },
    { property: 'og:description', content: description, key: 'og:description' },
    { property: 'og:type', content: 'website', key: 'og:type' },
    { name: 'twitter:title', content: title, key: 'twitter:title' },
    { name: 'twitter:description', content: description, key: 'twitter:description' },
  ];

  // Add social image meta tags only if socialImageUrl is provided
  if (socialImageUrl) {
    baseMeta.push(
      { property: 'og:image', content: socialImageUrl, key: 'og:image' },
      { property: 'og:image:width', content: '1200', key: 'og:image:width' },
      { property: 'og:image:height', content: '630', key: 'og:image:height' },
      { name: 'twitter:card', content: 'summary_large_image', key: 'twitter:card' },
      { name: 'twitter:image', content: socialImageUrl, key: 'twitter:image' },
    );
  } else {
    baseMeta.push({ name: 'twitter:card', content: 'summary', key: 'twitter:card' });
  }

  return {
    title: title,
    meta: baseMeta,
  };
}

// Also export as named export for backwards compatibility
export { generatePageSocialMeta };
