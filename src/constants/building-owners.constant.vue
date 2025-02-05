<script lang="ts">

import { IBuildingOwners} from './buildings-custom-info.constant.vue';

export default { };

  // export interface IBuildingOwner {
  //   key: string;
  //   name: string;
  //   nameShort: string; // Name for table view
  //   logoSmall?: string; // A square logo for table view
  //   logoLarge?: string; // Any size logo for building details
  //   links?: Array <ILink>; // Extra links for supplementary info
  // }

  // export interface IBuildingOwners {
  //   [ownerKey: string]: IBuildingOwner;
  // }
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
      links: [
        {
            url : 'https://bpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/a/3657/files/2023/06/UChicago_GHG_Plan_2022.pdf',
            text : 'Greenhouse Gas Emissions Reduction Plan | FY2022-FY2030',
        },
        {
            url: 'https://sustainability.uchicago.edu/reporting/formal-reporting/',
            text: 'Annual Progress Report',
        },
        {
            url : 'https://sustainability.uchicago.edu/reporting/dashboards/',
            text : 'Campus Dashboards',
        },
        {
            url : 'https://bpb-us-w2.wpmucdn.com/voices.uchicago.edu/dist/a/3657/files/2023/07/SUS16-0774.Sustainability-Plan-Report.Final_.pdf',
            text : 'Sustainability Plan (2016)',
        },
        ],
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

  </script>