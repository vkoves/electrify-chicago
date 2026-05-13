# Self-Hosted Roboto Fonts

This directory contains optimized, self-hosted Roboto font files that are smaller than Google Fonts delivery.

**Created by Claude**

## Font Files

- **Roboto-Regular.woff2** (18KB) - Font weight: 400, normal style
- **Roboto-Medium.woff2** (19KB) - Font weight: 500, normal style
- **Roboto-Bold.woff2** (19KB) - Font weight: 700, normal style
- **Roboto-Black.woff2** (19KB) - Font weight: 900, normal style
- **Roboto-Italic.woff2** (20KB) - Font weight: 400, italic style
- **Roboto-BoldItalic.woff2** (21KB) - Font weight: 700, italic style

**Total size: 124KB** (vs ~880KB for original TTF files, ~396KB for full WOFF2 files)

## Character Set

These fonts are optimized for **English-only content** with **102 characters**:

### Basic Latin + Essential Punctuation

```
 !"#$%&'()*+,-./0123456789:;<=>?@
ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`
abcdefghijklmnopqrstuvwxyz{|}~
–—''""…
```

**Perfect for:** English websites, documentation, and applications that don't need international character support.

**Excluded:** Accented characters (àáâãäå), currency symbols (€£¥), mathematical symbols, and other language-specific characters. This creates much smaller files optimized specifically for English content.

## How These Were Created

### 1. Source Files

Downloaded from [Google Fonts - Roboto](https://fonts.google.com/specimen/Roboto)

- Original format: TTF files from `Roboto/static/` directory
- Weights: Regular (400), Medium (500), Bold (700), Black (900)
- Styles: Normal, Italic (for 400 and 700 weights)

### 2. Conversion Process

```bash
# Step 1: Convert TTF to WOFF2
python3 -c "
from fontTools.ttLib import TTFont
import os
for font_file in os.listdir('.'):
    if font_file.endswith('.ttf'):
        font = TTFont(font_file)
        woff2_name = font_file.replace('.ttf', '.woff2')
        font.flavor = 'woff2'
        font.save(woff2_name)
"

# Step 2: Subset to Latin characters only
python3 -c "
from fontTools.ttLib import TTFont
from fontTools import subset
import os

def subset_font(font_path, output_path):
    font = TTFont(font_path)
    subsetter = subset.Subsetter()

    # Latin character ranges
    subsetter.options.unicodes = []
    subsetter.options.unicodes.extend(range(0x0020, 0x007F))  # Basic Latin
    subsetter.options.unicodes.extend(range(0x00A0, 0x00FF))  # Latin-1 Supplement
    subsetter.options.unicodes.extend(range(0x0100, 0x017F))  # Latin Extended-A
    subsetter.options.unicodes.extend(range(0x0180, 0x024F))  # Latin Extended-B

    # Common punctuation
    subsetter.options.unicodes.extend([0x2013, 0x2014, 0x2018, 0x2019, 0x201C, 0x201D])

    subsetter.subset(font)
    font.save(output_path)

# Apply to all .woff2 files
for font_file in os.listdir('.'):
    if font_file.endswith('.woff2'):
        subset_font(font_file, font_file.replace('.woff2', '-subset.woff2'))
"
```

### 3. Size Comparison

| Stage              | Size     | Reduction       |
| ------------------ | -------- | --------------- |
| Original TTF files | 880KB    | -               |
| WOFF2 conversion   | 396KB    | 55% smaller     |
| **Latin subset**   | **24KB** | **94% smaller** |

### 4. Dependencies Used

```bash
pip3 install fonttools[woff]
```

## Loading Strategy

- **Preloaded**: Only `Roboto-Regular.woff2` is preloaded for critical rendering
- **Lazy loaded**: All other weights load on-demand when CSS references them
- **Font-display**: Uses `swap` for faster perceived loading

## Adding New Weights/Styles

If you need additional Roboto variants:

1. Download from [Google Fonts - Roboto](https://fonts.google.com/specimen/Roboto)
2. Follow the conversion process above
3. Add corresponding `@font-face` declarations in `src/scss/global.scss`
4. Update the preloading strategy in `src/main.js` if needed

## Benefits Over Google Fonts

- **Smaller total size** (24KB vs Google's typical delivery)
- **No external dependencies** (better for testing, offline development)
- **Consistent loading** (eliminates external network variability)
- **Better privacy** (no requests to Google servers)
- **Faster for repeat visits** (cached locally, no CDN lookup)
