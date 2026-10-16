# MRTPO：把每个可验证奖励只分配给相关 token

- **论文标题**：Each Reward to Its Relevant Tokens: Reward-Specific Token-Level Credit Assignment for Multi-Reward RL
- **作者**：Skylar Zhai, Haonan Wang, Zhining Liu, Linxin Song, Xuwei Ding, Jingcheng Liang, Jian Kang
- **首次公开日期**：2026-10-15
- **版本日期**：2026-10-15（v1）
- **原始论文**：https://arxiv.org/abs/2610.21439
- **项目页**：https://zhaihaotian.github.io/MRTPO/

## 一句话结论

MRTPO 通过“有/无某个 verifier 信息”的同轨迹重放分布差异，估计该奖励与每个 token 的相关性，从而避免把格式、正确性等局部 verifier 的优势均匀撒到整条响应。

## 真正新增的内容

**论文原文**：无需辅助模型或 token 标注，对每个奖励分别遮蔽其 verifier 信息并重放当前策略，用两次 next-token 分布的 Jensen–Shannon 距离作为 token relevance，再重新分配该奖励的 advantage。

**分析推断**：这为长轨迹多 verifier 系统提供了可执行的“奖励—步骤责任矩阵”，能把环境真值、格式约束、安全规则和 judge critique 分账，减少相互污染。

## 核心方法

在 reward-decoupled normalization 之后，对每个奖励构造反事实重放；按逐 token JSD 归一化该奖励的信用，使总 advantage 保持但只落在 verifier 真正影响的位置。

## 关键实验结果

**论文原文**：在 text-to-SQL、多约束 instruction following 和 tool calling 上，MRTPO 比所比较方法收敛更快、最终表现更好。摘要未提供具体绝对增益。

## 证据质量与局限

覆盖三个带可验证奖励的任务族且不依赖额外标注；但 relevance 是策略对 verifier 信息的敏感度，不等同于因果责任。若提示中泄露 verifier 或模型学会表面触发词，JSD 也可能被误导；长轨迹重放成本尚需验证。

## 最接近的相关工作

与 GDPO 的逐奖励归一化、BATON 的轨迹内/轨迹间双轴信用、UECR-GRPO 的熵重分配，以及 DRACO/RLDS 的分层步骤归因最接近。

## 如何复用或推进 LLM-as-a-Verifier

把每个 verifier 输出拆成独立通道：执行正确性、约束满足、证据质量、安全、风格。对每通道反事实移除其证据，得到 token/step relevance；只有环境真值通道可改变更新方向，软 judge 通道主要调节幅度。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：把 teacher 的 score shift 乘以 reward-specific relevance，而非对整条 trajectory 使用同一权重。
- **A/B/T 与序数分布**：每个评价轴独立产生 A/B/T 概率，再在相关步骤聚合，避免证据包装掩盖 outcome。
- **真值门控**：程序/环境 verifier 的 relevance 可作为硬门；LLM judge relevance 仅作软门。
- **critique states**：验证 critique 是否真的改变对应后续 token；无影响的 critique 不进入记忆。
- **高熵探索**：若多个 reward 通道指向不同步骤，保留分叉而非压成单一标量。
- **sealed eval**：用隐藏 verifier 定义和反事实扰动审计 relevance，防止模型记住训练期 verifier 表面形式。
