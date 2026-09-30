# VStress: Correlation-Aware Auditing and Adaptive Budget Allocation for Repeated Verifiers

- **作者**：Miaobo Hu, Shuhao Hu, Xiaobo Guo, Xin Wang, Bokun Wang, Peng Zhang, Daren Zha, Jun Xiao
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2609.36958
- **代码**：未发现公开代码链接

## 一句话结论

VStress 不把重复 Judge 调用当作独立投票，而按 sealed calibration 上的条件边际信息/成本选择下一 verifier，并在无新增信息时停止或 abstain。

## 真正新增的内容

【论文原文】提出可审计 replay contract 和 VStress-CA：估计未查询 verifier 的条件边际信息，折扣不确定性、按成本归一化，并设置停止/弃权；决策与成本账本在接触 clean oracle 前冻结，依赖漂移时退回 exact-stop。

【分析推断】它为多 Judge 的 A/B/T 聚合和在线 verifier 路由提供了比多数票更合适的控制器，也明确把 sealed calibration 写进协议。

## 核心方法

在冻结校准集估计通道互补性；每一步选择单位成本条件信息最高的 verifier，达不到阈值则停止或 abstain；监测依赖结构漂移并禁用偏好路由。

## 关键实验结果

【论文原文】35% 对称污染下 majority-5 的 balanced accuracy 从 0.6578 升到 0.7739，65% 污染时反而下降 0.1226。固定预算下 breadth、redundancy、adaptive 分别为 0.6048、0.6375、0.6538；VStress-CA 平均 3.4216 次调用，RLVR score 为 0.6417。条件边际增益从同模型重复到跨家族通道为 0.0126、0.0462、0.0913。

## 证据质量与局限

【论文原文】给出污染边界、成本匹配和依赖漂移防护，但摘要中的环境与真实生产 Judge 变化范围有限。【分析推断】sealed calibration 仍可能随模型 API 更新失效，需要版本锁定和持续漂移审计。

## 最接近的相关工作

Agreement Overstates Evidence、多 Judge 面板有效规模、Robust Conformal Consensus、Who Judges Matters、Calibration Is Not Verification。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier panel 视为相关通道而非票箱；输出选择路径、条件信息增益和 abstain 原因，并将其一起蒸馏给低成本 router。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：仅在新增 verifier 带来条件信息时更新分数，避免重复信号放大。
- **A/B/T 与序数分布**：T/INCONCLUSIVE 是正式停止结果；按依赖校正后的后验聚合 A/B。
- **硬真值门控**：clean oracle 只在账本冻结后接入，防止选择策略窥视真值。
- **critique states**：多 critique 若同源相关，不应被计为多份证据。
- **高熵探索**：高分歧且有互补通道时追加查询；只有相关重复时保留不确定性。
- **sealed eval**：直接采用其冻结控制器、成本账本与 dependence-shift alarm。
