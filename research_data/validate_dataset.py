
from pathlib import Path
import pandas as pd

# Locate the CSV in the same folder as this script
BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "synthetic_resume_profiles_100.csv"
REPORT_PATH = BASE_DIR / "dataset_validation_report.txt"

print("=" * 60)
print("SYNTHETIC RESUME DATASET VALIDATION")
print("=" * 60)

# Check whether the dataset exists
if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}\n"
        "Check that the CSV and this script are in research_data."
    )

# Read the dataset without changing the original file
df = pd.read_csv(DATASET_PATH)

required_columns = [
    "candidate_id",
    "name",
    "resume_text",
    "category",
    "education",
    "experience_years",
    "skills",
    "project_description",
    "training_or_certification",
    "data_origin",
]

issues = []
report_lines = []

def add_line(message=""):
    print(message)
    report_lines.append(str(message))

add_line(f"Dataset file: {DATASET_PATH.name}")
add_line(f"Total rows: {len(df)}")
add_line(f"Total columns: {len(df.columns)}")
add_line()

# 1. Check required columns
missing_columns = [
    col for col in required_columns if col not in df.columns
]

add_line("1. REQUIRED COLUMN CHECK")
if missing_columns:
    add_line(f"FAIL: Missing columns: {missing_columns}")
    issues.append(f"Missing columns: {missing_columns}")
else:
    add_line("PASS: All 10 required columns are present.")

# Continue detailed checks only if required columns exist
if not missing_columns:

    # 2. Check row count
    add_line()
    add_line("2. ROW COUNT CHECK")
    if len(df) == 100:
        add_line("PASS: Exactly 100 profiles found.")
    else:
        add_line(f"WARNING: Expected 100 profiles, found {len(df)}.")
        issues.append(f"Unexpected row count: {len(df)}")

    # 3. Check missing values
    add_line()
    add_line("3. MISSING VALUES CHECK")
    missing_counts = df[required_columns].isna().sum()
    if missing_counts.sum() == 0:
        add_line("PASS: No missing values in required columns.")
    else:
        add_line("Missing values by column:")
        for col, count in missing_counts.items():
            if count > 0:
                add_line(f"  {col}: {count}")
                issues.append(f"{col} has {count} missing values")

    # Also check blank strings
    blank_counts = {}
    for col in required_columns:
        blank_count = (
            df[col].astype("string").str.strip().eq("").sum()
        )
        if blank_count:
            blank_counts[col] = int(blank_count)

    add_line()
    add_line("4. BLANK STRING CHECK")
    if not blank_counts:
        add_line("PASS: No blank strings in required columns.")
    else:
        for col, count in blank_counts.items():
            add_line(f"WARNING: {col}: {count} blank values")
            issues.append(f"{col} has {count} blank values")

    # 5. Unique candidate IDs
    add_line()
    add_line("5. CANDIDATE ID CHECK")
    duplicate_ids = int(df["candidate_id"].duplicated().sum())
    if duplicate_ids == 0:
        add_line("PASS: All candidate IDs are unique.")
    else:
        add_line(f"FAIL: {duplicate_ids} duplicate candidate IDs.")
        issues.append(f"{duplicate_ids} duplicate candidate IDs")

    # 6. Duplicate resume text
    add_line()
    add_line("6. DUPLICATE RESUME TEXT CHECK")
    duplicate_resumes = int(
        df["resume_text"].duplicated().sum()
    )
    if duplicate_resumes == 0:
        add_line("PASS: No exact duplicate resume texts.")
    else:
        add_line(
            f"WARNING: {duplicate_resumes} exact duplicate resume texts."
        )
        issues.append(f"{duplicate_resumes} duplicate resume texts")

    # 7. Role category distribution
    add_line()
    add_line("7. CATEGORY DISTRIBUTION")
    category_counts = df["category"].value_counts(dropna=False)
    for category, count in category_counts.items():
        add_line(f"  {category}: {count}")

    add_line(f"Total distinct categories: {df['category'].nunique()}")

    if df["category"].nunique() == 7:
        add_line("PASS: Seven role categories found.")
    else:
        add_line("WARNING: Expected seven role categories.")
        issues.append(
            f"Found {df['category'].nunique()} categories, expected 7"
        )

    # 8. Data origin check
    add_line()
    add_line("8. DATA ORIGIN CHECK")
    origins = df["data_origin"].astype("string").str.strip().unique()
    add_line(f"Origin values: {list(origins)}")

    if df["data_origin"].astype("string").str.strip().eq("synthetic").all():
        add_line("PASS: Every record is marked synthetic.")
    else:
        add_line("WARNING: Some records are not marked synthetic.")
        issues.append("Unexpected data_origin value")

    # 9. Experience range
    add_line()
    add_line("9. EXPERIENCE RANGE CHECK")
    experience = pd.to_numeric(
        df["experience_years"], errors="coerce"
    )
    invalid_experience = (
        experience.isna()
        | (experience < 0)
        | (experience > 50)
    )

    if not invalid_experience.any():
        add_line(
            f"PASS: Experience values range from "
            f"{experience.min()} to {experience.max()} years."
        )
    else:
        add_line(
            f"WARNING: {int(invalid_experience.sum())} "
            "invalid experience values."
        )
        issues.append("Invalid experience values")

# 10. Final summary
add_line()
add_line("=" * 60)
add_line("VALIDATION SUMMARY")
add_line("=" * 60)

if not issues:
    add_line("No issues detected by these automated checks.")
    add_line(
        "Note: This does not prove resume realism or research validity."
    )
else:
    add_line(f"Potential issues detected: {len(issues)}")
    for issue in issues:
        add_line(f"- {issue}")

# Save report separately; the CSV remains unchanged
REPORT_PATH.write_text(
    "\n".join(report_lines) + "\n",
    encoding="utf-8"
)

print(f"\nReport saved to: {REPORT_PATH}")
print("Original dataset was not modified.")
