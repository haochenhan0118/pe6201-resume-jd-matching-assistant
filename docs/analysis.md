# Resume JD Matching and Human Review Assistant

## Executive summary

I built a decision-support prototype for a junior recruiter comparing one resume with one Junior Data Analyst job description. The system combines a transparent keyword baseline, local removal of common personal identifiers, and one structured foundation-model call. On 40 held-out synthetic cases, the LLM matcher achieved 75% strict accuracy, compared with 50% for the majority baseline and 25% for keyword overlap. It directly matched 17 of 20 qualified cases and routed the other three to manual review, so it did not directly reject a qualified test case. The result supports the value of semantic comparison on this controlled dataset, but it does not establish real-world hiring validity. The main constraints are synthetic data, author-created labels, one job family, and limited fairness testing.

## Problem and intended difference

The target user is Mei, a junior technology recruiter who reviews 40 to 60 resumes in a working day using ordinary office tools. Literal keyword matching is attractive because it is cheap and easy to explain, but it treats a word as evidence even when the resume says “no SQL experience” or simply copies a vacancy’s skill list. It can also miss relevant paraphrases such as “maintained relational queries” when a role requests SQL.

The prototype changes the review experience in a limited but useful way. Instead of presenting only a similarity score, it separates strengths, gaps and supporting resume evidence, and it identifies ambiguous cases for human review. This could help a recruiter decide what to inspect next. I did not measure review time or hiring outcomes, so I cannot claim that the prototype reduces time-to-hire or improves workforce quality. Its demonstrated contribution is narrower: it produces a more discriminating review aid than literal overlap on the supplied test set.

I excluded bulk resume processing, applicant-tracking-system integration, PDF parsing, external databases, RAG, agents, model training and automatic rejection. This scope allowed me to complete and test one end-to-end path rather than present several unfinished features.

## Product design and technical reasoning

The user pastes one job description and one resume into a Streamlit interface. Deterministic regular expressions remove a likely name, email address and telephone number before any external request. The user can inspect the redacted version. The application then offers two comparisons.

The non-AI baseline extracts a fixed skill vocabulary and measures the proportion of job-description skills that also appear in the resume. It provides an auditable reference point and makes the semantic model earn its additional cost. The AI path sends the job description and redacted resume to `openai/gpt-4.1-mini` through OpenRouter. A fixed prompt treats both documents as untrusted data, prohibits protected-attribute inference, and requires evidence grounded in the resume. A Pydantic schema validates the returned score, label, strengths, gaps and evidence.

Scores of 70 or above return `MATCH`, scores below 50 return `NO_MATCH`, and ambiguous cases return `MANUAL_REVIEW`. I treat manual review as abstention rather than a correct prediction. This prevents the model from improving its apparent accuracy by declining every difficult case. The interface, orchestration, prompt, baseline, redaction, dataset and evaluation are owned components; model inference is rented. One representative request used 383 input tokens and 71 output tokens and cost US$0.0002668. A single hosted call was therefore more proportionate than training or serving a model for this prototype.

RAG would add retrieval infrastructure without a document collection. An agent would add latency and new failure modes to a one-step comparison. I therefore excluded both.

## Data and evaluation method

I generated 60 synthetic resume and job-description pairs for one Junior Data Analyst role. Twenty cases form the development set and 40 form the held-out test set. The test set is balanced between `MATCH` and `NO_MATCH` and includes standard cases, semantic paraphrases, missing evidence, negated skills, keyword stuffing and one instruction-injection attempt. Scenario rules fix each label before either system runs. The generation script, prompt, cases and predictions are checked into the repository.

I compare three systems on the same 40 cases: an always-majority baseline, keyword overlap and the LLM matcher. Strict accuracy counts `MANUAL_REVIEW` as incorrect. Qualified-candidate recall measures how many true matches receive a direct match. Manual-review rate measures workload passed to a person. Selective accuracy measures accuracy only where the system gives a definite answer. These measures expose the trade-off between automation and caution better than a single accuracy figure.

The evaluation remains vulnerable to author bias because I designed the scenarios, label rules and system. Repeated templates may make the test easier than real applications, and the balanced distribution is unlike many recruitment pipelines. The results are an internal functional evaluation, not an estimate of deployment performance.

## Outcomes and performance critique

The majority baseline reached 50% strict accuracy because the test set is balanced. Its 100% qualified recall is operationally misleading: it labels every case as a match and therefore passes every unsuitable case to the recruiter. The keyword baseline reached 25% strict accuracy, 20% qualified recall, a 20% manual-review rate and 31.2% selective accuracy. It performed poorly because negation and copied terms were counted as positive evidence.

The LLM matcher reached 75% strict accuracy, 85% qualified recall and a 25% manual-review rate. It answered 30 cases definitively and achieved 100% selective accuracy on those cases. It directly identified 17 of 20 qualified cases and sent the remaining three to manual review. It also routed the prompt-injection case to manual review.

The strongest result is the absence of a direct false rejection among qualified test cases when manual review is treated as a safe route. The main weakness is coverage: one quarter of cases still require a person. That is acceptable for decision support, but it limits automation. The 100% selective accuracy is also unstable because it is based on only 30 answered synthetic cases. A few new failures would move it sharply. The 75% headline accuracy meets the revised provisional target, but it falls below the original 82% proposal target. I report the observed result rather than hiding this difference.

## Difficulties and tuning decisions

The first difficulty was making model output dependable enough for an application. Free-form responses varied in labels and formatting, so I used a fixed schema and validation. The second was handling uncertainty. A binary threshold produced confident-looking answers for incomplete resumes, so I introduced the 50-to-69 manual-review band and reported its cost as a separate metric. The third was privacy. Sending raw resumes would conflict with the project’s responsible-use claim, so redaction runs locally and appears in the interface before the model call.

I changed the provider path from a direct OpenAI configuration to OpenRouter while retaining the same structured comparison. Provider-specific setup remains inside `matcher.py`, so the interface and evaluation do not depend on the endpoint. One call and a concise schema reduce cost and latency. I did not conduct a formal latency benchmark, threshold sweep or multi-model comparison.

## Risks rough edges and future path

The most serious failure is a qualified candidate receiving a low score without detection. Abstention, evidence display and the prohibition on automatic rejection reduce this risk, but they do not eliminate bias or unsupported reasoning. Regular-expression redaction can miss unusual identifiers. The application has no authentication, audit log or demographic subgroup tests, which makes it unsuitable for real hiring.

The next useful step is an externally labelled pilot dataset. Two recruiters should independently label de-identified resume-role pairs, resolve disagreements, and keep the final test set hidden during prompt development. I would then report precision, recall, false-rejection rate and manual-review workload by case type and relevant subgroups. A threshold sweep could show whether higher coverage is possible without introducing direct false rejections. Only after that evidence would PDF ingestion, stronger redaction, role-specific criteria, monitoring and applicant-tracking-system integration be worth considering.

## Conclusion

The project demonstrates a complete, reproducible comparison between literal matching and a constrained foundation-model component. Semantic matching performed better on the synthetic test, while abstention preserved human control over ambiguous cases. The result is useful as coursework evidence and as a basis for a better-labelled pilot. It is not evidence that the system should make employment decisions.
