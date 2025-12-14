# Database Migration Guide: SQLite to Online Database

## Current Setup (SQLite - Local File)

**How it works:**
- SQLite is a file-based database stored locally on your computer
- The file `database.db` is created in your project root directory
- When you run `app.py`, the `init_db()` function creates the database file if it doesn't exist
- All data is stored in this single file on your local machine

**Location:** `C:\vanshita\omindustry\omIndustries\database.db`

**Limitations:**
- Only accessible from the machine where the file is located
- Not suitable for production deployments (Heroku, Railway, etc.)
- Can't be shared across multiple servers
- File can get corrupted if multiple processes access it simultaneously

---

## Free Online Database Options

### 1. **Supabase (PostgreSQL)** - RECOMMENDED ⭐
- **Free tier:** 500MB database, unlimited API requests
- **URL:** https://supabase.com
- **Pros:** Easy setup, includes dashboard, auto-backups, real-time features
- **Best for:** Production apps, easy migration

### 2. **ElephantSQL (PostgreSQL)**
- **Free tier:** 20MB database
- **URL:** https://www.elephantsql.com
- **Pros:** Simple, reliable, good for small projects
- **Best for:** Small to medium projects

### 3. **Railway (PostgreSQL)**
- **Free tier:** $5 credit/month (usually enough for small projects)
- **URL:** https://railway.app
- **Pros:** Easy deployment, good documentation
- **Best for:** Full-stack deployments

### 4. **Render (PostgreSQL)**
- **Free tier:** 90 days free, then $7/month
- **URL:** https://render.com
- **Pros:** Reliable, good for production
- **Best for:** Long-term projects

### 5. **MongoDB Atlas (NoSQL)**
- **Free tier:** 512MB storage
- **URL:** https://www.mongodb.com/cloud/atlas
- **Pros:** Flexible schema, good for document storage
- **Note:** Requires code changes (different database type)

---

## Migration Steps (Using Supabase as Example)

### Step 1: Create Supabase Account
1. Go to https://supabase.com
2. Sign up for free account
3. Create a new project
4. Wait for project to initialize (2-3 minutes)

### Step 2: Get Database Connection String
1. In Supabase dashboard, go to **Settings** → **Database**
2. Find **Connection string** section
3. Copy the **URI** connection string (looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`)

### Step 3: Set Environment Variable
Create a `.env` file in your project root:
```
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

### Step 4: Update Code
The updated `app.py` will automatically use PostgreSQL if `DATABASE_URL` is set, otherwise fall back to SQLite.

### Step 5: Run Migration
The app will automatically create tables when you first run it with PostgreSQL.

---

## Benefits of Online Database

✅ **Accessible from anywhere** - Your app can run on any server
✅ **Backups included** - Most services provide automatic backups
✅ **Scalable** - Can handle more traffic and data
✅ **Production-ready** - Suitable for deploying to Heroku, Railway, etc.
✅ **Multiple connections** - Multiple app instances can connect simultaneously
✅ **No file management** - No need to worry about database file location

---

## Security Note

⚠️ **Never commit your `.env` file or database credentials to Git!**

Make sure `.env` is in your `.gitignore` file.

