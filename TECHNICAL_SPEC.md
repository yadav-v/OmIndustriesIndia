# OM Industries Technical Specification

## 1. Overview

- **Project:** OM Industries (Python Flask web app)
- **Purpose:** Industrial products/services display, ordering, contact, feedback, and admin management.
- **Language/Framework:** Python 3.x with Flask.
- **Template Engine:** Jinja2.
- **Frontend:** Bootstrap, custom CSS, Font Awesome, AOS animations, Slick carousel.
- **Databases:** SQLite local default, PostgreSQL (Supabase) optional.

## 2. Key components

- `app.py`: main application entry point with route definitions, DB setup, business logic, and email operations.
- `products_data.py`: static service/product seed data.
- `templates/`: UI layer with `public/` and `admin/` sections.
- `static/`: CSS, JS, images.
- `requirements.txt`: Python dependencies.
- `.env`: runtime config values (DB URL, secret key, SMTP, etc.).

## 3. Database engine selection

- `DATABASE_URL` present in environment -> PostgreSQL via `psycopg2`.
- If missing -> SQLite local file `database.db`.
- Checks and migrations run in `init_db()`.

## 4. Data models

### Services
- `id`, `name`, `slug`, `division`, `division_id`, `short_desc`, `description`, `image`, `gallery_images`, `sort_order`, `created_at`.

### Feedback
- `id`, `name`, `rating`, `message`, `status`, `date`.

### Contacts
- `id`, `name`, `email`, `phone`, `message`, `date`.

### Orders
- `id`, `name`, `address`, `phone`, `email`, `quantity`, `order_date`, `status`, `created_at`.

### Order Status Log
- `id`, `order_id`, `status`, `changed_at`.

## 5. Routing and functionality

### Public routes
- `/` home
- `/about` about
- `/services` services listing
- `/service/<slug>` service details
- `/product/<id>` product detail
- `/feedback` feedback form
- `/contact` contact form
- `/search` goods search endpoint

### Admin routes
- `/admin` admin login
- `/admin/dashboard` admin overview
- `/admin/services`, `/admin/users`, `/admin/orders`, `/admin/feedback`, `/admin/contacts` CRUD and listing

## 6. UI Architecture

- `templates/public/base_public.html`: includes common head, header, footer, scripts, and chatbot widget.
- `templates/public/components/header_public.html`: top bar + navigation; currently `fixed-top`.
- `templates/public/components/footer_public.html`: footer and contact links.

## 7. Styles and appearance

- `static/css/style.css`: branding colors, header/nav styling, smooth hover effects.
- `static/css/chatbot.css`: floating assistant widget.

### Fixed header adjustment
- `header` class now `fixed-top`.
- Body top padding adjusted to `80px` in style to avoid content overlap.

## 8. Search and interactive features

- `static/js/search.js`: typeahead search, realtime suggestions, result click nav.
- `static/js/chatbot.js`: UI show/hide interactions for built-in chatbot widget.

## 9. Email and contact flow

- `smtplib` + `email.mime` used in contact/feedback forms.
- Configurable SMTP host, port, user, pass in `.env`.

## 10. Setup and deployment

### Local (SQLite)
- `pip install -r requirements.txt`
- `python app.py`

### Supabase / PostgreSQL
- `DATABASE_URL=postgresql://<user>:<pass>@<host>:<port>/<db>` in `.env`
- optionally `psycopg2-binary` installed

### Misc
- `create_db.py`, `migrate_db.py` for DB creation/migration.
- recommended to set `SECRET_KEY` in `.env`.


