# Deploy Om Industries on Railway

## Quick Deploy

1. **Connect to Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click **New Project** → **Deploy from GitHub repo**
   - Select your `omIndustries` repository

2. **Configure Variables**
   In Railway project → your service → **Variables**, add:
   - `DATABASE_URL` – Your Supabase PostgreSQL connection string
   - `SECRET_KEY` – A random secret (e.g. `openssl rand -hex 32`)

3. **Deploy**
   - Railway will detect the `Dockerfile` and build automatically
   - Your app will be live at the generated URL

## Environment Variables

| Variable      | Required | Description                                      |
|---------------|----------|--------------------------------------------------|
| `DATABASE_URL`| Yes      | Supabase PostgreSQL connection string            |
| `SECRET_KEY`  | Yes      | Flask secret key for sessions                    |
| `PORT`        | No       | Set by Railway automatically                     |

Optional (for contact form email):
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `RECIPIENT_EMAIL`

**Local setup:** Copy `.env.example` to `.env` and fill in values.  
**Railway:** Add variables in project → Variables tab. See [SUPABASE_RAILWAY_SETUP.md](SUPABASE_RAILWAY_SETUP.md) for details.

## Database Setup

Ensure your Supabase project has the tables. On first deploy, `init_db()` runs via gunicorn startup and creates:
- `feedback`, `contacts`, `orders`, `order_status_log`

## Custom Domain

In Railway: Service → **Settings** → **Domains** → Add your domain.
