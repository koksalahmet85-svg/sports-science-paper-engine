# Review – Round 2

**Manuscript:** "Box-score performance indices depend on player role and show no advantage over coaches' rotations for lineup selection: an out-of-sample evaluation in EuroLeague basketball"
**Reviewer role:** Senior reviewer (Q1 sports science / sports analytics)
**Date:** 2026-11-18
**Material reviewed:** `manuscript_b/index.qmd`, `manuscript_b/sections/{introduction,methods,results,discussion}.qmd`, `manuscript_b/figures/fig1–3`, rendered `manuscript_b/_output/index.docx` (rendered after the last source edit; inline values checked in the docx), `manuscript/references.bib`, `manuscript/analysis/results.json` (keys `paper_b_values`, `ilp_validation`, `lineup_model_roles_final_K5`, `roles_final`, `paper_a`), `manuscript/analysis/{paper_b_values,ilp_validation,lineup_model}.py`, `literature/answers/20261118-rol-dizilim-calismalari-dogrulama.md`, `manuscript/OPEN_QUESTIONS.md`, `manuscript_b/reviews/round-1.md`.

---

## 1. Decision

**Major revision.** The revision is substantial and in good faith. C1 and C10 are closed. The circularity and reliability problems (C3, C4) are now handled with a criterion-conditional analysis, a non-PIR role partition and split-half reliability. Paired contrasts were added. But two new blocking problems have appeared. First, the abstract and Discussion state that only RAPM had a CI excluding zero, while results.json shows that first-half minutes did too. Second, the "paired" ILP-versus-coach difference is in fact a difference between two contrasts with different reference groups and team-season sets, and the Limitations defend it with an unsupported "not biased in either direction". The prior work (thesis, Paper A) is still not formally cited. Several round-1 items are also only partly addressed: no SWC or equivalence margin, no common-sample analysis out of time, an untested "add little beyond the coach" claim, and no archived provenance.

## 2. Scores (1–5)

| Criterion | R1 | R2 | Comment |
|---|---|---|---|
| Originality | 3 | 3 | The contribution is clearer, but the Introduction still has only 8 sources. It does not engage with positional box-score literature (`sampaio2006discriminant`) or EuroLeague role work (`konca2026from`), both already in the .bib. |
| RQ–design fit | 3 | 4 | Aim 1 is now matched by a criterion-conditional analysis. Aim 3 has a coach contrast, but see N2. |
| Internal validity | 2 | 3 | Circularity and information asymmetry are largely handled. Remaining problems: the replacement-level asymmetry out of time, ILP–coach contrasts with non-common reference groups, conditioning on a noisy criterion (RAPM reliability 0.59), and role labels for the constrained ILP that use full-season data. |
| Statistics | 2 | 3 | Paired differences and a common-subset analysis were added. Still missing: an SWC or equivalence margin, a multiplicity framing, joint (incremental) models, CIs for the conditional role contrasts and the corrected η², and point estimates for the R² differences. |
| Reporting-guideline compliance | 2 | 3 | Possession share, team-seasons and overlap are now reported. Still missing: the STROBE flow diagram and checklist, a reconciliation of segment counts, a correct threshold disclosure (60 vs 90 min), software/seed/GMM details, declarations and hard-coded numbers. |
| Discussion tied to evidence | 2 | 3 | Much improved. Overstatements remain in `discussion.qmd:7` ("only measure clearly associated", "add little") and in `discussion.qmd:13` ("similar results", "conclusions unchanged", "not biased in either direction"). |
| Practical implication | 3 | 3 | "Benchmark lineup tools against the coach" is supported. "Do not compare PIR across roles without role-specific reference values" is sensible, but the remedy (role-normalised PIR, OPEN_QUESTIONS #22) is not tested. Without an SWC, "no advantage" gives practitioners no usable bound. |

Accept is not possible until every score is ≥ 4 and all critical issues are closed.

---

## 3. Point-by-point status of round-1 critical issues

| # | Round-1 issue | Status | Evidence / remaining action |
|---|---|---|---|
| C1 | "More than doubled" SD | **Resolved** | `results.qmd:7` now reads "increased the spread (SD 1.64 to 3.03)", read inline from `rapm_sd`. |
| C2 | Citation misattribution; uncited prior work | **Partly resolved** | `martonosi2023predicting` is now used for "lineup quality can be predicted from individual player data", which the verification file supports. `muniz2022sports` is reduced to near title level. `petridis2026lineup` is removed. `kubatko2007starting` is now cited only for the possession formula. **Open:** the thesis is mentioned in prose (`introduction.qmd:3`, `methods.qmd:9`) but has no reference entry, and Paper A ("a companion analysis", `methods.qmd:13`) is not cited at all. Carried forward as **K3** below. |
| C3 | Circular roles; η² ≠ bias | **Largely resolved** | The overlap is now disclosed (`methods.qmd:13`). Partial η² conditional on RAPM (0.33, CI 0.27–0.40) and a non-PIR partition (η² 0.32) are reported. Residual problems are listed as major item M1. |
| C4 | Reliability confound | **Largely resolved** | Split-half Spearman–Brown reliability is 0.91 for PIR40 and 0.59 for RAPM (n = 485). Corrected η² is 0.36 for PIR40 and 0.02 for RAPM. These match `guvenirlik` and `eta2_duzeltilmis`. ω²/ε² and CIs for the corrected η² are still missing (minor). |
| C5 | Unequal information; VAL40_havuz omitted | **Largely resolved** | Pooled PIR40 and VAL40 are reported (`results.qmd:29`, Fig. 2) and matched to RAPM's information set. RAPM from the first half only was not added, which is acceptable. The Limitations still spin the result (M3). |
| C6 | Unequal samples; replacement asymmetry; thresholds | **Partly resolved** | Within season: a common subset (77%) and paired differences were added. Out of time: no common-sample analysis, the box-score models still have no low-minutes indicator, and the share of test appearances by players seen in training (0.757) is not reported. The disclosed threshold is wrong for the out-of-time PIR (M2). |
| C7 | Inference by comparing significance levels; equivalence wording | **Partly resolved** | Paired differences were added for both slopes and ILP contrasts, and the Limitations now say "absence of evidence … rather than equivalence". **Open:** no SWC or ROPE, no multiplicity framing, and equivalence wording remains in the Fig. 3 caption, the Table 2 caption and the abstract (M4). |
| C8 | ILP design reporting; endogeneity | **Partly resolved** | Possession share, team-seasons and overlap with the coach five (2.75–3.19) are now reported. Constrained coach benchmarks are defined, and the optimiser's curse is cited and discussed. **New problem** in how the "paired" contrast is built (N2, critical). |
| C9 | Untested "add little"; RAPM recommendation contradicts ILP | **Partly resolved** | The Conclusions now limit RAPM to cross-role player comparison, which is good. "Box-score indices thus appear to add little to what coaches already reveal through playing time" (`discussion.qmd:7`) is still untested: there is no joint minutes + value model. The paper also does not explain why RAPM-optimised fives have the lowest paired differences (−1.66, −0.37, −1.08) (M5). |
| C10 | Results/code mismatch; provenance | **Partly resolved** | `lineup_model_roles_final_K5` now contains `ayristirma`, so the stored output matches the current code. Commit hash and package versions are still not recorded in results.json, and archiving is still deferred "on acceptance" (`index.qmd:47`) (M8). |

---

## 4. Critical issues (block publication)

### N1. The abstract and Discussion contradict results.json on which measures predict within season
- **Location:** `index.qmd:33` ("Within seasons, only RAPM-based lineup value had a confidence interval excluding zero") and `discussion.qmd:7` ("RAPM-based lineup value was the only measure clearly associated with second-half performance").
- **Evidence:** `ilp_validation.amac_fonksiyonu_egimi.DAKIKA` = 1.07 (95% CI 0.02 to 1.98). First-half minutes, which the Methods define as one of the compared measures (`methods.qmd:21`), also excluded zero in the full sample. The Results text (`results.qmd:29`) reports this correctly, so the abstract and Discussion disagree with the paper's own Results. "Clearly" is also not justified for RAPM in the common subset (1.10, CI 0.12 to 2.15).
- **Fix:** Write "only RAPM and the coach's own minutes allocation had confidence intervals excluding zero (in the common subset, only RAPM); paired differences between measures included zero". Drop "clearly".

### N2. The "paired" ILP-versus-coach difference is not a paired comparison, and the Limitations defend it with an unsupported statement
- **Location:** `methods.qmd:25`, `results.qmd:35`, Table 2, Fig. 3, `discussion.qmd:13` ("because the coach benchmark was evaluated in the same way, the comparison is not biased in either direction"). Code: `ilp_validation.py:173–190`.
- **Problem:**
  - Each contrast is (segments with ≥ 4 of five X) minus (all *other* segments of the team-seasons in which X was observed). The "paired difference" is contrast(ILP) − contrast(coach).
  - The two contrasts have different reference groups. The coach five's segments sit in the ILP reference group, and vice versa.
  - They also cover different team-season sets (e.g. 124 vs 155 for VAL40/none, 105 vs 129 for VAL40/rim protector).
  - Because the fives share about three players, many segments can count in both the ILP and the coach group. This share is not reported, and the overlap pulls the difference towards zero mechanically.
  - Resampling team-seasons jointly does not make this a within-team-season paired contrast.
  - Coach-five segments (17.9% of possessions) and ILP-five segments (5–9%) occur in different game states (starts of quarters, closing time, garbage time), and the two are selected differently by the coach. "Not biased in either direction" is therefore an assertion, not a result.
- **Fix:**
  1. Restrict to team-seasons in which both fives were observed. Within each team-season compute mean y_adj(ILP five) − mean y_adj(coach five), possession-weighted, and average across team-seasons. Report the n of team-seasons.
  2. Report the share of segments that qualify for both groups, and repeat the analysis with those segments excluded (or attributed to one group only).
  3. Optionally adjust for game state (quarter, score margin at segment start), or add a deployment-independent evaluation such as held-out RAPM-predicted value of each five.
  4. Delete "not biased in either direction". Describe the selection mechanism and the direction of bias it could introduce.

### K3. Prior work is still not formally cited (carried over from C2)
- **Location:** `introduction.qmd:3` and `methods.qmd:9` ("the author's doctoral thesis"), `methods.qmd:13` ("a companion analysis"), `methods.qmd:25` ("the constraint used in earlier work").
- **Problem:** The role solution, the VAL40 definition and the rim-protector constraint come from the thesis and from Paper A (`roles_final`). Neither has a reference entry. Journals require related or overlapping submissions to be cited and disclosed to the editor; otherwise the paper risks being treated as duplicate or salami publication.
- **Fix:** Add both to references.bib, the thesis as `@phdthesis` and Paper A as a preprint or "under review" entry, using the project's add-source workflow. Cite them at each location above. In the Introduction, add one sentence on what is new relative to them.

---

## 5. Major issues

**M1. Remaining construct problems in the role-dependence analysis** (`methods.qmd:13`, `results.qmd:7`, `index.qmd:33–34`, `discussion.qmd:5,17`)
- (a) The "non-PIR" partition is not free of PIR components. `pir_bilesensiz_roller.degiskenler` includes `USG_pct`, which is computed from FGA, FTA and TOV (missed shots and turnovers are PIR terms). It also includes `second_chance_rate` (downstream of offensive rebounds) and `fastbreak_rate` (points). **Fix:** describe the variables accurately. Re-run without USG_pct and second_chance_rate. Report bootstrap CIs and the ARI with the main partition.
- (b) "Players with the same on-court impact" treats estimated RAPM as true impact. RAPM's reliability is 0.59, so conditioning on it leaves residual confounding. **Fix:** say "the same estimated RAPM". Add an errors-in-variables sensitivity analysis (regression calibration with the reported reliability, or SIMEX). State the criterion assumption explicitly.
- (c) The conditional role contrasts (`rol_farki_RAPM_sabit`) have no CIs, and only two of four are reported. Ball handlers are also rated +4.54 PIR/40 above stretch forwards at equal RAPM. The summary "interior roles are rated higher" (abstract, Introduction, Conclusions) is therefore incomplete; the pattern is "stretch forwards and wings are rated lower than all other roles". **Fix:** report all four contrasts with bootstrap CIs, for example in Table 1, and reword.
- (d) The terminology is still inconsistent. The abstract Purpose and the Methods use "role bias … quantified as η²", but η² alone measures dependence, not bias. Reserve "bias" for the RAPM-conditional analysis.

**M2. Out-of-time comparison: unequal handling not addressed and thresholds misreported** (`methods.qmd:9,17`; `lineup_model.py:131–149`)
- The Methods state a 60-minute threshold for all box-score values. The out-of-time PIR40 uses ≥ 90 training minutes. The out-of-time VAL40 is a minutes-weighted mean of player-season VAL40 with no minimum.
- RAPM gives low-possession players the replacement coefficient (−6.56), while box-score predictors give them the league mean. RAPM therefore carries a minutes signal that the box-score models lack.
- The within-season results show this matters: the RAPM slope falls from 1.76 to 1.10 in the common subset.
- **Fix:** Report the actual thresholds. Report the share of test appearances by players seen in training (75.7%). Re-estimate test R² on test segments in which all ten players have defined values under every measure, or give the box-score models the same low-minutes indicator. Report point estimates of the R² differences as well as the CIs.

**M3. Limitations overstate robustness** (`discussion.qmd:13`)
- "Box-score values pooled over the same period gave similar results": pooled VAL40 nearly doubled the slope (0.54 → 0.95), and with matched information the RAPM − VAL40 difference was 0.36 (CI −0.84 to 1.55).
- "The conclusions were unchanged in the subset": in the common subset the minutes slope lost significance (0.62, CI −0.50 to 1.62) and the RAPM slope fell by about a third.
- **Fix:** Report these changes plainly. State that, with matched information and samples, RAPM's within-season advantage over box-score values is not established. Its advantage rests on the out-of-time test, which itself needs M2.

**M4. No SWC/equivalence margin or multiplicity framing; equivalence wording remains**
- The ILP − coach CIs run from lower limits of −5.84 to −4.14 up to upper limits of 2.03 to 5.13 points per 100 possessions. Without a pre-specified smallest worthwhile change, "did not differ" (abstract), "do not outperform" (Table 2 caption) and "perform no differently" (Fig. 3 caption) read as equivalence.
- **Fix:** Define an SWC for lineup net rating, for example anchored to the net rating per extra win, or 0.2 × the between-team-season SD of net rating, and justify it. Classify each CI as clear, trivial or unclear against that SWC. Rephrase the captions and abstract as "not shown to outperform; differences of up to about 5 points in either direction cannot be excluded". State that the slopes and the 9 + 9 contrasts are interval estimates without multiplicity adjustment.
- The Fig. 2 caption ("RAPM, unlike box-score indices, is associated") also states an untested contrast and ignores the minutes result. Change it to a description.

**M5. "Add little beyond the coach" remains untested, and the RAPM-ILP result is unexplained** (`discussion.qmd:7,9`)
- **Fix:** Fit joint models (minutes + PIR40_havuz; minutes + RAPM) within season and report the partial slopes of the value measures with team-season bootstrap CIs. Otherwise delete the sentence.
- Discuss explicitly why the measure with the best predictive validity produced the lowest point estimates against the coach (RAPM: −1.66 / −0.37 / −1.08). Plausible reasons are lower overlap with the coach five (2.75), selection of low-minute high-RAPM players and the optimiser's curse. The overlap and possession-share data already allow a first look.

**M6. Look-ahead leakage in the constrained ILP** (`ilp_validation.py:74–75,97`)
- The roles used for the rim-protector and balanced constraints are full-season player-season labels (`roles_final_K5.csv`), so they use second-half data. The effect is probably small and applies to the coach benchmark too, but it contradicts "information available at the split only" (`methods.qmd:21`).
- **Fix:** Use previous-season roles, or roles refitted on first-half data. At minimum, disclose the leakage.

**M7. STROBE compliance is still incomplete**
- There is no flow diagram and no checklist. Segment counts are not reconciled: 64,549 (lineup model), 64,324 (`ilp_validation.segment_N`, which counts team-segments because each segment is mirrored), 64,125 (Paper A).
- There are 156 team-seasons in the slope analysis but 155 for the coach contrast.
- Methods details are missing: software and versions, random seed (20261111), GMM covariance (`tied`), K selection and stability, playoff handling, and how traded players are handled (they enter each team's ILP pool separately).
- **Fix:** Add a supplementary flow diagram, the STROBE checklist and a short "Statistical analysis / software" paragraph. State that mirrored rows place each segment in two clusters, and justify one-way team-season clustering or run two-way (game × team-season) clustering as a sensitivity analysis.

**M8. Provenance** (`index.qmd:47`)
- **Fix:** Record the git commit hash and package versions in results.json, for example as `meta`. Tag the release and archive it on Zenodo with a DOI *before* resubmission, not "on acceptance".

---

## 6. Minor issues

1. **Spurious precision in the abstract.** The rendered abstract reads "32.70%", "1.20%" and "33.10%". Use η² = 0.33 / 0.01 / 0.33 (format with 0 decimals for percentages, or report η² values directly).
2. **The abstract has no quantitative results for aims 2–3.** Add the out-of-time R² values and difference (e.g. 0.36% vs 0.11%; difference 0.10 to 0.39 pp), the RAPM and minutes slopes with CIs, and the range of ILP − coach differences.
3. **Hard-coded numbers** (CLAUDE.md rule 2): "400 minutes" in the Table 1 and Fig. 1 captions (`results.qmd:11,21`; `V["asgari_dakika"]` exists), "λ = 1,000", "300 possessions", "60 minutes", "five-fold", "500 bootstrap resamples", "100 first-half minutes", "2016–2022 / 2023–2024". Write each to results.json and read it inline. The main λ (4000, `lambda_ana`) is not reported at all; report it with the CV grid.
4. **VAL40 definition** (`methods.qmd:9`). "Omits fouls and blocked shots" is ambiguous, because blocks *made* are included (`BlocksFavour`). Write "omits fouls drawn, fouls committed and own shots blocked by opponents".
5. **Uncited mechanism** (`discussion.qmd:5`): "creating space, drawing defenders, making the extra pass" and "coaches observe … defence, matchups, health" (`discussion.qmd:9`). Mark these as hypotheses or support them with sources found through the project's literature-search workflow.
6. **Literature positioning.** The Introduction does not cite studies of positional differences in game statistics or EuroLeague role work already in the .bib. Add 2–4 sources through the `sspe-ask` pipeline. `smith2006optimizer` has no entry in `literature/answers/`; add a verification note.
7. **Bibliography quality.** `grassetti2020extended` lacks DOI, volume and pages, and `kalman2020lineup` lacks a venue. Complete them via `sspe-doi`. There is still no primary peer-reviewed source for player-level ridge RAPM; Grassetti et al. is an extended lineup variant.
8. **Fig. 1** has no uncertainty. Add bootstrap CIs for the role means, or show the RAPM-conditional contrasts with CIs instead.
9. **Typography.** Rendered negative numbers use hyphens ("-0.60"); use U+2212. There are nested parentheses in `results.qmd:29` ("PIR40 0.51 (95% CI …)"). Season notation is still mixed ("2016–2022" vs "2016–17 to 2024–25").
10. **Out-of-time target alignment.** RAPM is fitted to segment net rating, the same outcome it is later tested on; PIR is not. Acknowledge this in the Limitations next to the "does not presuppose that RAPM is correct" argument.
11. **η² refinements.** Report ω² or ε² (the in-sample η² is upward-biased), and give bootstrap CIs for the reliability-corrected η² and the λ-grid sensitivity (500–8000).
12. **Role-normalised objective (OPEN_QUESTIONS #22).** The Discussion recommends "role-specific reference values" but does not test them. Add within-role standardised PIR40 as a value measure in Fig. 2 and Fig. 3, or justify omitting it.
13. **Declarations missing:** affiliation, ORCID, funding, competing interests, author contributions. The AI-use statement is adequate. The ethics statement is adequate.
14. **Generalisation** (`discussion.qmd:5`). "In scouting or contract decisions" goes beyond a EuroLeague, net-rating-criterion study. Add "in EuroLeague-level competition" or similar.

---

## 7. Citation audit

`grep` of every `[@key]` in `manuscript_b/index.qmd` and `sections/*.qmd` against `manuscript/references.bib`:

| Key | Uses | In .bib | Content check |
|---|---|---|---|
| muniz2022sports | 2 | Yes | Title-level use ("OR approaches to team building", "optimisation approaches to team building"), which the verification note allows. OK. |
| grassetti2020extended | 3 | Yes (no DOI/volume) | OK for EuroLeague RAPM. Weak as the sole method source (minor 7). |
| kubatko2007starting | 1 | Yes | OK (possession formula). |
| ribes2026identifying | 1 | Yes | OK. |
| kalman2020lineup | 1 | Yes (no venue) | OK. |
| smith2006optimizer | 2 | Yes | Use matches the title (optimiser's curse). No verification note (minor 6). |
| martonosi2023predicting | 1 | Yes | Now matches the verification note. OK. |
| hennig2007cluster | 1 | Yes | OK. |

All 8 keys resolve and no keys are missing. **Uncited prior work:** the thesis and Paper A (K3).

## 8. Number consistency with results.json (checked in the rendered docx)

| Claim (location) | results.json | Status |
|---|---|---|
| 9 seasons, 2,646 games; 64,549 segments | `paper_a`, `lineup_model…segment_N` | OK |
| η² 0.33 (0.27–0.40), 0.42 (0.36–0.49), 0.01 (0.00–0.04) | `eta2`, `eta2_GA95` | OK |
| Partial η² 0.33 (0.27–0.40); +6.5 / +6.8 PIR/40 for interior big / rim protector vs stretch forward | `RAPM_kosullu.PIR40` (role 2 = 6.46, role 4 = 6.77; reference role 1 = stretch forward) | OK. Ball handler +4.54 omitted (M1c). |
| Non-PIR roles η² 0.32 / 0.02 | `pir_bilesensiz_roller.eta2` | OK (but see M1a). |
| Reliability 0.91 / 0.59 (n = 485); corrected η² 0.02 / 0.36 | `guvenirlik`, `eta2_duzeltilmis` | OK |
| SD 1.64 → 3.03; η² λ1000 0.01; r = 0.24 | `rapm_sd`, `eta2.RAPM_l1000`, `korelasyon` | OK (C1 closed) |
| Table 1 role means and n (sum 519) | `rol_ortalamasi_ham`, `rol_N` | OK |
| Test R² 0.36 / 0.11 / 0.05%; difference CIs 0.10–0.39, 0.17–0.45 pp | `test_R2` | OK |
| Slopes RAPM 1.76 (0.90–2.64), minutes 1.07 (0.02–1.98), PIR40 0.51, PIR40_havuz 0.78, VAL40_havuz 0.95 | `amac_fonksiyonu_egimi` | OK in Results. **The abstract (`index.qmd:33`) and Discussion (`discussion.qmd:7`) "only RAPM" claim contradicts the DAKIKA CI (N1).** |
| Coverage 83%; common subset 77%; RAPM 1.10 (0.12–2.15); paired CIs −0.65–1.75, −0.57–1.60 | `kapsam`, `ortak_alt_kume` | OK. The RAPM − VAL40_havuz difference (−0.84–1.55) and the point estimates of the differences are not reported. |
| Coach 3.84 (1.35–6.13) | `ilp_beslisi.DAKIKA_yok` | OK |
| Overlap "about three of five" | `antrenor_beslisiyle_ortak_oyuncu` 2.75–3.19 | OK |
| Paired differences −1.66 to 0.38; all CIs include 0; "±4–5" | `ilp_antrenore_gore_fark` | Numbers OK. The CIs are asymmetric (lower limits −5.84 to −4.14, upper limits 2.03 to 5.13); report the limits instead of "±4–5". The construction of the contrast is flawed (N2). |
| "Box-score values pooled … gave similar results"; "conclusions were unchanged in the subset" (`discussion.qmd:13`) | VAL40 0.54 → 0.95; minutes 1.07 → 0.62 (CI includes 0); RAPM 1.76 → 1.10 | **Overstated (M3).** |

## 9. Checklist

| Item | Status |
|---|---|
| Sample justification | Partly: the 400-minute and 100-minute thresholds are stated but not justified; there is no precision or power rationale for the lineup contrasts. |
| Clustered data | Team-season bootstrap is used. Mirrored rows and two-way clustering are not discussed (M7). |
| Multiple comparisons | Not addressed (M4). |
| Effect size + CI | Yes, throughout. CIs are missing for the conditional contrasts and the corrected η² (M1c, minor 11). |
| SWC/TE | **Absent** (M4). |
| Causal language | Generally appropriate for observational data ("associated", "depend on"). "Follows from their construction" and "so their rotations already favour the best players" are interpretive and should be flagged as such. |
| Limitations | Present and mostly paired with responses. Three responses overstate (M3, N2). |
| Over-generalisation | Minor (minor 14). |
| MBI | Not used (good). |
| p-hacking signals | Many variants (2 information sets × 3 measures × 3 constraints) and no pre-registration. Because everything is reported, selective reporting is not suspected. State that the variants were specified before outcome analysis, if true. |
| Data/code availability | Public API and a GitHub repository. DOI archive deferred (M8). |
| AI statement | Present and adequate. |
