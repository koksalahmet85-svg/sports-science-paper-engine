# Review – Round 3

**Manuscript:** "Box-score performance indices depend on player role and show no advantage over coaches' rotations for lineup selection: an out-of-sample evaluation in EuroLeague basketball"
**Reviewer role:** Senior reviewer (Q1 sports science / sports analytics)
**Date:** 2026-11-18
**Material reviewed:**
- Manuscript: `manuscript_b/index.qmd` and `manuscript_b/sections/{introduction,methods,results,discussion}.qmd`.
- Rendered output: `manuscript_b/_output/index.docx`, rendered 17:22:17, after the last source edit (`discussion.qmd`, 17:22:04). I checked the inline values in the docx.
- Figures: `manuscript_b/figures/fig1–3`.
- References: `manuscript/references.bib`.
- Results file: `manuscript/analysis/results.json`, keys `paper_b_values`, `ilp_validation` (including `dogrudan_eslestirilmis_fark`), `lineup_model_roles_final_K4`, `roles_final` and `provenance`.
- Code: `manuscript/analysis/{ilp_validation,paper_b_values,lineup_model,provenance}.py`.
- Supporting files: `manuscript_b/STROBE.md`, `manuscript/OPEN_QUESTIONS.md`, and reviews `round-1.md` and `round-2.md`.
- An independent check of role-label coverage among ILP candidates using `data/processed/roles_final_K4.csv` and `player_game.csv.gz` (read only).

---

## 1. Decision

**Major revision. This is a borderline case close to minor revision.** All three round-2 blocking problems have been dealt with:
- **N1 is resolved.** The abstract, Discussion and Fig. 2 now agree with results.json.
- **N2 is resolved in substance.** The comparison is now a true within-team-season contrast, the overlapping segments are reported and excluded, and the unsupported "not biased" sentence is gone.
- **K3 is acceptable as a pending administrative item.** It is not yet closed (see §3).

Several major items are still only partly addressed, and the round-3 changes introduced new problems:
- The out-of-time asymmetry that favours RAPM is still untreated (M2).
- There is no smallest worthwhile change (SWC) or reference margin (M4).
- The "same on-court impact" criterion assumption is not stated (M1b).
- New: the 2SLS check, which the paper now relies on, violates its exclusion restriction (P1).
- New: the switch from five to four roles changed every role-based result, and no sensitivity analysis is reported (P2).

## 2. Scores (1–5)

| Criterion | R1 | R2 | R3 | Comment |
|---|---|---|---|---|
| Originality | 3 | 3 | 3 | Unchanged. The Introduction still cites 8 sources. It does not engage with the positional box-score literature or EuroLeague role work, and it does not say what is new relative to the thesis. |
| RQ–design fit | 3 | 4 | 4 | Aim 3 is now matched by a direct within-team comparison. |
| Internal validity | 2 | 3 | 3 | Much improved: direct comparison, previous-season constraint roles, 2SLS. Still open: the out-of-time minutes asymmetry (M2), the 2SLS exclusion problem (P1), game-state selection of coach and optimised fives (N2 residual), and an unstated criterion assumption (M1b). |
| Statistics | 2 | 3 | 3 | Multiplicity is now acknowledged. Still missing: an SWC or reference margin, point estimates for the R² differences, and any treatment of the mirrored-row cross-cluster dependence. 2SLS is mis-specified (P1). No K sensitivity analysis (P2). |
| Reporting-guideline compliance | 2 | 3 | 3 | Provenance is recorded and segment counts are partly reconciled. Still missing: an English STROBE checklist in the supplement, a flow diagram, a software/statistics paragraph in the manuscript, declarations and the thesis reference. Hard-coded numbers remain. |
| Discussion tied to evidence | 2 | 3 | 4 | The over-claims flagged in N1, M3 and M5 are gone. The remaining issues are wording: "same on-court impact", "moderate differences" and "show no advantage" in the title. |
| Practical implication | 3 | 3 | 3 | "Benchmark against the coach" is well supported. Without an SWC, and with lower CI limits down to −9.5 points per 100 possessions, practitioners cannot tell how large a loss optimisation might cause. The role-normalised remedy is still untested. |

Accept is not possible until every score is ≥ 4 and all critical issues are closed.

---

## 3. Point-by-point status of round-2 critical issues

| # | Round-2 issue | Status | Evidence / remaining action |
|---|---|---|---|
| N1 | Abstract and Discussion said "only RAPM" excluded zero | **Resolved** | `index.qmd:40`, `discussion.qmd:7` and the Fig. 2 caption (`results.qmd:31`) now say "RAPM-based lineup value and first-half minutes, but no box-score measure". This matches `amac_fonksiyonu_egimi.DAKIKA` (1.07, CI 0.02 to 1.98). The "clearly" wording is removed. The common-subset caveat is in the Results and Discussion. |
| N2 | The "paired" ILP − coach difference was not paired | **Resolved in substance; residual moved to major** | `methods.qmd:25` and `ilp_validation.py:217–242` now implement what was requested: ILP-only segments against coach-only segments within each team-season in which both are observed, with harmonic possession weights and a team-season bootstrap. The number of team-seasons (104–140) and the share of excluded segments that qualify for both groups (44–49%) are reported (`results.qmd:35`, Table 2). "Not biased in either direction" is deleted. **Residual:** the Limitations say only that the exclusion "limits its precision" (`discussion.qmd:13`). They do not describe how coach-only and ILP-only segments differ in game state (start of quarter, closing time, garbage time) or the likely direction of the resulting bias. Round-2 fix item 3 (adjust for quarter and score margin) was not attempted. See **M9**. |
| K3 | Prior work not formally cited | **Partly resolved. Disclosure acceptable; formal reference pending and still blocks submission** | See the assessment below. |

### Assessment of the "Prior dissemination" statement (K3)

The statement (`index.qmd:52–54`) is, in substance, an adequate disclosure to the editor. It names the thesis and its institution, says that results are re-examined and partly corrected, and discloses the companion manuscript. I accept it **for this round** as a placeholder, given that the thesis has no DOI and CLAUDE.md forbids writing BibTeX from memory. It cannot go to a journal in this form, for four reasons:

1. **A missing DOI does not prevent citation.** The national thesis repository (YÖK Ulusal Tez Merkezi) assigns a thesis number, and `OPEN_QUESTIONS.md:3` shows that the project holds the full text (title, Ege University, 2026). A `@phdthesis` entry transcribed from that primary record is not "from memory". Either the author supplies the repository record, or the project adds a documented route for sources without a DOI: a verification note in `literature/` and a manual entry checked against the title page. Log this in `OPEN_QUESTIONS.md` now. Then cite the key at `introduction.qmd:3`, `methods.qmd:9`, `methods.qmd:17` ("thesis inclusion criteria") and `methods.qmd:25` ("earlier work").
2. **"Re-examined, and in part corrected" is vague.** Name the corrections in one sentence. For example: the role clustering is replaced by a stability-selected solution, and the ILP lineups, which the thesis did not validate on court, are tested out of sample. Editors check overlap with plagiarism software against repository theses, so the statement must make clear which results are new.
3. **"Manuscript under review" (`methods.qmd:13`) must be literally true.** If the companion paper has not yet been submitted, write "submitted" or "in preparation", and supply it to the editor as a related manuscript.
4. **The Introduction still lacks a sentence on what is new** relative to the thesis and the companion paper (requested in round 2).

---

## 4. Point-by-point status of round-2 major issues

| # | Issue | Status | Remaining action |
|---|---|---|---|
| M1 | Construct problems in role dependence | **(a) Largely resolved. (b) Open. (c) Resolved. (d) Resolved.** | (a) A strict non-PIR partition was added: η² 0.28 for PIR40 and 0.006 for RAPM. The ARI against the main partition and bootstrap CIs for the alternative-partition η² are still missing (minor). The `methods.qmd:13` description of the first alternative set leaves out fast-break and second-chance rates, which the strict version then "also" excludes; list the variables accurately. (c) All three contrasts against the reference role are now reported with CIs. (d) The terminology is now consistent ("bias" is reserved for analyses conditional on RAPM). **(b)** "Players with the same on-court impact" still appears in the abstract (Purpose and Conclusions, `index.qmd:38,41`), `introduction.qmd:7`, `methods.qmd:13`, `discussion.qmd:3` and `discussion.qmd:17`. 2SLS addresses noise in RAPM but not bias in RAPM. The role-bias claim assumes that RAPM is an unbiased criterion of impact *across roles*. That assumption is not stated. For example, ridge shrinkage and collinearity between frequently paired bigs could make RAPM itself depend on role. The Limitations argue that the out-of-time analysis "does not presuppose that RAPM is correct" (`discussion.qmd:13`), but the role-bias analysis does presuppose it. **Fix:** write "same estimated RAPM" in the abstract and Conclusions. Add one Limitations sentence stating the criterion assumption and its consequence. |
| M2 | Out-of-time asymmetry; thresholds | **Partly resolved** | Thresholds are now disclosed: PIR40 ≥ 90 minutes, the replacement coefficient, and 76% of test appearances by players seen in training (`methods.qmd:17`). The Limitations say the asymmetry "may favour RAPM". **Open:** (i) No common-sample R² and no low-minutes indicator for the box-score models, so the only analysis that establishes RAPM's advantage is still biased in RAPM's favour. (ii) The point estimates of the R² differences are not reported, only the CIs. They are 0.25 pp (RAPM − PIR40) and 0.32 pp (RAPM − VAL40), from `test_R2`. (iii) "VAL40 from player-seasons meeting the thesis inclusion criteria" is undefined. The code (`lineup_model.py:131–133`) takes a minutes-weighted mean over `player_season` with no minimum of its own; state the actual criterion. (iv) The abstract and `introduction.qmd:7` ("RAPM predicts future lineup outcomes better") state the advantage without the asymmetry caveat. **Fix:** re-estimate test R² on test segments in which all ten players were seen in training with ≥ 300 possessions *and* ≥ 90 minutes, or add a low-minutes indicator to all three models. Report the point differences. Qualify the Introduction claim. |
| M3 | Limitations overstated robustness | **Resolved** | `results.qmd:29` and `discussion.qmd:7,13` now state the common-subset changes plainly and say the within-season comparison "does not establish that any measure is better". Minor: "increased somewhat" understates the pooled VAL40 change (0.54 → 0.95). The RAPM − VAL40_havuz paired CI (−0.84 to 1.55) is still not reported. |
| M4 | SWC / equivalence / multiplicity | **Partly resolved** | Multiplicity is now acknowledged (`discussion.qmd:13`), and the Fig. 2 caption has been made descriptive. **Open:** (i) There is still no SWC. "No smallest worthwhile difference was specified in advance" is a disclosure, not a remedy. A post hoc reference margin, clearly labelled as such, is still needed to interpret intervals ranging from −9.51 to +7.68. Examples: the net-rating difference that corresponds to one extra win per season, or 0.2 × the between-team-season SD of net rating. (ii) Equivalence wording remains in the title ("show no advantage"), `introduction.qmd:7` ("show no advantage"), the Table 2 caption ("direct comparisons show no difference from it", `results.qmd:39`) and `results.qmd:35` ("no optimisation variant differed from the coach benchmark"). (iii) The abstract's "moderate differences could not be excluded" understates the lower limits, which reach −8.5 to −9.5 points per 100 possessions in five variants. That is a large disadvantage, not a moderate one. **Fix:** "showed no evidence of an advantage". In the abstract, give the CI limits ("disadvantages of up to about 9 points and advantages of up to about 8 points per 100 possessions could not be excluded"). Classify each interval against the stated margin. |
| M5 | Untested "add little"; RAPM-ILP result | **Resolved** | The claim is withdrawn explicitly (`discussion.qmd:7`). The optimiser's-curse discussion is generalised (`discussion.qmd:9`). Minor: "favoured the coach five in most optimisation variants" counts 7 of 9 point estimates that are strongly dependent (shared coach group, overlapping fives). Say that this count is not independent evidence. |
| M6 | Look-ahead leakage in constraint roles | **Largely resolved** | Previous-season roles are now used (`ilp_validation.py:83–88,110`), and the 34% of candidates with current-season roles is disclosed (`discussion.qmd:13`). My own check: only 9 of 1,725 candidate player-team-seasons have no role label at all, so role 0 is negligible. Two minor points remain. First, the 34% includes the whole of 2016–17, which by design has no previous season; report a sensitivity analysis that excludes 2016–17. Second, the GMM is fitted on pooled seasons, so even previous-season labels come from a model that saw later seasons; disclose this in one clause. The `n_cur` expression in `ilp_validation.py:112` contains a dead sub-expression, `all(... for x in ())`, which is always True. It does not change the result but should be removed. |
| M7 | STROBE compliance | **Partly resolved** | The segment counts are now partly reconciled (`methods.qmd:21`: team-segment observations against segments). The number of second-half segments (64,324 / 2) is not given. `manuscript_b/STROBE.md` exists, but it is an internal Turkish checklist shared with Paper A, and item 22 (funding) is unfilled. **Open:** an English STROBE checklist with page or line numbers in the supplement; a participant/segment flow diagram; a "Statistical analysis and software" paragraph *in the manuscript* (Python and package versions; GMM with tied covariance, n_init = 5, reg_covar = 1e-4; scipy `milp`; seed); handling of playoffs and traded players; and the discrepancy of 156 vs 155 team-seasons. The mirrored rows place each segment in two team-season clusters with exactly opposite outcomes. The one-way team-season bootstrap ignores this cross-cluster dependence, and the paper neither discusses it nor checks it with two-way (game × team-season) clustering. |
| M8 | Provenance | **Largely resolved** | `results.json["provenance"]` records the commit (41403dc), Python, the seed and package versions. Remaining: (i) `results.json` is git-ignored (`.gitignore:11`), so the "results file (`provenance`)" cited at `index.qmd:58` is not in the public repository. Commit it or archive it with the code. (ii) `provenance.py` does not record a dirty-tree flag. The current working tree differs from 41403dc (`discussion.qmd` and all three Paper B figures are modified and uncommitted). Commit, re-run, and record `git status --porcelain` or `dirty: true/false`. (iii) Archiving "before submission" is acceptable. |

---

## 5. New issues

### Critical
None. No numerical mismatches were found (§8).

### Major

**P1. The 2SLS measurement-error check violates the exclusion restriction** (`paper_b_values.py:119–128`; `methods.qmd:13` item 4; `results.qmd:7`; `discussion.qmd:5`)
- The outcome is career PIR40 computed from **all** games (`d["PIR40"]`). The instrument is RAPM from **odd** games.
- PIR40 therefore contains the odd-game box-score noise. That noise is correlated with odd-game plus-minus noise, because good box-score games coincide with positive on-court margins.
- The instrument is therefore correlated with the structural error. The bias is probably small (r(PIR40, RAPM) = 0.24), but the check is presented as one of the "four checks" that support the main claim.
- **Fix:** use PIR40 from even games as the outcome (`PIR40_c` is already in `j2`), with RAPM_even as the endogenous regressor and RAPM_odd as the instrument. Repeat with the halves swapped and report both, or their average. Also state that IV corrects classical error, not ridge-shrinkage bias.

**P2. The change from five to four roles alters every role-based result, and no sensitivity analysis is reported** (`index.qmd:14–16`; `methods.qmd:13`; `results.qmd:5–7`; Tables 1–2)
- Between rounds 2 and 3, `roles_final.K` changed from 5 to 4. This followed the companion paper's revision, commit 9d72224. As a result:
  - η² for PIR40 fell from 0.33 to 0.26.
  - Partial η² fell from 0.33 to 0.27.
  - The reference role changed from stretch forward to ball handler, so the headline contrasts fell from +6.5/+6.8 to +4.6/+4.3.
  - The rim-protector and balanced constraints were redefined.
- The selection is not clear-cut. In `roles_final.tarama`, mean Jaccard is 0.781 for K = 4 and 0.765 for K = 5, but new-player ARI is 0.578 for K = 4 and 0.758 for K = 5.
- The conclusions do not depend on K, but readers need to see that.
- **Fix:**
  - State that K was fixed by the companion analysis before the Paper B outcome analyses were run, if true.
  - Report the K = 5 results as a supplementary sensitivity table (η², partial η², 2SLS, ILP − coach direct differences); `lineup_model_roles_final_K5` already exists.
  - Report role contrasts against the grand mean (effect coding) or all pairwise contrasts, so that the headline magnitude does not depend on which arbitrary role is labelled "1". Interior roles are about 6.5–6.8 PIR/40 above wing/forwards but only 4.3–4.6 above ball handlers.

**M9. Selection by game state in the direct comparison (residual from N2)** (`discussion.qmd:13`)
- Coach-only segments (most-used players) are concentrated at starts of quarters and in close finishes. ILP-only segments are lineups the coach did *not* choose to field together; these are typically rest-time or garbage-time units, or units fielded because of fouls or injuries.
- The bias could run in either direction, but it is systematic and is the main threat to the paper's third conclusion.
- **Fix:** adjust y_adj for quarter and score margin at segment start (one regression within the existing bootstrap). Alternatively, add a deployment-independent check: the held-out RAPM-predicted value of each five, which needs no on-court co-occurrence. In addition, write two sentences in the Limitations describing the mechanism and its possible direction.

### Minor (new or carried over)
1. **Hard-coded numbers (CLAUDE.md rule 2, carried over from round-2 minor 3).** "Nine EuroLeague seasons" (`index.qmd:39`, `discussion.qmd:3`; `A["seasons"]` exists), "60 minutes", "300 possessions", "90 training-period minutes", "100 first-half minutes", "λ = 1,000", "five-fold", "500 bootstrap resamples", "2016–2022 / 2023–2024". I checked these against the code (`MIN_POSS = 300`, `ROSTER_MIN = 100`, `MIN ≥ 90`, `GroupKFold(5)`, 500 test bootstraps) and they agree, but they must be written to results.json and read inline. The main λ (`lambda_ana` = 4000) and the CV grid are still not reported.
2. **Typography.** Inline negatives are rendered with a hyphen-minus (abstract "-3.6"; "−3.00 to −1.34" appears as "-3.00 to -1.34" throughout). Fix `ci()` and the abstract f-string to emit U+2212. The abstract's "differed … by −3.6 to +1.5" reads as if there were real differences; write "point estimates ranged from …".
3. **Fig. 1** still has no uncertainty, and the caption's justification ("η² and its CI are given in Table 1") does not address the role means. Add bootstrap CIs, or plot the RAPM-conditional contrasts with CIs.
4. **Literature positioning, mechanism claims and bibliography (carried over from round-2 minors 5–7).** The Introduction does not cite positional box-score literature (e.g. `sampaio2006discriminant`, `konca2026from`, already in the .bib). Two Discussion statements are unsupported: "spacing the floor and moving the ball are only partly recorded" (`discussion.qmd:5`) and "so their rotations already favour the best players" (`discussion.qmd:9`). Mark them as hypotheses or support them via `sspe-ask`. `grassetti2020extended` lacks DOI, volume and pages, and `kalman2020lineup` lacks a venue; complete both via `sspe-doi`. `smith2006optimizer` still has no verification note in `literature/answers/`.
5. **η² refinements (carried over).** Report ω² or ε², and give bootstrap CIs for the reliability-corrected η².
6. **Role-normalised PIR (OPEN_QUESTIONS #22, carried over).** It is still recommended (`discussion.qmd:5`) but not tested.
7. **Out-of-time target alignment (carried over from round-2 minor 10).** RAPM is fitted to segment net rating, the same quantity it is tested on, and PIR is not. Acknowledge this next to the "does not presuppose that RAPM is correct" sentence.
8. **Generalisation (carried over).** "For example in scouting or contract decisions" (`discussion.qmd:5`): add "in EuroLeague-level competition".
9. **Declarations (carried over).** Affiliation, ORCID, funding, competing interests and author contributions are still missing from `index.qmd`. The AI-use and ethics statements are adequate.
10. **Constraint mapping.** "≥ 1 rim protector (the constraint used in earlier work)" (`methods.qmd:25`): the thesis constraint was defined on the thesis archetypes, not on the present four-role solution. Write "analogous to".

---

## 6. Citation audit

I grepped every `[@key]` in `manuscript_b/index.qmd` and `sections/*.qmd` against `manuscript/references.bib`:

| Key | Uses | In .bib | Content check |
|---|---|---|---|
| grassetti2020extended | 3 | Yes (no DOI/volume/pages) | OK for EuroLeague RAPM. Weak as the sole method source (minor 4). |
| hennig2007cluster | 1 | Yes | OK (bootstrap cluster stability). |
| kalman2020lineup | 1 | Yes (no venue) | OK. |
| kubatko2007starting | 1 | Yes | OK (possession formula). |
| martonosi2023predicting | 1 | Yes | OK; matches the verification note. |
| muniz2022sports | 2 | Yes | Title-level use. OK. |
| ribes2026identifying | 1 | Yes | OK. |
| smith2006optimizer | 2 | Yes | Use matches the title. No verification note (minor 4). |

All 8 keys resolve; no keys are missing. **Uncited prior work:** the thesis (mentioned in prose 4 times, no entry; K3 pending) and the companion manuscript (disclosed in prose; acceptable for a manuscript that is not yet published, provided the "under review" status is accurate).

## 7. Number consistency with results.json (checked in the rendered docx)

| Claim (location) | results.json | Status |
|---|---|---|
| 2,646 games; 64,549 segments; 48,309 / 16,240 | `paper_a.games`, `lineup_model_roles_final_K4` | OK |
| Abstract: role explained 26% (PIR) vs 0.5% (RAPM); 27% at the same RAPM; +4.6 / +4.3 vs ball handlers | `eta2` 0.263 / 0.005; `RAPM_kosullu.PIR40.kismi_eta2` 0.271; `rol_farki_RAPM_sabit` 2 = 4.61, 4 = 4.33; reference role 1 = Ball handler | OK |
| η² 0.26 (0.20–0.33), 0.38 (0.31–0.45), 0.005 (0.001–0.031) | `eta2`, `eta2_GA95` | OK |
| Partial η² 0.27 (0.21–0.34); rim protector 4.6 (3.52–5.75), interior big 4.3 (3.11–5.57), wing/forward −2.2 (−3.00 to −1.34) | `RAPM_kosullu.PIR40` | OK |
| 2SLS 4.4 (3.07–5.65), 4.3 (2.91–5.64); n = 481 | `olcum_hatasi_denetimi` | Numbers OK. Specification flawed (P1). |
| Non-PIR η² 0.30; strict 0.28; RAPM 0.006 | `pir_bilesensiz_roller(_kati).eta2` | OK |
| Reliability 0.91 / 0.59 (n = 485); corrected η² 0.009 / 0.29 | `guvenirlik`, `eta2_duzeltilmis` | OK |
| SD 1.64 → 3.03; η² λ1000 0.003; r = 0.24 | `rapm_sd`, `eta2.RAPM_l1000`, `korelasyon` | OK |
| Table 1: role n 177/62/226/54 (sum 519); means | `rol_N`, `rol_ortalamasi_ham` | OK |
| Test R² 0.36 / 0.11 / 0.05%; CIs 0.10–0.39 and 0.17–0.45 pp; 76% seen | `test_R2`, `testte_egitimde_gorulen_oyuncu_payi` 0.757 | OK. Point differences (0.25 / 0.32 pp) not reported (M2). |
| Slopes: RAPM 1.76 (0.90–2.64), minutes 1.07 (0.02–1.98), PIR40 0.51 / 0.78, VAL40 0.95; coverage 83%; common subset 77%, RAPM 1.10, minutes 0.62 (−0.50–1.62); paired CIs −0.65–1.75, −0.57–1.60 | `amac_fonksiyonu_egimi`, `kapsam`, `ortak_alt_kume` | OK (abstract now consistent; N1 closed) |
| Coach five 3.84 (1.35–6.13) | `ilp_beslisi.DAKIKA_yok` | OK |
| Direct ILP − coach: −3.61 to 1.49 (abstract −3.6 to +1.5); all CIs include 0; width up to 13.1 (Limitations "13"); 44–49% excluded | `dogrudan_eslestirilmis_fark` (min −3.61 RAPM_dengeli, max 1.49 RAPM_tez; widest VAL40_sezon_tez −9.51 to 3.58; shares 0.435–0.494) | OK |
| Overlap "about three of five"; possession share 5.4–8.7% vs 17.9% | `antrenor_beslisiyle_ortak_oyuncu` 2.75–3.13; `hucum_payi` | OK |
| 34% current-season constraint roles | `kisit_rolu_cari_sezondan_pay` 0.34 | OK (see M6 on the 2016–17 component) |
| "Moderate differences could not be excluded" (abstract) | Lower CI limits −8.5 to −9.5 in five variants | Understated (M4) |

No sentence contradicts results.json. Figures 1–3 match the stored values (K = 4 labels; Fig. 3 plots `dogrudan_eslestirilmis_fark`).

## 8. Checklist

| Item | Status |
|---|---|
| Sample justification | Thresholds are stated but not justified, and there is no precision rationale for the direct comparison (team-seasons fall from 156 to 104–140). |
| Clustered data | Team-season bootstrap throughout. The cross-cluster dependence from mirrored rows is not addressed (M7). |
| Multiple comparisons | Acknowledged (`discussion.qmd:13`). Adequate for an estimation-focused paper. |
| Effect size + CI | Yes, throughout. R² point differences and CIs for the corrected η² are missing. |
| SWC/TE | **Absent** (M4). |
| Causal language | Appropriate overall. "So their rotations already favour the best players" (`discussion.qmd:9`) is asserted rather than shown. |
| Limitations | Comprehensive and now candid. Missing: the criterion assumption (M1b), game-state selection (M9) and target alignment (minor 7). |
| Over-generalisation | Minor (minor 8). |
| MBI | Not used (good). |
| p-hacking signals | The K change between rounds (P2) is a forking-path risk unless the K = 5 results are shown. All variants are reported. |
| Data/code availability | Public API and GitHub. The results file is git-ignored; archive before submission (M8). |
| AI statement | Present and adequate. |

## 9. Summary of what must be done for the next round

1. **P1:** re-specify the 2SLS with PIR40 from even games, swap the halves, and report both.
2. **P2:** supplementary K = 5 sensitivity analysis, a statement that K was fixed beforehand, and contrasts that do not depend on the reference role.
3. **M2:** common-sample out-of-time R², or a low-minutes indicator; report the point differences; define the VAL40 criterion; qualify the Introduction claim.
4. **M4:** a post hoc reference margin with justification; remove equivalence wording (title, Introduction, Table 2 caption, `results.qmd:35`); state the CI limits in the abstract.
5. **M1b:** state the criterion assumption; use "same estimated RAPM".
6. **M9:** game-state adjustment, or a deployment-independent check, plus a Limitations sentence.
7. **M7:** English STROBE checklist and flow diagram in the supplement; software/statistics paragraph; clustering note.
8. **K3:** obtain the thesis record from the national repository and add a verified entry through a documented route; cite it at the four locations; specify the corrections.
9. Minor items 1–10.
