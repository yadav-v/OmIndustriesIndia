# 🚀 Start Here: Supabase Setup

Your code is **already configured** to use Supabase! You just need to add your connection string.

## Quick Setup (3 Steps)

### Step 1: Get Supabase Connection String

1. Go to https://app.supabase.com
2. Click on your project
3. Go to **Settings** (⚙️) → **Database**
4. Scroll to **"Connection string"**
5. Copy the **URI** connection string
6. **Note your database password** (you'll need it)

The connection string looks like:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

### Step 2: Create .env File

Create a file named `.env` in this folder (`C:\vanshita\omindustry\omIndustries\.env`)

**Add this (replace with your actual values):**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres
SECRET_KEY=your-secret-key-here
```

**Example:**
```env
DATABASE_URL=postgresql://postgres:MyPassword123@db.abcdefghijk.supabase.co:5432/postgres
SECRET_KEY=super-secret-key-12345
```

### Step 3: Install & Run

```bash
pip install -r requirements.txt
python app.py
```

You should see:
```
✅ Connected to Supabase (PostgreSQL)
✅ Database initialized with Supabase (PostgreSQL - online)
```

## ✅ Done!

Your app is now using Supabase! All data will be stored online.

## Need Help?

- **Detailed guide**: See `SUPABASE_SETUP.md`
- **Quick reference**: See `README_SUPABASE.md`
- **Test connection**: Run `python setup_supabase.py`

## What Changed?

✅ Code already supports Supabase (no code changes needed!)
✅ Just add your `DATABASE_URL` to `.env` file
✅ App automatically detects and uses Supabase
✅ All existing features work the same!

