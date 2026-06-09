# 📊 Streamlit RAG Data Analyst

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" />
  <img src="https://img.shields.io/badge/Streamlit-App-red.svg" />
  <img src="https://img.shields.io/badge/AI-RAG-green.svg" />
  <img src="https://img.shields.io/badge/LLM-GPT%20%7C%20LLaMA-purple.svg" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey.svg" />
</p>

---

## 🧠 AI-Powered Business Data Analyst (RAG + LLMs)

A **Retrieval-Augmented Generation (RAG) analytics assistant** built with **Streamlit**, enabling natural language analysis of CSV datasets using **GPT-4.1 Mini / LLaMA 3**.

It transforms raw data into:
- 📌 Insights  
- ⚠️ Risks  
- 💡 Opportunities  
- 📈 Visual recommendations  

---

## 🚀 Live App

👉 **[Launch Streamlit App](https://app-rag-data-analyst-pk9ohfsmd8ps2hfxwpqwbp.streamlit.app/)**

---

## 📸 UI Preview

Add your screenshot below:

---

## ✨ Features

- 📂 Upload your own CSV dataset
- 📦 Preloaded sample datasets for instant testing
- 📈 Interactive dataset visualization (Plotly)
- 🔎 Retrieval-Augmented Generation (RAG) context filtering
- 🧠 AI-powered business analysis (GPT-4.1 Mini / LLaMA 3)
- ⚠️ Risk detection & anomaly insights
- 💡 Opportunity identification
- 💬 Chat with your dataset
- 🛡️ Prompt injection protection layer
- ⚡ Cached dataset loading for performance optimization
- 📊 Expandable dataset explorer

---

## 🧠 How It Works (RAG Pipeline)

1. User uploads or selects a dataset
2. User asks a natural language question
3. System retrieves relevant rows using lightweight RAG logic
4. Retrieved context is injected into the LLM prompt
5. LLM returns structured business insights

---

## 📊 Output Format

The AI responds in a structured format:

- 📌 **Insights** → key trends, patterns
- ⚠️ **Risks** → anomalies, drops, concerns
- 💡 **Opportunities** → growth signals
- 📈 **Recommended Charts** → best visualizations

---

## 📂 Default Dataset

If no file is uploaded, the app loads:

- `sales.csv`

You can override this by uploading your own CSV file.

---

## 🛠️ Run Locally

git clone https://github.com/your-username/streamlit-rag-data-analyst.git

cd streamlit-rag-data-analyst

pip install -r requirements.txt

streamlit run streamlit_rag_analysis_prompt_app.py

---

## 🔐 Environment Variables

Create a `.env` file for local development:

GITHUB_TOKEN_GPT_MINI=your_token_here
GITHUB_TOKEN_LLAMA_INSTRUCT=your_token_here

---

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
- Safe context builder (prevents LLM overload)
- RAG-based controlled data retrieval
- API failure handling & fallback safety

---

## 📌 Notes

- This project is designed for business analytics use cases
- Works best with structured CSV datasets
- Optimized for small-to-medium datasets (< 5MB recommended)
