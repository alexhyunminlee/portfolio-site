# Page Creation Guide

Directions for adding or updating pages in this portfolio site. Follow these conventions so new pages stay consistent with the existing stack (FastAPI, Jinja2, Tailwind CDN, Alpine.js, HTMX).

---

## 1. Browser tab title

**Every page must use the tab title `Alex H Lee`.**

Do not append page names, suffixes, or dynamic values (e.g. avoid `Alex H Lee — Home` or `About — {{ portfolio.name }}`).

- **Default:** `app/templates/base.html` sets the fallback:

  ```jinja2
  <title>{% block title %}Alex H Lee{% endblock %}</title>
  ```

- **Per-page override:** Each page template should repeat the same value so the rule stays explicit:

  ```jinja2
  {% block title %}Alex H Lee{% endblock %}
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
   {% block title %}Alex H Lee{% endblock %}
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

Page copy and structured data live in `content/portfolio.yaml`.

- Add new top-level keys or lists as needed for the page.
- Access values in templates via the `portfolio` context (e.g. `{{ portfolio.your_key }}`).
- Keep placeholder/sample data in YAML; avoid hardcoding personal content in templates when it belongs in the content file.

---

## 6. Interactive behavior

| Need | Use |
|------|-----|
| Toggle panels, local UI state | Alpine.js (`x-data`, `x-show`, `x-transition`) |
| Lazy-load HTML from the server | HTMX (`hx-get`, `hx-trigger`, etc.) + a route in `app/main.py` or a router |
| Scroll effects, nav highlighting | `static/js/interactions.js` |

For HTMX endpoints that return HTML fragments, follow the pattern in `app/main.py` (`GET /api/fun-facts`).

---

## 7. Checklist for a new page

- [ ] Route in `app/routers/pages.py`
- [ ] Template in `app/templates/` extending `base.html`
- [ ] `{% block title %}Alex H Lee{% endblock %}`
- [ ] Nav link in `base.html` (if the page should appear in the header)
- [ ] YAML updates in `content/portfolio.yaml` (if applicable)
- [ ] Manual check: visit the URL, confirm tab title, nav highlight, and mobile layout

---

## File map

```
app/
├── main.py              # App setup, static mount, API stubs (e.g. HTMX fragments)
├── routers/
│   └── pages.py         # Page routes
└── templates/
    ├── base.html        # Layout, nav, footer, CDN scripts
    └── *.html           # One template per page

content/
└── portfolio.yaml       # Site content

static/
├── css/custom.css
└── js/interactions.js
```
