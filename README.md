#  Autonomous AI Code Review Agent

An intelligent AI-powered source code auditing platform that autonomously ingests public GitHub repositories, parses Python files using Abstract Syntax Tree (AST) analysis, and generates confidence-rated code review findings using Large Language Models (LLMs).

This project is built around the principle of **Epistemic Humility**, where the AI explicitly communicates uncertainty levels instead of treating every prediction as fully reliable.

---

#  Live Demo & Repository

-  Live Application: https://aicodereviewagent-ekpc5w8ffiqipvekuu5cjs.streamlit.app/

---

#  Features

-  Automated GitHub repository ingestion
-  AST-based static code analysis
-  AI-powered code review generation
-  Confidence-based issue separation
-  Severity & category filtering
-  CSV export support
-  Interactive Streamlit dashboard
-  Responsible AI uncertainty reporting

---

#  System Architecture

```text
User Input (GitHub URL)
        │
        ▼
GitPython Repository Cloning
        │
        ▼
AST Parsing Engine
        │
        ▼
LLM Analysis (Groq + Llama-3.3-70B)
        │
        ▼
Confidence Classification
        │
        ▼
Interactive Streamlit Dashboard
```

---

#  Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend Logic |
| Streamlit | Frontend Dashboard |
| Groq API | LLM Inference |
| Llama-3.3-70B | AI Code Review |
| GitPython | Repository Cloning |
| AST Module | Static Analysis |
| Pandas | Data Processing |

---

#  Project Structure

```text
ai-code-reviewer/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── core/
│   ├── ingestion.py
│   ├── parser.py
│   └── llm_client.py
│
└── cloned_repos/
```

---

#  Installation

## 1. Clone Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
cd ai-code-reviewer
```

---

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

#  Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

#  Run The Application

```bash
streamlit run app.py
```

The application launches at:

```text
http://localhost:8501
```

---

#  Streamlit Cloud Deployment

## Deployment Steps

1. Push project to GitHub
2. Open Streamlit Community Cloud
3. Create a new app
4. Select:
   - Repository → your GitHub repo
   - Branch → `main`
   - Main file → `app.py`
5. Add secret:

```text
GROQ_API_KEY="your_key_here"
```

6. Deploy the application

---

#  Dashboard Capabilities

- 📈 Real-time audit metrics
- 🔴 Critical issue tracking
- 🔒 Verified findings panel
- ⚠️ Verify-this uncertainty panel
- 🎛️ Interactive sidebar filtering
- 📥 CSV export support

---

#  Example AI Finding

## Example Code

```python
def calculate_discount(price, discount_percentage):
    final_price = price - (price * (discount_percentage / 100))
    return final_price
```

## AI Observation

- Missing input validation
- No percentage range checking
- Potential runtime errors

## Suggested Fix

```python
if discount_percentage < 0 or discount_percentage > 100:
    raise ValueError("Discount percentage must be between 0 and 100.")
```

---

#  Responsible AI Design

This project implements:
- Confidence scoring
- Human verification pathways
- Explicit uncertainty reporting
- Secure environment variable handling

---

#  Known Limitations

- Python-only support
- Single-file analysis scope
- No cross-file dependency tracking
- LLM responses may occasionally hallucinate

---

#  Future Improvements

- Multi-language support
- Cross-file relationship analysis
- Docker deployment
- CI/CD integrations
- Pull request review automation
- Vector database memory
- Persistent audit history

---

#  Author

Developed as an educational AI engineering project focused on autonomous code auditing and responsible LLM-based software analysis.

---

#  License

This project is intended for educational and research purposes.
