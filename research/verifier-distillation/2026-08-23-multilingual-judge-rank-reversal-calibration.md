# Rank Reversal in Multilingual LLM Judges: A Label-Free Double-Centering Calibrator

## 基本信息

- 作者：Alhasan Mahmood、Samir Abdaljalil、Hasan Kurban
- 首次公开日期：2026-08-23
- 版本日期：2026-08-23（v1）
- arXiv：2608.22432
- 原始论文：https://arxiv.org/abs/2608.22432
- DOI：https://doi.org/10.48550/arXiv.2608.22432
- 代码：论文公开页未提供

## 一句话结论

多语言 LLM Judge 的模型排名会随评分语言发生反转；一个无需人工标签的双中心化校准器可显著改善跨语言排序一致性，并在独立人类偏好集上提高准确率。

## 真正新增的内容

**论文原文结论：** 将 Judge 分数分解为任务难度、Judge backbone 能力和“语言 × backbone”交互项，并用双中心化恢复交互偏差；同时给出有限样本界和在任务—语言交互存在时的无偏性结果。

**分析推断：** 这不是 verifier 蒸馏算法，但它指出蒸馏 teacher 的分数分布可能携带语言条件偏差；若直接做 score-level distillation，student 会固化这种排名反转。

## 核心方法

对“任务 × 语言 × Judge”得分矩阵执行 Consensus-Based Calibration（CBC），移除可识别的语言—Judge 交互项，再聚合校准后的评分。它本质上是带 sum-to-zero 约束的双向 ANOVA 交互恢复。

## 关键实验结果

- Agent-as-a-Judge：6 个 backbone、8 种语言、55 个任务、3 个框架，共 7,920 次评分；15 对 backbone 中有 7 对显著排名反转。
- CBC 将跨任务 held-out 排序一致性 Kendall τ 从 0.650 提高到 0.902。
- 在 M-RewardBench 的 10,500 个语言—样本实例上，五 Judge panel 与人类偏好一致率从 68.7% 提高到 76.6%，增益 7.9 点，95% CI 为 [6.0, 9.9]。

## 证据质量与局限

证据质量中高：有独立人类偏好集、置信区间和理论性质。主要局限是 Agent 数据上的主要指标是内部一致性而非真实正确性；加性分解也可能遗漏更高阶交互，不能替代人工或环境真值。

## 最接近的相关工作

最接近多 Judge 校准、语言偏差审计、IRT/Bradley–Terry 聚合与 JuryProbe 的共识风险诊断。区别在于本文校准的是语言—backbone 交互，而非仅做多数投票或全局温度缩放。

## 如何复用或推进 LLM-as-a-Verifier

可把每个 verifier 的语言条件偏差作为独立校准层，在进入投票、序数分布聚合或 teacher 蒸馏前先校正；同时保留原始分数与校准分数，供 sealed eval 审计。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 蒸馏前先校准 teacher score/logit，避免 student 学到语言相关排名反转。
- **Pairwise A/B/T 与序数分布：** 应按语言分别估计 A/B/T 概率，再校准后合并，不能只比较总体胜率。
- **真值门控：** 有环境真值时优先作为校准锚点；CBC 只在无标签区域使用。
- **Student critique states：** 对不同语言生成的 critique 分别审计，否则 critique 风格会成为隐含偏差源。
- **高熵探索：** 语言间分歧可作为不确定性信号，而不是强行压成单一排序。
- **Sealed eval：** 保留未参与 CBC 拟合的语言、任务与 Judge 组合，防止校准器与 evaluator 共适应。
