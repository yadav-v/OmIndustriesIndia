# Supabase Connection: Local + Railway

## Overview

| Environment | Database      | Where to set variables     |
|-------------|---------------|----------------------------|
| **Local**   | Supabase      | `.env` file in project     |
| **Railway** | Supabase      | Railway → Variables        |
| **Local**   | SQLite        | No DATABASE_URL (optional) |

---

## 1. Get Supabase connection string

1. Go to [Supabase Dashboard](https://app.supabase.com) → your project  
2. **Settings** → **Database**  
3. Scroll to **Connection string**  
4. Copy one of these:

**Session pooler** (recommended for Railway):
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:6543/postgres?pgbouncer=true
```

**Direct** (use if pooler has issues):
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

Replace `[YOUR-PASSWORD]` with your **Database password** (from Settings → Database → Database password).

---

## 2. Local development

### Step 1: Create `.env` file

```bash
# Windows
copy .env.example .env

# Linux / Mac
cp .env.example .env
```

### Step 2: Edit `.env` and add your values

```env
DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.xxxxx.supabase.co:6543/postgres?pgbouncer=true
SECRET_KEY=any-random-string-for-local
```

### Step 3: Run the app

```bash
pip install python-dotenv
python app.py
```

You should see: `Connected to Supabase (Session Pooler)...`

---

## 3. Railway deployment

### Step 1: Add variables in Railway

1. Open your project on [Railway](https://railway.app)  
2. Select your service  
3. Go to **Variables** tab  
4. Add:

| Variable      | Value                                                                 |
|---------------|-----------------------------------------------------------------------|
| `DATABASE_URL`| Your Supabase connection string (same as above)                       |
| `SECRET_KEY`  | Random secret: `python -c "import secrets; print(secrets.token_hex(32))"` |

### Step 2: Deploy

Railway uses these variables automatically. No `.env` file is needed on Railway.

---

## 4. Use SQLite locally (no Supabase)

To use a local SQLite file instead:

- **Do not** set `DATABASE_URL` in `.env`  
- Or remove the `DATABASE_URL` line  
- The app will use `database.db` in your project folder

---

## 5. Troubleshooting

| Issue | Fix |
|-------|-----|
| Connection timeout | Use Session pooler (port 6543) |
| Password has special chars | URL-encode them in DATABASE_URL |
| Railway can't connect | Confirm Supabase project is not paused |
| Local works, Railway fails | Use same connection string; check no typos |
