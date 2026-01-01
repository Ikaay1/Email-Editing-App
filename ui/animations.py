import streamlit as st

def fade_container(content_fn):
    with st.container():
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        content_fn()
        st.markdown('</div>', unsafe_allow_html=True)
