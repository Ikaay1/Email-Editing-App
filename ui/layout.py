import streamlit as st

GEN_MODELS = ["gpt-4o-mini", "gpt-4.1"]

def sidebar_controls(email_ids):
    st.sidebar.title("⚙️ Controls")

    selected_id = st.sidebar.selectbox("📨 Email Record", email_ids)
    action = st.sidebar.radio("✏️ Action", ["Lengthen", "Shorten", "Tone"])

    tone = None
    if action == "Tone":
        tone = st.sidebar.selectbox(
            "🎭 Tone",
            ["Friendly", "Sympathetic", "Professional"]
        )

    st.sidebar.divider()
    gen_model = st.sidebar.selectbox("🧠 Generation Model", GEN_MODELS)

    return selected_id, action, tone, gen_model
