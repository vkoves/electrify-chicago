<!-- eslint-disable max-len -->
<script lang="ts">
// The function Gridsome uses to make slugs, so it should match
import slugify from '@sindresorhus/slugify';
import { IBuilding } from '../common-functions.vue';

export default {};

export interface IBuildingImage {
  // The URL we can link to for attributing the image
  attributionUrl?: string;
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
    imgUrl: BuildingImagesBase + 'art-institute.webp',
  },
  // john-g-shedd-aquarium
  '166134': {
    attributionUrl: 'https://en.wikipedia.org/wiki/File:Shedd_Aquarium_E.jpg',
    imgUrl: BuildingImagesBase + 'shedd-aquarium.webp',
  },
  // museum-of-science-and-industry
  '102460': {
    attributionUrl:
      'https://en.wikipedia.org/wiki/File:Museum_of_Science_and_Industry_(Chicago).jpg',
    imgUrl: BuildingImagesBase + 'museum-of-science-and-industry.webp',
  },

  /**
   * General Famous Buildings
   */
  // marina-towers-condominium-association
  '239096': {
    attributionUrl:
      'https://en.wikipedia.org/wiki/File:Marina_City,_Chicago,_Illinois,_Estados_Unidos,_2012-10-20,_DD_01.jpg',
    imgUrl: BuildingImagesBase + 'marina-towers.webp',
    isTall: true,
  },
  // navy-pier-inc
  '105864': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Navy_Pier_1190x1585.jpg',
    imgUrl: BuildingImagesBase + 'navy-pier.webp',
    isTall: true,
  },
  // McCormick Place
  // metropolitan-pier-and-exposition-authority
  '101551': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:20070110_McCormick_Place_(4).JPG',
    imgUrl: BuildingImagesBase + 'mccormick-place.webp',
  },
  // aqua
  '231019': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Aqua_(Building)_cropped.jpg',
    imgUrl: BuildingImagesBase + 'aqua.webp',
    isTall: true,
  },
  // willis-tower
  '103606': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Chicago_Sears_Tower.jpg',
    imgUrl: BuildingImagesBase + 'willis-tower.webp',
    isTall: true,
  },
  // the-john-hancock-center
  '100429': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:John_Hancock_Center_viewed_from_Navy_Pier.jpg',
    imgUrl: BuildingImagesBase + 'john-hancock.webp',
    isTall: true,
  },
  // merchandise-mart
  '103656': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Merchandise_Mart_080405.jpg',
    imgUrl: BuildingImagesBase + 'merchandise-mart.webp',
  },
  // the-monadnock-building
  '101567': {
    attributionUrl: 'https://goo.gl/maps/8CUXVcLq7k9uS3yr7',
    imgUrl: BuildingImagesBase + 'monadnock-building.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // Chicago Theatre
  '173598': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Chicago_Theatre_blend.jpg',
    imgUrl: BuildingImagesBase + 'chicago-theatre.webp',
    fromGoogleMaps: false,
    isTall: false,
  },
  // Rookery Building
  '103721': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Rookery_Building,_LaSalle_Street_and_Adams_Street,_Chicago,_IL.jpg',
    imgUrl: BuildingImagesBase + 'rookery-building.webp',
    fromGoogleMaps: false,
    isTall: false,
  },
  // 20 N Wacker Dr (Civic Opera)
  '101709': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Civic_Opera_House_060528.jpg',
    imgUrl: BuildingImagesBase + '20-n-wacker.webp',
    fromGoogleMaps: false,
    isTall: true,
  },
  // Adler Planetarium
  '165062': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Adler_Planetarium_Front.JPG',
    imgUrl: BuildingImagesBase + 'adler-planetarium.webp',
    fromGoogleMaps: false,
    isTall: false,
  },
  // Museum of Contemporary Art
  '165606': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:MCA_Chicago_060930.jpg',
    imgUrl: BuildingImagesBase + 'museum-of-contemporary-art.webp',
    fromGoogleMaps: false,
    isTall: false,
  },
  // Tribune Tower
  '101724': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Tribune_Tower_Chicago_2015.jpg',
    imgUrl: BuildingImagesBase + 'tribune-tower.webp',
    fromGoogleMaps: false,
    isTall: true,
  },
  // Thompson Center
  '101742': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:James_R._Thompson_Center_(162116090).jpg',
    imgUrl: BuildingImagesBase + 'thompson-center.webp',
    fromGoogleMaps: false,
    isTall: false,
  },
  // The Field Museum
  '103638': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Field_Museum_of_Natural_History.jpg',
    imgUrl: BuildingImagesBase + 'field-museum.webp',
    fromGoogleMaps: false,
    isTall: false,
  },
  // The Wrigley Building
  '101920': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Wrigley_Building_-_Chicago,_Illinois.JPG',
    imgUrl: BuildingImagesBase + 'wrigley-building.webp',
    fromGoogleMaps: false,
    isTall: true,
  },
  // 110 N. Wacker Drive
  '256782': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:110_North_Wacker_Drive,_Chicago.jpg',
    imgUrl: BuildingImagesBase + '110-n-wacker.webp',
    fromGoogleMaps: false,
    isTall: true,
  },
  // Aon Center
  '101713': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Aon_Center_2022.jpg',
    imgUrl: BuildingImagesBase + 'aon-center.webp',
    fromGoogleMaps: false,
    isTall: true,
  },
  // Auditorium Building
  '101784': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Auditorium_Building,_Michigan_Avenue,_Chicago,_IL.jpg',
    imgUrl: BuildingImagesBase + 'auditorium-building.webp',
    fromGoogleMaps: false,
    isTall: false,
  },
  // Humboldt Park Fieldhouse
  '250017': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Humboldt_Park_Field_House_(Chicago,_IL).jpg',
    imgUrl: BuildingImagesBase + 'humboldt-park-fieldhouse.webp',
    fromGoogleMaps: false,
    isTall: false,
  },
  // Edgewater Beach Apartments
  '237359': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:Edgewater_Beach_Apartments_(10127059874).jpg',
    imgUrl: BuildingImagesBase + 'edgewater-beach-apartments.webp',
    fromGoogleMaps: false,
    isTall: false,
  },
  // South Shore Cultural Center
  '250033': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:South_Shore_Cultural_Center_2.jpg',
    imgUrl: BuildingImagesBase + 'south-shore-cultural-center.webp',
    fromGoogleMaps: false,
    isTall: false,
  },
  // The National
  '103705': {
    attributionUrl: 'https://viktorkoves.com',
    imgUrl: BuildingImagesBase + 'the-national-103705.webp',
    fromGoogleMaps: false,
    isTall: true,
  },

  /**
   * Particularly Low GHG Intensity Buildings
   */
  // king-college-prep-cps
  '101572': {
    attributionUrl: 'https://goo.gl/maps/Y4AVkhcaFhuQAk5j6',
    imgUrl: BuildingImagesBase + 'king-college-prep.webp',
    fromGoogleMaps: true,
  },
  // clinton-complex-condominium-association
  '254105': {
    attributionUrl: 'https://goo.gl/maps/XdsAqhXxDBsQSGLC9',
    imgUrl: BuildingImagesBase + 'clinton-complex-condos.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // state-place-condominium-association
  '229402': {
    attributionUrl: 'https://goo.gl/maps/exkd8jYSeNUmjer99',
    imgUrl: BuildingImagesBase + 'state-place-condos.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // park-1500-lofts
  '239994': {
    attributionUrl: 'https://goo.gl/maps/3fQf99PGpCzEU1Vs6',
    imgUrl: BuildingImagesBase + 'park-1500-lofts.webp',
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
    imgUrl: BuildingImagesBase + 'crown-hall.webp',
  },
  // herman-hall
  '256427': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:IIT_Hermann_Hall_1.jpg',
    imgUrl: BuildingImagesBase + 'herman-hall.webp',
  },
  // keating-hall
  '256434': {
    attributionUrl: 'https://goo.gl/maps/nuWwajKGroNySAQU7',
    imgUrl: BuildingImagesBase + 'keating-hall.webp',
    fromGoogleMaps: true,
  },
  // tech-business-center
  '256438': {
    attributionUrl: 'https://goo.gl/maps/aT7PYiyMQzmSwQ8f6',
    imgUrl: BuildingImagesBase + 'tech-business-center.webp',
    fromGoogleMaps: true,
  },
  // iit-tower
  '256440': {
    attributionUrl: 'https://goo.gl/maps/pW2F1yfAvwKjwFL27',
    imgUrl: BuildingImagesBase + 'iit-tower.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // mc-cormick-tribune-campus-center
  '256428': {
    attributionUrl: 'https://goo.gl/maps/nnGyrZ4nZZ1oaK6J6',
    imgUrl: BuildingImagesBase + 'mccormick-tribune-campus-center.webp',
    fromGoogleMaps: true,
  },
  // IIT life-sciences-research-building
  '256439': {
    attributionUrl: 'https://goo.gl/maps/DRpUvwYquHtWFaT58',
    imgUrl: BuildingImagesBase + 'life-sciences-research.webp',
    fromGoogleMaps: true,
  },
  // John T Retalliata
  '256420': {
    attributionUrl: 'https://maps.app.goo.gl/CVX7HYd27Y3EyihB9',
    imgUrl: BuildingImagesBase + 'ID-256420-John-T-Rettaliata.webp',
    fromGoogleMaps: true,
  },

  // Automated IIT buildings
  '111290': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/iit/111290-10_West_35th_Street_60616.webp',
    fromGoogleMaps: true,
  },
  '158403': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/iit/158403-565_W_Adams_St_60661.webp',
    fromGoogleMaps: true,
  },
  '256421': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/iit/256421-3105_S_Dearborn_St_60616.webp',
    fromGoogleMaps: true,
  },
  '256423': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/iit/256423-10_W_33rd_Street_60616.webp',
    fromGoogleMaps: true,
  },
  '256424': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/iit/256424-10_W_31st_Street_60616.webp',
    fromGoogleMaps: true,
  },
  '256425': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/iit/256425-3255_S_Dearborn_Street_60616.webp',
    fromGoogleMaps: true,
  },
  '256429': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/iit/256429-60_E_32nd_Street_60616.webp',
    fromGoogleMaps: true,
  },
  '256433': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/iit/256433-3301_S_State_Street_60616.webp',
    fromGoogleMaps: true,
  },
  '256435': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/iit/256435-55_W_34th_Street_60616.web',
    fromGoogleMaps: true,
  },

  /**
   * Biggest Buildings
   */
  '103712': {
    imgUrl: BuildingImagesBase + 'ID-103712-water-tower-place.webp',
    fromGoogleMaps: true,
  },
  '244099': {
    imgUrl: BuildingImagesBase + 'ID-244099-trump-hotel.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  '158121': {
    imgUrl: BuildingImagesBase + 'ID-158121-chase-tower.webp',
    fromGoogleMaps: true,
    isTall: true,
  },

  /** Auto streetview biggest buildings */
  '100851': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/100851-600_W_Chicago_60654.webp',
    fromGoogleMaps: true,
  },
  '101715': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101715-227_W_Monroe_60606.webp',
    fromGoogleMaps: true,
  },
  '101716': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101716-311_S_Wacker_60606.webp',
    fromGoogleMaps: true,
  },
  '101717': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101717-55_E_Monroe_St_60603.webp',
    fromGoogleMaps: true,
  },
  '101718': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101718-70_W_Madison_St_60602.webp',
    fromGoogleMaps: true,
  },
  '101727': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101727-500_W_Madison_St_60661.webp',
    fromGoogleMaps: true,
  },
  '101731': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101731-175_W_Jackson_60604.webp',
    fromGoogleMaps: true,
  },
  '101735': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101735-101_N_State_St_E_60602.webp',
    fromGoogleMaps: true,
  },
  '101736': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101736-71_S_Wacker_Dr_60606.webp',
    fromGoogleMaps: true,
  },
  '101738': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101738-300_E_Randolph_60601.webp',
    fromGoogleMaps: true,
  },
  '101744': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101744-1_N_Wacker_Dr_60606.webp',
    fromGoogleMaps: true,
  },
  '101757': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101757-219_S_Dearborn_60604.webp',
    fromGoogleMaps: true,
  },
  '101770': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101770-10_S_Wacker_Dr_60606.webp',
    fromGoogleMaps: true,
  },
  '101776': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101776-151_E_Wacker_Dr_60601.webp',
    fromGoogleMaps: true,
  },
  '101801': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/101801-205_N_Michigan_Ave_60601.webp',
    fromGoogleMaps: true,
  },
  '102157': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/102157-130_E_Randolph_St_60601.webp',
    fromGoogleMaps: true,
  },
  '102285': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/102285-836_W_Wellington_Ave_60657.webp',
    fromGoogleMaps: true,
  },
  '103630': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/103630-1901_W_Harrison_St_60612.webp',
    fromGoogleMaps: true,
  },
  '103632': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/103632-251_E_Huron_St_60611.webp',
    fromGoogleMaps: true,
  },
  '103647': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/103647-135_S_LaSalle_St_60603.webp',
    fromGoogleMaps: true,
  },
  '103653': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/103653-350_N_Orleans_St_60654.webp',
    fromGoogleMaps: true,
  },
  '103689': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/103689-404_W_HARRISON_ST_60607.webp',
    fromGoogleMaps: true,
  },
  '103716': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/103716-17_E_Monroe_St_60603.webp',
    fromGoogleMaps: true,
  },
  '103745': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/103745-900_North_Michigan_60611.webp',
    fromGoogleMaps: true,
  },
  '103816': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/103816-330_N_Wabash_Av_60611.webp',
    fromGoogleMaps: true,
  },
  '112638': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/112638-1100_S_Hamilton_Ave_60612.webp',
    fromGoogleMaps: true,
  },
  '112765': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/112765-5333_N_Sheridan_Rd_60640.webp',
    fromGoogleMaps: true,
  },
  '157955': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/157955-720_S_Michigan_Ave_60605.webp',
    fromGoogleMaps: true,
  },
  '159510': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/159510-555_W_Madison_St_60661.webp',
    fromGoogleMaps: true,
  },
  '160297': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/160297-150_W_Roosevelt_Rd_60605.webp',
    fromGoogleMaps: true,
  },
  '243773': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/243773-680_N_Lake_Shore_Dr_60611.webp',
    fromGoogleMaps: true,
  },
  '250165': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/250165-322_E_Illinois_St_60611.webp',
    fromGoogleMaps: true,
  },
  '256838': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/biggest/256838-5841_S__Maryland_Ave_MC0985.webp',
    fromGoogleMaps: true,
  },

  /**
   * DePaul Buildings (auto & manual)
   */
  '101562': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/101562-1_E_Jackson_Blvd_60604.webp',
    fromGoogleMaps: true,
  },
  '101975': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/101975-14_E_Jackson_Blvd_60604.webp',
    fromGoogleMaps: true,
  },
  '103634': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/103634-25_E_Jackson_Blvd_60604.webp',
    fromGoogleMaps: true,
  },
  '119808': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/119808-1110_W_Belden_60614.webp',
    fromGoogleMaps: true,
  },
  '134779': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/134779-243_S_Wabash_Ave_60604.webp',
    fromGoogleMaps: true,
  },
  '138514': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/138514-2323_N_Sheffield_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '166264': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/166264-525_S_State_St_60605.webp',
    fromGoogleMaps: true,
  },
  '173724': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/173724-2320_N_Kenmore_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '175365': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/175365-2247_N_Halstead_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251324': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251324-2315_N_Kenmore_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251325': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251325-2311_N_Racine_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251326': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251326-2345_N_Sheffield_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251328': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251328-2350_N_Kenmore_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251331': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251331-2312_N_Clifton_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251332': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251332-2235_N_Sheffield_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251334': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251334-2325_N_Sheffield_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251335': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251335-2250_N_Sheffield_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251337': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251337-2350_N_Racine_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251338': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251338-2322_N_Kenmore_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '251925': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/251925-2219_N_Kenmore_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '254989': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/depaul/254989-2330_N_HALSTED_ST_60614.web',
    fromGoogleMaps: true,
  },
  '251330': {
    imgUrl: BuildingImagesBase + 'ID-251330-depaul-mcgowan-north.webp',
    fromGoogleMaps: true,
  },
  '251329': {
    imgUrl: BuildingImagesBase + 'ID-251329-depaul-mccabe-hall.webp',
    fromGoogleMaps: true,
  },
  '251321': {
    imgUrl: BuildingImagesBase + 'ID-251321-depaul-1150-w-fullerton.webp',
    fromGoogleMaps: true,
  },
  '251322': {
    imgUrl: BuildingImagesBase + 'ID-251322-depaul-990-w-fullerton.webp',
    fromGoogleMaps: true,
  },

  /**
   * City of Chicago Buildings
   */
  '103812': {
    imgUrl:
      BuildingImagesBase + 'city-of-chicago/ID-103812-400-w-superior.webp ',
    fromGoogleMaps: true,
  },
  '157964': {
    imgUrl:
      BuildingImagesBase +
      'city-of-chicago/ID-157964-harold-washington-library.webp ',
    fromGoogleMaps: true,
  },
  '250057': {
    imgUrl:
      BuildingImagesBase +
      'city-of-chicago/ID-250057-englewood-health-center.webp ',
    fromGoogleMaps: true,
  },
  '250058': {
    imgUrl:
      BuildingImagesBase +
      'city-of-chicago/ID-250058-mlk-community-center.webp ',
    fromGoogleMaps: true,
  },
  '250063': {
    imgUrl: BuildingImagesBase + 'city-of-chicago/ID-250063-gallery-37.webp ',
    fromGoogleMaps: true,
  },
  '250065': {
    imgUrl:
      BuildingImagesBase + 'city-of-chicago/ID-250065-sulzer-library.webp ',
    fromGoogleMaps: true,
  },
  '250068': {
    imgUrl:
      BuildingImagesBase +
      'city-of-chicago/ID-250068-police-training-academy.webp ',
    fromGoogleMaps: true,
  },
  '250115': {
    imgUrl: BuildingImagesBase + 'city-of-chicago/ID-250115-city-hall.webp',
    fromGoogleMaps: true,
  },

  /**
   * UChicago Buildings
   */
  // 6045-kenwood-building
  '172151': {
    attributionUrl: 'https://goo.gl/maps/TyJgFT4wfqyRaFtt5',
    imgUrl: BuildingImagesBase + '6045-s-kenwood.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // accelerator-high-energy-physics
  '252039': {
    attributionUrl: 'https://goo.gl/maps/gkWsHoymmwNiwDAU6',
    imgUrl: BuildingImagesBase + 'uchicago-accelerator-ellis.webp',
    fromGoogleMaps: true,
  },
  // gordon-center-for-integrative-science-gcis
  '110848': {
    attributionUrl: 'https://goo.gl/maps/wgyeibwbqyr1UdvY9',
    imgUrl: BuildingImagesBase + 'gordon-center.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // hinds-laboratory
  '173925': {
    attributionUrl: 'https://goo.gl/maps/yManrKMWU5xFEVQC8',
    imgUrl: BuildingImagesBase + 'uchicago-hinds-laboratory.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // searle-chemistry-laboratory
  '134735': {
    attributionUrl: 'https://goo.gl/maps/ME1PsC6gepn5W5Ms7',
    imgUrl: BuildingImagesBase + 'searle-chemistry-laboratory.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // william-eckhardt-research-center
  '254382': {
    attributionUrl: 'https://goo.gl/maps/GJaEQAau4odVgF2A6',
    imgUrl: BuildingImagesBase + 'william-eckhardt-research-center.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // Auto streetview
  '102455': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/102455-5807_S_Woodlawn_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '118776': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/118776-450_N_Cityfront_Plz_60611.webp',
    fromGoogleMaps: true,
  },
  '136212': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/136212-1155_E_60th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '156942': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/156942-1005_E_60th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '252036': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/252036-1101_E_56th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '252037': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/252037-5530_S_Ellis_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '252038': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/252038-5730_S_Ellis_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '252041': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/252041-970_E_58th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '252044': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/252044-1111_E_60th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '252047': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/252047-5757_S_University_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '252049': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/252049-5811___5827_S_Ellis_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '252050': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/252050-5747_S_Ellis_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '252057': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/252057-1126_E_59th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '252061': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/252061-1313_E_60th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '254181': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/254181-1414_E_59th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '254381': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/254381-5500_S_UNIVERSITY_AVE_60637.webp',
    fromGoogleMaps: true,
  },
  '256502': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/uchicago/256502-1442_E__59th_Street_60637.web',
    fromGoogleMaps: true,
  },

  /**
   * Misc. High Emitters
   */
  //
  '100867': {
    attributionUrl:
      'https://commons.wikimedia.org/wiki/File:RUMC_-_new_tower.jpg',
    imgUrl: BuildingImagesBase + 'ID-100867-Rush-Medical-Center.webp',
  },
  // digital-lakeside
  '101185': {
    attributionUrl: 'https://goo.gl/maps/1H9Wct1qprbtzNux9',
    imgUrl: BuildingImagesBase + 'digital-lakeside.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // 352-360-w-wellington-ave
  '159651': {
    attributionUrl: 'https://goo.gl/maps/cqJ8Ao4PCyKktJqW7',
    imgUrl: BuildingImagesBase + '352-w-wellington.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // lowden-homes
  '250075': {
    attributionUrl: 'https://goo.gl/maps/StosjYVtT3XjeQ8J7',
    imgUrl: BuildingImagesBase + 'lowden-homes.webp',
    fromGoogleMaps: true,
  },
  // core-site
  '131236': {
    attributionUrl: 'https://goo.gl/maps/hLejrJBazqKHTs5x9',
    imgUrl: BuildingImagesBase + 'core-site.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // digital-printer-s-row
  '168367': {
    attributionUrl: 'https://goo.gl/maps/F3dnKuzJ29cTxD6F7',
    imgUrl: BuildingImagesBase + 'digital-printers-row.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // shop-and-save-market-nagle
  '173497': {
    attributionUrl: 'https://goo.gl/maps/DRpUvwYquHtWFaT58',
    imgUrl: BuildingImagesBase + 'shop-and-save-nagle.webp',
    fromGoogleMaps: true,
  },
  // hyde-park-west-apartments
  '102854': {
    attributionUrl: 'https://goo.gl/maps/DRpUvwYquHtWFaT58',
    imgUrl: BuildingImagesBase + 'hyde-park-west-apartments.webp',
    fromGoogleMaps: true,
    isTall: true,
  },
  // salem-baptist-church-of-chicago
  '163223': {
    attributionUrl: 'https://goo.gl/maps/DRpUvwYquHtWFaT58',
    imgUrl: BuildingImagesBase + '10909-s-cottage-grove.webp',
    fromGoogleMaps: true,
  },

  /**
   * Cleanest Buildings
   */
  '159571': {
    imgUrl: BuildingImagesBase + 'ID-159571-2144-n-lincoln-park-west.webp',
    fromGoogleMaps: true,
  },
  '133242': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/133242-1444_N_ORLEANS_ST_60610.webp',
    fromGoogleMaps: true,
  },
  '232666': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/232666-600_S_Dearborn_St_60605.webp',
    fromGoogleMaps: true,
  },
  '160455': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/160455-28_E_Jackson_Blvd_60604.webp',
    fromGoogleMaps: true,
  },
  '173618': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/173618-318_W_Adams_St_60606.webp',
    fromGoogleMaps: true,
  },
  '255934': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/255934-33_S_Aberdeen_St_60607.webp',
    fromGoogleMaps: true,
  },
  '251294': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/251294-954_W_Washington_Blvd_60607.webp',
    fromGoogleMaps: true,
  },
  '172613': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/172613-2720_2730_N_Greenview_Ave_60614.webp',
    fromGoogleMaps: true,
  },
  '175686': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/175686-1001_W_BELMONT_AVE_60657.webp',
    fromGoogleMaps: true,
  },
  '102610': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/102610-420_432_W_ONTARIO_ST_60654.webp',
    fromGoogleMaps: true,
  },
  '256645': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/256645-1419_S_Wabash_Ave.webp',
    fromGoogleMaps: true,
  },
  '254527': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/254527-6321_S_Cottage_Grove_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '134136': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/134136-141_173_W_OAK_ST_60610.webp',
    fromGoogleMaps: true,
  },
  '252033': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/252033-1405_N_Washtenaw_60622.webp',
    fromGoogleMaps: true,
  },
  '151257': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/151257-2758_2768_N_MILWAUKEE_AVE_60647.webp',
    fromGoogleMaps: true,
  },
  '113706': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/113706-233_E_ERIE_ST_60611.webp',
    fromGoogleMaps: true,
  },
  '158654': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/158654-2300_N_Lincoln_Park_West_60614.webp',
    fromGoogleMaps: true,
  },
  '132489': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/132489-4537_S_DREXEL_BLVD_60653.webp',
    fromGoogleMaps: true,
  },
  '251382': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/251382-24_W_Walton_St_60610.webp',
    fromGoogleMaps: true,
  },
  '175813': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/175813-4260_N_BROADWAY_ST_60613.webp',
    fromGoogleMaps: true,
  },
  '175837': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/175837-220_E_GARFIELD_BLVD_60615.webp',
    fromGoogleMaps: true,
  },
  '257035': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/257035-2929_W_83rd_St_60652.webp',
    fromGoogleMaps: true,
  },
  '174247': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/174247-421_E_62ND_ST_60637.webp',
    fromGoogleMaps: true,
  },
  '256815': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/256815-2480_N_MILWAUKEE_AVE_60647.webp',
    fromGoogleMaps: true,
  },
  '252295': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/252295-1501_W_Belmont_Ave_60657.webp',
    fromGoogleMaps: true,
  },
  '156021': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/156021-717_N_Michigan_Ave_60611.webp',
    fromGoogleMaps: true,
  },
  '124236': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/124236-830_N_Michigan_Ave_60611.webp',
    fromGoogleMaps: true,
  },
  '113652': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/113652-233_E_Walton_Place_60611.webp',
    fromGoogleMaps: true,
  },
  '252072': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/252072-641_W_Lake_St_60661.webp',
    fromGoogleMaps: true,
  },
  '175981': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/175981-860_W_Evergreen_Ave_60642.webp',
    fromGoogleMaps: true,
  },
  '256891': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/256891-104_S_LAFLIN_ST_60607.webp',
    fromGoogleMaps: true,
  },
  '255932': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/255932-33_S_Ashland_Ave_60607.webp',
    fromGoogleMaps: true,
  },
  '250071': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/250071-900_N_Hudson_60610.webp',
    fromGoogleMaps: true,
  },
  '156750': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/156750-800_810_N_CLARK_ST_60610.webp',
    fromGoogleMaps: true,
  },
  '117024': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/117024-1830_N_WINCHESTER_AVE_60622.webp',
    fromGoogleMaps: true,
  },
  '104431': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/cleanest/104431-5948_5958_N_BROADWAY_60660.webp',
    fromGoogleMaps: true,
  },

  // New buildings from 2023 streetview imagery
  '103580': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/103580-6720_S_Cornell_Ave.webp',
    fromGoogleMaps: true,
  },
  '109191': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/109191-1020_W_Bryn_Mawr_Ave.webp',
    fromGoogleMaps: true,
  },
  '126141': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/126141-839_W__79th_Street.webp',
    fromGoogleMaps: true,
  },
  '155614': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/155614-3447_3457_W_Foster_Avenue.webp',
    fromGoogleMaps: true,
  },
  '156139': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/156139-300_N_Michigan.webp',
    fromGoogleMaps: true,
  },
  '157158': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/157158-2800_S__Ashland_Ave.webp',
    fromGoogleMaps: true,
  },
  '158061': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/158061-5700_North_Ashland_Ave.webp',
    fromGoogleMaps: true,
  },
  '165245': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/165245-2320_W_113th_Place.webp',
    fromGoogleMaps: true,
  },
  '175053': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/175053-5330_N_Damen_Ave.webp',
    fromGoogleMaps: true,
  },
  '175579': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/175579-7645_N_Sheridan_Rd.webp',
    fromGoogleMaps: true,
  },
  '175845': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/175845-2451_W_Howard_St.webp',
    fromGoogleMaps: true,
  },
  '254998': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/254998-165_W__Superior_St.webp',
    fromGoogleMaps: true,
  },
  '255003': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/255003-2211_N_Milwaukee_Ave.webp',
    fromGoogleMaps: true,
  },
  '255925': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/255925-1955_North_Richmond_Street.webp',
    fromGoogleMaps: true,
  },
  '256531': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256531-180_N__Ada_Street.webp',
    fromGoogleMaps: true,
  },
  '256534': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256534-811_W_Agatite_Avenue.webp',
    fromGoogleMaps: true,
  },
  '256542': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256542-5525_W_Diversey_Avenue.webp',
    fromGoogleMaps: true,
  },
  '256675': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256675-1750_N_Wolcott_Avenue.webp',
    fromGoogleMaps: true,
  },
  '256779': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256779-1346_W_Taylor_St.webp',
    fromGoogleMaps: true,
  },
  '256789': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256789-4022_N_Elston.webp',
    fromGoogleMaps: true,
  },
  '256795': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256795-2845_W_Belden_Avenue.webp',
    fromGoogleMaps: true,
  },
  '256805': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256805-2410_W_Pratt.webp',
    fromGoogleMaps: true,
  },
  '256886': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256886-215_N_Peoria_St.webp',
    fromGoogleMaps: true,
  },
  '256893': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256893-211_N_Harbor_Dr.webp',
    fromGoogleMaps: true,
  },
  '256894': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256894-228_W_Hill_Sr.webp',
    fromGoogleMaps: true,
  },
  '256897': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256897-1646_N__Halsted_St.webp',
    fromGoogleMaps: true,
  },
  '256898': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256898-1520_W__Harrison_Street.webp',
    fromGoogleMaps: true,
  },
  '256904': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256904-2344_S_State_St.webp',
    fromGoogleMaps: true,
  },
  '256953': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256953-532_W_Hobbie_551_W_Elm_531_W_Elm.webp',
    fromGoogleMaps: true,
  },
  '256962': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256962-30_E_Balbo_Ave.webp',
    fromGoogleMaps: true,
  },
  '256997': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/256997-400_N_Aberdeen_Street.webp',
    fromGoogleMaps: true,
  },
  '257024': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257024-1454_W_Randolph_St.webp',
    fromGoogleMaps: true,
  },
  '257030': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257030-2322_S_Canal_St.webp',
    fromGoogleMaps: true,
  },
  '257032': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257032-3460_N_Broadway_St.webp',
    fromGoogleMaps: true,
  },
  '257043': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257043-4308_S_Calument_Ave.webp',
    fromGoogleMaps: true,
  },
  '257044': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257044-808_S_Michigan_Ave.webp',
    fromGoogleMaps: true,
  },
  '257046': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257046-1400_S_Wabash_Ave.webp',
    fromGoogleMaps: true,
  },
  '257149': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257149-345_N_Morgan_St.webp',
    fromGoogleMaps: true,
  },
  '257153': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257153-1135_S_Delano_Ct_E.webp',
    fromGoogleMaps: true,
  },
  '257154': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257154-4144_N_Sheridan.webp',
    fromGoogleMaps: true,
  },
  '257161': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257161-320_South_Canal_Street.webp',
    fromGoogleMaps: true,
  },
  '257167': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257167-306_W_Erie_St.webp',
    fromGoogleMaps: true,
  },
  '257173': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257173-24_East_Washington_Street.webp',
    fromGoogleMaps: true,
  },
  '257174': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257174-725_S__Wells.webp',
    fromGoogleMaps: true,
  },
  '257175': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257175-1132_S_Jefferson_St.webp',
    fromGoogleMaps: true,
  },
  '257178': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257178-4533_W_Roscoe_St.webp',
    fromGoogleMaps: true,
  },
  '257179': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257179-2011_W_Hastings_St.webp',
    fromGoogleMaps: true,
  },
  '257180': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257180-905_W_Fulton_Street.webp',
    fromGoogleMaps: true,
  },
  '257182': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257182-6230_South_Cottage_Grove_Avenue.webp',
    fromGoogleMaps: true,
  },
  '257183': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257183-1023_East_47th_St.webp',
    fromGoogleMaps: true,
  },
  '257185': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257185-1221_W_Sherwin_Avenue.webp',
    fromGoogleMaps: true,
  },
  '257186': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257186-4431_N__Clifton.webp',
    fromGoogleMaps: true,
  },
  '257188': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257188-2928_S_Archer_Avenue.webp',
    fromGoogleMaps: true,
  },
  '257189': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257189-852_854_W__Sunnyside.webp',
    fromGoogleMaps: true,
  },
  '257191': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257191-2614_N_Emmett_Street.webp',
    fromGoogleMaps: true,
  },
  '257193': {
    imgUrl:
      BuildingImagesBase +
      'auto-streetview/new-buildings-2023/257193-4034_W_56th_St.webp',
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
