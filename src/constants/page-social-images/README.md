# Page Social Image Constants

The `PageSocialCard.vue` is a component we use to generate social images for pages with building
collections, with imagery from matching buildings, e.g. showing the first 8 all electric buildings
for the meta image for `all-electric`. These constants help coordinate that:

- `page-social-configs.json` - defines the available static pages with social images, including the
  titles and descriptions we show in the image, and ID, routing to `/social-card/:ID`. This is exposed
  as a JSON so the Gridsome server JS file and the Vue component can use it.

- `page-social-configs.vue` - helper functions for the social data.
