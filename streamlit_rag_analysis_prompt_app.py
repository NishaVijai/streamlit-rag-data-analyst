import os
import pandas as pd
import streamlit as st
import plotly.express as px
import yaml
import requests
from dotenv import load_dotenv

from streamlit_rag_analysis_prompt_layer import retrieve_relevant_data

# -------------------
# Setup
# -------------------
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN_GPT_MINI")

if not GITHUB_TOKEN:
    st.error("Missing GITHUB_TOKEN in .env")
    st.stop()

st.title("💬📊 Streamlit RAG Data Analyst")

# -------------------
# Upload CSV
# -------------------
uploaded_file = st.file_uploader(
    "Upload sales CSV",
    type=["csv"]
)

if uploaded_file:

    # -------------------
    # Load CSV
    # -------------------
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Dataset")
    st.dataframe(df)

    # -------------------
    # Chart
    # -------------------
    st.subheader("📈 Sales Trend")

    fig = px.line(
        df,
        x="month",
        y="sales",
        title="Sales Over Time",
        markers=True
    )

    st.plotly_chart(fig)

    # -------------------
    # Load YAML Prompt
    # -------------------
    with open(
        "analysis_prompt.yml",
        "r",
        encoding="utf-8"
    ) as file:

        prompt_template = yaml.safe_load(file)

    # -------------------
    # Extract Prompts
    # -------------------
    system_prompt = prompt_template["system_prompt"]

    analysis_prompt = prompt_template["analysis_prompt"]

    # -------------------
    # Session Memory
    # -------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -------------------
    # Render Chat History
    # -------------------
    st.subheader("💬 Chat with your data")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # -------------------
    # Chat Input
    # -------------------
    user_input = st.chat_input(
        "Ask about your sales data..."
    )

    if user_input:

        # -------------------
        # Save User Message
        # -------------------
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        # -------------------
        # RAG Retrieval
        # -------------------
        relevant_df = retrieve_relevant_data(
            df,
            user_input
        )

        # -------------------
        # Show Retrieved Data
        # -------------------
        st.subheader("🔍 Retrieved Data (RAG)")
        st.dataframe(relevant_df)

        # -------------------
        # Build Final Prompt
        # -------------------
        final_prompt = analysis_prompt.format(
            context=relevant_df.to_string(index=False),
            question=user_input
        )

        # -------------------
        # Build Messages
        # -------------------
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": final_prompt
            }
        ]

        # -------------------
        # API Call
        # -------------------
        url = "https://models.github.ai/inference/chat/completions"

        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": prompt_template["model"],
            "messages": messages
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload
        )

        # -------------------
        # AI Response
        # -------------------
        if response.status_code == 200:

            result = response.json()

            ai_reply = result["choices"][0]["message"]["content"]

            # Save assistant message
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_reply
                }
            )

            # Refresh UI
            st.rerun()

        else:
            st.error(f"API Error: {response.status_code}")
            st.write(response.text)