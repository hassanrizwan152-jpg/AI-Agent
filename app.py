import json
import os

import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Decision Duel", page_icon="⚔️", layout="wide")

# ---------- API key handling ----------
def get_api_key():
    try:
        if "GEMINI_API_KEY" in st.secrets:
            return st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass
    return os.getenv("GEMINI_API_KEY", "")


with st.sidebar:
    st.header("⚙️ Settings")
    api_key = get_api_key() or st.text_input("Gemini API Key", type="password")
    model_name = st.selectbox(
        "Gemini model",
        ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.5-pro"],
    )
    tone = st.radio("Debate tone", ["Serious", "Funny", "Brutally honest"])
    st.caption("Get a free key at aistudio.google.com")

# ---------- Gemini helper ----------
def ask(client, system, prompt, as_json=False):
    config = types.GenerateContentConfig(
        system_instruction=system,
        temperature=0.9,
        response_mime_type="application/json" if as_json else "text/plain",
    )
    resp = client.models.generate_content(
        model=model_name, contents=prompt, config=config
    )
    return resp.text


OPTIMIST = (
    "You are The Optimist in a debate. Argue strongly FOR the user's decision "
    "with 3 sharp, concrete points. Max 150 words. Tone: {tone}."
)
SKEPTIC = (
    "You are The Skeptic in a debate. Argue strongly AGAINST the user's decision "
    "with 3 sharp, concrete risks. Max 150 words. Tone: {tone}."
)
JUDGE = (
    "You are The Judge. Read both arguments and decide fairly. Tone: {tone}. "
    "Return ONLY JSON with keys: verdict (string, 2-3 sentences), "
    "confidence (integer 0-100 that the decision is a good idea), "
    "winner (\"Optimist\" or \"Skeptic\"), "
    "action_plan (list of exactly 7 short strings, one per day)."
)

# ---------- UI ----------
st.title("⚔️ Decision Duel")
st.write("Type a dilemma. Two AIs fight about it. A judge decides.")

decision = st.text_area(
    "What are you trying to decide?",
    placeholder="Should I quit my job to build a startup?",
    height=100,
)
context = st.text_input("Any extra context? (optional)", placeholder="I have 6 months of savings")

if st.button("Start the duel 🥊", type="primary"):
    if not api_key:
        st.error("Add your Gemini API key in the sidebar or secrets.")
        st.stop()
    if not decision.strip():
        st.warning("Write a decision first.")
        st.stop()

    client = genai.Client(api_key=api_key)
    prompt = f"Decision: {decision}\nContext: {context or 'none'}"

    try:
        col1, col2 = st.columns(2)
        with st.spinner("The debaters are warming up..."):
            pro = ask(client, OPTIMIST.format(tone=tone), prompt)
            con = ask(client, SKEPTIC.format(tone=tone), prompt)
        with col1:
            st.subheader("😇 The Optimist")
            st.info(pro)
        with col2:
            st.subheader("😈 The Skeptic")
            st.error(con)

        with st.spinner("The Judge is deliberating..."):
            raw = ask(
                client,
                JUDGE.format(tone=tone),
                f"{prompt}\n\nOPTIMIST SAID:\n{pro}\n\nSKEPTIC SAID:\n{con}",
                as_json=True,
            )
            result = json.loads(raw)

        st.divider()
        st.subheader("⚖️ The Judge's Verdict")
        st.success(f"Winner: **{result['winner']}**")
        st.write(result["verdict"])
        st.progress(int(result["confidence"]) / 100, text=f"Confidence it's a good idea: {result['confidence']}%")

        st.subheader("📅 Your 7-Day Action Plan")
        for i, step in enumerate(result["action_plan"], 1):
            st.checkbox(f"Day {i}: {step}", key=f"day{i}")

    except Exception as e:
        st.error(f"Something went wrong: {e}")
