<script lang="ts">
// The function Gridsome uses to make slugs, so it should match
import slugify from '@sindresorhus/slugify';
import { IBuilding } from '../common-functions.vue';

export default {};

export interface IBuildingImage {
  // The URL we can link to for attributing the image
  attributionUrl: string;
  // The actual local image URL
  imgUrl: string;
  // Whether this image is a tall portrait style photo - assumed fall if not specified
  isTall?: boolean;
  // Whether this image is from Google Maps, which will have a custom citation See:
  // https://about.google/brand-resource-center/products-and-services/geo-guidelines/#required-attribution
  fromGoogleMaps?: boolean;
}

export interface IBuildingImages {
  [buildingSlug: string]: IBuildingImage;
}

const BuildingImagesBase = '/building-imgs/';

/**
 * Manually sourced and downloaded building images for famous buildings
 *
 * ❗Important - Make sure to only use images we have rights to use, such as those in the public
 * domain or in a share-alike.
 *
 * A few other recommendations:
 *
 * - Make the photo landscape style, cropped to 1000px wide
 * - Have extra space on the bottom for the text, but crop pretty tightly up top to save space
 * - If the image must be TALL, make it ~600px wide (e.g. Marina Towers, Aqua)
 * - Use the JPG format with 80% quality for a good compromise of file size and quality
 */
export const BuildingImages: IBuildingImages = {
  /**
   * Museums
   */
  // the-art-institute-of-chicago
  '160196': {
    attributionUrl:
      'https://en.wikipedia.org/wiki/File:Art_Institute_of_Chicago_(51575570710).jpg',
    imgUrl: BuildingImagesBase + 'art-institute.jpg',
  },
  // john-g-shedd-aquarium
  '166134': {
    attributionUrl: 'https://en.wikipedia.org/wiki/File:Shedd_Aquarium_E.jpg',
    imgUrl: BuildingImagesBase + 'shedd-aquarium.jpg',
  },
  // museum-of-science-and-industry
  '102460': {
    attributionUrl:
      'https://en.wikipedia.org/wiki/File:Museum_of_Science_and_Industry_(Chicago).jpg',
    imgUrl: BuildingImagesBase + 'museum-of-science-and-industry.jpg',
  },

  /**
   * General Famous Buildings
   */
  // marina-towers-condominium-association
  '239096': {
    attributionUrl:
      'https://en.wikipedia.org/wiki/File:Marina_City,_Chicago,_Illinois,_Estados_Unidos,_2012-10-20,_DD_01.jpg',
    imgUrl: BuildingImagesBase + 'marina-towers.jpg',
    isTall: true,
  },
  // navy-pier-inc
  '105864': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Navy_Pier_1190x1585.jpg',
    imgUrl: BuildingImagesBase + 'navy-pier.jpg',
    isTall: true,
  },
  // McCormick Place
  // metropolitan-pier-and-exposition-authority
  '101551': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:20070110_McCormick_Place_(4).JPG',
    imgUrl: BuildingImagesBase + 'mccormick-place.jpg',
  },
  // aqua
  '231019': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Aqua_(Building)_cropped.jpg',
    imgUrl: BuildingImagesBase + 'aqua.jpg',
    isTall: true,
  },
  // willis-tower
  '103606': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Chicago_Sears_Tower.jpg',
    imgUrl: BuildingImagesBase + 'willis-tower.jpg',
    isTall: true,
  },
  // the-john-hancock-center
  '100429': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:John_Hancock_Center_viewed_from_Navy_Pier.jpg',
    imgUrl: BuildingImagesBase + 'john-hancock.jpg',
    isTall: true,
  },
  // merchandise-mart
  '103656': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Merchandise_Mart_080405.jpg',
    imgUrl: BuildingImagesBase + 'merchandise-mart.jpg',
  },
  // the-monadnock-building
  '101567': {
    attributionUrl: 'https://goo.gl/maps/8CUXVcLq7k9uS3yr7',
    imgUrl: BuildingImagesBase + 'monadnock-building.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // Chicago Theatre
  '173598': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Chicago_Theatre_blend.jpg',
    imgUrl: BuildingImagesBase + 'chicago-theatre.jpg',
    fromGoogleMaps: false,
    isTall: false,
  },
  // Rookery Building
  '103721': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Rookery_Building,_LaSalle_Street_and_Adams_Street,_Chicago,_IL.jpg',
    imgUrl: BuildingImagesBase + 'rookery-building.jpg',
    fromGoogleMaps: false,
    isTall: false,
  },
  // 20 N Wacker Dr (Civic Opera)
  '101709': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Civic_Opera_House_060528.jpg',
    imgUrl: BuildingImagesBase + '20-n-wacker.jpg',
    fromGoogleMaps: false,
    isTall: true,
  },
  // Adler Planetarium
  '165062': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Adler_Planetarium_Front.JPG',
    imgUrl: BuildingImagesBase + 'adler-planetarium.jpg',
    fromGoogleMaps: false,
    isTall: false,
  },
  // Museum of Contemporary Art
  '165606': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:MCA_Chicago_060930.jpg',
    imgUrl: BuildingImagesBase + 'museum-of-contemporary-art.jpg',
    fromGoogleMaps: false,
    isTall: false,
  },
  // Tribune Tower
  '101724': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Tribune_Tower_Chicago_2015.jpg',
    imgUrl: BuildingImagesBase + 'tribune-tower.jpg',
    fromGoogleMaps: false,
    isTall: true,
  },
  // Thompson Center
  '101742': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:James_R._Thompson_Center_(162116090).jpg',
    imgUrl: BuildingImagesBase + 'thompson-center.jpg',
    fromGoogleMaps: false,
    isTall: false,
  },
  // The Field Museum
  '103638': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Field_Museum_of_Natural_History.jpg',
    imgUrl: BuildingImagesBase + 'field-museum.jpg',
    fromGoogleMaps: false,
    isTall: false,
  },
  // The Wrigley Building
  '101920': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Wrigley_Building_-_Chicago,_Illinois.JPG',
    imgUrl: BuildingImagesBase + 'wrigley-building.jpg',
    fromGoogleMaps: false,
    isTall: true,
  },
  // 110 N. Wacker Drive
  '256782': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:110_North_Wacker_Drive,_Chicago.jpg',
    imgUrl: BuildingImagesBase + '110-n-wacker.jpg',
    fromGoogleMaps: false,
    isTall: true,
  },
  // Aon Center
  '101713': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Aon_Center_2022.jpg',
    imgUrl: BuildingImagesBase + 'aon-center.jpg',
    fromGoogleMaps: false,
    isTall: true,
  },
  // Auditorium Building
  '101784': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Auditorium_Building,_Michigan_Avenue,_Chicago,_IL.jpg',
    imgUrl: BuildingImagesBase + 'auditorium-building.jpg',
    fromGoogleMaps: false,
    isTall: false,
  },
  // Humboldt Park Fieldhouse
  '250017': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Humboldt_Park_Field_House_(Chicago,_IL).jpg',
    imgUrl: BuildingImagesBase + 'humboldt-park-fieldhouse.jpg',
    fromGoogleMaps: false,
    isTall: false,
  },
  // Edgewater Beach Apartments
  '237359': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Edgewater_Beach_Apartments_(10127059874).jpg',
    imgUrl: BuildingImagesBase + 'edgewater-beach-apartments.jpg',
    fromGoogleMaps: false,
    isTall: false,
  },
  // South Shore Cultural Center
  '250033': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:South_Shore_Cultural_Center_2.jpg',
    imgUrl: BuildingImagesBase + 'south-shore-cultural-center.jpg',
    fromGoogleMaps: false,
    isTall: false,
  },
  // The National
  '103705': {
    attributionUrl: 'https://viktorkoves.com',
    imgUrl: BuildingImagesBase + 'the-national-103705.jpg',
    fromGoogleMaps: false,
    isTall: true,
  },



  /**
   * Particularly Low GHG Intensity Buildings
   */
  // king-college-prep-cps
  '101572': {
    attributionUrl: 'https://goo.gl/maps/Y4AVkhcaFhuQAk5j6',
    imgUrl: BuildingImagesBase + 'king-college-prep.jpg',
    fromGoogleMaps: true,
  },
  // clinton-complex-condominium-association
  '254105': {
    attributionUrl: 'https://goo.gl/maps/XdsAqhXxDBsQSGLC9',
    imgUrl: BuildingImagesBase + 'clinton-complex-condos.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // state-place-condominium-association
  '229402': {
    attributionUrl: 'https://goo.gl/maps/exkd8jYSeNUmjer99',
    imgUrl: BuildingImagesBase + 'state-place-condos.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // park-1500-lofts
  '239994': {
    attributionUrl: 'https://goo.gl/maps/3fQf99PGpCzEU1Vs6',
    imgUrl: BuildingImagesBase + 'park-1500-lofts.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },

  /**
   * IIT (Illinois Tech) buildings
   */
  // Crown Hall
  '256419': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:S.R._Crown_Hall.jpg',
    imgUrl: BuildingImagesBase + 'crown-hall.jpg',
  },
  // herman-hall
  '256427': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:IIT_Hermann_Hall_1.jpg',
    imgUrl: BuildingImagesBase + 'herman-hall.jpg',
  },
  // keating-hall
  '256434': {
    attributionUrl: 'https://goo.gl/maps/nuWwajKGroNySAQU7',
    imgUrl: BuildingImagesBase + 'keating-hall.jpg',
    fromGoogleMaps: true,
  },
  // tech-business-center
  '256438': {
    attributionUrl: 'https://goo.gl/maps/aT7PYiyMQzmSwQ8f6',
    imgUrl: BuildingImagesBase + 'tech-business-center.jpg',
    fromGoogleMaps: true,
  },
  // iit-tower
  '256440': {
    attributionUrl: 'https://goo.gl/maps/pW2F1yfAvwKjwFL27',
    imgUrl: BuildingImagesBase + 'iit-tower.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // mc-cormick-tribune-campus-center
  '256428': {
    attributionUrl: 'https://goo.gl/maps/nnGyrZ4nZZ1oaK6J6',
    imgUrl: BuildingImagesBase + 'mccormick-tribune-campus-center.jpg',
    fromGoogleMaps: true,
  },
  // IIT life-sciences-research-building
  '256439': {
    attributionUrl: 'https://goo.gl/maps/DRpUvwYquHtWFaT58',
    imgUrl: BuildingImagesBase + 'life-sciences-research.jpg',
    fromGoogleMaps: true,
  },

  /**
   * UChicago Buildings
   */
  // 6045-kenwood-building
  '172151': {
    attributionUrl: 'https://goo.gl/maps/TyJgFT4wfqyRaFtt5',
    imgUrl: BuildingImagesBase + '6045-s-kenwood.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // accelerator-high-energy-physics
  '252039': {
    attributionUrl: 'https://goo.gl/maps/gkWsHoymmwNiwDAU6',
    imgUrl: BuildingImagesBase + 'uchicago-accelerator-ellis.jpg',
    fromGoogleMaps: true,
  },
  // gordon-center-for-integrative-science-gcis
  '110848': {
    attributionUrl: 'https://goo.gl/maps/wgyeibwbqyr1UdvY9',
    imgUrl: BuildingImagesBase + 'gordon-center.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // hinds-laboratory
  '173925': {
    attributionUrl: 'https://goo.gl/maps/yManrKMWU5xFEVQC8',
    imgUrl: BuildingImagesBase + 'uchicago-hinds-laboratory.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // searle-chemistry-laboratory
  '134735': {
    attributionUrl: 'https://goo.gl/maps/ME1PsC6gepn5W5Ms7',
    imgUrl: BuildingImagesBase + 'searle-chemistry-laboratory.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // william-eckhardt-research-center
  '254382': {
    attributionUrl: 'https://goo.gl/maps/GJaEQAau4odVgF2A6',
    imgUrl: BuildingImagesBase + 'william-eckhardt-research-center.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },

  /**
   * Misc. High Emitters
   */
  //
  '100867': {
    attributionUrl: 'https://commons.wikimedia.org/wiki/File:RUMC_-_new_tower.jpg',
    imgUrl: BuildingImagesBase + 'ID-100867-Rush-Medical-Center.webp',
  },
  // digital-lakeside
  '101185': {
    attributionUrl: 'https://goo.gl/maps/1H9Wct1qprbtzNux9',
    imgUrl: BuildingImagesBase + 'digital-lakeside.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // 352-360-w-wellington-ave
  '159651': {
    attributionUrl: 'https://goo.gl/maps/cqJ8Ao4PCyKktJqW7',
    imgUrl: BuildingImagesBase + '352-w-wellington.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // lowden-homes
  '250075': {
    attributionUrl: 'https://goo.gl/maps/StosjYVtT3XjeQ8J7',
    imgUrl: BuildingImagesBase + 'lowden-homes.jpg',
    fromGoogleMaps: true,
  },
  // core-site
  '131236': {
    attributionUrl: 'https://goo.gl/maps/hLejrJBazqKHTs5x9',
    imgUrl: BuildingImagesBase + 'core-site.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // digital-printer-s-row
  '168367': {
    attributionUrl: 'https://goo.gl/maps/F3dnKuzJ29cTxD6F7',
    imgUrl: BuildingImagesBase + 'digital-printers-row.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // shop-and-save-market-nagle
  '173497': {
    attributionUrl: 'https://goo.gl/maps/DRpUvwYquHtWFaT58',
    imgUrl: BuildingImagesBase + 'shop-and-save-nagle.jpg',
    fromGoogleMaps: true,
  },
  // hyde-park-west-apartments
  '102854': {
    attributionUrl: 'https://goo.gl/maps/DRpUvwYquHtWFaT58',
    imgUrl: BuildingImagesBase + 'hyde-park-west-apartments.jpg',
    fromGoogleMaps: true,
    isTall: true,
  },
  // salem-baptist-church-of-chicago
  '163223': {
    attributionUrl: 'https://goo.gl/maps/DRpUvwYquHtWFaT58',
    imgUrl: BuildingImagesBase + '10909-s-cottage-grove.jpg',
    fromGoogleMaps: true,
  },
};

/**
 * A helper function to get the building image object for a given building
 */
export function getBuildingImage(building: IBuilding): IBuildingImage | null {
  const buildingSlug = slugify(building.ID as string);
  const buildingImageObj = BuildingImages[buildingSlug];

  return buildingImageObj ?? null;
}
</script>
