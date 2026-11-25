# Review – Round 4

**Manuscript:** "Functional player roles in EuroLeague basketball: stability, positional overlap and no robust added value for lineup performance beyond player quality"
**Reviewer role:** Senior reviewer (Q1 sports science / sports analytics)
**Date:** 2026-11-25
**Material reviewed:** `index.qmd`, `sections/{introduction,methods,results,discussion}.qmd`, `_output/index.docx` (rendered 08:45:28, after `results.json` 08:45:23, so it is current), `figures/fig1–6`, `references.bib`, `analysis/results.json` (keys `roles_final`, `role_trends`, `lineup_model_roles_final_K4/K5`, `lineup_model_thesis_archetypes`, `paper_a`, `provenance`), `analysis/role_trends.py`, `analysis/lineup_model.py`, `OPEN_QUESTIONS.md`, `literature/answers/20261125-literatur-genisletme-dogrulama.md`, `literature/answers/20261118-rol-dizilim-calismalari-dogrulama.md`, `reviews/round-1..3.md`.

Line numbers refer to the `.qmd` source files.

---

## 1. Decision

**Major revision (narrow scope; no new data needed).** Every round-3 critical item has been resolved or reduced to a residual, which is real progress. But the new trends section and the revised leakage text bring in new statements that the CIs in `results.json` contradict. The leakage checks that drop roles for new players also have a coding asymmetry that biases them against any gain. And several of the new citations are used for claims their verification note does not support.

The thesis reference and the front matter are author-dependent (§7b). They do not affect this scientific verdict.

## 2. Scores (1–5)

| Criterion | R1 | R2 | R3 | R4 | Comment |
|---|---|---|---|---|---|
| Originality | 3 | 4 | 4 | 4 | Stability-first roles, a RAPM-anchored permutation test, a split leakage check and now a longitudinal view. This is a useful package for the role literature. |
| RQ–design fit | 3 | 4 | 4 | 4 | Aim 2 now has a time dimension. The design deliberately separates relative structure (standardised within season) from absolute style (raw variables), which is good. |
| Internal validity | 2 | 2 | 3 | 3 | The split check (new players without a role) is the right idea. But checks 1–2 apply a composition model trained on fully role-coded lineups to test lineups that contain an "unassigned" category, which penalises the gain by construction (R4-C2). The trend CIs keep role labels fixed and ignore season-level variation (R4-M1). |
| Statistics | 2 | 2 | 3 | 3 | Power is now correct (true co-occurring pair, δ = 0 control, 100 replicates), and every gain has a game-bootstrap CI. Still missing: a smallest worthwhile effect or equivalence bound, a confirmatory designation and multiplicity control. About 25 unadjusted trend CIs have been added. |
| Reporting-guideline compliance | 2 | 3 | 3 | 3 | Scientific items are mostly complete. Missing: an English STROBE checklist with page numbers, the AI model and version, the raw-variable bootstrap B, an archive DOI, and the front matter (the last two are author-dependent). |
| Discussion tied to evidence | 2 | 2 | 3 | 3 | The positional-overlap text is now correct. New overreach: "stable / did not erode / differs from the NBA" (R4-C3), "showed that this gain depended on … new players" (R4-C2), and four citation claims beyond their notes (R4-C4). |
| Practical implication | 2 | 3 | 3 | 3 | Role persistence (84%) now supports scouting use (R3-m3 resolved). The new recommendation to combine the roles with @courelibanez2025profiling reference values goes beyond that source (R4-C4). |

Accept is not possible: no score is 5, five scores are below 4, and four new critical issues are open.

---

## 3. Status of round-3 critical and major issues

| # | Issue | Status | Evidence / residual |
|---|---|---|---|
| R3-C1 | Power pair and "65%" mis-described | **Resolved (K = 4)** | The code now selects by true presence (`lineup_model.py:301–309`). BH × W/F is present in 95.5% of training and 95.8% of test lineups (`guc.cift_dizilim_payi_*`), which matches my round-3 recomputation. Methods (`methods.qmd:33`) and Results (`results.qmd:75`, "96% of test lineups") are correct. There is now a δ = 0 control (7%) and 100 simulations. *Residual (minor):* the `lineup_model_roles_final_K5.guc` block is stale (50 simulations, old `cift_test_frekansi` definition, no δ = 0). It is not printed, but rerun it or delete it. |
| R3-C2 | "Disappears/vanished" from two non-significant checks | **Largely resolved, replaced by R4-C1/C2** | Game-bootstrap CIs are given for every gain, the requested split check was added (`yeni_oyuncu_rolsuz`), and the Introduction now says "not robust". New problems: the summary wording contradicts the CIs (R4-C1), and checks 1–2 are biased by coding (R4-C2). No minimum detectable gain is given for the all-seen subset. |
| R3-C3 | "Frontcourt" contradicts Table 3 | **Resolved (residual minor)** | Results (`results.qmd:57`), Discussion (`discussion.qmd:7`) and the Introduction are now correct ("guards and forwards on the wing … forwards and centres inside"). *Residual:* the abstract (`index.qmd:63`) still names only interior bigs as mixed and omits the wing/forward role (24% guards). `discussion.qmd:3` says "tied" where "largely tied" is meant. |
| R3-C4 | Text and tables vs `results.json` | **Resolved** | (a) BIC: "lowest at six roles and changed little between five and eight" is correct (61,232 at K6; 61,321 / 61,361 / 61,257 at K5/K7/K8). (b) Table 4 caption reworded. (c) Fig. 3 caption now refers to the table. (d) The Ward-7 B (200) is stated. (e) Table 2 is from a separate B = 100 run, and this is disclosed (`methods.qmd:19`). |
| C9″ | Thesis not cited | **Unchanged – author-dependent** | `index.qmd:79` is unchanged. This blocks submission, not the scientific verdict (`OPEN_QUESTIONS.md` #37/#48). |
| R3-M1 | Two-stage design limits power | **Partly resolved** | Done: δ = 0 control, 100 replicates, the true pair, and absorption by RAPM stated in Results (`results.qmd:75`). Open: (i) MC SE ≈ 5 pp at 53%, so ≥ 200 replicates are still advisable. (ii) Only one pair, and the most favourable one (96% presence); add one rare pair. (iii) There is no joint model. (iv) The Limitations (`discussion.qmd:15`) still attribute low power to noise only, whereas Results correctly names absorption. (v) "Excludes … about two points or more" (`results.qmd:75`) is a power statement, not an exclusion. Write "would very likely (95%) have been detected". |
| R3-M2 | No smallest worthwhile effect or equivalence bound | **Not resolved** | All gains are still in R² hundredths of a pp. The value is author-dependent (#47), but the analyst can implement the framework now (§7a-7). |
| R3-M3 | Multiplicity, no confirmatory test | **Partly resolved** | Table 4 now says "not adjusted for multiplicity", which is good. There is still no confirmatory designation and no Holm adjustment. Exploratory thesis p-values are still interpreted (`results.qmd:73`; `discussion.qmd:11`, "a small gain persisted"), although the game-bootstrap CIs of those same gains include zero (thesis new-players-without-role: −0.008 to 0.075; all-seen: −0.084 to 0.202). |
| R3-M4 | Literature claims beyond sources | **Largely resolved** | "Three to nine" is now used, Penner is no longer cited for a role count, and Petridis is moved to the method sentence. Open: there is no primary RAPM/APM source. `hvattum2019comprehensive` is already in the .bib and verified, so cite it at `methods.qmd:31`. CLAUDE.md rule 4 (`sspe-ask`) is still met only by manual verification (#42). New problems: R4-C4. |
| R3-M5 | Variable group confounded with count | **Resolved** | Captions are descriptive, and `discussion.qmd:5` states the confound explicitly. |

---

## 4. Critical issues (block publication)

### R4-C1. "No positive gain in any of the three leakage checks" and "intervals … include gains of the size observed" contradict `results.json`
- **Location:**
  - `index.qmd:64` (abstract: "no positive gain remained in three leakage checks")
  - `results.qmd:73` ("However, no positive gain was found in any of the three leakage checks"; "These intervals are wide and also include gains of the size observed with season-specific roles"; "The five-role solution behaved similarly (no positive gain in any check)")
  - `discussion.qmd:11` ("no positive gain remained")
- **Evidence** (`sizinti_denetimi`; counts gain in pp, game-bootstrap 95% CI; permutation p):

  | Check | K = 4 | K = 5 |
  |---|---|---|
  | Original (season-specific roles) | 0.032 (0.014 to 0.051) | 0.036 (0.020 to 0.055) |
  | Training-period roles | −0.048 (−0.090 to **0.000**), p = .361 | −0.032 (−0.066 to 0.007), p = .176 |
  | New players without role | −0.024 (−0.066 to **0.017**), p = .070 | −0.005 (−0.041 to 0.028), **p = .018** |
  | All players seen (11.2%) | **+0.011** (−0.045 to 0.061), p = .152 | **+0.026** (−0.025 to 0.077), p = .094 |

  - "No positive gain" is literally false for the all-seen check at both K. The point estimates are positive; they are just imprecise.
  - "Include gains of the size observed" is true only for the all-seen check. The upper limits of the other two checks (0.000 and 0.017 pp) **exclude** the original 0.032 pp. So the evidence is stronger than the text says for two checks, and weaker for the third.
  - For K = 5, the split check is significant under the permutation criterion that the paper uses as its primary test (p = .018). "Behaved similarly" hides this.
- **Fix:**
  - Replace "no positive gain" with "no gain distinguishable from zero".
  - Report per check whether the CI excludes the original gain: yes for training-period roles and new players without role (K = 4); no for the all-seen subset.
  - Report the K = 5 split-check p = .018 and interpret it together with R4-C2. Say which criterion (gain over RAPM, or gain over permuted labels) governs the conclusion, and apply it consistently. The same inconsistency affects the thesis solution: counts p = .002 while the CI is −0.009 to 0.081.

### R4-C2. Leakage checks 1–2 are biased against a gain by a coding asymmetry, so "showed that this gain depended on … new players" is not demonstrated
- **Location:** `lineup_model.py:185–188`, `:242–258` (`prior_map`, `split_map`); `results.qmd:73` ("which isolates the new-player mechanism"); `discussion.qmd:11` ("The leakage checks showed that this gain depended on role labels … which carry information about players new to the league"); `discussion.qmd:19` ("Once leakage … was removed").
- **Problem:**
  - In `comp_gain`, the composition model is always **fitted on training lineups in which (almost) every player has a role**. Only then is it applied to test lineups in which new players are coded 0 (unassigned).
  - Count differences no longer sum to zero across roles in those test lineups. The model therefore predicts off its training support.
  - The negative point estimates are the signature of this. Most clearly, the thesis training-period check is significantly *worse than RAPM alone* (−0.071 pp, CI −0.109 to −0.035), which a neutral "information removed" check cannot produce.
  - The permutation null uses the same coding (`split_map(permuted())`), so the permutation p-values are internally fair. The "gain over RAPM" and its CI are not. This is also why K = 5 gives p = .018 with a negative gain.
- **Fix (choose one):**
  1. **Preferred rerun:** apply the same coding in training. For checks 1–2, code each training lineup the way test lineups are coded: each player's previous-season role, and unassigned in his first EuroLeague season. Refit the composition model on that, then evaluate. Report gain, CI and permutation p.
  2. Alternatively, make the permutation comparison primary for checks 1–2 and state that the "gain over RAPM" in these checks is downward-biased by the coding.

  In either case, reword `discussion.qmd:11` to: "the gain was not robust to restricting role information to what was available before the test period; this is consistent with, but does not prove, role labels acting as a proxy for the quality of new players."

### R4-C3. The trend claims go beyond their CIs (absence of evidence presented as stability)
- **Location:**
  - `index.qmd:63` ("showed no trend"), `index.qmd:66` ("their relative structure was stable over nine seasons")
  - `results.qmd:63` ("was stable"; "did not weaken"; "did not increase")
  - `discussion.qmd:9` ("did not erode"; "a stable feature … rather than an ongoing dissolution of roles, which differs from …"; "the absolute style of every role, except that of rim protectors, moved with the league"; "rim protectors specialised further")
  - `discussion.qmd:19`, `introduction.qmd:8`
- **Evidence** (`role_trends.K4`; slope per season × 8 seasons = change compatible over the study period):

  | Quantity | Slope per season (95% CI) | Change compatible over the period |
  |---|---|---|
  | Ball-handler share | +0.69 pp (−0.52 to 1.80) | −4 to **+14 pp**, on a base of 36% |
  | Rim-protector share | −0.55 pp (−1.27 to 0.21) | **−10** to +2 pp, on a base of 15% |
  | Wing/forward share | −0.63 pp (−1.77 to 0.56) | −14 to +4 pp |
  | Cramér's V | 0.0002 (−0.010 to 0.010) | a decline of up to **0.08** (0.72 → 0.64) is not excluded |

  - The observed ball-handler share went from 35.7% to 39.9%, and the rim-protector share from 14.7% to 11.1%. These are not small; they are imprecise.
  - **Within-role 3PAr:** the CIs include zero for **every** role (`ham_degisken_egilimi.3PAr.rol.*.egim_GA95`). "The absolute style of every role except rim protectors moved with the league" is therefore not shown.
  - A rough decomposition with the reported values attributes about 70% of the league rise to within-role change and about 25% to the growth of the high-3PAr ball-handler share. Report this properly.
  - **"Rim protectors specialised further":** this rests on a CI lower bound of **0.0001** (`rim_rate.rol.2`), one of about 25 unadjusted trend CIs (5 variables × 4 roles + league). About one CI of 20 is expected to exclude zero by chance. The usage decline (−0.0063 to −0.0014) is more robust.
  - **"Differs from … the NBA" (Durmuş; Madeira):** this study did not measure within-position variability or perimeter-profile consolidation, so no contrast was tested.
  - **League 3PAr rise (abstract):** this is given as endpoints only. The league slope (`lig_egim` 0.005) has **no CI**.
- **Fix:**
  - Use "no detectable trend" and state the change compatible with the data (e.g., "changes in role shares of up to ±10–14 pp over the period, and a decline in Cramér's V of up to 0.08, could not be excluded").
  - Remove "stable / did not erode / did not weaken" from the abstract and Conclusions, or define an equivalence margin and test it.
  - Add a CI for the league 3PAr slope and report the within-role vs composition decomposition.
  - Downgrade "specialised further" to "the rim-attempt share of rim protectors tended to rise (CI lower bound ≈ 0)" and flag it as exploratory.
  - Delete the "every role moved with the league" clause.
  - Rephrase the NBA comparison as "whether the NBA findings … apply to the EuroLeague cannot be judged from relative roles".

### R4-C4. New citations used beyond their verification note (`20261125-literatur-genisletme-dogrulama.md`)

| Key | Location | Text claim | Note supports | Fix |
|---|---|---|---|---|
| foteinakis2025decade | `introduction.qmd:3`; `discussion.qmd:9` | 3PA "have risen steadily … in the leading European leagues"; "long-term increase … in European leagues" | Only "the EuroLeague relies more on three-point shooting than the NBA" (a cross-sectional comparison, not a rise) | Remove it from both increase clauses. Optionally use it for "EuroLeague teams attempt relatively more threes than NBA teams". |
| silva2021three | `introduction.qmd:3` | 3PA "have risen steadily in the NBA" | "Three eras; modern era since 2013" | Remove it from this clause, or verify a 3PA trend in the abstract and add it to the note. |
| courelibanez2025profiling | `discussion.qmd:19` | "use these roles, together with role-specific reference values" | Six roles and normative values for the **Spanish women's league**, which are not these four roles | Reword: "analogous to the role-specific reference values proposed for women's basketball [@courelibanez2025profiling], EuroLeague reference values could be derived for these roles". |
| grassetti2026revisiting | `discussion.qmd:11` | "Plus-minus studies of the NBA **likewise** find that synergies … have become less important over time" | The note supports the NBA finding. But this study did not examine synergy over time, so "likewise" is a non sequitur, and "studies" is plural for one source. | Delete the sentence or reword: "In the NBA, the importance of player synergies in RAPM models has declined over time [@grassetti2026revisiting]; whether this holds in the EuroLeague was not tested here." Also, the .bib entry has **no DOI** and is not in `sspe-doi` format: re-fetch it via `sspe-doi` (rule 1). |
| (no key) | `introduction.qmd:3` | "In the EuroLeague … the full set of player roles has not been derived" | The project's own sources show women's-EuroLeague roles (@pendolareinecke2025exploring, 3 roles) and a EuroLeague GMM with season-to-season transitions (@vazquezguerrero2026shooting; shooting profiles) | Qualify: "in the men's EuroLeague, a full role partition from open data covering all players has not been reported", and contrast it with these two studies. |
| durmus2026from, madeira2026tempo | `discussion.qmd:9` | "which differs from …" | The notes support the NBA findings. No comparable EuroLeague measure exists here (see R4-C3) | As in R4-C3. |
| mourer2023selecting | `discussion.qmd:15` | "Stability criteria **tend to favour** partitions that are too coarse" | "Stability alone cannot detect a K that is too small" | Minor wording change: "stability alone cannot detect a number of roles that is too small". |

Verified as within their notes: zajac2023long, nietoacevedo2025modern, gomez2020performance, garcia2026immediate, garcia2026assist, fewell2012basketball, durmus2026from (Introduction use), madeira2026tempo (Introduction and Methods use), vazquezguerrero2026shooting (Methods use), gong2024estimating, lange2004stability, luxburg2010clustering, fang2012selection, courelibanez2025profiling (Introduction list). For the round-1 to round-3 sources, @chen2023modeling, @kalman2020lineup and @penner2025player in `discussion.qmd:11` match the full-text note.

### C9″ (carried over). Thesis reference: author-dependent pre-submission blocker
The situation is unchanged since round 3; see §7b.

---

## 5. Major issues

- **R4-M1. The design of the trend inference.**
  1. **Within-season standardisation.** Methods (`methods.qmd:27`) and Discussion state the limitation correctly. However, role-share trends are then insensitive by construction to any uniform shift in style. Only Cramér's V, the ambiguity share and changes in covariance structure can show "dissolution". Say explicitly that these are the informative tests of aim 2, and that the no-trend result for shares was largely expected under standardisation.
  2. **Pooled GMM.** A single mixture is fitted to all seasons. If role structure changed over time, a pooled model would still force one structure. Add a check: fit 2016–2019 and 2020–2024 separately (as already done for temporal ARI) and compare role centroids and position shares.
  3. **Bootstrap.** `role_trends.py:64–70` resamples players with fixed role labels, so the GMM is not refitted. Classification uncertainty is ignored. The OLS slope over 9 season points treats season-to-season deviations as fixed, so the CIs reflect player sampling only, not inference about a temporal trend. Add a season-level inference as well: an OLS or HAC CI on the 9 season values, or a permutation of season order. Report both.
  4. **Raw-variable bootstrap B.** It is hard-coded at 200 (`role_trends.py:110`), but Methods implies 1,000. State the value or align it.
  5. **Selective reporting.** AST% (in Methods) and corner-3 share (computed, `c3_share`) are not reported. Put all 5 variables × 4 roles plus the league in a supplementary table, with CIs and a statement that they are exploratory and unadjusted.
  6. **Persistence of 84% has no benchmark.** Report the persistence expected from classification noise alone, e.g., agreement of the same player-season across bootstrap refits. Without it, 84% cannot be read as role stability rather than label stability.
  7. **Interrupted seasons.** 2020–21 is visibly atypical in Fig. 4a (ball-handler and interior-big shares). Add a sensitivity analysis without 2019–20 and 2020–21 (this also closes R3-m9).
- **R4-M2 (= R3-M2). Smallest worthwhile effect and equivalence.** See §3. The framework is fixable now; the value is author-dependent.
- **R4-M3 (= R3-M3). Confirmatory test and multiplicity.**
  - Designate the K = 4 counts gain under the corrected leakage-free specification (R4-C2, option 1) as confirmatory.
  - Give Holm-adjusted p-values for the rest of Table 4 and for the trend CIs.
  - Stop interpreting the thesis p-values (`results.qmd:73`, `discussion.qmd:11`) beyond "not robust; CIs include zero".
- **R4-M4 (= R3-M1 residual). Power.** See §3: ≥ 200 replicates, one rare pair, Limitations wording, and "excludes" → "would very likely have been detected".

---

## 6. Minor issues

- **m1. Abstract.**
  - Mention the wing/forward role as mixed (24% guards), as R3-C3 requested.
  - Use season labels "2016–17 to 2022–23" / "2023–24 and 2024–25" (R3-m7, still open; it also applies to "From 2016 to 2024").
  - "0.365" renders as "0.36" (binary-float rounding). Use three decimals or decimal rounding.
- **m2. Figures.**
  - Fig. 4 (trends; file `fig6_trends.png`) has no uncertainty bands. Add player-bootstrap bands, or at least slope CIs in the legend.
  - The file names do not match the rendered numbering (fig6 → Figure 4, fig5 → Figure 6, fig3 → Figure 5). Rename them before journal upload.
  - The Fig. 6 (leakage) caption "positive only when test-season roles are estimated from test-season data" is technically defensible, because the all-seen check uses current roles. Reword it with R4-C1 so that it cannot be read as "no positive point estimate in the checks".
- **m3. Thesis p = 1.000** is rendered as "1.000". Write "> .99" (R3-m1 residual).
- **m4. Decision rule:** "above 0.5" vs code ≥ 0.5 (R3-m5, open).
- **m5. Fig. 2 caption:** say that merged duplicates give 7 columns and supply the full 24-variable profile (R3-m6, open).
- **m6. Unseen players = league average** while the replacement level is −6.56 (R3-m8, open). This is now directly relevant to R4-C2.
- **m7.** State that the Cramér's V CI keeps role labels fixed and that the pairs-increment CI is conditional on the fitted training models (R3-m10/m11, open).
- **m8. Bibliography.**
  - `foteinakis2025decade` has a malformed author field (`author={ and Foteinakis, … and }`), which renders as "Foteinakis, Panagiotis F. and, and Stefania P. and Pavlidou".
  - `fang2012selection` and `garcia2026assist` render "&amp;Amp;".
  - `grassetti2026revisiting`, `grassetti2020extended`, `penner2025player` and `wei2025enhancing` have no DOI.
  - `kalman2020lineup` has no venue.
  - `petridis2026lineup` is not marked as a preprint.
  - There are two "Contreras García … 2026" works; check that the CSL disambiguates them (2026a/b).
  - Fix all of these via `sspe-doi`.
- **m9. Provenance:** `provenance.git_commit` is 256379c, but HEAD is 3be7fb4. Regenerate after the final render (R3-m14).
- **m10. Unused code:** `TOP` (`index.qmd:50–51`) is still computed and never printed (R3-m17).
- **m11. Structure.** Discussion P4 (`discussion.qmd:11`) is now 9 sentences mixing leakage, NBA synergy, prior work, the thesis sensitivity analysis, power and the thesis clusters. Limitations (`discussion.qmd:15`) is still one paragraph of about 11 sentences. Split both by topic (R3-m16).
- **m12. Typography:** negative numbers render with a hyphen ("-0.52"). Use U+2212.
- **m13. Methods trends:** state that the league 3PAr is the minute-weighted mean of player rates among player-seasons with at least 400 minutes, not league totals (3PA/FGA).

---

## 7. Remaining items, prioritised

### (a) Fixable now by the analyst
1. **R4-C1:** reword the leakage summary in the abstract, Results, Discussion and Conclusions; report which CIs exclude the original gain; report K = 5 split-check p = .018. *(text only)*
2. **R4-C2:** rerun checks 1–2 with the same coding in training (preferred), or make the permutation comparison primary. Hedge `discussion.qmd:11`. *(1 rerun of `lineup_model.py` per role solution)*
3. **R4-C3:** use compatibility/equivalence language for the trends; add a league-slope CI and the within-role vs composition decomposition; downgrade "specialised further"; delete "every role moved"; fix the NBA contrast. *(small additions to `role_trends.py` + text)*
4. **R4-C4:** fix the seven citation uses; re-fetch `grassetti2026revisiting` via `sspe-doi`; cite `hvattum2019comprehensive` for RAPM.
5. **R4-M1:** season-level trend inference, split-period GMM check, persistence benchmark, report B = 200 (or align it), supplementary table of all raw-variable trends, sensitivity analysis without 2019–20 and 2020–21.
6. **R4-M3:** Holm adjustment for Table 4 and the trend CIs; stop interpreting the thesis p-values. The confirmatory designation should be proposed by the analyst and signed off by the author.
7. **R4-M2 framework:** express role-count coefficients as pts/100 per role swap with game-bootstrap CIs; show them against candidate bounds (e.g., ±1 and ±2 pts/100). Plug in the final value once #47 is answered.
8. **R4-M4:** ≥ 200 power replicates and one rare pair; fix the Limitations wording; rerun or delete the stale K = 5 power block.
9. Minor items m1–m13; regenerate provenance after the final render; draft an English STROBE checklist (page numbers after final layout).

### (b) Author-dependent (do not affect the scientific verdict)
1. **Thesis reference (C9″, #37/#48):** the YÖK record (thesis number, URL, embargo status) and the decision on the manual `@phdthesis` exception to rule 1. Then cite it at every mention and declare it in the cover letter.
2. **Front matter (#38):** authors and order, affiliation, ORCID, funding, competing interests, CRediT.
3. **Smallest worthwhile effect value (#47):** coaching or literature-based bound for lineup net rating.
4. **Archive DOI (#41):** Zenodo release; add the EuroLeague API terms of use.
5. **AI statement:** confirm the model name and version and the dates of use (R3-m15).
6. **Rule 4 / full texts (#42):** whether manual verification replaces `sspe-ask`; obtain the Wei 2025 full text. New Discussion comparisons are verified at abstract level only.
7. **Ethics basis:** institutional confirmation of the exemption, if the target journal requires it.
8. **Target journal (#39):** needed for `make journal` and the final reference style.

---

## 8. Citation audit

### 8a. Keys against `references.bib`
- **Method:** extracted every `@key` from `index.qmd` and `sections/*.qmd` (excluding `@fig-`/`@tbl-`/`@sec-`), then ran `grep -cE "^@[A-Za-z]+\{key,"` on each.
- **Result:** **34 distinct keys, and each matches exactly one .bib entry.** No key is missing and there are no duplicates.
- **New since round 3 (18 keys):** courelibanez2025profiling, durmus2026from, fang2012selection, fewell2012basketball, foteinakis2025decade, garcia2026assist, garcia2026immediate, gomez2020performance, gong2024estimating, grassetti2026revisiting, lange2004stability, luxburg2010clustering, madeira2026tempo, mourer2023selecting, nietoacevedo2025modern, silva2021three, vazquezguerrero2026shooting, zajac2023long.
- **Content check:** §4, R4-C4. Seven uses go beyond their notes. One entry (`grassetti2026revisiting`) lacks a DOI.
- **Uncited source:** the thesis (8 mentions, no key) is author-dependent.

### 8b. Numbers against `results.json`
I evaluated every inline expression and compared it with the rendered docx.

- **Match:**
  - Data and stability: 2,646 games; 1,286 / 473; 24 variables; B = 500; MC SE; Table 1; 0.889 / 0.848; ARI 0.77 / 0.60; Ward-7 0.44 / 0.29 with B = 200; Brob = 100; height ARI.
  - Positions: Cramér's V 0.72 (0.69–0.75); 92 / 90 / 69 / 24 / 59 / 39%.
  - Trends: B = 1,000; slopes and CIs 0.69 (−0.52, 1.80), −0.55 (−1.27, 0.20/0.21), −0.63 (−1.77, 0.56), 0.49 (−0.17, 1.18); V 0.69–0.78, slope 0.0002 (−0.010, 0.010); ambiguity 4.4–8.0%, 0.20 (−0.18, 0.60); 1,154 pairs; persistence 84 / 87 / 70%; transitions 18% / 12% (correct mapping: role 3 = W/F, role 2 = RP); 3PAr 0.36→0.41, BH 0.45→0.47, W/F 0.45→0.50; RP rim 0.35→0.43, CI 0.0001–0.0170; RP usage 0.20→0.18; K = 5 persistence 75%.
  - Lineup: 693 players; λ 4,000; HA 4.89; R² 0.36%; 76% seen; penalty 20,000; total 0.055 (0.021–0.093), p = .014; counts 0.032 (0.014–0.051), p = .008; checks −0.048 (−0.090, 0.000), −0.024 (−0.066, 0.017), 11%, 0.011 (−0.045, 0.061); thesis 0.032, p = .002 / .014 / 1.000; pairs 0.023 (−0.002, 0.048); power 20 / 53 / 95%, FP 7%, 100 simulations, 96% presence; abstract power 53% / 95%.
  - Table 4: all values match.
  - Sensitivity analysis: unchanged from round 3.
- **Numbers with wrong qualitative wording (critical):**
  - "No positive gain" (all-seen +0.011 / +0.026).
  - "Intervals include gains of the size observed" (false for two of three checks).
  - "K = 5 behaved similarly" (p = .018 not reported).
  - These are all in R4-C1.
  - "Stable / did not erode", "every role moved with the league" (R4-C3).
- **Numbers that should be reported but are not:** the league 3PAr slope CI; the raw-variable bootstrap B (200); AST% and corner-3 trends; the minimum detectable gain for the all-seen subset.
- **Rounding:** 0.365 → "0.36" (m1).

---

## 9. Checklist

| Item | Status |
|---|---|
| Sample justification | Whole population; power simulation corrected (R4-M4 residual) |
| Clustered data | Player bootstrap (roles, V, trends), game-grouped CV and bootstrap: resolved. Trend CIs lack season-level inference (R4-M1) |
| Multiple comparisons | Disclosed as unadjusted; no Holm, no confirmatory designation; about 25 new trend CIs (R4-M3) |
| Effect size + CI | All gains and trends now have CIs: resolved. Interpretation overreaches (R4-C1, R4-C3) |
| SWC / TE | Absent (R4-M2; value author-dependent) |
| Causal language | Mostly associational; "showed that this gain depended on …" (R4-C2) |
| Limitations | Good content; still one paragraph (m11); trend-specific limitations should be expanded (R4-M1) |
| Overgeneralisation | "Stable / did not erode / differs from the NBA" (R4-C3); Courel-Ibáñez reference values (R4-C4) |
| MBI | Not used |
| p-hacking signs | History disclosed; new trend section adds many unadjusted tests and selective variable reporting (R4-M1 item 5) |
| Data / code access | URL present; DOI pending (author-dependent) |
| AI statement | Present; model and version missing (author-dependent) |

---

### Summary for the editor
- **What is done:** The round-3 blockers (power-pair description, frontcourt claim, BIC and caption mismatches) are resolved. The requested split leakage check and CIs for every gain were delivered.
- **What remains:** four new critical issues, all fixable without new data:
  1. **R4-C1:** the leakage summary is worded against its own CIs.
  2. **R4-C2:** checks 1–2 carry a training/test coding asymmetry that biases them against any gain; the mechanism claim must be hedged or the checks rerun.
  3. **R4-C3:** the new trend section reads absence of evidence as stability.
  4. **R4-C4:** seven uses of new citations go beyond their abstract-level notes.
- **Author-dependent items:** the thesis reference and the front matter are pending author input; they block submission but not this verdict.
- **Outlook:** one more round should be enough.
