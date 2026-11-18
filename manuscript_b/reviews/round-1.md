# Review – Round 1

**Manuscript:** "Box-score performance indices are role-biased and weak guides to lineup decisions: an out-of-sample evaluation in EuroLeague basketball"
**Reviewer role:** Senior reviewer (Q1 sports science / sports analytics: JSS, IJSPP, JQAS; JORS for the optimisation part)
**Date:** 2026-11-18
**Material reviewed:** `manuscript_b/index.qmd`, `manuscript_b/sections/{introduction,methods,results,discussion}.qmd`, `manuscript_b/figures/fig1–3`, `manuscript_b/OUTLINE_15steps.md`, `manuscript/references.bib`, `manuscript/analysis/results.json` (keys `paper_a`, `paper_b_values`, `lineup_model_roles_final_K5`, `ilp_validation`; `roles_final.degiskenler` for the role features), `manuscript/analysis/{paper_b_values,lineup_model,ilp_validation,roles_final,figures_paper_b}.py`, `literature/answers/20261118-rol-dizilim-calismalari-dogrulama.md`, `manuscript/OPEN_QUESTIONS.md`.

---

## 1. Decision

**Major revision.** The question matters, the data are open and the out-of-time and within-season designs are a real step up from in-sample box-score studies. However, the three headline claims all go further than the evidence supports. "Role-biased" rests on an η² that is partly circular, because the roles are clustered on PIR components. "Weak guides" rests on comparisons that give RAPM more data and a different, easier sample. "No better than the coach" rests on overlapping CIs rather than paired differences or an equivalence margin. There is also one numerical claim that contradicts results.json and two citations whose content is misattributed.

## 2. Scores (1–5)

| Criterion | Score | Comment |
|---|---|---|
| Originality | 3 | Out-of-sample and coach-benchmarked evaluation of PIR is useful. "Box-score indices favour bigs" is well known informally, and the paper does not position itself against literature on PIR or positional box-score differences. |
| RQ–design fit | 3 | Aim 1 is measured with a statistic (η²) that cannot separate bias from true role differences. Aim 3 asks whether ILP five-player lineups "outperform" the coach's choice, but there is no paired ILP-minus-coach contrast. |
| Internal validity | 2 | Roles are defined on PIR components (circularity). Information sets are unequal (RAPM uses all prior seasons, PIR the first half only). Analytic samples are unequal (68% vs 100% coverage). Replacement-level asymmetry. The ILP evaluation is endogenous to coach deployment. |
| Statistics | 2 | Inference by comparing significance levels. No paired differences. No SWC/equivalence margin. Uncorrected in-sample η² with no reliability correction. Mirrored team-perspective rows. 17 interval estimates with no multiplicity framing. |
| Reporting-guideline compliance | 2 | STROBE is claimed but there is no flow diagram and no checklist. A pre-specified analysis (VAL40 on all prior data) is omitted from the text. Inclusion thresholds (60/90 min) are undisclosed. The possession share and team-season n per ILP variant (promised in the outline) are missing. Several numbers are hard-coded. |
| Discussion tied to evidence | 2 | Equivalence and "add little" claims are untested. The shrinkage artefact is "excluded" without a reliability analysis. The mechanism (spacing, off-ball value) is uncited. The RAPM recommendation for lineups contradicts the ILP results. |
| Practical implication | 3 | "Benchmark lineup tools against the coach's rotation" is concrete and well supported in spirit. "Use RAPM for lineups" is not supported by Fig. 3. |

Accept is not possible until every score is ≥ 4 and all critical issues below are closed.

---

## 3. Critical issues (block publication)

### C1. A numerical claim contradicts results.json
- **Location:** `sections/results.qmd:5` ("which more than doubled the spread of RAPM values (SD 3.03 vs 1.64)").
- **Problem:** `paper_b_values.rapm_sd` gives l1000 = 3.03 and ana = 1.64. The ratio is 1.85, so the spread did not "more than double".
- **Fix:** Write "nearly doubled" or "increased the SD by 85%". Better still, compute the ratio inline from results.json so the wording cannot drift from the numbers.

### C2. Citation content is misattributed or unverified; prior work is uncited
- **`[@martonosi2023predicting]`** is cited at `introduction.qmd:5` ("the coach's rotation is the natural benchmark that any decision aid must beat") and at `discussion.qmd:9` ("coaches observe information that box scores do not record … so their rotations are a strong benchmark"). According to `literature/answers/...dogrulama.md`, this paper classifies elite NBA lineups from individual player order statistics. It says nothing about coach rotations as a benchmark, so neither sentence is supported. **Fix:** Either remove the citation and present the sentences as the authors' argument, or find a source via `sspe-search`/`sspe-ask` that actually makes the claim.
- **`[@muniz2022sports]`** is cited at `introduction.qmd:3` ("decision-support frameworks have used them, or predictions of them, as inputs for lineup and roster optimisation with integer programming") and at `discussion.qmd:9`. The verification file states explicitly that the abstract is unavailable and the paper "can be cited only at title level". The manuscript makes specific content claims about it (box-score inputs, integer programming), which breaks CLAUDE.md rule 4. **Fix:** Verify against the full text, or reduce the claim to title level.
- **`[@petridis2026lineup]`** (arXiv preprint, not checked in literature/answers) is used as the methodological authority for player-level ridge RAPM at `methods.qmd:9` and `discussion.qmd:5`. That preprint is about *lineup* RAPM with informed priors, not the player RAPM specified here. **Fix:** Add a peer-reviewed primary RAPM source via `sspe-search`/`sspe-doi`, and keep the preprint only where it is actually relevant.
- **`[@kubatko2007starting]`** is cited for "comparable linear indices are used in the NBA" (`introduction.qmd:3`). Kubatko et al. is a source for possession and rating definitions, not for linear composite indices. **Fix:** Keep it for the possession formula (`methods.qmd:5`) and find a proper source for the NBA-index sentence.
- **Uncited prior work:** "a closely related composite used in earlier work on these data" (`methods.qmd:9`) and "the constraint used in earlier work" (`methods.qmd:25`) refer to the author's thesis. The role solution comes from the companion Paper A (`roles_final`). Neither is cited. This is a transparency and duplicate-publication issue. **Fix:** Cite the thesis and Paper A (as a preprint or under review) and state what is new here.

### C3. The role-bias construct is circular, and η² does not equal bias
- **Location:** `methods.qmd:13`, `results.qmd:5`, title, `abstract (index.qmd:32–33)`, `discussion.qmd:5`.
- **Problem (circularity):** `results.json["roles_final"]["degiskenler"]` shows the clustering inputs include ORB_pct, DRB_pct, BLK_pct, STL_pct, AST_pct, TOV_pct, FD_pct and PF_pct. Those are rate versions of nearly every PIR component. The Methods describe them only as "possession shares", which hides this. Roles defined from PIR's ingredients will mechanically explain PIR variance, so η²(PIR) = 0.33 is inflated by construction.
- **Problem (construct):** A high η² shows that PIR *differs* between roles, not that it is *biased*. Rim protectors could genuinely be more valuable. Bias needs an external criterion.
- **Fix:**
  1. Define bias relative to a criterion, for example the role effect in PIR z-scores conditional on RAPM (or in PIR − predicted-from-RAPM residuals), with a bootstrap CI.
  2. Re-derive roles using only features that are not PIR components (shot location plus assist network) and report η² under that role solution as a sensitivity analysis.
  3. Describe the clustering variables accurately in `methods.qmd:13`.
  4. Unless 1–2 support it, soften "role-biased" in the title to "role-dependent".

### C4. η² comparisons are confounded by measurement reliability
- **Location:** `results.qmd:5`, `discussion.qmd:5` ("so it is not an artefact of shrinkage").
- **Problem:** RAPM is far noisier between players than per-40 box-score rates. A measure that is mostly noise has η² near 0 whatever its true role structure. The λ = 1,000 sensitivity changes the scale (SD ×1.85) but not the signal-to-noise ratio; η² is scale-invariant, so this check cannot rule out the artefact. Also, the in-sample η² (`paper_b_values.py:27–29`) is upward-biased, and PIR40 per-40 values for 400-minute players are themselves noisy.
- **Fix:**
  - Report the split-half (odd/even games) or season-to-season reliability of each measure.
  - Report η² for each measure divided by its reliability (disattenuated), or its role structure in a measurement-error model.
  - Report ω² or ε² alongside η².
  - Remove "so it is not an artefact of shrinkage" unless the reliability analysis supports it.

### C5. Unequal information in the within-season test, and selective reporting
- **Location:** `methods.qmd:21`, `results.qmd:27`, abstract `index.qmd:32`, `ilp_validation.py:79–89`.
- **Problem:** RAPM is fitted on all earlier seasons plus the first half. PIR40 and VAL40 use the first half only. The pre-specified VAL40 on all prior data (`VAL40_havuz`) is listed in the Methods and plotted in Fig. 2, but omitted from the Results text and the Abstract. Its slope is 0.95 (95% CI −0.09 to 2.02), roughly halfway between first-half VAL40 (0.54) and RAPM (1.76). Part of RAPM's advantage is therefore an information advantage, and omitting the analysis that shows this is selective reporting.
- **Fix:**
  - Report VAL40_havuz in the Results text and the Abstract.
  - Add PIR40 on pooled prior data.
  - Add RAPM from the first half only.
  - Present the comparison at matched information sets.

### C6. Unequal analytic samples and asymmetric replacement-level handling
- **Location:** `results.qmd:27` (coverage 68% vs 100%), `discussion.qmd:13`, `ilp_validation.py:47,53` (undisclosed ≥ 60 first-half minutes), `lineup_model.py:52–61,137–149` (undisclosed ≥ 90 training minutes for PIR; unseen players or those below 90 min get the league mean).
- **Problem:** The RAPM slope is estimated on all segments, including bench and garbage-time lineups. There, the replacement coefficient (`yedek_katsayisi` = −6.56 per player) creates a large, easily predicted spread. PIR and VAL are estimated on the 68% of segments where every player has ≥ 60 minutes. In the out-of-time test, RAPM likewise has a low-minutes penalty built in, while box-score predictors assign the league mean. The comparisons are therefore partly "minutes-proxy vs no minutes-proxy" and use different samples. Limitations (`discussion.qmd:13`) name the problem but offer no response.
- **Fix:**
  - Re-estimate all slopes and all test R² on the common subset of segments where every measure is defined.
  - Give the box-score models the same low-minutes indicator.
  - State the 60 and 90 minute thresholds and the share of test appearances by players seen in training (`testte_egitimde_gorulen_oyuncu_payi` = 0.757) in the Methods.

### C7. Inference by comparing significance levels, and unsupported equivalence claims
- **Location:** title ("weak guides"), `index.qmd:32–33`, `introduction.qmd:7`, `results.qmd:27,33`, `discussion.qmd:3,7,9,17`.
- **Problem:**
  - "RAPM … strongest association" and "box-score … none distinguishable from zero" are based on separate CIs. The CI of PIR (−0.60 to 1.64) overlaps that of RAPM (0.90 to 2.64), and no slope difference is estimated.
  - "No better than the coach's most-used players" and "none of the optimisation variants exceeded the benchmark" are based on overlapping CIs. They are also factually wrong for the point estimate: VAL40 unconstrained is 4.23 (CI 0.32 to 8.78), above the coach benchmark of 3.84 (CI 1.54 to 6.14).
  - The CIs are 7–10 points per 100 possessions wide, so the study cannot rule out practically large advantages. The Limitations admit this (`discussion.qmd:13`) while the title and abstract state the opposite.
  - No smallest worthwhile change (SWC) for net rating is defined.
- **Fix:**
  1. Estimate paired team-season bootstrap differences: slope(RAPM) − slope(PIR40/VAL40/minutes), and contrast(ILP variant) − contrast(coach) on the same team-seasons.
  2. Pre-specify an SWC for lineup net rating, anchored to wins, and interpret the CIs against it (equivalence / ROPE).
  3. Rewrite the title, abstract and conclusions as "not shown to outperform; advantages larger than X cannot be excluded".
  4. Present the 17 interval estimates explicitly as estimation, not hypothesis tests, or apply a multiplicity framing.

### C8. The ILP evaluation design is incompletely reported and endogenous
- **Location:** `methods.qmd:25`, `results.qmd:33`, Fig. 3 caption.
- **Problems:**
  - Data in results.json are not reported. ILP lineups account for only 5–9% of possessions, against 18% for the coach five (`hucum_payi`). They are evaluated in 105–143 team-seasons, against 155 for the coach (`takim_sezon`). The overlap between each ILP five and the coach five is not computed. Outline step 8–9 promised the possession share would be reported.
  - The "optimised five" is observed only when the coach chooses to field ≥ 4 of its players (selection on coach deployment and game state). The comparison group ("other segments") also differs between variants (`ilp_validation.py:159–160`).
  - Coach benchmarks "with ≥ 1 rim protector" and "balanced", shown in Fig. 3, are not defined in the Methods.
  - Optimising on noisy first-half values produces post-decision disappointment (the optimizer's curse). `[@smith2006optimizer]` is already in the .bib but not cited.
- **Fix:**
  - Report possession share, team-season n and the mean number of players shared with the coach five for every variant.
  - Compare ILP and coach on the same team-seasons (paired).
  - Define the constrained coach benchmarks.
  - Discuss the optimizer's curse.
  - Optionally add an evaluation of selected fives using held-out RAPM-predicted value, which does not depend on coach deployment.

### C9. The conclusions contradict the ILP results; the "add little beyond the coach" claim is untested
- **Location:** `discussion.qmd:7` ("Box-score indices thus add little to what coaches already reveal through playing time"), `discussion.qmd:17`, abstract conclusions (`index.qmd:33`).
- **Problem:** Each slope comes from a separate model, so no model tests incremental value over first-half minutes. In Fig. 3 the RAPM-optimised five has the *lowest* point estimate (2.18) and VAL40 the highest (4.23). The recommendation to use RAPM-type values for lineup decisions is therefore not supported by the decision-level results.
- **Fix:**
  - Fit joint models (minutes + PIR40; minutes + RAPM) and report the partial slopes with paired CIs.
  - Limit the RAPM recommendation to player comparison, or add evidence that it helps lineup decisions.
  - Discuss explicitly why the measure with better predictive validity did not give better optimised lineups.

### C10. Reproducibility: the stored results do not match the current code
- **Location:** `results.json["lineup_model_roles_final_K5"]` vs `lineup_model.py:276`.
- **Problem:** The current script always writes an `ayristirma` field. The stored key has none, which suggests the reported test R² values were produced by a different code version from the one in the repository. Separately, the "earlier work" VAL40 definition and the role solution depend on Paper A outputs, but no version is recorded.
- **Fix:** Re-run `make analysis` from a tagged commit, record the commit hash and package versions in results.json, and archive the code with a DOI (Zenodo) *before* acceptance, not after.

---

## 4. Minor issues

1. **Hard-coded numbers** (CLAUDE.md rule 2): "400 minutes" (`results.qmd:9`, `results.qmd:19`; `V["asgari_dakika"]` exists), "300 possessions", "λ = 1,000" (`methods.qmd:9,13`), "500 bootstrap resamples" (`methods.qmd:17`) and "100 first-half minutes" (`methods.qmd:25`). Write each of these to results.json and read it inline.
2. **Spurious precision:** "32.70%" and "1.20%" (abstract) and two-decimal R² percentages. Use η² = 0.33 / 0.01 in the abstract.
3. **Missing point estimates for R² differences** (`results.qmd:23`): only the CIs are given. Add the point differences. Also report RMSE, and lineup-season or game-level R², so that the 0.36% figure can be interpreted.
4. **Season notation:** "training 2016–2022, test 2023–2024" (`index.qmd:31`, `methods.qmd:17`) versus "2016–17 to 2024–25" (`methods.qmd:5`). Use one convention.
5. **Segment flow (STROBE item 13):** 64,549 (`lineup_model…segment_N`), 64,324 (`ilp_validation.segment_N`) and 64,125 (`paper_a.stints_model`) are not reconciled. Add a flow diagram and the STROBE checklist as a supplement.
6. **Mirrored rows:** `ilp_validation.py:105–115` enters every second-half segment once per team (sign-flipped), so `segment_N` counts team-segments and each segment falls in two clusters. State this, and consider two-way clustering (game × team-season).
7. **Figures:** the x-axis labels are cut off in Fig. 2 and Fig. 3. Fig. 1 has no uncertainty; add bootstrap CIs per role mean. Fig. 3 includes undefined coach-constraint variants (see C8).
8. **The abstract has no quantitative results for aims 2 and 3.** Add the R² difference and the slope and contrast estimates with 95% CIs.
9. **"Favour interior roles":** ball handlers also sit above the mean in PIR40 (z = +0.50, `rol_ortalamasi_z["5"]`). Qualify the sentence (`index.qmd:33`, `discussion.qmd:17`).
10. **Methods detail is missing:** software and versions, seeds, GMM specification (covariance type, K = 5 selection and its stability), the median-Gamecode split and playoff handling, and how traded players are assigned to teams in the ILP pool.
11. **VAL40 definition** (`methods.qmd:9`): `ilp_validation.py:42–47` omits fouls drawn, fouls committed and shots blocked against. "Blocked shots" is ambiguous; state exactly which terms are dropped.
12. **Uncited mechanism:** "creating space, drawing defenders, making the extra pass" (`discussion.qmd:5`) is speculation. Cite it or mark it as a hypothesis.
13. **Literature positioning:** the Introduction (3 paragraphs, 7 sources) does not engage with studies of positional differences in game statistics or with EuroLeague role work already in the .bib (`sampaio2006discriminant`, `konca2026from`). Add them through the `sspe-ask` pipeline.
14. **Bibliography quality:** `grassetti2020extended` lacks DOI, volume and pages. `kalman2020lineup` has no venue (grey literature). `petridis2026lineup` is a preprint. Complete the entries via `sspe-doi`.
15. **Declarations missing:** affiliation, ORCID, funding, competing interests, author contributions. The AI-use statement is present and adequate, and the data/code statement is present (but see C10).
16. **OPEN_QUESTIONS #22** suggested a within-role standardised PIR/VAL objective. That is the obvious remedy to test: does role-normalised PIR recover predictive validity or improve ILP lineups? Add it, or justify leaving it out.
17. **No MBI is used** (good). The λ = 1,000 sensitivity value is arbitrary; show η² across the full CV grid (500–8000).

---

## 5. Drake & Han (15 steps) check

| Item | Status |
|---|---|
| Thesis (step 1) | Clear, but stronger than the evidence (C3, C7). |
| Topic and transition sentences | Good throughout. Each Introduction, Results and Discussion paragraph opens with a topic sentence, and the transitions ("Two consequences follow…", "The predictive comparison points in the same direction.") work. |
| Figure and table captions start with a full sentence | Yes for Fig. 1–3 and Tbl. 1. The Fig. 2 caption ("unlike box-score indices") overstates in the same way as C7, and Fig. 3's ("perform no better") is an equivalence statement that is not tested. |
| Limitations paired with responses (steps 8–9) | **Only partly.** Of five limitations (`discussion.qmd:13`), only "RAPM as reference" (out-of-time confirmation) and "EuroLeague only" (open data) have a response. Noise, coverage and the lack of fatigue/matchup modelling have none. Outline problems missing from the text: ILP fives rarely play together, possible leakage in the coach baseline, net rating vs wins, opponent strength. Circular roles (C3) are not acknowledged. |
| Concluding paragraph ends on a concrete application | Yes: "evaluate any lineup decision tool against the coach's most-used players rather than against the team average." This is concrete and supported. The preceding RAPM recommendation is not (C9). |
| Outline fidelity | Step 7 B3 and step 8–9 ("possession share reported") are not implemented. The Fig. 2 caption was correctly toned down from the outline. The outline planned 6 Discussion paragraphs; the manuscript has 4 plus Limitations and Conclusions, which is acceptable. |

---

## 6. Citation audit

`grep` of every `[@key]` in `manuscript_b/index.qmd` and `sections/*.qmd` against `manuscript/references.bib`:

| Key | Uses | In .bib | Content check (literature/answers) |
|---|---|---|---|
| kubatko2007starting | 2 | Yes | OK for the possession formula; doubtful for "linear indices in NBA" (C2) |
| muniz2022sports | 2 | Yes | **Title-level only allowed; content claims made** (C2) |
| grassetti2020extended | 3 | Yes (no DOI) | Abstract-verified: EuroLeague RAPM for lineups; OK |
| petridis2026lineup | 3 | Yes (arXiv) | **Not verified**; lineup RAPM ≠ player RAPM (C2) |
| ribes2026identifying | 1 | Yes | Abstract-verified; OK |
| kalman2020lineup | 1 | Yes (no venue) | Full-text verified; OK for "data-driven roles" |
| martonosi2023predicting | 2 | Yes | **Misattributed in both places** (C2) |
| hennig2007cluster | 1 | Yes | OK (bootstrap stability) |

Every key resolves, so there are no missing keys. Three keys have content problems, and two pieces of prior work (the thesis and Paper A) are uncited.

## 7. Number consistency with results.json

| Claim (location) | results.json | Status |
|---|---|---|
| 9 seasons, 2,646 games (`methods.qmd:5`, abstract) | `paper_a.seasons/games` | OK |
| 64,549 segments (`methods.qmd:5`) | `lineup_model_roles_final_K5.segment_N` | OK (but see minor 5) |
| η² PIR40 0.33 (0.27–0.40), VAL40 0.42 (0.36–0.49), RAPM 0.01 (0.00–0.04/0.05), RAPM λ1000 0.01 | `paper_b_values.eta2`, `eta2_GA95` | OK |
| "more than doubled" SD 3.03 vs 1.64 (`results.qmd:5`) | ratio 1.85 | **Mismatch (C1)** |
| Role ordering of PIR40 and RAPM (`results.qmd:5`) | `rol_ortalamasi_ham/z` | OK |
| r(PIR40, RAPM) = 0.24 | `korelasyon.RAPM.PIR40` = 0.239 | OK |
| Test R² 0.36% / 0.11% / 0.05%; CI of differences | `test_R2` | OK (the PIR value 0.00115 renders as 0.11) |
| Slopes RAPM 1.76, minutes 1.07, PIR40 0.51, VAL40 0.54 with CIs | `amac_fonksiyonu_egimi` | OK; **VAL40_havuz 0.95 omitted (C5)** |
| Coverage 68% vs 100% | `kapsam` | OK |
| Coach 3.84 (1.54–6.14); ILP PIR40 3.37, VAL40 4.23, RAPM 2.18 | `ilp_beslisi` | Numbers OK; **"none … exceeded the benchmark" false for the VAL40 point estimate (C7)** |
| "most of their confidence intervals included zero" | 8 of 9 ILP CIs include 0 | OK |
| n = 519 players, 156 team-seasons, B = 1,000 | `oyuncu_N`, `takim_sezon_N`, `B` | OK |
