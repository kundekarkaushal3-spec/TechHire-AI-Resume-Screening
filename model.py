import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from utils import extract_skills

# ----------------------------
# Load BERT Model
# ----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# Load Dataset
# ----------------------------

try:

    data = pd.read_csv("dataset.csv")

    dataset_embeddings = model.encode(
        data["resume_text"].tolist()
    )

except:

    data = pd.DataFrame(
        columns=["name","resume_text","category"]
    )

    dataset_embeddings = []

# ----------------------------
# Role Skill Dictionary
# ----------------------------
ROLE_SKILLS = {

    "AI/ML Engineer": [
        "python","machine learning","deep learning",
        "tensorflow","pytorch","nlp","opencv",
        "scikit-learn","ai","ml","bert"
    ],

    "Data Science":[
        "python","pandas","numpy","sql",
        "tableau","power bi","statistics",
        "data analysis","machine learning"
    ],

    "Frontend Developer":[
        "html","css","javascript",
        "react","angular","vue",
        "bootstrap","tailwind"
    ],

    "Backend Developer":[
        "java","spring","spring boot",
        "node","nodejs","express",
        "api","mysql","postgres","sql"
    ],

    "Full Stack Developer":[
        "react","node","express",
        "mongodb","mysql",
        "html","css","javascript"
    ],

    "DevOps Engineer":[
        "docker","kubernetes",
        "jenkins","aws","azure",
        "linux","git","github"
    ]
}

# ----------------------------
# Predict Role
# ----------------------------
def predict_category(text):

    if len(dataset_embeddings) == 0:

        return {
            "role":"Other",
            "dataset_similarity":0
        }

    resume_embedding = model.encode(text)

    similarity = cosine_similarity(

        [resume_embedding],

        dataset_embeddings

    )[0]

    best_index = similarity.argmax()

    predicted_role = data.iloc[
        best_index
    ]["category"]

    similarity_percent = round(

        similarity[best_index] * 100,

        2

    )

    return {

        "role": predicted_role,

        "dataset_similarity": similarity_percent

    }

# ----------------------------
# Semantic Ranking
# ----------------------------
def smart_rank(resumes, job_desc):

    job_embedding = model.encode(job_desc)

    job_skills = extract_skills(job_desc)

    results = []

    for resume in resumes:

        resume_embedding = model.encode(resume)

        # -------------------------
        # Semantic Score
        # -------------------------

        semantic = cosine_similarity(
            [resume_embedding],
            [job_embedding]
        )[0][0]

        semantic_score = round(
            semantic * 100,
            2
        )

        # -------------------------
        # Skill Score
        # -------------------------

        resume_skills = extract_skills(resume)

        matched = list(
            set(job_skills) &
            set(resume_skills)
        )

        missing = list(
            set(job_skills) -
            set(resume_skills)
        )

        if len(job_skills) == 0:

            skill_score = 0

        else:

            skill_score = (
                len(matched)
                /
                len(job_skills)
            ) * 100

        # -------------------------
        # Final Score
        # -------------------------

        final_score = (
            semantic_score * 0.70
            +
            skill_score * 0.30
        )

        final_score = min(
            round(final_score,2),
            100
        )

        results.append({

            "final": round(float(final_score), 2),

            "semantic": round(float(semantic_score), 2),

            "skill": round(float(skill_score), 2),

            "matched": matched,

            "missing": missing

        })

    return results