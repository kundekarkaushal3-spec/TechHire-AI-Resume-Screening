
from pathlib import Path
import json
import re
import urllib.error
import urllib.request

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. Project paths and configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "synthetic_resume_profiles_100.csv"
JOB_DESCRIPTION_PATH = BASE_DIR / "test_job_description.txt"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen2.5:1.5b"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3


# --------------------------------------------------
# 2. Load the dataset and job description
# --------------------------------------------------

def load_inputs():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    if not JOB_DESCRIPTION_PATH.exists():
        raise FileNotFoundError(
            f"Job description not found: {JOB_DESCRIPTION_PATH}"
        )

    data = pd.read_csv(DATASET_PATH)

    required_columns = {"candidate_id", "category", "resume_text"}
    missing_columns = required_columns - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Dataset is missing columns: {sorted(missing_columns)}"
        )

    job_description = JOB_DESCRIPTION_PATH.read_text(
        encoding="utf-8"
    ).strip()

    if not job_description:
        raise ValueError("The job description file is empty.")

    return data, job_description


# --------------------------------------------------
# 3. Split resume text into evidence passages
# --------------------------------------------------

def split_into_passages(resume_text):
    if pd.isna(resume_text):
        return []

    text = str(resume_text).strip()

    if not text:
        return []

    # Separate sentences and lines while preserving their text.
    passages = re.split(r"(?<=[.!?])\s+|\n+", text)

    # Also split long sections separated by semicolons.
    cleaned_passages = []

    for passage in passages:
        for part in passage.split(";"):
            part = part.strip()
            if part:
                cleaned_passages.append(part)

    return cleaned_passages



def build_verified_report(
    candidate_id,
    role_category,
    evidence,
    audit_results
):
    lines = [
        "VERIFIED RESUME EVIDENCE REPORT",
        "=" * 35,
        f"Candidate ID: {candidate_id}",
        f"Dataset role category: {role_category}",
        "",
        "A. Retrieved Resume Evidence",
        "-" * 28,
    ]

    for number, item in enumerate(evidence, start=1):
        lines.append(
            f"{number}. {item['text']}"
        )
        lines.append(
            f"   Retrieval similarity: {item['similarity']}%"
        )

    lines.extend([
        "",
        "B. Terms Found in Full Resume Text",
        "-" * 34,
    ])

    for requirement, result in audit_results.items():
        if result["matched_terms"]:
            terms = ", ".join(result["matched_terms"])
            lines.append(f"- {requirement}: {terms}")

    lines.extend([
        "",
        "C. Terms Not Found in Full Resume Text",
        "-" * 36,
    ])

    for requirement, result in audit_results.items():
        if not result["matched_terms"]:
            lines.append(
                f"- {requirement}: Not found in full resume text"
            )

    lines.extend([
        "",
        "D. Limitations",
        "-" * 14,
        "This report checks keyword presence in the full stored resume text.",
"Keyword presence does not verify proficiency.",
"Missing terms do not prove that a candidate lacks those skills.",
"Retrieval similarity is not hiring probability or model accuracy.",
    ])

    return "\n".join(lines)


def audit_requirements(resume_text):
    evidence_text = str(resume_text).lower()

    requirements = {
        "Python programming": ["python"],
        "NLP and text processing": [
            "nlp",
            "natural language processing",
            "text classification"
        ],
        "Transformer models such as BERT": [
            "bert",
            "transformers"
        ],
        "Git": ["git"],
        "Machine learning algorithms": [
            "machine learning algorithm",
            "random forest",
            "decision tree",
            "regression",
            "xgboost"
        ],
        "Deep learning fundamentals": [
            "deep learning",
            "neural network",
            "tensorflow",
            "pytorch"
        ],
        "Scikit-learn": ["scikit-learn", "sklearn"],
        "TensorFlow or PyTorch": ["tensorflow", "pytorch"],
        "Data preprocessing and model evaluation": [
            "data preprocessing",
            "model evaluation",
            "preprocessing"
        ],
        "Computer vision": ["computer vision", "opencv"],
        "Model deployment": ["model deployment", "deployed"]
    }

    results = {}

    for requirement, keywords in requirements.items():
        found = [
            keyword for keyword in keywords
            if keyword in evidence_text
        ]

        results[requirement] = {
            "status": (
    "Mentioned in full resume text"
    if found
    else "Not found in full resume text"
),
            "matched_terms": found
        }

    return results

# --------------------------------------------------
# 4. Retrieve the most relevant resume evidence
# --------------------------------------------------

def retrieve_evidence(model, resume_text, job_description):
    passages = split_into_passages(resume_text)

    if not passages:
        raise ValueError(
            "No resume passages were found for this candidate."
        )

    job_embedding = model.encode(
        job_description,
        convert_to_numpy=True
    )

    passage_embeddings = model.encode(
        passages,
        convert_to_numpy=True
    )

    scores = cosine_similarity(
        [job_embedding],
        passage_embeddings
    )[0]

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: float(scores[i]),
        reverse=True
    )

    evidence = []

    for index in ranked_indices[:TOP_K]:
        evidence.append({
            "text": passages[index],
            "similarity": round(float(scores[index]) * 100, 2)
        })

    return evidence


# --------------------------------------------------
# 5. Ask the local Ollama LLM to generate an analysis
# --------------------------------------------------


def generate_analysis(
    candidate_id,
    role_category,
    job_description,
    evidence
):
    evidence_text = "\n".join(
        f"{i}. Evidence: {item['text']}\n"
        f"   Retrieval similarity: {item['similarity']}%"
        for i, item in enumerate(evidence, start=1)
    )

    prompt = f"""
You are an assistant writing a concise resume evidence summary.

Candidate ID: {candidate_id}
Dataset role category: {role_category}

Retrieved resume evidence:
{evidence_text}

Instructions:
1. Summarize only information explicitly present in the retrieved evidence.
2. Do not copy the job description.
3. Do not invent skills, tools, education, projects, or experience.
4. Do not classify skills as present or missing. A separate Python
   keyword audit handles that task.
5. Do not infer proficiency from a keyword mention.
6. Do not make a hiring recommendation.
7. Prefer the words "mentions", "lists", or "states" when describing
   candidate skills.
8. Do not use "expertise", "proficient", "proficiency", "strong skills",
   or "experienced in" unless the retrieved evidence explicitly supports
   that level of ability or experience.
9. A skill appearing in a technical skills list proves only that it is
   listed in the resume evidence, not that proficiency has been verified.
Write only these two sections:

A. Evidence Summary
Briefly summarize the candidate information demonstrated by the
retrieved passages. Mention the actual evidence.

B. Limitations
State that only the retrieved passages were evaluated and that
keyword mentions do not establish proficiency.
"""


    request_body = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 300
        }
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(request_body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=600
        ) as response:
            result = json.loads(
                response.read().decode("utf-8")
            )

    except (urllib.error.URLError, TimeoutError) as error:
        raise RuntimeError(
            "Could not obtain a response from Ollama. "
            "Check that Ollama is running and try again. "
            "Local generation may take several minutes."
        ) from error

    answer = result.get("response", "").strip()

    if not answer:
        raise RuntimeError(
            "Ollama returned an empty response. Please try again."
        )

    return answer



# --------------------------------------------------
# 6. Run the complete retrieval + generation pipeline
# --------------------------------------------------

def main():
    print("=" * 60)
    print("RAG RESUME ANALYSIS")
    print("=" * 60)

    print("\nLoading dataset and job description...")
    data, job_description = load_inputs()

    candidate_id = input(
        "\nEnter candidate ID (example: SYN013): "
    ).strip().upper()

    matches = data[
        data["candidate_id"].astype(str).str.upper()
        == candidate_id
    ]

    if matches.empty:
        print(f"\nCandidate ID '{candidate_id}' was not found.")
        print("Please check the ID and run the script again.")
        return

    candidate = matches.iloc[0]

    print("\nLoading Sentence Transformer...")
    print("First-time model loading may take a little while.")

    model = SentenceTransformer(EMBEDDING_MODEL)

    print("\nRetrieving relevant resume evidence...")

    evidence = retrieve_evidence(
        model=model,
        resume_text=candidate["resume_text"],
        job_description=job_description
    )

    print("\n" + "=" * 60)
    print("RETRIEVED EVIDENCE")
    print("=" * 60)

    for number, item in enumerate(evidence, start=1):
        print(f"\nEvidence {number}")
        print(f"Similarity: {item['similarity']}%")
        print(f"Text: {item['text']}")


    # Run a deterministic keyword-presence audit
    audit_results = audit_requirements(
    candidate["resume_text"]
)

    print("\n" + "=" * 60)
    print("KEYWORD PRESENCE AUDIT")
    print("=" * 60)

    for requirement, result in audit_results.items():
        print(f"\n{requirement}: {result['status']}")

        if result["matched_terms"]:
            terms = ", ".join(result["matched_terms"])
            print(f"Matched terms: {terms}")

    print("\nGenerating explanation using local Ollama LLM...")
    print(f"Model: {OLLAMA_MODEL}")
    print("This may take a few minutes on your computer.")

    analysis = generate_analysis(
        candidate_id=candidate_id,
        role_category=str(candidate["category"]),
        job_description=job_description,
        evidence=evidence
    )

    
    verified_report = build_verified_report(
        candidate_id=candidate_id,
        role_category=str(candidate["category"]),
        evidence=evidence,
        audit_results=audit_results
    )

    print("\n" + "=" * 60)
    print("VERIFIED RESUME EVIDENCE REPORT")
    print("=" * 60)
    print(verified_report)


    print("\n" + "=" * 60)
    print("GENERATED CANDIDATE ANALYSIS")
    print("=" * 60)
    print(analysis)

    # Save the generated report in the existing research_data folder.
    output_path = BASE_DIR / f"{candidate_id}_rag_analysis.txt"

    report = (
        f"Candidate ID: {candidate_id}\n"
        f"Dataset Role Category: {candidate['category']}\n"
        f"LLM Model: {OLLAMA_MODEL}\n"
        "\n"
        "RETRIEVED EVIDENCE\n"
        "==================\n"
    )



    report += "\n\nKEYWORD PRESENCE AUDIT\n"
    report += "======================\n"

    for requirement, result in audit_results.items():
        report += f"{requirement}: {result['status']}"

        if result["matched_terms"]:
            terms = ", ".join(result["matched_terms"])
            report += f" (matched terms: {terms})"

        report += "\n"

    for number, item in enumerate(evidence, start=1):
        report += (
            f"\nEvidence {number}\n"
            f"Similarity: {item['similarity']}%\n"
            f"Text: {item['text']}\n"
        )

    report += (
        "\n\nGENERATED ANALYSIS\n"
        "==================\n"
        f"{analysis}\n"
    )

    output_path.write_text(report, encoding="utf-8")

    
    verified_path = (
        BASE_DIR / f"{candidate_id}_verified_rag_report.txt"
    )
    verified_path.write_text(
        verified_report,
        encoding="utf-8"
    )

    print("\nVerified report saved to:")
    print(verified_path)



    print("\nAnalysis saved to:")
    print(output_path)
    print("\nRAG retrieval and generation test completed.")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"\nERROR: {error}")
