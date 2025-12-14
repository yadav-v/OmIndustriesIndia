# Quick Setup Guide: Using Online Database

## Option 1: Use Local SQLite (Current - No Changes Needed)
Your app currently works with SQLite. Just run:
```bash
pip install -r requirements.txt
python app.py
```
The database file `database.db` will be created automatically in your project folder.

---

## Option 2: Use Free Online PostgreSQL Database

### Step 1: Choose a Free Database Service

**Recommended: Supabase** (500MB free)
1. Go to https://supabase.com
2. Sign up (free)
3. Create a new project
4. Wait 2-3 minutes for setup

**Alternative: ElephantSQL** (20MB free)
1. Go to https://www.elephantsql.com
2. Sign up (free)
3. Create a new instance
4. Select "Tiny Turtle" (free plan)

### Step 2: Get Your Database Connection String

**For Supabase:**
1. Go to **Settings** → **Database**
2. Scroll to **Connection string**
3. Copy the **URI** (looks like: `postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres`)
4. Replace `[PASSWORD]` with your actual database password

**For ElephantSQL:**
1. Click on your instance
2. Copy the **URL** from the details page

### Step 3: Configure Your App

1. Create a `.env` file in your project root:
```bash
# Copy the example file
cp .env.example .env
```

2. Edit `.env` and add your database URL:
```
DATABASE_URL=postgresql://postgres:yourpassword@db.xxxxx.supabase.co:5432/postgres
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run your app:
```bash
python app.py
```

The app will automatically:
- ✅ Detect you're using PostgreSQL
- ✅ Create all necessary tables
- ✅ Work exactly the same as before!

---

## How It Works

- **If `DATABASE_URL` is set**: Uses PostgreSQL (online database)
- **If `DATABASE_URL` is NOT set**: Uses SQLite (local file database)

You can switch between them anytime by adding/removing the `DATABASE_URL` from your `.env` file!

---

## Troubleshooting

**Error: "psycopg2 not installed"**
```bash
pip install psycopg2-binary
```

**Error: "Connection refused"**
- Check your `DATABASE_URL` is correct
- Make sure your database service is running
- Check if your IP needs to be whitelisted (some services require this)

**Want to go back to SQLite?**
Just remove or comment out the `DATABASE_URL` line in your `.env` file.

