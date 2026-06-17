# Page Creation Guide

Directions for adding or updating pages in this portfolio site. Follow these conventions so new pages stay consistent with the existing stack (FastAPI, Jinja2, Tailwind CDN, Alpine.js, HTMX).

---

## 1. Browser tab title

**Every page must use the tab title `Alex H. Lee`.**

Do not append page names, suffixes, or dynamic values (e.g. avoid `Alex H. Lee — Home` or `About — {{ portfolio.name }}`).

- **Default:** `app/templates/base.html` sets the fallback:

  ```jinja2
  <title>{% block title %}Alex H. Lee{% endblock %}</title>
  ```

- **Per-page override:** Each page template should repeat the same value so the rule stays explicit:

  ```jinja2
  {% block title %}Alex H. Lee{% endblock %}
  ```

If you add a new page, include that block even though it matches the default.

---

## 2. Add a route handler

Register the page in `app/routers/pages.py`:

1. Add a `@router.get("/your-path")` handler.
2. Call `load_portfolio()` to load YAML content.
3. Return `templates.TemplateResponse("your-page.html", {"request": request, "portfolio": data})`.

Example:

```python
@router.get("/contact")
async def contact(request: Request):
    data = load_portfolio()
    return templates.TemplateResponse(
        "contact.html", {"request": request, "portfolio": data}
    )
```

---

## 3. Create the Jinja2 template

Add `app/templates/your-page.html` that:

1. **Extends** `base.html`:

   ```jinja2
   {% extends "base.html" %}
   ```

2. **Sets the tab title** (see section 1):

   ```jinja2
   {% block title %}Alex H. Lee{% endblock %}
   ```

3. **Optionally overrides meta description:**

   ```jinja2
   {% block meta_description %}Short description for SEO.{% endblock %}
   ```

4. **Fills the main content block:**

   ```jinja2
   {% block content %}
   <!-- page markup here -->
   {% endblock %}
   ```

Use existing pages (`index.html`, `about.html`, `projects.html`) as layout references. Prefer Tailwind utility classes; add shared styles to `static/css/custom.css` only when utilities are not enough.

---

## 4. Add a nav link

Update the navigation in `app/templates/base.html`:

```html
<li><a href="/your-path" class="nav-link hover:text-white transition-colors">Label</a></li>
```

The active link styling is handled in `static/js/interactions.js` via the `.nav-link` class and current pathname.

---

## 5. Content from YAML (optional)

Page copy and structured data live in the `content/` directory, split by category. All files are merged at request time by `app/content.py` into a single `portfolio` dict — templates access everything the same way regardless of which file the data lives in.

```
content/
├── profile.yaml              # name, tagline, bio, social (site-wide identity)
├── professional/
│   ├── skills.yaml
│   ├── experience.yaml
│   ├── education.yaml
│   └── projects.yaml
└── personal/
    └── projects.yaml
```

**Rules:**
- **Professional content** (work experience, technical skills, academic credentials, professional projects) → `content/professional/`
- **Personal content** (personal projects, hobbies, side interests) → `content/personal/`
- **Site-wide identity** (name, tagline, bio, social links) → `content/profile.yaml`
- Each YAML file must use unique top-level keys — files are merged with `dict.update()` so duplicate keys will overwrite each other.
- Professional and personal projects use separate keys: `projects` (professional) and `personal_projects` (personal).
- Each project entry should include a unique `slug` (lowercase kebab-case). Used for deep links: `/projects#project-{slug}`. Slugs must be unique across **all** projects (professional + personal).
- Experience entries may include an optional `projects` list linking to project slugs (rendered on the About page as pill links that open the project modal). See section 6 for deep-linking details.
- Access values in templates via `{{ portfolio.your_key }}` as before.
- To add content for a new page, add a new key to an existing file or create a new file in the appropriate directory.

---

## 6. Interactive behavior

| Need | Use |
|------|-----|
| Toggle panels, local UI state | Alpine.js (`x-data`, `x-show`, `x-transition`) |
| Lazy-load HTML from the server | HTMX (`hx-get`, `hx-trigger`, etc.) + a route in `app/main.py` or a router |
| Scroll effects, nav highlighting | `static/js/interactions.js` |

### Modals / popups

This site uses **Alpine.js + `x-teleport`** for all popup modals. This is the standard pattern — do not use a separate shared modal with data passed through attributes.

**How it works:**

Each element that needs a popup owns its own `x-data` scope and embeds its modal content directly inside a `<template x-teleport="body">` block:

```html
<article x-data="{ open: false }">

  <button @click="open = true">Open</button>

  <template x-teleport="body">
    <div
      x-show="open"
      x-transition:enter="transition ease-out duration-200"
      x-transition:enter-start="opacity-0"
      x-transition:enter-end="opacity-100"
      x-transition:leave="transition ease-in duration-150"
      x-transition:leave-start="opacity-100"
      x-transition:leave-end="opacity-0"
      @keydown.escape.window="open = false"
      class="fixed inset-0 z-50 flex items-center justify-center p-4"
      style="display:none">

      <!-- Backdrop -->
      <div class="absolute inset-0 bg-black/75" @click="open = false"></div>

      <!-- Panel -->
      <div class="relative ... bg-gray-900 rounded-xl ..." @click.stop>
        <!-- Jinja2-rendered content goes here — no data passing needed -->
        <button @click="open = false" aria-label="Close">✕</button>
        ...
      </div>
    </div>
  </template>

</article>
```

**Why `x-teleport`:**

- `x-teleport="body"` moves the modal DOM node to `<body>` at runtime, escaping any `overflow: hidden`, stacking context, or z-index issues from ancestor elements.
- The modal still belongs to the same Alpine.js component scope — `open` works correctly from both the button and the close button inside the modal.
- All content is rendered by Jinja2 server-side and is already in the HTML. No data-passing gymnastics needed for rich content like lists or formatted text.

**Key details:**
- `style="display:none"` prevents a flash of the modal before Alpine initializes.
- `@keydown.escape.window` closes on Escape key.
- `@click` on the backdrop closes the modal; `@click.stop` on the panel prevents the backdrop click from firing when clicking inside.
- `z-50` on the modal matches the nav's z-index; since the modal is later in the DOM it renders on top.

**Reference implementations:**
- `app/templates/projects.html` — project detail modal (one per card, `x-teleport`)
- `app/templates/about.html` — digital diploma viewer (`x-show` without teleport, since it's a shared modal at section level)

### Deep-linking to a specific project modal

Every project card has a stable `id="project-{slug}"` and uses `x-init` to auto-open its modal when the page URL hash matches:

```html
<article
  id="project-{{ project.slug }}"
  x-data="{ open: false }"
  x-init="if (location.hash === '#project-{{ project.slug }}') { $nextTick(() => { open = true }) }">
```

To link to a specific project from another page (e.g., the About page experience section):

```html
<a href="/projects#project-predictive-maintenance-pipeline">Predictive Maintenance Pipeline →</a>
```

When the Projects page loads with that hash, Alpine's `x-init` detects the match and opens the modal via `$nextTick` (which waits for `x-teleport` to finish moving the modal to `<body>` before setting `open = true`).

**Rules for slugs:**
- Defined as a `slug` field in each project entry in the YAML (`content/professional/projects.yaml`, `content/personal/projects.yaml`).
- Must be **unique across all projects** (professional + personal) since they share one URL space.
- Use lowercase kebab-case only (e.g., `predictive-maintenance-pipeline`). No spaces, no special characters.
- The URL anchor is always `/projects#project-{slug}`.

**Linking from experience entries:**
Add a `projects` list to an experience entry in `content/professional/experience.yaml`:
```yaml
projects:
  - title: "Predictive Maintenance Pipeline"
    slug: "predictive-maintenance-pipeline"
```
The About page route (`pages.py`) builds a `projects_by_slug` dict from all project YAML data and passes it to the template. The template looks up the full project object by slug and renders a self-contained `x-teleport` modal inline — the same pattern as the Projects page. No API call or network request is made; all content is already available at render time.

---

### Passing server-rendered values into Alpine.js event handlers

**Never interpolate Jinja2 values directly inside an `@click` (or any Alpine event) attribute as string literals.** Quote characters in the value will break the HTML attribute and Alpine will silently do nothing.

```html
<!-- WRONG — breaks if value contains quotes -->
@click="myVar = '{{ some.value }}'"

<!-- WRONG — tojson wraps in double quotes, collides with the attribute delimiters -->
@click="myVar = {{ some.value | tojson }}"
```

**The correct pattern: `data-*` attributes + `$el.dataset`.**

Store the server-rendered value in a `data-*` attribute (Jinja2's auto-escaping makes it safe), then read it in the handler:

```html
<button
  data-my-value="{{ some.value }}"
  @click="myVar = $el.dataset.myValue">
```

- Jinja2 auto-escaping handles all special characters (quotes, ampersands, etc.) in the HTML attribute.
- The `@click` expression contains no string literals — just a DOM property read.
- `data-my-value` is accessed as `$el.dataset.myValue` (camelCase conversion is automatic in the browser).

This pattern is used for the Digital Diploma button in `about.html` and should be the default approach whenever a Jinja2 loop or variable needs to pass a value to an Alpine.js handler.

---

## 7. Checklist for a new page

- [ ] Route in `app/routers/pages.py`
- [ ] Template in `app/templates/` extending `base.html`
- [ ] `{% block title %}Alex H. Lee{% endblock %}`
- [ ] Nav link in `base.html` (if the page should appear in the header)
- [ ] YAML updates in the appropriate `content/` file (professional, personal, or profile)
- [ ] Manual check: visit the URL, confirm tab title, nav highlight, and mobile layout

---

## File map

```
app/
├── main.py              # App setup, static file mount, health check
├── routers/
│   └── pages.py         # Page routes
└── templates/
    ├── base.html        # Layout, nav, footer, CDN scripts
    └── *.html           # One template per page

content/
├── profile.yaml             # Site-wide identity
├── professional/            # Work, skills, education, projects
│   ├── skills.yaml
│   ├── experience.yaml
│   ├── education.yaml
│   └── projects.yaml
└── personal/                # Personal projects, hobbies
    └── projects.yaml          # key: personal_projects

app/content.py               # Merges all content/ YAML files into one dict

static/
├── css/custom.css
├── js/interactions.js
└── images/
    ├── logos/           # All logo/icon assets (see context/assets.md)
    └── (figures, photos, etc.)

context/
├── page-creation.md
└── assets.md            # Image and logo conventions
```
