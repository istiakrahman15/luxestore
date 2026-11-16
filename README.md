# LuxeStore

A premium-feeling e-commerce **demo** storefront built with Django 5 — created as a portfolio
piece to showcase clean, modular Django development rather than to run a real shop.

> **Scope note:** LuxeStore intentionally has **no accounts, cart, checkout, or payments**.
> It's a browsing experience — search, filter, and view products — backed by a clean model
> layer and a fully customized Django admin. Adding real commerce features was a deliberate
> non-goal; see [Why no cart?](#why-no-cart) below.

![Django](https://img.shields.io/badge/Django-5.0-0C4B33?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---


## Features

**Storefront**
- Home, Products, Product Detail, About, Contact, and a custom 404 page
- Hero banner, featured products, category grid, "why choose us," latest products, and a
  UI-only newsletter section
- Live search and category filtering on the product list (query-string driven, no JS required)
- Featured badges and in-stock / out-of-stock states on every product card
- Graceful placeholder tiles for products without an uploaded image — no broken image icons

**Design**
- Apple / Vercel / Stripe–inspired minimalist layout: rounded cards, soft shadows, restrained motion
- Dark mode and light mode with a working toggle, persisted via `localStorage`
- Custom type system: **Fraunces** for display, **Inter** for body copy, **IBM Plex Mono** for
  prices and labels
- Signature "gilded edge" hover state on cards, a champagne-gold accent against near-black /
  near-white surfaces
- Fully responsive, mobile-first layout built on the Bootstrap 5 grid
- Sticky header, scroll-to-top button, scroll-reveal animations, smooth scrolling, and a subtle
  page-load progress bar
- Respects `prefers-reduced-motion`

**Admin**
- Custom branding: *"LuxeStore Admin"* header, title, and index title
- Product thumbnails and a larger image preview in the edit form
- Search across name / description, filters by category / stock / featured status
- Sortable columns (price, date created) and a date-hierarchy drilldown
- One-click boolean toggles for stock and featured status in the changelist

**Data**
- 5 demo categories, ~19 demo products
- Seeded via a management command **or** a JSON fixture (see below)

---

## Technology used

| Layer | Tech |
|---|---|
| Backend | Python 3.13, Django 5.0 |
| Database | SQLite |
| Frontend | HTML5, CSS3 (custom, no framework build step), Bootstrap 5, vanilla JavaScript |
| Images | Pillow (for `ImageField` support) |
| Icons | Bootstrap Icons |
| Fonts | Fraunces, Inter, IBM Plex Mono (Google Fonts) |

No Node/npm build step, no frontend framework, no third-party JS libraries beyond Bootstrap's
own bundle — everything is served as plain static files.

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/istiakrahman15/luxestore.git
cd luxestore

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Running locally

```bash
# 4. Apply migrations
python manage.py migrate

# 5. Load demo data (choose ONE of the following)
python manage.py seed_demo_data          # management command (recommended)
# — or —
python manage.py loaddata demo_data      # JSON fixture, same dataset

# 6. Create an admin account
python manage.py createsuperuser
# Follow the prompts for username / email / password

# 7. Run the dev server
python manage.py runserver
```

Then visit:
- **Storefront:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/

To reset and reseed the catalog at any point:

```bash
python manage.py seed_demo_data --flush
```

---

## Deploying to Vercel

LuxeStore is pre-configured for [Vercel's zero-config Django support](https://vercel.com/docs/frameworks/full-stack/django).
Two things are different in production versus local dev, both already handled in `settings.py`:

- **Database:** Vercel's filesystem is ephemeral, so SQLite can't be used in production. The
  project automatically switches to Postgres whenever a `DATABASE_URL` environment variable is
  present, and falls back to SQLite when it isn't (i.e. on your machine).
- **Uploaded images:** for the same reason, files uploaded through the admin (`ImageField`)
  won't persist between requests/deploys on Vercel. Products without an image already show a
  built-in placeholder tile, so this is safe to ignore for a demo. If you want uploads to
  persist, connect [`django-storages`](https://django-storages.readthedocs.io/) to an
  S3-compatible bucket (Cloudflare R2's free tier works well) and set `DEFAULT_FILE_STORAGE`
  accordingly.

### 1. Add a Postgres database
In the Vercel dashboard: **Storage → Create Database → Postgres** (or connect Neon). This
automatically creates a `DATABASE_URL` environment variable on your project.

### 2. Set the remaining environment variables
In **Project Settings → Environment Variables**, add:

| Key | Value |
|---|---|
| `SECRET_KEY` | A long random string — generate one with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-project.vercel.app` (add your custom domain later, comma-separated) |

(`DATABASE_URL` is already set for you from step 1.) See `.env.local.example` for the full list
with comments.

### 3. Import and deploy
- Push this repo to GitHub (see below)
- In Vercel: **Add New → Project**, select the repo
- Vercel detects `manage.py` automatically, runs `collectstatic` for you, and deploys — no
  `vercel.json` edits needed beyond what's already in this repo
- Click **Deploy**

### 4. Run migrations against the live database
Locally, pull the environment variables Vercel just created, then run Django's normal commands
against them:

```bash
npm i -g vercel        # if you don't have the CLI yet
vercel link             # connect this folder to your Vercel project
vercel pull              # writes .env.local with DATABASE_URL, SECRET_KEY, etc.

python manage.py migrate
python manage.py seed_demo_data
python manage.py createsuperuser
```

`settings.py` automatically loads `.env.local` via `python-dotenv` if it's present, so these
commands will run against your **production** database — the same one your live Vercel
deployment uses.

### 5. Verify
Visit your Vercel URL and `/admin/` — both should look identical to your local setup, just
backed by Postgres instead of SQLite.

---

## Project structure

```
luxestore/
├── luxestore/                 # Project package
│   ├── settings.py            # Apps, templates, static/media config, handler404
│   ├── urls.py                # Root URL conf (admin + store app + media/static in DEBUG)
│   ├── asgi.py / wsgi.py
│
├── store/                     # The only Django app — the product catalog
│   ├── models.py              # Category, Product
│   ├── admin.py                # Branded, customized ModelAdmin classes
│   ├── views.py                # home, product_list, product_detail, about, contact, custom_404
│   ├── urls.py                 # App-level URL conf (namespaced as "store")
│   ├── context_processors.py   # Injects SITE_NAME / SITE_TAGLINE into every template
│   ├── management/commands/
│   │   └── seed_demo_data.py   # Idempotent demo data seeder (--flush to reset)
│   ├── fixtures/
│   │   └── demo_data.json      # Same dataset as a loaddata-compatible fixture
│   └── migrations/
│
├── templates/
│   ├── base.html                # Navbar, footer, theme toggle, scroll-to-top, loading bar
│   └── store/
│       ├── home.html            # Hero, featured, categories, why-us, latest, newsletter
│       ├── product_list.html    # Search + category filter chips + grid
│       ├── product_detail.html  # Media, price/stock, description, related products
│       ├── about.html
│       ├── contact.html         # UI-only form (no backend submission)
│       ├── 404.html             # Custom branded error page
│       └── _product_card.html   # Shared product card partial
│
├── static/
│   ├── css/style.css            # Design tokens + every component style
│   ├── js/main.js               # Theme toggle, scroll-to-top, reveal animations
│   └── img/favicon.svg
│
├── media/products/              # Uploaded product images (gitignored, kept via .gitkeep)
├── requirements.txt
├── manage.py
├── vercel.json                  # Vercel Function config (maxDuration)
├── .env.local.example           # Template for production-style env vars
├── .gitignore
└── README.md
```

---

## Django Admin

The admin is available at `/admin/` and requires a superuser account (see step 6 above — Django's
built-in `createsuperuser` command handles this; only superusers/staff can log in).

Once inside, **Store Catalog → Products** gives you:
- A thumbnail column and an inline image preview on the edit form
- Search across name, description, and short description
- Filters for category, stock status, and featured status
- Sorting by price and creation date, plus a date-hierarchy drilldown
- Boolean toggle icons for stock and featured status directly in the list view

**Store Catalog → Categories** gives you name/slug/description/icon management, with the slug
auto-populated from the name.

---

## Why no cart?

The brief for this project was to demonstrate Django fundamentals for a portfolio — models,
admin customization, querysets, templating, and a polished UI — without the scope (and security
surface) of real commerce logic. Authentication, cart state, checkout flows, and payment
integrations are each substantial projects on their own; bolting on a shallow version of them
would add surface area without demonstrating anything new. If you'd like to extend this project,
natural next steps would be a session-based cart app, Django's built-in auth for accounts, and a
sandboxed payment provider (e.g. Stripe test mode).

---

## License

MIT — use this as a starting point for your own portfolio projects.
