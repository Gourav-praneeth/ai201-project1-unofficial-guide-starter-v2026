# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Four of five leaves room for one miss without calling the system broken. My
corpus is 14 short guides, and a question like the Elder Ness flood count lives
in a single sentence inside the walking guide, which a chunk boundary could
easily split. Five of five would punish one unlucky split; three of five would
let retrieval fail on most of what I ask.

> **Revised in unit 2:** For at least 4 of my 5 test questions, at least one of
> the top 5 retrieved chunks contains the `expects` text from `questions.py`
> (case-insensitive).
>
> **Why revised:** "the retrieved chunks" did not say how many, and "contains the
> answer" had no check behind it. When I scored the before run I had to choose
> top 5 and the `expects` string myself. The target (4 of 5) is unchanged, and
> this revision was written after the run had come out 5/5, so it changes how the
> count is made, not how hard it is.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
All of them, because attribution is a property of the pipeline, not of the
question: the prompt and the output format ask for the source file every time.
If one answer comes back without a source, that is a bug to fix, not noise to
tolerate. It could only fail if the model ignores the format or the answer is a
refusal, and refusals are covered by criterion 3.


---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
Four of five, not five, because the out-of-scope questions share some words
with the guides in vocabulary (a question about "oil" or "loops" could still
land near a walking or transport chunk), which can pull a distance under the
cutoff. My in-corpus best distance was 0.341 against a
cutoff of 0.6 (to be tuned in Milestone 4); I expect a gap but have not yet
measured the out-of-scope side, so I will not promise a clean 5 of 5.


---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->



At least 4 of 5 randomly sampled chunks (from `python app.py chunks`) read as a
complete thought, with no sentence cut in half at either end, and no chunk is
shorter than 100 characters.

**Why this target:**
My guides are short (about 350-450 words) and organised under `##` headings, so
a chunk that stops mid-sentence is a visible defect, not a judgement call. The
first index produced a 24-character chunk, so the 100-character floor is
something the current chunking demonstrably fails. 4 of 5 rather than 5 of 5
because sampling five chunks by eye is a small sample and one oddly cut chunk
should not sink a working splitter.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->



For all 5 test questions, the source file the answer names is one of the
retrieved chunks that contains the `expects` text, not just any retrieved file.

**Why this target:**
Criterion 2 only checks that a source is named, and I care that it is the right
one. In my first test the answer cited `guide_eating.md` correctly, but the
retrieved list also included `guide_regional_transport.md`, which has nothing to
do with the question, so a name being present proves little. All 5 rather than
4 because the same fact often appears in two guides (a town guide and a
cross-cutting one), so a correct citation should be easy to get; a wrong one
means the model is naming files it didn't use.

> **Revised in unit 2:** For all 5 test questions, a file named in the answer is
> the source of at least one top-5 retrieved chunk that contains the `expects`
> text.
>
> **Why revised:** the original said the cited "source file ... is one of the
> retrieved chunks", but a file is not a chunk, so a stranger could not tell what
> to compare. The target (all 5) is unchanged, and I scored the before run with
> this reading.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
