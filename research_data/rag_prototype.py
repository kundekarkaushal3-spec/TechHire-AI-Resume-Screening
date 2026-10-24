
from pathlib import Path

import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. Define file paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "synthetic_resume_profiles_100.csv"
JOB_PATH = BASE_DIR / "test_job_description.txt"


# --------------------------------------------------
# 2. Load the existing Transformer embedding model
# --------------------------------------------------

print("Loading Sentence Transformer model...")

model = SentenceTransformer("all-MiniLM-L6-v2")


# --------------------------------------------------
# 3. Load synthetic resumes and job description
# --------------------------------------------------

if not DATASET_PATH.exists():
    raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

if not JOB_PATH.exists():
    raise FileNotFoundError(f"Job description not found: {JOB_PATH}")

df = pd.read_csv(DATASET_PATH)
job_description = JOB_PATH.read_text(encoding="utf-8")


# --------------------------------------------------
# 4. Select one candidate to inspect
# --------------------------------------------------

candidate_id = input(
    "Enter candidate ID (example: SYN013): "
).strip().upper()

candidate_rows = df[df["candidate_id"] == candidate_id]

if candidate_rows.empty:
    raise ValueError(f"Candidate ID not found: {candidate_id}")

candidate = candidate_rows.iloc[0]

resume_text = candidate["resume_text"]


# --------------------------------------------------
# 5. Split the resume into evidence passages
# --------------------------------------------------

passages = [
    part.strip()
    for part in resume_text.split(".")
    if part.strip()
]

if not passages:
    raise ValueError("No resume passages were found.")


# --------------------------------------------------
# 6. Encode job description and resume passages
# --------------------------------------------------

print("\nEncoding resume evidence and job description...")

job_embedding = model.encode(
    job_description,
    convert_to_numpy=True
)

passage_embeddings = model.encode(
    passages,
    convert_to_numpy=True
)


# --------------------------------------------------
# 7. Retrieve the most relevant passages
# --------------------------------------------------

similarities = cosine_similarity(
    passage_embeddings,
    job_embedding.reshape(1, -1)
).flatten()

ranked_indices = similarities.argsort()[::-1]

top_k = min(3, len(passages))

print("\n" + "=" * 60)
print("RESUME EVIDENCE RETRIEVAL RESULTS")
print("=" * 60)

print(f"Candidate ID: {candidate['candidate_id']}")
print(f"Role category: {candidate['category']}")

for rank, index in enumerate(ranked_indices[:top_k], start=1):
    print(f"\nEvidence {rank}")
    print(f"Similarity: {similarities[index] * 100:.2f}%")
    print(f"Text: {passages[index]}")

print("\n" + "=" * 60)
print("Retrieval test completed.")
print("No dataset or application files were modified.")
