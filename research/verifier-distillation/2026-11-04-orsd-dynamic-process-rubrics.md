# Using Experience Twice：动态过程 Rubric 的特权 Token 信用分配

## 基本信息

- **作者**：Shumao Wu, Kongcheng Zhang, Jianqiang Huang, Baisheng Lai
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（v1）
- **原始论文**：https://arxiv.org/abs/2611.06543
- **DOI**：https://doi.org/10.48550/arXiv.2611.06543
- **代码**：https://github.com/AnnaXChun/ORSD

## 一句话结论

ORSD 从同组 on-policy 轨迹的行为差异中生成动态过程 rubric，由冻结 verifier 选出与真实成败最一致的 rubric，再用有/无 rubric 的 token likelihood gap 为 GRPO 提供稠密信用。

## 真正新增的内容

**论文原文结论**：同一批 Agent 经验既能用于 outcome RL，也能被提炼成自然语言过程监督；动态 rubric 可连接稀疏轨迹回报和 token-level credit。

**分析推断**：它是“程序/环境真值定方向、生成式 verifier 定局部幅度”的直接实现，但冻结 verifier 只保证训练期不漂移，不自动保证 rubric 正确或独立。

## 核心方法

- 当前策略在同一组轨迹上独立生成多组 candidate process rubrics。
- 冻结 verifier 评价每条轨迹对 rubric items 的满足情况。
- 选择 rubric satisfaction 与任务成功最对齐的 bundle。
- 把该 bundle 作为 privileged information，比较原始 token 在有/无 rubric 条件下的 log-likelihood。
- 将 likelihood gap 形成的 token credit 加到原 GRPO trajectory advantage。

## 关键实验结果

论文在 ALFWorld 与 WebShop、Qwen3-1.7B 与 Qwen3-4B 上报告：在相同环境交互预算下，ORSD 加速策略改进并提升最终任务表现。公开摘要未给出统一绝对提升数字，因此不补写未报告数值。

## 证据质量与局限

直接覆盖两个长轨迹 Agent 基准、两个模型规模，并公开代码，证据相关性较高。局限是 rubric 与 verifier 的错误可能被密集放大；摘要未说明跨环境迁移、verifier 校准和 sealed evaluator。bundle selection 依赖组内成败相关性，可能把偶然共现当因果信用。

## 最接近的相关工作

与 SCOPE、targeted guidance、process reward model、动态 rubric、OPSD 和 advantage shaping 最接近。区别是先从组内行为差异生成 rubric，再用 privileged likelihood gap 做 token credit。

## 如何复用或推进 LLM-as-a-Verifier

让 generative verifier 输出“rubric—证据指针—可证伪条件”，并用环境 counterfactual replay 验证 rubric 是否真的解释成败。把 rubric satisfaction 从二值扩展为序数分布，并保留无法判定项。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：直接加入 ORSD 作为“动态 rubric + token gap”基线。
- **A/B/T/序数分布**：rubric item 对同状态候选生成 A/B/T；证据不足为 T。
- **程序真值门控**：终局成功决定优势方向，局部测试/重放验证 rubric 信用。
- **critique states**：只蒸馏与任务成败对齐且可重放验证的 rubric。
- **高熵分叉**：同组轨迹应保持多种成功路径，避免 rubric 只奖励单一路径。
- **sealed eval**：训练中 verifier 冻结；最终再用不同模型族和环境 oracle 独立评估。
