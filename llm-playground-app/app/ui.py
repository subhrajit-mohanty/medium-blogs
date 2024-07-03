import streamlit as st

def create_ui(available_models):
    num_models = st.slider("Select number of models", min_value=2, max_value=5, value=5)
    selected_models = st.multiselect("Select models", available_models, default=available_models[:num_models])

    if len(selected_models) != num_models:
        st.warning(f"Please select exactly {num_models} models.")
        return None, None, None

    user_input = st.text_area("Enter your prompt (Markdown supported)", height=150)

    return num_models, selected_models, user_input