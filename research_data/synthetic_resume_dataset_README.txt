SYNTHETIC RESUME PROFILES — DATASET NOTES

Purpose
-------
Initial controlled pilot dataset for research on resume screening and candidate ranking.

Origin and limitations
----------------------
All 100 profiles were synthetically generated for this research workflow. Names are fictional placeholders and are not intended to identify real people. No real resumes or personal records were used to create these profiles.

This is a pilot dataset, not a validated benchmark and not evidence of real-world hiring performance. Role categories are assigned during generation; they are not independent human relevance judgments for a particular job description. The dataset should be reviewed before experimental use.

Files
-----
synthetic_resume_profiles_100.csv: one row per synthetic candidate.

Columns
-------
candidate_id: synthetic unique ID.
name: fictional placeholder name.
resume_text: combined resume-like text for text-matching experiments.
category: synthetic target role category.
education: synthetic education detail.
experience_years: synthetic numeric experience value.
skills: semicolon-separated skills.
project_description: synthetic project summary.
training_or_certification: synthetic coursework/training entry.
data_origin: always 'synthetic'.

Category counts
---------------
category
AI/ML Engineer          15
Backend Developer       14
Cloud Engineer          14
Data Science            15
DevOps Engineer         14
Frontend Developer      14
Full Stack Developer    14

Important research notes
------------------------
1. Keep the original dataset.csv and application code unchanged.
2. Store this file in the separate research_data folder.
3. Before evaluation, prepare job descriptions and independently defined relevance judgments.
4. Avoid using candidate names as model features.
5. Do not treat the assigned category as ground truth for ranking relevance to every job.
6. Document dataset generation and all subsequent cleaning or transformations.
