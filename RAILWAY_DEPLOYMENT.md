# Railway Deployment Guide

## Prerequisites
1. Create a [Railway account](https://railway.app/)
2. Install Railway CLI (optional): `npm i -g @railway/cli`

## Deployment Steps

### 1. Push Your Code to GitHub
```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### 2. Deploy on Railway

#### Option A: Using Railway Dashboard (Easiest)

1. Go to [Railway.app](https://railway.app/) and log in
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `Personal-Finance-AI` repository
5. Railway will detect your Django app automatically

#### Option B: Using Railway CLI
```bash
# Login to Railway
railway login

# Initialize project
cd backend
railway init

# Deploy
railway up
```

### 3. Add PostgreSQL Database

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically create a `DATABASE_URL` environment variable

### 4. Configure Environment Variables

In Railway dashboard, go to your service → **Variables** tab and add:

```
DJANGO_SETTINGS_MODULE=config.settings.railway
SECRET_KEY=your-super-secret-key-here-generate-a-new-one
GEMINI_API_KEY=your-gemini-api-key
DEBUG=False
FRONTEND_URL=https://your-frontend-url.vercel.app
```

**To generate a new SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Deploy and Migrate

Railway will automatically:
- Install dependencies from `requirements.txt`
- Run migrations (configured in `railway.json`)
- Start the server with Gunicorn

### 6. Get Your Backend URL

After deployment, Railway will provide a URL like:
```
https://your-app-name.up.railway.app
```

### 7. Update Frontend Configuration

Update your frontend's API configuration to use the Railway URL:
```javascript
// In frontend/src/utils/api.js
const API_BASE_URL = 'https://your-app-name.up.railway.app';
```

### 8. Update CORS Settings

Add your frontend URL to the environment variables:
```
FRONTEND_URL=https://your-frontend-domain.vercel.app
```

## Important Files Created

- **`Procfile`**: Tells Railway how to run your app
- **`runtime.txt`**: Specifies Python version
- **`railway.json`**: Railway-specific configuration
- **`config/settings/railway.py`**: Production settings for Railway

## Monitoring Your App

- **Logs**: View in Railway dashboard under "Deployments" → "View Logs"
- **Metrics**: CPU, Memory, Network usage available in dashboard
- **Restart**: Click "Restart" if needed

## Troubleshooting

### Database Connection Issues
Make sure `DATABASE_URL` is set automatically by Railway's PostgreSQL service.

### Static Files Not Loading
Run manually if needed:
```bash
railway run python manage.py collectstatic --noinput
```

### Environment Variables Not Working
Ensure `DJANGO_SETTINGS_MODULE=config.settings.railway` is set.

### Migration Errors
Run migrations manually:
```bash
railway run python manage.py migrate
```

## Free Tier Limits

Railway free tier includes:
- $5 of usage per month
- Typically enough for small projects
- Upgrade to Pro ($20/month) for unlimited usage

## Next Steps

1. Deploy frontend to Vercel
2. Update frontend API URL to point to Railway backend
3. Test the full application
4. Monitor usage in Railway dashboard

---

**Your backend is now ready to deploy to Railway! 🚀**
