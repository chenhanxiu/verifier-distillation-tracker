# FOCUS：面向长时程 Agent 的主动 Critic 学习

## 基本信息

- **论文标题**：FOCUS: Active Critic Learning for Long-Horizon Language Model Agents
- **作者**：Zhengping Jiang, William Jurayj, Liaoyaqi Wang, Chunsheng Zuo, Anqi Liu, Benjamin Van Durme
- **首次公开日期**：2026-10-26
- **版本日期**：2026-10-26（v1）
- **论文链接**：https://arxiv.org/abs/2610.35801
- **代码链接**：未发现公开代码

## 一句话结论

FOCUS 不在每个状态盲目采样 continuation，而是主动选择最能降低 critic 估计误差的分叉，并在上下文压缩边界之间计算 TD(λ) 信用。

## 真正新增的内容

**论文原文结论**：rollout controller 依据预期误差下降选择状态进行续接采样；这些分支既作为 critic 训练目标，也为相邻 segment 提供价值估计与优势。

**分析推断**：这给“高熵分叉下保留探索”增加了比策略熵更直接的标准：分叉价值应由 verifier/critic 的预期信息增益决定，并且长轨迹信用可以落在 compaction-defined segment，而非每个 token 或整条轨迹。

## 核心方法

- 以 context compaction 产生的边界定义长轨迹 segment。
- 主动挑选最可能纠正 critic 的中间状态并采样多个 continuation。
- 使用续接结果监督 value estimator。
- 用 TD(λ) advantage 对相邻状态之间的 segment 评分；context manager 与 rollout allocation 解耦。

## 关键实验结果

**论文报告**：在法律推理、深度搜索和代码定位上，以相同逐步生成预算优于 GRPO 与 VinePPO。Qwen3.5-9B 在 BrowseComp-Plus 上为 55.4，对最强基线 48.2；DeonticBench 为 56.5，对 52.4。

## 证据质量与局限

覆盖三类长时程任务且预算匹配，证据较强。局限是 critic 与策略仍在同一训练闭环中，摘要没有给出跨 critic 家族的稳健性，也未证明估计误差下降必然对应真实任务效用；长轨迹边界依赖 compaction 策略。

## 最接近的相关工作

VinePPO、BATON、EPIG-Tree、Policy-Aligned Predictive Verification、MRTPO。FOCUS 的区别是把 critic 学习与分叉预算分配联合起来。

## 如何复用或推进 LLM-as-a-Verifier

将 continuation 的环境终局结果作为强标签，训练 distributional critic 输出成功概率及区间；用预测方差、分支间分歧和校准误差共同决定是否继续采样，而非只看单点 value。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：把 critic 的 segment-level 后验作为蒸馏幅度，硬终局结果决定方向。
- **A/B/T**：同状态 continuation 的后验重叠时输出 T，避免伪造确定顺序。
- **硬真值门控**：优先使用可执行终局和程序断言更新 critic。
- **critique states**：只接受能改善后续 continuation 的 critique。
- **高熵探索**：按 critic 信息增益分叉，补充单纯 entropy branching。
- **sealed eval**：使用冻结 critic、独立环境快照和未参与分叉选择的 holdout。