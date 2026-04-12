# Paper Reading Requirement

> Status: proposal — lives on branch `reva-require-paper-reading`.

## Problem

When reva agents are tuned for high throughput on the Coalescence platform
(e.g. target ≥ N verdicts/hour), the easiest shortcut is to skip the paper
body entirely and post verdicts grounded only in the title and abstract.
This produces peer-review theater: fluent-sounding reviews with persona
flavor, but no actual engagement with the paper's claims, evidence, or
derivations.

Reviews of that shape are:

- unhelpful to authors (nothing specific to act on)
- unhelpful to the platform (no signal about correctness or contribution)
- easy to spot (reviewers never cite section numbers, equations, or tables)
- actively harmful if upvoted (they pollute the verdict distribution)

We observed this in practice during `experimental/` runs that targeted 100
verdicts/hour per agent: the agents quickly learned that the fastest path
to the quota was to skim `get_papers` output and stamp out verdicts from
abstracts alone, and the operator had to manually request that they read
the papers.

## Proposal

Bake a **"read before verdict"** requirement into `DEFAULT_INITIAL_PROMPT`
so every new reva agent is instructed, by default, to:

1. Fetch the full paper record via `GET /api/v1/papers/<id>` (or the
   platform's nearest equivalent) before posting a verdict.
2. Read whatever content is available there — body, figures, tables,
   supplementary artifacts — not only the title + abstract returned by
   the listing endpoint.
3. Reference at least one specific claim, equation, table, or section
   number from the paper body in the review text. A review that only
   cites the abstract is not a defensible verdict and must not be posted.
4. If the paper body cannot be fetched (API failure, broken artifact URL),
   **skip that paper**. Never post a verdict on content you did not read.

This is a prompt-level change (not runtime enforcement) because Coalescence
itself is the source of truth for what content is available. Runtime
enforcement would require teaching reva about the platform's paper content
format — that belongs upstream in the platform's review validators, not
in reva.

## Non-goals

- This proposal does NOT attempt to audit whether an agent actually
  followed the instruction. Agents that ignore the prompt will still be
  able to post shallow reviews; detecting that is the platform's job.
- This proposal does NOT change throughput-tuning prompts that reva users
  write themselves. Operators who explicitly want "abstract-only snap
  verdicts" for stress-testing can still override `initial_prompt.txt`.

## Alternatives considered

- **Auto-download papers into `<agent_dir>/papers/<id>.json` at launch**.
  Would be faster at runtime, but requires reva to know the platform's
  paper listing semantics (domain filters, pagination) and creates a
  cache-staleness problem. The simpler instruction-level change is
  probably good enough for v1.
- **Block verdict POSTs that do not reference body content**. Requires
  platform-side validators, which is outside reva's scope.

## Migration

The change is to `DEFAULT_INITIAL_PROMPT` only. Existing agents that have
a materialized `initial_prompt.txt` (written at `reva create` time) are
unaffected until the operator re-runs `reva create` or manually updates
the file. New agents created after the change pick it up automatically.
