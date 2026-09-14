---
title: 'Towards Robust and Adaptive Motion Forecasting: A Causal Representation Perspective'
authors:
  - Yuejiang Liu
  - admin
  - Jonas Schweizer
  - Sherwin Bahmani
  - Alexandre Alahi
date: '2022-01-01'
publication_types:
  - paper-conference
publication: '*IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2022 Workshop on Distribution Shifts at NeurIPS, 2021*'
publication_short: 'CVPR 2022'
abstract: 'Learning behavioral patterns from observational data has been a de-facto approach to motion forecasting. Yet, the current paradigm suffers from two shortcomings: brittle under covariate shift and inefficient for knowledge transfer. In this work, we propose to address these challenges from a causal representation perspective. We first introduce a causal formalism of motion forecasting, which casts the problem as a dynamic process with three groups of latent variables, namely invariant mechanisms, style confounders, and spurious features. We then introduce a learning framework that treats each group separately: (i) unlike the common practice of merging datasets collected from different locations, we exploit their subtle distinctions by means of an invariance loss encouraging the model to suppress spurious correlations; (ii) we devise a modular architecture that factorizes the representations of invariant mechanisms and style confounders to approximate a causal graph; (iii) we introduce a style consistency loss that not only enforces the structure of style representations but also serves as a self-supervisory signal for test-time refinement on the fly. Experiment results on synthetic and real datasets show that our three proposed components significantly improve the robustness and reusability of the learned motion representations, outperforming prior state-of-the-art motion forecasting models for out-of-distribution generalization and low-shot transfer.'
featured: false
tags:
  - CVPR
url_code: 'https://github.com/vita-epfl/causalmotion'
links:
  - name: 'arxiv'
    url: 'https://arxiv.org/abs/2111.14820'
  - name: 'IEEE'
    url: 'https://ieeexplore.ieee.org/document/9879717'
  - name: 'Short Version (NeuriPS''21)'
    url: 'https://openreview.net/forum?id=MPqliTsloys'
---
