import PyPDF2
import re
import nltk
import string
from nltk.corpus import stopwords

# Download stopwords only once
try:
    stop_words = set(stopwords.words("english"))
except:
    nltk.download("stopwords")
    stop_words = set(stopwords.words("english"))


# --------------------------------------------------
# PDF TEXT EXTRACTION
# --------------------------------------------------

def extract_text_from_pdf(file):

    reader = PyPDF2.PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + " "

    return text


# --------------------------------------------------
# TEXT PREPROCESSING
# --------------------------------------------------

def preprocess_text(text):

    text = text.lower()

    text = text.translate(
        str.maketrans("", "", string.punctuation)
    )

    words = text.split()

    words = [
        word
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)


# --------------------------------------------------
# NORMALIZE COMMON SKILLS
# --------------------------------------------------

NORMALIZATION = {

    "ml":"machine learning",
    "ai":"artificial intelligence",
    "js":"javascript",
    "nodejs":"node",
    "mongodb":"mongodb",
    "postgres":"postgresql",
    "reactjs":"react",
    "expressjs":"express",

    "mern stack":"mern",
    "mean stack":"mean",

    "dl":"deep learning",

}


# --------------------------------------------------
# SKILL DATABASE
# --------------------------------------------------

SKILL_DATABASE = [

    # Languages

    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",

    # Frontend

    "html",
    "css",
    "react",
    "angular",
    "vue",
    "bootstrap",
    "tailwind",

    # Backend

    "node",
    "express",
    "spring",
    "spring boot",
    "django",
    "flask",

    # Database

    "mysql",
    "mongodb",
    "postgresql",
    "sqlite",
    "oracle",
    "sql",

    # AI

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "nlp",
    "computer vision",

    "tensorflow",
    "keras",
    "pytorch",

    "opencv",

    "scikit-learn",

    "bert",

    # Data Science

    "numpy",

    "pandas",

    "matplotlib",

    "seaborn",

    "power bi",

    "tableau",

    # Cloud

    "aws",

    "azure",

    "gcp",

    # DevOps

    "docker",

    "kubernetes",

    "jenkins",

    "git",

    "github",

    "linux",

    # Others

    "api",

    "rest api",

    "mern",

    "mean",

    "full stack"

]


# --------------------------------------------------
# EXTRACT SKILLS
# --------------------------------------------------

def extract_skills(text):

    text = preprocess_text(text)

    found = []

    # Normalize text

    for key, value in NORMALIZATION.items():

        text = text.replace(key, value)

    for skill in SKILL_DATABASE:

        if re.search(r"\b" + re.escape(skill) + r"\b", text):

            found.append(skill)

    # MERN detection

    if (
        "mongodb" in found and
        "express" in found and
        "react" in found and
        "node" in found
    ):

        found.append("mern")

    # Full Stack detection

    if (
        "html" in found and
        "css" in found and
        "javascript" in found and
        "react" in found and
        "node" in found
    ):

        found.append("full stack")

    return sorted(list(set(found)))