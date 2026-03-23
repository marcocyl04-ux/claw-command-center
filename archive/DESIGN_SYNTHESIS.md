# SYNTHESIS: The 8.5/10 Formula for Claw Command Center

## The 7 Premium Techniques (Stolen, Not Copied)

### 1. Layered Surface Elevation (from Image 1 - Finance)
**Technique:** Every surface is one barely-perceptible step lighter than its parent
- `#141414` → `#1A1A1A` → `#1E1E1E` → `#242424`
- Separated by `rgba(255,255,255,0.06)` borders
- Creates physical depth without aggressive shadows

**CSS Implementation:**
```css
--bg-canvas: #141414;
--bg-card: #1A1A1A;
--bg-elevated: #1E1E1E;
--bg-hover: #242424;
border: 1px solid rgba(255,255,255,0.06);
```

### 2. Ambient Environmental Glow (from Image 2 - Gantt)
**Technique:** Subtle radial gradient emanating from behind the main card
- `radial-gradient(ellipse at 50% 100%, rgba(30,180,140,0.1) 0%, transparent 60%)`
- Creates "floating above a lit surface" effect
- The under-cabinet lighting of dashboard design

**CSS Implementation:**
```css
.app::before {
  content: '';
  position: fixed;
  bottom: -20%;
  left: 50%;
  transform: translateX(-50%);
  width: 100vw;
  height: 60vh;
  background: radial-gradient(ellipse, rgba(224,145,42,0.08) 0%, transparent 70%);
  pointer-events: none;
  z-index: -1;
}
```

### 3. Background Bokeh/Blobs (from Image 3 - Tracking)
**Technique:** Large, heavily blurred colored orbs positioned at edges
- `filter: blur(80px)` on `rgba(245,200,66,0.15)` circles
- Creates atmospheric depth without distraction
- Two colors: primary accent + secondary (amber + teal)

**CSS Implementation:**
```css
.orb-1 {
  position: fixed;
  top: -10%;
  right: -5%;
  width: 500px;
  height: 500px;
  background: rgba(224,145,42,0.12);
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
}
.orb-2 {
  position: fixed;
  bottom: -10%;
  left: -5%;
  width: 400px;
  height: 400px;
  background: rgba(43,191,160,0.08);
  border-radius: 50%;
  filter: blur(60px);
  pointer-events: none;
}
```

### 4. 3D Particle Mesh Hero (from Image 4 - Splunk)
**Technique:** WebGL-rendered point cloud with additive blending
- Particles intensify brightness when overlapping
- Ambient bottom glow on the 3D scene
- Creates "living data" feeling

**For Claw (simplified):** Large hero chart with gradient area fill and animated sparkline

### 5. Gradient Bleed-Through Glass (from Image 5 - Calendar)
**Technique:** Warm gradient behind frosted glass window
- `backdrop-filter: blur(40px)` on semi-transparent dark
- Background opacity: 0.88-0.94 (critical range)
- Creates living warmth underneath

**CSS Implementation:**
```css
body {
  background: linear-gradient(135deg, #8B5CF6 0%, #F472B6 50%, #FB923C 100%);
}
.app {
  background: rgba(20,20,20,0.92);
  backdrop-filter: blur(40px) saturate(1.2);
}
```

### 6. Heatmap Intensity Grid (from Image 6 - Sapphire)
**Technique:** Grid cells with opacity-based intensity
- `rgba(139,92,246, var(--intensity))` where intensity 0.1-0.9
- Creates glanceable pattern recognition
- GitHub contribution graph style but with brand colors

### 7. Timeline with Avatar Stacks (from Image 7 - Relatewise)
**Technique:** Clean vertical timeline with overlapping avatars
- `-6px margin-left` on stacked avatars
- Creates social proof and activity sense
- Minimal, focused, task-oriented

---

## The 8.5/10 Formula for Claw

### Color System: "Thermal Predator"
```css
/* Base (cool-neutral dark) */
--bg-canvas: #141414;
--bg-card: #1A1A1A;
--bg-elevated: #1E1E1E;
--bg-hover: #242424;

/* Accent (warm amber - predatory) */
--claw-amber: #E0912A;
--claw-amber-glow: rgba(224,145,42,0.4);
--claw-amber-subtle: rgba(224,145,42,0.12);

/* Secondary (signal teal - success) */
--signal-teal: #2BBFA0;
--signal-teal-glow: rgba(43,191,160,0.3);

/* Semantic */
--blood-red: #E5484D;
--bone-white: #EDEDEC;
--muted-gray: #8A8A8A;

/* Borders */
--border-subtle: rgba(255,255,255,0.05);
--border-default: rgba(255,255,255,0.08);
--border-active: rgba(224,145,42,0.3);
```

### Typography: "Precise Wealth"
```css
--font-display: 'Geist', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Hero P&L */
font-size: 48px;
font-weight: 700;
font-family: var(--font-mono);
font-variant-numeric: tabular-nums slashed-zero;
color: var(--claw-amber);
text-shadow: 0 0 40px var(--claw-amber-subtle);

/* Labels */
font-size: 11px;
font-weight: 500;
text-transform: uppercase;
letter-spacing: 0.08em;
color: var(--muted-gray);
```

### Visual Effects Stack
```css
/* 1. Ambient orbs */
.orb { filter: blur(80px); opacity: 0.12; }

/* 2. Card elevation */
.card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.4);
}

/* 3. Hero glow */
.hero-card {
  box-shadow:
    0 0 40px var(--claw-amber-subtle),
    0 0 80px rgba(224,145,42,0.06),
    inset 0 1px 0 rgba(224,145,42,0.1);
}

/* 4. Hover lift */
.card:hover {
  transform: translateY(-2px);
  border-color: var(--border-active);
  box-shadow: 0 4px 24px rgba(224,145,42,0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 5. Ambient background glow */
body::before {
  background: radial-gradient(ellipse at 30% 50%, rgba(224,145,42,0.05) 0%, transparent 70%);
}
```

### Layout: "Asymmetric Bento with Hero"
```
┌─────────────────────────────────────┐
│  HERO: Portfolio Value (2fr)        │
│  $9.10 (glowing amber)              │
│  ▲ +$0.42 (+4.8%)                   │
├──────────┬──────────┬───────────────┤
│ Win Rate │ Positions│ Pending       │
│   71%    │   94     │   12          │
├──────────┴──────────┴───────────────┤
│  CHART (60%)    │  POSITIONS (40%) │
│  (large hero)   │  (scrollable)    │
├──────────┬──────────┬───────────────┤
│ Recent   │ Skills   │ Activity      │
│ Trades   │ Radar    │ Feed          │
└──────────┴──────────┴───────────────┘
```

### Animation: "Restrained Cinematic"
```css
/* Entrance */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}
.hero { animation: fadeUp 0.5s ease-out; }
.tile:nth-child(1) { animation: fadeUp 0.5s ease-out 0.1s both; }
.tile:nth-child(2) { animation: fadeUp 0.5s ease-out 0.2s both; }

/* Hover */
transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* Pulse glow on live indicator */
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px var(--claw-amber-subtle); }
  50% { box-shadow: 0 0 30px var(--claw-amber-glow); }
}
```

---

## Implementation Priority

1. **Color system + ambient orbs** (highest impact)
2. **Typography + spacing** (readability)
3. **Card elevation + glows** (tactile feel)
4. **Hero layout** (visual hierarchy)
5. **Animations** (polish)

This formula takes Claw from 5/10 to 8.5/10.
