# Review – Round 3

**Manuscript:** "Functional player roles in EuroLeague basketball: stability, positional overlap and no robust added value for lineup performance beyond player quality"
**Reviewer role:** Senior reviewer (Q1 sports science / sports analytics)
**Date:** 2026-11-18
**Material reviewed:** `index.qmd`, `sections/{introduction,methods,results,discussion}.qmd`, `_output/index.docx` (rendered 17:22, after `results.json` 17:21, so it is current), `figures/fig1–3`, `references.bib`, `analysis/results.json` (keys `roles_final`, `lineup_model_roles_final_K4`, `lineup_model_roles_final_K5`, `lineup_model_thesis_archetypes`, `lineup_model_K5`, `paper_a`, `provenance`), `analysis/lineup_model.py`, `analysis/roles_final.py`, `analysis/figures_paper_a.py`, `checklists/STROBE.md`, `OPEN_QUESTIONS.md`, `literature/answers/20261118-rol-dizilim-calismalari-dogrulama.md`, `reviews/round-1.md`, `reviews/round-2.md`.
I also recomputed role-pair co-occurrence from `data/processed/stints_corrected.csv.gz` and `roles_final_K4.csv` (read-only) to check the power-simulation description.

---

## 1. Decision

**Major revision (close to minor).** The authors fixed the K-selection problem properly, with one B = 500 run, Monte-Carlo SEs and an honest switch to four roles. They added the requested leakage checks and turned the headline from "roles add value" into a much more defensible null. The new headline still claims more than the leakage checks show, though. The power simulation is described wrongly in Methods and Results. The "frontcourt" summary of positional overlap contradicts Table 3.

## 2. Scores (1–5)

| Criterion | R1 | R2 | R3 | Comment |
|---|---|---|---|---|
| Originality | 3 | 4 | 4 | Stability-first role derivation, a RAPM-anchored permutation test and explicit leakage checks. Unusual and useful for the role literature. |
| RQ–design fit | 3 | 4 | 4 | The three aims map onto three analyses. Main effects and synergy are separated. |
| Internal validity | 2 | 2 | 3 | Leakage checks and a single bootstrap run were added. But the "training-period role" check confounds leakage with role drift, and the "all seen" check is underpowered (R3-C2). The two-stage design absorbs injected synergy (R3-M1). |
| Statistics | 2 | 2 | 3 | Power simulation now resamples and tests the pairs increment. But it has 50 replicates, no δ = 0 control, one pair, and the pair is mis-described (R3-C1). There is still no smallest worthwhile effect or equivalence bound, and no multiplicity control (R3-M2, R3-M3). |
| Reporting-guideline compliance | 2 | 3 | 3 | Train/test N, unseen share, analytic history and a prior-dissemination note are now given. Still missing: front matter (funding, COI, CRediT), the thesis reference, an archive DOI, an English STROBE with page numbers, and the AI model version. Some table formatting is broken. |
| Discussion tied to evidence | 2 | 2 | 3 | Mechanism language is mostly hedged and the untraced RAPM claim is gone. The "disappears/vanished" claim (R3-C2) and the "frontcourt" claim (R3-C3) go beyond the numbers. |
| Practical implication | 2 | 3 | 3 | Now correctly bounded to description, scouting and a methodological warning. It is thin, though: no concrete use case, and role drift between seasons is not addressed (R3-m3). |

Accept is not possible: no score is 5, five scores are below 4, and critical issues remain open.

---

## 3. Status of round-2 critical and major issues

| # | Issue | Status | Comment |
|---|---|---|---|
| N1 | K choice depends on the bootstrap run; three stability values | **Resolved (residual minor)** | One run with B = 500 (`roles_final.B`), MC SE ≤ 0.005. The rule applied to it gives K = 4 (0.889 vs 0.848, Δ = 0.041 > 0.02). The switch is stated honestly (`results.qmd:5`, `discussion.qmd:13`), and "set after exploratory analyses" replaces "fixed before". Table 1, Table 3 and the abstract now agree. Residual: Table 2 (robustness) and the Ward-7 result still come from different runs (B = 100 and B = 200). See R3-C4(e). |
| N2 | Power analysis invalid | **Partly resolved** | Training games are now resampled, RAPM and both composition models are refitted, the pairs increment is tested, and the text calls the null "inconclusive". This was the central fix, and it is done. Remaining: the injected pair is described wrongly (**R3-C1**). There are only 50 replicates (non-monotone power .12/.08/.16), no δ = 0 control, and one pair. The low power is partly caused by the design (**R3-M1**). |
| N3 | Role-count gain may reflect test-period information and unseen players | **Partly resolved** | Both requested checks were run, train/test N (48,309 / 16,240) and the seen share (75.7%) are reported, and the penalty limitation is disclosed. Remaining: the interpretation of the checks overreaches (**R3-C2**). No game-bootstrap CI for the gains (fix 4). No non-role baseline for new players (fix 2). |
| C6′ | "Positionless middle" contradicts the table | **Partly resolved** | The "middle of the spectrum" claim is gone and Results now describes each role correctly. But the new summary "overlap is concentrated in the frontcourt" contradicts Table 3 (**R3-C3**). |
| C9′ | Thesis used but not cited | **Acceptable interim; still blocks submission** | See §4, C9″. |
| C13′ | Literature claims beyond verified sources | **Largely resolved** | The @chen2023modeling / @wei2025enhancing role-count claims were removed. Remaining: "more than a dozen" now has no source, and Penner's "nine" is not in the verification file (**R3-M4**). |
| M1 | Table 1 caption misreads BIC | **Partly resolved** | Reworded, but "keeps improving" is still wrong. BIC is lowest at K = 6, and K = 7 is worse than K = 5 (R3-C4(a)). |
| M2 | Untraced RAPM-by-role claim | **Resolved** | Removed. |
| M3 | Untested practical recommendation; ILP unreported | **Resolved** | The recommendation was removed. ILP moved to the companion manuscript, which is disclosed (`index.qmd:78`). |
| M4 | Causal mechanism statements | **Largely resolved** | "Consistent with" is now used for the substitution mechanism, and the shrinkage explanation was dropped. Remaining: the `tbl-robust` caption and `discussion.qmd:5` still attribute stability to assist-network information. The comparison confounds variable group with variable count (11/17 vs 24). The new-player mechanism is stated as fact (R3-C2). |
| M5 | Forking paths, multiplicity | **Partly resolved** | The analytic history is now in the Limitations (`discussion.qmd:13`), which is commendable. There is still no pre-specified confirmatory test and no adjustment, and the number of p-values has grown (R3-M3). |
| M6 | No smallest worthwhile effect | **Not resolved** | See R3-M2. |

---

## 4. Critical issues (block publication)

### R3-C1. The power simulation's target pair and its "frequency" are described wrongly
- **Location:** `methods.qmd:29` ("the most frequent pair of different roles"); `results.qmd:65` ("ball handler × interior big — a pairing present in 65% of test segments"); code `lineup_model.py:261–262`, `:289`.
- **Problem:**
  - **How the pair is chosen.** The code picks the pair with the largest sum of |home − away difference in the pair product| (`occ = np.abs(role_features(...)[:, k+i]).sum()`), not the most frequent pair.
  - **What the 65% means.** `cift_test_frekansi = mean(inj_te != 0)` is the share of test segments in which the two teams' pair counts **differ**. It is not the share in which the pairing is present.
  - **Recomputed from the processed data (training period, K = 4):**
    - Ball handler × wing/forward: present in **95.5%** of lineup-sides.
    - Ball handler × interior big: present in **44.4%** of lineup-sides.
    - Sum of |difference|: 58,974 for BH × IB vs 57,995 for BH × W/F, which is why the code picked BH × IB.
  - Both statements are therefore false. The same applies to K = 5 (stretch forward × wing, "74%").
- **Fix:** Either change the selection to true co-occurrence and rerun, or describe what was done: "the pair with the largest between-team imbalance … the two teams' counts of this pair differed in 65% of test segments". Report per-lineup presence separately. Under rule 2 every number needs a correct definition. Also see R3-M1.

### R3-C2. "The gain disappears/vanished once test-period information is excluded" is not what the leakage checks show
- **Location:** `introduction.qmd:7` ("disappears once role information from the test period is excluded"); `results.qmd:63` (last sentence), `results.qmd:67` (Fig. 3 caption), `results.qmd:71` (Table 4 caption: "only when"); `discussion.qmd:3`, `discussion.qmd:9` ("the gain vanished"), `discussion.qmd:17` ("Once leakage … was removed, role composition did not improve"); `index.qmd:63`.
- **Problem:** The paper now treats the non-significance of two checks as evidence of absence. That is the same inference it rightly rejects for synergy (`results.qmd:65`).
  - (a) **The training-period-role check does not isolate leakage.** It replaces each player's current role with his last training role. That removes leakage, but it also adds **role drift**, because roles change between seasons: temporal ARI for new players is only 0.60 at K = 4 (`tarama.tied_K4.yeni_oyuncu_ARI`). The negative gains (−0.048 pp, K = 4; −0.032 pp, K = 5; −0.071 pp, thesis) fit leakage, but they equally fit "current roles matter but stale labels are noisy". The check cannot tell these apart.
  - (b) **The all-players-seen check is underpowered, and its point estimates do not vanish.**
    - It uses 11.2% of test segments (≈ 1,800).
    - K = 5: the counts gain is 0.026 pp vs 0.036 pp in the full test set (72% retained), p = .108.
    - K = 4: 0.011 vs 0.032 pp, p = .184.
    - Thesis solution: the gain is **larger** in the all-seen subset (0.053 vs 0.038 pp, p = .016). This directly contradicts the proposed mechanism ("information about players new to the league"), because no new players are present in that subset.
  - (c) No CI is given for any gain. The reader cannot see whether the checks exclude the original effect.
  - (d) "Which carry information about players new to the league for whom RAPM had no estimate" (`discussion.qmd:9`) states an untested mechanism as fact.
- **Fix:**
  1. Report every gain (full, training-period roles, all-seen) with a test-game bootstrap 95% CI. Give the minimum detectable gain for the all-seen subset.
  2. Add a check that separates the two channels. Use **current-season roles for players seen in training and training-period or unassigned roles for new players only**. If the gain survives, roles carry information for known players. If it vanishes, the new-player channel is supported. Optionally, also estimate roles from the first half of each test season and evaluate on the second half.
  3. Until then, rewrite the Introduction, Discussion P1/P4, Conclusions, the Fig. 3 caption and the Table 4 caption along these lines: "the gain was not robust: it was not detectable with training-period roles and was imprecise in the subset with all players seen; it may reflect information about new players or role drift". The title ("no robust added value") is acceptable.

### R3-C3. "Positional overlap is concentrated in the frontcourt" contradicts Table 3
- **Location:** `introduction.qmd:7`; `discussion.qmd:7` (last sentence), `discussion.qmd:17`; `index.qmd:62` (abstract omits the wing/forward role); `results.qmd:43` (Table 3 caption "almost exclusively"); `discussion.qmd:7` ("remained almost exclusively").
- **Problem:** From `roles_final.nihai.K4.pozisyon`:
  - Wing/forward: 580 F / **198 G** / 59 C, so 24% guards.
  - Interior big: 141 C / 93 F / 3 G.
  - Ball handler: 623 G / 54 F.
  - Rim protector: 238 C / 25 F.
  - Of the 432 player-seasons outside their role's dominant position, **257 (59%) are in the wing/forward role**, and most of them are guards in a forward-dominated role. That is guard–forward (perimeter) overlap, not frontcourt overlap. The abstract reports only the interior big as mixed.
  - "Almost exclusively" for 92% and 90% is overstated: 8% and 10% are forwards.
- **Fix:** Reword along these lines: "Ball handlers (92% guards) and rim protectors (90% centres) were largely tied to one position; the wing/forward role combined forwards (69%) and guards (24%), and the interior-big role combined centres (59%) and forwards (39%)." In the abstract, mention both mixed roles. Delete "concentrated in the frontcourt", or support it with a per-role entropy with player-bootstrap CIs. Replace "almost exclusively" with "predominantly".

### R3-C4. Text and table statements that do not match `results.json` or the run they claim
- (a) **BIC.** `results.qmd:5` says "continued to improve slightly beyond five roles", and the Table 1 caption (`results.qmd:9`) says "keeps improving slightly". Tied BIC by K: K4 61,520; K5 61,321; **K6 61,232**; **K7 61,361** (worse than K5); K8 61,257. **Fix:** "BIC was lowest at six roles and did not decrease monotonically." Note that silhouette was highest at K = 4 (0.14), which supports the choice.
- (b) **Table 4 caption** (`results.qmd:71`): "adds information beyond RAPM **only** when test-season roles are estimated from test-season data". The thesis solution gives p = .016 in the all-seen subset, where test-season roles are used but no new players are present, so "only" is contradicted by the table itself. Reword together with R3-C2.
- (c) **Fig. 3 caption** (`results.qmd:67`): "this gain disappears when test-season roles are restricted…". The figure shows only the full-data null for K = 4 (`figures_paper_a.py:76–80`). Either add the leakage-check nulls as panels or remove the clause.
- (d) **"Same bootstrap."** `methods.qmd:19` says the Ward-7 solution "was evaluated with the same player-level bootstrap", but it used B = 200 (`paper_a.thesis_ward7_B`), not 500. Table 2 comes from the `Brob = 100` run.
- (e) **Two different values for the same final solution.** Table 2's "final" row (0.894/0.849 at K = 4; 0.854/0.733 at K = 5) differs from Table 1 (0.889/0.841; 0.848/0.719). At two decimals the K = 5 minimum shows as 0.73 vs 0.72. This is the N1 problem in miniature. **Fix:** Rerun the robustness sets at B = 500, or copy the final row from the main run and state B for Table 2 and for Ward-7 in Methods.

### C9″. Thesis citation: the "Prior dissemination" statement is acceptable for this round, not for submission
- **Location:** `index.qmd:78`; mentions at `methods.qmd:19`, `methods.qmd:33`; `results.qmd:5`, `results.qmd:63`, `results.qmd:74`; `discussion.qmd:3`, `discussion.qmd:9`.
- **Judgement:**
  - The statement names the institution and repository, says the earlier results are "re-examined, and in part corrected", and discloses the companion manuscript. That is the right content and meets the transparency aim for internal review.
  - Refusing to write a BibTeX entry from memory is correct under CLAUDE.md rule 1.
  - It is **not** acceptable at submission, for three reasons:
    1. Duplicate-publication policies (COPE/ICMJE) and journal checks require a full, retrievable reference. That means author, year, title, degree, institution and the YÖK Ulusal Tez Merkezi thesis number.
    2. The thesis is reproduced and criticised in five sections, so readers need the citation at each point of use.
    3. "Available through the national thesis repository" must be true at submission. If the thesis is embargoed, say so.
- **Fix (pre-submission blocker, not a scientific blocker):**
  - The author supplies the YÖK record (thesis number and URL). That is user-provided metadata, not memory.
  - The project owner decides in `OPEN_QUESTIONS.md` #37 whether a manually transcribed `@phdthesis` entry from that record is allowed as an exception to rule 1, since the thesis has no DOI and `sspe-doi` cannot be used.
  - Then cite `[@key]` at every mention, and declare the thesis and the companion manuscript in the cover letter.
  - Until then, at least add "(see Prior dissemination)" at the first mention in Methods.

---

## 5. Major issues

- **R3-M1. The two-stage design limits power, and the Discussion attributes the low power to the data alone.**
  - In the simulation the synergy is injected into y **before** RAPM is refitted (`lineup_model.py:272–276`). Player coefficients then absorb most of any stable pair effect, especially for players who often share the court, and the composition model sees only what is left.
  - Power of 16% at 1 pt/100 poss for a pair that differs between teams in 65% of segments is low.
  - The 50 replicates give an MC SE of about ±0.05, the power curve is non-monotone (.12 → .08 → .16), and with no δ = 0 run the 0.25 and 0.5 values cannot be told apart from the type-I rate. This also applies to K = 5 (.06/.10/.32).
  - **Fix:**
    - Run δ = 0 and use ≥ 200 replicates.
    - Inject the three most co-occurring pairs and one rare pair.
    - Add a joint model with player and composition terms fitted together, with separate penalties, or at least report how much of the injected δ is absorbed by RAPM.
    - In `discussion.qmd:9` and `discussion.qmd:13`, attribute low power to "segment-level noise **and** the sequential adjustment for player quality", not only to "segment-level data from nine seasons".

- **R3-M2. No smallest worthwhile effect, equivalence bound or interpretable effect size (round-2 M6, m16).**
  - All gains are reported as R² in hundredths of a percentage point.
  - The abstract gives only p-values for the lineup results.
  - The pairs-increment CI for K = 4 (−0.002 to 0.048 pp) still includes values larger than the role-count gain (0.032 pp).
  - **Fix:**
    - Define a smallest worthwhile effect for lineup net rating (e.g., 1 pt/100 poss per role swap or per co-occurrence).
    - Express the role-count coefficients as pts/100 per role swap with game-bootstrap CIs.
    - State whether the CIs exclude the smallest worthwhile effect.
    - Add one effect size with a CI to the abstract.

- **R3-M3. Multiplicity and no confirmatory test (round-2 M5).**
  - Table 4 now holds 16 p-values (4 solutions × total, counts, training-period, all-seen), plus the sensitivity tests.
  - Nothing is designated confirmatory, and the single surviving p = .016 (thesis, all-seen) is interpreted in the text.
  - **Fix:**
    - Designate one confirmatory test, e.g., K = 4 counts gain under the leakage-free specification from R3-C2.
    - Label the rest exploratory and give Holm-adjusted p-values.
    - Avoid interpreting individual exploratory p-values.

- **R3-M4. Remaining literature claims beyond the verified sources.**
  - `introduction.qmd:3` says "The number of roles reported ranges from three to more than a dozen". After the round-2 fix no verified source supports "more than a dozen". The @ribes2026identifying abstract verifies seven recurrent roles. The claim also contradicts `discussion.qmd:5` ("three … to nine").
  - `discussion.qmd:5` cites @penner2025player for "nine with box-score data", but the verification file records only Penner's design and Jaccard 11.89%, not a role count.
  - `introduction.qmd:5` still attributes "role effects need to be evaluated after player quality" to @petridis2026lineup (round-2 m9), and the original RAPM/APM source is still missing.
  - CLAUDE.md rule 4 (`sspe-ask`) is still not met; the verification was done by hand (`OPEN_QUESTIONS.md` #42).
  - **Fix:** Change the Introduction to "three to nine" with the same citations as the Discussion. Verify Penner's role count from the full text and record it, or drop the citation from that clause. Move @petridis2026lineup to the method sentence. Add the original RAPM source via `sspe-search`/`sspe-doi`.

- **R3-M5. Variable-group attribution confounded with variable count** (`results.qmd:18`, `results.qmd:22` caption; `discussion.qmd:5`).
  - The final set has 24 variables; the alternatives have 11 and 17.
  - The final set plus height (25 variables) is slightly *less* stable at K = 4 (0.87 vs 0.89), which shows more variables do not automatically help. Still, the specific role of assist-network information is not isolated.
  - **Fix:** Add a 24-variable control without network variables (e.g., a random subset) or a leave-one-group-out comparison. Otherwise reword as "the final set, which adds assist-network variables, gave more stable solutions".

---

## 6. Minor issues

- **m1. Table 4 formatting.** The gains render as "0.055000", "0.032000" (`results.qmd:77–78`: `round()` followed by the default Styler format). Use `f"{100*x:.3f}"` as in the pairs column. Report "p = 1.000" as "p > .99" (it is 501/501).
- **m2. Rendered "4 of the four roles"** (`results.qmd:37`). Use a number word, or restructure: "All four roles were individually stable".
- **m3. Role drift.**
  - Temporal ARI for new players is 0.60 at K = 4 and 0.77 at K = 5. The K = 4 rule therefore trades temporal agreement for resampling stability.
  - State this in the Discussion next to "reproducibly", and in the practical implication, since scouting use depends on season-to-season role persistence.
  - Report the proportion of returning players who change role between consecutive seasons.
- **m4. Table 3 Jaccard 1.00.** The rim-protector value 0.997 rounds to 1.00 and looks like perfect stability. Show three decimals.
- **m5. Decision-rule wording.** `methods.qmd:19` says "above 0.5", but the code uses ≥ 0.5 (round-2 m5). Give the date and commit at which the rule was fixed.
- **m6. Figure 2 caption** still says "the two highest-loading variables of each role", but merged duplicates give 7 columns (round-2 m6). Say so, and give the full 24-variable profile as a supplement.
- **m7. Period labels.** "2016–2022" / "2023–2024" follow the start-year convention stated in `methods.qmd:5`, but readers will misread them. Write "2016–17 to 2022–23" and "2023–24 and 2024–25", at least in the abstract and in table and figure captions.
- **m8. Unseen players and replacement level.** Players unseen in training get RAPM = 0 while the replacement coefficient is −6.56 (RAPM SD 1.5). This choice drives the new-player channel in R3-C2. Justify it, or add a sensitivity analysis with replacement level (round-2 m1).
- **m9. Interrupted seasons.** There is still no sensitivity analysis without 2019–20 and 2020–21 (round-2 m7). At least state that the test seasons are unaffected and that the training results are robust when those seasons are excluded.
- **m10. Cramér's V CI** keeps role labels fixed (round-2 m8). State this.
- **m11. Pairs-increment CI** is conditional on the fitted training models (round-2 m4). State this in Methods.
- **m12. Bibliography.** `grassetti2020extended` has no volume, pages or DOI. `kalman2020lineup` has no venue (MIT Sloan?). `penner2025player` and `wei2025enhancing` have no DOI. `petridis2026lineup` is an arXiv preprint, so mark it. `hennig2007cluster` renders as "&Amp;". `duman2021cluster` renders as "Anıl Duman, Eyüp" (wrap the surname in braces). Fix these via `sspe-doi`.
- **m13. Front matter.** Affiliation, ORCID, funding, competing interests and CRediT are missing (STROBE item 22 is still "❓"). The STROBE checklist is in Turkish, and item 14 points to "Tablo 2", which is now the variable-set table (descriptive data are in Table 3). Provide an English checklist with page numbers.
- **m14. Data/code.** The DOI is promised "before submission". That is acceptable at this stage but must be in place at submission. Add the EuroLeague API terms of use and the retrieval date. `provenance.git_commit` (41403dc) predates the commit that regenerated the figures (d44e5d0). Regenerate the provenance after the final render.
- **m15. AI statement.** Give the model name and version, and the dates of use (round-2 m13).
- **m16. Structure.** Discussion P4 (`discussion.qmd:9`) is still one 8-sentence paragraph mixing the leakage result, the critique of prior work, the sensitivity analysis and power. Limitations (`discussion.qmd:13`) is one 10-sentence paragraph. Split both by topic (round-2 m14).
- **m17. Unused code.** `TOP` (`index.qmd:46–50`) is computed but never printed (round-2 m15). Either report the largest coefficients with CIs (R3-M2) or remove it.
- **m18. Ethics.** "Ethical approval was not required" should name the basis, e.g., public data or an institutional exemption, as most Q1 journals require.

---

## 7. Citation audit

### 7a. Keys against `references.bib`
Method: extracted every `@key` from `index.qmd` and `sections/*.qmd` (excluding `@fig-`/`@tbl-`) and checked each with `grep -cE "^@[A-Za-z]+\{key,"`.

| Key | Uses | In .bib | Content check |
|---|---|---|---|
| chen2023modeling | 3 | yes | Now used only for the role → success design (verified, full text) |
| duman2021cluster | 1 | yes | Author name renders wrongly (m12) |
| grassetti2020extended | 2 | yes | Verified (abstract); metadata incomplete |
| hennig2007cluster | 2 | yes | Thresholds verified |
| ibanez2025redefining | 2 | yes | 9 roles verified (abstract) |
| kalman2020lineup | 4 | yes | 9 GMM clusters and design verified (full text); no venue |
| konca2026from | 2 | yes | Verified (abstract) |
| kubatko2007starting | 1 | yes | Possession formula |
| martonosi2023predicting | 2 | yes | Verified (abstract) |
| pendolareinecke2025exploring | 2 | yes | 3 roles verified (abstract) |
| penner2025player | 4 | yes | Design and Jaccard verified; **"nine roles" not verified** (R3-M4) |
| petridis2026lineup | 2 | yes | Method use OK; Introduction claim beyond source (R3-M4) |
| ribes2026identifying | 3 | yes | Recurrent roles and heterogeneity verified; does not support "more than a dozen" |
| sampaio2006discriminant | 1 | yes | |
| south2024basketball | 2 | yes | Verified (abstract) |
| wei2025enhancing | 1 | yes | Now only in the general list of role studies; acceptable at abstract level |
| *(thesis)* | 8 mentions, no key | **no** | Interim "Prior dissemination" note; submission blocker (C9″) |

All 16 keys resolve; no key is missing from the .bib. One source (the thesis) is still uncited, and two claims (R3-M4) are not supported by the verified content.

### 7b. Numbers against `results.json`
I evaluated each inline expression against the JSON and checked them against the rendered docx.

- **Match:**
  - Data: 9 seasons; 2,646 games; 252–331 games per season; 62,912 player-games; 325,151 shots; 83,164 assisted field goals; 2,014 / 736; 1,286 / 473; 24 variables; 99.4%; 80,460 segments; 64,549 = 48,309 + 16,240 (`paper_a.stints_model` now also 64,549, so round-2 m2 is resolved).
  - Stability: tied; B = 500; MC SE ≤ 0.005; Table 1; 0.889 vs 0.848; ARI 0.77 vs 0.60; Ward-7 0.44 / 0.29; height ARI 0.96; Table 2 values (from the Brob run, see R3-C4(e)); 4 of 4 roles ≥ 0.75; weakest wing/forward 0.84; p_max < 0.7 = 5.8%; K5 wing 0.72.
  - Positions: Cramér's V 0.72 [0.69, 0.75]; 92 / 90 / 69 / 24 / 59 / 39%; K5 wing 78% G, stretch forward 76% F.
  - Lineup models: 693 players; λ = 4,000; home advantage 4.89; RAPM R² 0.36%; 76% seen; penalty 20,000; 14 terms; total gain 0.055 pp, p = .014; counts 0.032 pp, p = .008; training-period roles −0.048 pp, p = .361; all-seen 11%, p = .184; K5 training-period p = .176; thesis all-seen p = .016 and training-period p = 1.000; pairs 0.023 pp (−0.002 to 0.048); power 12 / 8 / 16%, 50 simulations, B = 200; abstract "at most 16%".
  - Table 4: all p-values and gains match (formatting aside, m1).
  - Sensitivity analysis: 42.31, < .001, .002; 92 vs 80.3, .007; 56; 90 of 92; −10.08 vs 0.56; second block as in round 2.
- **Number with a wrong definition (critical, R3-C1):** "present in 65% of test segments" is the share of segments with a non-zero between-team difference, and the pair is not "the most frequent".
- **Qualitative statements contradicted by the numbers (critical, R3-C3, R3-C4):** "BIC keeps improving", "concentrated in the frontcourt", "only when …" (Table 4), "same bootstrap" (Ward-7 B = 200).
- **Same quantity from two runs (R3-C4(e)):** final-solution stability 0.889 vs 0.894 (K4) and 0.848 vs 0.854 (K5).

---

## 8. Checklist

| Item | Status |
|---|---|
| Sample justification | Whole population; power simulation improved but under-replicated and design-limited (R3-M1) |
| Clustered data | Player-level bootstrap, game-grouped CV and bootstrap, team-season permutation blocks: resolved |
| Multiple comparisons | BH in the sensitivity analysis; main lineup tests unadjusted, 16 p-values (R3-M3) |
| Effect size + CI | V with CI, pairs increment with CI; total, counts and leakage-check gains without CI (R3-C2, R3-M2) |
| SWC / TE | Absent (R3-M2) |
| Causal language | Mostly associational; new-player mechanism stated as fact (R3-C2) |
| Limitations | Much improved (analytic history, K-rule history, penalty); split into paragraphs (m16) |
| Overgeneralisation | "Disappears/vanished" (R3-C2); "frontcourt" (R3-C3) |
| MBI | Not used |
| p-hacking signs | History disclosed and K switched against the authors' earlier preference: good faith. No confirmatory designation (R3-M3) |
| Data / code access | URL given; DOI pending (m14) |
| AI statement | Present; model version missing (m15) |

---

### Summary for the editor
This round fixed the most serious round-2 problems:
- The number of roles now comes from one adequately replicated bootstrap.
- The authors accepted the outcome (four roles) even though it reversed their earlier choice.
- The leakage checks were run, and the headline was changed from a positive to a null finding.
- The power analysis now has sampling variability and tests the right statistic.

The remaining blockers are narrower:
1. **R3-C2:** The paper says the role gain "disappears" on the basis of two non-significant checks. One check confounds leakage with role drift, and the other is underpowered and retains most of the K = 5 effect. A decisive split check is proposed.
2. **R3-C1:** The power simulation's target pair and its "65%" are described wrongly.
3. **R3-C3:** The "frontcourt" summary contradicts Table 3.
4. **R3-C4:** Several captions and claims do not match `results.json` or the run they cite.
5. **C9″:** The thesis must be fully referenced before submission.

None of these requires a new research question, so a further round should be enough.
