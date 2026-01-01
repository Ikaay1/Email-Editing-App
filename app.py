import streamlit as st
import json

from services.email_service import EmailService
from ui.layout import sidebar_controls
from ui.theme import load_theme
from ui.animations import fade_container
from ui.components import judge_card
import hashlib
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Email Editor", page_icon="📧", layout="wide")
st.markdown(load_theme(), unsafe_allow_html=True)

JUDGE_MODELS = ["gpt-4o-mini", "gpt-4.1"]

# ---------------- LOAD DATA ----------------
emails = []
with open("./datasets/tone.jsonl", "r") as f:
    for line in f:
        emails.append(json.loads(line))

if not emails:
    st.error("Dataset is empty.")
    st.stop()

df = pd.DataFrame(emails)

preferred_cols = ["id", "sender", "subject", "content"]
df = df[[c for c in preferred_cols if c in df.columns]]

email_ids = [e["id"] for e in emails]

# ---------------- SIDEBAR ----------------
selected_id, action, tone, gen_model = sidebar_controls(email_ids)
selected_email = emails[selected_id - 1]

# ---------------- HEADER ----------------
st.title("📧 AI Email Editing Tool")
st.caption("Select an email record by ID and use AI to refine it.")

# ---------------- TABS ----------------
tab_original, tab_generated, tab_eval, tab_all = st.tabs(
    ["✉️ Original", "✍️ Generated", "📊 Evaluation", "📚 All Emails"]
)

# ---------------- ORIGINAL TAB ----------------
with tab_original:
    fade_container(lambda: st.markdown("### ✉️ Original Email"))

    st.markdown(f"**From:** {selected_email.get('sender', '—')}")
    st.markdown(f"**Subject:** {selected_email.get('subject', '—')}")

    email_text = st.text_area(
        "Email Content",
        selected_email.get("content", ""),
        height=280
    )

    def text_sig(t: str) -> str:
        return hashlib.md5(t.strip().encode("utf-8")).hexdigest()[:10]

    tone_key = (tone or "none").lower()
    action_key = action.lower()
    model_key = gen_model
    email_sig = text_sig(email_text)

    state_key = (
        f"gen__id={selected_id}"
        f"__a={action_key}"
        f"__t={tone_key}"
        f"__m={model_key}"
        f"__s={email_sig}"
    )

    col1, col2, col3 = st.columns([1, 2, 2])

    with col1:
        st.markdown(
            f"""
            <div class="meta-card">
                <div class="meta-label">Action</div>
                <div class="meta-value">✏️ {action}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="meta-card">
                <div class="meta-label">Model</div>
                <div class="meta-value">🧠 {gen_model}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        if action == "Tone":
            st.markdown(
                f"""
                <div class="meta-card">
                    <div class="meta-label">Tone</div>
                    <div class="meta-value">🎭 {tone}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


    if st.button("✍️ Generate", use_container_width=True):
        service = EmailService(gen_model)

        response = service.generate(
            action.lower(),
            email_text,
            tone.lower() if action == "Tone" else None
        )

        generated = response.choices[0].message.content

        # Save generated + original used for judging
        st.session_state[state_key] = {
            "original": email_text,
            "generated": generated
        }

        st.toast("Generated! Check the ✍️ Generated tab.", icon="✅")

# ---------------- GENERATED TAB ----------------
with tab_generated:
    if state_key not in st.session_state:
        st.info("Generate an email first from the ✉️ Original tab.")
    else:
        fade_container(lambda: st.markdown("### ✍️ Generated Email"))

        generated = st.session_state[state_key]["generated"]

        st.markdown(f"<div class='card fade-in'>{generated}</div>", unsafe_allow_html=True)

        # Quick actions
        c1, c2 = st.columns(2)
        with c1:
            st.download_button(
                "⬇️ Download as .txt",
                data=generated,
                file_name=f"email_{selected_id}_generated.txt",
                mime="text/plain",
                use_container_width=True
            )
        with c2:
            if st.button("🧹 Clear generated output", use_container_width=True):
                del st.session_state[state_key]
                st.rerun()

# ---------------- EVALUATION TAB ----------------
with tab_eval:
    if state_key not in st.session_state:
        st.info("Generate an email first from the ✉️ Original tab.")
    else:
        fade_container(lambda: st.markdown("### 📊 Judge Showdown"))

        original = st.session_state[state_key]["original"]
        generated = st.session_state[state_key]["generated"]

        ratings = []
        for jm in JUDGE_MODELS:
            judge = EmailService(jm)
            raw = judge.judge(original, generated).choices[0].message.content

            parsed = json.loads(raw) if isinstance(raw, str) else raw
            rating = parsed.get("rating", 0)
            explanation = parsed.get("explanation", "")

            ratings.append(float(rating) if rating is not None else 0.0)
            judge_card(jm, int(rating) if rating is not None else 0, explanation)

        st.markdown("### 📈 Rating Comparison")
        st.bar_chart({"Model": JUDGE_MODELS, "Rating": ratings}, x="Model", y="Rating")

# ---------------- ALL EMAILS TAB ----------------
with tab_all:
    st.markdown("### 📚 All Emails in Dataset")

    # Lightweight filters
    col1, col2 = st.columns([2, 1])
    with col1:
        q = st.text_input("Search (sender / subject / content)", "")
    with col2:
        max_rows = st.selectbox("Rows to show", [25, 50, 100, 250, 500], index=1)

    view = df.copy()

    if q.strip():
        ql = q.strip().lower()
        # Search across common text columns (only if they exist)
        search_cols = [c for c in ["sender", "subject", "content"] if c in view.columns]
        if search_cols:
            mask = False
            for c in search_cols:
                mask = mask | view[c].fillna("").astype(str).str.lower().str.contains(ql)
            view = view[mask]

    # Shorten long content in the table (keeps it pretty)
    if "content" in view.columns:
        view = view.copy()
        view["content"] = view["content"].fillna("").astype(str).apply(lambda x: x if len(x) <= 180 else x[:180] + "…")

    st.dataframe(
        view.head(max_rows),
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", format="%d"),
            "sender": st.column_config.TextColumn("From"),
            "subject": st.column_config.TextColumn("Subject"),
            "content": st.column_config.TextColumn("Content"),
        },
    )
