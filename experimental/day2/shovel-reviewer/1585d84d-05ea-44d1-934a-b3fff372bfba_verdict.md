# Verdict Reasoning: 1585d84d-05ea-44d1-934a-b3fff372bfba

**Paper:** The Training Instability Onset Index: A Scaling Law for When Large Model Training Breaks

**Read:** Abstract and metadata.

**Reasoning:**
The paper unearths a specific, testable scaling law (TIOI) for training instability, moving beyond the "trial and error" approach currently used in large-scale pretraining.
The formula (eta * sqrt(N)) / (sigma_g * sqrt(B)) provides a clear handle for practitioners to measure their distance from the "edge of stability."
Calibration against GPT-3, PaLM, and LLaMA provides strong empirical leverage.
However, the transparency of the "gradient noise scale" (sigma_g) measurement remains a concern; if this value isn't easily computable from standard training logs, the utility of the index is buried.
The reproducibility of the calibration relies on the accuracy of published hyperparameters, which are often incomplete in frontier model reports.

**Evidence:**
Formula: TIOI = (eta * sqrt(N)) / (sigma_g * sqrt(B))
Calibration: GPT-3, PaLM, LLaMA, Chinchilla logs.
Critical Threshold: TIOI* approx 2.5 - 4.0.

**Conclusion:**
Accept. The contribution is a significant step toward making large model training a science rather than an art.
