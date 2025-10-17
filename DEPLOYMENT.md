# Deployment Guide for TraderBlockAI

## 🚀 Backend Deployment (Render)

### Step 1: Prepare Backend for Render

1. **Create a Render account** at [render.com](https://render.com)

2. **Connect your GitHub repository** to Render

3. **Create a new Web Service**:
   - **Name**: `traderblockai-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

4. **Environment Variables** (optional):
   ```
   PYTHON_VERSION=3.11
   ```

5. **Deploy**: Click "Create Web Service" and wait for deployment

6. **Get your backend URL**: Copy the URL (e.g., `https://traderblockai-backend.onrender.com`)

### Step 2: Test Backend API

```bash
curl https://your-backend-url.onrender.com/api/v1/analyze/AAPL
```

## 🌐 Frontend Deployment (Vercel)

### Step 1: Prepare Frontend for Vercel

1. **Create a Vercel account** at [vercel.com](https://vercel.com)

2. **Connect your GitHub repository** to Vercel

3. **Configure the project**:
   - **Framework Preset**: `Next.js`
   - **Root Directory**: `traderblockai-app`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)

4. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
   ```

5. **Deploy**: Click "Deploy" and wait for deployment

### Step 2: Update Frontend Code

In `traderblockai-app/app/page.tsx`, uncomment the real API call:

```typescript
// Replace the mock response section with:
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/analyze/${ticker}`)
if (!response.ok) {
  throw new Error(`Failed to analyze ${ticker}`)
}
const data = await response.json()
setAnalysisData(data)
```

## 🔧 Alternative Deployment Options

### Option 1: Docker Deployment

1. **Backend on any Docker host**:
   ```bash
   cd backend
   docker build -t traderblockai-backend .
   docker run -p 8000:8000 traderblockai-backend
   ```

2. **Frontend on any Docker host**:
   ```bash
   cd traderblockai-app
   docker build -t traderblockai-frontend .
   docker run -p 3000:3000 traderblockai-frontend
   ```

### Option 2: Railway Deployment

1. **Backend**: Connect GitHub repo, select `backend` folder
2. **Frontend**: Connect GitHub repo, select `traderblockai-app` folder

### Option 3: DigitalOcean App Platform

1. **Create App**: Connect GitHub repository
2. **Backend Service**: Python service, root directory `backend`
3. **Frontend Service**: Static site, root directory `traderblockai-app`

## 🔒 Security Considerations

### Production Checklist

- [ ] Update CORS settings in backend for production domains
- [ ] Set up proper environment variables
- [ ] Configure rate limiting for API endpoints
- [ ] Add input validation and sanitization
- [ ] Set up monitoring and logging
- [ ] Configure SSL certificates
- [ ] Review and update legal disclaimers

### Backend Security Updates

In `backend/main.py`, update CORS for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.vercel.app"],  # Your Vercel URL
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

## 📊 Monitoring and Maintenance

### Health Checks

1. **Backend Health**: `GET https://your-backend-url.onrender.com/`
2. **Frontend Health**: Visit your Vercel URL

### Logs and Debugging

1. **Render Logs**: Available in Render dashboard
2. **Vercel Logs**: Available in Vercel dashboard
3. **Local Debugging**: Use `docker-compose up` for full stack

### Performance Optimization

1. **Backend**: 
   - Add caching for API responses
   - Implement connection pooling
   - Add request rate limiting

2. **Frontend**:
   - Implement client-side caching
   - Add loading states
   - Optimize bundle size

## 🚨 Important Notes

1. **Free Tier Limitations**: 
   - Render free tier spins down after inactivity
   - Vercel has bandwidth limits
   - Consider upgrading for production use

2. **API Rate Limits**: 
   - Yahoo Finance API has rate limits
   - Consider implementing caching
   - Monitor usage patterns

3. **Legal Compliance**: 
   - Ensure disclaimers remain prominent
   - Review terms of service
   - Consider adding privacy policy

## 🔄 Updates and Maintenance

### Backend Updates
```bash
# Update dependencies
pip install -r requirements.txt --upgrade

# Test locally
python main.py

# Deploy to Render (automatic if connected to GitHub)
```

### Frontend Updates
```bash
# Update dependencies
npm update

# Test locally
npm run dev

# Deploy to Vercel (automatic if connected to GitHub)
```

## 📞 Support

For deployment issues:
1. Check Render/Vercel documentation
2. Review application logs
3. Test locally with `docker-compose up`
4. Verify environment variables are set correctly

Remember: This application is for educational purposes only and should not be considered as financial advice.
