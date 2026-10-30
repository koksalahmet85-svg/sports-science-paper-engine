# I am preparing a Q1 journal article from a doctoral thesis in basketball analyti

**Question:** I am preparing a Q1 journal article from a doctoral thesis in basketball analytics. Thesis summary: an AI-based decision-support framework from player performance measurement to lineup optimization, tested on EuroLeague data 2016–2024 (2,014 player-season observations, 67,001 five-man lineup segments). Pipeline: VAL40 (EuroLeague Valuation/PIR normalized per 40 minutes) modeled with a Gradient Boosting Regressor; Ward hierarchical clustering yields 7 functional player archetypes (positionless roles); optimal five-man lineups selected with integer linear programming; framework completed with Bayesian updating. Main finding: archetype distribution in successful lineups is non-random; documents EuroLeague's positionless structure.

Please do all of the following and return one structured report:

1. NOVELTY / CLOSEST WORK: Find the peer-reviewed papers closest to this framework: (a) clustering basketball players into roles/archetypes beyond traditional positions (NBA, EuroLeague, FIBA, other leagues); (b) relating lineup archetype composition to lineup performance; (c) mathematical programming / integer programming / optimization for basketball lineup or roster selection; (d) Bayesian or regularized lineup/player ratings (RAPM, adjusted plus-minus with priors). For each, state data, method, main finding, and how my framework differs. Explicitly note any prior work on EuroLeague specifically.

2. EVALUATE PIR/VALUATION as a player-value metric: evidence on validity and known limitations of box-score linear metrics (PIR, PER, Win Score) versus plus-minus based metrics, and evidence on per-minute normalization noise for low-minute players and shrinkage/empirical Bayes remedies.

3. METHODOLOGICAL REMEDIES for likely reviewer objections, citing methodological papers (sports or general statistics):
   - circularity/target leakage when predicting a composite metric from its own components;
   - small-sample noise in lineup segments (minimum possessions, possession weighting, regularization);
   - testing non-randomness of lineup composition when segments are non-independent (permutation tests respecting team/season structure, mixed-effects models);
   - optimizer's curse / winner's curse when optimizing over noisy estimates, and out-of-sample validation of optimized lineups;
   - cluster validation and stability (number of clusters, bootstrap stability) for Ward clustering.

4. Suggest which journals have recently published comparable basketball lineup/archetype/optimization work.

For every claim give the paper (authors, year, journal, DOI if available). Prefer peer-reviewed work; mark preprints as preprints.

# Synthesis of **Positionless Lineup Analytics** and Decision Support in Basketball

Synthesizing multi-season tracking, play-by-play, and box-score data establishes the viability of data-driven player archetypes, lineup synergy quantification, and mathematical optimization for team construction [[1.1]](https://consensus.app/papers/player-archetypes-within-basketball-optimizing-roster-penner/14b3c3ca913e57e9aef5faecc48f71e3/) [[2.1]](https://consensus.app/papers/nba-lineup-analysis-on-clustered-player-tendencies-a-new-kalman-bosch/bba122fca0a5594bb106dd188d2862b0/) [[3.1]](https://consensus.app/papers/sports-analytics-for-balanced-teambuilding-decisions-muniz-flamand/e56acea13a235728affa181d1b9059cc/). The literature demonstrates that traditional categorical positions fail to represent modern tactical specializations and frontcourt convergence [[4.1]](https://consensus.app/papers/from-position-to-role-konca-erilli/b58a1415d84155feab9d95b47704d683/) [[5.1]](https://consensus.app/papers/redefining-player-roles-in-professional-women’s-ibáñez-courel-ibáñez/45f2c382350f5f0dbfe85cb3c2414ceb/).

## Closest Work Across Analytics Dimensions

Research in player clustering, lineup composition, and mathematical programming provides strong points of comparison for end-to-end decision-support frameworks.

| Dimension / Paper | Data & Context | Methodology | Key Findings | Differentiation from Your Framework |
| :--- | :--- | :--- | :--- | :--- |
| **Global Role Clustering** <br>Penner (2025) [[1.2]](https://consensus.app/papers/player-archetypes-within-basketball-optimizing-roster-penner/14b3c3ca913e57e9aef5faecc48f71e3/) [[1.3]](https://consensus.app/papers/player-archetypes-within-basketball-optimizing-roster-penner/14b3c3ca913e57e9aef5faecc48f71e3/) | 22,500 athletes across 110 professional and college leagues | Per-48 box metrics, $k$-means clustering, tier adjustments | Identified **9 player archetypes** and derived optimal roster proportions [[1.3]](https://consensus.app/papers/player-archetypes-within-basketball-optimizing-roster-penner/14b3c3ca913e57e9aef5faecc48f71e3/) [[1.4]](https://consensus.app/papers/player-archetypes-within-basketball-optimizing-roster-penner/14b3c3ca913e57e9aef5faecc48f71e3/). | Relies on linear regression on points per minute rather than machine learning on normalized efficiency [[1.5]](https://consensus.app/papers/player-archetypes-within-basketball-optimizing-roster-penner/14b3c3ca913e57e9aef5faecc48f71e3/). |
| **Lineup Efficiency Modeling** <br>Kalman & Bosch (preprint) [[2.1]](https://consensus.app/papers/nba-lineup-analysis-on-clustered-player-tendencies-a-new-kalman-bosch/bba122fca0a5594bb106dd188d2862b0/) [[2.2]](https://consensus.app/papers/nba-lineup-analysis-on-clustered-player-tendencies-a-new-kalman-bosch/bba122fca0a5594bb106dd188d2862b0/) | 10 NBA seasons (2009–2018) | Gaussian mixture models, soft cluster assignment | Modeled net rating as a function of **soft archetype combinations** [[2.2]](https://consensus.app/papers/nba-lineup-analysis-on-clustered-player-tendencies-a-new-kalman-bosch/bba122fca0a5594bb106dd188d2862b0/) [[2.3]](https://consensus.app/papers/nba-lineup-analysis-on-clustered-player-tendencies-a-new-kalman-bosch/bba122fca0a5594bb106dd188d2862b0/). | Focuses strictly on NBA rotations without integer programming optimization or Bayesian rating updates [[2.1]](https://consensus.app/papers/nba-lineup-analysis-on-clustered-player-tendencies-a-new-kalman-bosch/bba122fca0a5594bb106dd188d2862b0/). |
| **EuroLeague Lineup RAPM** <br>Grassetti et al. (2020) [[6.1]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) [[6.2]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) | 2018/19 EuroLeague (240 games, play-by-play) | Bayesian regularized adjusted plus-minus on multi-component scores | Separated lineup skill contributions and tracked **in-season Bayesian updates** [[6.3]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) [[6.4]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) [[6.5]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/). | Directly analyzes EuroLeague lineups via RAPM, but lacks functional clustering or prescriptive optimization [[6.6]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/). |
| **Roster Optimization** <br>Muniz & Flamand (2022) [[3.2]](https://consensus.app/papers/sports-analytics-for-balanced-teambuilding-decisions-muniz-flamand/e56acea13a235728affa181d1b9059cc/) [[3.3]](https://consensus.app/papers/sports-analytics-for-balanced-teambuilding-decisions-muniz-flamand/e56acea13a235728affa181d1b9059cc/) | NBA 2019–2020 tracking and box data | Network clustering, Mixed-Integer Nonlinear Programming (MINLP) | Maximized team win potential via **archetype pairwise synergy metrics** [[3.4]](https://consensus.app/papers/sports-analytics-for-balanced-teambuilding-decisions-muniz-flamand/e56acea13a235728affa181d1b9059cc/) [[3.1]](https://consensus.app/papers/sports-analytics-for-balanced-teambuilding-decisions-muniz-flamand/e56acea13a235728affa181d1b9059cc/). | Operates at the whole-roster transaction level rather than five-man tactical substitution segment optimization [[3.5]](https://consensus.app/papers/sports-analytics-for-balanced-teambuilding-decisions-muniz-flamand/e56acea13a235728affa181d1b9059cc/). |
| **Lineup Regularization** <br>Petridis & Pelechrinis (2026, preprint) [[7.1]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/) [[7.2]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/) | Multi-season NBA lineup possessions | Ridge-regularized L-RAPM with informative individual priors | Priors mitigate variance in **low-possession sparse lineups** [[7.3]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/) [[7.4]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/) [[7]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/). | Targets possession-level regression without linking lineup ratings to functional archetype topologies [[7.5]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/). |

**Figure 3.** L-RAPM &#x27;s improvements over the baseline are larger when we have observed fewer data for the lineups making predictions for. The prior incorporated in our method allows L-RAPM to obtain lineup ratings with good predictive power with fewer data. [[7]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/)

*How to read: The plot contrasts predictive performance against observed possession sample sizes: the horizontal axis represents possession sample size bins and the vertical axis indicates prediction error. Curves demonstrate error reduction gains from informed Bayesian priors.*

## Evaluation of Performance Index Rating

European basketball research frequently analyzes the EuroLeague Valuation or Performance Index Rating (PIR) to assess overall player value alongside modern adjusted metrics [[6.2]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) [[6.7]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/). While composite ratings combine volume box-score statistics into a straightforward summary of individual productivity, they exhibit clear structural limitations [[6.8]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) [[8.1]](https://consensus.app/papers/modeling-the-influence-of-basketball-players’-offense-chen-zhang/c31c0efb1a2d5ac99d39a0f30ac3344e/):

* Linear composite metrics aggregate positive and negative counting events without accounting for **lineup teammate synergies** or quality of opposing personnel [[6.6]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) [[7.2]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/) [[9.1]](https://consensus.app/papers/measuring-players’-importance-in-basketball-using-the-metulini-gnecco/e32f7a9470df5f44ba510a9748257e86/).
* Unadjusted box indices disproportionately reward ball-dominant usage and traditional box contributions while failing to measure **off-ball defensive impact** [[10.1]](https://consensus.app/papers/offensive-lineup-analysis-in-basketball-with-clustering-yamada-fujii/57c85a1d01c450838461e31e839890ed/) [[11.1]](https://consensus.app/papers/enhancing-team-dynamics-unveiling-synergy-effects-wei-li/d147d6019b415345a0af7f03a674ad37/) [[12.1]](https://consensus.app/papers/predicting-elite-nba-lineups-using-individual-player-martonosi-gonzález/72568186715e541b85728f3852b9bda1/).
* Normalizing statistics on a per-minute or per-40 basis induces severe variance in small sample sizes, where extreme outliers emerge among players with **limited court exposure** [[7.6]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/) [[7.7]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/) [[5.2]](https://consensus.app/papers/redefining-player-roles-in-professional-women’s-ibáñez-courel-ibáñez/45f2c382350f5f0dbfe85cb3c2414ceb/).
* Regularization schemes and hierarchical empirical Bayes shrinkage mitigate extreme noise by pulling estimates toward informative archetype priors [[6.3]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) [[13.1]](https://consensus.app/papers/a-basketball-paradox-exploring-nba-team-defensive-south/320edd4969955098a450e995896edb5c/) [[7.8]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/).

## Methodological Remedies for Reviewer Objections

Anticipating methodological critique requires addressing target leakage, segment sparsity, statistical dependencies, optimization bias, and cluster stability.

First, predicting a composite index from identical constituent box-score statistics risks target leakage; using Gradient Boosting Regressors requires separating predictor inputs into independent efficiency, opportunity, and tracking metrics rather than simple arithmetic identities [[2.1]](https://consensus.app/papers/nba-lineup-analysis-on-clustered-player-tendencies-a-new-kalman-bosch/bba122fca0a5594bb106dd188d2862b0/) [[10.2]](https://consensus.app/papers/offensive-lineup-analysis-in-basketball-with-clustering-yamada-fujii/57c85a1d01c450838461e31e839890ed/). Second, five-man lineup segments are right-skewed, with the vast majority appearing for fewer than 50 possessions [[7.7]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/) [[7.9]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/) [[7]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/). Mitigate extreme variance by imposing strict minute thresholds, possession weighting, and Bayesian regularization distributions [[6.3]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) [[7.4]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/) [[12.2]](https://consensus.app/papers/predicting-elite-nba-lineups-using-individual-player-martonosi-gonzález/72568186715e541b85728f3852b9bda1/). 

**Figure 1.** The majority of the lineups during a season appear on the court for a small number of possessions. The distribution (in log-log scale) for the number of offensive (left) and defensive (right) possessions per lineup is right skewed, with a small number of lineups playing for thousands of possessions, while the vast majority of them plays for less than 50 possessions. [[7]](https://consensus.app/papers/lineup-regularized-adjusted-plusminus-lrapm-basketball-petridis-pelechrinis/116d8015c1565771b28b5c3db30a2ee4/)

*How to read: The two panels present log-log distributions of offensive and defensive possessions per lineup segment. The horizontal axis represents the possession count and the vertical axis displays frequency, illustrating that sparse, low-possession segments dominate.*

Third, non-randomness in lineup success cannot be evaluated under naive independence assumptions because lineup segments share players across teams and seasons; linear mixed-effects models with random team/season intercepts and block permutation tests preserve hierarchical grouping structures [[13.2]](https://consensus.app/papers/a-basketball-paradox-exploring-nba-team-defensive-south/320edd4969955098a450e995896edb5c/) [[4.2]](https://consensus.app/papers/from-position-to-role-konca-erilli/b58a1415d84155feab9d95b47704d683/) [[4.3]](https://consensus.app/papers/from-position-to-role-konca-erilli/b58a1415d84155feab9d95b47704d683/). Fourth, integer programming over noisy point estimates introduces the optimizer's curse, systematically selecting lineups with upward-biased estimation error; evaluating lineups using out-of-sample holdout seasons or conservative risk bounds protects against over-optimistic projections [[14.1]](https://consensus.app/papers/bioinformaticsinspired-robust-smithwatermanguided-biró-kovács/02fe14d33f2351428b7ad0c0e25eb1fc/) [[14.2]](https://consensus.app/papers/bioinformaticsinspired-robust-smithwatermanguided-biró-kovács/02fe14d33f2351428b7ad0c0e25eb1fc/) [[12.3]](https://consensus.app/papers/predicting-elite-nba-lineups-using-individual-player-martonosi-gonzález/72568186715e541b85728f3852b9bda1/). Finally, for Ward hierarchical clustering, cluster numbers and stability should be validated via silhouette coefficients, dendrogram distance thresholds, and bootstrap resampling algorithms [[15.1]](https://consensus.app/papers/quantifying-player-versatility-through-lineupbased-guo-ley/7bb4e30e8f095f798dce64e77d2b8b2a/) [[4.2]](https://consensus.app/papers/from-position-to-role-konca-erilli/b58a1415d84155feab9d95b47704d683/) [[8.2]](https://consensus.app/papers/modeling-the-influence-of-basketball-players’-offense-chen-zhang/c31c0efb1a2d5ac99d39a0f30ac3344e/) [[10]](https://consensus.app/papers/offensive-lineup-analysis-in-basketball-with-clustering-yamada-fujii/57c85a1d01c450838461e31e839890ed/).

**Figure 2.** Hierarchical clustering dendrogram of shooting style clustering. The vertical axis represents the 1-Wasserstein distance and the horizontal axis represents each player. [[10]](https://consensus.app/papers/offensive-lineup-analysis-in-basketball-with-clustering-yamada-fujii/57c85a1d01c450838461e31e839890ed/)

*How to read: The dendrogram illustrates hierarchical clustering agglomeration: the vertical axis indicates the 1-Wasserstein cluster distance and the horizontal axis represents individual player instances.*

## Target Journals for Basketball Optimization

Target Q1 and leading peer-reviewed venues actively publishing basketball lineup models, positionless clustering, and sports operations research:

* **Journal of Quantitative Analysis in Sports (JQAS)**: Publishes hierarchical Bayesian lineup evaluations, positionless defensive efficiency, and multi-classifier lineup predictions [[13.3]](https://consensus.app/papers/a-basketball-paradox-exploring-nba-team-defensive-south/320edd4969955098a450e995896edb5c/) [[13.1]](https://consensus.app/papers/a-basketball-paradox-exploring-nba-team-defensive-south/320edd4969955098a450e995896edb5c/) [[12.4]](https://consensus.app/papers/predicting-elite-nba-lineups-using-individual-player-martonosi-gonzález/72568186715e541b85728f3852b9bda1/) [[12.5]](https://consensus.app/papers/predicting-elite-nba-lineups-using-individual-player-martonosi-gonzález/72568186715e541b85728f3852b9bda1/).
* **IMA Journal of Management Mathematics**: Specializes in Bayesian regularized adjusted plus-minus, play-by-play modeling, and mathematical team management in EuroLeague contexts [[6.1]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) [[6.2]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/) [[6.9]](https://consensus.app/papers/an-extended-regularized-adjusted-plusminus-analysis-for-grassetti-bellio/912affabbf4352dfad5265d6f5d20e0b/).
* **Annals of Operations Research**: Features game-theoretic evaluations, generalized Shapley values, and mathematical lineup optimization models under real-world constraints [[16.1]](https://consensus.app/papers/efficient-statistical-computation-for-kplayer-mountantonakis/660bfd70e5015bbba9b301d39e04d80f/) [[9.2]](https://consensus.app/papers/measuring-players’-importance-in-basketball-using-the-metulini-gnecco/e32f7a9470df5f44ba510a9748257e86/) [[9.3]](https://consensus.app/papers/measuring-players’-importance-in-basketball-using-the-metulini-gnecco/e32f7a9470df5f44ba510a9748257e86/).
* **Journal of the Operational Research Society**: Focuses on mixed-integer nonlinear programming, data-driven roster construction, and player archetype synergy optimization [[3.2]](https://consensus.app/papers/sports-analytics-for-balanced-teambuilding-decisions-muniz-flamand/e56acea13a235728affa181d1b9059cc/) [[3.1]](https://consensus.app/papers/sports-analytics-for-balanced-teambuilding-decisions-muniz-flamand/e56acea13a235728affa181d1b9059cc/).
* **Applied Soft Computing**: Features integrated frameworks combining unsupervised dimensionality reduction, neural networks, and roster selection under budgetary limits [[17.1]](https://consensus.app/papers/a-unified-machine-learning-framework-for-basketball-team-ke-bian/cdd3e66aab0259748b888bafebb97eac/) [[17.2]](https://consensus.app/papers/a-unified-machine-learning-framework-for-basketball-team-ke-bian/cdd3e66aab0259748b888bafebb97eac/).
* **International Journal of Sports Science & Coaching**: Regularly covers positionless versatility frameworks, non-negative matrix factorization, and rotation Markov modeling [[15.2]](https://consensus.app/papers/quantifying-player-versatility-through-lineupbased-guo-ley/7bb4e30e8f095f798dce64e77d2b8b2a/) [[15.3]](https://consensus.app/papers/quantifying-player-versatility-through-lineupbased-guo-ley/7bb4e30e8f095f798dce64e77d2b8b2a/) [[16.2]](https://consensus.app/papers/efficient-statistical-computation-for-kplayer-mountantonakis/660bfd70e5015bbba9b301d39e04d80f/).
 
_These search results were found and analyzed using Consensus, an AI-powered search engine for research. Try it at https://consensus.app. © 2026 Consensus NLP, Inc. Personal, non-commercial use only; redistribution requires copyright holders’ consent._
 
## References
 
`1.` Penner LSJ. Player archetypes within basketball: optimizing roster composition to create a championship team. *Frontiers in Sports and Active Living.* 2025;7. doi:10.3389/fspor.2025.1639431
 
> [1.1] The present study assessed the feasibility of grouping university and professional basketball players across different leagues based on their playing styles to optimize championship team construction, moving beyond traditional positional constraints towards a positionless approach. (Body)
 
> [1.2] A comprehensive dataset of 22,500 elite professional and university athletes from 110 leagues, sourced from EuroBasket, RealGM, and USportsHoops, was analyzed. (Body)
 
> [1.3] Utilizing the k-means algorithm, players were clustered into 9 distinct player archetypes. (Body)
 
> [1.4] Optimal player cluster proportions were derived from analyses of 2018/19 NBA lineups and 2014−2018 international medal-winning teams to create the most effective team line-ups. (Body)
 
> [1.5] Multiple linear regression models were then developed for each archetype, predicting “points per minute” to facilitate player ranking, further refined by a data-driven league quality weighting system. (Body)
 
`2.` Kalman S, Bosch J. NBA Lineup Analysis on Clustered Player Tendencies: A new approach to the positions of basketball & modeling lineup efficiency of soft lineup aggregates. 2020.
 
> [2.1] With ten seasons (2009-2018) of NBA player stats [1] that account for a player’s efficiency, opportunity, and tendencies, we were able to implement unsupervised machine learning techniques to create a framework for how NBA playing styles can be clustered on the court and used for strategic decision making when building rosters and creating lineup rotations. (Abstract)
 
> [2.2] Our unique methods give players a soft assignment for all clusters, that is, a probabilistic weighting onto each of the clusters indicating their likelihood of specific cluster fit. (Abstract)
 
> [2.3] Our models also contain a predictive component where we have the ability to predict the net rating of a potential lineup. (Abstract)
 
`3.` Muniz M, Flamand T. Sports analytics for balanced team-building decisions. *Journal of the Operational Research Society.* 2022;74:1892 - 1909. doi:10.1080/01605682.2022.2118634
 
> [3.1] These inform a mixed-integer nonlinear programming model for the draft, trade and free agent acquisition problem that maximizes the total team value and balances the synergy among players. (Abstract)
 
> [3.2] We consider “archetypes” of players that represent logical groupings of players based on their characteristics. (Abstract)
 
> [3.3] Finally, we conduct a case study on a National Basketball Association (NBA) team using 2019–2020 data. (Abstract)
 
> [3.4] To estimate the synergy potential between two players, we develop a new metric that encompasses the synergy potential between archetype pairs that each player belongs to. (Abstract)
 
> [3.5] Abstract We address a team-building problem for a basketball team, where the team decides on new players to draft, current players to trade with those of other teams, and/or which free agents to acquire, to maximize its total value. (Abstract)
 
`4.` Konca E, Erilli N. From position to role. *Journal of Human Sport and Exercise.* 2026. doi:10.55860/9sfjc227
 
> [4.1] Contemporary elite professional basketball has shifted from rigid positional boundaries toward fluid, hybridized frontcourt roles. (Abstract)
 
> [4.2] Analyses included Exploratory Factor Analysis (EFA), Linear Mixed Models (LMM) with unstructured covariance to account for repeated measures, and Fuzzy C-Means (FCM) clustering validated by Artificial Neural Network (ANN) stability procedures. (Abstract)
 
> [4.3] Nakagawa’s R² values demonstrated strong model fit (Marginal R² = .17 – .25; Conditional R² = .51 – .58). (Abstract)
 
`5.` Ibáñez S, Courel-Ibáñez J, Contreras-García JM, Piñar-López MI. Redefining player roles in professional women’s basketball: From traditional positions to functional profiles. *PLOS One.* 2025;20:e0330726 - e0330726. doi:10.1371/journal.pone.0330726
 
> [5.1] These contributions converge on a clear conclusion: static positional models fail to capture the complexity of contemporary basketball. (Body)
 
> [5.2] Game-related statistics were normalized by effective playing time and scaled to a 40-minute format. (Abstract)
 
`6.` Grassetti L, Bellio R, Di Gaspero L, Fonseca G, Vidoni P. An extended regularized adjusted plus-minus analysis for lineup management in basketball using play-by-play data. *IMA Journal of Management Mathematics.* 2020. doi:10.1093/imaman/dpaa022
 
> [6.1] In this work we analyse basketball play-by-play data in order to evaluate the efficiency of different five-man lineups employed by teams. (Abstract)
 
> [6.2] For the empirical analysis, we use the 2018/2019 regular season of the Turkish Airlines Euroleague Championship, with play-by-play and box scores for 240 matches, which are made available by the league website. (Abstract)
 
> [6.3] The model fitting procedure is Bayesian and provides the necessary regularisation. (Abstract)
 
> [6.4] As a side result, our score measure can also be viewed as the composition of four sources, providing further insight on the effective strength of a given lineup: the inside scoring skill (lay-ups, dunks and free shots), the mid-range shooting skill, the three-pointers shooting skill and the set of complementary skills (assists, rebounds, blocks and steals), hereafter called other skills . (Introduction)
 
> [6.5] The results of the model fitting can be used for several investigations as, for instance, the comparative analysis of the effects of single players and the estimation of total and synergic effects of lineups monitoring. (Abstract)
 
> [6.6] The second extension focuses on entire lineups rather than individual players, using a suitable extended model specification. (Abstract)
 
> [6.7] An innovative feature of our model is the adoption as a response variable of a more comprehensive performance index rating, rather than the simple point differential; in the sequel, such performance index rating is simply called overall score . (Introduction)
 
> [6.8] The first extension replaces the classical response variable (scored points) with a comprehensive score that combines a set of box score statistics. (Abstract)
 
> [6.9] The proposed model has been estimated following a Bayesian approach, which offers several advantages compared to the ridge regression approach adopted in the literature. (Conclusion)
 
`7.` Petridis C, Pelechrinis K. Lineup Regularized Adjusted Plus-Minus (L-RAPM): Basketball Lineup Ratings with Informed Priors. *ArXiv.* 2026;abs/2601.15000. doi:10.48550/arxiv.2601.15000
 
> [7.1] To solve this problem Sill (2010) introduced the regularized version of the APM model (RAPM) that has more (Introduction)
 
> [7.2] In this work, we propose a regression-based approach that controls for the opposition faced by each lineup, while it also utilizes information about the players making up the lineups. (Abstract)
 
> [7.3] In this work we design L-RAPM , a regression-based model to evaluate basketball lineups. (Discussion)
 
> [7.4] Our experiments indicate that L-RAPM provides benefits over current baselines, and these benefits are higher when the sample size of observed lineup performance is smaller (i.e., in those settings that we are most interested in). (Discussion)
 
> [7.5] A player's APM is calculated through a regression model, where each data point corresponds to a possession and the dependent variable is the points scored during the possession. (Introduction)
 
> [7.6] L-RAPM addresses the major problem when rating lineups, that is, small sample size. (Discussion)
 
> [7.7] A typical lineup will play an average of 30 to 40 total possession for a whole season and its observed performance is susceptible to variance. (Discussion)
 
> [7.8] Even though our main objective for this work is to show that adjusting for opposition (through the model covariates) and for the players in the lineup (through the prior), one could further tweak the model to improve its predictive performance even more. (Discussion)
 
> [7.9] In particular, a National Basketball Association (NBA) team will use more than 600 lineups during a season, which translates to an average lineup having seen the court in approximately 25-30 possessions. (Abstract)
 
`8.` Chen R, Zhang M, Xu X. Modeling the influence of basketball players’ offense roles on team performance. *Frontiers in Psychology.* 2023;14. doi:10.3389/fpsyg.2023.1256796
 
> [8.1] However, the studies mentioned above primarily rely on basic statistics, such as box scores, which have inherent limitations (Shea and Baker, 2013). (Body)
 
> [8.2] The clustering results obtained fourteen offensive roles for native players and five for foreign players. (Abstract)
 
`9.` Metulini R, Gnecco G. Measuring players’ importance in basketball using the generalized Shapley value. *Annals of Operations Research.* 2022;325:441 - 465. doi:10.1007/s10479-022-04653-z
 
> [9.1] It follows that players and team should not be evaluated separately (e.g., by studying players' performance by means of points made or team performance by means of percentage of winnings), but according to comprehensive advanced measures that take into account the team and the players together. (Introduction)
 
> [9.2] A novelty, allowed by explicitly considering single lineups, is represented by the possibility of forming best lineups based on players' estimated generalized Shapley values conditional on specific constraints, such as an injury or an 'a-priori' coach's decision. (Abstract)
 
> [9.3] A novelty, allowed by explicitly considering single lineups, is represented by the possibility of forming best lineups based on players’ estimated generalized Shapley values conditional on specific constraints, such as an injury or an “a-priori” coach’s decision. (Abstract)
 
`10.` Yamada K, Fujii K. Offensive Lineup Analysis in Basketball with Clustering Players Based on Shooting Style and Offensive Role. *ArXiv.* 2024;abs/2403.13821. doi:10.48550/arxiv.2403.13821
 
> [10.1] However, because the features used for clustering in this study included both offensive and defensive features simultaneously, it was not possible to specifically analyze which aspect of offense or defense is more compatible with each other. (Introduction)
 
> [10.2] For the former, interpretable hand-crafted shot features and Wasserstein distances between shooting style distributions were utilized. (Abstract)
 
`11.` Wei B, Li Z, Zhou C, Gómez M, Zhang M. Enhancing team dynamics: Unveiling synergy effects through social network analysis in professional basketball.. *Acta psychologica.* 2025;261:105747. doi:10.1016/j.actpsy.2025.105747
 
> [11.1] Further analysis revealed that: (1) only ten player roles were highly correlated with excellent lineups; (2) the presence of the C6 Core Ball Handler enhanced the performance of most teammates; (3) the C1 Off-Ball Shooter's performance heavily depended on the interaction with the C6 Ball Handler and the C2 Versatile Big; and (4) the C3 Ball Dominant Scorer negatively impacted the performance of all other player roles. (Abstract)
 
`12.` Martonosi SE, González M, Oshiro N. Predicting elite NBA lineups using individual player order statistics. *Journal of Quantitative Analysis in Sports.* 2023;19:51 - 71. doi:10.1515/jqas-2022-0039
 
> [12.1] Hustle stats are included since they quantify a player's defensive contribution to the lineup. (Introduction)
 
> [12.2] To train the models, we use a random sample of 712 lineups with at least 25 min of playing time. (Introduction)
 
> [12.3] Wetrain and test the model on individual player and lineup data from the 2017-18 season and use the model to predict the performance of lineups drawn from all 30 NBA teams' 2018-19 regular season rosters. (Introduction)
 
> [12.4] https://doi.org/10.1515/jqas-2022-0039 Received June 8, 2021; accepted May 8, 2023; published online May 23, 2023 Abstract : NBA team managers and owners try to acquire high-performing players. (Body)
 
> [12.5] Although the ANC is conservative and misses some high-performing lineups, it achieves high precision and recommends positionally balanced lineups. (Introduction)
 
`13.` South C. A basketball paradox: exploring NBA team defensive efficiency in a positionless game. *Journal of Quantitative Analysis in Sports.* 2024;21:345 - 359. doi:10.1515/jqas-2024-0010
 
> [13.1] I find that the fuzzy k -means approach leads to a modest improvement in both the root mean squared error and median 95 % posterior predictive interval width for the test data, and, more importantly, identifies 11 modern archetypes that, when combined, are correlated with team win total and adjusted team defensive rating. (Abstract)
 
> [13.2] Using data from the 2016-17, 2017-18, and 2018-19 seasons, I explore how Bayesian hierarchical models can be used to estimate team defensive strength in three ways. (Abstract)
 
> [13.3] Charles South* https://doi.org/10.1515/jqas-2024-0010 Received July 7, 2023; accepted July 17, 2024; published online August 19, 2024 Abstract : In the last decade, the offensive and defensive philosophies employed by teams in the National Basketball Association (NBA) have changed substantially. (Body)
 
`14.` Biró A, Kovács L, Szilágyi L. Bioinformatics-Inspired Robust Smith-Waterman-Guided Lineup Optimization in Basketball Using HMM Surrogates, PWMs, and Cantelli-Bounded Genetic Algorithms. *2026 IEEE 24th World Symposium on Applied Machine Intelligence and Informatics (SAMI).* 2026. doi:10.1109/sami68106.2026.11420354
 
> [14.1] The genetic algorithm jointly maximizes expected net rating, motif alignment, and fatigue balance, while minimizing variance and enforcing risk-aware guarantees. (Abstract)
 
> [14.2] A no-overlap constraint prevents conflicting player combinations, and robust lower bounds on lineup performance are derived using Cantelli’s inequality. (Abstract)
 
`15.` Guo T, Ley C, Cui Y, Shen Y, Zhang C, Mi J. Quantifying player versatility through lineup-based playing styles in elite basketball. *International Journal of Sports Science & Coaching.* 2025;20:688 - 697. doi:10.1177/17479541241312390
 
> [15.1] A two-step clustering algorithm based on cosine distance was then used to group typical performance patterns and quantify each player ' s versatility. (Abstract)
 
> [15.2] We collected data from 11,978 games spanning 10 NBA regular seasons and extracted lineup-based player statistics and applied Non-negative Matrix Factorization to reduce dimensionality, identifying 6 performance bases that represent playing styles in speci fi c lineups. (Abstract)
 
> [15.3] This framework offers basketball practitioners a powerful tool to assess player performance across lineups, supporting informed decisions in lineup optimization, player development and recruitment in basketball and other team sports. (Abstract)
 
`16.` Mountantonakis M. Efficient Statistical Computation for K-Player Basketball Lineups Using Semilattice Structures. *Electronics.* 2025. doi:10.3390/electronics14112104
 
> [16.1] Ann. (Body)
 
> [16.2] ; Kostakidis, T. Evaluating basketball player's rotation line-ups performance via statistical markov chain modelling. (Body)
 
`17.` Ke Y, Bian R, Chandra R. A unified machine learning framework for basketball team roster construction: NBA and WNBA. *Appl. Soft Comput..* 2024;153:111298. doi:10.1016/j.asoc.2024.111298
 
> [17.1] In this paper, we present a unified framework that features a combination of unsupervised and supervised machine learning models for basketball team roster construction. (Abstract)
 
> [17.2] Finally, with some practical limits such as free agents and salary prediction, we give the optimal team roster based on the clustering, team model, rates, and player salaries. (Abstract)
