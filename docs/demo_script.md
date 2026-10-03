# Demo Video Script

Target length: about 5 minutes. The permitted range is 2 to 8 minutes; only the
first 8 minutes will be reviewed. Keep a webcam view of your face visible while
also sharing the relevant GitHub and Streamlit screens. Speak precisely and do
not display the `.env` file or API key.

Before recording, test the OpenRouter call, close unrelated windows and
notifications, enlarge the browser text, and keep the repository, application,
and evaluation report open in separate tabs.

## 0 00 to 0 30 Introduction

Show the title slide or README.

Say:

> My project is a Resume JD Matching and Human Review Assistant. It compares one resume with one job description and helps a junior recruiter prioritise manual review. It does not automatically hire or reject candidates.

## 0 30 to 1 00 Design choice

Show the system flow in the README or briefly show the code files.

Say:

> I compare a transparent keyword baseline with one foundation-model call. I use deterministic code for privacy redaction and the baseline, and I use a rented model only for semantic comparison. I do not use RAG or an agent because the task requires no external knowledge or multi-step tool loop.

## 1 00 to 1 40 Privacy preview

Open the Streamlit application. Point to the sample job description and resume. Expand **Preview resume after local PII redaction**.

Say:

> Before the API call, the application removes the candidate name, email address and phone number locally. The user can inspect the redacted version. The demonstration uses synthetic data only.

## 1 40 to 2 15 Keyword baseline

Select **Keyword baseline** and click **Run keyword baseline**.

Say:

> The baseline counts skill overlap. It is cheap and explainable, but it does not understand context. For example, it can count the words SQL and Python even when a resume says the candidate has no experience with them.

## 2 15 to 3 00 AI comparison

Select **AI comparison** and click **Run AI comparison**.

Say:

> The model returns a validated structure containing a score, decision-support label, strengths, gaps and evidence. This case is a match because the resume demonstrates Python, SQL, Excel and dashboard experience. Missing or unclear requirements remain visible as gaps.

## 3 00 to 3 30 Abstention and safety

Replace the resume with an ambiguous example or show one of the stored manual-review cases.

Say:

> Scores from 50 to 69 produce Manual Review. This is an abstention, not a failed response. It prevents the system from presenting an uncertain result as a confident employment decision. The application explicitly prohibits automatic rejection.

## 3 30 to 4 20 Evaluation results

Open `results/evaluation_report.md` or the results table.

Say:

> I evaluated both systems on 40 held-out synthetic cases. The majority baseline achieved 50 percent strict accuracy, the keyword baseline achieved 25 percent, and the LLM achieved 75 percent. The LLM directly identified 17 of 20 qualified cases and sent the other three to manual review. It did not directly reject any qualified test case.

## 4 20 to 4 50 Limitations and close

Say:

> The dataset is synthetic, small and limited to one role, so this result does not establish production hiring validity or fairness. The contribution is a complete reproducible comparison with privacy checks, abstention and explicit human control. The system is suitable for coursework demonstration only.

End on the repository README and briefly show the commands used to install, test and run the project.
