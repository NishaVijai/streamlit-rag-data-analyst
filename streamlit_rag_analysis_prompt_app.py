import pandas as pd
import streamlit as st
import plotly.express as px
import yaml
import requests
import re
from dotenv import load_dotenv

from streamlit_rag_analysis_prompt_layer import retrieve_relevant_data
from model_selector import load_model_selector

# -------------------
# SETUP
# -------------------
load_dotenv()

st.set_page_config(
    page_title="Streamlit RAG Data Analyst", page_icon="📊", layout="wide"
)

st.title("💬📊 Streamlit RAG Data Analyst")

st.info("Choose a sample dataset or upload your own CSV.")

# -------------------
# FILE SIZE GUARDRAIL
# -------------------
MAX_FILE_SIZE_MB = 5


def validate_file(uploaded_file):
    if uploaded_file is not None:
        size_mb = uploaded_file.size / (1024 * 1024)

        if size_mb > MAX_FILE_SIZE_MB:
            st.error(
                f"File too large ({size_mb:.2f}MB). "
                f"Please upload a file smaller than {MAX_FILE_SIZE_MB}MB."
            )
            st.stop()


# -------------------
# DATASETS
# -------------------

DATASETS = {
    "Basic Sales Dataset": {
        "file": "sample_data/sales.csv",
        "description": """
Simple monthly sales dataset.

Best for:
- Highest sales
- Lowest sales
- Total sales
- Average sales
- Trend analysis
""",
    },
    "Sales Performance Dataset": {
        "file": "sample_data/sales_performance.csv",
        "description": """
Sales, marketing spend,
customer acquisition and returns.

Best for:
- Marketing effectiveness
- Growth analysis
- Return analysis
""",
    },
    "Regional Sales Dataset": {
        "file": "sample_data/regional_sales.csv",
        "description": """
Regional sales performance.

Best for:
- Region comparison
- Best region
- Regional trends
""",
    },
    "Product Sales Dataset": {
        "file": "sample_data/product_sales.csv",
        "description": """
Product-level sales.

Best for:
- Product comparison
- Product growth
""",
    },
    "SaaS Metrics Dataset": {
        "file": "sample_data/saas_metrics.csv",
        "description": """
Revenue, MRR,
customers and churn.

Best for:
- SaaS KPI analysis
- Churn analysis
- Revenue growth
""",
    },
}

# -------------------
# EXAMPLE QUESTIONS
# -------------------

EXAMPLE_QUESTIONS = {
    "Basic Sales Dataset": [
        "Which month had highest sales?",
        "Show sales trend",
        "What is average sales?",
    ],
    "Sales Performance Dataset": [
        "Analyze marketing effectiveness",
        "Which month had most returns?",
        "Show growth trend",
    ],
    "Regional Sales Dataset": ["Which region performs best?", "Compare regions"],
    "Product Sales Dataset": [
        "Which product sells most?",
        "Analyze product performance",
    ],
    "SaaS Metrics Dataset": [
        "Analyze churn risk",
        "Show revenue growth",
        "What opportunities exist?",
    ],
}

# -------------------
# PROMPT INJECTION
# -------------------


def is_prompt_injection(text):

    t = text.lower()

    patterns = [
        r"ignore.*instructions",
        r"system prompt",
        r"developer mode",
        r"jailbreak",
        r"reveal.*prompt",
        r"you are now",
        r"act as",
    ]

    return any(re.search(p, t) for p in patterns)


def sanitize_user_input(text):

    if is_prompt_injection(text):

        st.warning("Prompt injection attempt blocked.")

        return "Analyze only the provided dataset " "and return business insights."

    return text


# -------------------
# DATA SELECTION UI
# -------------------
st.subheader("📂 Dataset")

selected_dataset = st.selectbox("Choose sample dataset", list(DATASETS.keys()))

st.info(DATASETS[selected_dataset]["description"])

with st.expander("💡 Example Questions"):

    for q in EXAMPLE_QUESTIONS[selected_dataset]:

        st.markdown(f"- {q}")

uploaded_file = st.file_uploader("Upload your own CSV (optional)", type=["csv"])

# -------------------
# CACHED DATA LOADING (NEW)
# -------------------


@st.cache_data(show_spinner=False)
def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


# -------------------
# LOAD DATA
# -------------------
df = None

if uploaded_file is not None:
    validate_file(uploaded_file)
    df = pd.read_csv(uploaded_file)
    st.success("Using uploaded dataset")

else:
    # df = pd.read_csv(DATASETS[selected_dataset]["file"])
    df = load_csv(DATASETS[selected_dataset]["file"])
    st.success(f"Using sample dataset: {selected_dataset}")

# -------------------
# VALIDATION
# -------------------
if df.empty:
    st.error("Dataset is empty")
    st.stop()

if len(df.columns) < 2:
    st.error("Dataset must contain at least 2 columns")
    st.stop()

# -------------------
# DATA VIEW
# -------------------
with st.expander("📊 View Dataset", expanded=False):
    st.dataframe(df, width="stretch")

# -------------------
# DYNAMIC CHART
# -------------------
numeric_cols = df.select_dtypes(include="number").columns.tolist()
non_numeric_cols = [c for c in df.columns if c not in numeric_cols]

if numeric_cols and non_numeric_cols:
    x_col = non_numeric_cols[0]
    y_col = numeric_cols[0]

    st.subheader("📈 Dataset Trend")

    fig = px.line(df, x=x_col, y=y_col, markers=True, title=f"{y_col} by {x_col}")

    st.plotly_chart(fig, width="stretch")

# -------------------
# PROMPT CONFIG
# -------------------
if "analysis_prompt" not in st.secrets:
    st.error("Missing analysis_prompt in secrets")
    st.stop()

prompt_template = yaml.safe_load(st.secrets["analysis_prompt"])

system_prompt = prompt_template["system_prompt"]
analysis_prompt = prompt_template["analysis_prompt"]

# -------------------
# MODEL CONFIG
# -------------------
selected_model, github_token = load_model_selector(prompt_template)

if not selected_model or not github_token:
    st.error("Model configuration failed. Check secrets and prompt YAML.")
    st.stop()


# -------------------
# SMART CONTEXT BUILDER (IMPORTANT)
# -------------------
def build_safe_context(df: pd.DataFrame) -> str:
    """
    Prevents LLM overload by sampling + summarizing instead of full dataset.
    """

    numeric_df = df.select_dtypes(include="number")

    # Case 1: small dataset → safe full sample
    if len(df) <= 30:
        return df.to_string(index=False)

    # Case 2: medium dataset → sample rows
    sample_df = df.sample(n=min(30, len(df)))

    context_parts = [
        "=== SAMPLE ROWS ===",
        sample_df.to_string(index=False),
    ]

    # Case 3: add statistical summary for numeric columns
    if not numeric_df.empty:
        context_parts.append("\n=== NUMERIC SUMMARY ===")
        context_parts.append(numeric_df.describe().to_string())

    return "\n".join(context_parts)


# -------------------
# CHAT MEMORY
# -------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader("💬 Chat with your data")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------------------
# USER INPUT
# -------------------
user_input = st.chat_input("Ask about your dataset...")

if user_input:

    safe_input = sanitize_user_input(user_input)

    # Save user message
    st.session_state.messages.append({"role": "user", "content": safe_input})

    # -------------------
    # SINGLE CLEAN LOADING FLOW
    # -------------------
    with st.spinner("⏳ Analyzing data and generating insights..."):

        try:
            relevant_df = retrieve_relevant_data(df, safe_input)
        except Exception as e:
            st.error(f"RAG retrieval failed: {e}")
            st.stop()

        safe_context = build_safe_context(relevant_df).strip()

        final_prompt = analysis_prompt.format(context=safe_context, question=safe_input)

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": final_prompt},
        ]

        url = "https://models.github.ai/inference/chat/completions"

        headers = {
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json",
        }

        payload = {"model": selected_model, "messages": messages}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
        except Exception as e:
            st.error(f"Request failed: {e}")
            st.stop()

    # OUTSIDE spinner (clean UI separation)
    with st.expander("🧠 View RAG Retrieval"):
        st.dataframe(relevant_df, width="stretch")

    # -------------------
    # RESPONSE HANDLING (outside spinner)
    # -------------------
    if response.status_code == 200:

        result = response.json()
        ai_reply = result["choices"][0]["message"]["content"]

        st.session_state.messages.append({"role": "assistant", "content": ai_reply})

        st.rerun()

    else:
        st.error(f"API Error: {response.status_code}")
        st.write(response.text)
