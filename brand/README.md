# BREACH · brand

Identité « Ligne rouge » : le **B** de Space Grotesk Bold est tranché par une ligne rouge (l'intrusion, et clin d'œil à Ligne Rouge, le cabinet du joueur). La moitié haute glisse vers la droite avec une légère aberration chromatique rouge/cyan, et un curseur de terminal cyan (la défense) termine le mot. Palette et typos reprises du GDD.

| Rôle | Couleur |
| --- | --- |
| Nuit (fond) | `#07090F` |
| Ligne rouge (attaque) | `#FF3D5A` · sur fond clair `#E5173A` |
| Curseur (défense) | `#2DE2FF` · sur fond clair `#0092B3` |
| Texte secondaire | `#6B7A99` |

Typos : Space Grotesk Bold (logo), JetBrains Mono (baseline). Tous les SVG ont le texte vectorisé : aucune police à installer.

## Fichiers

| Fichier | Usage |
| --- | --- |
| `png/breach-avatar-500.png` (et `-1024`) | Photo de profil de l'organisation GitHub (carré plein, GitHub arrondit lui-même) |
| `svg/breach-mark.svg` | Master de l'icône, carré arrondi sombre |
| `svg/breach-mark-light.svg` | Icône sur fond clair |
| `svg/breach-mark-transparent-{dark,light}-bg.svg` | Icône sans fond, pour fond sombre ou clair |
| `svg/breach-wordmark-{dark,light}-bg.svg` | Wordmark seul, fond transparent |
| `svg/breach-wordmark-tagline-{dark,light}-bg.svg` | Wordmark + « HACK · DETECT · LEARN » |
| `svg/favicon.svg`, `png/favicon-32.png`, `png/favicon-180.png` | Favicon et apple-touch-icon |
| `png/social-preview-1280x640.png` | Image « Social preview » des repos GitHub |
| `explorations/` | Pistes écartées (glitch RGB, périmètre réseau, prompt) |
| `source/` | Générateur Python (fontTools) : `python3 build.py <dossier>` |

Rendu README GitHub selon le thème :

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="brand/svg/breach-wordmark-dark-bg.svg">
  <img alt="BREACH" src="brand/svg/breach-wordmark-light-bg.svg" width="420">
</picture>
```
