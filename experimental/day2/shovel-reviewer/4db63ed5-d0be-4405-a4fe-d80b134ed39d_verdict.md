# Reproducibility Audit: OneReward: Unified Mask-Guided Image Generation via Multi-Task Human Preference Learning

### Summary
OneReward aims to unify disparate mask-guided image generation tasks (inpainting, editing, object placement) under a single reward model trained on multi-task human preferences. While the vision of a shared preference foundation is ambitious, the execution is buried under proprietary dirt. The reliance on an internal base model (Seedream 3.0) makes the entire training pipeline inaccessible to the independent researcher.

### Findings
The central reproducibility failure is the lack of access to the base model and the lack of specificity regarding the Vision-Language Model (VLM) used for the reward signal. The paper claims "code and model available," but this appears to refer only to the final fine-tuned weights, not the foundation required to replicate the results. Furthermore, comparing against commercial black boxes (Adobe Photoshop, Ideogram, Flux Fill Pro) makes longitudinal verification impossible as those systems evolve behind closed doors.

### Open Questions
- Can the OneReward method be successfully replicated using open-source base models like Stable Diffusion or Flux.1 [dev]?
- What are the exact prompt templates used for the VLM to derive the "probability of token Yes" reward signal?

### Method Description Completeness
The high-level concept of multi-task RLHF is clear. However, the specific details needed for implementation—reward model prompts, task-specific dataset mixtures, and human evaluation protocols—are missing or vague.

### Experimental Setup Completeness
The datasets used for the four tasks are mentioned but not fully documented in terms of preprocessing or exact splits. The reliance on commercial baselines for "state-of-the-art" claims is methodologically weak from a reproducibility standpoint.

### Code and Artifact Availability
While a project page is mentioned, the core artifacts (base model) are proprietary. This limits the paper to Level 2 (Empirical Reproducibility) at best, and even that is shaky without the base weights.

### Computational Requirements
Training an RLHF pipeline for image generation is a heavy lift, requiring significant GPU hours. The exact compute costs are not reported.

### Transparency Assessment
The research process is obscured by the use of internal ByteDance infrastructure. The lack of detailed ablations between the unified reward and task-specific rewards makes it hard to see if the "unification" actually unearths synergy or just saves on model count.

### The Email Test Result
**Not reproducible from paper alone.** A researcher would need the proprietary base model and significantly more detail on the preference dataset to even begin digging.

### Overall Reproducibility Verdict
**Significant gaps.** The proprietary foundation is a rock that prevents any meaningful independent verification of the training process.

---
**Score Justification**: The paper presents a legitimate research question but fails the transparency test due to its reliance on internal models and commercial baselines. The reproducibility is severely limited.
**Final Verdict**: Weak Reject
