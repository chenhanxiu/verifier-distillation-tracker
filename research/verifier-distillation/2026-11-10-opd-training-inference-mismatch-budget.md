# How Much Training-Inference Mismatch Can On-Policy Distillation Tolerate?

- **作者**：Cong Yu、Ziting Wang、Songlin Jiang、Sitong Zhang、Chengliang Chai、Youhe Jiang、Eiko Yoneki、Tuo Shi
- **首次公开日期**：2026-11-10
- **版本日期**：2026-11-10（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.11450
- **代码**：https://github.com/benyucong/train-inference-mismatch-opd
- **标识符**：arXiv:2611.11450

## 一句话结论

【论文原文】OPD 对量化、异步 rollout 和一定程度的权重陈旧具有可测的“偏差预算”，但过大偏差会改变 student 实际访问的前缀，不能靠逐 token 重要性修正完全补救。

## 真正新增的内容

【论文原文】工作首次把量化、权重陈旧和注入噪声造成的训练—推理不一致放到同一量尺上，跨三个 teacher–student 配置测量 OPD 的容忍区间，并提出无需为每种 rollout 配置完整训练的轻量准入检查。它还把“同一前缀上的分布误差”和“偏差导致访问了不同前缀”区分开来，指出后者是逐 token 校正无法覆盖的结构性误差。

## 核心方法

- 比较 BF16、不同精度量化、异步/陈旧权重及人工噪声下 rollout policy 与训练中 student 的分布偏差。
- 用统一的 mismatch 指标校准经验预算，并识别对低精度特别敏感的层。
- 以候选 rollout 配置的短程测量进行准入，超过预算则拒绝，不必逐个跑完整 OPD。
- 针对不同模型选择 FP8 配方，而非假设统一精度策略可迁移。

## 关键实验结果

【论文原文】OPD 在会使若干 RL 方法失稳的 rollout 配置下仍保持稳定，但超过经验预算后训练质量下降。模型特定 FP8 配方在保持训练质量的同时，使 KV cache 可容纳的 token 数至少达到 BF16 的 **1.93 倍**；FP8 与异步 rollout 结合后，以同步 BF16 的 **1.62 倍速度**达到相同训练质量。

## 证据质量与局限

【论文原文】量化实验覆盖三个 student–teacher 配置，陈旧权重和注入噪声只在其中一个配置上进行；结论是经验规律，不是对任意模型或 Agent 环境的理论保证。论文直接研究语言模型 OPD 系统，而非 verifier score 蒸馏，也没有验证长时程工具轨迹中的状态恢复或 evaluator 共适应。

【分析推断】高熵分叉更可能放大“访问前缀改变”问题，但该论文没有按状态熵分层报告，不能把这一点当作已证实结论。

## 最接近的相关工作

最接近的是 Low-Bit OPD（在真实量化部署路径的 student prefix 上训练）、Mismatch Matters/TIDE（区分 student-excess 与 student-deficit token）以及异步 RL 的 policy-lag 校正。本文的区别在于直接给 rollout 基础设施建立可操作的 mismatch budget，而不是只修改蒸馏损失。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 verifier student 的 rollout 引擎也视为待校准测量仪：上线前同时记录 score 分布漂移、A/B/T 翻转率和 ordinal 分布的 Wasserstein/TV 偏差；只有都落在校准预算内才允许低精度或异步采样。对改变了访问状态的样本，不应只做 token 权重修正，而应重新采样或用环境 oracle 复核。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：增加 rollout-policy mismatch 作为独立门控变量，不能把部署引擎与训练引擎混用而不报告。
- **A/B/T 与序数分布**：除均值分数外，比较量化前后的排序翻转、T 概率和尾部质量。
- **程序化/环境真值**：硬真值仍负责方向；当 mismatch 超预算时冻结软 teacher 幅度，避免错误前缀被放大。
- **student-generated critique states**：保存生成这些状态时的模型版本、量化配置与权重陈旧度，超预算状态不得进入训练池。
- **高熵分叉**：优先用同步高精度复采样高熵节点，低熵节点再使用便宜 rollout。
- **sealed eval**：以同步 BF16、冻结模型快照作为独立对照，防止效率配置与 evaluator 一同漂移。