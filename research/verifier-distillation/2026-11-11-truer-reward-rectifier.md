# TRUER: Test-Time Reward Correction Using an Error-Aware Rectifier for Reinforcement Learning

- **作者**：Mingxiang Shen、Jinhao Li、Jiaming Xu、Yibo Han、Guohao Dai、Yijia Zhang、Ningyi Xu
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.13714
- **代码**：未发现公开代码链接
- **标识符**：arXiv:2611.13714

## 一句话结论

【论文原文】多数票在 test-time RL 中会把“错误多数”当成正确奖励；TRUER 用少量有标签源数据训练并冻结 reward rectifier，专门纠正错误多数和正确少数。

## 真正新增的内容

【论文原文】训练审计发现 reward error 以 false positive——错误答案获得正奖励——为主。论文不要求大规模目标域真值，而是用有限源域标签学习“共识与正确性何时分离”，再把 rectifier 固定用于后续 test-time adaptation。

## 核心方法

- 从少量有真值的数据构造 consensus 与 correctness 冲突样本。
- 重点训练 incorrect-majority 与 correct-minority 两类难例。
- 冻结 error-aware rectifier，避免与正在适配的 policy 同步漂移。
- 在 test-time RL 中先修正自生成 reward，再更新模型。

## 关键实验结果

【论文原文】在所有已评配置上，TRUER 的 reward accuracy 与最终模型性能均稳定超过 naive test-time RL。公开摘要没有给出绝对分数、标签预算、跨域距离或统计区间，因此无法判断收益规模和样本效率。

## 证据质量与局限

【论文原文】方法针对经过审计确认的主要错误类型，并明确冻结 rectifier，设计上降低 evaluator 共适应。但源域标签能否覆盖目标域的新型错误是核心假设；多数/少数结构也不直接等同于多轮 Agent 环境中的可执行真值。

## 最接近的相关工作

最接近 Coupled Calibration and Learning、Calibration Is Not Verification、Robust Conformal Consensus 与多 Judge 有效规模研究。TRUER 的重点是使用少量真值纠正 consensus reward，而不是重新训练整个 reward model。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可将 rectifier 输入扩展为完整 ordinal reward distribution、panel disagreement 和环境证据；输出不只做二元翻转，还包括 A/B/T/abstain 的校正概率。对新域无证据时应提高 T，而非沿用源域过度自信。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：先由冻结 rectifier 修正 teacher score，再蒸馏 student。
- **A/B/T 与序数分布**：错误多数、正确少数应成为专门的校准切片。
- **程序化/环境真值**：有限真值用于训练方向纠偏，不用来假装覆盖全部目标域。
- **student-generated critique states**：只有经 rectifier 与证据一致性检查的 critique 获得正权重。
- **高熵分叉**：少数分支不能因投票失败而删除；高分歧状态保留并送强 verifier。
- **sealed eval**：rectifier 训练集与最终评测题严格隔离，冻结后再测试跨域。