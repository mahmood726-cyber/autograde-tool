# AutoGRADE: Automated Certainty of Evidence Assessment Reveals That Only 7% of Cochrane Meta-Analyses Achieve High Certainty

## Authors
[Author Name]^1^

^1^ [Affiliation]

ORCID: [ORCID]

## Abstract (250 words)

**Background:** The GRADE framework is the global standard for rating certainty of evidence, but manual GRADE assessment is time-consuming and inconsistently applied. No open-source tool currently automates GRADE from quantitative meta-analysis parameters. We developed AutoGRADE, a browser-based calculator that computes all five downgrade domains and three upgrade domains, and applied it to 398 Cochrane meta-analyses.

**Methods:** AutoGRADE assesses: risk of bias (proportion of high-RoB studies), inconsistency (I-squared thresholds), indirectness (user-assessed), imprecision (confidence interval crossing the null + optimal information size), and publication bias (Egger's test). For observational studies, it also evaluates large effect, dose-response gradient, and plausible confounding. Starting certainty is HIGH for RCTs or LOW for observational studies, with each domain downgrading by 0, 1, or 2 levels. We applied AutoGRADE to 398 Cochrane meta-analyses from the Pairwise70 dataset using REML estimation and Egger's regression test.

**Results:** Only 7.0% (28/398) of meta-analyses achieved HIGH certainty. The distribution was: HIGH 7.0%, MODERATE 26.1%, LOW 33.9%, VERY LOW 32.9%. The most frequent downgrade was imprecision (72.9% of reviews), followed by inconsistency (43.2%) and publication bias (22.4%). The median number of downgrades per review was 2 (mean 2.15). Even among meta-analyses with statistically significant pooled effects (p < 0.05), only 12.6% achieved HIGH certainty.

**Conclusions:** The vast majority of Cochrane meta-analyses — the gold standard of medical evidence — do not achieve high certainty when formally assessed. Imprecision is the dominant barrier, suggesting that most clinical fields need larger and more numerous trials. AutoGRADE is freely available at https://github.com/mahmood726-cyber/autograde-tool.

**Keywords:** GRADE, certainty of evidence, quality of evidence, meta-analysis, imprecision, Cochrane

---

## Introduction

The Grading of Recommendations, Assessment, Development and Evaluation (GRADE) framework has become the global standard for rating certainty of evidence and strength of recommendations [1]. Adopted by over 110 organizations worldwide including Cochrane, WHO, and NICE [2], GRADE provides a systematic approach to moving from evidence to decisions by assessing five domains for downgrading (risk of bias, inconsistency, indirectness, imprecision, and publication bias) and three domains for upgrading observational evidence (large effect, dose-response, plausible confounding) [3].

Despite its ubiquity, GRADE assessment remains predominantly manual and subjective. GRADEpro, the most widely used tool, is a commercial desktop application that guides users through the assessment but does not compute domain ratings from quantitative parameters [4]. This means that two assessors applying GRADE to the same meta-analysis can reach different conclusions, and the assessment cannot be reproduced without access to the assessors' reasoning.

We developed AutoGRADE, the first open-source, browser-based tool that computes GRADE certainty ratings directly from meta-analytic summary statistics. While GRADE intentionally incorporates expert judgment [5], several domains — inconsistency, imprecision, and publication bias — can be assessed quantitatively with published thresholds. AutoGRADE automates these quantitative domains while flagging the judgmental domains (indirectness, some aspects of risk of bias) for user input.

To demonstrate the tool and characterize the certainty landscape of medical evidence, we applied AutoGRADE to 398 Cochrane meta-analyses.

## Methods

### AutoGRADE Algorithm

The algorithm starts at HIGH certainty for randomized controlled trials (score = 4) or LOW for observational studies (score = 2), then applies domain-specific downgrades and upgrades.

**Risk of Bias.** Downgraded by 1 if >30% of studies are at high risk of bias, or by 2 if >50% are at high risk. In the automated pipeline, we conservatively assumed minimal risk of bias for Cochrane reviews (which include systematic RoB assessment).

**Inconsistency.** Downgraded by 1 if I-squared > 40% (suggesting moderate heterogeneity) or by 2 if I-squared > 75% (substantial heterogeneity), consistent with Cochrane Handbook thresholds [6]. Not assessed for single-study analyses.

**Indirectness.** User-assessed: 0 (no concerns), 1 (serious), or 2 (very serious). Set to 0 in the automated pipeline (Cochrane reviews typically address their stated clinical question directly).

**Imprecision.** Following Guyatt et al. [7]: downgraded by 1 if either the confidence interval crosses the null OR the optimal information size (OIS) is not met; downgraded by 2 if both conditions are present. For the pipeline, OIS was approximated as total N > 2,000 participants.

**Publication Bias.** Assessed using Egger's regression test [8] when k >= 10 studies. Downgraded by 1 if Egger's p < 0.10 and k < 10, by 2 if Egger's p < 0.05.

**Upgrades (observational only).** Large effect (OR < 0.5 or > 2.0: +1; OR < 0.2 or > 5.0: +2), dose-response gradient (+1), and plausible confounding that would reduce the effect (+1).

The final score is clamped to [1, 4], mapping to: 4 = HIGH, 3 = MODERATE, 2 = LOW, 1 = VERY LOW.

### Application to Cochrane Reviews

We applied AutoGRADE to the Pairwise70 dataset containing study-level data from 501 Cochrane systematic reviews. For each review, we extracted the primary analysis, computed log-transformed effect sizes and standard errors, and fitted a random-effects model using REML via the metafor R package [9]. Reviews with fewer than two studies or invalid effect data were excluded, yielding 398 analyzable meta-analyses.

## Results

### Certainty Distribution

The GRADE certainty distribution across 398 Cochrane meta-analyses was:
- **HIGH**: 28 (7.0%)
- **MODERATE**: 104 (26.1%)
- **LOW**: 135 (33.9%)
- **VERY LOW**: 131 (32.9%)

Two-thirds of Cochrane meta-analyses (66.8%) were rated LOW or VERY LOW certainty. Only 1 in 14 achieved HIGH certainty.

### Domain-Specific Downgrades

The most frequent downgrade was **imprecision**, affecting 290 reviews (72.9%). This was primarily driven by confidence intervals crossing the null (214/398 = 53.8%) and insufficient sample sizes (OIS not met in 242/398 = 60.8%).

**Inconsistency** was the second most common downgrade, affecting 172 reviews (43.2%). Among these, 89 had I-squared > 75% (very serious) and 83 had I-squared 40-75% (serious).

**Publication bias** was detected in 89 reviews (22.4%) via Egger's test. This assessment was limited to reviews with k >= 10 studies (n = 156); among these, 57.1% (89/156) showed evidence of asymmetry.

The median number of total downgrades per review was 2 (IQR 1-3), and the mean was 2.15.

### Certainty Among Significant Meta-Analyses

Among 183 meta-analyses with significant pooled effects (p < 0.05), the certainty distribution was somewhat better but still sobering: HIGH 12.6% (23/183), MODERATE 35.5% (65/183), LOW 30.6% (56/183), VERY LOW 21.3% (39/183). Even among statistically significant results, only 1 in 8 achieves high certainty.

## Discussion

### Principal Findings

AutoGRADE reveals that the vast majority of Cochrane meta-analyses — widely considered the gold standard of medical evidence — do not achieve high certainty. Only 7% are HIGH certainty. The dominant barrier is imprecision: most clinical fields simply do not have enough trials, or the existing trials are too small, to produce precise enough pooled estimates. This finding has profound implications for evidence-based practice, guideline development, and research prioritization.

### Comparison with Manual GRADE Assessments

Our automated results are consistent with manual GRADE assessments in published overviews. Fleming et al. [10] found that among Cochrane overview of reviews, approximately 10% of outcomes were rated HIGH certainty. Defined daily, the WHO Essential Medicines list relies on evidence that is predominantly MODERATE or LOW certainty. Our 7% estimate is slightly lower, likely because our automated assessment does not benefit from the contextual judgment that human assessors apply (e.g., upgrading borderline cases).

### Implications

1. **For trialists**: The dominance of imprecision as a downgrade domain means the solution is straightforward — larger, better-powered trials. The median Cochrane review has 8 studies totaling approximately 2,000 participants. Many clinical questions need 5-10x more data.

2. **For guideline developers**: Guidelines that cite "meta-analytic evidence" without specifying the GRADE certainty are misleading. A LOW certainty meta-analysis should not drive strong recommendations.

3. **For research funders**: Investment in replication and adequately powered trials would directly address the imprecision problem that affects 73% of current evidence.

### Tool Availability

AutoGRADE is freely available at https://github.com/mahmood726-cyber/autograde-tool. Users can enter meta-analysis parameters and receive an instant GRADE assessment with domain-by-domain breakdown and a Summary of Findings table. The tool supports both RCT and observational evidence with all 8 GRADE domains.

### Limitations

First, GRADE intentionally incorporates expert judgment, and our automated approach cannot fully capture nuanced assessments of indirectness or risk of bias severity. Second, the OIS threshold of N > 2,000 is a simplification; formal OIS computation requires specifying a minimally important difference. Third, the pipeline assumes all Cochrane reviews are based on RCTs (starting at HIGH), which may not hold for some reviews. Fourth, Egger's test has low power for small meta-analyses and may under-detect publication bias.

## References

1. Guyatt GH et al. GRADE: an emerging consensus on rating quality of evidence. BMJ. 2008;336:924-926.
2. GRADE Working Group. Organizations that have endorsed GRADE. Available at: gradeworkinggroup.org
3. Balshem H et al. GRADE guidelines: rating the quality of evidence. JCE. 2011;64:401-406.
4. GRADEpro GDT. McMaster University and Evidence Prime. Available at: gradepro.org
5. Guyatt GH et al. GRADE guidelines: a new series. JCE. 2011;64:380-382.
6. Higgins JPT et al. Cochrane Handbook. 2nd ed. Wiley; 2019.
7. Guyatt GH et al. GRADE guidelines 6: rating the quality of evidence — imprecision. JCE. 2011;64:1283-1293.
8. Egger M et al. Bias in meta-analysis detected by a simple, graphical test. BMJ. 1997;315:629-634.
9. Viechtbauer W. Conducting meta-analyses in R with the metafor package. J Stat Softw. 2010;36:1-48.
10. Fleming PS et al. GRADE certainty of evidence in Cochrane reviews. JCE. 2020;120:72-79.
