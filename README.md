# AI Engineer Learning & Certification Repo

> A structured learning repository for the **AI Engineer** path — covering Python, Math, Machine Learning, Deep Learning, NLP, LLMs, MLOps, and Data Engineering.

---

## 📂 Structure

```
Data-science/
├── 01_python_fundamentals/     # Python basics, OOP, libraries (NumPy, Pandas, etc.)
├── 02_math_for_ai/             # Linear algebra, calculus, probability, optimization
├── 03_machine_learning/        # Supervised/unsupervised learning, sklearn, ensembles
│                               # ⚠️  ML module to be expanded as we progress
├── 04_deep_learning/           # Neural networks, CNNs, RNNs, Transformers
├── 05_nlp/                     # Text preprocessing, embeddings, language models
├── 06_llms_and_generative_ai/  # Prompting, RAG, Agents, Claude API
├── 07_mlops/                   # Experiment tracking, model serving, monitoring
├── 08_data_engineering/        # SQL, pipelines, vector databases
│
├── utils/                      # Shared helper utilities (imported across modules)
├── resources/                  # Cheat sheets, PDFs, reference material
├── projects/                   # Capstone and mini-projects
│
├── pyproject.toml              # ALL packages declared here (single root env)
├── .venv/                      # Shared virtual environment (git-ignored)
└── .env                        # API keys — copy from .env.example
```

Each module follows the pattern:

```
03_machine_learning/
├── README.md                   # Module overview and learning goals
├── 01_supervised_learning/
│   ├── concept_notes.ipynb     # Jupyter notebook with theory + code
│   └── practice.py            # Python script for hands-on practice
├── 02_unsupervised_learning/
...
```

---

## ⚙️ Setup

### Prerequisites

- Python 3.11+
- [`uv`](https://docs.astral.sh/uv/) package manager

### Install

```bash
# 1. Clone the repo
git clone <repo-url>
cd Data-science

# 2. Create virtual environment and install all packages
uv sync

# 3. Copy env template and fill in your API keys
cp .env.example .env

# 4. Launch JupyterLab
uv run jupyter lab
```

### Using the shared environment in notebooks

Select the kernel **`.venv (Python 3.x)`** in JupyterLab — it has all packages installed.

---

## 🗺️ Learning Path

| #   | Module               | Status                        |
| --- | -------------------- | ----------------------------- |
| 01  | Python Fundamentals  | 🟡 In Progress                |
| 02  | Math for AI          | 🔲 Planned                    |
| 03  | Machine Learning     | 🔲 Planned — _to be expanded_ |
| 04  | Deep Learning        | 🔲 Planned                    |
| 05  | NLP                  | 🔲 Planned                    |
| 06  | LLMs & Generative AI | 🟡 In Progress                |
| 07  | MLOps                | 🔲 Planned                    |
| 08  | Data Engineering     | 🔲 Planned                    |

---

## 📦 Package Management

All packages are managed from the **root** `pyproject.toml`. Never create separate `venv` or `requirements.txt` inside module folders.

```bash
# Add a new package
uv add <package-name>

# Add a dev-only package
uv add --dev <package-name>
```

---

## 📝 Notes

- `claude-certification/` — standalone project with its own environment, kept separately.
- `resources/` — PDFs and cheat sheets for quick reference.
- `utils/helpers.py` — shared utility functions importable from any notebook/script.

---

## 🏷️ Certification Target

This repo tracks preparation for the **AI Engineer** certification. Roadmap details in [`Roadmap/README.md`](Roadmap/README.md).
