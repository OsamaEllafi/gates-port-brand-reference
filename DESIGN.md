---
name: GatesPort Brand Reference
description: An airport-concourse signage system in burgundy enamel, gold edge lines and cream legend plates.
colors:
  burgundy: "#48151D"
  burgundy-deep: "#2F0D13"
  antique-gold: "#B39567"
  warm-cream: "#F0E5D2"
  bright-cream: "#F7F0E4"
  espresso: "#241C19"
  black: "#111111"
  ink-soft-on-cream: "#6A4A4D"
typography:
  display:
    fontFamily: "Montserrat, Segoe UI, Arial, sans-serif"
    fontSize: "clamp(2.6rem, 6vw, 5rem)"
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Montserrat, Segoe UI, Arial, sans-serif"
    fontSize: "clamp(2rem, 4.2vw, 3.4rem)"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "-0.025em"
  title:
    fontFamily: "Montserrat, Segoe UI, Arial, sans-serif"
    fontSize: "1.35rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.015em"
  body:
    fontFamily: "Source Sans 3, Segoe UI, Arial, sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Montserrat, Segoe UI, Arial, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 600
    letterSpacing: "0.14em"
rounded:
  sm: "10px"
  md: "14px"
  badge: "7px"
spacing:
  sm: "0.5rem"
  md: "1rem"
  lg: "2rem"
  section: "clamp(4.5rem, 9vw, 8rem)"
components:
  button-solid:
    backgroundColor: "{colors.antique-gold}"
    textColor: "{colors.burgundy-deep}"
    rounded: "{rounded.sm}"
    padding: "0.55rem 1.05rem"
    height: "2.75rem"
  button-solid-on-cream:
    backgroundColor: "{colors.burgundy}"
    textColor: "{colors.warm-cream}"
    rounded: "{rounded.sm}"
    padding: "0.55rem 1.05rem"
  button-line:
    backgroundColor: "transparent"
    textColor: "{colors.warm-cream}"
    rounded: "{rounded.sm}"
    padding: "0.55rem 1.05rem"
  sign-cream:
    backgroundColor: "{colors.warm-cream}"
    textColor: "{colors.burgundy}"
    rounded: "{rounded.md}"
    padding: "1.6rem"
  sign-deep:
    backgroundColor: "{colors.burgundy-deep}"
    textColor: "{colors.warm-cream}"
    rounded: "{rounded.md}"
    padding: "1.6rem"
  gate-badge:
    textColor: "{colors.antique-gold}"
    rounded: "{rounded.badge}"
    size: "2.25rem"
---

# Design System: GatesPort Brand Reference

## Overview

**Creative North Star: "The Concourse"**

The brand reference is an airport concourse. The four brands are four gates, A to D, and the page is the signage programme that points to them. Burgundy enamel sign panels with a hairline gold edge hang against a warm cream wall; legend plates, pictograms and prohibition signs do the teaching. Every file is one sign away, and the family reads at a glance: GatesPort Aviation is the cream holding-company sign, and Cargo, Catering and VIP hang off a gold rule beside it.

The page is composed and capable rather than loud. Colour is committed at page scale: a drenched burgundy hero, a cream floor, an espresso colour section, and a deep-burgundy closing sign. Type is Montserrat for every legend and heading, Source Sans 3 for reading text. Nothing imitates a material the page does not render; signs are flat enamel, separated by a 1px gold edge line rather than shadow.

**Key Characteristics:**
- Gate letters A to D as square gold-outlined badges, the one repeated wayfinding device.
- Signs are flat panels with a 14px radius and an inset gold edge line at half opacity.
- Gold is an accent and an edge, never body text on cream.
- One authored motion moment: signs mount from the top edge in a staggered clip reveal.
- Logical properties throughout so the page can mirror to right-to-left.

## Colors

A closed palette taken from the approved identity board; roles are fixed by surface, not by taste.

### Primary
- **Burgundy** (#48151D): the hero ground, the selected gate tab, the emblem plate, filled buttons on cream.
- **Deep Burgundy** (#2F0D13): the header deck, subsidiary signs, the closing sign. The darkest brand tone.

### Secondary
- **Antique Gold** (#B39567): edge lines, gate badges, the primary button on dark, the progress hairline. 5.3:1 on burgundy; never used as text on cream.

### Neutral
- **Warm Cream** (#F0E5D2): the page floor and the Aviation sign.
- **Bright Cream** (#F7F0E4): legend plates, the take panel, swatch labels.
- **Espresso** (#241C19): the colour section ground, body text on cream, the footer.
- **Black** (#111111): the black-logo variant ground only.
- **Soft burgundy ink** (#6A4A4D): secondary text on cream, 6.2:1.

### Named Rules
**The Enamel Rule.** Dark surfaces are burgundy or deep burgundy, never black or neutral grey; black exists only as a logo variant ground.
**The Gold Edge Rule.** Gold separates and accents. It outlines, underlines and fills small controls, and it never carries a paragraph.

## Typography

**Display Font:** Montserrat (with Segoe UI, Arial), self-hosted from `assets/fonts/Montserrat.ttf`.
**Body Font:** Source Sans 3 (with Segoe UI, Arial), from Google Fonts.

**Character:** Montserrat's geometry matches the GATESPORT wordmark, so headings and legends read as extensions of the logo. Source Sans 3 stays out of the way for reading.

### Hierarchy
- **Display** (700, clamp(2.6rem, 6vw, 5rem), 1.02): the single page title.
- **Headline** (700, clamp(2rem, 4.2vw, 3.4rem), 1.08): section headings, balanced, no label above them.
- **Title** (700, 1.35rem, 1.2): sub-blocks such as Clear space and The GP emblem.
- **Body** (400, 1.0625rem, 1.6): supporting copy, held to about 40 to 44ch beside headings.
- **Label** (600 to 700, 0.7 to 0.78rem, +0.07 to +0.14em, uppercase): sign legends, button text, swatch names.

### Named Rules
**The Brand Weight Rule.** Montserrat is used at 500 to 700 only, matching the approved brand typography; the wordmark itself is Bold.

## Layout

A 1360px maximum container with a fluid side gutter of clamp(1rem, 4vw, 3rem). Sections stack as full-bleed bands (burgundy, cream, espresso, cream, bright cream, burgundy, espresso) inside that container. Section padding is clamp(4.5rem, 9vw, 8rem). The hero board is a two-column grid, the Aviation sign on the left and three one-row subsidiary signs on the right, joined by a gold connector rule; it collapses to one column at 1100px. The picker is a four-tab gate band over a stage-and-take pair and a five-up colour strip, collapsing to two and then one column. All spacing and insets use logical properties.

## Elevation & Depth

Flat by default. Depth comes from tonal layering of enamel panels on a different ground, plus a 1px inset gold edge line on signs and a 1px hairline on cream plates. There are no drop shadows. Hover state changes are colour and flex-grow, not lift.

### Named Rules
**The No-Shadow Rule.** A panel is separated by ground contrast, a hairline, or the gold edge line, never by a box shadow.

## Shapes

Rounded rectangles that echo the emblem's large corner radii: 14px for signs, plates and stages; 10px for buttons; 7px for gate badges. Prohibition pictograms are circles with a diagonal slash. The gold edge line follows the panel with a 9px radius, inset 0.5rem.

## Components

### Buttons
- **Shape:** 10px radius, 44px minimum height on touch, Montserrat 700 uppercase at +0.07em.
- **Solid:** antique gold on dark surfaces, burgundy on cream surfaces. Hover inverts to cream or deep burgundy.
- **Line:** transparent with a 1.5px currentColor border; hover fills with the ink colour.
- **Done:** the label swaps to "Copied" with a cream fill for 1.8 seconds; a failed copy shows "Use PNG".

### Signs
- **Cream sign:** the holding-company panel. Burgundy ink, burgundy buttons, gold edge line.
- **Deep sign:** subsidiary panels laid out in one row (gate badge, logo, actions).
- **Mount motion:** clip-path wipe from the top edge, 800ms exponential ease-out, staggered 130ms.

### Gate tabs and swatches
- **Gate band:** four tabs on deep burgundy; the selected tab is burgundy with a 3px gold underline.
- **Swatch strip:** five radio buttons, each showing the current brand on its approved ground; the selected one fills burgundy.

### Colour chips
Tall plates whose widths follow emphasis (burgundy widest); the hovered chip grows. Copying a HEX underlines it.

## Do's and Don'ts

### Do:
- **Do** show every logo only on its approved ground: burgundy on cream, gold on burgundy, cream on espresso, black on gold, white on black.
- **Do** keep gold off body text on cream and keep ink-soft text at or above 4.5:1.
- **Do** use gate letters only where they identify a brand (hero signs and picker tabs).
- **Do** keep the logo's proportions: width set, height auto.

### Don't:
- **Don't** add drop shadows, glass or gradient text; panels are flat enamel.
- **Don't** place a label above a section heading; the heading carries itself.
- **Don't** nest plates inside a bordered container; the gate band and its panels sit directly on the floor.
- **Don't** recolour, stretch, rotate or rearrange any logo, including in demonstrations (the prohibited examples are labelled with a prohibition sign).

Not canonized: Montserrat is flagged by a generic font detector, but it is a binding brand typeface and stays.
