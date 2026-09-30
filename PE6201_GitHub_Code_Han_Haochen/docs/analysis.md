# Resume JD Matching and Human Review Assistant Analysis

## Problem and significance

My project addresses a narrow recruitment task: helping a junior recruiter compare one resume with one job description before manual review. Literal keyword matching is attractive because it is cheap and transparent, but it treats every occurrence of a word as positive evidence. It can therefore miss a relevant synonym and can also reward a resume that says “no SQL experience” or simply copies the vacancy’s skill list. My system tests whether a foundation model can make a more useful semantic comparison while retaining deterministic privacy checks and human control.

The primary user is a junior recruiter reviewing applications for a Junior Data Analyst position. The prototype is not an applicant tracking system and does not make employment decisions. Its purpose is to provide a consistent summary that helps the recruiter decide what to inspect next. I deliberately exclude bulk processing, PDF parsing, external databases, RAG, agents, model training and automatic rejection. This limited scope makes it possible to implement and evaluate the complete path rather than demonstrating an unfinished collection of features.

## Design and implementation

The application is built in Python with a Streamlit interface. A user pastes a job description and resume. Before any external call, deterministic regular expressions remove common names, email addresses and telephone numbers. The interface lets the user preview the redacted resume. The semantic matcher then sends the job description and redacted resume to `openai/gpt-4.1-mini` through OpenRouter.

The model receives a fixed system prompt that treats both documents as untrusted data, prohibits protected-attribute inference, and requires decisions to be based only on evidence in the supplied text. Structured Outputs constrain the response to a validated schema containing a label, score, strengths, gaps and evidence. Scores of 70 or above map to `MATCH`, scores below 50 map to `NO_MATCH`, and ambiguous cases map to `MANUAL_REVIEW`. The last category is an abstention rather than a prediction.

The non-AI baseline uses a fixed vocabulary and calculates the proportion of job-description skills also mentioned in the resume. It is intentionally simple, explainable and reproducible. The model, API access and infrastructure are rented; I own the interface, orchestration, prompt, baseline, redaction, dataset and evaluation. A representative structured request consumed 383 input tokens and 71 output tokens and cost about US$0.00027 through OpenRouter. Training or hosting a dedicated model would therefore add complexity without a clear benefit for this prototype.

## Data and evaluation

I created 60 synthetic pairs for one Junior Data Analyst role. Twenty are development cases and 40 form the held-out test set. The test set contains 20 `MATCH` and 20 `NO_MATCH` labels and mixes standard, hard and adversarial cases. Hard negatives mention relevant skills without evidence of use. The adversarial case asks the model to ignore its instructions and award a perfect score. Labels are assigned from scenario rules before evaluation, and the generation script is included in the repository.

I compare three systems on the same test set: a majority-class baseline, the keyword baseline and the LLM matcher. Strict accuracy treats an abstention as not automatically correct. I also measure qualified-candidate recall, manual-review rate and selective accuracy, which is accuracy only on cases where the system gives a definite answer.

The majority baseline achieved 50% strict accuracy. Its 100% qualified-candidate recall is misleading because it labelled every case `MATCH`. The keyword baseline achieved 25% strict accuracy, 20% qualified recall and a 20% manual-review rate. Its largest failure was counting a negated or copied skill term as evidence.

The LLM matcher achieved 75% strict accuracy, 85% qualified recall and a 25% manual-review rate. On the 30 cases where it gave a definite answer, selective accuracy was 100%. It directly identified 17 of 20 qualified cases and sent the other three to manual review; it did not label any qualified test case `NO_MATCH`. It also sent the prompt-injection case to manual review. These results meet the provisional accuracy target and show a clear advantage over literal overlap on this dataset.

## Risks and limitations

The most important risk is a qualified candidate being incorrectly ranked low. The prototype reduces this risk through abstention, evidence display and an explicit prohibition on automatic rejection. Privacy risk is reduced by local redaction and synthetic evaluation data. Prompt manipulation is addressed by treating resume content as data rather than instructions. The interface also states that the output supports, but never replaces, human judgment.

The evaluation has substantial limitations. The dataset is synthetic, small and limited to one role. Scenario templates repeat across cases, labels were not produced by independent recruiters, and the balanced class distribution does not represent a real applicant population. Regular-expression redaction is not a production privacy control, and the experiment does not establish fairness across demographic groups. A production study would require authorised real data, independent expert labels, subgroup testing, stronger privacy controls and ongoing error monitoring.

## Conclusion

The project demonstrates a complete and reproducible AI workflow: a defined user problem, a transparent non-AI baseline, a justified model choice, a running interface, fixed test data, measurable abstention and documented limitations. Within the synthetic test, semantic comparison substantially outperformed keyword overlap while preserving human review for ambiguous cases. The appropriate conclusion is not that the system is ready for hiring, but that a small foundation-model component can improve resume-review assistance when its scope and decision authority are tightly constrained.

