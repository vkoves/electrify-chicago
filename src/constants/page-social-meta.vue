<script lang="ts">
export default {};

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
 */
export function generatePageSocialMeta(
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
    {
      name: 'twitter:description',
      content: description,
      key: 'twitter:description',
    },
  ];

  // Add social image meta tags only if socialImageUrl is provided
  if (socialImageUrl) {
    baseMeta.push(
      { property: 'og:image', content: socialImageUrl, key: 'og:image' },
      { property: 'og:image:width', content: '1200', key: 'og:image:width' },
      { property: 'og:image:height', content: '630', key: 'og:image:height' },
      {
        name: 'twitter:card',
        content: 'summary_large_image',
        key: 'twitter:card',
      },
      { name: 'twitter:image', content: socialImageUrl, key: 'twitter:image' },
    );
  } else {
    baseMeta.push({
      name: 'twitter:card',
      content: 'summary',
      key: 'twitter:card',
    });
  }

  return {
    title: title,
    meta: baseMeta,
  };
}

/**
 * Generate social media meta tags for owner pages
 *
 * @param ownerId - The owner ID (e.g., 'depaul', 'uchicago')
 * @param ownerName - The display name of the owner (e.g., 'DePaul University')
 * @param description - Description for the owner
 */
export function generateOwnerSocialMeta(
  ownerId: string,
  ownerName: string,
  description?: string,
): PageSocialMetaResult {
  const title = `${ownerName} Buildings`;
  const defaultDescription = `Explore emissions and energy efficiency data for buildings owned by
    ${ownerName}.`;
  const socialImageUrl = `/social-images/owner-${ownerId}.webp`;

  const baseMeta = [
    {
      name: 'description',
      content: description || defaultDescription,
      key: 'description',
    },
    { property: 'og:title', content: title, key: 'og:title' },
    {
      property: 'og:description',
      content: description || defaultDescription,
      key: 'og:description',
    },
    { property: 'og:type', content: 'website', key: 'og:type' },
    { property: 'og:image', content: socialImageUrl, key: 'og:image' },
    { property: 'og:image:width', content: '1200', key: 'og:image:width' },
    { property: 'og:image:height', content: '630', key: 'og:image:height' },
    { name: 'twitter:title', content: title, key: 'twitter:title' },
    {
      name: 'twitter:description',
      content: description || defaultDescription,
      key: 'twitter:description',
    },
    {
      name: 'twitter:card',
      content: 'summary_large_image',
      key: 'twitter:card',
    },
    { name: 'twitter:image', content: socialImageUrl, key: 'twitter:image' },
  ];

  return {
    title: title,
    meta: baseMeta,
  };
}
</script>