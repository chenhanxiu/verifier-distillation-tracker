# The Chase Is the Curriculum, the Capture Anchors the Credit: Pursuit-Evasion Self-Play for Zero-Data LLM Reasoning

## 基本信息

- 作者：Jing Yu、Shengchao Chen、Yiyun Tan
- 首次公开日期：2026-08-22
- 版本日期：2026-08-22（v1）
- arXiv：2608.21871
- 原始论文：https://arxiv.org/abs/2608.21871
- DOI：https://doi.org/10.48550/arXiv.2608.21871
- 代码：论文公开页未提供

## 一句话结论

LURE 把任务生成与求解建模为追逃自博弈，让任务难度自动停在约 50% 可解边界，并用终局捕获锚定单调 verifier 进展，形成稠密过程信用。

## 真正新增的内容

**论文原文结论：** Environment evader 学习把任务放在 solver 的能力前沿；planner-executor pursuer 则同时接收终局 capture 和组归一化的单调 verifier progress，避免仅靠稀疏终奖。

**分析推断：** “约 50% 可解”天然对应高信息量/高熵训练区，可用于选择 Agent 分叉和 verifier 蒸馏样本；但共演化 verifier 与策略仍需独立 sealed eval。

## 核心方法

Evader 以 capture-frontier reward 生成难度恰在学习边界的任务；pursuer 在可验证交互环境中求解。过程奖励要求 verifier progress 单调，并与终局 capture 一同组归一化；round-anchored KL 稳定双边共同演化。

## 关键实验结果

在三个可验证推理环境和三个 backbone 家族中，LURE 在 unified 与 specialist 设置下优于高级基线；统一模型在三个任务家族、九个 held-out benchmark 上取得更强的聚合 OOD zero-shot 准确率。公开摘要未提供逐项绝对增益。

## 证据质量与局限

证据质量中等：跨环境、跨模型和 OOD 评估是优点，但论文仅 9 页，摘要缺少效应量与统计区间。单调 progress verifier 的可靠性、环境生成漏洞和训练—评测共演化风险仍需独立审计。

## 最接近的相关工作

最接近 SPADE、Task-CoEvolve、EnvHarness、I-SDPO 和 milestone/process reward。其区别是用追逃博弈直接学习“刚好可解”的课程位置，并以终态捕获约束过程信用。

## 如何复用或推进 LLM-as-a-Verifier

把最终环境成功作为 outcome anchor，把每步 verifier 分数限制为与真实进展方向一致；对同一任务难度区间持续校准 50% 成功边界，并监控 verifier 是否被生成器利用。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 用 capture-anchored progress 分数调节蒸馏强度，而非独立使用 teacher logits。
- **A/B/T：** 在同状态比较前进、停滞、退步三类分支，学习序数进展分布。
- **真值门控：** terminal capture 决定过程信号方向，防止 verifier 自说自话。
- **Student critique states：** 从刚好失败的边界任务生成 critique，信息密度高于过易/过难样本。
- **高熵探索：** 约 50% 可解区域应重点保留多分支 rollout。
- **Sealed eval：** 冻结独立环境生成器、隐藏 verifier 和 OOD 任务，避免双方共同利用训练检查器。
