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
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/101562-1_E_Jackson_Blvd_60604.webp',
    fromGoogleMaps: true
  },
  '101975': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/101975-14_E_Jackson_Blvd_60604.webp',
    fromGoogleMaps: true
  },
  '103634': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/103634-25_E_Jackson_Blvd_60604.webp',
    fromGoogleMaps: true
  },
  '119808': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/119808-1110_W_Belden_60614.webp',
    fromGoogleMaps: true
  },
  '134779': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/134779-243_S_Wabash_Ave_60604.webp',
    fromGoogleMaps: true
  },
  '138514': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/138514-2323_N_Sheffield_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '166264': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/166264-525_S_State_St_60605.webp',
    fromGoogleMaps: true
  },
  '173724': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/173724-2320_N_Kenmore_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '175365': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/175365-2247_N_Halstead_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251324': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251324-2315_N_Kenmore_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251325': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251325-2311_N_Racine_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251326': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251326-2345_N_Sheffield_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251328': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251328-2350_N_Kenmore_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251331': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251331-2312_N_Clifton_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251332': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251332-2235_N_Sheffield_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251334': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251334-2325_N_Sheffield_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251335': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251335-2250_N_Sheffield_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251337': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251337-2350_N_Racine_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251338': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251338-2322_N_Kenmore_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '251925': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/251925-2219_N_Kenmore_Ave_60614.webp',
    fromGoogleMaps: true
  },
  '254989': {
    imgUrl: BuildingImagesBase + 'auto-streetview/depaul/254989-2330_N_HALSTED_ST_60614.web',
    fromGoogleMaps: true
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
  // Auto streetview
  '102455': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/102455-5807_S_Woodlawn_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '118776': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/118776-450_N_Cityfront_Plz_60611.webp',
    fromGoogleMaps: true,
  },
  '136212': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/136212-1155_E_60th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '156942': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/156942-1005_E_60th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '252036': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/252036-1101_E_56th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '252037': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/252037-5530_S_Ellis_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '252038': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/252038-5730_S_Ellis_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '252041': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/252041-970_E_58th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '252044': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/252044-1111_E_60th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '252047': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/252047-5757_S_University_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '252049': {
    // eslint-disable-next-line max-len
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/252049-5811___5827_S_Ellis_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '252050': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/252050-5747_S_Ellis_Ave_60637.webp',
    fromGoogleMaps: true,
  },
  '252057': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/252057-1126_E_59th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '252061': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/252061-1313_E_60th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '254181': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/254181-1414_E_59th_St_60637.webp',
    fromGoogleMaps: true,
  },
  '254381': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/254381-5500_S_UNIVERSITY_AVE_60637.webp',
    fromGoogleMaps: true,
  },
  '256502': {
    imgUrl: BuildingImagesBase + 'auto-streetview/uchicago/256502-1442_E__59th_Street_60637.web',
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
