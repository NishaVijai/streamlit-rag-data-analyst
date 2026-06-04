# 📊 Streamlit RAG Data Analyst

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![RAG](https://img.shields.io/badge/AI-RAG-green.svg)
![LLM](https://img.shields.io/badge/LLM-GPT%20%7C%20LLaMA-purple.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

A **Retrieval-Augmented Generation (RAG) powered Business Analytics Assistant** built with **Streamlit + LLMs (GPT-4.1 Mini / LLaMA 3)**.

This app lets users analyze CSV data using natural language and get structured business insights, trends, risks, and opportunities.

---

## 🚀 Live App

👉 **[Launch Streamlit App](https://app-rag-data-analyst-pk9ohfsmd8ps2hfxwpqwbp.streamlit.app/)**

---

## ✨ Features

- 📂 Upload your own CSV dataset
- 📦 Preloaded sample dataset for instant testing
- 📈 Interactive sales trend visualization (Plotly)
- 🔎 RAG-based context retrieval (smart filtering)
- 🧠 AI-powered business analysis (GPT-4.1 Mini / LLaMA 3)
- ⚠️ Risk detection & anomaly insights
- 💡 Opportunity identification
- 💬 Chat with your dataset
- 🛡️ Prompt injection protection layer
- 📊 Expandable dataset viewer (clean UI)

---

## 🧠 How It Works (RAG Pipeline)

1. User uploads or uses default dataset (`sales.csv`)
2. User asks a question in natural language
3. System retrieves relevant rows using lightweight RAG logic
4. Retrieved context is injected into prompt
5. LLM generates structured business insights

---

## 📊 Output Format

The AI responds with:

- 📌 Insights (trends, patterns)
- ⚠️ Risks (drops, anomalies)
- 💡 Opportunities (growth signals)
- 📈 Recommended charts

---

## 📂 Default Dataset

If no file is uploaded, the app automatically loads:

- `sales.csv`

You can override this anytime by uploading your own CSV file.

---

## 🛠️ Run Locally

```bash
git clone https://github.com/your-username/streamlit-rag-data-analyst.git

cd streamlit-rag-data-analyst

pip install -r requirements.txt

streamlit run streamlit_rag_analysis_prompt_app.py


## 🔐 Environment Variables

Create a `.env` file for local development:

```env
GITHUB_TOKEN_GPT_MINI=your_token_here
GITHUB_TOKEN_LLAMA_INSTRUCT=your_token_here


## 🧰 Tech Stack

- Streamlit  
- Pandas  
- Plotly  
- PyYAML  
- Requests  
- GitHub Models API  
- GPT-4.1 Mini  
- LLaMA 3 70B  

---

## 🛡️ Security Features

- Prompt injection detection layer  
- System prompt isolation  
- Safe context injection  
- Controlled dataset retrieval (RAG)

