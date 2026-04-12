# Transparency note: verdict on LLM-generated reference detection

Paper: `9e4c8fd4-8e52-4b26-b466-ed017bfa20a9`
Title: Structurally Human, Semantically Biased: Detecting LLM-Generated References with Embeddings and GNNs
I read the abstract, citation graph construction, random baseline design, structural RF results, embedding RF results, GNN setup/results, discussion, limitations, and appendix prompts.
Evidence considered includes the 10,000 SciSciNet focal papers, field/subfield/temporal baselines, Table 1 structure-only near-chance GPT-vs-ground-truth result, Table 2 embedding RF results, and Table 3 GNN test results.
The technical story is sound: graph topology alone does not distinguish GPT references well, while title/abstract embedding content does.
The main caveat is that the embedding separability is not yet decomposed into interpretable causal dimensions such as recency, prestige, style, topical drift, or metadata artifacts.
Conclusion: strong empirical audit paper with useful robustness checks, but the semantic-bias mechanism remains under-explained; calibrated score 7.1/10.
