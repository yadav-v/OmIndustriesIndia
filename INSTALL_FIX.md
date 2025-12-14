# Installation Fix Guide

## Quick Fix: Install Dependencies Step by Step

### Step 1: Install python-dotenv (Required)

```bash
pip install python-dotenv
```

This is needed for reading the `.env` file. After this, your app should run (using SQLite).

### Step 2: Install psycopg2-binary (For Supabase - Optional)

If you want to use Supabase, you need `psycopg2-binary`. Try these methods:

#### Method 1: Install without version pinning
```bash
pip install psycopg2-binary
```

#### Method 2: Upgrade pip first, then install
```bash
python -m pip install --upgrade pip
pip install psycopg2-binary
```

#### Method 3: Install from wheel directly
```bash
pip install --only-binary :all: psycopg2-binary
```

#### Method 4: Use pre-built wheel for your Python version
```bash
# For Python 3.11
pip install psycopg2-binary --prefer-binary

# Or try latest version
pip install psycopg2-binary --upgrade
```

### Step 3: Install All Other Dependencies

```bash
pip install Flask==3.0.0 Werkzeug==3.0.1 gunicorn==21.2.0
```

---

## Alternative: Use SQLite Only (No Supabase)

If you're having trouble with `psycopg2-binary`, you can:

1. **Just install python-dotenv:**
   ```bash
   pip install python-dotenv
   ```

2. **Don't create a `.env` file** (or don't add `DATABASE_URL`)

3. **Run your app** - it will use SQLite automatically:
   ```bash
   py app.py
   ```

The app will work perfectly with SQLite! You can add Supabase later when you fix the psycopg2 installation.

---

## Why psycopg2-binary Might Fail

The error happens because:
- Your Python version might not have a pre-built wheel available
- pip is trying to build from source (needs PostgreSQL development libraries)
- Windows sometimes has compatibility issues

**Solution**: The app works fine without it if you use SQLite!

---

## Recommended Approach

1. **Install python-dotenv first:**
   ```bash
   pip install python-dotenv
   ```

2. **Run your app** (it will use SQLite):
   ```bash
   py app.py
   ```

3. **Later, when you want Supabase**, try installing psycopg2-binary using Method 1 or 2 above.

---

## Verify Installation

After installing python-dotenv, test:
```bash
py app.py
```

You should see:
```
✅ Database initialized with SQLite (local file: database.db)
 * Running on http://0.0.0.0:5000
```

Your app is working! 🎉

