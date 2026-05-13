/**
 * Building image converter — enforces the rules from the "Adding Building Images" section
 * of the README so contributors don't have to remember the magic numbers:
 *
 *   - landscape images are resized to 1000px wide
 *   - portrait images (--tall) are resized to 600px wide
 *   - output is webp at quality 70
 *   - images are only downscaled, never enlarged (the `>` modifier on -resize)
 *
 * Run via `yarn convert-img <input> [--tall] [--out=<path>]`. Requires ImageMagick on PATH
 * (`magick` for v7, `convert` for v6 — we auto-detect).
 */
import { execFileSync, spawnSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

const LandscapeWidthPx = 1000;
const PortraitWidthPx = 600;
const WebpQuality = 70;
// Project target from the README; output above this triggers a warning so we crop tighter.
const MaxFileSizeKb = 200;

interface CliArgs {
  input: string;
  output?: string;
  tall: boolean;
}

/** Print CLI usage to stdout. Called on --help or invalid args. */
function printUsage(): void {
  console.log(
    [
      'Usage: yarn convert-img <input-image> [options]',
      '',
      'Converts a building image to our standard webp format:',
      `  - ${LandscapeWidthPx}px wide for landscape (default)`,
      `  - ${PortraitWidthPx}px wide for portrait (--tall)`,
      `  - webp at quality ${WebpQuality}`,
      '',
      'Options:',
      '  --tall              Treat as a portrait image (narrower output width)',
      '  --out=<path>        Output file path (default: input path with .webp ext)',
      '  -h, --help          Show this help',
    ].join('\n'),
  );
}

/**
 * Parse our small argv vocabulary: one positional input path, plus `--tall` and `--out=<path>`.
 * Exits the process on --help or invalid input rather than throwing — this is a CLI entry point,
 * not a reusable library function.
 */
function parseArgs(argv: string[]): CliArgs {
  let input: string | undefined;
  let output: string | undefined;
  let tall = false;

  for (const arg of argv) {
    if (arg === '-h' || arg === '--help') {
      printUsage();
      process.exit(0);
    } else if (arg === '--tall') {
      tall = true;
    } else if (arg.startsWith('--out=')) {
      output = arg.slice('--out='.length);
    } else if (!arg.startsWith('--')) {
      input = arg;
    } else {
      console.error(`Unknown option: ${arg}`);
      printUsage();
      process.exit(1);
    }
  }

  if (!input) {
    printUsage();
    process.exit(1);
  }

  return { input, output, tall };
}

/**
 * Find the ImageMagick CLI binary. ImageMagick 7 ships as `magick`; v6 (still common on Linux
 * distros) ships as `convert`. We prefer v7 when available since `convert` is deprecated upstream.
 */
function resolveImageMagickBinary(): string {
  for (const bin of ['magick', 'convert']) {
    const result = spawnSync(bin, ['-version'], { stdio: 'ignore' });
    if (result.status === 0) return bin;
  }

  console.error(
    'ImageMagick not found. Install it (e.g. `sudo apt install imagemagick` or `brew install imagemagick`) and try again.',
  );
  process.exit(1);
}

/**
 * Run the actual ImageMagick conversion. Defaults the output to the input's directory with
 * `.webp` swapped in for the original extension, and creates any missing parent directories
 * so callers can target a new owner folder (e.g. `static/building-imgs/loyola/...`) without
 * pre-creating it.
 */
function convert(args: CliArgs): void {
  const inputAbs = path.resolve(args.input);

  if (!fs.existsSync(inputAbs)) {
    console.error(`Input file does not exist: ${inputAbs}`);
    process.exit(1);
  }

  const outputAbs = path.resolve(
    args.output ??
      path.join(
        path.dirname(inputAbs),
        `${path.basename(inputAbs, path.extname(inputAbs))}.webp`,
      ),
  );

  fs.mkdirSync(path.dirname(outputAbs), { recursive: true });

  const targetWidth = args.tall ? PortraitWidthPx : LandscapeWidthPx;
  const bin = resolveImageMagickBinary();

  // `${width}>` only downscales — it never enlarges smaller source images.
  const imArgs = [
    inputAbs,
    '-resize',
    `${targetWidth}>`,
    '-quality',
    String(WebpQuality),
    '-define',
    'webp:method=6',
    outputAbs,
  ];

  console.log(
    `Converting ${path.relative(process.cwd(), inputAbs)} → ${path.relative(
      process.cwd(),
      outputAbs,
    )} (${args.tall ? 'portrait' : 'landscape'}, ${targetWidth}px wide, q${WebpQuality})`,
  );

  execFileSync(bin, imArgs, { stdio: 'inherit' });

  const sizeKb = Math.round(fs.statSync(outputAbs).size / 1024);
  console.log(
    `✅ Wrote ${path.relative(process.cwd(), outputAbs)} (${sizeKb} kB)`,
  );

  if (sizeKb > MaxFileSizeKb) {
    console.warn(
      `⚠️  Output is over our ${MaxFileSizeKb} kB target. Consider cropping the source tighter.`,
    );
  }
}

convert(parseArgs(process.argv.slice(2)));
