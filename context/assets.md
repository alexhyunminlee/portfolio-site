# Assets Guide

This project uses **two separate systems** for visual assets depending on their purpose. Using the right one matters for styling flexibility, especially as the site grows.

---

## System 1 — Inline SVG icons (`app/templates/icons/`)

**Use for: any icon used as part of the UI** — social links, buttons, nav elements, status indicators, skill badges, etc.

### Why inline SVG?

When an SVG is included via `{% include 'icons/name.svg' %}`, Jinja2 pastes the SVG markup directly into the HTML. Because the SVG is part of the DOM, it responds to CSS like any other element:

- `fill="currentColor"` makes the icon inherit the CSS `color` property.
- Tailwind classes like `hover:text-indigo-400` on the parent `<a>` change both text and icon color simultaneously — no extra CSS needed.
- Icons are sharp at any size and add zero HTTP requests.
- Changing a color site-wide means editing one SVG file.

Using `<img src="...">` for UI icons breaks all of this: the browser treats the file as an opaque image, and CSS cannot reach inside to change the fill.

### File location

```
app/templates/icons/
├── github.svg
├── linkedin.svg
└── email.svg
```

Icons live in the templates directory alongside the HTML — not in `static/` — because they are template fragments, not standalone served files.

### How to use in a template

```jinja2
<a href="{{ url }}" class="text-gray-500 hover:text-indigo-400 transition-colors" aria-label="GitHub">
  {% include 'icons/github.svg' %}
</a>
```

The SVG itself should always have:
- `fill="currentColor"` — so it inherits color from the parent
- `class="w-5 h-5"` (or whatever size fits) — Tailwind controls the size
- `aria-hidden="true"` — the parent `<a>` carries the `aria-label`

### Adding a new icon

1. Find the SVG path data for your icon (e.g. from [heroicons.com](https://heroicons.com) or [simpleicons.org](https://simpleicons.org)).
2. Create `app/templates/icons/your-icon.svg` following this template:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5" aria-hidden="true">
  <path d="...path data..."/>
</svg>
```

3. Include it anywhere in a template: `{% include 'icons/your-icon.svg' %}`

---

## System 2 — Static image assets (`static/images/`)

**Use for: photos, figures, screenshots, and brand/logo images that are referenced as `<img>` tags** — profile photo, project screenshots, company logos in the experience section, etc.

These files are served directly by FastAPI's static file mount and referenced with `/static/images/...` paths.

### Directory layout

```
static/
└── images/
    ├── logos/          ← third-party brand marks (company logos, tech logos)
    └── (other images)  ← photos, diagrams, project screenshots
```

| Folder | What goes here |
|--------|----------------|
| `static/images/logos/` | Brand marks used as images — e.g. a company logo in the experience section, a university seal. Not UI icons. |
| `static/images/` | Everything else: headshots, project screenshots, diagrams. |

### How to reference in a template

```html
<img src="/static/images/headshot.jpg" alt="Alex H. Lee" class="rounded-full w-24 h-24" />
<img src="/static/images/logos/ut-austin.png" alt="UT Austin" class="h-8" />
```

### Format guide

| Format | Use when |
|--------|----------|
| SVG | Simple brand marks / logos used as images (flat, vector art) |
| WebP / JPEG | Photos, hero images, screenshots |
| PNG | Images requiring a transparent background |

Optimize images before committing — large uncompressed files slow page load.

---

## Quick decision guide

> **Is it a UI element you want to style with CSS (hover color, size via Tailwind)?**
> → Inline SVG icon → `app/templates/icons/`

> **Is it a photo, diagram, screenshot, or brand logo displayed as a standalone image?**
> → Static asset → `static/images/`

---

## Current icon inventory

| Icon | Source file | Inline icon | Notes |
|------|-------------|-------------|-------|
| GitHub | `static/images/logos/github_logo.svg` | `app/templates/icons/github.svg` | `fill="currentColor"`, styled via `text-white` |
| LinkedIn | `static/images/logos/linkedin_logo.svg` | `app/templates/icons/linkedin.svg` | Background rect uses `currentColor` (#0A66C2); logo mark hardcoded `fill="#fff"` |
| Email | `static/images/logos/email_logo.svg` | `app/templates/icons/email.svg` | `fill="currentColor"`, styled via `text-white` |
