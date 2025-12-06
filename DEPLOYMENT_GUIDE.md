# Free Deployment Guide for Om Industries India Flask App

## 🚀 Best Free Hosting Options

### 1. **Render.com** (Recommended - Easiest)
**Free Tier:** 750 hours/month (enough for 24/7)
**Best for:** Beginners, easy setup

#### Steps:
1. **Create account** at [render.com](https://render.com)
2. **Prepare your code:**
   - Make sure `requirements.txt` exists ✅
   - Make sure `Procfile` exists ✅
   - Commit all files to Git

3. **Create new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Settings:
     - **Name:** om-industries-app
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Plan:** Free

4. **Add Environment Variables:**
   - Go to Environment tab
   - Add:
     ```
     SMTP_SERVER=smtp.gmail.com
     SMTP_PORT=587
     SMTP_USER=your-email@gmail.com
     SMTP_PASSWORD=your-app-password
     RECIPIENT_EMAIL=admin@omindustriesindia.com
     FLASK_ENV=production
     ```

5. **Deploy!** - Render will automatically deploy

**URL:** `https://om-industries-app.onrender.com`

---

### 2. **Railway.app** (Also Great)
**Free Tier:** $5 credit/month (usually enough for small apps)

#### Steps:
1. **Create account** at [railway.app](https://railway.app)
2. **New Project** → "Deploy from GitHub repo"
3. **Select your repository**
4. **Add Environment Variables** (same as Render)
5. **Deploy!**

**Note:** Railway auto-detects Flask apps

---

### 3. **PythonAnywhere** (Good for Learning)
**Free Tier:** Limited but works

#### Steps:
1. **Sign up** at [pythonanywhere.com](https://www.pythonanywhere.com)
2. **Upload files** via Files tab
3. **Create Web App:**
   - Go to Web tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Python 3.11
4. **Configure WSGI:**
   - Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - Add:
     ```python
     import sys
     path = '/home/yourusername/yourproject'
     if path not in sys.path:
         sys.path.append(path)
     
     from app import app as application
     ```
5. **Reload web app**

---

## 📋 Pre-Deployment Checklist

### 1. Update requirements.txt
Make sure it includes:
```
Flask==3.0.0
gunicorn==21.2.0
Werkzeug==3.0.1
```

### 2. Create Procfile (for Render/Railway)
```
web: gunicorn app:app
```

### 3. Update app.py for Production
Add at the bottom:
```python
if __name__ == "__main__":
    init_db()
    # For production, use gunicorn instead
    # app.run(debug=True)  # Only for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### 4. Database Considerations
- **SQLite works** for small apps on free tiers
- For production, consider PostgreSQL (Render/Railway offer free PostgreSQL)
- Current SQLite setup will work fine for now

### 5. Static Files
- Make sure `static/` folder is in your repository
- Flask serves static files automatically

### 6. Secret Key
Update in `app.py`:
```python
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
```

---

## 🔧 Quick Setup Commands

### For Render/Railway:
1. Install gunicorn locally (for testing):
   ```bash
   pip install gunicorn
   ```

2. Test locally:
   ```bash
   gunicorn app:app
   ```

3. Update requirements.txt:
   ```bash
   pip freeze > requirements.txt
   ```

### Git Setup (if not done):
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

---

## 🌐 Domain Setup (Optional)

### Free Custom Domain:
- **Render:** Add custom domain in settings (free SSL)
- **Railway:** Add custom domain in settings
- **Freenom:** Get free .tk/.ml domains (not recommended for production)

---

## 📧 Email Configuration

After deployment, set environment variables in your hosting platform:
- `SMTP_SERVER`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `RECIPIENT_EMAIL`

---

## 🐛 Common Issues

### Issue: App crashes on startup
**Solution:** Check logs, ensure all dependencies in requirements.txt

### Issue: Database errors
**Solution:** SQLite file might need write permissions, or switch to PostgreSQL

### Issue: Static files not loading
**Solution:** Ensure `static/` folder is in repository root

### Issue: 500 errors
**Solution:** Check application logs in hosting dashboard

---

## 🎯 Recommended: Render.com

**Why Render?**
- ✅ Easiest setup
- ✅ Free SSL certificate
- ✅ Automatic deployments from Git
- ✅ Free tier is generous
- ✅ Good documentation
- ✅ Environment variables easy to set

**Steps Summary:**
1. Push code to GitHub
2. Connect GitHub to Render
3. Add environment variables
4. Deploy!

**Your app will be live at:** `https://your-app-name.onrender.com`

---

## 📝 Notes

- **Free tiers have limitations:** May sleep after inactivity (Render), or have usage limits
- **Database:** SQLite works but consider PostgreSQL for production
- **Email:** Configure SMTP after deployment
- **Backups:** Regularly backup your database

---

## 🆘 Need Help?

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Flask Deployment: https://flask.palletsprojects.com/en/latest/deploying/

