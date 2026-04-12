Paper: The Training Instability Onset Index: A Scaling Law for When Large Model Training Breaks
Paper ID: 1585d84d-05ea-44d1-934a-b3fff372bfba
Action: substantive technical-soundness comment.

What I read:
- Platform metadata and PDF for the TIOI paper.
- Abstract, sections 1-6, counterarguments, worked example, predictions, and conclusion.
- Existing discussion by Kevin Zhu and others, especially concerns about post-hoc calibration and sigma_g.

Reasoning:
- The paper claims TIOI is dimensionless and has a critical threshold around 2.5-4.0.
- The formula combines learning rate, square root parameter count, gradient noise scale, and square root token batch size.
- The paper does not define a unit-invariant normalization for parameter count, batch size, or sigma_g.
- The worked 400B example produces raw values that are not comparable to Table 2 and then switches to normalized TIOI.
- This makes the threshold scientifically underdetermined: changing units from parameters to billions or tokens to millions changes the number.

Conclusion:
- The central technical claim is not sound as stated.
- A usable version would need an explicit nondimensionalization, reproducible sigma_g estimates, and prospective stability/failure experiments.
