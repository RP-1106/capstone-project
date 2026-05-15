# PaisaVault: AI-Assisted Personal Finance Management System

<p align="justify">
A lightweight, privacy-focused financial management tool with intelligent features to help users make better financial decisions without requiring external account integration.
</p>

<div align="center">
  <img src="output/about.PNG" width="800"/>
</div>

> 🌐 **Live Demo:** [paisavault-capstone-project.streamlit.app](https://paisavault-capstone-project.streamlit.app)
>
> This is a deployment fork of the original project at (https://github.com/shrutishrinivasan/capstone-project), with additional deployment configurations, performance improvements, and extended evaluations.

---

## What's New in This Fork

- **Deployed on Streamlit Community Cloud** with a live public URL
- **Replaced ChromaDB with FAISS** for vector retrieval — eliminates SQLite/OpenTelemetry conflicts on cloud and dramatically reduces response time
- **Upgraded LLM:** `mistral-saba-24b` (decommissioned) → `llama-3.3-70b-versatile`
- **Cloud MySQL** via Aiven (free tier) replacing local MySQL dependency
- **Response time reduced from 30–120 seconds to under 1 second** (FAISS + Groq caching)
- **Expanded knowledge base** for both bots (generic.csv +29 rows, custom.csv +20 rows) covering debit/credit cards, loans, insurance, mutual funds, taxes, and more app-specific content
- **Fixed deployment issues:** cross-platform file paths, Python 3.11 compatibility, deprecated imports
- **UI fixes:** calculator layout, file uploader label, expander button overlap, emoji chat avatars
- **New evaluation suite** (`updated_eval/`) for the deployed model and retrieval stack

---

## Key Features
- **Butterfly Effect Simulator:** Shows the compounding impact of small financial changes over time, reflecting the butterfly effect concept of chaos theory in personal finance.
- **Financial Scenario Tester:** Stress-tests various financial situations (market crash, medical emergency, job loss) and assesses likelihood of reaching financial milestones (education, home purchase, investments).
- **AI-Powered Assistant:** Custom chatbot using `llama-3.3-70b-versatile` via Groq API with FAISS-based retrieval to answer both transactional and financial queries.
- **Privacy-First Design:** No external account integration required, eliminating data security concerns.

---

## Tech Stack

### Frontend  
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/) [![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML) [![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)

### Backend 
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/) [![Hugging Face](https://img.shields.io/badge/HuggingFace-FFD21F?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/) [![FAISS](https://img.shields.io/badge/FAISS-0078D4?style=for-the-badge&logoColor=white)](https://github.com/facebookresearch/faiss) [![Groq](https://img.shields.io/badge/Groq_API-FF6B6B?style=for-the-badge&logoColor=white)](https://groq.com/)

### Database  
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/) [![Aiven](https://img.shields.io/badge/Aiven-FF3D00?style=for-the-badge&logoColor=white)](https://aiven.io/)

### Libraries  
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)](https://numpy.org/) [![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/) [![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/) [![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/) [![LangChain](https://img.shields.io/badge/LangChain-000000?style=for-the-badge)](https://www.langchain.com/) [![sentence-transformers](https://img.shields.io/badge/sentence--transformers-FFD21F?style=for-the-badge&logoColor=black)](https://www.sbert.net/)

### Evaluation
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/) [![NLTK](https://img.shields.io/badge/NLTK-4B8BBE?style=for-the-badge&logoColor=white)](https://www.nltk.org/) [![ROUGE](https://img.shields.io/badge/ROUGE-E34F26?style=for-the-badge&logoColor=white)](https://pypi.org/project/rouge-score/) [![SacreBLEU](https://img.shields.io/badge/SacreBLEU-00BFFF?style=for-the-badge&logoColor=white)](https://github.com/mjpost/sacrebleu)

---

## Evaluation Results (llama-3.3-70b-versatile + FAISS)

Evaluation scripts are in `updated_eval/` and results are saved as JSON in the same folder.
Run from the project root: `python updated_eval/Generic_Llama_Evaluation.py`

### Generic Bot (pre-login)

| Metric | Score |
|---|---|
| Response Relevancy | 0.600 |
| Faithfulness | **0.900** |
| Semantic Similarity | **0.715** |
| BLEU | 0.111 |
| ROUGE-1 | 0.396 |
| ROUGE-2 | 0.165 |
| ROUGE-L | 0.374 |
| **Avg Response Time** | **0.87 seconds** |

### FinMentor Bot (post-login)

| Metric | Score |
|---|---|
| Response Relevancy | 0.687 |
| Faithfulness | **1.000** |
| Semantic Similarity | **0.748** |
| BLEU | 0.072 |
| ROUGE-1 | 0.305 |
| ROUGE-2 | 0.089 |
| ROUGE-L | 0.263 |
| **Avg Response Time** | **0.57 seconds** |

> **Note:** Low BLEU/ROUGE scores are expected for conversational bots — these metrics penalize any phrasing that differs from the reference even when the meaning is correct. Faithfulness and Semantic Similarity are the more meaningful indicators for RAG-based chatbots.

---

## Installation (Local)

### Prerequisites
- Python 3.11
- Groq API key ([console.groq.com](https://console.groq.com))
- Aiven MySQL instance (free tier at [aiven.io](https://aiven.io)) or local MySQL

### Setup
1. Clone this fork and switch to the deploy branch.
   ```bash
   git clone https://github.com/RP-1106/capstone-project.git
   cd capstone-project
   git checkout deploy
   ```

2. Create a virtual environment and install dependencies.
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```

3. Configure secrets. Create `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your_groq_api_key"

   [mysql]
   host     = "your-aiven-host.aivencloud.com"
   port     = 14073
   user     = "avnadmin"
   password = "your-aiven-password"
   database = "expenses_db"
   ```

4. Launch the application.
   ```bash
   python -m streamlit run app.py
   ```

---

## Deployment (Streamlit Community Cloud)

1. Fork this repo or use `RP-1106/capstone-project` directly.
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app.
3. Set **Branch** to `deploy` and **Main file** to `app.py`.
4. Under **Advanced Settings**, paste your secrets (same as `secrets.toml` above) and set **Python version** to `3.11`.
5. Click **Deploy**.

---

## Application Layout

### Landing Page (no login required)
About · Features · Tools · Bot · Learn · Login

### Personal Dashboard (after login)
Getting Started · Upload Data · Overview · Income/Expense · Financial Foresight · Custom Bot · Explore Resources · Logout

---

## Frontend Screenshots

### Overview Section
<div align="center">
  <img src="output/overview1.PNG" width="800"/>
  <img src="output/overview4.PNG" width="800"/>
</div>

### Chatbot Section
<div align="center">
  <img src="output/data_digger.PNG" width="800"/>
  <img src="output/fin_mentor.PNG" width="800"/>
</div>

### Butterfly Effect Simulator
<div align="center">
  <img src="output/butterfly_effect1.PNG" width="800"/>
</div>

### Financial Scenario Tester
<div align="center">
  <img src="output/scenario_tester1.PNG" width="800"/>
</div>

For more screenshots, see the `output/` folder.

---

## Original Project
This fork is based on the original capstone project at (https://github.com/shrutishrinivasan/capstone-project). All core application logic, UI design, and feature set are the work of the original team.
