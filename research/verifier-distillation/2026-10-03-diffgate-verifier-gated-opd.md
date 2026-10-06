# DiffGate: Difficulty-Gated Teacher Guidance for On-Policy Distillation

- 作者：Karn Tiwari、Varnith Chordia、Prathosh A P
- 首次公开日期：2026-10-03
- 当前版本日期：2026-10-03（v1）
- arXiv：2610.04596
- 原始论文：https://arxiv.org/abs/2610.04596
- Canonical URL：https://doi.org/10.48550/arXiv.2610.04596
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】DiffGate 让 verifier 决定哪些失败轨迹需要 teacher，teacher 只在这些轨迹内提供有界的密集 token 更新，从而结合 RLVR 的结果方向与 OPD 的局部信用。

## 真正新增的内容

【论文原文】teacher guidance 仅施加于失败轨迹，按 group difficulty 缩放，并对过大 teacher–student gap 平滑限幅；它明确把“是否更新”交给 verifier，把“如何更新”交给 teacher。

## 核心方法

【论文原文】以 GRPO 为基础，对 all-failure/困难组引入选择性 OPD；结果奖励提供轨迹级门控，teacher 分布提供 token 方向，bounded gate 防止极端差异主导梯度。

## 关键实验结果

【论文原文】Qwen3-0.6B/1.7B 上，代码 avg@8 比匹配 GRPO 高 1.7/1.8 点，pass@8 高 1.6/5.7 点；数学 avg@8 与 GRPO 差距不超过 0.5 点，pass@8 高 1.1/3.9 点。四个模型×领域设置的 pass@8 均改善。

## 证据质量与局限

【论文原文】结果同时报告平均与覆盖指标，并跨两尺度两领域。局限是“失败”来自可验证答案，开放式 Agent 的失败定义更噪；teacher 仍可能在失败前缀上给错方向；group difficulty 依赖 rollout 数量。

## 最接近的相关工作

最接近 VG-OPD、UECR-GRPO、DCSD、SIGNBALANCE，以及“硬真值定方向、软 teacher 定幅度”的既有路线。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】这是最直接的 Agent verifier × OPD 基线：环境终局判定是否开放 teacher loss，distributional verifier 决定幅度，teacher 只分配失败轨迹内部信用。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：【分析推断】实现 outcome gate × bounded score weight × token KL 的三因子目标。
- **A/B/T 与序数分布**：【分析推断】失败组内部用 A/B/T；未结算轨迹不得当作失败。
- **硬真值门控**：【分析推断】硬真值决定 teacher loss 的开关与符号。
- **critique states**：【分析推断】只为被门控失败轨迹生成 critique，并验证修复。
- **高熵探索**：【分析推断】以 pass@K 为主指标，避免 avg 提升但覆盖下降。
- **sealed eval**：【分析推断】冻结 verifier 与隐藏测试，单独审计 teacher 在失败前缀上的错误率。
