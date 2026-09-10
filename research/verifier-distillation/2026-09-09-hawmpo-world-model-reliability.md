# HaWMPO：面向长时程机器人策略的世界模型幻觉感知优化

- **论文标题**：HaWMPO: Hallucination-Aware World Model-based Policy Optimization for Generalist Robot Policy
- **作者**：Zengjue Chen, Peidong Liu, Jiawei Li, Qi Wang
- **首次公开日期**：2026-09-09
- **版本日期**：2026-09-09（v1）
- **原始论文**：https://arxiv.org/abs/2609.09941
- **代码**：截至本次记录未发现公开代码

## 一句话结论

HaWMPO 训练 action-conditioned 模型估计世界模型生成轨迹的幻觉风险，并以 Reward-Soft 连续降权不可靠 action chunk，使虚拟 rollout 不再被当作等可信真值。

## 真正新增的内容

**论文原文结论**：方法不是简单过滤整条轨迹，而是按行动条件估计生成图像序列的可靠性，再把幻觉分数注入 GRPO reward；在 LIBERO 与真实 G1 机器人上均提升成功率。

**分析推断**：其结构可迁移为长 Agent 的 distributional verifier：把“轨迹质量”拆成任务进展与模拟/观察可信度，两者分别预测，避免错误世界模型或工具回执为 teacher 信号背书。

## 核心方法

VLA 在世界模型中生成闭环想象轨迹；Hallucination-Aware Model（HAM）结合行动与图像序列预测幻觉分数；Reward-Soft 按分数连续抑制对应 action chunk 的 GRPO 奖励。惩罚系数控制丢弃风险与保留有用但不完美虚拟经验的平衡。

## 关键实验结果

LIBERO 平均成功率：base 48.7、WMPO 56.8、WoVR 60.9、HaWMPO 63.7；相对 base +15.0、相对最强基线 +2.8。真实 G1 两项任务平均成功率从 67.5% 提至 80.0%。HAM 仅用 50 个标注 chunk 做独立审计，且最优惩罚强度随任务变化；Goal 任务在更强惩罚下达到 66.2%。

## 证据质量与局限

同时包含模拟、真实机器人和组件分析，方向证据较好。但 HAM 的监督由人工设计的特征差异、深度不一致和轨迹偏移构成，可能漏掉其他幻觉；独立可靠性评测只有 50 个 chunk；惩罚系数任务相关，尚无语言/工具 Agent 或 sealed evaluator 证据。

## 最接近的相关工作

WMPO、WoVR、世界模型可靠性估计、Speculative Uncertainty，以及以 reward confidence 调节策略更新的方法最接近。HaWMPO 的重点是 action-conditioned、chunk-level 的连续软门控。

## 如何复用或推进 LLM-as-a-Verifier

为 Agent 轨迹并行输出两套分布：任务价值分布与证据/环境模型可信度分布；最终 teacher 权重由二者组合。对生成式 critique，还应标注每项判断依赖真实工具回执、模拟状态还是模型推断。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：将 `value score × reliability weight` 与单一标量 teacher 对照。
- **A/B/T 与序数分布**：若两分支价值相近或可靠性区间重叠则保留 tie。
- **真值门控**：真实环境回放拥有最终否决权；世界模型只提供可折扣的密集信号。
- **critique states**：student critique 必须附证据来源与 hallucination/reliability 估计。
- **高熵探索**：软降权替代硬删，保留尚不可靠但可能有价值的分支。
- **sealed eval**：用未参与 HAM 训练的真实执行验证，并按轨迹长度报告可靠性校准漂移。
