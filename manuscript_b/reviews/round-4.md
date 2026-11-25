# Review – Round 4 (final round)

**Manuscript:** "Box-score performance indices depend on player role and show no detectable advantage over coaches' rotations for lineup selection: an out-of-sample evaluation in EuroLeague basketball"
**Reviewer role:** Senior reviewer (Q1 sports science / sports analytics)
**Date:** 2026-11-25
**Material reviewed:**
- Manuscript: `manuscript_b/index.qmd` and `sections/{introduction,methods,results,discussion}.qmd`.
- Rendered output: `manuscript_b/_output/index.docx` (08:45:32, after the last source and figure edits). I checked the inline values in the docx text.
- Figures: `manuscript_b/figures/fig1–4`.
- References: `manuscript/references.bib`.
- Results file: `manuscript/analysis/results.json`, keys `paper_b_values`, `ilp_validation`, `lineup_model_roles_final_K4`, `roles_final` and `provenance`.
- Code: `manuscript/analysis/{ilp_validation,paper_b_values,lineup_model,provenance}.py`.
- Verification notes: `literature/answers/20261125-literatur-genisletme-dogrulama.md` (abstract level).
- Git history: `git log`, commits a2a6a86 → 3be7fb4.
- Read-only check of `data/processed/player_season.csv.gz`.

Line numbers refer to the source files. Methods lines are counted from `# Methods`, and Discussion lines from `# Discussion`.

---

## 1. Decision

**Major revision. This is borderline: the remaining work is small, but some of it is not optional.**

What improved since round 3:
- **P1 is resolved.** The 2SLS is now specified correctly and run in both directions.
- **P2 is largely resolved.** The K = 5 sensitivity analysis and a role difference that does not depend on the reference role are reported.
- **Mostly resolved:** the Limitations now state the criterion assumption (M1b), the game-state mechanism (M9) and the mirrored-row dependence (M7).
- **Role-normalised PIR (OPEN_QUESTIONS #22) is now tested.**
- The Introduction now places the work in the literature.

Why this is not yet minor revision:
1. **New critical issue C1.** The Methods now say the number of roles "was fixed before the analyses reported here". The git history contradicts this.
2. **New critical issue C2.** The abstract's claim that role adjustment "removes this bias" was never tested.
3. **Critical issue C3.** Two Methods sentences describe things the code does not do.
4. **Three major items are still open in substance:** the common-sample out-of-time R² (M2), the game-state adjustment (M9), and an SWC or reference margin (M4). M4 is author-dependent.

C1–C3 and most of the major items can be fixed by the analyst in one pass.

## 2. Scores (1–5)

| Criterion | R1 | R2 | R3 | R4 | Comment |
|---|---|---|---|---|---|
| Originality | 3 | 3 | 3 | **4** | 24 sources now place the paper against box-score index critiques, plus-minus and lineup work. The role-adjusted remedy adds a genuine test. A sentence saying what is new relative to the thesis is still missing (author-dependent). |
| RQ–design fit | 3 | 4 | 4 | 4 | Unchanged. The role-adjusted analysis follows from Aim 1 → remedy. |
| Internal validity | 2 | 3 | 3 | **3** | 2SLS is fixed. Still open: the out-of-time minutes asymmetry favouring RAPM (M2), no game-state adjustment of the direct comparison (M9), and an untested bias-removal claim (C2). |
| Statistics | 2 | 3 | 3 | **3** | 2SLS is now correct, the R² point differences are reported, and K sensitivity is shown. Still missing: an SWC or reference margin, any check of the mirrored-row dependence (asserted to make intervals "somewhat narrow"), and the first-stage F. The common subset was silently redefined (N3). |
| Reporting-guideline compliance | 2 | 3 | 3 | **3** | A software paragraph has been added. Still missing: an English STROBE checklist and flow diagram, GMM settings, the thesis reference and declarations. Hard-coded numbers remain. Methods and code disagree (C3). |
| Discussion tied to evidence | 2 | 3 | 4 | **4** (at risk) | The Limitations are candid. But "removes this bias" (C2), "suggests that the problem lies in the box-score components", and three over-stretched citations (N4) would pull this back to 3 if left. |
| Practical implication | 3 | 3 | 3 | **3** | Role adjustment is now tested, which improves this. Without a reference margin, practitioners still cannot judge intervals ranging from −9.5 to +7.7 points per 100 possessions. |

Accept is not possible until every score is ≥ 4 and all critical issues are closed.

---

## 3. Point-by-point status of round-3 items

### Critical / administrative
| # | Status | Evidence / remaining action |
|---|---|---|
| K3 Prior work (thesis) | **Partly resolved. Author-dependent.** | `index.qmd:54` now names the corrections: the archetypes were not reproducible, and the ILP was not validated out of sample. This meets round-3 point 2. The companion manuscript is no longer called "under review" (point 3 met). **Open:** (1) the thesis `@phdthesis` entry, cited at `introduction.qmd:3`, `methods.qmd:9`, `methods.qmd:29` ("earlier work"); (2) a novelty sentence in the Introduction. Both are author-dependent. |

### Major
| # | Status | Evidence / remaining action |
|---|---|---|
| **P1** 2SLS exclusion | **Resolved** | `paper_b_values.py:119–138`: PIR40(h) ~ role + RAPM(h), with RAPM from the other half as instrument, h = even/odd. This is a valid instrument for classical split-half error: the even-game box-score noise that is correlated with even-game RAPM noise is exactly the endogeneity the instrument removes. Results agree in both directions (largest role difference 6.63 [5.78–8.00] and 6.73 [5.55–8.13]). **Minor residue:** (i) report the first-stage F (expected ≫ 10 given split-half r = 0.42, n = 481); (ii) still state that IV corrects classical noise, not ridge-shrinkage or role-specific bias in RAPM; (iii) say in the Fig. 2 caption (`results.qmd:23`) that the 2SLS points are the even-half specification. |
| **P2** K sensitivity | **Largely resolved, with a new critical issue (C1)** | K = 5: η² 0.33, partial η² 0.33 (0.27–0.40), largest difference 6.8. A reference-independent largest role difference is reported (6.81). The conclusions clearly do not depend on K. **Open:** (a) the "fixed before" statement is inaccurate; see C1. (b) The K = 5 2SLS and ILP − coach direct differences, requested in round 3, are not reported. This is low priority given the near-identical partial η²; one supplementary row each would do. |
| **M9** Game-state selection | **Partly resolved** | The Limitations now state the mechanism and cite `sampaio2026beyond` (`discussion.qmd:13`). **Open:** (i) No adjustment and no deployment-independent check. Adjusting y_adj for quarter and start-of-segment score margin inside the existing bootstrap is a one-regression change in `ilp_validation.py` (around lines 141–145). (ii) The likely direction is not stated. Coach-only units are concentrated in close, high-leverage minutes against opponents' best units; ILP-only units are concentrated in rest or garbage time. The opponent-RAPM adjustment absorbs only part of this. Say which way this biases the contrast. |
| **M1b** Criterion assumption | **Largely resolved** | `discussion.qmd:13` now states that bias interpretation assumes RAPM measures impact equally well in all roles. **Open (wording):** "same on-court impact" remains in the abstract Conclusions (`index.qmd:41`), `introduction.qmd:7` (twice: "same on-court impact", "same impact"), `methods.qmd:13`, `discussion.qmd:3` and `discussion.qmd:17`. Replace with "the same estimated RAPM" (or "the same plus-minus estimate"), at least in the abstract and Conclusions. |
| **M2** Out-of-time asymmetry | **Partly resolved** | (ii) The point differences are now reported (0.25 / 0.32 pp): **resolved.** (iii) The VAL40 criterion is now stated, but inaccurately; see C3b. **Open:** (i) No common-sample R² and no low-minutes indicator, so the only analysis that establishes RAPM's advantage is still biased toward RAPM. `sizinti_denetimi.hepsi_gorulmus` shows the analyst can already build the "all ten seen" subset (11.2% of test segments). Re-estimate the four test R² values on test segments in which all ten players have ≥ 300 training possessions and ≥ 90 training minutes, with a game bootstrap, or add a low-minutes count covariate to every model. (iv) `introduction.qmd:7` still says "RAPM predicts future lineup outcomes better" without qualification. Write "predicted ... better out of time". The `watts2026dummy` entry already in the .bib is directly relevant to how low-minute players are represented and could be cited there. |
| **M4** SWC / equivalence wording | **Partly resolved; SWC is author-dependent** | The title now says "no detectable advantage", the abstract says "no evidence of an advantage", and `results.qmd:37` says "differed detectably": **resolved.** **Open:** (i) `introduction.qmd:7` "show no advantage"; (ii) the Table 2 caption (`results.qmd:41`) "direct comparisons show no difference from it"; (iii) `discussion.qmd:13` "moderate advantages or disadvantages" conflicts with the abstract's "several points". Lower limits reach −8.5 to −9.5 in five variants. Write the limits: "disadvantages of up to about 9.5 and advantages of up to about 7.7 points per 100 possessions could not be excluded". (iv) There is still no SWC or post hoc reference margin. The choice of margin is author-dependent. The analyst can compute candidate anchors now, labelled post hoc: 0.2 × between-team-season SD of net rating, and the net-rating difference that corresponds to one win per season. |
| **M7** STROBE / clustering | **Partly resolved** | A software paragraph (`methods.qmd:33`) has been added, and the mirrored-row dependence is now acknowledged. **Open:** (i) The claim that it "makes the intervals somewhat narrow" is asserted, not checked. Run a two-way (game × team-season) bootstrap, or a bootstrap at the level of the game block within team-season pairs, for the direct comparison only, and report the change in width. (ii) GMM settings (tied covariance, n_init, reg_covar) are not given. (iii) `manuscript_b/STROBE.md` is unchanged since 18 Nov: Turkish, shared, item 22 empty. There is no English checklist with page/line numbers and no flow diagram. (iv) 156 versus 155 team-seasons (`takim_sezon_N` against `DAKIKA_yok.takim_sezon`) is unexplained. (v) Playoffs and traded players are not described. |
| M1a Alternative partition | Largely resolved | The variable lists now match the code, with "shot profile" covering fast-break and second-chance rates. Make that explicit. ARI against the main partition is still missing (minor). |
| M3 | Resolved | "Increased somewhat" (`discussion.qmd:13`) is still vague; give 0.54 → 0.95 (minor). |
| M5 | Mostly resolved | "Favoured the coach five in most optimisation variants" is now 9 of 12. Add that these point estimates share the coach group and largely the same players, so the count is not independent evidence (minor). |
| M6 | Largely resolved | Still open: the sensitivity analysis excluding 2016–17; disclosure that the pooled GMM saw later seasons; the dead sub-expression `all(... for x in ())` at `ilp_validation.py:120`. |
| M8 Provenance | Largely resolved | `provenance.git_commit` = 256379c. The analysis code is unchanged from that commit to HEAD, except `figures_paper_b.py`, and the working tree is clean: acceptable. **Open:** `results.json` is still git-ignored (`.gitignore:11`), so the cited "results file (`provenance`)" is not public. There is still no dirty-tree flag in `provenance.py`. |

### Round-3 minors
| # | Item | Status |
|---|---|---|
| 1 | Hard-coded numbers | **Open.** "Nine" (`index.qmd:39`, `discussion.qmd:3`; `A["seasons"]` exists), 60 min, 300 possessions, 90 min, 10 games, 100 first-half minutes, λ = 1,000, five-fold, 500 resamples. The main λ (4,000) and the CV grid are still not reported. |
| 2 | Typography (U+2212) | **Open.** Abstract "-0.03 … -0.10", "-3.6"; throughout ("-3.00 to -1.34", "-0.60 to 1.64"). Fix `ci()`, `cipp()` and the abstract f-strings. |
| 3 | Fig. 1 without uncertainty | **Open** (caption unchanged). The new Fig. 2 (conditional, with CIs) partly answers this. Either add CIs to Fig. 1 or move it to the supplement. |
| 4 | Literature / mechanisms / bib | **Partly resolved.** Positioning is much improved, but `sampaio2006discriminant` and `konca2026from` are still not cited. "Spacing the floor and moving the ball are only partly recorded" (`discussion.qmd:5`) and "so their rotations already favour the best players" (`discussion.qmd:9`) are still asserted. The latter is now followed by `guo2022exploring`, which does not support it (N4). `grassetti2020extended` still lacks DOI, volume and pages; `kalman2020lineup` still lacks a venue; `ghimire2020measuring` lacks DOI and pages. `smith2006optimizer` still has no verification note. |
| 5 | ω² / CI for corrected η² | Open. |
| 6 | Role-normalised PIR | **Resolved** (tested); see §5 for the evaluation. |
| 7 | Target alignment | **Open.** `discussion.qmd:13`, "does not presuppose that RAPM is correct": add that RAPM is fitted to the same target (segment net rating) on which it is tested, whereas PIR is not. |
| 8 | Generalisation | **Open.** `discussion.qmd:5`, "for example in scouting or contract decisions": add "in EuroLeague-level competition". |
| 9 | Declarations | Author-dependent. |
| 10 | "the constraint used in earlier work" | **Open** (`methods.qmd:29`). Write "analogous to". |

---

## 4. New critical issues

**C1. Inaccurate statement about analysis order** (`methods.qmd:13`: "in which the number of roles was fixed before the analyses reported here")
- Git history contradicts this:
  - Paper B analyses were run and reviewed with **K = 5** (commits a2a6a86 and 2bcaf4b; reviews round 1 and round 2).
  - The companion analysis switched to K = 4 afterwards (9d72224, "Paper A round 2: four-role main solution").
  - Paper B's role results then changed: η² 0.33 → 0.26; headline contrasts +6.5/+6.8 → +4.6/+4.3.
- It is true that K was chosen on stability criteria in the companion analysis, without reference to Paper B outcomes. It is not true that it was fixed before these analyses.
- Q1 editors treat misstatements of analysis order as a research-integrity issue, even when the substantive results are robust, as they are here.
- **Fix:** "The number of roles was chosen in the companion analysis by bootstrap stability, without reference to the outcomes analysed here. An earlier version of the present analyses used the five-role solution of that analysis; those results are reported as a sensitivity analysis." Keep the K = 5 row.

**C2. "Adjusting them for role removes this bias" is untested** (`index.qmd:41`, abstract Conclusions; also `discussion.qmd:5`, "makes PIR fairer for comparisons across roles")
- The bias is defined as role differences in PIR **at equal RAPM**. Role-adjusted PIR subtracts **unconditional**, minutes-weighted role means.
- In sample, this removes unconditional role η² by construction. Whether it removes the conditional difference is a separate empirical question.
- From the stored role means, the residual conditional differences are probably small (raw rim-protector minus ball-handler gap 4.77 against conditional 4.61). But this was not estimated, and it was not estimated out of sample, where role means come from other players or periods.
- No number in results.json supports the sentence.
- **Fix (analyst):** compute partial η² and the largest role difference of role-adjusted PIR at equal RAPM, with player-bootstrap CIs. Do it out of sample: training-period role means applied to test-period players, or role means cross-fitted over player folds. Store the result in `paper_b_values`. If this is not done, rephrase as "subtracting role means removes the average role differences by construction".

**C3. Methods text does not match the code**
- (a) `methods.qmd:17`: in the within-season analysis "the means were computed among the team-season's players". In `ilp_validation.py:105–111`, `rmean` is computed over **all players active in the season's first half** (league-wide, by role), not within team-season. Correct the text.
- (b) `methods.qmd:21`: "VAL40 from player-seasons with at least 10 games and 90 minutes". `lineup_model.py:131–133` applies no filter of its own. `player_season.csv.gz` contains 10 of 2,014 player-seasons with G < 10 (minimum G = 7; minimum MIN = 90). Either state the criterion the data actually satisfy ("player-seasons in the thesis data set, ≥ 90 minutes"), or apply G ≥ 10 in code and re-run. The effect is negligible, but the description must be exact.

## 5. Evaluation of the role-adjusted PIR analysis

The analysis is well motivated and correctly placed in time. Out of time, it uses training-period main roles and training-period role means (`lineup_model.py:152–158`). Within seasons, it uses previous-season roles and data available at the split. It is reported in all three analyses. Its interpretation, however, goes further than the data allow in four places.

1. **The test of bias removal is missing** (C2).

2. **The predictive null may be largely uninformative, and the paper should show this.**
   - Within a lineup sum, role adjustment changes the value only through the role composition of the five: Σ PIR − Σ role means. Most EuroLeague fives contain one or two bigs, so the role component varies little across lineups, and summed adjusted and unadjusted PIR are probably very highly correlated.
   - A null difference is then nearly guaranteed. It says little about whether the role component is "noise" or "signal".
   - **Fix:** report the possession-weighted correlation between summed PIR40 and summed role-adjusted PIR40 in test segments (and within team-season for the second-half segments), and the SD of the role-composition term.
   - The informative statement the data *do* support is a bounded one: the out-of-time gain from role adjustment is at most +0.03 pp (upper CI limit), against a RAPM advantage of 0.14–0.44 pp. Role adjustment therefore cannot close the gap to RAPM. Say this.

3. **"Suggests that the problem lies in the box-score components and their weights rather than only in their distribution across roles"** (`discussion.qmd:5`). This is a reasonable hypothesis, but given point 2 it is not demonstrated. Label it as an interpretation ("is consistent with").

4. **Wording of the null.**
   - "Does not improve their predictive validity" (abstract) → "did not detectably improve".
   - "No more than unadjusted PIR40" (`results.qmd:27`) is fine. Add the bound.
   - "Behaved like optimisation on unadjusted PIR40" (`results.qmd:37`) is reasonable: −1.96 to 0.71 against −3.02 to −0.36, with overlapping CIs. It is not a test. Role-adjusted fives also share the most players with the coach five (3.06–3.15). This is worth one clause, because it supports the "coaches already pick the best players within role" interpretation.

Two further points:

**N3. Common subset redefined (forking path).**
- Adding `PIR40_rol` to `COMMON` (`ilp_validation.py:47`) reduced the common subset from 77% to 75.5% of segments, because role-adjusted PIR requires a previous-season role.
- This changed the round-3 common-subset results: RAPM 1.10 → 1.21; minutes 0.62 → 0.60; paired CIs changed.
- These are small, but a robustness subset should not shift each time a measure is added.
- **Fix:** define the common subset by the round-3 measures (pooled PIR40, VAL40, RAPM, minutes). Report role-adjusted PIR on its own coverage (75.5%), or report both subsets.

**Pooled PIR against previous-season role.** Within seasons, pooled PIR mixes all prior seasons, but the role is that of the last season. For players who changed role, adjusted value is mis-centred. This is minor; one clause will do.

## 6. Citation audit

`python engine/check_cites.py` → "Atıf denetimi: OK". A manual grep confirms that all 24 keys used in Paper B resolve in `manuscript/references.bib`, and that every key appears exactly once in the .bib.

Content against the verification note (abstract level):

| Key | Use in manuscript | Supported by note? | Verdict |
|---|---|---|---|
| carta2026winscore | PIR weights lack formal justification (Intro, Disc.) | Yes | OK |
| marmarinos2019structural | "indices built from the same box-score data can be more valid and reliable than PIR" (Intro); "alternative box-score indices can be…" (Disc.) | One index (TPI) only | **Minor over-generalisation:** write "an alternative box-score index (TPI) was more valid and reliable than PIR" |
| senatore2022efficiency | Intro: productivity, weight on scoring (OK). Disc.: "simple efficiency indices weight scoring heavily and are **not comparable across tactical roles**" | The note says *reducing* the point weight allows role-independent comparison; the converse is an inference, and the index is Ei, not PIR | **Minor:** "…and that reducing the weight of points allowed players to be compared independently of their tactical roles" |
| martinez2012factors | Weight on scoring (Intro) | Yes ("separating scoring") | OK |
| berri2012measuring | Consistency over time, relation to winning (Intro) | Yes | OK |
| franks2016meta | Intro: stability, discrimination, independence (OK). Methods: "stability of a metric is a **precondition** for its use" | The note says only "evaluated by" | **Minor:** "one of the criteria by which metrics are evaluated" |
| hvattum2019comprehensive | RAPM description (Intro) | Yes (review) | OK |
| terner2021modeling | RAPM description (Intro) | General review; the note lists it for Paper A | Acceptable |
| ghimire2020measuring | "RAPM has itself been **shown to depend** on teammate quality **and complementarities**" (Limitations) | The note says it is *related* to teammate quality and *does not capture* complementarity; the note also lists "**not suitable for out-of-sample prediction**" | **Major (N4):** (i) the wording inverts "does not capture complementarity" into "depends on complementarities"; (ii) the source's out-of-sample finding bears directly on the paper's out-of-time RAPM claim and is omitted. Write: "RAPM estimates have been reported to be associated with teammate quality and not to capture complementarities between players, and their out-of-sample predictive value has been questioned [@ghimire2020measuring]". Then reconcile this with the present out-of-time result: small absolute R², single league. Also complete the .bib entry (DOI, pages) via `sspe-doi`. |
| damoulaki2025lasso, josephs2025hypergraph | Alternative plus-minus formulations (Limitations) | Yes | OK |
| gomez2016exploring | Substitution effects (Intro) | Yes | OK |
| guo2022exploring | Intro: substitution networks (OK). Disc. :9: appended to "so their rotations already favour the best players; rotation structures themselves are associated with team success" | The second clause is supported (playoff standing); the first is not supported by any source | **Minor:** mark the first clause as a hypothesis ("may already favour") |
| sampaio2026beyond | Game state affects rotations (Limitations) | Yes | OK |
| metulini2022measuring | Shapley best lineups (Intro) | Yes | OK |
| courelibanez2025profiling | Role-specific reference values (Methods, Disc.) | Yes; population is the Spanish **women's** league | OK. Optionally note the population. |
| muniz2022sports, grassetti2020extended, hennig2007cluster, kalman2020lineup, kubatko2007starting, martonosi2023predicting, ribes2026identifying, smith2006optimizer | Unchanged from round 3 | — | OK in content. Bib completeness is still open for grassetti and kalman, and smith2006 has no verification note (minor 4). |

General caveat: every new claim was verified **at abstract level only**. That is acceptable for the descriptive uses above. Before submission, ghimire2020measuring and senatore2022efficiency, which carry interpretive weight, should be checked against full text.

## 7. Number consistency with results.json (checked in the rendered docx)

| Claim (location) | results.json | Status |
|---|---|---|
| 2,646 games; 64,549 segments; 48,309 / 16,240; 76% seen | `paper_a.games`; `lineup_model_roles_final_K4` | OK |
| Abstract: 26% / 0.5%; 27% partial; 4.6 / 4.3 vs ball handlers | `eta2` 0.263 / 0.005; `kismi_eta2` 0.271; `rol_farki_RAPM_sabit` 2 = 4.61, 4 = 4.33 | OK |
| Partial η² 0.27 (0.21–0.34); 4.6 (3.52–5.75); 4.3 (3.11–5.57); −2.2 (−3.00 to −1.34); largest 6.8 | `RAPM_kosullu.PIR40` incl. `rol_araligi` 6.81 | OK |
| 2SLS: 4.3 (3.01–5.41), 4.6 (3.07–5.89), largest 6.6 (5.78–8.00); swapped 6.7 (5.55–8.13); n = 481 | `olcum_hatasi_denetimi.cift/tek` | OK; Fig. 2 plots `cift` |
| K = 5: η² 0.33, partial 0.33 (0.27–0.40), largest 6.8 | `K_duyarliligi` 0.327 / 0.331 [0.271, 0.396] / 6.77 | OK |
| Non-PIR η² 0.30 / 0.28; RAPM 0.006; reliability 0.91 / 0.59 (n = 485); corrected 0.009 / 0.29; SD 1.64 → 3.03; η² 0.003; r = 0.24 | `pir_bilesensiz_roller(_kati)`, `guvenirlik`, `eta2_duzeltilmis`, `rapm_sd`, `korelasyon` | OK |
| Table 1 role n and means | `rol_N`, `rol_ortalamasi_ham` | OK |
| Out of time: 0.36 / 0.11 / 0.05%; differences 0.25 (0.10–0.39), 0.32 (0.17–0.45) | `test_R2` | OK (point differences now reported) |
| Role-adjusted: 0.08%; −0.03 (−0.10 to 0.03); vs RAPM 0.14–0.44 | `PIR40_rol_toplami` 0.00083; `fark_GA95` | OK |
| Slopes: RAPM 1.76 (0.90–2.64), minutes 1.07 (0.02–1.98), PIR40 0.51 / 0.78, VAL40 0.95, role-adjusted 0.59 (−0.54–1.75); coverage 83% | `amac_fonksiyonu_egimi`, `kapsam` | OK |
| Common subset 76%; RAPM 1.21 (0.21–2.27); minutes 0.60 (−0.53–1.65); paired −0.70–1.87, −0.50–1.76 | `ortak_alt_kume` (0.755 → "76") | OK numerically; definition changed (N3) |
| Coach five 3.84 (1.35–6.13) | `ilp_beslisi.DAKIKA_yok` | OK |
| Direct: −3.61 to 1.49 (abstract −3.6 to +1.5); widest 13.1 (Limitations "13"); role-adjusted −1.96 to 0.71; 44–49% excluded | `dogrudan_eslestirilmis_fark` (widest VAL40_sezon_tez 13.09; shares 0.435–0.494) | OK |
| Table 2 (36 cells checked for role-adjusted rows; spot checks elsewhere) | `ilp_antrenore_gore_fark`, `dogrudan_eslestirilmis_fark`, `antrenor_beslisiyle_ortak_oyuncu` | OK |
| 34% current-season constraint roles | `kisit_rolu_cari_sezondan_pay` | OK |
| "Adjusting for role removes this bias" (abstract) | **No supporting value** | **C2** |
| "VAL40 … at least 10 games" | Data: min G = 7 | **C3b** |

No inline number contradicts results.json. Figures 2–4 match the stored values. Fig. 1 is unchanged.

## 8. Checklist

| Item | Status |
|---|---|
| Sample justification | Thresholds stated but not justified. No precision rationale for the direct comparison (104–141 team-seasons). |
| Clustered data | Team-season bootstrap. Mirrored-row dependence is acknowledged but not checked (M7). |
| Multiple comparisons | Acknowledged. Adequate for estimation framing. |
| Effect size + CI | Yes throughout. First-stage F, ω², and CIs for corrected η² are missing. |
| SWC/TE | **Absent** (M4; author-dependent choice). |
| Causal language | Appropriate. "Removes this bias" (C2) and "so their rotations already favour the best players" are asserted. |
| Limitations | Comprehensive. Missing: the direction of the game-state bias, target alignment, the uninformativeness of the role-adjusted null. |
| Over-generalisation | Minor (scouting sentence; Marmarinos plural). |
| MBI | Not used. |
| p-hacking signals | K change now shown as sensitivity, but misdescribed (C1). Common subset redefined (N3). |
| Data/code availability | Public API + GitHub. results.json is git-ignored; DOI archive pending. |
| AI statement | Present and adequate. |

---

## 9. Prioritised list of remaining items

### (a) Fixable now by the analyst
1. **C1:** rewrite the K sentence at `methods.qmd:13` (wording supplied above).
2. **C2:** compute out-of-sample partial η² and the largest role difference at equal RAPM for role-adjusted PIR, with CIs, and store them in `paper_b_values`. Otherwise rephrase the abstract Conclusions and `discussion.qmd:5`.
3. **C3:** correct the role-mean description (`methods.qmd:17`) and the VAL40 criterion (`methods.qmd:21`), or apply G ≥ 10 in code.
4. **N4 / citations:** reword the Ghimire sentence and add its out-of-sample caveat. Fix Marmarinos (single index), Senatore (direction), Franks ("precondition") and the Guo-attached hypothesis. Complete the .bib entries for grassetti, kalman and ghimire via `sspe-doi`. Add a verification note for smith2006.
5. **Role-adjusted interpretation (§5):** report the correlation between summed PIR and summed role-adjusted PIR and the SD of the role term. State the bound (≤ +0.03 pp against a RAPM gap of 0.14–0.44 pp). Soften "problem lies in components". Write "did not detectably improve".
6. **N3:** restore the round-3 common-subset definition, or report both.
7. **M2(i):** common-sample out-of-time R² (all ten players seen, with possession and minute thresholds), or a low-minutes covariate. Qualify `introduction.qmd:7`.
8. **M9:** quarter and score-margin adjustment in the direct comparison, plus one sentence on the likely direction of bias.
9. **M4 wording:** `introduction.qmd:7`, the Table 2 caption, and Limitations "moderate" → explicit limits (−9.5 / +7.7). Prepare the candidate reference-margin anchors for the author.
10. **M1b wording:** "same estimated RAPM" in the abstract, Introduction, Methods, Discussion and Conclusions.
11. **M7:** two-way-cluster sensitivity for the direct comparison; GMM settings; 156/155 explanation; playoffs and traded players; English STROBE checklist with line numbers; flow diagram.
12. **P1 / P2 residue:** first-stage F; "IV does not correct shrinkage" clause; name the half in the Fig. 2 caption; K = 5 2SLS and direct-difference rows in the supplement.
13. **Minors:** U+2212 in `ci()`, `cipp()` and the abstract; move hard-coded constants and λ_main = 4,000 into results.json; Fig. 1 CIs or move to supplement; ω²; target-alignment sentence; "EuroLeague-level" generalisation; "analogous to" (`methods.qmd:29`); M3, M5 and M6 residues (2016–17 exclusion, pooled-GMM clause, dead code at `ilp_validation.py:120`); ARI for the alternative partition; cite `sampaio2006discriminant` / `konca2026from`; `provenance.py` dirty flag; un-ignore or archive `results.json`.

### (b) Author-dependent
1. **K3:** thesis `@phdthesis` entry from the YÖK record (documented manual route), cited at the three locations listed in §3, plus an Introduction sentence on what is new relative to the thesis and the companion paper.
2. **SWC / reference margin:** choose and justify the margin (the analyst supplies the candidates). Then classify each direct-comparison interval against it.
3. **Front matter and declarations:** affiliation, ORCID, funding (STROBE item 22), competing interests, author contributions.
4. **Companion manuscript status:** confirm "submitted" or "in preparation", and supply it to the editor.
5. **Persistent archive** (Zenodo DOI) of code and results.json at submission.
6. **Full-text check** of ghimire2020measuring and senatore2022efficiency (only abstracts were verified).

**Path to acceptance:** close C1–C3 and items (a) 4–10. Once the author supplies the thesis reference and an SWC, this manuscript can reach minor revision or accept in the next round. The substantive conclusions (role dependence of PIR; no detectable advantage of optimisation over the coach) have held up across four rounds of checks.
