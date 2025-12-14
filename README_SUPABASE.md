# Quick Start: Using Supabase

Your app is now configured to use Supabase! Follow these simple steps:

## 🚀 Setup Steps

### 1. Get Your Supabase Connection String

1. Go to https://app.supabase.com
2. Select your project
3. Go to **Settings** → **Database**
4. Scroll to **"Connection string"** section
5. Copy the **URI** (it looks like: `postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres`)
6. **Important**: Note your database password (you'll need it)

### 2. Create .env File

Create a file named `.env` in your project root (same folder as `app.py`):

**Windows:**
```powershell
# In PowerShell, navigate to your project folder
cd C:\vanshita\omindustry\omIndustries

# Create .env file (you can use Notepad or any text editor)
notepad .env
```

**Add this content to .env:**
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD_HERE@db.xxxxx.supabase.co:5432/postgres
SECRET_KEY=your-secret-key-change-this
```

**Replace:**
- `YOUR_PASSWORD_HERE` with your actual Supabase database password
- `db.xxxxx.supabase.co` with your actual Supabase host
- Keep everything else the same

**Example:**
```env
DATABASE_URL=postgresql://postgres:MyPassword123@db.abcdefghijk.supabase.co:5432/postgres
SECRET_KEY=super-secret-key-12345
```

### 3. Install Dependencies

Open terminal/command prompt in your project folder and run:

```bash
pip install -r requirements.txt
```

### 4. Test Connection (Optional)

Test your Supabase connection:

```bash
python setup_supabase.py
```

You should see:
```
✅ Successfully connected to Supabase!
✅ Tables created successfully!
🎉 Everything is set up correctly!
```

### 5. Run Your App

```bash
python app.py
```

You should see:
```
✅ Connected to Supabase (PostgreSQL)
✅ Database initialized with Supabase (PostgreSQL - online)
 * Running on http://0.0.0.0:5000
```

## ✅ Verify It's Working

1. Open http://localhost:5000
2. Submit a contact form or feedback
3. Go to Supabase dashboard → **Table Editor**
4. You should see your data in `contacts` or `feedback` tables!

## 🔧 Troubleshooting

### "DATABASE_URL not found"
- Make sure `.env` file is in the same folder as `app.py`
- Make sure the file is named exactly `.env` (not `.env.txt`)

### "Connection refused" or "could not connect"
- Check your `DATABASE_URL` is correct
- Make sure password doesn't have extra spaces
- Verify Supabase project is active (not paused)

### "psycopg2 not installed"
```bash
pip install psycopg2-binary
```

### Still using SQLite?
- Check `.env` file exists and has `DATABASE_URL=...`
- Make sure no `#` in front of `DATABASE_URL` (that comments it out)
- Restart your app after creating `.env` file

## 📝 Notes

- Your old `database.db` file will no longer be used
- All data now goes to Supabase (online)
- You can access your data from anywhere
- Perfect for deploying to cloud platforms!

## 📚 More Help

See `SUPABASE_SETUP.md` for detailed instructions.

