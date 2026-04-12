### Summary
UniRoute addresses the challenge of model routing in a dynamic pool of LLMs where models are frequently added or deprecated. By representing each LLM as a feature vector based on its error performance across representative clusters of prompts, the method avoids the need for expensive router retraining. The authors provide two cluster-based instantiations and a theoretical excess risk bound, demonstrating effectiveness across several benchmarks with over 30 unseen LLMs.

### Findings

#### Claim-Evidence Scope Analysis
- **Universal Routing Capability**: [Fully supported]. The experiments on EmbedLLM and RouterBench across >30 LLMs demonstrate that the cluster-based representation generalizes to models not seen during the training of the prompt embedder.
- **Theoretical Optimality**: [Partially supported]. While the excess risk bound is provided, the 'optimality' depends heavily on the assumption that the validation set {val}$ is representative of the test distribution.
- **Competitive with Static Routers**: [Partially supported]. Table 2 shows it is competitive but often slightly underperforms MLP baselines that learn model-specific representations.

#### Missing Experiments and Analyses
- **Probing Cost Analysis**: [Essential]. To represent a new LLM, it must be run on the entire validation set {val}$. A more detailed analysis of the trade-off between the size of {val}$ and routing performance is conspicuously absent.
- **Sensitivity to $\lambda*: [Expected]. The routing rule depends on a hyperparameter $\lambda$ to balance cost and error. How this choice affects the dynamic generalization as the pool changes is not thoroughly explored.
- **Domain Shift on {val}*: [Helpful]. Performance when the validation set prompts come from a different domain than the test prompts.

#### Hidden Assumptions
- **Labeled Validation Set**: The method assumes ground truth labels are available for {val}$ to compute the error vector. This is a significant requirement that may not hold in all real-world deployment scenarios.
- **Inference Latency of Router**: The paper focuses on monetary cost/quality trade-offs but assumes the latency of the router itself (prompt embedding + cluster assignment + dot product) is negligible.

#### Limitations Section Audit
[Quality assessment: specific but minimal]. The authors acknowledge the gap in static settings and the design space of clusters. However, they minimize the 'probing' cost of new models, which is a major practical hurdle for 'universal' routing.

#### Negative Results and Failure Modes
[Partially reported]. Acknowledge that K-NN underperforms in moderate data regimes. Concede that MLP baselines win in static settings.

#### Scope Verdict
The claims mostly match the evidence, but the 'universality' is gated by the requirement of a labeled, representative probing set.

#### Overall Completeness Verdict
Mostly complete with minor gaps.

### Open Questions
- What is the minimum size of {val}$ required for stable performance across diverse LLM families?
- How does the method handle cases where the ground truth for {val}$ is noisy or unavailable (e.g., using a 'silver' judge model)?
- Can the 'probing' be done on-the-fly, or must it be a discrete benchmarking step?
