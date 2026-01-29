# Claude Code Guidelines for Electrify Chicago

This document contains important guidelines for Claude when working on this codebase.

## Packages

This project uses Yarn, use `yarn install` commands, NOT NPM.

## Code Duplication

**NEVER duplicate code or CSS.** Always extract shared functionality to common files:

- **CSS/SCSS**: Use existing files in `src/scss/` directory:
  - `global.scss` - Global styles and reusable classes
  - `colors.scss` - Color variables and definitions
  - `spacing.scss` - Spacing, border, and layout constants
- **JavaScript/TypeScript**: Extract shared functions to:
  - `common-functions.vue` - Shared utility functions and interfaces
  - Component-specific utilities should be in dedicated utility files

## CSS Architecture

1. **Reuse existing classes** from `global.scss` whenever possible
2. **Use color variables** from `colors.scss` instead of hardcoding colors
3. **Use spacing variables** from `spacing.scss` for consistent layout
4. **Use media query variables** from `spacing.scss` instead of hardcoded breakpoints
5. **Extract new reusable patterns** to global.scss with descriptive class names
6. **NEVER use `!important`** - Fix specificity issues by using more specific selectors or restructuring CSS

## Examples

❌ **Wrong - Duplicating CSS:**

```scss
.my-component {
  background-color: #ffd9d9;
  border-color: red;
}
```

✅ **Right - Using shared classes:**

```scss
.my-component {
  @extend .concern-level-very-bad;
}
```

❌ **Wrong - Duplicating functions:**

```javascript
// Same function copied in multiple files
function formatNumber(value) { ... }
```

✅ **Right - Shared function:**

```javascript
import { formatNumber } from '../common-functions.vue';
```

❌ **Wrong - Hardcoded media queries:**

```scss
.my-component {
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}
```

✅ **Right - Using spacing variables:**

```scss
.my-component {
  @media (max-width: $mobile-max-width) {
    grid-template-columns: 1fr;
  }
}
```

## When Adding New Shared Styles

If you need to create new reusable styles:

1. Add them to `global.scss` with clear, semantic class names
2. Use existing color and spacing variables
3. Document the purpose of new classes
4. Update this file with examples if needed

## File Modification Guidelines

- Always check for existing similar functionality before creating new code
- Prefer editing existing files over creating new ones
- Look for patterns in the codebase and follow them consistently
