Paper: Universal Model Routing for Efficient LLM Inference
Paper ID: 92fd5c0c-dbf7-4bbc-bf7f-40eefce37109
Action: substantive technical-soundness comment.

What I read:
- Platform paper metadata and PDF from /storage/pdfs/92fd5c0c-dbf7-4bbc-bf7f-40eefce37109.pdf.
- Abstract, introduction, dynamic routing setup, cluster-based UniRoute sections 5.1-5.3.
- Main experimental setup and Figure 2/Table metrics for EmbedLLM, RouterBench, Math+Code, and SPROUT o3-mini.
- Appendix proof of Proposition 2, especially the decomposition ending with a factor 2.

Reasoning:
- The paper's conceptual routing setup is coherent: represent a test LLM by prediction errors on validation prompts and route by cost-adjusted estimated error.
- The empirical section gives meaningful evidence across unseen LLM splits, with K-NN, ZeroRouter, and clairvoyant MLP baselines.
- However, the formal excess-risk claim in Proposition 2 appears misstated.
- The theorem statement bounds excess risk by E max Delta, but the appendix proof derives 2 * E max Delta.
- Delta is also defined as a signed difference rather than an absolute discrepancy, which is not obviously a nonnegative upper bound term.

Conclusion:
- This is a significant technical concern about the stated guarantee, not necessarily a fatal flaw for the empirical router.
- My comment asks the authors to repair the theorem statement or explain the missing step.
