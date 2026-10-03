# Project Problem Statement

**Name:** Han Haochen

**Section:** C

**Working title:** Resume JD Matching and Human Review Assistant

## Problem

A junior recruiter may review 40 to 60 resumes in one day. A simple keyword
search is fast, but it can miss candidates who describe the same skill in
different words. It can also give a high score to a resume that copies skill
names without showing real experience. My project is a small tool that compares
one resume with one job description and helps the recruiter decide what to
review next. It does not make hiring or rejection decisions.

## User and output

The main user is Mei, a junior recruiter with no specialist AI knowledge. She
pastes a Junior Data Analyst job description and a resume into a Streamlit
page. The tool returns a score, a MATCH, NO_MATCH or MANUAL_REVIEW label, and
short lists of strengths, gaps and evidence. Unclear cases are sent to manual
review.

## Approach

I compare two methods. The first is a keyword baseline based on a fixed list of
skills. The second uses GPT-4.1-mini through OpenRouter for semantic comparison.
Before the model call, Python code removes a likely name, email address and
phone number. The model returns a fixed structure that the program validates.
I did not use RAG or an agent because the task only compares two supplied texts.

I built the interface, baseline, redaction, prompt, dataset and evaluation code.
I rent the model call through OpenRouter. One sample call cost about
US$0.00027, so using a hosted model was more practical than training my own.

## Data and success measure

I generated 60 synthetic resume and job-description pairs for one Junior Data
Analyst role. Twenty were used for development and 40 were kept for testing.
The test set contains equal numbers of MATCH and NO_MATCH cases. The main target
is at least 75% strict accuracy. MANUAL_REVIEW counts as incorrect for this
metric. I also report qualified-candidate recall and manual-review rate.

## Scope and risks

The first version accepts pasted text only. It excludes PDF parsing, bulk
processing, ATS integration and automatic rejection. The main risks are privacy
leaks, unfair scoring and unsupported model claims. I reduce these risks through
local redaction, evidence display and human review. These controls are not
strong enough for real hiring, so the project is only for coursework and
demonstration.
