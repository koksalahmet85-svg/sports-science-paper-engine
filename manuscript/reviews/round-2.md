# Review – Round 2

**Manuscript:** "Functional player roles in EuroLeague basketball: stability, positional overlap and no evidence of role synergy in lineup performance"
**Reviewer role:** Senior reviewer (Q1 sports science / sports analytics)
**Date:** 2026-11-18
**Material reviewed:** `index.qmd`, `sections/{introduction,methods,results,discussion}.qmd`, `figures/fig1–3`, `_output/index.docx` (rendered 15:18, after `results.json` 15:16, so it is current), `references.bib`, `analysis/results.json` (keys `roles_final`, `lineup_model_roles_final_K5`, `lineup_model_roles_final_K4`, `lineup_model_thesis_archetypes`, `lineup_model_K5`, `formula_test_corrected_min{0,2}_tezarketip`, `paper_a`, `ilp_validation`), `analysis/roles_final.py`, `analysis/lineup_model.py`, `checklists/STROBE.md`, `literature/answers/20261118-rol-dizilim-calismalari-dogrulama.md`, `reviews/round-1.md`.
Note: the key `paper_a_summary` that the editor asked about does **not exist** in `results.json`. The manuscript reads `paper_a` instead.

---

## 1. Decision

**Major revision.** The revision is substantial and honest in several places: a player-level bootstrap, constrained GMMs, height removed from the role definition, a tuned composition penalty, the omitted sensitivity results now reported, and a current rendered output. However, the paper's two new headline claims rest on analyses that do not yet support them. "No evidence of role synergy" relies on a power simulation that does not simulate sampling variability and does not test the synergy statistic. "Roles carry information beyond RAPM" may be an artefact of how roles and RAPM are handled in the test period. The choice of five roles also reverses under the authors' own decision rule when the larger bootstrap run is used.

## 2. Scores (1–5)

| Criterion | R1 | R2 | Comment |
|---|---|---|---|
| Originality | 3 | 4 | Related work (Konca & Erilli 2026, South 2024, Martonosi 2023) is now discussed. The stability-first approach plus the RAPM-controlled permutation test is a real contribution. |
| RQ–design fit | 3 | 4 | The RQs map onto the design. RQ3 is now split into main effects vs synergy, which is a good conceptual step. |
| Internal validity | 2 | 2 | Bootstrap unit and height circularity are fixed. New problems: possible test-period leakage and new-player confounding in the role-count gain (N3), and K selection depends on Monte-Carlo noise (N1). |
| Statistics | 2 | 2 | The power analysis is invalid as implemented (N2). Stability is reported from three different bootstrap runs. The main tests have no multiplicity control. There is no smallest worthwhile effect. |
| Reporting-guideline compliance | 2 | 3 | STROBE checklist supplied, docx current, segment N reported. Still missing: front matter (funding, COI, contributions), train/test N, persistent DOI, and a thesis citation. |
| Discussion tied to evidence | 2 | 2 | The "positionless middle" claim contradicts Table 3. The synergy null is overstated. The RAPM-by-role claim is untraced. Several mechanisms are stated causally. |
| Practical implication | 2 | 3 | Toned down, but "lineup decisions should start from individual quality" is still not tested here, and the project's own ILP validation is unreported. |

Accept is not possible: three scores are below 4 and critical issues remain open.

---

## 3. Status of round-1 critical issues

| # | Issue | Status | Comment |
|---|---|---|---|
| C1 | "Five stable roles" vs the 0.75 threshold | **Partly resolved** | The text now says "4 of 5 roles ≥ 0.75", which is honest. But three inconsistent stability runs and a K choice that reverses under the larger run remain. See **N1**. |
| C2 | Undisclosed feature-set selection | **Largely resolved** | Disclosed (`methods.qmd:19`) and Table `tbl-robust` added. Remaining: the variable set changed again between rounds (27 → 24 variables). The Discussion over-interprets Table `tbl-robust` (M4). |
| C3 | Bootstrap ignores clustering | **Resolved** | Player-level resampling (`roles_final.py:78–93`). Temporal ARI is computed only on players first seen after 2019 (N = 398). Minor: the Cramér's V CI holds the labels fixed (m8). |
| C4 | Over-parameterised, misattributed GMM | **Resolved, with one new problem** | Tied/diag covariance chosen by BIC, sklearn 1.9.1, `reg_covar` 1e-4, posterior assignment, and mclust no longer cited. But the Table 1 caption misreads the BIC (M1). |
| C5 | Height imputed from position | **Resolved** | Height is excluded from the role variables. Missingness is reported (`eksik_pay` empty in the fitting sample). Low-minute values are set to the season mean. |
| C6 | Role–position narrative vs table | **Not resolved** | The numbers are now inline, but the sentence around them contradicts them. See **C6′**. |
| C7 | Null composition result without power, penalty fixed | **Partly resolved** | The penalty is tuned by game-grouped CV within training and reported. Counts vs pairs are decomposed, with a CI for the pairs increment. The power analysis was added but is invalid (**N2**). Still missing: a smallest worthwhile effect or equivalence bound, and CIs on the coefficients. |
| C8 | K4 sensitivity used a different set and B | **Resolved** | `lineup_model_roles_final_K4`: same 24-variable set, B = 1000. |
| C9 | Selective reporting; thesis uncited | **Partly resolved** | (a), (c) and (d) resolved: min-0 permutation p = .002 and .007, BH survivors 56 vs 4, weighted vs unweighted NRTG40, metric stated. (b) is still open: the thesis is mentioned (`methods.qmd:19`, `methods.qmd:33`) but **not cited**. There is no thesis entry in `references.bib`. See **C9′**. |
| C10 | "Role-biased valuation index" | **Resolved by removal** | The VAL40/η² claims are gone from the text. A residual untraced RAPM-by-role claim remains (M2). |
| C11 | Untested practical recommendation; ILP unreported | **Partly resolved** | Softened, but still untested here, and `ilp_validation` is still unreported (M3). |
| C12 | Text/code/output inconsistencies | **Largely resolved** | 64,549 segments reported, the docx re-rendered and matches `results.json`, the abstract has numbers. Train/test N are still missing, and there is a stale JSON key (m2). |
| C13 | Literature claims not verified | **Not resolved** | See **C13′**. |

---

## 4. Remaining and new critical issues (block publication)

### N1. K = 5 depends on which bootstrap run is used, and three different stability values are reported for the same solution
- **Location:** `methods.qmd:19` (decision rule; B = 100 scan, B = 200 final); `results.qmd:5`, `results.qmd:9–13` (Table 1); `results.qmd:22–28` (Table 3); `results.qmd:33` and `results.qmd:39–48` (Table 2); `index.qmd:51`; code `roles_final.py:139–144`, `:163`, `:185`.
- **Problem:**
  - The rule is: highest mean Jaccard among K with minimum Jaccard ≥ 0.5, with ties within 0.02 broken by temporal ARI. It was applied to the **B = 100 scan**: tied K4 0.877 vs K5 0.861, a difference of 0.016, so K5 wins on ARI (0.77 vs 0.60).
  - In the **B = 200 final run** (`roles_final.nihai`), K4 = 0.894 and K5 = 0.844, a difference of 0.050. Under the same rule this selects **K = 4**.
  - In the robustness run (`duyarlilik`, **B = 50**, not reported in Methods), K4 = 0.897 vs K5 = 0.849. This also selects K = 4.
  - The same five-role solution therefore appears as mean/min Jaccard 0.86/0.75 (Table 1), 0.84/0.71 (Table 2, abstract) and 0.85/0.72 (Table 3). Table 1 implies all five roles reach 0.75, but the text says four of five do.
  - The code comment at `roles_final.py:146` ("same scan run's Jaccard values") is false: line 163 runs a fresh bootstrap.
  - The 0.02 margin sits just above the observed 0.016. The claim that the rule was "fixed before the final solution was examined" cannot be verified: there is no preregistration and no timestamped protocol.
- **Fix:** (a) Run one bootstrap with B ≥ 500 for all K, both covariance structures and the final solution. Report Monte-Carlo SEs or percentile CIs for mean and minimum Jaccard, and draw every table and figure from that run. (b) Apply the rule to those values and report the outcome, even if it is K = 4. Alternatively, present K = 4 and K = 5 as equally supported, with K = 5 as a finer description. (c) Disclose that the rule was set after round-1 review, not preregistered. Give the date and commit hash, and drop "fixed before the final solution was examined" unless a timestamped record exists. (d) Report B = 50 for Table 3, or rerun it with the common B.

### N2. The power analysis does not estimate power and does not test synergy
- **Location:** `methods.qmd:29` (last sentence); `results.qmd:61`; `discussion.qmd:9` ("even small synergies for common pairings would have been detected"); `discussion.qmd:13`; code `lineup_model.py:218–238`.
- **Problem:**
  - (a) **No sampling variability.** Each "simulation" adds the same deterministic term (`tr["y"] + delta * inj_tr`) to the same data. The 10 replicates differ only in the permutation draws (B = 100). "80% power at 0.25" therefore means that 8 of 10 permutation p-values for one and the same dataset fell below .05. That is Monte-Carlo noise around a single p-value, not power.
  - (b) **Wrong statistic.** The test inside the simulation is the **total** composition gain (counts + pairs). The paper's conclusion about synergy rests on the **pairs increment** (CI −0.022 to 0.048 pp). The total-gain test is already significant **without any injection** (observed p = .038), so detection at δ > 0 is close to guaranteed and says nothing about the ability to detect pairwise synergy. There is also no δ = 0 control.
  - (c) Only one pair (stretch forward × wing) was injected, in the exact functional form the model estimates. This is the most favourable case, yet the Discussion generalises to "common pairings".
  - (d) Ten replicates give a 95% CI of roughly 0.44–0.97 around 0.80.
- **Equivalence:** The pairs-increment CI upper bound (0.048 pp) **exceeds the entire role-count gain** (0.036 pp) and equals the total gain (0.049 pp). The data therefore cannot rule out pairwise synergy as large as the main effect the paper does accept as real. The fitted pair coefficients are among the largest in the model (n3×n4 = +1.58, n1×n5 = +1.32, n2×n3 = +1.23 pts/100 poss; `rol_bilesimi.en_buyuk_katsayilar`) and come with no uncertainty.
- **Fix:**
  - Simulate properly: resample games (or residuals) per replicate, inject δ, refit everything, and test the **pairs increment** with its own permutation null (permute labels, refit counts-only and full, and take the difference).
  - Use ≥ 200 replicates and ≥ 200 permutations, include δ = 0 to check type-I error, and inject at least the 3 most frequent pairs plus one rare pair.
  - Translate δ into the R² scale so readers can compare it with the CI bound.
  - Define a smallest worthwhile effect for lineup net rating (e.g., 1 pt/100 poss per co-occurrence) and state an equivalence conclusion only if the CI excludes it.
  - Until then, change the title and abstract to "no detectable pairwise synergy; synergies as large as the role-count effect could not be excluded".

### N3. The out-of-time role-count gain may reflect test-period information and players unseen in training, not role value
- **Location:** `methods.qmd:27–29`; `results.qmd:57`; `discussion.qmd:9` (shrinkage interpretation); `index.qmd:53`; code `lineup_model.py:52–62`, `:111–112`, `:129`, `:156–176`.
- **Problem:**
  - (a) **Leakage.** Role labels for the 2023–24 and 2024–25 test segments come from those **same seasons'** box-score, shot and assist data, and the GMM itself is fitted on all seasons. Several role variables (usage, AST%, FTr, shot location) correlate with the minutes and quality a player shows in that season. The test-period predictor therefore contains test-period information that the RAPM baseline does not have.
  - (b) **Unseen players.** 24.3% of test player-appearances are players unseen in training (`testte_egitimde_gorulen_oyuncu_payi = 0.757`). They are set to RAPM = 0 (league average), while their role labels are known. Role counts can then act as a crude prior for new players: a structural advantage for the composition model that has nothing to do with "roles worth more than RAPM credits".
  - (c) **Interpretation built in.** The composition model is trained on in-sample RAPM residuals (`resid = y − p_rapm_tr`). In training, player coefficients absorb any stable role effect, so what remains is exactly the shrinkage residual. The interpretation in `discussion.qmd:9` is therefore partly built in by the design rather than shown.
  - (d) **Selection outside the null.** The composition penalty is selected with the observed labels, and selection is not repeated inside the permutation loop, so the null is slightly anti-conservative.
  - (e) **Not robust across definitions.** The earlier five-role solution gives no gain (p = .41, Table `tbl-comp`), whereas the unstable Ward-7 solution gives p = .014. The signal is not specific to stable roles. This fits the idea that any label correlated with playing profile or minutes helps for new players.
- **Fix:**
  1. Repeat the test (i) on test segments in which all ten players had a training RAPM, and (ii) using role labels from each player's most recent **training** season, or from a GMM fitted on training seasons only, with new players given a missing-role indicator.
  2. Add a non-role baseline for new players (e.g., prior-season minutes, or a replacement level instead of 0) and test roles beyond it.
  3. Re-select the penalty inside each permutation.
  4. Report the composition gain with a game-bootstrap CI (the abstract gives only p).
  5. If the gain disappears under (1), the abstract, Discussion P4 and Conclusions must be rewritten.

### C6′. The "positionless middle" narrative still contradicts Table 2
- **Location:** `index.qmd:52` (abstract); `results.qmd:53`; `discussion.qmd:3`, `discussion.qmd:7`; `discussion.qmd:17`; `introduction.qmd:7`.
- **Problem:** From `roles_final.nihai.K5.pozisyon`:
  - Stretch forward: **76% forwards**, 15% guards, 9% centres.
  - Wing: **78% guards**, 21% forwards.
  - Interior big: 62% centres, 37% forwards.

  The dominant-position shares (`baskin_pozisyon_payi`) form a gradient: 0.96 / 0.90 / 0.78 / 0.76 / 0.62. Rim protector (0.90) and wing (0.78) differ only modestly, so there is no "extremes vs middle" break. Only the interior big genuinely draws on two positions. "Each drew substantially on two positions" (Results) and "each combined two registered positions" (Discussion) are false for two of the three roles. The same holds for the abstract's "drew on two positions".
- **Fix:** Rewrite as: "Dominant-position shares ranged from 96% (ball handler) to 62% (interior big). Only the interior-big role drew substantially on two positions (centres and forwards)." Remove "positionless play is a property of the middle of the positional spectrum" or support it with a test, e.g., a per-role entropy with player-bootstrap CIs. Also reconsider the label "wing" for a 194-cm role that is 78% guards ("off-ball guard"?).

### C9′. The author's doctoral thesis is used but not cited
- **Location:** `methods.qmd:19`, `methods.qmd:33`; `results.qmd:5`, `results.qmd:68–69`, `results.qmd:80`; `discussion.qmd:5`; `index.qmd:51`.
- **Problem:** The thesis's seven-cluster solution and its role-combination procedure are reproduced and criticised. It is referred to only as "the author's doctoral thesis". `references.bib` has no thesis entry (no `@phdthesis`, no "thesis" match). This violates CLAUDE.md rule 1 and is a duplicate-publication disclosure issue for the editor.
- **Fix:** Add a `@phdthesis` entry from the institutional repository record via `sspe-doi` or the repository metadata (not from memory), cite it at every mention, and declare the overlap in the cover letter.

### C13′. Literature claims still go beyond the verified sources
- **Location:** `discussion.qmd:5` ("studies using play-type data distinguish ball handlers, spot-up wings and several types of bigs [@chen2023modeling; @wei2025enhancing]"; "more than a dozen with play-type data [@chen2023modeling; @wei2025enhancing]"); `introduction.qmd:3`.
- **Problem:** The project's own verification file (`literature/answers/20261118-…dogrulama.md`, line 11) states that only the abstract of @wei2025enhancing was available and that the role details "should not be claimed in the text". For @chen2023modeling the file verifies only the role→success design, **not** the role count or role types. The verification was done by hand, not with `sspe-ask` as CLAUDE.md rule 4 requires.
- **Fix:** Verify the role counts and labels for both papers from the full text and record them in `literature/answers/`. Otherwise remove both citations from these two clauses. Use, for example, @ibanez2025redefining (verified as 9 roles) and @ribes2026identifying for the range.

---

## 5. Major issues

- **M1. The Table 1 caption misreads BIC** (`results.qmd:9`). The caption says "Stability and fit decline beyond five roles". Within the retained tied structure, BIC is **lower** (better) at K = 6 (61,232) and K = 8 (61,257) than at K = 5 (61,321). Silhouette is also higher at K = 4 (0.14) than at K = 5 (0.08). **Fix:** Say that BIC favours more components while stability favours four or five, and justify putting stability ahead of BIC.

- **M2. An untraced and partly incorrect RAPM-by-role claim** (`discussion.qmd:9`: "rim protectors and ball handlers had the highest RAPM"). This is not reported in Results or pulled from `results.json` (rule 2). In `rol_ortalamalari`, ball handler = 0.24, rim protector = 0.05, **stretch forward = 0.05** (tie), wing = −0.09 and interior big = −0.18. η² for RAPM by role = 0.007, with no CI. **Fix:** Report the role means with player-bootstrap CIs in Results, or delete the clause.

- **M3. The practical recommendation is untested and the ILP results are still unreported** (`discussion.qmd:17`).
  - "Lineup decisions should start from the individual quality of the players available" is not tested in this paper.
  - `ilp_validation` shows that a RAPM-optimised lineup does not beat the coach's choice (`ilp_antrenore_gore_fark.RAPM_yok` = −1.66 [−5.33, 2.03]).
  - It also shows that the RAPM objective slope is positive (1.76 [0.90, 2.64]).
  - **Fix:** Report this in a supplementary table and phrase the application as supported: "RAPM-type ratings predict lineup outcomes, but selecting lineups by RAPM alone did not outperform coaches". Otherwise limit the conclusion to scouting and description.

- **M4. Causal and over-interpreted mechanism statements.**
  - `discussion.qmd:5`: "assist relationships are what make a five-role partition stable". The comparison confounds the variable group with the number of variables (17 vs 24), and the possession shares + shot profile set already reaches mean Jaccard 0.755.
  - `discussion.qmd:9`: "because lineups that concede runs are substituted quickly". The weighted vs unweighted means (0.56 vs −10.08) are consistent with this but do not show it.
  - `discussion.qmd:9`: the shrinkage explanation, which is partly built in by design (N3c).
  - **Fix:** Use "consistent with" or "may", and name the alternatives: number of variables, leakage, new players.

- **M5. Forking paths and multiplicity in the lineup tests.**
  - Between rounds the primary lineup result flipped from null (R1: p = .51; the earlier five-role solution re-run with the tuned penalty: p = .41) to positive (p = .038). Along the way the variable set, covariance, K rule and penalty grid all changed.
  - Four role solutions and at least three tests (total, counts, four-role) are reported with no multiplicity control, and the headline p = .038 is close to .05. The authors do show the earlier and thesis solutions in Table `tbl-comp`, which is commendable.
  - **Fix:** Name one confirmatory test in advance, label the others exploratory, give a Holm-adjusted p or at least discuss the multiplicity, and add a sentence in the Limitations on the analytic history.

- **M6. No smallest worthwhile effect or practical-relevance anchor.**
  - Results are given as R² gains in hundredths of a percentage point, which readers cannot interpret.
  - "About a quarter as large as differences in player quality" (`index.qmd:53`) compares prediction SDs (1.69 vs 7.03 pts/100). That is the spread of model predictions, not "differences in player quality".
  - **Fix:** Define a smallest worthwhile effect for net rating (e.g., 1 or 2 pts/100). Express role-count effects as expected pts/100 per role swap with CIs, and rephrase the abstract sentence.

---

## 6. Minor issues

- **m1. Train/test N and unseen players.** Train/test segment N (48,309 / 16,240), the unseen-player share (24.3%) and the replacement coefficient (−6.56, against an RAPM SD of 1.5) are still not reported. Justify setting unseen players to 0 rather than to replacement level (round-1 minor 4).
- **m2. Inconsistent segment counts.** `results.json` holds three counts for the "model" segments: `paper_a.stints_model` = 64,125, `lineup_model_*.segment_N` = 64,549 and `ilp_validation.segment_N` = 64,324. Remove or regenerate the stale key and give a flow diagram (80,460 → 64,549 → 48,309 / 16,240).
- **m3. Ambiguous period labels.** "2016–2022", "2023–2024" and "2016–2019 / 2020–2024" (`methods.qmd:19`, `methods.qmd:29`; `results.qmd:57`) are ambiguous. The code uses start-year codes (≤ 2022 means 2016–17 to 2022–23). Use season labels throughout.
- **m4. Permutation counts.** The role-counts permutation p uses 500 permutations (`min(a.B, 500)`, `lineup_model.py:191`), not the 1,000 stated. The pairs-increment CI is a test-game bootstrap conditional on the fitted models, so it ignores training uncertainty. State both.
- **m5. Decision-rule wording.** The rule says "above 0.5" but the code uses ≥ 0.5.
- **m6. Figure 2 caption.** It says "the two highest-loading variables of each role", but the figure shows 7 variables (duplicates merged). Say so, and give the full 24-variable profile in a supplement.
- **m7. Interrupted seasons.** The interrupted seasons (2019–20, and 2020–21 without spectators) are now mentioned, but there is no sensitivity analysis (round-1 minor 5). At least report the lineup test without 2020–21, or explain why the test period is unaffected.
- **m8. Cramér's V CI.** The CI resamples players with the role labels held fixed (`roles_final.py:157–162`), so it ignores clustering uncertainty. State this.
- **m9. Wrong source for a claim.** `introduction.qmd:5` attributes "role effects need to be evaluated after player quality" to @petridis2026lineup. That paper proposes informed priors for lineup RAPM and does not make this argument. Use it only for the method. The original RAPM/APM methods source is still missing (round-1 minor 3). Add it via `sspe-search`/`sspe-doi`.
- **m10. Bibliography metadata.** Still incomplete. `kalman2020lineup` has no venue or URL and its peer-review status is unclear. `grassetti2020extended` has no DOI, volume or pages. `wei2025enhancing`, `penner2025player` and `petridis2026lineup` have no DOI.
- **m11. Front matter.** Affiliation, funding, competing interests and author contributions are still missing. STROBE item 22 is open. The STROBE checklist is in Turkish; provide an English version with page or line numbers for submission.
- **m12. Data and code availability.** A GitHub URL is given, but the DOI is deferred "on acceptance". Most Q1 journals require it at submission for review. Also give the EuroLeague API terms of use and the retrieval date.
- **m13. AI statement.** Give the model and version (round-1 minor 16).
- **m14. Structure (Drake & Han).**
  - Discussion P4 (`discussion.qmd:9`) is still a single 9-sentence paragraph mixing the null, the mechanism, the critique of prior work, the sensitivity analysis and the implication. Split it into (i) main effects vs synergy, (ii) prior work, (iii) observation artefacts.
  - The Limitations are still one paragraph; split by problem.
  - The Introduction's "Here we show … reproducibly" and the abstract's "recovered reproducibly" should follow whatever N1 shows.
- **m15. Unused code.** `TOP` in `index.qmd:39–40` is computed but never used. Either report the largest composition coefficients with CIs (see N2) or remove the variable.
- **m16. Abstract.** The abstract gives p but no effect size with CI for the main lineup result. Add the gain in pp with its CI, or the effect in pts/100.

---

## 7. Citation audit

### 7a. Keys against `references.bib`
Method: extracted every `@key` from `index.qmd` and `sections/*.qmd` (excluding `@fig-`/`@tbl-`) and checked each with `grep -E "^@[A-Za-z]+\{key,"`.

| Key | Uses | In .bib | Content check |
|---|---|---|---|
| chen2023modeling | 5 | yes | Role count and role types **not verified** (C13′) |
| duman2021cluster | 1 | yes | |
| grassetti2020extended | 2 | yes | Verified (2018/19 EuroLeague RAPM, abstract). Metadata incomplete |
| hennig2007cluster | 2 | yes | Thresholds verified |
| ibanez2025redefining | 2 | yes | 9 roles verified (abstract) |
| kalman2020lineup | 4 | yes | Verified (full text). No venue |
| konca2026from | 2 | yes | Verified (abstract): convergence of EuroLeague bigs |
| kubatko2007starting | 1 | yes | |
| martonosi2023predicting | 2 | yes | Verified (abstract) |
| pendolareinecke2025exploring | 2 | yes | 3 roles verified (abstract) |
| penner2025player | 3 | yes | Verified (full text). No DOI |
| petridis2026lineup | 3 | yes | arXiv preprint. Introduction use goes beyond what it says (m9) |
| ribes2026identifying | 3 | yes | Verified (abstract) |
| sampaio2006discriminant | 1 | yes | |
| south2024basketball | 2 | yes | Verified (abstract) |
| wei2025enhancing | 3 | yes | **Abstract only; the verification file says not to claim role details** (C13′) |
| *(thesis)* | 6 mentions, no key | **no** | **Uncited source** (C9′) |

All 16 keys resolve. There are no missing keys, but there is one uncited source (the thesis) and two content-level problems.

### 7b. Numbers against `results.json`
I evaluated every inline expression against the JSON and checked them against the rendered docx.

- **Match:**
  - Data: 9 seasons; 2,646 games; 252–331 games per season; 62,912 player-games; 325,151 shots; 83,164 assisted field goals; 2,014 player-seasons; 736 players; 1,286 player-seasons from 473 players; 24 variables; 99.4% of time; 80,460 / 64,549 segments.
  - Stability: tied covariance; Bscan 100, B 200; Table 1 values; Ward-7 0.44 / 0.29; K5 0.84; 4 of 5 roles ≥ 0.75; wing 0.71; p_max < 0.7 = 7.4%; height ARI 0.89 (0.885).
  - Positions: Cramér's V 0.73 [0.70, 0.76]; 96% / 90% / 78% / 21% / 76% / 15% / 62% / 37%.
  - RAPM and composition: 693 players; λ 4,000; home advantage 4.89; RAPM R² 0.36%; composition penalty 20,000; gain 0.049 pp; null mean 0.012; p = .038; K4 p = .013; prediction SD 1.69 vs 7.03; counts 0.036 pp (p = .008); pairs 0.013 pp (−0.022 to 0.048); power 80/100/100% (stretch forward × wing).
  - Table `tbl-comp`: .038 / .013 / .411 / .014.
  - Sensitivity analysis: χ²(6) 42.31, naive p < .001, permutation p = .002; 92 selected vs 80.3 expected, p = .007; 56 after BH; 90 of 92 negative; −10.08 vs 0.56; 28 vs 26.3, p = .367; 4 after BH; χ² 8.85, permutation p = .232.
- **Same quantity, different values (critical, N1):** K5 mean/min Jaccard 0.861/0.750 (Table 1, B = 100), 0.844/0.707 (Table 2 and abstract, B = 200), 0.849/0.715 (Table 3, B = 50). K4 0.877 / 0.894 / 0.897.
- **Untraced number-like claim (M2):** "rim protectors and ball handlers had the highest RAPM" does not match `rol_ortalamalari` (rim protector ties with stretch forward at 0.05).
- **Text contradicts the numbers it prints (C6′):** "each drew substantially on two positions" sits next to 76% / 15% and 78% / 21%.
- **Stale or conflicting JSON keys (m2):** `paper_a.stints_model` 64,125 vs `segment_N` 64,549. The requested `paper_a_summary` key does not exist.
- **Still unreported but relevant (M3):** `ilp_validation`.

---

## 8. Checklist

| Item | Status |
|---|---|
| Sample justification | Whole population (all games); acceptable. The power analysis is invalid (N2) |
| Clustered data | Player-level bootstrap and game-grouped CV and bootstrap: resolved |
| Multiple comparisons | BH in the sensitivity analysis: yes. Main lineup tests: no (M5) |
| Effect size + CI | V with CI, pairs increment with CI. Total and counts gains have no CI; role coefficients have no CI (N3, M6) |
| SWC / TE | Absent (M6) |
| Causal language | Mostly associational; mechanism sentences are causal (M4) |
| Limitations | Present, but they rely on the invalid power claim (N2) |
| Overgeneralisation | "Positionless middle" (C6′), "common pairings" (N2) |
| MBI | Not used |
| p-hacking signs | Result flipped between rounds after several analytic changes; 0.02 tie margin just above the observed 0.016 (N1, M5) |
| Data / code access | URL given; DOI deferred (m12) |
| AI statement | Present; model version missing (m13) |

---

### Summary for the editor
The authors fixed most of the round-1 mechanics (clustered bootstrap, GMM specification, circular height, fixed penalty, selective reporting, stale output), and the paper is clearly better. The new central claims are not yet secure:
1. With a larger bootstrap, the authors' own K rule selects four roles, not five.
2. The power simulation behind "no evidence of synergy" contains no sampling variability and tests the wrong statistic. The pairs-increment CI cannot exclude synergy as large as the accepted role-count effect.
3. The positive role-count result may come from test-season role labels and the 24% of test appearances by players unseen in training.

In addition, the role–position narrative still contradicts its own table, the doctoral thesis must be cited and disclosed, and the unverified literature claims must be fixed.
