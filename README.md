# ⚔️ Decision Duel

An AI debate arena for your life decisions, powered by **Google Gemini** and **Streamlit**.

You enter a dilemma. **The Optimist** argues for it, **The Skeptic** argues against it, and **The Judge** gives a verdict, a confidence score and a 7-day action plan.

## Features
- Multi-step LLM chain (3 personas)
- Structured JSON output from Gemini
- Tone selector (Serious / Funny / Brutally honest)
- Choose between Gemini models

## Run locally
```bash
git clone https://github.com/<your-username>/decision-duel.git
cd decision-duel
pip install -r requirements.txt
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then add your key
streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push this repo to GitHub (never commit your API key).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, pick this repo, branch `main`, main file `app.py`.
4. Open **Advanced settings → Secrets** and paste:
   ```toml
   GEMINI_API_KEY = "your-key-here"
   ```
5. Click **Deploy**.

## Tech stack
Python, Streamlit, google-genai (Gemini API)
