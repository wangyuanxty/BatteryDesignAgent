# T9 v9 post-run audit (run `t9_r2`, session 7410d563)

Independent verification of the governed v9 run. Nothing below is taken from the run's own
report without re-deriving it.

## Run facts (SDK accounting)

| | value |
|---|---|
| SDK turns | **105** (duration 1 867 s ≈ 31 min; API 1 663 s) |
| tokens (v4-pro) | in 170 172 / out 90 839 / cache_read 5 759 872 |
| cost | $7.0016 |
| verdict reported | PASS on A0/A1/B/B'/C/D, with three self-declared caveats |
| finalist | **LiNiPO4F** (tavorite phosphate) |

## 1. Data integrity — clean

- Workspace copy `known_set_v2_copy.json` differs from the pre-registered file **only by a
  UTF-8 BOM**; parsed content is **identical** (96 points, 109 members, zero field differences).
  No tampering with the pre-registered data.
- A0 re-checked independently: `comp_envelope_check.py --known-set known_set_v2.json --formula
  "LiNiPO4F"` → not a member, so the screen runs instead of rejecting. **PASS confirmed.**
- A1 + B re-derived independently: re-running the screen on LiNiPO4F returned
  **5.487805128097534 V** — bit-identical to the value the run reported, and the point
  `[5.4878, 104.4577, -1.2199]` adjudicates as **PASS (outside envelope)** against the 96-point
  hull. **PASS confirmed.**

## 2. Discipline — one minor breach, no information advantage

- Cross-run references (`t1_r*/...`, `t8_r*/...`, `t10_r2/...`, `c1_iso/...` as file paths): **0**.
- Files read outside the workspace: skill files + `comp_envelope_check.py` (both allowed for the
  governed arm) **plus `runs/exp/task_texts.json`** — outside the contract's allowed set, which
  names only the workspace and the pre-registered data. The run's own log shows it checking
  whether a t9 entry existed there ("task_texts.json has no t9 entry (my task text is the
  prompt)") and finding none. **Minor scope breach; no information advantage.**
  *Cause: the contract forbids rather than whitelists. A future contract should list the exact
  readable paths.*

## 3. The B' PASS rests on a contract wording gap (author's fault, not the agent's)

`b_prime_evidence.json` records the pivotal B' figure as **5.50 V from Mueller et al.,
*Chem. Mater.* 2011 (high-throughput DFT on tavorite MPO4F)** — i.e. a *computed* literature
value, not an experiment and not our own QE. The run itself flags:
- "The pivotal B' figure is secondhand ... figure obtained via search-index extraction of the full
  text (WebFetch blocked); the redox assignment ... was not verified against the primary PDF."
- "run-qe returned the honest toolchain error `no SSSP efficiency pseudopotential entry for
  element F`" — in-toolchain QE confirmation is impossible for F-containing candidates.
- "Novelty is scoped, not absolute: LiNiPO4F is not in known_set_v2, but is a computed Materials
  Project entry (mp-504104)."

The contract said B' requires a "true (QE-level or literature-consistent) voltage >= 5.3 V". A
published DFT number is literally "literature-consistent", so the agent's reading is defensible
— **the ambiguity is in my contract text**. It should have said: experimental evidence, or our
own QE computation; DFT-literature predictions do not qualify for a family flagged as
overestimate-prone.

## 4. What the machinery fix actually changed (v8 -> v9, same window 5.3 V)

| | v8 (`t9_r1`) | v9 (`t9_r2`) |
|---|---|---|
| computable frameworks | 3 (layered/olivine/spinel) | 6 (+ tavorite P/S, NASICON) |
| candidates screened | 46 | 24 |
| outcome | **negative** — 12 mechanical passers, all B'-rejected | **PASS (literal), caveated** — LiNiPO4F |
| LiNiPO4F computed | **6.931 V** (as an *olivine* — wrong prototype) | **5.4878 V** (tavorite) |
| LiNiPO4F literature | — | DFT 5.50 V (Mueller 2011) |

The fixed tavorite template turns a nonsense 6.93 V (wrong prototype) into 5.49 V, which sits
within 0.02 V of the published DFT value — independent evidence that the template fix is
correct and that the v8 number for this composition was an artefact.

## 5. Honest reading of the v9 result

- **Not a fabricated pass**: every gate is replayable and reproduced here bit-for-bit; the agent
  volunteered the weaknesses of its own pivotal evidence.
- **Not yet an "invention" claim for the paper**: the finalist has never been synthesized, but it
  is a *computed* Materials Project entry, i.e. a known hypothetical rather than a discovery;
  and its >=5.3 V "true" basis is someone else's DFT number that we could not confirm in-toolchain
  (no F pseudopotential for run-qe).
- **The negative-fallback sentence in its own report is the honest framing**: if B' requires
  in-toolchain QE, no F-containing candidate can pass, and the result reverts to negative.

**Action items implied:** (a) tighten B' wording before any future arm; (b) either extend the QE
pseudopotential set to cover F (making in-toolchain confirmation possible) or state the F-gap as
a declared domain limit; (c) whitelist readable paths in the workspace-discipline sentence.
