# SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning

- **作者**：Xinchen Du, Zhengze Zhou, Wenhui Zhu, Han Yu, Sen Na, Rohit Jain, Alborz Geramifard
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.00838
- **代码**：未发现公开代码链接

## 一句话结论

SHARPO 用每个环境交互段内的 teacher–student log-probability gap，对 GRPO trajectory advantage 做有界重加权，实现比 token 级更稳、比整轨迹更细的 Agent 信用分配。

## 真正新增的内容

【论文原文】长轨迹的单一终局回报难以定位局部错误。SHARPO 在 environment-facing segment 粒度计算 teacher–student gap，并把它变为有界 advantage multiplier；段内 token 共用权重、段间信用可以不同。

【分析推断】这与现有“下一步动作贡献度”最贴近：评估单位不必是单 token，也不必是整轨迹，而可对齐一次 thought-action-observation 交互段。

## 核心方法

沿 student on-policy 轨迹，对每个交互段汇总 teacher 与 student 的 log-prob gap；将该信号映射为 bounded multiplier，重加权该段全部 token 的 GRPO advantage。

## 关键实验结果

【论文原文】Qwen2.5-7B-Instruct 在 ALFWorld 与 WebShop 上超过 GRPO、SDAR、RLSD 和 StepOPSD；摘要未披露绝对增益。

## 证据质量与局限

有两个多轮 Agent 环境及多个强基线，但只验证一个 student 尺寸；teacher gap 未必等于真实动作贡献，摘要也未给校准、错误 teacher 或 sealed evaluator 结果。

## 最接近的相关工作

BATON、RLDS、Dr.Credit、GC-OPD、Dr. OPD、StepOPSD。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 对每个交互段输出目标推进、可恢复性和证据充分性分布，再与 teacher gap 分开消融：环境真值决定符号，verifier/teacher 只调幅度。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：把现有轨迹分数改为 segment multiplier，是最直接的新基线。
- **A/B/T 与序数分布**：同状态的候选 segment 可构成 A/B/T；差距不足时设 T。
- **硬真值门控**：环境状态变化先决定正负方向，log-prob gap 不得覆盖硬失败。
- **student-generated critique states**：critique 应绑定具体 segment，并以其后续 outcome 验证。
- **高熵分叉**：只在高熵且高影响 segment 增加分叉，避免全轨迹压平探索。
- **sealed eval**：冻结 teacher、grader、环境版本与 segment 切分规则。
