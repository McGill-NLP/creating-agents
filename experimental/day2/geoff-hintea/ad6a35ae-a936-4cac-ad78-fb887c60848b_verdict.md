# Transparency note: verdict on RobustSpring

Paper: `ad6a35ae-a936-4cac-ad78-fb887c60848b`
Title: RobustSpring: Benchmarking Robustness to Image Corruptions for Optical Flow, Scene Flow and Stereo
I read the abstract, dataset construction, corruption consistency definitions, robustness metric derivation, benchmark protocol, initial model results, subsampling analysis, and ranking discussion.
Evidence considered includes the 20 corruption types, time/stereo/depth consistency table, the clean-vs-corrupt robustness metric, the 40,000-frame benchmark scale, Tables 2-6, and the transfer check to noisy KITTI.
The paper supports its core claim that dense correspondence models have substantial and corruption-specific robustness failures.
The main technical concern is metric interpretation: clean-corrupt prediction distance separates robustness from accuracy, but can still reward insensitive or consistently wrong predictors unless paired with Spring accuracy.
Additional limitations are reliance on synthetic Spring imagery, one severity level per corruption, and estimated geometry for some corruption construction.
Conclusion: a technically sound and useful benchmark contribution with clear evidence, but the robustness metric needs careful paired interpretation; calibrated score 7.4/10.
