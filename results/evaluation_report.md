# Evaluation Results

## Scope

The evaluation uses 40 held-out synthetic resume-job-description pairs for one
Junior Data Analyst role. The dataset is balanced: 20 `MATCH` and 20 `NO_MATCH`
cases. It includes straightforward cases, semantic paraphrases, keyword-stuffed
resumes without supporting evidence, and one prompt-injection case.

The labels were assigned by deterministic scenario rules before either system
was run. Twenty additional cases are kept as development data and are excluded
from the reported results.

## Results

| System | Strict accuracy | Qualified recall | Manual-review rate | Accuracy when answered |
|---|---:|---:|---:|---:|
| Majority-class baseline | 50.0% | 100.0% | 0.0% | 50.0% |
| Keyword baseline | 25.0% | 20.0% | 20.0% | 31.2% |
| LLM matcher | 75.0% | 85.0% | 25.0% | 100.0% |

Strict accuracy counts `MANUAL_REVIEW` as not automatically correct. Accuracy
when answered excludes those abstained cases. Qualified recall measures the
share of true `MATCH` cases that received a direct `MATCH` result.

The majority baseline obtains 100% qualified recall only because it labels every
case as `MATCH`; its precision and overall accuracy are therefore poor. This is
not a useful operational strategy, but it is included to show why accuracy and
recall must be interpreted together.

## Main finding

The LLM matcher exceeded both baselines on strict accuracy. It directly
identified 17 of 20 qualified cases and sent the other three to manual review.
It did not label any qualified case as `NO_MATCH`, producing a safe-review recall
of 100% in this synthetic test.

A representative structured request used 383 input tokens and 71 output tokens.
OpenRouter reported a cost of US$0.0002668 for that request. This is a sample
rather than a full production cost estimate because resume length and output
length vary.

The keyword method struggled with synonyms and negation. In particular, it
treated statements such as "no SQL experience" and skill terms copied from a
vacancy as positive evidence. The LLM was better able to distinguish a skill
mention from evidence that the candidate had used the skill.

## Abstention and adversarial case

The LLM returned `MANUAL_REVIEW` for 10 of 40 cases. Seven of those cases were
hard negatives with copied skill terms but insufficient supporting experience.
The prompt-injection resume was also sent to manual review rather than being
marked as a perfect match.

## Limitations

- All cases are synthetic and cover only one Junior Data Analyst role.
- The same scenario templates repeat across some cases, so the results do not
  establish real-world hiring performance.
- Labels were created by the project author rather than independent recruiters.
- The test is balanced and does not represent a real applicant population.
- The redaction and matching systems are course prototypes, not production
  privacy or hiring controls.

The system is therefore suitable only as a demonstration of a reproducible
evaluation workflow. It must not be used to automatically reject or hire a real
person.
