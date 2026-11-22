# BREACH · brand

The "Ligne rouge" (red line) identity: the Space Grotesk Bold **B** is sliced by a red line (the intrusion, and a nod to Ligne Rouge, the player's firm). The top half slides to the right with a slight red/cyan chromatic aberration, and a cyan terminal cursor (the defence) ends the word. Palette and fonts come from the GDD.

| Role | Colour |
| --- | --- |
| Night (background) | `#07090F` |
| Red line (attack) | `#FF3D5A` · on light backgrounds `#E5173A` |
| Cursor (defence) | `#2DE2FF` · on light backgrounds `#0092B3` |
| Secondary text | `#6B7A99` |

Fonts: Space Grotesk Bold (logo), JetBrains Mono (tagline). All SVGs have their text converted to outlines: no font to install.

## Files

| File | Use |
| --- | --- |
| `png/breach-avatar-500.png` (and `-1024`) | GitHub organization profile picture (full square, GitHub rounds it itself) |
| `svg/breach-mark.svg` | Master icon, dark rounded square |
| `svg/breach-mark-light.svg` | Icon on a light background |
| `svg/breach-mark-transparent-{dark,light}-bg.svg` | Icon without background, for dark or light backgrounds |
| `svg/breach-wordmark-{dark,light}-bg.svg` | Wordmark only, transparent background |
| `svg/breach-wordmark-tagline-{dark,light}-bg.svg` | Wordmark + "HACK · DETECT · LEARN" |
| `svg/favicon.svg`, `png/favicon-32.png`, `png/favicon-180.png` | Favicon and apple-touch-icon |
| `png/social-preview-1280x640.png` | "Social preview" image for the GitHub repositories |
| `explorations/` | Discarded directions (RGB glitch, network perimeter, prompt) |
| `source/` | Python generator (fontTools): `python3 build.py <folder>` |

Theme-aware rendering in a GitHub README:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="brand/svg/breach-wordmark-dark-bg.svg">
  <img alt="BREACH" src="brand/svg/breach-wordmark-light-bg.svg" width="420">
</picture>
```
