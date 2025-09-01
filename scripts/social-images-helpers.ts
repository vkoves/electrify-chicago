/**
 * A set of Typescript helper functions for our social image generation
 */

import * as fs from 'fs-extra';
import * as path from 'path';
import { parse } from 'csv-parse/sync';

import pageSocialConfigs from '../src/constants/page-social-images/page-social-configs.json';
import buildingOwnersData from '../src/constants/building-owners.json';

// Shared constants
export const SOCIAL_IMAGES_DIR = './static/social-images';
export const BUILDING_DATA_FILE = './src/data/dist/building-benchmarks.csv';
export const BASE_URL =
  process.env.SOCIAL_CARD_BASE_URL || 'http://localhost:8080';

// Shared types
export interface BuildingData {
  ID: string | number | boolean;
}

// Building data utilities
export async function loadAllBuildingData(): Promise<BuildingData[]> {
  const buildingDataRaw = await fs.readFile(BUILDING_DATA_FILE, 'utf8');

  return parse(buildingDataRaw, {
    columns: true,
    skip_empty_lines: true,
  }) as BuildingData[];
}

export async function loadBuildingIds(): Promise<string[]> {
  const buildingData = await loadAllBuildingData();

  return buildingData.map((building) => String(building.ID));
}

// File system utilities
export function getSocialImagePath(buildingId: string): string {
  return path.join(SOCIAL_IMAGES_DIR, `building-${buildingId}.webp`);
}

export function getPageSocialImagePath(pageId: string): string {
  return path.join(SOCIAL_IMAGES_DIR, `page-${pageId}.webp`);
}

export async function imageExists(buildingId: string): Promise<boolean> {
  const imagePath = getSocialImagePath(buildingId);
  return await fs.pathExists(imagePath);
}

export async function pageImageExists(pageId: string): Promise<boolean> {
  const imagePath = getPageSocialImagePath(pageId);
  return await fs.pathExists(imagePath);
}

// Page data utilities
export function getAvailablePageIdsFromConfig(): string[] {
 return Object.keys(pageSocialConfigs);
}

export function getAvailableOwnerIds(): string[] {
  return Object.keys(buildingOwnersData);
}

export async function ensureSocialImagesDirectory(): Promise<void> {
  await fs.ensureDir(SOCIAL_IMAGES_DIR);
}

// Filtering utilities
export async function findMissingImages(): Promise<string[]> {
  const buildingIds = await loadBuildingIds();
  const missingIds: string[] = [];

  for (const buildingId of buildingIds) {
    if (!(await imageExists(buildingId))) {
      missingIds.push(buildingId);
    }
  }

  return missingIds;
}

// Clean up specific images
export async function removeImages(buildingIds: string[]): Promise<void> {
  for (const buildingId of buildingIds) {
    const imagePath = getSocialImagePath(buildingId);
    if (await fs.pathExists(imagePath)) {
      await fs.remove(imagePath);
      console.log(`   🗑️  Removed building-${buildingId}.webp`);
    }
  }
}

// Owner social image utilities
export function getOwnerSocialImagePath(ownerId: string): string {
  return path.join(SOCIAL_IMAGES_DIR, `owner-${ownerId}.webp`);
}

export async function ownerImageExists(ownerId: string): Promise<boolean> {
  const imagePath = getOwnerSocialImagePath(ownerId);
  return await fs.pathExists(imagePath);
}
