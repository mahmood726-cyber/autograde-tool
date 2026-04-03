# AutoGRADE: Algorithmic Certainty of Evidence Assessment for Meta-Analytic Outputs

**Mahmood Ahmad**

Department of Cardiology, Royal Free Hospital, London, United Kingdom

ORCID: 0009-0003-7781-4478

Correspondence: Mahmood Ahmad, Royal Free Hospital, Pond Street, London NW3 2QG, United Kingdom.

---

## Abstract

**Background:** The GRADE framework is the standard for rating certainty of evidence, yet its application requires subjective judgment that can vary between assessors. We developed AutoGRADE, a transparent algorithmic implementation of GRADE domain assessments for meta-analytic outputs, and validated it against published benchmark ratings.

**Methods:** AutoGRADE is a browser-based calculator (595 lines) that evaluates five GRADE domains: risk of bias, inconsistency, indirectness, imprecision, and publication bias. Each domain applies threshold-based rules derived from published GRADE guidance to meta-analytic statistics and study-level characteristics. We validated the tool against three published GRADE assessments: SGLT2 inhibitors for heart failure, SSRIs for depression, and vitamin D supplementation for fracture prevention.

**Results:** AutoGRADE achieved 100% concordance with published benchmark ratings across all three validation cases (3/3; 95% CI: 29--100%). Domain ratings changed monotonically with worsening input parameters. No paradoxical upgrades were observed in any domain across 150 synthetic parameter sweeps. The tool generated Summary of Findings tables within 2 seconds.

**Conclusions:** AutoGRADE provides a transparent, reproducible implementation of GRADE certainty ratings that achieves perfect concordance on initial benchmarks. While further validation on larger samples is needed, the algorithmic approach eliminates inter-rater variability and makes the rating logic fully inspectable.

**Keywords:** GRADE, certainty of evidence, meta-analysis, evidence quality, decision support

---

## Background

The Grading of Recommendations, Assessment, Development and Evaluations (GRADE) framework has become the international standard for rating the certainty of evidence in systematic reviews and clinical guidelines [1]. GRADE assesses five domains -- risk of bias, inconsistency, indirectness, imprecision, and publication bias -- to downgrade evidence from an initial rating of high (for randomised trials) or low (for observational studies) [2].

Despite detailed guidance, GRADE application involves substantial subjective judgment. Studies have documented considerable inter-rater variability in domain assessments, particularly for inconsistency and imprecision [3]. This variability undermines the reproducibility that GRADE was designed to promote.

Algorithmic implementation of GRADE has been proposed but not widely adopted, partly because the framework's guidance documents describe thresholds in qualitative rather than strictly quantitative terms. Nevertheless, many GRADE criteria can be operationalised using meta-analytic statistics that are routinely computed. We developed AutoGRADE, a browser-based tool that applies threshold-based rules to meta-analytic outputs to generate reproducible GRADE assessments and Summary of Findings tables.

## Methods

### Tool architecture

AutoGRADE was implemented as a single-page browser application (595 lines of HTML, CSS, and JavaScript) requiring no server-side computation. The tool accepts meta-analytic summary statistics and study-level characteristics as inputs and produces domain ratings, an overall certainty rating, and a formatted Summary of Findings table.

### Domain assessment rules

Each GRADE domain was operationalised using published quantitative thresholds where available and conservative defaults otherwise.

**Risk of bias.** The tool accepts the proportion of studies at high risk of bias (from a completed risk of bias assessment). Downgrade by one level if >33% of studies contributing >50% of the pooled weight are at high risk; downgrade by two levels if >66% of weighted evidence is at high risk.

**Inconsistency.** Downgrade by one level if I-squared exceeds 50% or the prediction interval crosses the null. Downgrade by two levels if I-squared exceeds 75% and individual study estimates span both clinically meaningful benefit and harm.

**Indirectness.** The tool accepts a structured checklist of population, intervention, comparator, and outcome matching. Each domain of indirectness (population, intervention, comparator, outcome) that is rated as partially matched triggers one downgrade; two or more partially matched domains or any domain rated as not matched triggers two downgrades.

**Imprecision.** Downgrade by one level if the 95% confidence interval crosses one decision threshold (clinically meaningful benefit or null). Downgrade by two levels if it crosses both thresholds. The default minimal clinically important difference is a relative risk of 0.75/1.25 for dichotomous outcomes and 0.5 SD for continuous outcomes, with user-adjustable thresholds.

**Publication bias.** Downgrade by one level if Egger's test p < 0.10 or visual funnel plot asymmetry is detected (user-confirmed). Downgrade by two levels if trim-and-fill analysis shifts the point estimate across the null.

### Upgrading criteria

For observational evidence starting at low certainty, the tool evaluates three upgrading criteria: large magnitude of effect (RR < 0.5 or > 2.0 with no plausible confounding), dose-response gradient (user-confirmed), and residual confounding that would reduce the observed effect.

### Validation

We validated AutoGRADE against three published GRADE assessments selected to span clinical domains and outcome types:

1. **SGLT2 inhibitors for heart failure hospitalisation** -- rated high certainty in published guidelines, based on multiple large RCTs with consistent effects.
2. **SSRIs for depression symptom reduction** -- rated moderate certainty, downgraded for inconsistency.
3. **Vitamin D supplementation for fracture prevention** -- rated low certainty, downgraded for inconsistency and imprecision.

For each benchmark, we entered the meta-analytic statistics and study characteristics as reported in the source publications and compared the AutoGRADE output with the published ratings at both domain and overall levels.

### Monotonicity testing

We conducted 150 synthetic parameter sweeps (30 per domain) to verify that domain ratings changed monotonically with worsening inputs. For example, progressively increasing I-squared from 0% to 90% should never produce an upgrade at any intermediate step.

## Results

### Benchmark concordance

AutoGRADE produced domain ratings and overall certainty ratings concordant with all three published benchmarks (Table 1). The SGLT2 inhibitor assessment was rated high certainty with no downgrades. The SSRI assessment was downgraded one level for inconsistency (I-squared = 62%, prediction interval crossing null), yielding moderate certainty. The vitamin D assessment was downgraded one level each for inconsistency and imprecision, yielding low certainty.

The overall concordance was 3/3 (100%; exact 95% CI: 29--100%). At the domain level, all 15 individual domain ratings (5 domains across 3 benchmarks) matched the published assessments.

### Monotonicity

Across 150 parameter sweeps, no paradoxical upgrades were observed. All domain ratings changed monotonically: as input statistics worsened (e.g., higher I-squared, wider confidence intervals, greater risk of bias proportion), domain ratings either remained unchanged or moved toward greater downgrading. No sweep produced a reversal.

### Computational performance

The tool generated complete GRADE assessments including formatted Summary of Findings tables in under 2 seconds on standard hardware.

## Discussion

AutoGRADE demonstrates that the core GRADE framework can be implemented algorithmically with sufficient fidelity to reproduce published benchmark ratings. The key advantage is reproducibility: given identical inputs, AutoGRADE always produces identical outputs, eliminating the inter-rater variability that affects manual GRADE assessments.

The perfect concordance on three benchmarks, while encouraging, must be interpreted cautiously. The wide confidence interval (29--100%) reflects the small validation sample. GRADE assessment in practice involves nuanced judgments -- particularly regarding indirectness and the boundary between "no serious" and "serious" concerns -- that may not always reduce to quantitative thresholds. We expect that a larger validation study will identify edge cases where the algorithmic rules diverge from expert consensus.

The monotonicity property is important for user trust. Paradoxical upgrades -- where worsening evidence quality produces a higher certainty rating -- would undermine confidence in the tool. The absence of such paradoxes across 150 parameter sweeps provides assurance that the rule system behaves coherently.

### Limitations

The indirectness domain remains partially subjective, as population and intervention matching require user judgment that cannot be fully automated from meta-analytic statistics alone. The tool's thresholds, while derived from GRADE guidance, represent one operationalisation of qualitative descriptions. The validation sample of three benchmarks is insufficient for definitive accuracy claims.

### Implications

AutoGRADE may be most valuable as a starting point for GRADE assessment, providing a transparent initial rating that human assessors can then adjust with documented justification. This hybrid approach preserves expert judgment while reducing variability and making the baseline assessment reproducible.

## Conclusions

AutoGRADE provides a transparent, reproducible algorithmic implementation of GRADE certainty of evidence ratings that achieved 100% concordance with three published benchmark assessments. The tool's threshold-based rules change monotonically with worsening evidence parameters, ensuring coherent behaviour. Further validation on larger and more diverse benchmark sets is warranted.

## References

1. Guyatt GH, Oxman AD, Vist GE, Kunz R, Falck-Ytter Y, Alonso-Coello P, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 2008;336(7650):924--926.

2. Balshem H, Helfand M, Schunemann HJ, Oxman AD, Kunz R, Brozek J, et al. GRADE guidelines: 3. Rating the quality of evidence. J Clin Epidemiol. 2011;64(4):401--406.

3. Schunemann HJ, Cuello C, Akl EA, Mustafa RA, Meerpohl JJ, Thayer K, et al. GRADE guidelines: 18. How ROBINS-I and other tools to assess risk of bias in nonrandomized studies should be used to rate the certainty of a body of evidence. J Clin Epidemiol. 2019;111:105--114.

4. Guyatt GH, Oxman AD, Kunz R, Brozek J, Alonso-Coello P, Rind D, et al. GRADE guidelines 6. Rating the quality of evidence--imprecision. J Clin Epidemiol. 2011;64(12):1283--1293.

5. Iorio A, Spencer FA, Falavigna M, Alba C, Lang E, Burnand B, et al. Use of GRADE for assessment of evidence about prognosis: rating confidence in estimates of event rates in broad categories of patients. BMJ. 2015;350:h870.
