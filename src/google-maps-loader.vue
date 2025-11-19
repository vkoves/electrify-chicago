<script lang="ts">
export default {};

/**
 * Utility for dynamically loading the Google Maps JavaScript API
 * Based on: https://developers.google.com/maps/documentation/javascript/load-maps-js-api
 */

// Extend the Window interface to include Google Maps types
declare global {
  interface Window {
    google?: {
      maps?: {
        __ib__?: () => void;
        importLibrary?: (libraryName: string) => Promise<unknown>;
        [key: string]: unknown;
      };
    };
  }
}

/**
 * Load the Google Maps JavaScript API dynamically
 * @param apiKey - Google Maps API key
 * @returns Promise that resolves when Google Maps is loaded
 */
export async function loadGoogleMaps(apiKey: string): Promise<void> {
  // Check if already loaded
  if (window.google?.maps) {
    return;
  }

  // Inject the loader script
  injectGoogleMapsLoader(apiKey);

  // Wait for the script to load with polling
  return new Promise((resolve, reject) => {
    const checkInterval = setInterval(() => {
      if (window.google?.maps) {
        clearInterval(checkInterval);
        resolve();
      }
    }, 100);

    // Timeout after 10 seconds
    setTimeout(() => {
      clearInterval(checkInterval);
      if (!window.google?.maps) {
        reject(new Error('Google Maps failed to load within 10 seconds'));
      }
    }, 10000);
  });
}

/**
 * Inject the Google Maps loader script into the page
 * This implements Google's dynamic loading pattern
 */
function injectGoogleMapsLoader(apiKey: string): void {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const google = (window as any).google || ((window as any).google = {});

  const maps = google.maps || (google.maps = {});
  const libraries = new Set<string>();
  const params = new URLSearchParams();

  // Create the loader function
  const loadScript = (): Promise<void> => {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');

      // Build URL parameters
      params.set('libraries', [...libraries].join(','));
      params.set('key', apiKey);
      params.set('v', 'weekly');
      params.set('callback', 'google.maps.__ib__');

      script.src = `https://maps.googleapis.com/maps/api/js?${params}`;
      script.onerror = () =>
        reject(new Error('Google Maps JavaScript API could not load'));

      // Preserve nonce for Content Security Policy if present
      const existingScript = document.querySelector(
        'script[nonce]',
      ) as HTMLScriptElement | null;
      if (existingScript?.nonce) {
        script.nonce = existingScript.nonce;
      }

      // Set callback
      maps.__ib__ = resolve;

      document.head.append(script);
    });
  };

  // Set up importLibrary function if not already present
  if (!maps.importLibrary) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    maps.importLibrary = (libraryName: string): Promise<any> => {
      libraries.add(libraryName);
      return loadScript().then(() => maps.importLibrary?.(libraryName));
    };
  }
}
</script>
