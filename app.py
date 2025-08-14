import streamlit as st
from fact_checker_bot.src.fact_checker import fact_check_claim

# --- Page Config ---
st.set_page_config(page_title="AI Fact Checker Bot", page_icon="🕵️‍♂️", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
        .main {
            background-color: #f7f9fc;
        }
        .stButton>button {
            background-color: #4B9CD3;
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 8px 20px;
        }
        .stButton>button:hover {
            background-color: #3178A9;
            color: white;
        }
        .fact-card {
            background-color: white;
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
            color: black; /* ✅ Ensures black text */
        }
        .verdict {
            font-size: 18px;
            font-weight: bold;
        }
        /* ✅ Force black text in success/info/warning boxes */
        .stAlert p {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown("<h1 style='text-align:center;'>🕵️‍♂️ AI Fact Checker Bot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Enter a claim below and let AI verify it with real evidence 📚</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Session state ---
if "result" not in st.session_state:
    st.session_state.result = None
if "claim" not in st.session_state:
    st.session_state.claim = ""

# --- Input Area ---
col1, col2 = st.columns([3, 1])
with col1:
    claim = st.text_input("✍️ **Enter a claim to fact-check:**", value=st.session_state.claim)
with col2:
    st.write("")  # space
    if st.button("🔍 Fact Check", use_container_width=True):
        if claim.strip():
            with st.spinner("🔎 Analyzing and verifying your claim..."):
                st.session_state.result = fact_check_claim(claim)
                st.session_state.claim = claim
        else:
            st.warning("⚠️ Please enter a claim first.")

if st.button("❌ Clear Session", use_container_width=True):
    st.session_state.result = None
    st.session_state.claim = ""
    st.success("✅ Session cleared. Start fresh!")

# --- Verdict Badge ---
def verdict_badge(verdict):
    verdict = verdict.lower().strip()
    if verdict == "true":
        return "✅ **True**"
    elif verdict == "false":
        return "❌ **False**"
    else:
        return "⚠️ **Uncertain**"

# --- Results Display ---
if st.session_state.result:
    result = st.session_state.result
    
    st.markdown("### 📜 Fact-Check Report")
    st.markdown(f"<div class='fact-card'><b>Claim:</b> {result['claim']}<br><b>Initial Answer:</b> {result['initial_answer']}</div>", unsafe_allow_html=True)

    st.markdown("### 🔍 Assumptions & Verification")
    if result['assumptions']:
        for r in result['assumptions']:
            with st.expander(f"📌 Assumption: {r['assumption']}"):
                st.markdown(f"<p class='verdict'>Verdict: {verdict_badge(r['verdict'])}</p>", unsafe_allow_html=True)
                st.markdown(f"**Explanation:** {r['explanation']}")
                if r.get("evidence_links"):
                    st.markdown("**📂 Evidence Links:**")
                    for link in r["evidence_links"]:
                        st.markdown(f"- [{link}]({link})")
    else:
        st.warning("No assumptions extracted for this claim.")

    st.markdown("### ✅ Final Answer")
    st.success(result['final_answer'])
