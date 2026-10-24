# TechHire AI — Resume Screening and Candidate Ranking

An AI-powered resume screening application that helps compare resumes against a job description using semantic similarity, skill matching, and optional Retrieval-Augmented Generation (RAG) explanations.

## Overview

TechHire AI is a Python-based project that explores how pretrained language models can support resume analysis. Users can upload resumes, provide a job description, review candidate match scores, and inspect ranking results through an interactive Streamlit interface.

## Key Features

- **Resume Processing:** Extract text from PDF resumes.
- **Semantic Similarity:** Use the pretrained `all-MiniLM-L6-v2` Sentence Transformer to represent text as embeddings.
- **Skill Matching:** Compare resume skills with requirements in the job description.
- **Candidate Ranking:** Combine matching signals to produce an ordered candidate list.
- **Interactive Dashboard:** Review candidate results and available analytics.
- **RAG-Based Explanations (Optional):** Retrieve relevant resume evidence and generate a natural-language explanation using a locally running Ollama model.
- **Requirement Audit:** Display a keyword-presence report separately from the generated explanation.
- **Research Dataset:** Includes synthetic resume profiles for experimentation.

## Technology Stack

- **Language:** Python
- **Interface:** Streamlit
- **NLP and Embeddings:** Sentence Transformers, `all-MiniLM-L6-v2`
- **Machine Learning Utilities:** scikit-learn
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly
- **PDF Processing:** PyPDF2
- **Optional Local LLM:** Ollama with Qwen 2.5 1.5B

## How It Works

1. Upload PDF resumes.
2. Enter the job description.
3. Extract text from the resumes.
4. Generate text embeddings using the pretrained Sentence Transformer.
5. Calculate semantic similarity and skill-matching signals.
6. Rank candidates and review results in the dashboard.
7. Optionally retrieve relevant resume passages and generate a RAG-based explanation.

## Project Structure

```text
TechHire-AI-Resume-Screening/
├── app.py
├── model.py
├── utils.py
├── sidebar.py
├── dashboard.py
├── candidate_cards.py
├── charts.py
├── skill_analytics.py
├── login.py
├── recommendation.py
├── resume_analysis.py
├── report_generator.py
├── style.py
├── requirements.txt
├── assets/
└── research_data/
    ├── rag_generation.py
    ├── rag_prototype.py
    ├── synthetic_resume_profiles_100.csv
    ├── synthetic_resume_dataset_README.txt
    ├── dataset_validation_report.txt
    ├── test_job_description.txt
    └── validate_dataset.py
```

*The structure above describes the intended repository layout. Confirm that every listed file exists before publishing.*

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/kundekarkaushal3-spec/TechHire-AI-Resume-Screening.git
cd TechHire-AI-Resume-Screening
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## Optional RAG Setup

The RAG explanation feature requires a locally running Ollama service and the configured language model. If you want to use this feature, install Ollama, download the model configured by the project, and ensure the Ollama service is running before using the RAG option.

The standard resume-ranking workflow and optional RAG workflow should be evaluated separately.

## Research Dataset

The `research_data/` directory contains synthetic resume profiles and supporting validation and experimentation files. Synthetic data is used for development and does not represent a validated real-world hiring benchmark.

## Limitations and Responsible Use

- Match scores indicate similarity to a supplied job description; they are **not** probabilities of hiring success.
- Keyword presence does not establish a candidate's actual proficiency.
- Generated explanations can contain errors and should be checked against retrieved resume evidence.
- Synthetic data does not establish performance on real recruitment data.
- The system is a decision-support prototype and should not make hiring decisions autonomously.
- Candidate information should be handled with appropriate privacy and consent safeguards.

## Future Improvements

- Evaluate ranking quality using a labelled relevance dataset.
- Compare keyword-based, semantic, and hybrid ranking methods.
- Measure ranking metrics such as Precision@K, Recall@K, and NDCG@K.
- Improve evidence traceability and explanation verification.
- Add tests and improve deployment documentation.

## Author

**Kaushal Kundekar**

MCA — Artificial Intelligence and Machine Learning

## Disclaimer

This project is developed for educational and research purposes. It is not a substitute for human review in recruitment.
