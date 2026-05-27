<script lang="ts">
export default {};

/**
 * Ward council member information extracted from GeoJSON.
 * Maps ward number to alderperson name (in "Last, First" format) and
 * Councilmatic profile link.
 *
 * This constant avoids loading the 450KB GeoJSON file when only basic
 * ward information is needed.
 *
 * Note: Names are kept in the original "Last, First" format from the source data.
 * Use formatAlderName() from utils/alder-data.vue to convert to "First Last" format.
 */
export const WardCouncilMembers: Record<
  string,
  { councilMember: string; detailLink: string }
> = {
  '1': {
    councilMember: 'La Spata, Daniel',
    detailLink: '/person/la-spata-daniel-82131030fe01',
  },
  '2': {
    councilMember: 'Hopkins, Brian',
    detailLink: '/person/hopkins-brian-daa737472fb4',
  },
  '3': {
    councilMember: 'Dowell, Pat',
    detailLink: '/person/dowell-pat-878bbdf82627',
  },
  '4': {
    councilMember: 'Robinson, Lamont J.',
    detailLink: '/person/robinson-lamont-j-132eea32c952',
  },
  '5': {
    councilMember: 'Yancy, Desmon C.',
    detailLink: '/person/yancy-desmon-c-c93f2d5f0290',
  },
  '6': {
    councilMember: 'Hall, William E.',
    detailLink: '/person/hall-william-e-90d43d455e37',
  },
  '7': {
    councilMember: 'Mitchell, Gregory I.',
    detailLink: '/person/mitchell-gregory-i-3441ebe27c67',
  },
  '8': {
    councilMember: 'Harris, Michelle A.',
    detailLink: '/person/harris-michelle-a-04880566b07e',
  },
  '9': {
    councilMember: 'Beale, Anthony',
    detailLink: '/person/beale-anthony-1a1cae5f66b8',
  },
  '10': {
    councilMember: 'Chico, Peter',
    detailLink: '/person/chico-peter-8b011035a4c6',
  },
  '11': {
    councilMember: 'Lee, Nicole T.',
    detailLink: '/person/lee-nicole-t-edc136f48eec',
  },
  '12': {
    councilMember: 'Ramirez, Julia M.',
    detailLink: '/person/ramirez-julia-m-4a1b9deaf6df',
  },
  '13': {
    councilMember: 'Quinn, Marty',
    detailLink: '/person/quinn-marty-a33401de1ab1',
  },
  '14': {
    councilMember: 'Gutierrez, Jeylu B.',
    detailLink: '/person/gutierrez-jeylu-b-69235adf7a49',
  },
  '15': {
    councilMember: 'Lopez, Raymond A.',
    detailLink: '/person/lopez-raymond-a-b087801cdeec',
  },
  '16': {
    councilMember: 'Coleman, Stephanie D.',
    detailLink: '/person/coleman-stephanie-d-7bcc9a1d4983',
  },
  '17': {
    councilMember: 'Moore, David H.',
    detailLink: '/person/moore-david-h-ee688e5a69d2',
  },
  '18': {
    councilMember: 'Curtis, Derrick G.',
    detailLink: '/person/curtis-derrick-g-10b32bc26e2c',
  },
  '19': {
    councilMember: "O'Shea, Matthew J.",
    detailLink: '/person/oshea-matthew-j-45134b1c5b9c',
  },
  '20': {
    councilMember: 'Taylor, Jeanette B.',
    detailLink: '/person/taylor-jeanette-b-7c477bd799ac',
  },
  '21': {
    councilMember: 'Mosley, Ronnie L.',
    detailLink: '/person/mosley-ronnie-l-77899fbd49f6',
  },
  '22': {
    councilMember: 'Rodriguez, Michael D.',
    detailLink: '/person/rodriguez-michael-d-50f3431b00ab',
  },
  '23': {
    councilMember: 'Tabares, Silvana',
    detailLink: '/person/tabares-silvana-9a91e474c1fe',
  },
  '24': {
    councilMember: 'Scott, Monique L.',
    detailLink: '/person/scott-monique-l-0f545d00d830',
  },
  '25': {
    councilMember: 'Sigcho-Lopez, Byron',
    detailLink: '/person/sigcho-lopez-byron-4249ff45ce85',
  },
  '26': {
    councilMember: 'Fuentes, Jessica L.',
    detailLink: '/person/fuentes-jessica-faceb657886b',
  },
  '27': {
    councilMember: 'Burnett, Jr., Walter',
    detailLink: '/person/burnett-jr-walter-e95bbbec9a13',
  },
  '28': {
    councilMember: 'Ervin, Jason C.',
    detailLink: '/person/ervin-jason-c-cb1d3455326b',
  },
  '29': {
    councilMember: 'Taliaferro, Chris',
    detailLink: '/person/taliaferro-chris-eab63f0460fc',
  },
  '30': {
    councilMember: 'Cruz, Ruth',
    detailLink: '/person/cruz-ruth-f2fc8837da43',
  },
  '31': {
    councilMember: 'Cardona, Jr., Felix',
    detailLink: '/person/cardona-jr-felix-df1f9e28cda6',
  },
  '32': {
    councilMember: 'Waguespack, Scott',
    detailLink: '/person/waguespack-scott-1d374b738cf9',
  },
  '33': {
    councilMember: 'Rodriguez Sanchez, Rossana',
    detailLink: '/person/rodriguez-sanchez-rossana-7163b97c3957',
  },
  '34': {
    councilMember: 'Conway, William',
    detailLink: '/person/conway-william-fd13c2848393',
  },
  '35': {
    councilMember: 'Quezada, Anthony J.',
    detailLink: '/person/quezada-anthony-j-e1ef5a0ef6a4',
  },
  '36': {
    councilMember: 'Villegas, Gilbert',
    detailLink: '/person/villegas-gilbert-10ee465e7ba7',
  },
  '37': {
    councilMember: 'Mitts, Emma',
    detailLink: '/person/mitts-emma-d7b5799c8ce4',
  },
  '38': {
    councilMember: 'Sposato, Nicholas',
    detailLink: '/person/sposato-nicholas-1bf265dc9bf4',
  },
  '39': {
    councilMember: 'Nugent, Samantha',
    detailLink: '/person/nugent-samantha-d18d112ea760',
  },
  '40': {
    councilMember: 'Vasquez, Jr., Andre',
    detailLink: '/person/vasquez-jr-andre-579cbc9947bf',
  },
  '41': {
    councilMember: 'Napolitano, Anthony V.',
    detailLink: '/person/napolitano-anthony-v-972843bfaee1',
  },
  '42': {
    councilMember: 'Reilly, Brendan',
    detailLink: '/person/reilly-brendan-1e50c314ab27',
  },
  '43': {
    councilMember: 'Knudsen, Timothy R.',
    detailLink: '/person/knudsen-timothy-r-b966a9ec1329',
  },
  '44': {
    councilMember: 'Lawson, Bennett R.',
    detailLink: '/person/lawson-bennett-r-a21a6f15f2b4',
  },
  '45': {
    councilMember: 'Gardiner, James M.',
    detailLink: '/person/gardiner-james-m-6b0d1591916d',
  },
  '46': {
    councilMember: 'Clay, Angela',
    detailLink: '/person/clay-angela-ac572c6bc4fe',
  },
  '47': {
    councilMember: 'Martin, Matthew J.',
    detailLink: '/person/martin-matthew-j-54f1707f5a16',
  },
  '48': {
    councilMember: 'Manaa-Hoppenworth, Leni',
    detailLink: '/person/manaa-hoppenworth-leni-4b8ecbaaebbc',
  },
  '49': {
    councilMember: 'Hadden, Maria E.',
    detailLink: '/person/hadden-maria-e-e2f7ec1f2a8b',
  },
  '50': {
    councilMember: 'Silverstein, Debra L.',
    detailLink: '/person/silverstein-debra-l-12dd7f9d91d6',
  },
};
</script>
