Dear Editor,

I am pleased to submit the manuscript entitled "FAST-CP: A Lightweight Perturbation-Aware Conformal Prediction Framework for Corrupted Time-Series Classification" for consideration as an original research article in Pattern Analysis and Applications.

This manuscript addresses uncertainty estimation for corrupted time-series classification, a practical problem in sensor-driven pattern-recognition applications where missing segments, noise, and amplitude drift can affect deployed classifiers. The proposed FAST-CP framework is a lightweight post-hoc conformal prediction layer that uses perturbation-aware local weighting together with a global augmented conformal fallback. Rather than claiming a new distribution-shift validity guarantee, the paper positions the method as a practical coverage-efficiency tradeoff mechanism for limited-compute settings.

The main contributions are:

1. A lightweight post-hoc conformal prediction framework for corrupted time-series classification that does not require retraining the base classifier.
2. A two-mode deployment protocol separating coverage-prioritized global fallback from Pareto-oriented efficient operation.
3. A reproducible benchmark over 35 UCR datasets, five random seeds, three corruption families, and multiple conformal baselines including APS, RAPS, confidence-weighted CP, and Mondrian CP.
4. Additional UEA multivariate, MiniROCKET, and FCN checks to evaluate whether the observed tradeoff is tied to a single data type or backbone.
5. Public code, data access instructions, reproduction scripts, and saved result files, consistent with the journal's replicable research principle.

The manuscript has not been published previously and is not under consideration elsewhere. The author declares no competing interests and received no funding for this work. All datasets used in the study are public benchmark datasets. Code, reproduction scripts, public data access instructions, and saved result files are available at:

https://github.com/zoumaomao/fast-cp-reproducibility

Thank you for considering this submission. I believe the manuscript is suitable for Pattern Analysis and Applications because it focuses on a practical pattern-recognition problem, reports a reproducible empirical evaluation, and emphasizes deployable uncertainty estimation under limited compute.

Sincerely,

Maomao Zou  
Independent Researcher, Shanghai, China  
Email: zoumaomao98@gmail.com
