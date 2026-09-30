# Project Problem Statement

**Name:** Han Haochen  
**Section:** C  
**Working title:** Resume JD Matching and Human Review Assistant

## 1 Working title

Resume JD Matching and Human Review Assistant

## 2 The problem and why it matters

In the target scenario, a junior recruiter in a technology company reviews 40 to 60 resumes in a working day. Literal keyword screening can miss candidates who describe relevant experience with different wording, while copied skill terms can make an unsuitable resume appear relevant. I will build a decision-support prototype that helps the recruiter prioritise manual review without making hiring or rejection decisions. Bulk processing, ATS integration and automatic rejection are out of scope.

## 3 Primary user and domain

The primary user is Mei, a junior technology recruiter who reviews resumes using standard office software and has no specialist AI knowledge. She uses the system after receiving applications for a Junior Data Analyst role. The output helps her decide which resume to examine next and which cases need closer human review. The domain is corporate recruitment and human resources.

## 4 Why AI and which kind

My non-AI baseline counts overlaps between a fixed list of skills in the job description and resume. This is transparent but cannot reliably interpret synonyms, negation or whether a listed skill is supported by experience. I use one rented foundation model, `openai/gpt-4.1-mini`, through OpenRouter with a structured prompt and validated output schema. Deterministic code removes common direct identifiers and calculates the keyword baseline. I do not use RAG or an agent because the task compares two supplied texts and needs neither external documents nor a multi-step tool loop.

## 5 Proposed approach and build versus buy

I own the Streamlit interface, Python orchestration, redaction rules, keyword baseline, prompt, abstention thresholds, synthetic dataset and evaluation scripts. I rent model inference through OpenRouter. A representative request used 383 input tokens and 71 output tokens and cost approximately US$0.00027. This makes hosted inference cheaper and faster to deploy than training or serving a model for this small prototype. Streamlit is code rather than low-code; I chose it because one Python application is sufficient for the required demonstration.

## 6 Data

I generated 60 synthetic resume and job-description pairs for one Junior Data Analyst role. Twenty cases form the development set and 40 form a held-out test set. The test set is balanced between `MATCH` and `NO_MATCH` and includes paraphrases, missing evidence, keyword stuffing and a prompt-injection case. Labels are fixed by scenario rules before either system runs. The generation script and CSV are committed so the dataset is reproducible. No real applicant data is required or redistributed.

## 7 Success metric and evaluation

The primary metric is strict accuracy, where `MANUAL_REVIEW` is counted as not automatically correct. I compare the LLM with a keyword baseline and a majority-class baseline on the same 40 held-out cases. I also report qualified-candidate recall, manual-review rate and accuracy on cases where the system gives a definite answer. The provisional success target is at least 75% strict accuracy and no direct `NO_MATCH` decision for a ground-truth qualified case.

## 8 Risks limitations and responsible use

- **Personal data exposure:** common names, email addresses and phone numbers are removed locally before the API call; the demonstration uses only synthetic data.
- **Qualified candidate ranked too low:** ambiguous scores return `MANUAL_REVIEW`, and the interface prohibits automatic rejection.
- **Unsupported model claims:** every result contains short evidence grounded in the resume.
- **Keyword or prompt manipulation:** the prompt treats both documents as untrusted data, and the test set includes keyword-stuffed and instruction-injection cases.
- **Bias or unfair inference:** the prompt prohibits protected-attribute inference, but the small synthetic test cannot establish real-world fairness.

The intended use is classroom demonstration and first-pass review assistance. The explicit non-use is automated hiring, rejection, ranking of real applicants without human confirmation, or inference of protected characteristics.

## 9 Smallest first version

The smallest version accepts one pasted job description and one pasted resume, removes common direct identifiers, makes one structured model call and displays a score, a decision-support label, strengths, gaps and supporting evidence. It works when both the keyword baseline and AI comparison run from the interface and reproduce the documented result format on synthetic inputs.

