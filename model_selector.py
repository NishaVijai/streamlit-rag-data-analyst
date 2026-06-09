import os
import streamlit as st


def load_model_selector(prompt_template):
    """
    Streamlit model selector driven by YAML config
    + secure token mapping via env/secrets.
    """

    # -------------------
    # MODEL TOKEN MAP
    # -------------------
    model_map = {
        "openai/gpt-4.1-mini": "GITHUB_TOKEN_GPT_MINI",
        "meta/llama-3.3-70b-instruct": "GITHUB_TOKEN_LLAMA_INSTRUCT",
    }

    # -------------------
    # LOAD YAML CONFIG
    # -------------------
    yaml_models = prompt_template.get("models", {}).get("options", [])

    default_model = prompt_template.get("models", {}).get(
        "default", "openai/gpt-4.1-mini"
    )

    # -------------------
    # FALLBACK IF YAML IS EMPTY
    # -------------------
    if not yaml_models:
        yaml_models = list(model_map.keys())

    # -------------------
    # FILTER VALID MODELS
    # -------------------
    available_models = [m for m in yaml_models if m in model_map]

    if not available_models:
        st.error("No valid models configured in YAML.")
        st.stop()

    # -------------------
    # DEFAULT INDEX
    # -------------------
    default_index = 0

    if default_model in available_models:
        default_index = available_models.index(default_model)

    # -------------------
    # STREAMLIT DROPDOWN
    # -------------------
    selected_model = st.selectbox("Choose LLM", available_models, index=default_index)

    # -------------------
    # TOKEN RESOLUTION
    # -------------------
    token_key = model_map.get(selected_model)

    if not token_key:
        st.error(f"Unsupported model: {selected_model}")
        st.stop()

    github_token = st.secrets.get(token_key) or os.getenv(token_key)

    if not github_token:
        st.error(f"Missing API key: {token_key}")
        st.stop()

    # -------------------
    # DEBUG INFO (optional)
    # -------------------
    st.caption(f"Active Model: {selected_model}")

    return selected_model, github_token
