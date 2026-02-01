# Supabase Connection Fix Guide

## The Error

```
psycopg2.OperationalError: could not translate host name "db.xxxxx.supabase.co" to address
```

This error usually means:
- DNS resolution issue (can't find the hostname)
- Wrong connection string format
- Network/firewall blocking the connection

## Solution: Use Session Pooler Connection String

Supabase offers different connection types. For Flask apps, **Session Pooler** is recommended!

### Step 1: Get Session Pooler Connection String

1. Go to your Supabase project: https://app.supabase.com
2. Select your project
3. Go to **Settings** → **Database**
4. Scroll to **"Connection string"** section
5. **Select "Session pooler"** tab (not "URI" or "Direct connection")
6. Copy the connection string

It should look like:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:6543/postgres?pgbouncer=true
```

**Key differences:**
- Port is **6543** (not 5432)
- May include `?pgbouncer=true` parameter

### Step 2: Update Your .env File

Update your `.env` file with the Session Pooler connection string:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:6543/postgres?pgbouncer=true
```

**Important:** Replace `YOUR_PASSWORD` with your actual database password!

### Step 3: Test Connection

Run your app:
```bash
py app.py
```

You should see:
```
🔌 Connecting to Supabase (Session Pooler)...
   Host: db.xxxxx.supabase.co
   Port: 6543
✅ Connected to Supabase (PostgreSQL) via Session Pooler
```

## Alternative: Try Direct Connection

If Session Pooler doesn't work, try Direct connection:

1. In Supabase dashboard, go to **Settings** → **Database**
2. Select **"URI"** tab (Direct connection)
3. Copy the connection string (port should be 5432)
4. Update your `.env` file

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres
```

## Connection Types Comparison

| Type | Port | Best For | Connection Limit |
|------|------|----------|------------------|
| **Session Pooler** | 6543 | Serverless, Flask apps | Better for many connections |
| **Direct Connection** | 5432 | Direct database access | Lower connection limit |

**Recommendation:** Use **Session Pooler** for Flask apps!

## Common Issues

### Issue 1: "could not translate host name"
- ✅ Use Session Pooler connection string (port 6543)
- ✅ Check hostname is correct (should end with `.supabase.co`)
- ✅ Verify your Supabase project is active

### Issue 2: "password authentication failed"
- ✅ Make sure password in connection string is correct
- ✅ Try resetting your database password in Supabase dashboard
- ✅ Check for special characters - they might need URL encoding

### Issue 3: "connection refused"
- ✅ Check your internet connection
- ✅ Verify Supabase project is not paused
- ✅ Try the other connection type (Session Pooler ↔ Direct)

### Issue 4: Still getting errors
1. **Double-check your .env file:**
   - File is named exactly `.env` (not `.env.txt`)
   - `DATABASE_URL` line doesn't have `#` in front
   - No extra spaces around `=`

2. **Verify connection string format:**
   ```
   postgresql://username:password@host:port/database
   ```

3. **Test with setup script:**
   ```bash
   python setup_supabase.py
   ```

## Quick Checklist

- [ ] Using Session Pooler connection string (port 6543)
- [ ] `.env` file exists in project root
- [ ] `DATABASE_URL` is correct (no typos)
- [ ] Password is correct (no extra spaces)
- [ ] Supabase project is active
- [ ] Internet connection is working

## Still Having Issues?

1. **Verify Supabase project status:**
   - Go to Supabase dashboard
   - Check if project shows as "Active"
   - If paused, resume it

2. **Try resetting database password:**
   - Settings → Database → Reset database password
   - Update `.env` with new password

3. **Use test script:**
   ```bash
   python setup_supabase.py
   ```
   This will test the connection and show detailed error messages.

4. **Check network/firewall:**
   - Make sure your firewall isn't blocking port 6543 or 5432
   - Try from a different network

---

## Example .env File

```env
# Supabase Session Pooler (Recommended)
DATABASE_URL=postgresql://postgres:MySecurePassword123@db.abcdefghijk.supabase.co:6543/postgres?pgbouncer=true

# Or Direct Connection (Alternative)
# DATABASE_URL=postgresql://postgres:MySecurePassword123@db.abcdefghijk.supabase.co:5432/postgres

SECRET_KEY=your-secret-key-here
```

**Remember:** Only use ONE `DATABASE_URL` line (not both)!

---

## Railway: .env Does NOT Work

**Important:** When deployed on Railway, the `.env` file is **not used** (it's gitignored and not deployed).

You must add variables in Railway dashboard:
1. Project → Your service → **Variables**
2. Add `DATABASE_URL` and `SECRET_KEY` with your values

Local = uses `.env` | Railway = uses Variables in dashboard

---

## Test Connection Locally

Run: `python check_env.py` — verifies .env is loaded and Supabase connection works.

