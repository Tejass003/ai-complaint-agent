markdown# 🛒 AI-Powered Multilingual E-Commerce Complaint Resolution Agent

An end-to-end AI agent that automatically resolves e-commerce customer
complaints by reading real company policies and making data-driven decisions.

## 🎯 Problem Solved
E-commerce companies receive thousands of complaints daily.
Human agents take 15 minutes per complaint.
This system resolves complaints in **under 30 seconds**.

## ⚡ What It Does
- Customer submits complaint in **any language**
- AI detects language (English, Hindi, Tamil)
- Searches real **Amazon, Flipkart, Meesho** policies via RAG
- Checks order details automatically
- Decides: **REFUND / REPLACE / ESCALATE**
- Sends personalised email to customer in their language
- Logs everything to audit database

## 🏗️ Architecture
Customer Complaint (any language)
↓
Language Detection + Translation
↓
RAG Pipeline (LangChain + ChromaDB)
249 policy chunks from 3 companies
↓
Order Lookup (100+ orders)
↓
Groq LLM (Llama 3 70B) Decision
↓
Email Generation + Gmail SMTP
↓
SQLite Audit Log

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM Inference | Groq (Llama 3 70B) — Free |
| Agent Framework | LangChain |
| Vector Database | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| REST API | FastAPI |
| Frontend | Streamlit |
| Database | SQLite + SQLAlchemy |
| Authentication | bcrypt |
| Translation | deep-translator |
| Email | Gmail SMTP |
| PDF Parsing | PyPDF |

## 🚀 Features
- ✅ Multilingual support (English, Hindi, Tamil)
- ✅ Company-specific policy filtering
- ✅ Role-based access (Admin / Agent)
- ✅ Full audit log with AI reasoning
- ✅ Automated email sending
- ✅ Confidence scoring with auto-escalation
- ✅ Real policy documents from 3 companies

## 📁 Project Structure
complaint-agent/
├── app/
│   ├── agent.py         # AI decision engine
│   ├── auth.py          # Login + bcrypt
│   ├── db.py            # Database models
│   ├── email_sender.py  # Gmail SMTP
│   ├── main.py          # FastAPI routes
│   ├── schemas.py       # Pydantic models
│   └── translator.py    # Multilingual
├── rag/
│   ├── ingest.py        # PDF → ChromaDB
│   └── query.py        # Vector search
├── data/
│   ├── orders.json      # 100 sample orders
│   └── *.pdf            # Real policy docs
├── streamlit_app/
│   └── app.py           # UI dashboard
├── tests/
│   └── test_complaints.py
├── requirements.txt
└── README.md

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/Tejass003/ai-complaint-agent.git
cd ai-complaint-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create .env file
GROQ_API_KEY=your_groq_api_key
GMAIL_ADDRESS=your@gmail.com
GMAIL_APP_PASSWORD=your_app_password
CHROMA_PERSIST_DIR=./chroma_db
POLICY_PDF_PATH=./data/

### 4. Ingest policies
```bash
python rag/ingest.py
```

### 5. Run the app
```bash
streamlit run streamlit_app/app.py
```

## 🔑 Default Login
Email:    admin@complaints.com
Password: admin123

## 📊 Decision Logic

| Condition | Decision |
|---|---|
| Damaged product within 10 days | REPLACE |
| Refund request within 10 days | REFUND |
| Order value above Rs 50,000 | ESCALATE |
| Beyond 30 days since delivery | ESCALATE |
| Vague or unclear complaint | ESCALATE |
| AI confidence below 60% | ESCALATE |

## 👤 Author
**Tejas Kunde**
B.E. Information Technology — Vidyalankar Institute of Technology
CGPA: 9.02

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/https://www.linkedin.com/in/tejas-kunde/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/Tejass003)# ai-complaint-agent
AI-powered e-commerce complaint resolution system using RAG + LLM that automatically reads company policies, makes refund/replace/escalate decisions and drafts personalised emails.
