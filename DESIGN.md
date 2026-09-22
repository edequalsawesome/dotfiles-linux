---
name: Malarchy
description: A personal computer as a 1990s cut-and-paste magazine cover.
colors:
  base: "#1e1e2e"
  text: "#cdd6f4"
  ink: "#181825"
  paper: "#fbfbff"
  purple: "#471c8c"
  cyan: "#01baef"
  pink: "#f038ff"
  mint: "#6bffb8"
  yellow: "#ffc914"
  mauve: "#cba6f7"
  cream: "#f9e2af"
typography:
  annotation:
    fontFamily: "Georgia, serif"
    fontSize: "28px"
    fontWeight: 400
    fontStyle: "italic"
  display:
    fontFamily: "Bowlby, sans-serif"
    fontSize: "124px"
    fontWeight: 400
    lineHeight: 0.95
  slogan:
    fontFamily: "'Nimbus Mono PS', monospace"
    fontSize: "37px"
    fontWeight: 700
    lineHeight: 1.45
  sticker:
    fontFamily: "'Nimbus Mono PS', monospace"
    fontSize: "23px"
    fontWeight: 700
    lineHeight: 1.2
  label:
    fontFamily: "'Nimbus Mono PS', monospace"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "1px"
  stamp:
    fontFamily: "Bowlby, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.25
rounded:
  stamp: "50%"
components:
  cut-letter:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.display}"
    padding: "8px 9px 13px"
  slogan-strip:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    typography: "{typography.slogan}"
    padding: "0 15px"
  personal-sticker:
    backgroundColor: "{colors.mint}"
    textColor: "{colors.ink}"
    typography: "{typography.sticker}"
    padding: "12px 22px"
  edition-label:
    backgroundColor: "{colors.base}"
    textColor: "{colors.text}"
    typography: "{typography.label}"
    padding: "5px 8px"
  round-stamp:
    backgroundColor: "{colors.pink}"
    textColor: "{colors.ink}"
    typography: "{typography.stamp}"
    rounded: "{rounded.stamp}"
    width: "132px"
    height: "132px"
---

# Design System: Malarchy

## Overview

**Creative North Star: "A personal computer as a 1990s cut-and-paste magazine cover."**

Catppuccin Mocha anchors a loud paper collage: oversized cut letters, typewriter strips, saturated scraps and a photocopied real portrait. The finish is deliberately handmade, with tilted pieces and visible overlaps. This documents the implemented static wallpaper; normal desktop controls retain Catppuccin.

**Key Characteristics:**

- Oversized two-line wordmark and readable ownership slogan.
- Real Jason Sudeikis-as-Joe-Biden photography with a traced white edge.
- Catppuccin ground with purple, cyan, pink, mint and yellow paper.
- Static, layered composition with no interaction or animation.

## Colors

Primary identity comes from the purple field and cyan diagonal, supported by pink, mint and yellow clippings. Catppuccin mauve and cream connect those accents to the desktop palette. Base and text provide the quiet ground; ink and paper produce the strong printed contrast. Frontmatter records the exact implemented colors, not an expanded palette.

## Typography

Bowlby One SC, loaded locally under the family name Bowlby, supplies the cut-letter masthead and circular stamp. Nimbus Mono PS supplies the bold slogan, personal sticker and small edition credit. Italic Georgia provides the dictionary pronunciation (28px) and handwritten-feeling aside (bold, 31px). These are contrasting print voices, not a general application heading scale.

## Layout

The source uses a centered fixed canvas (1440 × 900px), exported at twice that size for the target display (2880 × 1800px). Absolute placement keeps the masthead and slogan on the left, the oversized portrait on the right, and the personal sticker and edition credit at the lower left. The cyan diagonal crosses behind the portrait. There are no responsive breakpoints; the HTML clips outside its viewport rather than reflowing like a webpage.

## Elevation & Depth

Offset dark shadows lift paper letters, slogan strips, the personal sticker and the portrait. A pale translucent tape fragment overlaps the portrait edge. A low-opacity dot pattern covers the background. Depth comes from these physical collage cues and explicit stacking, with no interactive elevation states. Exact shadow values are recorded in the sidecar.

## Shapes

Most pieces are sharp rectangular scraps with independent rotations. The right purple field has an irregular torn edge; the portrait is a hand-traced SVG silhouette with a white outline. The circular pink stamp has a dashed ink border. Tape uses a skewed polygon. Rounded application panels are not part of this wallpaper vocabulary.

## Components

Cut letters form two staggered rows with individually rotated colored backgrounds. Two slogan strips pair paper and yellow with dark typewriter text. The mint personal sticker and small edition label repeat that print language. The pink circular stamp provides a secondary editorial accent. These are static artwork elements, with no hover, focus, selected or disabled states.

The signature portrait uses a real local photograph, grayscale and increased contrast, clipped to a traced silhouette. Preserve its source provenance with every shipping raster; the photograph and derived wallpaper stay outside the public repository.

## Do's and Don'ts

- Do preserve Catppuccin for the desktop and use the collage palette for the wallpaper.
- Do keep the wordmark, ownership slogan and real portrait as the visual anchors.
- Do preserve sharp scraps, imperfect rotations and clear overlapping layers.
- Don't substitute AI-generated artwork for the real photograph.
- Don't introduce controls, hover states or animation into this static wallpaper.
- Don't publish the local photograph or derived wallpaper in the public repository.
