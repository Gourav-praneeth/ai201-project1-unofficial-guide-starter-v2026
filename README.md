# The Unofficial Guide

Gourav Bhimavarapu — corpus: `city_guides`

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

The Unofficial Guide answers questions about a fictional region of nine towns
(Brightwater, Halden Bay, Kestrelford and others), using 14 travel guides: one
per town plus five that cut across them (eating, seasons, walking, transport,
accessibility). It answers specific practical questions, such as which street
has cheaper food, how often a bus runs, or which walks flood at high tide. Each
answer is built only from the retrieved guide sections and names the file it
came from. When the guides don't cover a question, a relevance check refuses it
before the model is called.

## Chunking Strategy

**Chunk size:** one chunk per `##` section; no fixed character count. Sections under 150 characters are merged into the next one, and sections over 1,000 are split on paragraph breaks. Result: 84 chunks from 14 guides, 354 characters on average (shortest 188, longest 883).
**Overlap:** none (0).

I picked these after reading the guides in Milestone 1. Each is about 350-450
words under `##` headings such as "Eat and drink" and "Getting there", and each
section is one self-contained topic. The starter's 800-character windows cut
straight through those sections (51 chunks, shortest 24 characters, with a
sentence like "Everything closes by 9pm" landing in a chunk that no longer said
which town it was about). The facts I test for are one sentence inside a
section, so keeping the section whole keeps the sentence next to its context.

There is no overlap because a section never continues into the next. The cut
points are already topic boundaries, so there is nothing to carry across them.
Overlap would only repeat text and make neighbouring chunks match the same
question.

Each chunk is prefixed with "<guide title> — <section heading>", for example
"Halden Bay — Eat and drink". Many sections never name their town ("Prices on
the harbour front are roughly double..."), so without the prefix the chunk
cannot say what it is about.

I changed my mind once. My first version made the intro paragraph before the
first heading its own chunk. The Halden Bay one came out at 188 characters and
said only that it is a fishing port, which answers nothing. Intros are now
joined to the first section.

Chunks are produced by `chunker.py::split_documents`.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `guide_accessibility.md` — produced by: `chunker.py::split_documents`

```
Getting around the region with limited mobility — Practical

The nearest full hospital is in Marchwood. Brightwater has a hospital;
Kestrelford, Halden Bay, Corry Vale, Givens Mill and Elder Ness have minor
injuries units with limited hours or nothing at all.

Mobile coverage is good in the town centres and patchy on the outskirts, and
genuinely absent in parts of Corry Vale.
```

**Chunk 2** — source: `guide_eating.md` — produced by: `chunker.py::split_documents`

```
Eating across the region — Markets

Kestrelford's Saturday market has run since the 1400s and is the region's best,
though much reduced from November to February. Brightwater's Tuesday market
sets up at 7am in the square and is finished by 1pm. Marchwood's covered market
has operated since 1863, runs six days a week, and is at its best on a weekday
morning.
```

**Chunk 3** — source: `guide_halden_bay.md` — produced by: `chunker.py::split_documents`

```
Halden Bay — Where to stay

Almost entirely holiday lets rather than hotels, which means minimum stays of two or three nights in summer. There is one inn on the harbour. Prices roughly halve outside July and August.
```

**Chunk 4** — source: `guide_pellew_sands.md` — produced by: `chunker.py::split_documents`

```
Pellew Sands — Eat and drink

The seafront is chips and ice cream, done well and without pretence. The better cooking is on Marine Terrace, one street back, where four or five places are genuinely good and roughly half the seafront price. Sunday evening is difficult — most kitchens close.
```

**Chunk 5** — source: `guide_walking.md` — produced by: `chunker.py::split_documents`

```
Walking in the region — Easy, on good surfaces

The **Brightwater river path** runs four miles upstream from the town to a weir,
on a made surface, flat throughout. It is the most-walked route in the region
and deservedly so. Continuing downstream from Givens Mill reaches Brightwater in
about three hours.

The **Kestrelford trackbed** follows the railway line closed in 1963 for six
miles to the next village. Easy gradient, good surface, and the best walking in
the region for the effort involved.

**Thornby Wells** has flat, formal gardens and level streets — the region's
most accessible town on foot.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** Which street in Halden Bay has cheaper food than the harbour front?

**Answer:**

```
Fell Street has food that is roughly half the price of the harbour front for comparable food.

Sources: `guide_halden_bay.md` and `guide_eating.md`

(best distance 0.214, cutoff 0.65)
Sources retrieved: guide_eating.md, guide_halden_bay.md
```

**My relevance cutoff:** 0.65 (changed from the starter's 0.6).

The two groups did not overlap. The five questions my corpus covers had best
distances from 0.214 to 0.502. The five out-of-scope questions ran from 0.835 to
1.002. The gap is 0.502 to 0.835, and the midpoint is about 0.67. I put the
cutoff at 0.65, a little under the midpoint, because my test questions are
specific and phrased close to the text, while a real visitor's question will be
looser and land further from its chunk. The weakest covered question (limited
mobility, 0.502) shows that: it is worded generally, and its answer chunk was
ranked 4th. The old 0.6 would also have worked on these ten, but it leaves
less room for loosely worded questions.

Top-k stays at 5. For the limited-mobility question the chunk that holds the
answer ("Straightforward": Thornby Wells) ranked 4th, behind Corry Vale chunks
that only share the words "getting around". At k=3 it would never have come back.

The gate only separates questions from a different world. Two near-miss
questions pass it, since they are about this region but ask for things the
guides don't say:

- "Does Halden Bay have any vegetarian restaurants?" (0.319). The model
  answered "I do not have enough information", so the prompt caught it.
- "How much does a hotel room cost in Marchwood?" (0.459). The model said the
  amounts are not given and quoted only the document's "cheap" outside
  conference weeks, citing `guide_marchwood.md`.

I read `GROUNDING_INSTRUCTION` in `generate.py` and left it unchanged. It
already says to use only the documents, to refuse rather than guess, and to
name the file, and neither near-miss drifted past the sources.

| Question | In corpus? | Best distance |
|---|---|---|
| Which street in Halden Bay has cheaper food than the harbour front? | Yes | 0.214 |
| What time is the Brightwater Tuesday market finished by? | Yes | 0.248 |
| How many times a day does the Halden Bay coast bus service run? | Yes | 0.289 |
| How many times a year does the access road to the Elder Ness headland flood? | Yes | 0.289 |
| Which town in the region is the easiest to get around with limited mobility? | Yes | 0.502 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.835 |
| What is the capital of Mongolia? | No | 0.854 |
| How do I write a for loop in Rust? | No | 0.858 |
| How do I change the oil in a diesel engine? | No | 0.901 |
| Who won the 1994 World Cup? | No | 1.002 |

## How I Used AI

**1. Chunking the guides.** I described the guides to Claude (short files
split by `##` headings, one topic per section) and asked it to replace
`split_documents` with a section-based chunker. It wrote one chunk per section,
prefixed with the guide title and heading, merging short sections and splitting
long ones. When I printed chunks to read them, one was just the Halden Bay intro
paragraph on its own: 188 characters saying only that it is a fishing port,
which answers no question. I had Claude change the code so an intro is joined to
the first section, which brought the corpus from 93 chunks to 84. The overlap
decision was mine: I kept it at zero because section boundaries are already
topic boundaries.

**2. Writing the acceptance criteria.** I asked Claude to fill in the "why this
target" sentences and write criteria 4 and 5 in `criteria.md`. Its first pass
put the text of criteria 4 and 5 under the "Why this target" heading and left no
reasons, and its criterion 3 reason named example words ("lighthouse", "bus",
"dosage") that had nothing to do with my out-of-scope questions. I had it redo
those: criterion 4 now has a 100-character floor tied to the 24-character chunk
the starter produced, and criterion 5 checks that the cited source is a chunk
that really contains the answer. For the retrieval cutoff, Claude
measured the distances and chose 0.65 from the gap between 0.502 and 0.835; I
reviewed the numbers before keeping it.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

Evidence file: `results/run_2026-11-09_1241_before.md`, produced by
`run_eval.py::main` (retrieval by `store.py::search`, chunks from
`chunker.py::split_documents`, cutoff 0.65, top-k 5, caching off). `scorer.py`
does not exist yet, so I judged every answer myself by reading it. Three runs,
no changes in between.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Chunks are complete thoughts, none under 100 characters | 4 of 5 sampled, 0 under 100 | 5/5, 0 | 5/5, 0 | 5/5, 0 | MET |
| 5. Cited source is a chunk that contains the answer | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

How I counted:
- **1 and 5:** for each question I checked whether any of the top 5 retrieved
  chunks contains its `expects` text (case-insensitive), and whether a file the
  answer names is the source of such a chunk. Retrieval is deterministic, so
  criterion 1 is the same in all three runs. Criterion 5 was checked on every
  one of the 15 answers.
- **2:** all 15 answers contain at least one `guide_*.md` filename.
- **3:** one deterministic pass (5 of 5 refused), repeated in all three columns.
- **4:** also deterministic. I checked all 84 chunks rather than a sample: none is
  under 100 characters, and all end on sentence punctuation. The 5 chunks pasted
  under Sample Chunks all read as complete thoughts.

**Real output, criterion 1** (`python app.py retrieve`, produced by
`store.py::search`). The weakest question. The chunk with the answer
("Straightforward", Thornby Wells) is 4th:

```
Question: Which town in the region is the easiest to get around with limited mobility?

#   distance   source                           preview
1   0.5017     guide_accessibility.md           Getting around the region with limited mobility — Di...
2   0.5349     guide_corry_vale.md              Corry Vale — Getting around  Nothing within the vall...
3   0.5376     guide_corry_vale.md              Corry Vale — Getting there  Corry Vale is not a town...
4   0.5408     guide_accessibility.md           Getting around the region with limited mobility — St...
5   0.5541     guide_walking.md                 Walking in the region — Moderate, with hills  The **...

Gate: best distance 0.502 is under the 0.65 cutoff
```

**Real output, criterion 2** (`generate.py::answer_from_chunks`, run 2, from the
results file):

```
The Brightwater Tuesday market is finished by 1pm (Source: guide_brightwater.md and guide_eating.md).
```

**Real output, criterion 3** (`run_eval.py::check_out_of_scope`):

```
| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.854 | refused |
| How do I change the oil in a diesel engine? | 0.901 | refused |
| Who won the 1994 World Cup? | 1.002 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.835 | refused |
| How do I write a for loop in Rust? | 0.858 | refused |
```

**Real output, criterion 4** (`chunker.py::describe`, called by `app.py index`):

```
84 chunks, 354 characters on average (shortest 188, longest 883), produced by chunker.py::split_documents
```

**Real output, criterion 5** (`generate.py::answer_from_chunks`, run 1, from the
results file; the answer cites `guide_accessibility.md`, whose retrieved chunk
at rank 4 contains "Thornby Wells"):

```
Thornby Wells is the easiest town in the region to get around with limited mobility because it is flat, compact, and everything is within three minutes of everything else. 

This information comes from `guide_accessibility.md`.
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer (4 of 5) | MET | 5/5 in all three runs, above the 4 of 5 target. Retrieval is deterministic, so the three runs can't differ. The closest call was the limited-mobility question: its answer chunk ranked 4th (distance 0.541), so it passed only because top-k is 5; at 3 it would be 4/5, still a pass. |
| 2 | Every answer names a source (5 of 5) | MET | All 15 answers (5 questions × 3 runs) contain a `guide_*.md` filename. The target was every answer, and none was missing one. The format varied (backticks, brackets, a "Source:" line) but a filename was always there. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | 5/5 refused. The nearest call was ibuprofen at 0.835, which is 0.185 above the 0.65 cutoff, so this was not close. It is one deterministic pass, so there is no run-to-run variation to worry about. |
| 4 | Chunks are complete thoughts, none under 100 characters (4 of 5 sampled) | MET | Checked all 84 chunks, not a sample: shortest is 188 characters, and every chunk ends on sentence punctuation. The five I read for Sample Chunks all stood alone. "Complete thought" is partly a judgement, so the numeric floor carries most of the weight; the closest chunk to the floor is 188, nearly double it. |
| 5 | Cited source is a chunk that contains the answer (5 of 5) | MET | 15 of 15 answers name at least one file that is the source of a top-5 chunk containing the `expects` text. Because the same fact often sits in two guides, a model citing either one passes; I did not check whether it cited the one that is the best source. |

Two of the criteria (1 and 5) were ambiguous when I scored them, so I added a
revision under each original line in `criteria.md`. The targets did not change,
and none of the five was missed, so no target was lowered.

## Diagnoses

I missed nothing: all five criteria were met in all three runs, so there is no
failure to diagnose by stage. A system that clears everything on the first try
usually means the criteria were safe, so I looked for where my targets were set
low. These are the weak spots the run log does show:

- **Criterion 1 hid a weak retrieval.** The limited-mobility question
  (Thornby Wells) passed, but only just. Its answer chunk ("Straightforward") was
  ranked 4th at distance 0.541, behind two Corry Vale chunks ("Getting around",
  "Getting there") that match the question's words but are about a village with
  no transport. This is a retrieval-stage problem: the question says "easiest to
  get around", the answer chunk lists towns by name, and the embedding scores the
  wording match higher than the meaning match. The other four questions had their
  answer in the top-ranked chunk. At top-k 3 the score would have been 4/5; at
  top-k 1 it would have been 4/5 as well. A target of "4 of 5 in the top 5" could
  not see this.
- **Criterion 3 only tested easy refusals.** My out-of-scope questions (Mongolia,
  diesel engines, a Rust loop) had best distances of 0.835 to 1.002, far from the
  0.65 cutoff. The harder case is a question about this region that the guides
  don't answer. In Milestone 4 I tried one: "Does Halden Bay have any vegetarian
  restaurants?" got a best distance of 0.319, so the gate let it through, and it
  was only the grounding prompt that produced the refusal. The gate did not
  catch it, and criterion 3 as written would never have shown that.
- **Criteria 2 and 5 are weaker than they look.** Many facts sit in two guides
  (a town guide and a cross-cutting one), so any citation of either file passes.
  The model also cited both files for nearly every answer, and I did not check
  that the file it listed first was the best source.
- **Wording drift.** The Fell Street answer says "roughly half the price" while
  the guide says the harbour front is "roughly double". They agree, but a scorer
  that looks for a literal "double" would mark it wrong. This is a generation-stage
  paraphrase, and it will matter once the scorer exists.

The pattern is that my targets measured whether an answer was *reachable*
(top 5, any cited file, far-away refusals), not whether the system picked the
*best* one. That is one problem, not four.

**What I would tighten:**
1. **Criterion 1:** from "top 5 contain the answer, 4 of 5" to "the top 3 contain
   the answer, 5 of 5". My own run would still pass at 4 of 5 for the top 3 and
   miss at 5 of 5, which is the honest score for the Thornby Wells question.
2. **Criterion 3:** add five near-miss questions about the region that the
   guides don't answer (vegetarian restaurants, hotel prices, and so on) and
   require the system, gate or prompt, to refuse at least 4 of those 5.
3. **Criterion 5:** require that the first file the answer names is a source of a
   chunk containing the answer, not merely any of them.

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
