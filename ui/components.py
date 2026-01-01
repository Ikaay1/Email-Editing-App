import streamlit as st

def rating_style(rating):
    if rating >= 4:
        return "rating-good"
    if rating == 3:
        return "rating-mid"
    return "rating-bad"

def judge_card(model, rating, explanation):
    css = rating_style(rating)
    st.markdown(
        f"""
        <div class="card fade-in">
            <h4>{model}</h4>
            <p class="{css}">Rating: {rating}</p>
            <details>
                <summary>Explanation</summary>
                <p>{explanation}</p>
            </details>
        </div>
        """,
        unsafe_allow_html=True
    )
