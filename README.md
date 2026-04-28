# AI Admission Bot

This repository contains a Streamlit app for an AI-powered admission counselor.

## Deployment Options

### 1. Streamlit Community Cloud (recommended)
1. Create a GitHub repository and push this project.
2. Go to https://streamlit.io/cloud and sign in with GitHub.
3. Click **New app**.
4. Select your GitHub repo, branch, and set the main file to `app.py`.
5. Deploy the app.

#### Streamlit Cloud settings
- Add secrets via the app settings for `OPENAI_API_KEY`, `MONGO_URI`, `DB_NAME`, `DEFAULT_ADMIN_USER`, and `DEFAULT_ADMIN_PASS`.
- If you do not set `OPENAI_API_KEY`, the app will fall back to static FAQ-style responses.

### 2. Self-hosted deployment
Run locally or on your own server with:

```bash
python -m streamlit run app.py
```

## Required Files
- `app.py`
- `requirements.txt`
- `chatbot.py`
- `auth.py`
- `db.py`
- `.streamlit/config.toml`

## Notes
- Streamlit Community Cloud supports unlimited public apps for personal/hobby use.
- For private apps or enterprise usage, use Streamlit for Teams or a custom deployment.
