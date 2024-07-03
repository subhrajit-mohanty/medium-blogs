import streamlit as st
from app.models import AVAILABLE_MODELS, model_output
from app.ui import create_ui
from app.utils import process_markdown
import queue
import threading

# CSS styles
CSS = """
<style>
.stApp {
    max-width: 100%;
    padding-top: 2rem;
}
.output-box {
    border: 1px solid #4a4a4a;
    border-radius: 5px;
    padding: 10px;
    height: 300px;
    overflow-y: auto;
    margin-bottom: 10px;
    background-color: #2d2d2d;
    color: #e0e0e0;
    font-family: 'Courier New', Courier, monospace;
    white-space: pre-wrap;
    word-wrap: break-word;
}
.output-box pre {
    background-color: #1e1e1e;
    border-radius: 3px;
    padding: 10px;
    overflow-x: auto;
    white-space: pre;
}
.output-box code {
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.9em;
}
</style>
"""

def run_app():
    st.set_page_config(layout="wide", page_title="Dynamic Parallel Multi-Model App")
    
    # Apply CSS
    st.markdown(CSS, unsafe_allow_html=True)
    
    st.title("LLM Playground")

    num_models, selected_models, user_input = create_ui(AVAILABLE_MODELS)

    if st.button("Generate"):
        if user_input:
            generate_outputs(selected_models, user_input)
        else:
            st.warning("Please enter a prompt.")

def generate_outputs(selected_models, user_input):
    cols = st.columns(len(selected_models))
    placeholders = {}
    for i, model in enumerate(selected_models):
        with cols[i]:
            st.subheader(model)
            placeholders[model] = st.empty()

    output_queue = queue.Queue()
    threads = [
        threading.Thread(target=model_output, args=(model, user_input, output_queue))
        for model in selected_models
    ]

    for thread in threads:
        thread.start()

    outputs = {model: "" for model in selected_models}

    while any(thread.is_alive() for thread in threads):
        try:
            name, output = output_queue.get(timeout=0.1)
            outputs[name] = output
            processed_output = process_markdown(outputs[name])
            placeholders[name].markdown(f'<div class="output-box">{processed_output}</div>', unsafe_allow_html=True)
        except queue.Empty:
            continue
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    for thread in threads:
        thread.join()