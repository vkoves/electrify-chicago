<script lang="ts">
import type { Polygon, MultiPolygon } from 'geojson';

export default {};

// Data file paths
const ALDERS_INFO_CSV_PATH = '/alders-info.csv';
const WARD_BOUNDARIES_GEOJSON_PATH = '/chicago-wards-2025.geojson';

/** Alderperson contact information from CSV */
export interface AlderInfo {
  name: string;
  office: string;
  officePhone: string;
  email: string;
  website: string;
}

/** Ward metadata from GeoJSON properties */
export interface WardProperties {
  district: string; // e.g., "Ward 6"
  council_member: string; // e.g., "Smith, John"
  detail_link: string; // Councilmatic profile URL path
  select_id: string;
}

/** GeoJSON feature for a single ward */
export interface WardFeature {
  type: 'Feature';
  properties: WardProperties;
  geometry: Polygon | MultiPolygon;
}

/** Full GeoJSON collection of all Chicago wards */
export interface WardsGeoJSON {
  type: 'FeatureCollection';
  features: WardFeature[];
}

/**
 * Format alderperson name from "Last, First" or "Last, Jr., First" format
 * to "First Last" or "First Last Jr." format.
 *
 * Examples:
 * - "Vasquez, Jr., Andre" -> "Andre Vasquez Jr."
 * - "Yancy, Desmon C." -> "Desmon C. Yancy"
 * - "O'Shea, Matthew J." -> "Matthew J. O'Shea"
 */
export function formatAlderName(name: string): string {
  // Split by comma and trim each part
  const parts = name.split(',').map((part) => part.trim());

  if (parts.length === 3) {
    // Format: "Last, Jr., First" -> "First Last Jr."
    const [lastName, suffix, firstName] = parts;
    return `${firstName} ${lastName} ${suffix}`;
  } else if (parts.length === 2) {
    // Format: "Last, First" -> "First Last"
    const [lastName, firstName] = parts;
    return `${firstName} ${lastName}`;
  }

  // Return as-is if format is unexpected
  return name;
}

/**
 * Parse a CSV line handling quoted fields
 */
function parseCSVLine(line: string): string[] {
  const result: string[] = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];

    if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === ',' && !inQuotes) {
      result.push(current);
      current = '';
    } else {
      current += char;
    }
  }
  result.push(current);

  return result;
}

/**
 * Load ward boundary GeoJSON data
 */
export async function loadWardBoundaries(): Promise<WardsGeoJSON | null> {
  try {
    const response = await fetch(WARD_BOUNDARIES_GEOJSON_PATH);
    return (await response.json()) as WardsGeoJSON;
  } catch (err) {
    console.error('Failed to load ward boundaries:', err);
    return null;
  }
}

/**
 * Get ward properties by ward number from GeoJSON data
 *
 * @param wardNumber - The ward number (e.g., "6" or "40")
 * @returns WardProperties or null if not found
 */
export async function getWardInfo(
  wardNumber: string,
): Promise<WardProperties | null> {
  const wardsData = await loadWardBoundaries();
  if (!wardsData) return null;

  const wardFeature = wardsData.features.find(
    (feature) => feature.properties.district === `Ward ${wardNumber}`,
  );

  return wardFeature ? wardFeature.properties : null;
}

/**
 * Load alderperson contact information from CSV file and return a map
 * of ward number -> alder info.
 *
 * Ward numbers are normalized (e.g., "04" becomes "4") for consistent lookup.
 */
export async function loadAldersData(): Promise<Map<string, AlderInfo>> {
  const aldersData = new Map<string, AlderInfo>();

  try {
    const response = await fetch(ALDERS_INFO_CSV_PATH);
    const csvText = await response.text();

    // Parse CSV and build a map of ward number -> alder info
    const lines = csvText.split('\n');

    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();

      if (!line) continue;

      // Parse CSV line (handles quoted fields)
      const values = parseCSVLine(line);

      const office = values[1].trim();

      // Normalize ward number by converting to integer and back to string
      // This handles cases where CSV has "04" but we need to match "4"
      const normalizedWard = parseInt(office, 10).toString();

      aldersData.set(normalizedWard, {
        name: values[0].replace(/"/g, '').trim(),
        office,
        officePhone: values[2].trim(),
        email: values[4].trim(),
        website: values[5].trim(),
      });
    }
  } catch (err) {
    console.error('Failed to load alder info:', err);
  }

  return aldersData;
}
</script>
