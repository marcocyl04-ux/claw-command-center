# Claw Command Center — Visual Design Specification

## Design Philosophy

**Bloomberg density. Linear clarity. Vercel craft.**

This is an operational dashboard, not a marketing page. Every element exists because it communicates something. Color has meaning. Space has rhythm. Type has hierarchy.

---

## Color System

### Backgrounds (5 depth layers)
| Token | Hex | Usage |
|-------|-----|-------|
| `--bg-root` | `#111111` | App shell, deepest layer |
| `--bg-surface` | `#1a1a1a` | Cards, panels (primary containers) |
| `--bg-elevated` | `#222222` | Hover states, dropdowns, modals |
| `--bg-overlay` | `#2a2a2a` | Active/selected states |
| `--bg-wash` | `#333333` | Code blocks, badges, subtle fills |

**Rule:** Depth = importance. Deeper elements recede. Elevated elements draw attention.

### Foreground (4 contrast tiers)
| Token | Hex | Usage |
|-------|-----|-------|
| `--fg-primary` | `#ececec` | Headlines, key data, values |
| `--fg-secondary` | `#a0a0a0` | Body text, descriptions |
| `--fg-muted` | `#666666` | Timestamps, labels, metadata |
| `--fg-ghost` | `#444444` | Disabled, decorative |

**Rule:** Primary = numbers/data you're scanning for. Secondary = context. Muted = chrome.

### Status Colors (semantic only)
| State | Color | When to Use |
|-------|-------|-------------|
| Success | `#22c55e` | Healthy, online, completed, profit |
| Warning | `#eab308` | Degraded, attention needed, pending |
| Error | `#ef4444` | Critical, offline, failed, loss |
| Info | `#3b82f6` | Informational, in-progress |
| Neutral | `#666666` | Unknown, paused, inactive |

**Rule:** NEVER use status colors for decoration. Every green dot means "healthy." Every red badge means "broken." Diluting this breaks trust.

### Accent
- `#3b82f6` — Cool blue. Used for: interactive elements, links, focus rings, primary buttons
- Muted variants at 8% and 25% opacity for subtle backgrounds/borders

---

## Typography

### Font Stack
- **UI:** Inter (variable weight, excellent at small sizes)
- **Data:** JetBrains Mono (tabular nums, crisp at 11-14px)

### Scale (Minor Third — 1.2 ratio)
| Token | Size | Use |
|-------|------|-----|
| Display | 27.6px | Page titles (1 per view max) |
| Title | 23px | Section headers |
| Heading | 19.2px | Card titles |
| Body | 14px | Default text (intentionally compact) |
| Caption | 13px | Labels, secondary info |
| Micro | 11px | Badges, status text, table headers |

### Key Rules
1. **All numbers in monospace.** Prices, counts, percentages, IDs — always `font-mono`
2. **tabular-nums always on.** Numbers must align vertically in columns
3. **Labels are uppercase micro.** 11px, 600 weight, wide tracking — the Bloomberg pattern
4. **Max 3 type sizes per card.** More = visual noise

---

## Spacing

**4px base grid.** Everything aligns.

| Token | Value | Use |
|-------|-------|-----|
| space-1 | 4px | Hairline gaps, icon margins |
| space-2 | 8px | Tight padding, inline gaps |
| space-3 | 12px | Compact padding |
| space-4 | 16px | Default padding, stack gaps |
| space-5 | 20px | Card internal padding |
| space-6 | 24px | Section gaps, page padding |
| space-8 | 32px | Panel gaps |

**Rule:** Consistent vertical rhythm. Cards use `space-5` padding. Grid gap is `space-4`. No magic numbers.

---

## Component Patterns

### Cards
Three tiers:
1. **`.card`** — Default. Subtle border (`#ffffff08`), `#1a1a1a` background. Barely-there border brightens to `#ffffff12` on hover.
2. **`.card--raised`** — Important content. Elevated background + slight shadow. Stronger hover.
3. **`.card--inset`** — Nested data regions. Darker than parent (recedes visually).

**Interactive cards** get a 1px translateY on hover + accent border glow. Subtle, but you feel it.

### Status Indicators (3 patterns)
1. **Dot** (6px circle) — Inline next to text. Green = online. Red = error. Pulsing = live.
2. **Badge** (pill) — Categorical. Tinted background + matching text. "ACTIVE", "FAILED", "PENDING".
3. **Bar** (left border) — Card-level status. 3px left border in status color.

### Tables
- **Header:** Uppercase micro, sticky, elevated background
- **Rows:** Subtle hover highlight, 1px bottom border
- **Numbers:** Right-aligned, monospace, tabular
- **Compact variant:** For maximum density (Bloomberg-style)

### Metric Cards (KPI Pattern)
```
┌─────────────────────┐
│ TOTAL SESSIONS ←── uppercase micro label
│ 2,847          ←── mono value, large
│ ▲ 12.4%        ←── delta (green=up, red=down)
│ ▁▂▃▅▇▆▅▃▂▁    ←── optional sparkline
└─────────────────────┘
```

### Buttons
- Primary: Blue fill, white text. One per section max.
- Secondary: Border only, hover fills.
- Ghost: No border, hover tints.
- Danger: Red text, red hover fill.

---

## Animation Principles

1. **Under 200ms always.** Transitions confirm actions, never delay them.
2. **ease-out for entering.** Elements decelerate into position.
3. **Data updates are instant.** No animation on number changes.
4. **Three allowed animations:**
   - Hover transitions (100ms)
   - Panel open/close (150ms)
   - Status pulse (2s loop, for live indicators only)
5. **Skeleton shimmer** for loading states — not spinners (except inline).
6. **Respect `prefers-reduced-motion`** — all durations → 0.

---

## Layout

### Shell Structure
```
┌──────────┬────────────────────────────────┐
│          │           HEADER (56px)         │
│ SIDEBAR  ├────────────────────────────────│
│ (240px)  │                                │
│          │           MAIN CONTENT          │
│          │        (12-col grid, 16px gap)  │
│          │                                │
└──────────┴────────────────────────────────┘
```

- Sidebar: Fixed 240px, scrollable, nav groups with uppercase labels
- Header: Sticky 56px, blur backdrop, breadcrumb + actions
- Main: 12-column grid, `space-6` padding, scrollable

### Responsive Notes
- At narrow viewports: sidebar collapses to icon rail (48px)
- Grid columns collapse: 12 → 6 → 1
- Tables get horizontal scroll wrapper

---

## Scrollbar
Custom, minimal:
- 6px width, transparent track
- Thumb: `#333333`, rounds to pill
- Hover: slightly brighter

---

## Focus & Accessibility
- `:focus-visible` shows 2px blue ring with 2px offset
- All status colors pass 3:1 contrast against `#1a1a1a`
- Text colors pass WCAG AA against their backgrounds
- `::selection` uses accent tint
- `.sr-only` class for screen reader content

---

## File Reference
- **`design-system.css`** — Complete implementation of all tokens and components above
- Import Inter from Google Fonts (variable, 400/500/600)
- Import JetBrains Mono from Google Fonts (variable, 400/500/600)
