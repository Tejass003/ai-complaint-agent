# 🛒 AI-Powered Multilingual E-Commerce Complaint Resolution Agent

An end-to-end AI agent that automates the resolution of e-commerce customer complaints by analyzing customer issues, retrieving relevant company policies using Retrieval-Augmented Generation (RAG), and generating consistent, data-driven decisions.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.6-green)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-Llama3_70B-orange)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-purple)](LICENSE)

---

# 🎯 Problem Statement

Modern e-commerce platforms receive thousands of customer complaints every day. Handling these complaints manually is time-consuming, inconsistent, and expensive.

This project demonstrates how an AI-powered complaint resolution system can automatically analyze complaints, retrieve company policies, verify order details, and recommend appropriate actions within seconds.

**Average manual resolution time:** ~15 minutes

**AI-powered resolution time:** **Under 30 seconds**

---

# ✨ Key Features

* 🌍 Multilingual complaint support (English, Hindi, Tamil)
* 🤖 AI-powered complaint analysis using Llama 3 (70B)
* 📚 Retrieval-Augmented Generation (RAG) with ChromaDB
* 📄 Company-specific policy retrieval (Amazon, Flipkart, Meesho)
* 📦 Automated order verification
* 📧 Personalized email responses in the customer's language
* 👥 Role-based authentication (Admin & Agent)
* 📊 AI confidence scoring with automatic escalation
* 📝 Complete audit logging for transparency
* ⚡ FastAPI backend with Streamlit dashboard

---

# 🏗️ System Architecture

```text
Customer Complaint (Any Language)
            │
            ▼
Language Detection & Translation
            │
            ▼
RAG Pipeline (LangChain + ChromaDB)
249 Policy Chunks from 3 Companies
            │
            ▼
Order Lookup
100+ Sample Orders
            │
            ▼
Groq LLM (Llama 3 70B)
Complaint Resolution
            │
            ▼
Decision Engine
REFUND • REPLACE • ESCALATE
            │
            ▼
Email Generation
            │
            ▼
SQLite Audit Log
```

---

# 🛠️ Technology Stack

| Layer                | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python 3.11           |
| LLM                  | Groq – Llama 3 70B    |
| AI Framework         | LangChain             |
| Vector Database      | ChromaDB              |
| Embeddings           | sentence-transformers |
| Backend              | FastAPI               |
| Frontend             | Streamlit             |
| Database             | SQLite + SQLAlchemy   |
| Authentication       | bcrypt                |
| Translation          | deep-translator       |
| Email Service        | Gmail SMTP            |
| PDF Processing       | PyPDF                 |

---

# 📂 Project Structure

```text
ai-complaint-agent/
│
├── app/
│   ├── agent.py            # AI decision engine
│   ├── auth.py             # Authentication
│   ├── db.py               # Database models
│   ├── email_sender.py     # Email service
│   ├── main.py             # FastAPI application
│   └── translator.py       # Translation utilities
│
├── rag/
│   ├── ingest.py           # PDF → ChromaDB
│   └── query.py            # Policy retrieval
│
├── data/
│   └── orders.json         # Sample order database
│
├── streamlit_app/
│   └── app.py              # Dashboard UI
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Tejass003/ai-complaint-agent.git
cd ai-complaint-agent
```

## 2. Create and Activate a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 3. Configure Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key

GMAIL_ADDRESS=your_email@gmail.com

GMAIL_APP_PASSWORD=your_app_password

CHROMA_PERSIST_DIR=./chroma_db

POLICY_PDF_PATH=./data/
```

---

## 4. Build the Vector Database

```bash
python rag/ingest.py
```

---

## 5. Launch the Application

```bash
streamlit run streamlit_app/app.py
```

---

# 🔑 Default Credentials

```text
Email: admin@complaints.com
Password: admin123
```

---

# 📊 AI Decision Logic

| Scenario                                  | Decision |
| ----------------------------------------- | -------- |
| Damaged product reported within 10 days   | REPLACE  |
| Refund requested within 10 days           | REFUND   |
| Order value above ₹50,000                 | ESCALATE |
| Complaint submitted after 30 days         | ESCALATE |
| Unclear or insufficient complaint details | ESCALATE |
| AI confidence below 60%                   | ESCALATE |

---

# 🚀 Future Enhancements

* Voice complaint support
* WhatsApp integration
* OCR for invoice verification
* Multi-company onboarding portal
* Analytics dashboard
* Docker deployment
* Kubernetes support
* CI/CD with GitHub Actions

---

## 👨‍💻 Author

**Tejas Kunde**

B.E. Information Technology
Vidyalankar Institute of Technology
CGPA: **9.02**

Passionate about Artificial Intelligence, Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), Machine Learning, and Full-Stack Development. I enjoy building intelligent applications that solve real-world problems through practical AI solutions.

### 🌐 Connect with Me

* **GitHub:** https://github.com/Tejass003
* **LinkedIn:** https://www.linkedin.com/in/tejas-kunde/

Or use badges:

[![GitHub](https://img.shields.io/badge/GitHub-Tejass003-181717?style=for-the-badge\&logo=github)](https://github.com/Tejass003)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Tejas%20Kunde-0A66C2?style=for-the-badge\&logo=linkedin)](https://www.linkedin.com/in/tejas-kunde/)
