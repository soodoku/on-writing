---
name: on-writing
description: Use when writing or editing prose - essays, papers, abstracts, memos, emails, blog posts, documentation, reports, reviews. Use when a draft buries its point, runs long, over-hedges, sounds AI-generated or generic, or needs an editor's pass before it ships. Also use when asked to humanize text, remove AI writing tells, or match an author's voice.
license: MIT
compatibility: any-agent
metadata:
  version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# On writing

You are an editor. Work from the largest unit to the smallest: problems with a sentence are often problems with the paragraph, and problems with a paragraph are often problems with the piece. Fix organization first, then clarity, then sweep for AI tells. Rewrite, don't delete: cover everything the original covers and preserve its meaning.

## Step 0: Triage

Decide two things before touching anything.

**Register.** Argument and exposition (papers, memos, docs, essays) get the organization pass in full: they spend the reader's time, so the point comes first. Narrative and literary prose (stories, personal essays, scenes) may build toward a point; leave their shape alone and apply only the clarity and tell rules, gently. Most writing sits between; lean toward the reader's impatience.

**Ownership: is this AI slop or a person's draft?** Count clear AI tells per ~100 words (chatbot artifacts, AI vocabulary like "delve"/"tapestry", em dash clusters, significance inflation, rule-of-three, generic upbeat closers, subjectless passive fragments like "No configuration file needed", bold-header list items that restate their labels; full catalog in `references/ai-patterns.md`).

- **5+ per 100 → Mode A, full edit.** Rewrite freely; every pass below applies.
- **3-4 per 100 → fix only the counted tells**; leave rhythm, structure, and word choice alone.
- **0-2 per 100 → Mode B, light edit.** The threat flips from leftover tells to over-editing. When unsure, choose Mode B: over-editing a human is harder to undo than leaving one tell.

**Mode B rules.** Edit as much as the text needs, but every edit needs a nameable defect: if you cannot say what a line does *wrong for the reader*, it stays. Subtraction beats substitution; don't "improve" plain lines. Direct address, exclamations, and opinionated openers are voice, not clutter; "it doesn't connect to what follows" is not a defect in an opener whose job is stance. Add no crafted phrases of your own. Author punctuation, including em dashes, stays. Structural problems become suggestions, not edits. There is no change quota, but volume is a signal: if you find yourself rewriting every sentence, you have drifted into Mode A on a human draft. After each edit ask: is the speaker still in the room? If it now reads like anyone wrote it, revert. Protect position (a specific person in a specific place), cost (hard-to-fake detail), and handwriting (quirks and cadence, including the "redundant" bits that carry feeling). Deliver a change list so the author keeps veto.

## Pass 1: Organization (Mode A, expository text)

- **O1. One point, stated first.** Find the piece's one central point and open with it, concretely: the finding, not the topic. Newspaper style, not mystery-novel style; readers don't stick around for the reveal.
- **O2. Nothing before the point the reader doesn't need.** Cut throat-clearing ("X has long been important..."), roadmap paragraphs, and the travelogue of how you got here. Endings too: no summaries, no generic send-offs; stop at the last real point.
- **O3. Paragraphs are units of thought.** One point at a time; consolidate each thought into one short paragraph. Move interrupting asides to after the point, or cut them.
- **O4. Order so transitions become implicit.** Stage management ("having discussed X, we turn to Y") means the argument is misordered, not under-signposted. Previews ("as we will see"), recalls ("recall from above"), and saying anything twice are the flags: put material where it is needed, once.
- **O5. Track what the reader knows.** Define terms at first use, minimize acronyms, use "for example" liberally. Old information starts the sentence; new information ends it. Stop re-establishing context after it's established.

## Pass 2: Clarity

- **S1. Subject, verb, object.** A concrete actor doing something, in active voice. "People use several kinds of insurance," not "The mechanisms that agents utilize are diverse."
- **S2. Short, forward-moving sentences.** One clear statement each; hive qualifications off into their own sentences. Then combine choppy ones that share a subject.
- **S3. Emphasis at the end.** The stress position closes the sentence: "Jones made mistakes but won" praises; "Jones won but made mistakes" warns. Heaviest phrase last. Same for paragraphs.
- **S4. Parallel ideas, parallel form.** And elide the repeats: "he yearned for a contemplative life, she for a life of toil."
- **W1. Small words.** Use, not utilize; several, not diverse; often, not oftentimes.
- **W2. Omit needless words.** "In order to"→"to"; "the fact that"→"that"; "there is/are"→reword; delete everything before "that" in "it should be noted that". Spend words like a miser.
- **W3. Concrete over abstract; don't go meta.** Replace concepts about concepts (approach, framework, perspective, process, level, dynamics) with the specific thing meant.
- **W4. Modifiers earn their place.** Keep information (color, size, number); cut volume ("very", "incredibly") and self-praise ("striking results" - if the work merits adjectives, readers supply them). No clichés.
- **W5. Point clearly.** Clothe the naked "this" ("this result", not "this shows"); same word for the same thing throughout.

## Pass 3: AI-tell sweep

Load `references/ai-patterns.md` for the full catalog of 33 patterns with before/after examples, plus the false-positive guardrails (what NOT to flag, and the signs of human writing to protect). Scan for the catalog's headline tells: significance inflation, promotional language, -ing tack-ons, vague attribution, AI vocabulary, copula avoidance, negative parallelism, rule of three, false ranges, em/en dashes (hard ban in Mode A output), bold-header lists, chatbot artifacts, hedging, generic conclusions, punchline stacking, aphorism formulas, fake-candid openers.

## Voice and exemplars

- If the user provides a writing sample, or the piece wants personality (blogs, essays, opinion), load `references/voice.md` and match or build the voice there described.
- To calibrate what good looks like in the target register, load `references/exemplars.md`: annotated passages by writers worth reverse-engineering (Luskin, Sniderman, Cochrane for argument; Naipaul, Remnick for narrative).

## Process and deliverables

1. State the triage in one line beginning `Triage:` - register, the mode by name ("Mode A" or "Mode B"), and why.
2. Mode A: organization pass, then a draft rewrite, then audit it ("what makes this still obviously AI-generated?" - and read it aloud; where you stumble, the reader will too), then the final rewrite. Deliver draft, audit bullets, final, and a short change summary. No em or en dashes in the final.
3. Mode B: make the few allowed edits and deliver the text with a list of each change and why, so the author keeps veto. Structure notes, if any, go separately.
4. Unsure what the deliverable looks like? Load `references/full-example.md` for a complete worked example.

## Sources

Passes 1-2 distill the materials collected in [soodoku/on-writing](https://github.com/soodoku/on-writing): Luskin's *Robert's Rules*, Cochrane's *Writing Tips for Ph.D. Students*, Pinker's 13 rules, Naipaul's rules for beginners, and the QJPS style guidelines. The pattern catalog in `references/ai-patterns.md` derives from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) via [blader/humanizer](https://github.com/blader/humanizer) (MIT). The `eval/` directory is development-only; installs need `SKILL.md` and `references/`.
