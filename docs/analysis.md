# Resume JD Matching and Human Review Assistant

## What I built

I built a Streamlit prototype that compares one resume with one Junior Data
Analyst job description. My aim was not to replace a recruiter. I wanted to test
whether an AI comparison could give a more useful first review than simple
keyword matching.

The page has two paths. The keyword baseline looks for a fixed list of skills
such as Python, SQL and Excel. It is easy to understand, but it cannot tell the
difference between real experience and a sentence such as “no SQL experience.”
The AI path uses GPT-4.1-mini through OpenRouter. It returns a score, label,
strengths, gaps and evidence taken from the resume.

Before the API call, the program removes a likely name, email address and phone
number. The user can check the redacted text. Scores of 70 or above return
MATCH, scores below 50 return NO_MATCH, and scores from 50 to 69 return
MANUAL_REVIEW. I used this middle band because an uncertain answer should be
checked by a person.

## Data and evaluation

I created 60 synthetic cases for one job role. I used 20 while developing the
project and kept 40 for the final test. The test set has 20 MATCH and 20
NO_MATCH cases. It includes normal examples, different wording, missing
evidence, negated skills, copied keywords and one prompt-injection attempt.
Labels were fixed before either system was tested.

I compared three systems on the same 40 cases. The majority baseline always
predicts MATCH. The keyword baseline uses literal skill overlap. The LLM matcher
uses the structured model response. My main measure is strict accuracy, where a
MANUAL_REVIEW result is counted as incorrect. I also measured how many
qualified candidates received a direct match and how often a person still had
to review the case.

The majority baseline reached 50% accuracy because the test set is balanced.
The keyword baseline reached only 25%. It often treated a skill word as proof
even when the surrounding sentence showed no experience. The LLM matcher
reached 75% strict accuracy and 85% qualified-candidate recall. It sent 10 of
the 40 cases to manual review.

The model directly matched 17 of the 20 qualified cases. The other three went
to manual review, so no qualified test case received a direct NO_MATCH result.
The model was correct on all 30 cases where it gave a definite answer. However,
that 100% figure is based on a small synthetic sample and should not be treated
as real hiring performance.

## What worked and what did not

The main improvement over keyword matching was context. The AI was better at
handling paraphrases, negation and copied skill lists. Showing strengths, gaps
and evidence also made the result easier to check than a single similarity
score. The 75% accuracy met my final target, but it did not meet the original
82% target in my proposal. I kept both figures in the project documentation
instead of hiding the earlier target.

There are also clear weaknesses. A quarter of the test cases still needed
manual review. This is acceptable for a support tool, but it limits how much
work the system can save. I also did not measure review time, model latency or
real hiring outcomes. The project shows that the workflow runs and that the AI
performed better on my test set. It does not show that the tool improves hiring
quality.

## Difficulties and changes

One problem was inconsistent model output. Early free-form answers used
different labels and formats, so I changed the prompt and added a fixed output
schema. Another problem was uncertainty. A simple yes-or-no threshold made weak
cases look too confident, so I added the manual-review range and reported it as
a separate metric.

I also changed the provider setup to OpenRouter. The provider-specific code is
kept inside the matcher module, so the main interface did not need to change.
Local redaction was added because sending an unchanged resume would not match
the responsible-use goal of the project.

## Limits and next step

The evaluation is small and was designed by me. The same person created the
scenarios, labels and system, which may make the test easier than an independent
evaluation. All resumes are synthetic, the cases cover only one job role, and
the balanced test set is unlike many real applicant groups. The redaction rules
can also miss unusual personal details. I did not test fairness across
demographic groups.

The next useful step would be a small de-identified dataset labelled separately
by two recruiters. They could compare labels and resolve disagreements before
the final test. I would then check false-rejection rate, recall and manual-review
workload across different case types. Until that work is done, the prototype
should remain a classroom demonstration with a human making every final
decision.
