# Supabase Setup Guide

## Step 1: Get Your Supabase Connection String

1. **Go to your Supabase project dashboard**: https://app.supabase.com
2. **Select your project** (the one you just created)
3. **Go to Settings** (gear icon in the left sidebar)
4. **Click on "Database"** in the settings menu
5. **Scroll down to "Connection string"** section
6. **Copy the "URI" connection string** (not the other connection strings)

The connection string will look like:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres
```

**Important**: Replace `[YOUR-PASSWORD]` with your actual database password!

### How to get your database password:

1. In the same "Database" settings page
2. Look for **"Database password"** section
3. If you don't remember it, you can **reset it** (click "Reset database password")
4. Copy the password (you'll need it for the connection string)

---

## Step 2: Create .env File

1. **Create a file named `.env`** in your project root directory:
   ```
   C:\vanshita\omindustry\omIndustries\.env
   ```

2. **Add your Supabase connection string** to the `.env` file:
   ```env
   DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.xxxxx.supabase.co:5432/postgres
   SECRET_KEY=your-secret-key-change-this-in-production
   ```

   **Example** (replace with your actual values):
   ```env
   DATABASE_URL=postgresql://postgres:MySecurePassword123@db.abcdefghijk.supabase.co:5432/postgres
   SECRET_KEY=super-secret-key-12345
   ```

3. **Save the file**

---

## Step 3: Install Dependencies

Open your terminal/command prompt in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- `psycopg2-binary` (PostgreSQL driver)
- `python-dotenv` (for reading .env file)
- Other Flask dependencies

---

## Step 4: Run Your App

```bash
python app.py
```

You should see:
```
✅ Database initialized with PostgreSQL (online)
 * Running on http://0.0.0.0:5000
```

If you see this, **congratulations!** Your app is now using Supabase! 🎉

---

## Step 5: Verify It's Working

1. **Visit your app**: http://localhost:5000
2. **Submit a contact form** or **feedback**
3. **Check Supabase dashboard**:
   - Go to **Table Editor** in Supabase
   - You should see `contacts` and `feedback` tables
   - Your data should appear there!

---

## Troubleshooting

### Error: "psycopg2 not installed"
```bash
pip install psycopg2-binary
```

### Error: "Connection refused" or "could not connect"
- ✅ Check your `DATABASE_URL` is correct in `.env` file
- ✅ Make sure you replaced `[YOUR-PASSWORD]` with actual password
- ✅ Verify your Supabase project is active (not paused)
- ✅ Check if your IP needs to be whitelisted (usually not needed for Supabase)

### Error: "password authentication failed"
- ✅ Make sure your database password is correct
- ✅ Try resetting your database password in Supabase dashboard
- ✅ Make sure there are no extra spaces in your `.env` file

### Error: "relation does not exist"
- ✅ This is normal on first run - the tables will be created automatically
- ✅ Run `python app.py` again - it should create the tables

### Still using SQLite?
- ✅ Make sure `.env` file is in the project root (same folder as `app.py`)
- ✅ Make sure `DATABASE_URL` line doesn't have `#` in front (that comments it out)
- ✅ Make sure there are no spaces around the `=` sign: `DATABASE_URL=...` not `DATABASE_URL = ...`

---

## What Happens Next?

Once set up:
- ✅ All new data goes to Supabase (online)
- ✅ Your old `database.db` file is no longer used
- ✅ You can access your data from anywhere
- ✅ Perfect for deploying to cloud platforms!

---

## Need Help?

If you're stuck, check:
1. `.env` file exists and has correct `DATABASE_URL`
2. Password in connection string matches Supabase dashboard
3. All dependencies installed (`pip install -r requirements.txt`)
4. Supabase project is active (not paused)

