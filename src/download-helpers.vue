<script lang="ts">
import { toBlob } from 'html-to-image';

export default {};

/**
 * Trigger a browser download for an in-memory Blob.
 *
 * Creates an object URL, clicks a hidden anchor, and revokes the URL afterwards.
 */
export function downloadBlob(blob: Blob, filename: string): void {
  if (typeof document === 'undefined') {
    return;
  }

  const url = URL.createObjectURL(blob);
  const anchor = document.createElement('a');
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);
  URL.revokeObjectURL(url);
}

/**
 * Render a DOM element to a PNG blob using html-to-image.
 *
 * `pixelRatio` is forced to 1 because the source DOM is already authored at
 * its target export resolution (e.g. 1080x1080); leaving the default device
 * pixel ratio would double the output on hi-DPI screens.
 */
export async function elementToPngBlob(element: HTMLElement): Promise<Blob> {
  const blob = await toBlob(element, { pixelRatio: 1 });
  if (!blob) {
    throw new Error('Failed to render element to image');
  }
  return blob;
}

/**
 * Render a DOM element to a PNG and trigger a download.
 */
export async function downloadElementAsPng(
  element: HTMLElement,
  filename: string,
): Promise<void> {
  const blob = await elementToPngBlob(element);
  downloadBlob(blob, filename);
}
</script>
