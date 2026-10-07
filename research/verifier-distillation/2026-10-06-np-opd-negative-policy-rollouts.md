# On-Policy Distillation with Negative-Policy Rollouts

- 作者：Jaehui Hwang、Dongyoon Han、Sangdoo Yun、Byeongho Heo
- 首次公开日期：2026-10-06
- 版本日期：2026-10-06（v1）
- 原始论文：https://arxiv.org/abs/2610.07874
- Canonical URL：https://arxiv.org/abs/2610.07874
- 代码：https://github.com/naver-ai/np-opd

## 一句话结论

【论文原文】NP-OPD 用较弱负策略的 rollout 持续暴露“负策略偏好而 teacher 不偏好”的 token，弥补 teacher 与 student 分布重叠不足时仅靠正向模仿的稀薄信号。

## 真正新增的内容

【论文原文】不改 distillation reward，而在 rollout policy 处引入低能力 negative policy；这使负行为在训练中持续出现并接受 teacher 监督，从而形成显式远离负策略的信号。

## 核心方法

【论文原文】混合 student on-policy 与 negative-policy rollout，仍用正 teacher 进行 token-level OPD；重点追踪并压低 negative policy 相对 teacher 更偏好的 token，同时保持标准 OPD 正监督。

## 关键实验结果

【论文原文】在不同模型规模、生成模式、推理领域和多种 OPD 变体上均改善基线；分析显示 student 对负策略偏好 token 的概率被抑制，整体分布远离负策略。摘要未提供统一绝对增益，需以正文各设置为准。

## 证据质量与局限

【论文原文】覆盖多个规模、领域与 OPD 变体，并有机制分析。【分析推断】负策略的选择本身是强先验；若其“坏行为”与可接受少数策略重叠，会误伤探索。推理任务结果尚不能直接证明 Agent 长轨迹安全收益。

## 最接近的相关工作

【分析推断】接近对比式自蒸馏、OPD-Aha、DDO 与一般 negative sampling；差异是负样本由独立较弱策略在 rollout 层持续产生。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把历史失败 Agent 或已知 reward-hacking policy 作为负策略，让 verifier student 同时学习“靠近有真值支持的 teacher 分布”和“远离失败分布”；负信号最好由环境失败证书确认。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：增加 positive-only、negative-only、双向 rollout 三组。
- 【分析推断】A/B/T：negative policy 生成 B，但证据不足的差异保留 T。
- 【分析推断】真值门控：只有环境确认失败的负轨迹才能提供方向信号。
- 【分析推断】critique states：收集负策略 critique 作为 hard negative，并要求证据指针。
- 【分析推断】高熵分叉：限制负样本权重，避免把新颖但正确策略当坏策略清除。
- 【分析推断】sealed eval：在未见负策略和未见攻击模式上评估，防止只学会策略指纹。