# Deploy to Streamlit Cloud

## Step 1: Push to GitHub

Push your project to GitHub:
```bash
git add .
git commit -m "Convert Flask app to Streamlit"
git push origin main
```

## Step 2: Deploy to Streamlit Cloud

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Click "New app"
3. Select your GitHub repository: `d:\BCCA` (or your repo name)
4. Select branch: `main`
5. **Main file path**: `streamlit_app.py`
6. Click "Deploy"

## Step 3: Environment Variables (Optional)

If you need to set environment variables in Streamlit Cloud:
1. Click "⋯" → "Settings"
2. Go to "Secrets"
3. Add any environment variables (e.g., `SECRET_KEY`)

---

## Local Testing

Test the Streamlit app locally before deploying:

```bash
pip install -r requirements-streamlit.txt
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

---

## What Changed

✅ **Converted from Flask to Streamlit**
- Single-page app (all pages in one `streamlit_app.py`)
- Sidebar navigation for Home, Dashboard, Predict, About
- Multi-language support (English, Hindi, Telugu) via language selector
- Interactive charts using Plotly
- Real-time predictions

✅ **Files Created**
- `streamlit_app.py` - Main Streamlit application
- `requirements-streamlit.txt` - Lightweight dependencies

✅ **Features Preserved**
- 🤖 Random Forest ML predictions
- 📊 Interactive dashboard with Plotly charts
- 🌍 Multi-language UI
- 🔮 Churn probability predictions
- ℹ️ About page with feature descriptions

---

## Files to Delete (Optional)

These are no longer needed for Streamlit:
- `Dockerfile`
- `Procfile`
- `vercel.json`
- `runtime.txt`
- `requirements-deploy.txt`
- `app/app.py` (Flask app - optional to keep for reference)
- `app/static/` (no longer used)
- `app/templates/` (no longer used)

---

## Troubleshooting

**Q: Model training takes too long?**
A: Streamlit Cloud may timeout during first deployment. The model trains on first run and is cached afterwards.

**Q: Language selector not working?**
A: Clear browser cache or use incognito mode. Language is stored in Streamlit's session state.

**Q: Charts not displaying?**
A: Make sure `plotly>=5.17.0` is installed.

---

## Next Steps

After successful deployment:
1. Share your Streamlit Cloud URL with stakeholders
2. Monitor app traffic in Streamlit Cloud dashboard
3. Update model/add features as needed

**Your Streamlit app is now ready! 🚀**
