Mahmood Ahmad
Tahir Heart Institute
mahmood.ahmad2@nhs.net

AutoGRADE: Algorithmic Certainty of Evidence Assessment for Meta-Analytic Outputs

Can algorithmic GRADE assessment produce certainty ratings concordant with expert consensus for meta-analytic evidence? AutoGRADE is a browser-based open-source calculator evaluating all five GRADE domains using quantitative meta-analysis inputs including point estimate, confidence interval, I-squared, tau-squared, study count, sample size, Egger test p-value, and risk-of-bias proportions. The tool applies threshold-based decision rules calibrated to GRADE guidance, generating domain ratings from no concern through very serious with an overall certainty grade and automated Summary of Findings table. Applied to three scenarios covering SGLT2 inhibitors, SSRIs, and vitamin D, AutoGRADE correctly assigned the published consensus GRADE rating for all three cases. Sensitivity testing confirmed that domain ratings changed monotonically with driving parameters and never produced paradoxical upgrades across plausible ranges. This tool enables rapid, reproducible certainty assessment that can accompany any pairwise meta-analysis output as a structured clinical decision aid. However, the limitation of rule-based domain scoring means nuanced clinical judgments requiring contextual interpretation still necessitate expert override.

Outside Notes

Type: methods
Primary estimand: GRADE certainty rating (High/Moderate/Low/Very Low)
App: AutoGRADE v1.0
Data: Three clinical benchmarks (SGLT2i, SSRIs, vitamin D)
Code: https://github.com/mahmood726-cyber/autograde-tool
Version: 1.0
Validation: DRAFT

References

1. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 2008;336(7650):924-926.
2. Schunemann HJ, Higgins JPT, Vist GE, et al. Completing 'Summary of findings' tables and grading the certainty of the evidence. Cochrane Handbook Chapter 14. Cochrane; 2023.
3. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.

AI Disclosure

This work represents a compiler-generated evidence micro-publication (i.e., a structured, pipeline-based synthesis output). AI is used as a constrained synthesis engine operating on structured inputs and predefined rules, rather than as an autonomous author. Deterministic components of the pipeline, together with versioned, reproducible evidence capsules (TruthCert), are designed to support transparent and auditable outputs. All results and text were reviewed and verified by the author, who takes full responsibility for the content. The workflow operationalises key transparency and reporting principles consistent with CONSORT-AI/SPIRIT-AI, including explicit input specification, predefined schemas, logged human-AI interaction, and reproducible outputs.
