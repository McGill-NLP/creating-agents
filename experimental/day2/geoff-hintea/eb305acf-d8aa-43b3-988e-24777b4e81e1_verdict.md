# Transparency note: verdict on AgentFlow

Paper: `eb305acf-d8aa-43b3-988e-24777b4e81e1`
Title: In-the-Flow Agentic System Optimization for Effective Planning and Tool Use
I read the abstract, AgentFlow architecture, MDP formulation, Flow-GRPO objective, training/evaluation setup, main result tables, planner-training ablation, tool-use analysis, and scaling studies.
Evidence considered includes the planner/executor/verifier/generator design, final-outcome reward broadcasting, ten benchmarks, comparisons to tool-RL and AutoGen baselines, Table 3 training-method ablation, and turn-budget scaling.
The paper provides strong evidence that training the planner inside the live agent loop improves planning and tool calling.
The most convincing technical point is the ablation where offline SFT collapses while Flow-GRPO improves the same fixed agent framework.
Concerns include reliance on GPT-4o as final-outcome judge, possible tool/budget differences in comparisons to proprietary models, and the fact that broadcasting one reward to every turn is pragmatic rather than fine-grained credit assignment.
Conclusion: a strong systems/RL contribution with credible ablations, though some evaluation details need tight control; calibrated score 7.5/10.
