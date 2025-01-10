<script lang="ts">
// The function Gridsome uses to make slugs, so it should match
import slugify from '@sindresorhus/slugify';
import { IBuilding } from '../common-functions.vue';

export default {};

/**
 * A file containing supplementary building info based on their slug. This can be used
 * for things like adding custom images, notes, or building owners to very important buildings
 * (e.g. the top 10 worst or best).
 */

export interface IBuildingOwner {
  key: string;
  name: string;
  nameShort: string; // Name for table view
  logoSmall?: string; // A square logo for table view
  logoLarge?: string; // Any size logo for building details
}

export interface IBuildingOwners {
  [ownerKey: string]: IBuildingOwner;
}

/**
 * An object containing the name and logos of custom flagged building owners
 */
export const BuildingOwners: IBuildingOwners = {
  depaul: {
    key: 'depaul',
    name: 'DePaul University',
    nameShort: 'DePaul',
    logoSmall: '/building-owners/depaul/logo-small.jpg',
    logoLarge: '/building-owners/depaul/logo-large.png',
  },

  iit: {
    key: 'iit',
    name: 'Illinois Institute of Technology',
    nameShort: 'Illinois Tech',
    logoSmall: '/building-owners/iit/logo-small.png',
    logoLarge: '/building-owners/iit/logo-large.svg',
  },

  uchicago: {
    key: 'uchicago',
    name: 'University of Chicago',
    nameShort: 'UChicago',
    logoSmall: '/building-owners/uchicago/uchicago-small.jpg',
    logoLarge: '/building-owners/uchicago/uchicago-large.png',
  },

  uic: {
    key: 'uic',
    name: 'University of Illinois Chicago',
    nameShort: 'UIC',
    logoSmall: '/building-owners/uic/uic-large.jpg',
    logoLarge: '/building-owners/uic/uic-large.png',
  },

  northwestern: {
    key: 'northwestern',
    name: 'Northwestern University',
    nameShort: 'Northwestern',
    logoSmall: '/building-owners/northwestern/northwestern-large.png',
    logoLarge: '/building-owners/northwestern/northwestern-large.png',
  },

  loyola: {
    key: 'loyola',
    name: 'Loyola University Chicago',
    nameShort: 'Loyola',
    logoSmall: '/building-owners/loyola/loyola-small.png',
    logoLarge: '/building-owners/loyola/loyola-large.png',
  },

  /**
   * TODO: Change logoSmall and logoLarge for the following municipalities
   */
  cps: {
    key: 'cps',
    name: 'Chicago Public Schools',
    nameShort: 'CPS',
    logoSmall: '/building-owners/cps/cps-small.png',
    logoLarge: '/building-owners/cps/cps-large.png',
  },

  cha: {
    key: 'cha',
    name: 'Chicago Housing Authority',
    nameShort: 'CHA',
    logoSmall: '/building-owners/cha/cha-small.png',
    logoLarge: '/building-owners/cha/cha-large.png',
  },

  cityofchicago: {
    key: 'cityofchicago',
    name: 'City of Chicago',
    nameShort: 'Chicago',
    logoSmall: '/building-owners/cityofchicago/cityofchicago-small.png',
    logoLarge: '/building-owners/cityofchicago/cityofchicago-large.png',
  },

  columbia: {
    key: 'columbia',
    name: 'Columbia College Chicago',
    nameShort: 'Columbia',
    logoSmall: '/building-owners/columbia/columbia-large.png',
    logoLarge: '/building-owners/columbia/columbia-large.png',
  },

  ccc: {
    key: 'ccc',
    name: 'City Colleges of Chicago',
    nameShort: 'City Colleges',
    logoSmall: '/building-owners/ccc/ccc-large.png',
    logoLarge: '/building-owners/ccc/ccc-large.png',
  },

  moody: {
    key: 'moody',
    name: 'Moody Bible Institute',
    nameShort: 'Moody Bible',
    logoSmall: '/building-owners/moody/moody-large.png',
    logoLarge: '/building-owners/moody/moody-large.png',
  },

  saic: {
    key: 'saic',
    name: 'School of the Art Institute of Chicago',
    nameShort: 'SAIC',
    logoSmall: '/building-owners/saic/saic-small.png',
    logoLarge: '/building-owners/saic/saic-large.png',
  },

  npu: {
    key: 'npu',
    name: 'North Park University',
    nameShort: 'North Park',
    logoSmall: '/building-owners/npu/npu-large.png',
    logoLarge: '/building-owners/npu/npu-large.png',
  },

  /**
   * IMPORTANT! If you add a new building owner, make sure to add it to the gridsome.server.js to
   * register the owner page, since it cannot import this file.
   */
};

export interface IBuildingCustomInfo {
  owner?: string; // key from BuildingOwners
  links?: Array<ILink>;
  tags?: Array<BuildingTags>;
}

export interface ILink {
  url: string;
  text: string;
}

/**
 * Custom Tags for associating groups of buildings for later retrieval, like those that participated
 * in city programs
 * */
export enum BuildingTags {
  hasRetrofitCaseStudy = 'has-retrofit-case-study',
}

/**
 * An object containing our custom details about buildings. These are hand coded based on the
 * building ID, which is stable as the data updates (while names can change YoY)
 */
export const BuildingsCustomInfo: {
  [buildingId: string]: IBuildingCustomInfo;
} = {
  '166134': {
    links: [
      {
        url: 'https://www.sheddaquarium.org/stories/sustainability-at-shedd',
        text: 'Sustainability at Shedd | Shedd Aquarium',
      },
    ],
  },

  /**
   * City Retrofit Data (PDFs)
   */
  // Rookery Building Retrofit
  '103721': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/The%20Rookery.pdf',
        text: 'Rookery Building Retrofit Report',
      },
    ],
  },
  // Wrigley Building
  '101920': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/Wrigley.pdf',
        text: 'Wrigley Building Retrofit Report',
      },
    ],
  },
  // Institute of Cultural Affairs
  '102336': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/ICAGreenRise.pdf',
        text: 'Institute of Cultural Affairs Retrofit Report',
      },
    ],
  },

  // Sheraton Chicago Hotel & Towers
  // Listed as Sheraton Grand(Retrofit) or Sheraton Grand Chicago Riverwalk (google maps)
  '101852': {
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/TheSheraton.pdf',
        text: 'Sheraton Grand Chicago Hotel Retrofit Report',
      },
    ],
  },

  /**
   * DePaul Buildings
   * Helpful source: https://www.depaul.edu/campus-maps/Pages/default.aspx
   */
  // Mc-Gowan-North
  '251330': { owner: BuildingOwners.depaul.key },
  // Mc-Gowan-South
  '119808': { owner: BuildingOwners.depaul.key },
  // De-Paul-Center
  '101562': { owner: BuildingOwners.depaul.key },
  // Holtschneider-Performance-Center
  '254989': { owner: BuildingOwners.depaul.key },
  // Student-Center
  '251335': { owner: BuildingOwners.depaul.key },
  // Centennial-Hall
  '251326': { owner: BuildingOwners.depaul.key },
  // Sullivan Athletic Center
  '138514': { owner: BuildingOwners.depaul.key },
  // Ray Meyer Fitness and Recreation Center
  '251332': { owner: BuildingOwners.depaul.key },
  // Theatre School
  '251337': { owner: BuildingOwners.depaul.key },
  // College of Computing and Digital Media (CDM)
  '134779': { owner: BuildingOwners.depaul.key },
  // Thomas P. Levan Center
  '251338': { owner: BuildingOwners.depaul.key },
  // McCabe Hall
  '251329': { owner: BuildingOwners.depaul.key },
  // College of Education Building
  '175365': { owner: BuildingOwners.depaul.key },
  // Peter V. Byrne Hall
  '251925': { owner: BuildingOwners.depaul.key },
  // Munroe Hall
  '251331': { owner: BuildingOwners.depaul.key },
  // Seton Hall
  '251334': { owner: BuildingOwners.depaul.key },
  // Belden-Racine Hall
  '251325': { owner: BuildingOwners.depaul.key },
  // Arts & Letters Hall
  '251324': { owner: BuildingOwners.depaul.key },
  // Arthur J. Schmitt Academic Center
  '173724': { owner: BuildingOwners.depaul.key },
  // DePaul college of law
  '103634': { owner: BuildingOwners.depaul.key },
  // Richard M. and Maggie C. Daley Building
  '101975': { owner: BuildingOwners.depaul.key },
  // 990 W Fullerton Building
  '251322': { owner: BuildingOwners.depaul.key },
  // John T. Richardson Library
  '251328': {
    owner: BuildingOwners.depaul.key,
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/Richardson%20Library.pdf',
        text: 'Richardson Library Retrofit Report',
      },
    ],
  },
  // 1150 W. Fullerton Building
  '251321': { owner: BuildingOwners.depaul.key },
  // University Center Chicago
  '166264': { owner: BuildingOwners.depaul.key },

  /**
   * IIT buildings
   * Helpful source: https://en.wikipedia.org/wiki/List_of_Illinois_Institute_of_Technology_buildings
   */
  // Crown Hall
  '256419': { owner: BuildingOwners.iit.key },
  // Keating Hall
  '256434': { owner: BuildingOwners.iit.key },
  // Life Science Research Building
  '256439': { owner: BuildingOwners.iit.key },
  // Tech Business Center
  '256438': { owner: BuildingOwners.iit.key },
  // Herman Hall
  '256427': { owner: BuildingOwners.iit.key },
  // IIT Tower
  '256440': { owner: BuildingOwners.iit.key },
  // IIT Stuart School Of Business
  '158403': { owner: BuildingOwners.iit.key },
  // John T Rettaliata Engineering Center
  '256420': { owner: BuildingOwners.iit.key },
  // McCormick Tribune Campus Center
  '256428': { owner: BuildingOwners.iit.key },
  // Stuart Building
  '256424': { owner: BuildingOwners.iit.key },
  // Wishnick Hall
  '256425': { owner: BuildingOwners.iit.key },
  // Siegal Hall
  '256433': { owner: BuildingOwners.iit.key },
  // Incubator?
  '256435': { owner: BuildingOwners.iit.key },
  // Perlstein Hall
  '256423': { owner: BuildingOwners.iit.key },
  // IIT Tower
  '111290': { owner: BuildingOwners.iit.key },
  // IIT former Main building
  '103624': { owner: BuildingOwners.iit.key },
  // Gunsaulus Hall
  '256431': { owner: BuildingOwners.iit.key },
  // Carman Hall
  '256429': { owner: BuildingOwners.iit.key },
  // Pritzker Science Center
  '256421': { owner: BuildingOwners.iit.key },

  /**
   * UChicago Buildings
   * Helpful source: https://registrar.uchicago.edu/faculty-staff/classroom-scheduling/buildings-directory-2/
   */
  //Mansueto Library at UChicago
  '252064': {
    owner: BuildingOwners.uchicago.key,
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/UChicagoMansueto.pdf',
        text: 'Mansueto Library Retrofit Report',
      },
    ],
  },
  // 1155 E 60th St
  '136212': { owner: BuildingOwners.uchicago.key },
  // 5841 S Maryland Ave M C0985
  '256838': { owner: BuildingOwners.uchicago.key },
  // 6045 Kenwood Building
  '172151': { owner: BuildingOwners.uchicago.key },
  // Accelerator High Energy Physics
  '252039': { owner: BuildingOwners.uchicago.key },
  // Gordon Center For Integrative Science Gcis
  '110848': { owner: BuildingOwners.uchicago.key },
  // Hinds Laboratory
  '173925': { owner: BuildingOwners.uchicago.key },
  // Jones Laboratory
  '252050': { owner: BuildingOwners.uchicago.key },
  // Searle Chemistry Laboratory
  '134735': { owner: BuildingOwners.uchicago.key },
  // William Eckhardt Research Center
  '254382': { owner: BuildingOwners.uchicago.key },
  // Ratner Athletics Center
  '252037': { owner: BuildingOwners.uchicago.key },
  // Crerar Library
  '252038': { owner: BuildingOwners.uchicago.key },
  // Renee Granville Grossman Residential Commons
  '252043': { owner: BuildingOwners.uchicago.key },
  // Campus Residential North Commons
  '254381': { owner: BuildingOwners.uchicago.key },
  // Burton Judson Courts
  '156942': { owner: BuildingOwners.uchicago.key },
  '254181': { owner: BuildingOwners.uchicago.key },
  '252047': { owner: BuildingOwners.uchicago.key },
  // Bookstore!
  '252041': { owner: BuildingOwners.uchicago.key },
  // Booth School
  '102455': { owner: BuildingOwners.uchicago.key },
  // Cobb Hall
  '252049': { owner: BuildingOwners.uchicago.key },
  // Laird Bell Law Quadrangle
  '252044': { owner: BuildingOwners.uchicago.key },
  // Kersten Physics Teaching Center
  '252040': { owner: BuildingOwners.uchicago.key },
  // Gleacher Center
  '118776': { owner: BuildingOwners.uchicago.key },
  // Social Science Research Building
  '252057': { owner: BuildingOwners.uchicago.key },
  // Max Palevsky Residential Commons/Bartlett Commons
  '252036': { owner: BuildingOwners.uchicago.key },
  // 1156 E 61st St
  '256812': { owner: BuildingOwners.uchicago.key },
  // Breckinridge House
  '256502': { owner: BuildingOwners.uchicago.key },
  // Chapin Hall
  '252061': { owner: BuildingOwners.uchicago.key },

  /**
   * UIC Buildings
   *
   * See official summary, ignore leased buildings:
   * https://fimweb.fim.uic.edu/BuildingsData.aspx
   */
  // University Hall
  '251339': { owner: BuildingOwners.uic.key },
  // UIC College of Law, 304 S State (or 300 S State)
  '251220': { owner: BuildingOwners.uic.key },

  /**
   * Northwestern Buildings
   * Helpful source: https://maps.northwestern.edu/chicago
   */
  // 303 E Superior Street (Lurie Medical Research Center)
  '256405': {
    owner: BuildingOwners.northwestern.key,
    tags: [BuildingTags.hasRetrofitCaseStudy],
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/Northwestern%20Lurie.pdf',
        text: 'Lurie Medical Research Center - 303 E Superior St Retrofit Report',
      },
    ],
  },
  // 320 E Superior Street
  '256408': { owner: BuildingOwners.northwestern.key },
  // 300 E Superior Street
  '256410': { owner: BuildingOwners.northwestern.key },
  // NMH Olson Pavilion
  '103748': { owner: BuildingOwners.northwestern.key },
  // Northwestern University Chicago Campus
  '101840': { owner: BuildingOwners.northwestern.key },
  // Morton Medical Research Building
  '256409': { owner: BuildingOwners.northwestern.key },
  // Pritzker School of Law, 375 E Chicago Ave
  '256406': { owner: BuildingOwners.northwestern.key },
  // 345 E. Superior
  '101890': { owner: BuildingOwners.northwestern.key },
  // Wieboldt Hall, 340 E. Superior
  '256407': { owner: BuildingOwners.northwestern.key },
  // Chicago Campus 2, Feinberg Pavilion, 251 E Huron St
  '103632': { owner: BuildingOwners.northwestern.key },

  // Prentice Women's Hospital, 250 E Superior St
  '103615': { owner: BuildingOwners.northwestern.key },
  // NMH Arkes Family Pavilion, 676 N St Clair St
  '103684': { owner: BuildingOwners.northwestern.key },
  // 8792, Feinberg School of Medicine, 303 E Chicago Ave
  '256411': { owner: BuildingOwners.northwestern.key },

  /**
   * Loyola University
   *
   * See campus maps: https://www.luc.edu/welcomeweek/campusmaps/
   */
  // Damen Student Cetner
  '254161': { owner: BuildingOwners.loyola.key },
  // Corbow Law Center
  '101971': { owner: BuildingOwners.loyola.key },
  // Quinlan Life Sciences
  '254168': { owner: BuildingOwners.loyola.key },
  // Norville Center
  '254171': { owner: BuildingOwners.loyola.key },
  // Mundelein Center
  '102408': { owner: BuildingOwners.loyola.key },
  // Halas Recreation Center
  '254386': { owner: BuildingOwners.loyola.key },
  // Crown Center
  '254166': { owner: BuildingOwners.loyola.key },
  // Flanner Hall
  '158842': { owner: BuildingOwners.loyola.key },
  // de Nobili Hall
  '254169': { owner: BuildingOwners.loyola.key },
  // Maguire Hall
  '254163': { owner: BuildingOwners.loyola.key },
  // Simpson Living Learning Center
  '254167': { owner: BuildingOwners.loyola.key },
  // Fordham Hall
  '103681': { owner: BuildingOwners.loyola.key },
  // Sullivan Center
  '173858': { owner: BuildingOwners.loyola.key },
  // Campion Hall
  '254165': { owner: BuildingOwners.loyola.key },
  // Regis Hall
  '254172': { owner: BuildingOwners.loyola.key },
  // Cudahy Library
  '254164': { owner: BuildingOwners.loyola.key },
  // Lewis Towers
  '174182': { owner: BuildingOwners.loyola.key },
  // Santa Clara Hall
  '161053': { owner: BuildingOwners.loyola.key },
  // BVM Hall/IES
  '175895': { owner: BuildingOwners.loyola.key },
  // San Francisco Hall
  '254170': { owner: BuildingOwners.loyola.key },
  // Mertz Hall - CFSU
  '254162': { owner: BuildingOwners.loyola.key },
  // Baumhart Hall
  '160412': { owner: BuildingOwners.loyola.key },
  // Cuneo Hall
  '254160': { owner: BuildingOwners.loyola.key },
  // Bellarmine Hall
  '173888': { owner: BuildingOwners.loyola.key },
  // Fairfield Hall
  '105533': { owner: BuildingOwners.loyola.key },
  // Schreiber Center
  '254355': { owner: BuildingOwners.loyola.key },

  /**
   * CPS
   * Helpful source: main data set, schools tagged wit '-CPS'.
   * Also manually added selective enrollment schools
   */
  // Thorp Scholastic Academy, Ole A
  '251757': { owner: BuildingOwners.cps.key },
  // Lloyd Elementary
  '251714': { owner: BuildingOwners.cps.key },
  // Rudolph, Wilma Elementary Learning Center/ Hope Institute
  '166122': { owner: BuildingOwners.cps.key },
  // Smyser
  '251889': { owner: BuildingOwners.cps.key },
  // Englewood Academy HS
  '100533': { owner: BuildingOwners.cps.key },
  // Madero Middle
  '251451': { owner: BuildingOwners.cps.key },
  // Linne Elementary
  '251416': { owner: BuildingOwners.cps.key },
  // Durkin Park Elementary
  '251898': { owner: BuildingOwners.cps.key },
  // Ariel Elemenentary
  '251574': { owner: BuildingOwners.cps.key },
  // Ravenswood Elementary
  '251668': { owner: BuildingOwners.cps.key },
  // Clay Elementary, Henry
  '251593': { owner: BuildingOwners.cps.key },
  // Mayo Elementary
  '251429': { owner: BuildingOwners.cps.key },
  // Taylor, Douglas
  '251588': { owner: BuildingOwners.cps.key },
  // Bradwell Arts & Sciences Elementary
  '251698': { owner: BuildingOwners.cps.key },
  // Frazier International Magnet
  '251491': { owner: BuildingOwners.cps.key },
  // Gary Elementary
  '251651': { owner: BuildingOwners.cps.key },
  // Cooper Dual Language Academy
  '251683': { owner: BuildingOwners.cps.key },
  // Clissold Elementary
  '251408': { owner: BuildingOwners.cps.key },
  // Hubbard HS
  '100631': { owner: BuildingOwners.cps.key },
  // Pulaski Fine Arts Academy, Casimir
  '251518': { owner: BuildingOwners.cps.key },
  // Mozart
  '251600': { owner: BuildingOwners.cps.key },
  // Neil Elementary, Jane A
  '251401': { owner: BuildingOwners.cps.key },
  // Pasteur Elementary
  '251530': { owner: BuildingOwners.cps.key },
  // Nightingale Elementary
  '251692': { owner: BuildingOwners.cps.key },
  // Esmond Elementary
  '251488': { owner: BuildingOwners.cps.key },
  // Burr Elementary, Jonathan
  '251404': { owner: BuildingOwners.cps.key },
  // Reilly Es
  '251541': { owner: BuildingOwners.cps.key },
  // Tams Building
  '251352': { owner: BuildingOwners.cps.key },
  // Altgeld Elementary
  '251536': { owner: BuildingOwners.cps.key },
  // Washington Elementary, Harold
  '251461': { owner: BuildingOwners.cps.key },
  // Hendricks C A, Thomas A
  '251389': { owner: BuildingOwners.cps.key },
  // Park Manor Elementary
  '251399': { owner: BuildingOwners.cps.key },
  // Castellanos Elementary
  '251563': { owner: BuildingOwners.cps.key },
  // Peck Elementary
  '251544': { owner: BuildingOwners.cps.key },
  // Foster Park Elementary
  '251447': { owner: BuildingOwners.cps.key },
  // Nash Elementary, Henry H
  '251607': { owner: BuildingOwners.cps.key },
  // New Field Primary
  '251561': { owner: BuildingOwners.cps.key },
  // Hedges Elementary
  '251652': { owner: BuildingOwners.cps.key },
  // Peirce Sch Of Intl Studies
  '251687': { owner: BuildingOwners.cps.key },
  // Chicago Military Academy-Bronzeville
  '251690': { owner: BuildingOwners.cps.key },
  // Vaughn Occupational HS
  '251568': { owner: BuildingOwners.cps.key },
  // Nixon
  '251595': { owner: BuildingOwners.cps.key },
  // Polaris Charter Academy Elementary School - CPS
  '251508': { owner: BuildingOwners.cps.key },
  // Skinner North / Schiller Middle
  '251517': { owner: BuildingOwners.cps.key },
  // Henry Elementary, Patrick
  '251576': { owner: BuildingOwners.cps.key },
  // Locke Elementary
  '251657': { owner: BuildingOwners.cps.key },
  // Hitch Elementary
  '251418': { owner: BuildingOwners.cps.key },
  // Armstrong Intl Studies Elementary
  '251704': { owner: BuildingOwners.cps.key },
  // Jensen Scholastic Academy - CPS
  '251476': { owner: BuildingOwners.cps.key },
  // Hayt Elementary, Stephen K
  '251665': { owner: BuildingOwners.cps.key },
  // Sawyer Elementary
  '251553': { owner: BuildingOwners.cps.key },
  // U Of Chicago Charter- Donoghue
  '251535': { owner: BuildingOwners.cps.key },
  // Clemente Community Academy HS
  '100002': { owner: BuildingOwners.cps.key },
  // Fenger Achievement Academy
  '250043': { owner: BuildingOwners.cps.key },
  // Calmeca Fine Arts
  '251634': { owner: BuildingOwners.cps.key },
  // Miles Davis Elementary
  '251628': { owner: BuildingOwners.cps.key },
  // Walsh, John A
  '251760': { owner: BuildingOwners.cps.key },
  // Dewey Academy Of Fine Arts
  '251409': { owner: BuildingOwners.cps.key },
  // John Whistler Elementary
  '251406': { owner: BuildingOwners.cps.key },
  // Parkside Elementary Academy
  '161872': { owner: BuildingOwners.cps.key },
  // Deneen Elementary, Charles S
  '251584': { owner: BuildingOwners.cps.key },
  // Avalon Park Elementary
  '251581': { owner: BuildingOwners.cps.key },
  // Rogers Elementary
  '251755': { owner: BuildingOwners.cps.key },
  // Sabin Magnet CPS
  '251906': { owner: BuildingOwners.cps.key },
  // Schubert
  '251762': { owner: BuildingOwners.cps.key },
  // Norwood Park Elementary
  '251367': { owner: BuildingOwners.cps.key },
  // Carver Millitary Academy
  '102587': { owner: BuildingOwners.cps.key },
  // Higgins C A
  '161901': { owner: BuildingOwners.cps.key },
  // Jenner, Edward Elementary Academy Of The Arts
  '251556': { owner: BuildingOwners.cps.key },
  // Budlong Elementary, Lyman A
  '251617': { owner: BuildingOwners.cps.key },
  // Region 4 Office
  '251896': { owner: BuildingOwners.cps.key },
  // Beaubien Elementary
  '251644': { owner: BuildingOwners.cps.key },
  // Albany Park Multicultural Academy
  '251626': { owner: BuildingOwners.cps.key },
  // Ross Elementary (Cockrell Cpc)
  '251886': { owner: BuildingOwners.cps.key },
  // Greeley Elementary
  '251388': { owner: BuildingOwners.cps.key },
  // Hurley, Edward N
  '251377': { owner: BuildingOwners.cps.key },
  // Jamieson Elementary
  '251502': { owner: BuildingOwners.cps.key },
  // Bouchet Elementary Acad
  '251619': { owner: BuildingOwners.cps.key },
  // Spry Community Elementary
  '251437': { owner: BuildingOwners.cps.key },
  // Stem Magnet Academy / Old Thomas Jefferson
  '251887': { owner: BuildingOwners.cps.key },
  // Cather
  '251384': { owner: BuildingOwners.cps.key },
  // Amundsen HS
  '251745': { owner: BuildingOwners.cps.key },
  // Curie Metropolitan HS
  '100256': { owner: BuildingOwners.cps.key },
  // Senn Achievement Academy
  '102409': { owner: BuildingOwners.cps.key },
  // Revere Elementary
  '251604': { owner: BuildingOwners.cps.key },
  // Julian HS
  '250047': { owner: BuildingOwners.cps.key },
  // Moos Elementary
  '251695': { owner: BuildingOwners.cps.key },
  // Mather HS
  '251724': { owner: BuildingOwners.cps.key },
  // Coles Model For Excellence
  '251550': { owner: BuildingOwners.cps.key },
  // Ray Elementary
  '251884': { owner: BuildingOwners.cps.key },
  // Grant Campus
  '251694': { owner: BuildingOwners.cps.key },
  // Hale Elementary, Nathan
  '251394': { owner: BuildingOwners.cps.key },
  // NortHigh School ide College Prep HS
  '251746': { owner: BuildingOwners.cps.key },
  // Andrew Jackson Language Academy - CPS
  '251478': { owner: BuildingOwners.cps.key },
  // Daley
  '251509': { owner: BuildingOwners.cps.key },
  // Carter Elementary
  '251564': { owner: BuildingOwners.cps.key },
  // Ames Middle
  '251684': { owner: BuildingOwners.cps.key },
  // Gillespie Elementary
  '251580': { owner: BuildingOwners.cps.key },
  // Sexton
  '251464': { owner: BuildingOwners.cps.key },
  // Ninos Heroes Academic
  '161305': { owner: BuildingOwners.cps.key },
  // Dyett HS
  '251726': { owner: BuildingOwners.cps.key },
  // Burnside Scholastic Academy
  '251661': { owner: BuildingOwners.cps.key },
  // Mccormick
  '251521': { owner: BuildingOwners.cps.key },
  // Richards Career Academy HS
  '251455': { owner: BuildingOwners.cps.key },
  // National Teachers Academy
  '251715': { owner: BuildingOwners.cps.key },
  // Volta Elementary, Alessandro
  '251709': { owner: BuildingOwners.cps.key },
  // Farnsworth Elementary
  '251425': { owner: BuildingOwners.cps.key },
  // Sutherland Elementary, Elizabeth H
  '251666': { owner: BuildingOwners.cps.key },
  // Key Elementary
  '251527': { owner: BuildingOwners.cps.key },
  // Burley Elementary, Augustus H
  '251385': { owner: BuildingOwners.cps.key },
  // Brunson Math & Science
  '251623': { owner: BuildingOwners.cps.key },
  // Steinmetz Academic Center HS
  '250052': { owner: BuildingOwners.cps.key },
  // Trumbull Elementary, Lyman
  '251664': { owner: BuildingOwners.cps.key },
  // Clark Academic Prep HS
  '251710': { owner: BuildingOwners.cps.key },
  // Shoop Acad Of Math/Science/Tech
  '251753': { owner: BuildingOwners.cps.key },
  // Chappell, Eliza Elementary
  '251532': { owner: BuildingOwners.cps.key },
  // Faraday Elementary, Michael
  '251403': { owner: BuildingOwners.cps.key },
  // Waters Fine Arts
  '251393': { owner: BuildingOwners.cps.key },
  // Prussing Elementary, Ernst
  '251633': { owner: BuildingOwners.cps.key },
  // Hibbard
  '251731': { owner: BuildingOwners.cps.key },
  // DuSable Campus
  '101199': { owner: BuildingOwners.cps.key },
  // Eberhart Elementary
  '251732': { owner: BuildingOwners.cps.key },
  // Tilden HS
  '250054': { owner: BuildingOwners.cps.key },
  // Marshall Middle
  '251744': { owner: BuildingOwners.cps.key },
  // Cuffe Math/Science/Tech Academy
  '251522': { owner: BuildingOwners.cps.key },
  // Stowe
  '251489': { owner: BuildingOwners.cps.key },
  // Fuller
  '251582': { owner: BuildingOwners.cps.key },
  // Barton Elementary
  '251572': { owner: BuildingOwners.cps.key },
  // Chase Elementary
  '251910': { owner: BuildingOwners.cps.key },
  // Cook Elementary
  '251654': { owner: BuildingOwners.cps.key },
  // Juarez Com Academy HS
  '251751': { owner: BuildingOwners.cps.key },
  // Beasley Academic Magnet
  '251696': { owner: BuildingOwners.cps.key },
  // Gunsaulus Scholastic Academy
  '251608': { owner: BuildingOwners.cps.key },
  // Henson Elementary, Matthew A
  '251428': { owner: BuildingOwners.cps.key },
  // Bennett Elementary
  '251439': { owner: BuildingOwners.cps.key },
  // Langston Hughes Es
  '251621': { owner: BuildingOwners.cps.key },
  // Lavizzo Elementary - CPS
  '251557': { owner: BuildingOwners.cps.key },
  // Herzl
  '251707': { owner: BuildingOwners.cps.key },
  // Mahalia Jackson Elementary
  '251469': { owner: BuildingOwners.cps.key },
  // Phillip Murray Elementary Academy
  '251754': { owner: BuildingOwners.cps.key },
  // Palmer Elementary, John M
  '251520': { owner: BuildingOwners.cps.key },
  // West Ridge Es
  '251370': { owner: BuildingOwners.cps.key },
  // Owens
  '251351': { owner: BuildingOwners.cps.key },
  // South Loop
  '251878': { owner: BuildingOwners.cps.key },
  // King College Prep
  '101572': { owner: BuildingOwners.cps.key },
  // Lara Academy- CPS
  '251445': { owner: BuildingOwners.cps.key },
  // Barry
  '251526': { owner: BuildingOwners.cps.key },
  // Crane Achievement Academy
  '250042': { owner: BuildingOwners.cps.key },
  // Morgan Park HS
  '100418': { owner: BuildingOwners.cps.key },
  // Bell Elementary
  '251585': { owner: BuildingOwners.cps.key },
  // Pickard Elementary, Josiah L
  '251390': { owner: BuildingOwners.cps.key },
  // De Diego Community Academy
  '156414': { owner: BuildingOwners.cps.key },
  // Mckay, Francis M
  '251693': { owner: BuildingOwners.cps.key },
  // Inter- American Magnet
  '161628': { owner: BuildingOwners.cps.key },
  // Brown Elementary, William H
  '251432': { owner: BuildingOwners.cps.key },
  // Canty Elementary, Arthur E
  '251392': { owner: BuildingOwners.cps.key },
  // Clinton, Dewitt
  '251676': { owner: BuildingOwners.cps.key },
  // SoutHigh School ide Occupational Academy HS
  '251613': { owner: BuildingOwners.cps.key },
  // Lafayette Elementary
  '251720': { owner: BuildingOwners.cps.key },
  // Garvey Elementary
  '250044': { owner: BuildingOwners.cps.key },
  // Whitney
  '251761': { owner: BuildingOwners.cps.key },
  // Bethune Elementary
  '251493': { owner: BuildingOwners.cps.key },
  // Back Of The Yard
  '251873': { owner: BuildingOwners.cps.key },
  // Tonti
  '251880': { owner: BuildingOwners.cps.key },
  // Zapata Elementary Academy, Emiliano
  '251863': { owner: BuildingOwners.cps.key },
  // Ellington Elementary
  '251656': { owner: BuildingOwners.cps.key },
  // Dett
  '251402': { owner: BuildingOwners.cps.key },
  // Williams Multiplex Elementary
  '251877': { owner: BuildingOwners.cps.key },
  // Irving Elementary - CPS
  '251381': { owner: BuildingOwners.cps.key },
  // Lincoln Park HS
  '167562': { owner: BuildingOwners.cps.key },
  // Banneker Elementary
  '251427': { owner: BuildingOwners.cps.key },
  // Kelvyn Park HS
  '251734': { owner: BuildingOwners.cps.key },
  // Otis Elementary
  '251612': { owner: BuildingOwners.cps.key },
  // Irving Park Middle
  '251358': { owner: BuildingOwners.cps.key },
  // Perspectives Middle Academy
  '100572': { owner: BuildingOwners.cps.key },
  // Ryder, William H
  '251649': { owner: BuildingOwners.cps.key },
  // Mt Greenwood Elementary
  '251424': { owner: BuildingOwners.cps.key },
  // Sherwood Elementary
  '251671': { owner: BuildingOwners.cps.key },
  // Lathrop Elementary, Julia C
  '251413': { owner: BuildingOwners.cps.key },
  // Hammond Elementary
  '251396': { owner: BuildingOwners.cps.key },
  // Prieto, Dr Jorge Elementary
  '251865': { owner: BuildingOwners.cps.key },
  // Curtis Elementary
  '251632': { owner: BuildingOwners.cps.key },
  // Dulles
  '251490': { owner: BuildingOwners.cps.key },
  // Ebinger Elementary
  '251421': { owner: BuildingOwners.cps.key },
  // Saucedo Elementary Academy - CPS
  '251890': { owner: BuildingOwners.cps.key },
  // Haines Elementary
  '251504': { owner: BuildingOwners.cps.key },
  // Mark Skinner Elementary
  '251500': { owner: BuildingOwners.cps.key },
  // Roosevelt HS, Theodore
  '157767': { owner: BuildingOwners.cps.key },
  // Disney Magnet
  '102331': { owner: BuildingOwners.cps.key },
  // Brighton Park-Old Building
  '251511': { owner: BuildingOwners.cps.key },
  // Oglesby
  '251528': { owner: BuildingOwners.cps.key },
  // Gale Community Academy, Stephen F
  '251706': { owner: BuildingOwners.cps.key },
  // Monroe Elementary
  '251669': { owner: BuildingOwners.cps.key },
  // Hefferan Elementary
  '251405': { owner: BuildingOwners.cps.key },
  // Lincoln Elementary
  '251463': { owner: BuildingOwners.cps.key },
  // Schneider
  '251858': { owner: BuildingOwners.cps.key },
  // Payton College Prep HS
  '251721': { owner: BuildingOwners.cps.key },
  // Stone Scholastic Academy
  '251691': { owner: BuildingOwners.cps.key },
  // Rosenwald, Carroll Branch
  '251531': { owner: BuildingOwners.cps.key },
  // Mcauliffe
  '251570': { owner: BuildingOwners.cps.key },
  // Best Practice - CPS; Chicago Bulls College Prep
  '251866': { owner: BuildingOwners.cps.key },
  // Goudy Elementary, William C
  '251610': { owner: BuildingOwners.cps.key },
  // Kennedy HS / Kinzie ES
  '250048': { owner: BuildingOwners.cps.key },
  // Chicago HS for Agricultural - CPS
  '250040': { owner: BuildingOwners.cps.key },
  // Mason Elementary
  '167641': { owner: BuildingOwners.cps.key },
  // Edgebrook Elementary
  '251893': { owner: BuildingOwners.cps.key },
  // Emmet Elementary
  '251485': { owner: BuildingOwners.cps.key },
  // Ruiz Elementary - CPS
  '251482': { owner: BuildingOwners.cps.key },
  // Morton Elementary Career Academy - CPS
  '251480': { owner: BuildingOwners.cps.key },
  // Goethe Elementary, J W Von
  '251523': { owner: BuildingOwners.cps.key },
  // Beidler Elementary
  '251566': { owner: BuildingOwners.cps.key },
  // Smyth
  '251903': { owner: BuildingOwners.cps.key },
  // Yale
  '251705': { owner: BuildingOwners.cps.key },
  // Kenwood Acad HS
  '106819': { owner: BuildingOwners.cps.key },
  // School Of Leadership HS
  '251618': { owner: BuildingOwners.cps.key },
  // Evergreen Academy Middle
  '251347': { owner: BuildingOwners.cps.key },
  // Lewis Elementary, Leslie
  '251689': { owner: BuildingOwners.cps.key },
  // Cameron Elementary- CPS
  '208356': { owner: BuildingOwners.cps.key },
  // Scammon, Jonathan Y
  '251900': { owner: BuildingOwners.cps.key },
  // Dixon, Arthur
  '251565': { owner: BuildingOwners.cps.key },
  // Darwin
  '251677': { owner: BuildingOwners.cps.key },
  // Kelly HS
  '168174': { owner: BuildingOwners.cps.key },
  // Onahan Elementary, William J
  '251473': { owner: BuildingOwners.cps.key },
  // Washington HS , George
  '251368': { owner: BuildingOwners.cps.key },
  // Falconer Elementary
  '251719': { owner: BuildingOwners.cps.key },
  // Ace Technical Charter HS
  '117702': { owner: BuildingOwners.cps.key },
  // Suder Campus Montessori
  '251737': { owner: BuildingOwners.cps.key },
  // Sheridan Elementary
  '251391': { owner: BuildingOwners.cps.key },
  // Swift Specialty
  '251759': { owner: BuildingOwners.cps.key },
  // Harlan Comm Academy
  '159000': { owner: BuildingOwners.cps.key },
  // Manierre Elementary
  '251452': { owner: BuildingOwners.cps.key },
  // Young Elementary
  '251888': { owner: BuildingOwners.cps.key },
  // Holden Elementary
  '251583': { owner: BuildingOwners.cps.key },
  // Agassiz Elementary
  '251407': { owner: BuildingOwners.cps.key },
  // Harper HS
  '110223': { owner: BuildingOwners.cps.key },
  // Dvorak Math/Science/Tech Academy - CPS
  '251466': { owner: BuildingOwners.cps.key },
  // Powell Elementary Paideia Acad
  '251348': { owner: BuildingOwners.cps.key },
  // Delano Elementary, Edward C
  '251575': { owner: BuildingOwners.cps.key },
  // Mariano Azuela
  '251624': { owner: BuildingOwners.cps.key },
  // Reavis Specialty Elementary
  '251411': { owner: BuildingOwners.cps.key },
  // Stockton Specialty, Joseph
  '251438': { owner: BuildingOwners.cps.key },
  // Sherman Elementary, William T
  '251912': { owner: BuildingOwners.cps.key },
  // Farragut Career Academy HS
  '100598': { owner: BuildingOwners.cps.key },
  // Wadsworth - CPS
  '251477': { owner: BuildingOwners.cps.key },
  // Mireles Academy, Arnold
  '105288': { owner: BuildingOwners.cps.key },
  // Pilsen Comm Academy
  '251908': { owner: BuildingOwners.cps.key },
  // Dumas Elementary
  '251414': { owner: BuildingOwners.cps.key },
  // Bridge Elementary, Norman
  '251479': { owner: BuildingOwners.cps.key },
  // Fort Dearborn Elementary
  '251667': { owner: BuildingOwners.cps.key },
  // Fulton Elementary
  '251605': { owner: BuildingOwners.cps.key },
  // Mitchell, Ellen
  '251373': { owner: BuildingOwners.cps.key },
  // Chopin Elementary
  '251591': { owner: BuildingOwners.cps.key },
  // Hamline Elementary
  '251573': { owner: BuildingOwners.cps.key },
  // Bronzeville Charter, Hartigan - CPS
  '251419': { owner: BuildingOwners.cps.key },
  // Pope Elementary, Nathaniel
  '251703': { owner: BuildingOwners.cps.key },
  // Metcalfe Math And Science
  '251545': { owner: BuildingOwners.cps.key },
  // Northwest Middle
  '251702': { owner: BuildingOwners.cps.key },
  // Catalyst Charter Es - Howland
  '251697': { owner: BuildingOwners.cps.key },
  // Evers Elementary, Medgar
  '251355': { owner: BuildingOwners.cps.key },
  // Ogden Elementary - CPS
  '251382': { owner: BuildingOwners.cps.key },
  // Foreman HS, Edwin G
  '251736': { owner: BuildingOwners.cps.key },
  // Christopher Elementary
  '251512': { owner: BuildingOwners.cps.key },
  // Nathan S Davis
  '251699': { owner: BuildingOwners.cps.key },
  // Marshall Metro HS
  '101039': { owner: BuildingOwners.cps.key },
  // Kanoon Magnet Elementary
  '251431': { owner: BuildingOwners.cps.key },
  // Uplift Community HS
  '251902': { owner: BuildingOwners.cps.key },
  // Columbia Explorers Elementary Academy
  '251555': { owner: BuildingOwners.cps.key },
  // Hearst Elementary
  '251638': { owner: BuildingOwners.cps.key },
  // Portage Park Elementary
  '251870': { owner: BuildingOwners.cps.key },
  // Hinton Elementary, William Augustus
  '251442': { owner: BuildingOwners.cps.key },
  // Raby HS
  '251594': { owner: BuildingOwners.cps.key },
  // Garvey Elementary, John W
  '251909': { owner: BuildingOwners.cps.key },
  // Taft HS
  '250053': { owner: BuildingOwners.cps.key },
  // Smith
  '251534': { owner: BuildingOwners.cps.key },
  // Spencer Elementary Academy
  '251648': { owner: BuildingOwners.cps.key },
  // Claremont Academy Elementary
  '251722': { owner: BuildingOwners.cps.key },
  // Von Steuben Metro Science Center
  '250055': { owner: BuildingOwners.cps.key },
  // Seward Communication Arts Academy
  '251620': { owner: BuildingOwners.cps.key },
  // Brooks College Prep. Acad - CPS
  '250038': { owner: BuildingOwners.cps.key },
  // Eric Solorio HS
  '251742': { owner: BuildingOwners.cps.key },
  // May Elementary Community Academy
  '251670': { owner: BuildingOwners.cps.key },
  // Jungman Elementary
  '251484': { owner: BuildingOwners.cps.key },
  // Charles W Earle Elementary
  '251587': { owner: BuildingOwners.cps.key },
  // Edwards Elementary
  '251601': { owner: BuildingOwners.cps.key },
  // Gray Elementary
  '251662': { owner: BuildingOwners.cps.key },
  // Nicholson Math And Science Elementary - CPS
  '251434': { owner: BuildingOwners.cps.key },
  // Kershaw Elementary, Joshua D
  '251359': { owner: BuildingOwners.cps.key },
  // Stagg Elementary, Amos A
  '251874': { owner: BuildingOwners.cps.key },
  // Langford Elementary
  '161225': { owner: BuildingOwners.cps.key },
  // Prosser Career Acad HS
  '251362': { owner: BuildingOwners.cps.key },
  // Till, Emmett Louis Math & Science
  '251640': { owner: BuildingOwners.cps.key },
  // Parker Elementary
  '117535': { owner: BuildingOwners.cps.key },
  // Orozco Elementary
  '251599': { owner: BuildingOwners.cps.key },
  // Simeon Career Academy HS
  '250051': { owner: BuildingOwners.cps.key },
  // Sandoval Elementary
  '251750': { owner: BuildingOwners.cps.key },
  // Audubon Elementary, John J - CPS
  '251474': { owner: BuildingOwners.cps.key },
  // Burbank Elementary
  '251728': { owner: BuildingOwners.cps.key },
  // Pullman Elementary, George M
  '251716': { owner: BuildingOwners.cps.key },
  // Haugan Magnet, Helge A
  '251700': { owner: BuildingOwners.cps.key },
  // Shields Main
  '251899': { owner: BuildingOwners.cps.key },
  // Songhai Learning Institute
  '251400': { owner: BuildingOwners.cps.key },
  // Tarkington School Of Excellence Es
  '251590': { owner: BuildingOwners.cps.key },
  // Ogden Intl HS
  '251860': { owner: BuildingOwners.cps.key },
  // Dodge
  '251460': { owner: BuildingOwners.cps.key },
  // Holmes Elementary
  '251467': { owner: BuildingOwners.cps.key },
  // Bateman Elementary, Newton
  '251708': { owner: BuildingOwners.cps.key },
  // Pershing West
  '251567': { owner: BuildingOwners.cps.key },
  // Hancock College Prep HS
  '251717': { owner: BuildingOwners.cps.key },
  // Goodlow Elementary Magnet
  '251440': { owner: BuildingOwners.cps.key },
  // Hanson Park
  '251616': { owner: BuildingOwners.cps.key },
  // Ruggles, Martha M
  '251486': { owner: BuildingOwners.cps.key },
  // Bowen Environmental Studies HS
  '250036': { owner: BuildingOwners.cps.key },
  // Joplin Elementary
  '251598': { owner: BuildingOwners.cps.key },
  // Ortiz De Dominguez
  '251423': { owner: BuildingOwners.cps.key },
  // Burke Elementary
  '251497': { owner: BuildingOwners.cps.key },
  // Corkery Elementary
  '251487': { owner: BuildingOwners.cps.key },
  // Bogan HS
  '100397': { owner: BuildingOwners.cps.key },
  // Irene C Hernandez
  '251678': { owner: BuildingOwners.cps.key },
  // Finkl Elementary
  '251537': { owner: BuildingOwners.cps.key },
  // South Shore International College Prep
  '251871': { owner: BuildingOwners.cps.key },
  // Brentano Math & Science Academy
  '251650': { owner: BuildingOwners.cps.key },
  // Schurz HS
  '102309': { owner: BuildingOwners.cps.key },
  // Mayer
  '251501': { owner: BuildingOwners.cps.key },
  // Laura S Ward Elementary
  '251374': { owner: BuildingOwners.cps.key },
  // Fernwood Elementary
  '251457': { owner: BuildingOwners.cps.key },
  // Ashe Elementary
  '251375': { owner: BuildingOwners.cps.key },
  // Robeson HS
  '251894': { owner: BuildingOwners.cps.key },
  // Mark Twain Elementary
  '106236': { owner: BuildingOwners.cps.key },
  // Casals Elementary
  '251459': { owner: BuildingOwners.cps.key },
  // Murphy Elementary
  '251551': { owner: BuildingOwners.cps.key },
  // Ryerson
  '251606': { owner: BuildingOwners.cps.key },
  // Graham Elementary
  '251462': { owner: BuildingOwners.cps.key },
  // Peterson Elementary
  '251506': { owner: BuildingOwners.cps.key },
  // Ashburn Community Elementary
  '251376': { owner: BuildingOwners.cps.key },
  // Bontemps Elementary
  '251361': { owner: BuildingOwners.cps.key },
  // James Ward Elementary
  '251554': { owner: BuildingOwners.cps.key },
  // Webster
  '251749': { owner: BuildingOwners.cps.key },
  // Hyde Park Academy HS
  '250045': { owner: BuildingOwners.cps.key },
  // Little Village Academy
  '251435': { owner: BuildingOwners.cps.key },
  // North Grand HS
  '251739': { owner: BuildingOwners.cps.key },
  // Lyon Elementary
  '251682': { owner: BuildingOwners.cps.key },
  // North Lawndale College Prep Charter, Collins - CPS
  '250041': { owner: BuildingOwners.cps.key },
  // Gallistel Language Academy
  '251547': { owner: BuildingOwners.cps.key },
  // Boone Elementary
  '251542': { owner: BuildingOwners.cps.key },
  // Fiske Elementary
  '251468': { owner: BuildingOwners.cps.key },
  // Nathanael Green
  '251558': { owner: BuildingOwners.cps.key },
  // Carson, Rachel Elementary
  '251420': { owner: BuildingOwners.cps.key },
  // Dunbar Vocational Acad HS
  '112188': { owner: BuildingOwners.cps.key },
  // Alcott Elementary, Louisa May
  '251365': { owner: BuildingOwners.cps.key },
  // Epic Charter Academy - CPS
  '251859': { owner: BuildingOwners.cps.key },
  // Talcott Fine Arts And Museum Academy
  '251867': { owner: BuildingOwners.cps.key },
  // Cardenas Elementary
  '251911': { owner: BuildingOwners.cps.key },
  // Jones College Prep, William - CPS
  '250046': { owner: BuildingOwners.cps.key },
  // Corliss HS
  '159005': { owner: BuildingOwners.cps.key },
  // Caldwell Math & Science
  '251450': { owner: BuildingOwners.cps.key },
  // Carnegie Elementary, Andrew
  '251456': { owner: BuildingOwners.cps.key },
  // Burnham Mathematics And Science Academy
  '251907': { owner: BuildingOwners.cps.key },
  // Hampton Fine & Performing Arts
  '251560': { owner: BuildingOwners.cps.key },
  // Marquette Elementary
  '251733': { owner: BuildingOwners.cps.key },
  // Sullivan HS, Roger C
  '158841': { owner: BuildingOwners.cps.key },
  // Lowell Elementary
  '251679': { owner: BuildingOwners.cps.key },
  // Gregory Elementary
  '251647': { owner: BuildingOwners.cps.key },
  // Air Force Academy (Abbott Elementary )
  '251524': { owner: BuildingOwners.cps.key },
  // Lake View HS
  '102365': { owner: BuildingOwners.cps.key },
  // Galileo Scholastic Academy
  '251622': { owner: BuildingOwners.cps.key },
  // Bond Elementary
  '251680': { owner: BuildingOwners.cps.key },
  // Hirsch Metropolitan HS
  '251738': { owner: BuildingOwners.cps.key },
  // Little Village HS Campus
  '157011': { owner: BuildingOwners.cps.key },
  // Beethoven Elementary
  '251559': { owner: BuildingOwners.cps.key },
  // Manley Career Academy HS
  '101043': { owner: BuildingOwners.cps.key },
  // Okeeffe Elementary
  '251597': { owner: BuildingOwners.cps.key },
  // Chalmers
  '251417': { owner: BuildingOwners.cps.key },
  // Reinberg Elementary
  '251546': { owner: BuildingOwners.cps.key },
  // Logandale
  '251372': { owner: BuildingOwners.cps.key },
  // Depriest Elementary
  '251641': { owner: BuildingOwners.cps.key },
  // James N Thorp
  '251686': { owner: BuildingOwners.cps.key },
  // Jordan Comm
  '162360': { owner: BuildingOwners.cps.key },
  // Lindblom College Prep
  '100332': { owner: BuildingOwners.cps.key },
  // Hawthorne Elementary Academy
  '251505': { owner: BuildingOwners.cps.key },
  // Westinghouse HS
  '251891': { owner: BuildingOwners.cps.key },
  // Hope College Prepa HS
  '251729': { owner: BuildingOwners.cps.key },
  // Mcnair Academy Center, Ronald E
  '251383': { owner: BuildingOwners.cps.key },
  // Field Elementary
  '251637': { owner: BuildingOwners.cps.key },
  // Orr Academy HS
  '250049': { owner: BuildingOwners.cps.key },
  // Chicago Vocational Career Academy
  '102545': { owner: BuildingOwners.cps.key },
  // Stevenson, Adlai E
  '251577': { owner: BuildingOwners.cps.key },
  // Goldblatt Elementary, Nathan R
  '251412': { owner: BuildingOwners.cps.key },
  // Sumner Math & Science Community Acad, Charles
  '251496': { owner: BuildingOwners.cps.key },
  // Manuel Perez Elementary
  '251673': { owner: BuildingOwners.cps.key },
  // Franklin Fine Arts Center
  '251363': { owner: BuildingOwners.cps.key },
  // Randolph Elementary
  '251446': { owner: BuildingOwners.cps.key },
  // Madison Elementary
  '251443': { owner: BuildingOwners.cps.key },
  // Gage Park HS
  '251748': { owner: BuildingOwners.cps.key },
  // Nettelhorst Elementary
  '251625': { owner: BuildingOwners.cps.key },
  // Yates
  '251730': { owner: BuildingOwners.cps.key },
  // Edison Park Elementary
  '251627': { owner: BuildingOwners.cps.key },
  // Marsh Elementary
  '251397': { owner: BuildingOwners.cps.key },
  // Newberry Math/Science Academy
  '251433': { owner: BuildingOwners.cps.key },
  // James Shields Ms
  '251723': { owner: BuildingOwners.cps.key },
  // Lozano Bilingual Elementary
  '251533': { owner: BuildingOwners.cps.key },
  // Whitney Young
  '250056': { owner: BuildingOwners.cps.key },
  // Hay Community Academy, John
  '251569': { owner: BuildingOwners.cps.key },
  // Chavez, Cesar E Multicultural Academic Center Es
  '251441': { owner: BuildingOwners.cps.key },
  // Haley Elementary, Alex
  '251426': { owner: BuildingOwners.cps.key },
  // Mann Elementary
  '251611': { owner: BuildingOwners.cps.key },
  // Lawndale Community Academy
  '251660': { owner: BuildingOwners.cps.key },
  // Johnson Elementary
  '251356': { owner: BuildingOwners.cps.key },
  // Kilmer Elementary
  '251639': { owner: BuildingOwners.cps.key },
  // Crown Community Academy
  '251386': { owner: BuildingOwners.cps.key },
  // Austin Polytechical HS
  '250035': { owner: BuildingOwners.cps.key },
  // Kozminski Elementary Academy
  '251614': { owner: BuildingOwners.cps.key },
  // Gresham Elementary
  '251636': { owner: BuildingOwners.cps.key },
  // Blaine Elementary, James G
  '251642': { owner: BuildingOwners.cps.key },
  // Armour Elementary
  '251360': { owner: BuildingOwners.cps.key },
  // Pritzker Elementary, A.N
  '251735': { owner: BuildingOwners.cps.key },
  // Harvard Elemtary
  '251543': { owner: BuildingOwners.cps.key },
  // New Sullivan Elem, William K
  '251609': { owner: BuildingOwners.cps.key },
  // Gompers Fine Arts Option Elementary - CPS
  '251444': { owner: BuildingOwners.cps.key },
  // Calhoun North
  '251515': { owner: BuildingOwners.cps.key },
  // Tanner Elementary
  '251688': { owner: BuildingOwners.cps.key },
  // Lenart Regional Gifted Center
  '156999': { owner: BuildingOwners.cps.key },
  // Woodson South
  '251387': { owner: BuildingOwners.cps.key },
  // Andersen Elementary
  '251586': { owner: BuildingOwners.cps.key },
  // Belding Elementary, Hiram H - CPS
  '251475': { owner: BuildingOwners.cps.key },
  // Nobel
  '251589': { owner: BuildingOwners.cps.key },
  // Sauganash Elementary
  '251725': { owner: BuildingOwners.cps.key },
  // Kohn Elementary
  '251415': { owner: BuildingOwners.cps.key },
  // Betty Shabazz Intl Charter / Barbra A Sizemore
  '251892': { owner: BuildingOwners.cps.key },
  // Howe Elementary
  '251571': { owner: BuildingOwners.cps.key },
  // Phillips Academy HS
  '250050': { owner: BuildingOwners.cps.key },
  // Doolittle Elementary / Chi Arts
  '251655': { owner: BuildingOwners.cps.key },
  // Penn Elementary
  '251712': { owner: BuildingOwners.cps.key },
  // Camras Elementary
  '251674': { owner: BuildingOwners.cps.key },
  // Dawes Elementary
  '251513': { owner: BuildingOwners.cps.key },
  // Cleveland Elementary, Grover
  '251592': { owner: BuildingOwners.cps.key },
  // Sayre Language Academy
  '251539': { owner: BuildingOwners.cps.key },
  // Jahn World Language
  '251499': { owner: BuildingOwners.cps.key },
  // Bright, Orville T
  '251578': { owner: BuildingOwners.cps.key },
  // Otoole Elementary
  '251602': { owner: BuildingOwners.cps.key },
  // Carver Middle
  '250039': { owner: BuildingOwners.cps.key },
  // Ericson Scholastic Academy, Leif
  '251498': { owner: BuildingOwners.cps.key },
  // Henderson Elementary, CPS
  '251579': { owner: BuildingOwners.cps.key },
  // West Park Academy Of Fine Arts & Tech
  '251643': { owner: BuildingOwners.cps.key },
  // Tilton
  '251525': { owner: BuildingOwners.cps.key },
  // Wells Community Academy HS
  '156413': { owner: BuildingOwners.cps.key },
  // Frederico Garcia Lorca
  '251631': { owner: BuildingOwners.cps.key },
  // Attucks
  '251492': { owner: BuildingOwners.cps.key },
  // Goode HS
  '251872': { owner: BuildingOwners.cps.key },
  // Mcclellan Elementary
  '251395': { owner: BuildingOwners.cps.key },
  // Chicago Acad Elementary
  '101420': { owner: BuildingOwners.cps.key },
  // Hamilton Elementary, Alexander - CPS
  '251483': { owner: BuildingOwners.cps.key },
  // Morrill Math/Science Spec
  '251603': { owner: BuildingOwners.cps.key },
  // Robert Healy Elementary
  '251741': { owner: BuildingOwners.cps.key },
  // Mt Vernon Elementary
  '251548': { owner: BuildingOwners.cps.key },
  // Piccolo Specialty
  '251658': { owner: BuildingOwners.cps.key },
  // Douglass, Frederick Academy HS
  '251711': { owner: BuildingOwners.cps.key },
  // Brennemann Elementary, Joseph
  '250037': { owner: BuildingOwners.cps.key },
  // Funston, Frederick Elementary
  '251905': { owner: BuildingOwners.cps.key },
  // Libby Elementary
  '251449': { owner: BuildingOwners.cps.key },
  // Lane Tech HS
  '102363': { owner: BuildingOwners.cps.key },
  // Coonley, John C
  '251465': { owner: BuildingOwners.cps.key },
  // Mcpherson Elementary
  '251718': { owner: BuildingOwners.cps.key },
  // Lawrence Elementary
  '251516': { owner: BuildingOwners.cps.key },
  // Bass Elementary
  '251629': { owner: BuildingOwners.cps.key },
  // Lovett Elementary
  '251529': { owner: BuildingOwners.cps.key },
  // South Shore ES
  '251514': { owner: BuildingOwners.cps.key },
  // Powell
  '254099': { owner: BuildingOwners.cps.key },
  // Dugan
  '251885': { owner: BuildingOwners.cps.key },
  // Belding Earl
  '251875': { owner: BuildingOwners.cps.key },
  // NearNorthHS
  '251713': { owner: BuildingOwners.cps.key },
  // SouthLoopBrn
  '251743': { owner: BuildingOwners.cps.key },
  // Rowe
  '251364': { owner: BuildingOwners.cps.key },
  // PowellStBrdg
  '251630': { owner: BuildingOwners.cps.key },
  // Carroll-Rose
  '251562': { owner: BuildingOwners.cps.key },
  // Prodigy Wood
  '251740': { owner: BuildingOwners.cps.key },

  /**
   * CHA
   * Helpful source: https://www.thecha.org/residents/public-housing/find-public-housing
   */
  // ABLA/Brooks Homes
  '160397': { owner: BuildingOwners.cha.key },
  // 1 South Leavitt
  '256670': { owner: BuildingOwners.cha.key },
  // Ada S. Dennison-McKinley Apartments
  '250079': { owner: BuildingOwners.cha.key },
  // Albany Terrace Apts
  '250080': { owner: BuildingOwners.cha.key },
  // Alfreda Barnett Duster Apts
  '250081': { owner: BuildingOwners.cha.key },
  // Altgeld Gardens
  '250069': { owner: BuildingOwners.cha.key },
  // Archer Courts Apartments
  '105441': { owner: BuildingOwners.cha.key },
  // Armour Square Apartments
  '250082': { owner: BuildingOwners.cha.key },
  // Bridgeport Homes
  '250070': { owner: BuildingOwners.cha.key },
  // Britton Budd
  '115942': { owner: BuildingOwners.cha.key },
  // Cabrini Rowhomes
  '250071': { owner: BuildingOwners.cha.key },
  // Caroline Hedger Apartment
  '160419': { owner: BuildingOwners.cha.key },
  // Daniel Hudson Burnham Apartments
  '250083': { owner: BuildingOwners.cha.key },
  // Dearborn Plaza
  '105697': { owner: BuildingOwners.cha.key },
  // Domain Condominium
  '239679': { owner: BuildingOwners.cha.key },
  // Kenneth Campbell Apartments
  '250095': { owner: BuildingOwners.cha.key },
  // Edith Spurlock Sampson Apts
  '158668': { owner: BuildingOwners.cha.key },
  // Elizabeth Davis Apartments
  '250085': { owner: BuildingOwners.cha.key },
  // Elizabeth Wood Apartments
  '250086': { owner: BuildingOwners.cha.key },
  // Ella Flagg Young Apartments
  '159739': { owner: BuildingOwners.cha.key },
  // Fannie Emanuel
  '250087': { owner: BuildingOwners.cha.key },
  // Fountainview Apartments
  '172256': { owner: BuildingOwners.cha.key },
  // Frank O Lowden Homes
  '250075': { owner: BuildingOwners.cha.key },
  // Harry J. Schneider Apartments
  '250088': { owner: BuildingOwners.cha.key },
  // Hattie Callner
  '250089': { owner: BuildingOwners.cha.key },
  // Henry Horner
  '250078': { owner: BuildingOwners.cha.key },
  // Hilliard Homes Limited Partnership (Senior)
  '157607': { owner: BuildingOwners.cha.key },
  // Jazz on the Boulevard
  '175825': { owner: BuildingOwners.cha.key },
  // Judge Harry M. Fisher Apartments
  '250092': { owner: BuildingOwners.cha.key },
  // Judge Green Apartments
  '250091': { owner: BuildingOwners.cha.key },
  // Judge Frederick W. Slater Apartments
  '250093': { owner: BuildingOwners.cha.key },
  // Julia C Lathrop Homes
  '250073': { owner: BuildingOwners.cha.key },
  // Kenmore Plaza Tenant Association
  '159810': { owner: BuildingOwners.cha.key },
  // Lake Parc Place
  '250072': { owner: BuildingOwners.cha.key },
  // Lake Park Crescent Associates 1, LP
  '102239': { owner: BuildingOwners.cha.key },
  // Las Americas Apartments
  '157165': { owner: BuildingOwners.cha.key },
  // Lawndale Gardens
  '250074': { owner: BuildingOwners.cha.key },
  // Long Life Apts
  '250099': { owner: BuildingOwners.cha.key },
  // Lorraine Hansberry Senior Apartments
  '250100': { owner: BuildingOwners.cha.key },
  // Mahalia Jackson Apt
  '159982': { owner: BuildingOwners.cha.key },
  // Major Robert H Lawrence Apartments
  '250107': { owner: BuildingOwners.cha.key },
  // Margaret Day Blake Apartments
  '250101': { owner: BuildingOwners.cha.key },
  // Maria Diaz Martinez Apts
  '250102': { owner: BuildingOwners.cha.key },
  // Mary Hartwell Catherwood Apartments
  '250104': { owner: BuildingOwners.cha.key },
  // Mary Jane Richardson-Jones Apts
  '250105': { owner: BuildingOwners.cha.key },
  // Maudelle Brown Bousfield Apartments
  '250106': { owner: BuildingOwners.cha.key },
  // Minnie Riperton Apartments
  '159323': { owner: BuildingOwners.cha.key },
  // North Town Village
  '251767': { owner: BuildingOwners.cha.key },
  // Oakwood Shores 2B & 2D
  '256079': { owner: BuildingOwners.cha.key },
  // 3506 S STATE ST
  '111083': { owner: BuildingOwners.cha.key },
  // Park Douglas Apartments
  '254055': { owner: BuildingOwners.cha.key },
  // Patrick Sullivan Apartments
  '159247': { owner: BuildingOwners.cha.key },
  // Pershing Apartments
  '118998': { owner: BuildingOwners.cha.key },
  // Pomeroy
  '173863': { owner: BuildingOwners.cha.key },
  // Renaissance North
  '140771': { owner: BuildingOwners.cha.key },
  // River Village Pointe Condominium Association
  '110854': { owner: BuildingOwners.cha.key },
  // Roosevelt Square II
  '252258': { owner: BuildingOwners.cha.key },
  // Shops and Lofts at 47
  '175346': { owner: BuildingOwners.cha.key },
  // Sullivan Station Apartments
  '254173': { owner: BuildingOwners.cha.key },
  // Thomas Flannery Apartments
  '157348': { owner: BuildingOwners.cha.key },
  // Trumbull Park Homes
  '250076': { owner: BuildingOwners.cha.key },
  // Vivian Carter Apartments
  '250108': { owner: BuildingOwners.cha.key },
  // Vivian Gordon Harsh Apts
  '250109': { owner: BuildingOwners.cha.key },
  // Wentworth Gardens
  '250077': { owner: BuildingOwners.cha.key },
  // Westhaven Park Tower Condo Assoc (100 N. Hermitage Ave.)
  '214929': { owner: BuildingOwners.cha.key },
  // Wicker Park Apts
  '250111': { owner: BuildingOwners.cha.key },
  // William Castleman Apartments
  '250113': { owner: BuildingOwners.cha.key },
  // William Jones Apartments
  '250112': { owner: BuildingOwners.cha.key },
  // Zelda Ormes Apartments
  '250114': { owner: BuildingOwners.cha.key },

  /**
   * City of Chicago
   * Helpful source: https://www.chicago.gov/city/en/depts/dcd/supp_info/city-owned_land_inventory.html
   */
  // 400 W Superior St
  '103812': { owner: BuildingOwners.cityofchicago.key },
  // Chicago Indoor Sports
  '120015': { owner: BuildingOwners.cityofchicago.key },
  // City Hall
  '250115': { owner: BuildingOwners.cityofchicago.key },
  // Harold Washington Library
  '157964': { owner: BuildingOwners.cityofchicago.key },
  // Police Training Academy
  '250068': { owner: BuildingOwners.cityofchicago.key },
  // Martin Luther King Community Center
  '250058': { owner: BuildingOwners.cityofchicago.key },
  // Sulzer Library
  '250065': { owner: BuildingOwners.cityofchicago.key },
  // 1533 W.Warren Blvd
  '256759': { owner: BuildingOwners.cityofchicago.key },
  // Englewood Health Center
  '250057': { owner: BuildingOwners.cityofchicago.key },
  // Gallery 37
  '250063': { owner: BuildingOwners.cityofchicago.key },
  // CDOT Central Office
  '250066': { owner: BuildingOwners.cityofchicago.key },

  /**
   * Columbia College
   * Helpful source: https://www.colum.edu/columbia-central/on-campus/building-codes
   */
  // 600 S Michigan Ave
  '251929': { owner: BuildingOwners.columbia.key },
  // 618 S Michigan Ave
  '161103': { owner: BuildingOwners.columbia.key },
  // 72 E 11th St
  '161147': { owner: BuildingOwners.columbia.key },
  // 916 S Wabash Ave
  '251945': { owner: BuildingOwners.columbia.key },
  // 33 E Congress
  '103617': { owner: BuildingOwners.columbia.key },
  // 1104 S Wabash Ave
  '161150': { owner: BuildingOwners.columbia.key },
  // 623 S Wabash Ave
  '158429': { owner: BuildingOwners.columbia.key },
  // 624 S Michigan Ave
  '161145': { owner: BuildingOwners.columbia.key },

  /**
   * City Colleges of Chicago
   * Helpful source: https://www.ccc.edu/COLLEGES/Pages/default.aspx
   * Helpful source: https://www.ccc.edu/departments/pages/facilities-and-planning.aspx
   */
  // Harold Washington College
  '101980': { owner: BuildingOwners.ccc.key },
  // Harry S. Truman College
  '102332': { owner: BuildingOwners.ccc.key },
  // Kennedy-King College
  '250004': { owner: BuildingOwners.ccc.key },
  // Malcolm X College
  '250009': { owner: BuildingOwners.ccc.key },
  // Olive-Harvey College
  '102544': { owner: BuildingOwners.ccc.key },
  // Richard J. Daley College
  '100395': { owner: BuildingOwners.ccc.key },
  // Wilbur J. Wright College
  '101492': { owner: BuildingOwners.ccc.key },
  // Malcolm X College & School of Health Sciences
  '254347': { owner: BuildingOwners.ccc.key },
  // Dawson Technical Institute
  '250008': { owner: BuildingOwners.ccc.key },
  // Arturo Velasquez Institute
  '250002': { owner: BuildingOwners.ccc.key },

  /**
   * Moody Bible Institute
   */
  // Crowell Hall
  '161181': { owner: BuildingOwners.moody.key },
  // Torrey-Gray Doane
  '251959': { owner: BuildingOwners.moody.key },
  // Sweeting Center
  '162325': { owner: BuildingOwners.moody.key },
  // Solheim Center
  '165717': { owner: BuildingOwners.moody.key },

  /**
   * School of the Art Institute of Chicago
   */
  // The Chicago Building, 7 W Madison
  '173632': { owner: BuildingOwners.saic.key },
  // 162 North State Street
  '250167': { owner: BuildingOwners.saic.key },
  // 280 Building, 280 S Columbus Dr
  '252065': {
    tags: [ BuildingTags.hasRetrofitCaseStudy],
    owner: BuildingOwners.saic.key,
    links: [
      {
        url: 'https://www.chicago.gov/content/dam/city/sites/retrofit-chicago-2/pastparticipants/SAIC.pdf',
        text: 'SAIC 280 S Columbus Building Retrofit Report',
      },
    ],
  },
  // Alice B. Sharp Building, 37 S Wabash Ave
  '134783': { owner: BuildingOwners.saic.key },

  /**
   * North Park University
   */
  // Johnson Center for Science and Community Life, 5141 N Christiana Ave
  '254158': { owner: BuildingOwners.npu.key },
  // 5148 N Kedzie
  '101507': { owner: BuildingOwners.npu.key },
  // Helwig Recreation Center, 3205 W Carmen Ave
  '254159': { owner: BuildingOwners.npu.key },
  // 5114 N Christiana
  '254157': { owner: BuildingOwners.npu.key },
};

export function getBuildingCustomInfo(
  building: IBuilding,
): IBuildingCustomInfo | null {
  const buildingSlug = slugify(building.ID as string);

  return BuildingsCustomInfo[buildingSlug] ?? null;
}
</script>
