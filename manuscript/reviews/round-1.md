# Review – Round 1

**Manuscript:** "Functional player roles in EuroLeague basketball: stability, positional overlap, and their limited value for explaining lineup performance"
**Reviewer role:** Senior reviewer (Q1 sports science / sports analytics: JSS, IJSPP, JQAS)
**Date:** 2026-11-18
**Material reviewed:** `index.qmd`, `sections/{introduction,methods,results,discussion}.qmd`, `figures/fig1–3`, `references.bib`, `analysis/results.json`, `analysis/{archetypes_v2,lineup_model,role_position,archetype_formulas,paper_a_summary,figures_paper_a,thesis_archetypes}.py`, `OUTLINE_15steps.md`, `literature/answers/20261118-rol-dizilim-calismalari-dogrulama.md`, `_output/index.docx`.

---

## 1. Decision

**Major revision.** The design is sound and potentially valuable: stability-based choice of K, RAPM as a control for player quality, out-of-time validation and a label-permutation null are a real improvement on the role-to-success literature. However, the headline claims ("five stable roles", "role mix adds no measurable information", "build lineups with plus-minus") go further than the evidence in `results.json` supports. Several analytic choices (feature-set selection, the bootstrap unit, GMM specification, a fixed composition penalty, the four-role sensitivity check) are either undisclosed or would change the conclusions.

## 2. Scores (1–5)

| Criterion | Score | Comment |
|---|---|---|
| Originality | 3 | Stability-first roles plus a RAPM-controlled null test is new for the EuroLeague. Closely related work already in the .bib is not discussed (Martonosi 2023, South 2024, Konca & Erilli 2026). |
| RQ–design fit | 3 | RQ1–RQ3 match the design, but RQ3 is a null-hypothesis test that has no power analysis. |
| Internal validity | 2 | Feature sets chosen after the fact. The bootstrap ignores repeated players. Height is imputed from position, which makes the role–position analysis circular. |
| Statistics | 2 | Composition ridge penalty is fixed and untuned. No CIs on any effect size (V, η², R² gain, ARI). GMM is over-parameterised. Selective reporting in the sensitivity analysis. |
| Reporting-guideline compliance | 2 | No STROBE-type checklist (`checklists/` is empty). Key filters are not reported. VAL40 is not defined. The data/code location is not given. The rendered output is stale. |
| Discussion tied to evidence | 2 | "Stable", "reproducible", "positionless in the middle", "role-biased" and the practical recommendation all overreach. |
| Practical implication | 2 | The concrete recommendation (build lineups with plus-minus) is untested in the paper and contradicted by the project's own `ilp_validation` results. |

Accept is not possible until every score is ≥ 4 and all critical issues below are closed.

---

## 3. Critical issues (block publication)

### C1. "Five roles were stable" contradicts the stability threshold the authors set
- **Location:** `index.qmd:7` (abstract "Five roles were stable"); `results.qmd:5`, `results.qmd:16` (Fig. 1 caption), `results.qmd:22`; `discussion.qmd:3`, `discussion.qmd:19`.
- **Problem:** `methods.qmd:19` defines a stable cluster as Jaccard > 0.75. In `results.json["archetypes_v2_full"]`, the K = 5 GMM has mean Jaccard **0.708** and minimum **0.587**. Per-cluster values (`nihai.jaccard_kume`) are 0.776 / 0.589 / 0.628 / 0.903 / 0.574, so only ball handler and rim protector clear 0.75. Three of the five roles fall in Hennig's "patterns, but doubtful" band (0.6–0.75), or just below it. K = 4 has a *higher* mean Jaccard (0.723) and silhouette (0.151 vs 0.107). K = 5 was chosen on cross-period ARI 0.580 vs 0.541. That difference is small, has no uncertainty attached and rests on B = 100 resamples. Fig. 1 itself shows every GMM point below the dashed 0.75 line, so the caption "partitions finer than five are not stable" implies that ≤ 5 is stable, which the figure does not show. Table 1 (min 0.587) and Table 2 (wing 0.574) also disagree because they come from two separate bootstrap runs.
- **Evidence:** Hennig (2007) [@hennig2007cluster]; `results.json` keys above; `archetypes_v2.py:156` vs `:182` (two independent bootstrap calls).
- **Fix:** (a) Say what the data show: "two stable roles (ball handler, rim protector) and three moderately stable roles". Alternatively, make K = 4 primary and K = 5 the descriptive refinement. (b) Pre-state a decision rule for K and apply it. (c) Raise B to ≥ 500 and give Monte-Carlo SEs or bootstrap CIs for mean Jaccard and ARI. (d) Take Table 1 and Table 2 Jaccard values from the same bootstrap run. (e) Rewrite the Fig. 1 caption, abstract, Discussion P1 and Conclusions to match.

### C2. Feature-set selection is undisclosed, and the robustness claim is contradicted
- **Location:** `methods.qmd:19` ("Robustness to variable selection was examined…", with no results reported); `discussion.qmd:15` ("the same role structure emerged with each group of variables").
- **Problem:** `results.json` contains six feature sets: `archetypes_v2` (11 vars), `_extended` (18), `_advanced` (18), `_advanced_height` (19), `_full` (27) and `_full_ff` (35). K = 5 is moderately stable **only** with `full`. With `extended`, K = 5 has mean Jaccard 0.623 and min 0.375 (one cluster dissolved). With `advanced_height` it has mean 0.654 and min 0.421. With `full_ff` it has mean 0.691 and min 0.530. The base set was finalised at K = 4. `OPEN_QUESTIONS.md` #21/#23 document that K and the feature set were chosen after these results were seen. This is a garden of forking paths, and the Limitations sentence claiming the structure is invariant is not supported.
- **Fix:** Report every feature set in a supplementary table (silhouette, mean/min Jaccard, ARI for K = 4–8). Give the ARI between the final partition and the partition from each feature set. State plainly that the 27-variable set was chosen after exploration. Delete or rewrite the "same role structure" sentence.

### C3. The bootstrap and cross-period ARI ignore that player-seasons are clustered within players
- **Location:** `methods.qmd:19`; code `archetypes_v2.py:92` (`rng.choice(len(z), …)` over player-seasons) and `:146` (period split).
- **Problem:** The 1,286 player-seasons in the fitting sample come from far fewer players (736 across all 2,014 player-seasons). Resampling player-seasons puts the same player in both the "original" and the "bootstrap" partition through his other seasons, which inflates Jaccard. The cross-period ARI shares players across the 2016–19 and 2020–24 blocks, so it measures player persistence as well as role-structure stability.
- **Fix:** Resample players, with all of each player's seasons kept together (cluster bootstrap). Report how many players appear in both periods and recompute the ARI with those players excluded, or stratified by them.

### C4. The GMM is over-parameterised, misattributed, and applied inconsistently
- **Location:** `methods.qmd:19`; code `archetypes_v2.py:84`, `:155`, `:173–175`.
- **Problem:** (a) A full-covariance GMM in 27 dimensions with K = 5 has about 5 × (27 + 378) + 4 ≈ 2,029 free parameters, against n = 1,286. The fit is only identifiable because of `reg_covar = 1e-3`, which is not reported. No BIC/ICL is given. (b) Several inputs are near-collinear (`assisted_rate`, `assisted2_rate`, `assisted3_rate`; `creator_idx` vs `AST_pct`). (c) The paper cites mclust [@scrucca2016mclust], but the analysis uses scikit-learn `GaussianMixture`. (d) Players under 400 min, and the cross-period predictions, are assigned by **Euclidean nearest centroid** rather than the GMM posterior, so they are effectively in a k-means model, not the stated one.
- **Fix:** Use a constrained covariance (diag/tied, or mclust model selection by BIC), or reduce dimension first (PCA/factor analysis). Report BIC and the covariance structure. Assign all players with `predict_proba` and report posterior membership uncertainty (e.g., the share of players with max posterior < 0.7). Cite the software actually used, with versions.

### C5. Height imputed from registered position makes the role–position result circular
- **Location:** `methods.qmd:15` (height listed as a variable); `results.qmd:38`; code `archetypes_v2.py:56–59` (missing height filled with the **registered-position mean**), `:54` and `:64` (missing advanced, shot and network values filled with 0 before z-scoring).
- **Problem:** Height is one of the most discriminating variables (Fig. 2). Filling it from registered position pushes roles toward positions and inflates Cramér's V (0.735). Neither imputation nor its extent is reported.
- **Fix:** Report missingness per variable. Impute without using position (or drop those cases) and recompute the roles and Cramér's V. Disclose the zero-filling of other variables, or replace it.

### C6. The role–position description does not match Table 2, and one role is mislabelled
- **Location:** `results.qmd:38`; `discussion.qmd:7`; `index.qmd:18` (`ROLE` mapping); `index.qmd:7` (abstract).
- **Problem:** From `role_position.K5_tam`: "Stretch forward" is 80% forwards (447/562), so it does **not** "draw substantially from two positions". "Interior forward" is **64% centres** (141 C vs 79 F; mean height 207.4 cm), so the label is misleading. Only the wing (64% G / 35% F) and, partly, the interior role actually cut across positions. The "positionless middle" conclusion is therefore weaker than stated. Cramér's V has no CI and treats repeated player-seasons as independent.
- **Fix:** Rename role 2 (e.g., "interior big", "non-spacing big"). Rewrite the sentence using `baskin_pozisyon_payi` (0.96 / 0.64 / 0.80 / 0.92 / 0.64). Add a player-cluster bootstrap CI for V. Narrow the positionless claim to the wing role.

### C7. The null result on role composition comes without power analysis, and the penalty is fixed so as to favour the null
- **Location:** `methods.qmd:29`; `results.qmd:44`; `introduction.qmd:7` ("adds no measurable information"); `discussion.qmd:9` ("a good lineup is … a lineup of good players"); code `lineup_model.py:142` (`Ridge(alpha=5000)`, fixed and not reported).
- **Problem:** The composition model's penalty is neither tuned nor reported. A large fixed α can shrink composition effects to about zero by construction, which makes the "no gain" result partly an artefact. RAPM itself explains only 0.36% of test variance. The null 95th percentile of the gain (0.00053) is about 3× the observed gain (0.00019). No minimum detectable effect is given, so readers cannot tell whether a practically meaningful synergy (e.g., 2 pts/100 possessions for a role pair) could have been detected. The Limitations paragraph concedes "absence of evidence", but the Introduction, Abstract and Conclusion state evidence of absence.
- **Fix:** (a) Choose α for the composition model by game-grouped CV and report it. (b) Run a simulation-based power analysis: inject role-pair synergies of 1, 2 and 4 pts/100 poss into the observed segments and report detection rates under the same permutation test. Define a smallest worthwhile effect for net rating and add an equivalence-type statement. (c) Report composition coefficients with bootstrap CIs (game-blocked); the largest is n1×n4 = 1.57. (d) As a secondary analysis, aggregate to lineup-season units to cut noise. (e) Rephrase claims as "did not detectably improve…; effects smaller than X could not be excluded".

### C8. The "four-role" sensitivity check uses a different feature set and B
- **Location:** `results.qmd:44` ("The result was the same with the four-role solution"); `discussion.qmd:9`, `discussion.qmd:15`.
- **Problem:** `lineup_model_K4.roller = "archetypes_v2_advanced.csv"` is the 18-variable set without height or assist network, with **B = 500**, whereas K5 uses B = 1000. It is not the K = 4 solution in Table 1 (full set). Readers will assume it is.
- **Fix:** Re-run with the full-set K = 4 partition and B = 1000, or state explicitly which partition and B were used.

### C9. Selective reporting in the sensitivity analysis, and the prior work it replicates is uncited
- **Location:** `results.qmd:48`; `discussion.qmd:9`; `methods.qmd:19`, `methods.qmd:31`; `index.qmd:7` ("previously used seven-cluster Ward solution").
- **Problem:** (a) For the all-lineups variant, `formula_test_corrected_min0_tezarketip` shows permutation χ² **p = 0.002**, and 92 significant combinations vs 80.3 expected (**p = 0.007**). Both are omitted. The Discussion says the non-random distribution "disappears under a permutation test *and* a minimum-duration filter". It does **not** disappear under the permutation test alone, only with the ≥ 2-min filter. (b) "Earlier work on the same data" and "a previously used procedure" are not cited. This is the author's thesis. It must be cited, and the overlap disclosed to the editor (duplicate-publication policy). (c) The proposed mechanism (losing short lineups are substituted quickly) is asserted, but the supporting evidence already in `results.json` is not shown: unweighted mean NRTG40 is −10.08 vs a minute-weighted 0.56. (d) This analysis uses NRTG per 40 min, whereas the main analysis uses per 100 possessions. That is not stated.
- **Fix:** Report the naive p, permutation p and BH-FDR survivors (56 vs 4) for both variants. Correct the Discussion sentence. Cite the thesis. Show the weighted-vs-unweighted means as direct evidence for the selection mechanism. State the outcome metric.

### C10. The "role-biased valuation index" inference assumes RAPM is ground truth and that its shrinkage is role-neutral
- **Location:** `index.qmd:7` ("box-score valuation indices are role-biased"); `results.qmd:42`; `discussion.qmd:11`; code `lineup_model.py:160–172`.
- **Problem:** (a) VAL40 is never defined in Methods. (b) η² is computed at the **player (career)** level, using each player's main role and a RAPM fitted on **all** seasons including the test period. None of this is described. (c) Ridge RAPM with λ = 4000 shrinks every player toward a common zero (SD 1.5). Small between-role RAPM differences (η² = 0.006) are therefore partly built in, and true role-dependent value could be shrunk away. The pattern is equally consistent with "VAL40 captures real role differences that heavily shrunk RAPM cannot". (d) There are no CIs on η² (0.33 vs 0.006) or on r = 0.269.
- **Fix:** Define VAL40 (PIR per 40 min) and the player-level procedure. Give CIs (player bootstrap). Check sensitivity with a less penalised RAPM and with a role-informed prior (as in L-RAPM [@petridis2026lineup]). Reword to "between-role differences in VAL40 are not mirrored in RAPM", or else show that within-role VAL40 does predict out of time.

### C11. The practical recommendation is untested here and contradicted by the project's own out-of-sample results
- **Location:** `discussion.qmd:11` ("RAPM predicted future lineup outcomes considerably better"); `discussion.qmd:19` (Conclusions: "building lineups … with plus-minus-based measures").
- **Problem:** The only evidence offered is test R² 0.36% (RAPM) vs 0.05% (summed VAL40), with no uncertainty. `results.json["ilp_validation"]` shows that a RAPM-optimised five (vs the team's other lineups) gives **+2.18 [−1.41, 5.42]**, whereas the coach's most-used five gives **+3.84 [1.54, 6.14]**. Selecting lineups by RAPM was therefore not shown to beat coaches. Making the recommendation while this result sits unreported is a selective-reporting problem.
- **Fix:** Either report the ILP/out-of-sample lineup comparison (main text or supplement) and adjust the recommendation, or limit the conclusion to what is tested: "compare players across roles with plus-minus-type measures rather than VAL40". Add a game-blocked bootstrap CI for the R² difference (RAPM vs VAL40). The closing sentence should remain a concrete, *supported* application (Drake & Han, Step 10).

### C12. Inconsistencies between the text, the code, the rendered output and `results.json`
- **Location:** `methods.qmd:11` vs `results.qmd:42–44`; `_output/index.docx`.
- **Problem:** (a) Methods reports 80,460 segments of ≥ 10 s, but the lineup model uses **64,549** segments (`lineup_model_K5.segment_N`; filter `poss ≥ 1` at `lineup_model.py:41`), with 48,309 for training and 16,240 for testing. Neither the exclusion nor the train/test N is reported. (b) The rendered `_output/index.docx` is **stale**: it shows 500 permutations and p = 0.491, has no Fig. 3, and contains an older Discussion that also cites @wei2025enhancing for role effects. The current `results.json` gives B = 1000 and p = 0.5125. (c) The abstract contains no numbers at all, which Q1 journals require.
- **Fix:** Report every filter and the N at each step (a flow diagram is recommended). Re-run `make analysis && make render` before resubmission. Add the key estimates with uncertainty to the abstract (K, Jaccard, V, η², ΔR² and permutation p).

### C13. Literature claims not verified against full text (CLAUDE.md rule 4)
- **Location:** `discussion.qmd:5` ("studies using play-type data distinguish ball handlers, spot-up wings and several types of bigs [@chen2023modeling; @wei2025enhancing]"; "more than a dozen with play-type data [@chen2023modeling; @wei2025enhancing]"); `introduction.qmd:3` (roles "frequently linked to lineup success [@…; @wei2025enhancing]").
- **Problem:** `literature/answers/20261118-…dogrulama.md` records that for @wei2025enhancing only the abstract was available, and it does not verify role counts or role types for either @chen2023modeling or @wei2025enhancing. No `sspe-ask` output exists for any Discussion comparison (`OPEN_QUESTIONS.md` #31).
- **Fix:** Verify the role counts and role labels from the full text (`make ask`) and record them in `literature/answers/`. Drop @wei2025enhancing from any claim beyond what its abstract states.

---

## 4. Minor issues

1. **Unsupported gap claim.** `introduction.qmd:5`: "Most of this evidence comes from the NBA and from national leagues" has no citation. "Lineup-level work [in the EuroLeague] has focused on plus-minus … rather than roles" sits uneasily with [@pendolareinecke2025exploring] (women's EuroLeague roles), so narrow it to the men's EuroLeague.
2. **Relevant uncited literature already in the .bib.** `martonosi2023predicting` (lineups predicted from individual player statistics, which bears directly on "a good lineup is a lineup of good players"), `south2024basketball` (positionless defence), `konca2026from` ("From position to role", 2026, which may overlap in originality) and `muniz2022sports`. Discuss them.
3. **RAPM source.** RAPM is cited to an arXiv preprint [@petridis2026lineup] and to [@grassetti2020extended]. Add the original RAPM/APM methodological source via `sspe-search`/`sspe-doi`. Do not write it from memory.
4. **Unreported RAPM details.** The replacement coefficient (−6.56) and the treatment of players unseen in training (set to 0 = league average, 24.3% of test appearances; `testte_egitimde_gorulen_oyuncu_payi = 0.757`) are not reported. Justify setting unseen players to 0 rather than to replacement level.
5. **Interrupted seasons.** The 2019–20 season was COVID-truncated, 2020–21 was played without crowds (home advantage 4.89 pts/100 may differ), and Russian clubs left in 2021–22. Add a sensitivity analysis, or at least state how these seasons were handled.
6. **Standardisation sample.** Within-season z-scores use all 2,014 player-seasons, including those with 90–400 min and noisy shares (`archetypes_v2.py:66`), while the model is fitted on ≥ 400 min. Justify this, or standardise on the fitting sample.
7. **Ambiguous variable.** "Foul rates" covers both fouls drawn (`FD_pct`) and fouls committed (`PF_pct`). Say so.
8. **Unclear interaction terms.** "All pairwise role products" includes same-role pairs, coded n(n−1)/2. Describe the encoding and the number of terms (5 + 15 = 20).
9. **Mixed units in Table 2.** Player-seasons, height and positions are per player-season; VAL40 and RAPM are per player (career). Say so in the caption.
10. **Figure 2 variable selection.** It shows 11 of 27 variables without saying how they were chosen. Give the rule, and put the full profile in a supplement.
11. **Numeric formatting.** "0.58 vs 0.541" uses inconsistent precision. p is printed to 4 decimals (0.5125, 0.6228). χ² is reported without df. Use APA style (p = .51, χ²(6) = 42.31) and consistent 2–3 decimals.
12. **Weak cluster structure.** Silhouettes are 0.08–0.15. Say so explicitly, and frame roles as regions of a continuum (consider soft membership in the downstream model).
13. **Reporting checklist.** No reporting checklist is supplied (`manuscript/checklists/` is empty). Provide STROBE (observational) items, with software versions and seeds.
14. **Data and code availability.** `index.qmd:35`: "available in the project repository" needs a URL plus a persistent DOI (Zenodo/OSF snapshot). Mention the EuroLeague API terms of use and give the retrieval date. The Limitations sentence "data and code are open" depends on this.
15. **Front matter.** Add affiliation, funding, conflicts of interest and author contributions. The ethics statement is acceptable, but some journals require an explicit waiver statement.
16. **AI statement.** Acceptable. Specify the model/version and that analyses were run by deterministic code, not generated by the AI.
17. **Bibliography metadata.** Several entries are incomplete. `kalman2020lineup` has no venue, URL or DOI; state whether it is peer-reviewed (it may be a student report). `grassetti2020extended` lacks volume, pages and DOI. `wei2025enhancing`, `penner2025player` and `petridis2026lineup` lack DOIs. Re-fetch them via `sspe-doi`.
18. **Season count.** "Nine EuroLeague seasons" includes the truncated 2019–20 season; give the number of games per season.

### Drake & Han (15 steps): structure checks
- **Topic and transition sentences.**
  - *Introduction:* P1 is good: it opens with a topic sentence and closes with a transition ("…rather than how their roles combine"). P2 opens with an uncited gap statement rather than a topic sentence, and its niche (c) conflicts with Pendola-Reinecke. P3 ("Here we show") is a single sentence, which is fine, but it overclaims (see C1 and C7).
  - *Results:* "Number and stability of roles" (`results.qmd:5`) ends on the Ward-7 result with no transition to the role profiles. "The five roles" (`results.qmd:22`) has no substantive topic sentence; it only points to Fig. 2 and Table 2. Open it with what separates the roles (e.g., creation, shot location, size). The sensitivity paragraph (`results.qmd:48`) needs a topic sentence stating why the analysis was run.
  - *Discussion:* P2–P3 are well formed. P4 (`discussion.qmd:9`) is overloaded (null result, critique of prior work, mechanism, implication, caveat) and ends on a caveat rather than a transition; split it. P5 (`discussion.qmd:11`) has two sentences and no supporting numbers. Limitations (`discussion.qmd:15`) is a single paragraph holding six problem–response pairs. Split it, and note that two of the "responses" are unsupported: "the same role structure emerged" (see C2) and "the comparison is fair", which does not address power (see C7).
- **Figure captions.** All three open with a full declarative sentence, which is good. The Fig. 1 claim, however, is contradicted by the figure's own 0.75 line (C1). Table captions (`results.qmd:9`, `results.qmd:26`) are noun phrases; make them full sentences that state the finding.
- **Conclusion ends on a concrete application.** Yes (`discussion.qmd:19`), but the application is not supported (C11). The abstract ends on a warning ("box-score valuation indices are role-biased"), whereas Step 10 asks for a positive, actionable close.

---

## 5. Citation audit

### 5a. Keys in the manuscript against `references.bib`
Method: extracted every `@key` from `index.qmd` and `sections/*.qmd` (excluding `@fig-`/`@tbl-` cross-references) and checked each with `grep -E "^@[A-Za-z]+\{key,"` in `references.bib`.

| Key | Uses | In .bib | Note |
|---|---|---|---|
| chen2023modeling | 5 | yes | Role counts and role types not in the verification file (C13) |
| duman2021cluster | 1 | yes | |
| grassetti2020extended | 3 | yes | Missing volume, pages, DOI |
| hennig2007cluster | 2 | yes | Thresholds verified |
| ibanez2025redefining | 2 | yes | 9 roles verified (abstract) |
| kalman2020lineup | 3 | yes | No venue or DOI; Discussion claim verified against full text |
| kubatko2007starting | 1 | yes | |
| pendolareinecke2025exploring | 2 | yes | 3 roles verified (abstract) |
| penner2025player | 1 | yes | Claim verified against full text |
| petridis2026lineup | 2 | yes | arXiv preprint used as a methods source |
| ribes2026identifying | 2 | yes | Verified (abstract); "Coma Ribes et al." matches the .bib |
| sampaio2006discriminant | 1 | yes | |
| scrucca2016mclust | 1 | yes | Software misattributed: the analysis used sklearn (C4) |
| wei2025enhancing | 4 | yes | Abstract only; Discussion and Introduction claims unverified (C13) |

**Result:** all 14 keys resolve, so there are no missing keys. Content-level problems: C13 (wei2025enhancing, chen2023modeling) and the scrucca2016mclust misattribution (C4).

### 5b. Numbers against `results.json`
Every number in the text is pulled inline from `results.json`, and all the keys resolve. I checked them against the JSON:

- Data: 9 seasons, 2,646 games, 62,912 player-games, 325,151 shots, 83,164 assist edges, 2,014 player-seasons, 736 players, fit_N 1,286, 27 variables. Matches.
- Stints: 80,460 and 99.4%. Matches `paper_a`, **but the lineup model uses 64,549 segments (not reported; C12).**
- Stability: ARI 0.58 / 0.541, Ward-7 Jaccard 0.44 / 0.28. Matches. The Table 1 and Table 2 Jaccard values come from different bootstrap runs (C1).
- Positions: Cramér's V 0.735. Matches, but the narrative misstates the role splits (C6).
- RAPM: 693 players, SD 1.5, home advantage 4.89, η² 0.33 / 0.006, r 0.269, R² 0.00363 / 0.00047 / 0.00382, p 0.5125 with B = 1000, K4 p 0.6228. Matches, **but the K4 run uses a different feature set and B = 500 (C8).**
- Sensitivity analysis: χ² 42.31; 92 combinations, of which 2 positive; χ² 8.85; perm p 0.2318; 28 vs 26.3. Matches, **but the min-0 permutation p values (0.002, 0.007) are omitted (C9).**
- **Mismatch:** `_output/index.docx` shows p = 0.491 with 500 permutations, which differs from `results.json` (p = 0.5125, B = 1000). The rendered output is stale (C12).
- **Unreported result that contradicts the text:** `ilp_validation` (C11).

---

### Summary for the editor
The core idea is publishable and the analysis pipeline is unusually transparent. In revision the authors need to: (i) bring the stability claims in line with their own threshold; (ii) disclose and report the feature-set exploration; (iii) fix the bootstrap unit, the GMM specification and the height imputation; (iv) support the null composition result with a tuned penalty and a power/minimum-detectable-effect analysis; (v) report the omitted sensitivity and ILP results; (vi) cite the prior thesis; and (vii) re-render the manuscript so the output matches `results.json`.
