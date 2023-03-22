/**
 * Returns a string rank for very bad buildings, or null if not in top 50
 * worst
 *
 * @param {number} statRank
 * @param {boolean} isSquareFootage
 * @return {string | null}
 */
export function returnRankLabel(statRank, isSquareFootage) {
  if (isSquareFootage) {
    return 'Largest';
  } else if (statRank <= 10) {
    return 'Highest in Chicago 🚨 ';
  } else if (statRank <= 50) {
    return 'Highest in Chicago 🚩';
  } else {
    return null;
  }
}
