# AttnSR: Attention Step Reward for Long-Horizon Agentic RL

- **作者**：Mengsong Wu, Tianchen Zhou, Zhaochen Su, Zhenhua Liu, Zhe Cui, Aimin Zhou
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.07932
- **DOI**：https://doi.org/10.48550/arXiv.2611.07932
- **代码**：https://github.com/fairyshine/AttnSR

## 一句话结论

AttnSR 不训练额外 reward model，而是从 policy replay 的注意力图反向分配终局奖励，在长时程 Agent 上提高成功率并减少环境交互。

## 真正新增的内容

它把 policy 自身的 attention 当作步骤相关性先验，提供一种无需额外 rollout 或独立 RM 的 step-level credit augmentation；重点不是增加总奖励，而是决定终局信号应落在哪些历史步骤。

## 核心方法

训练 replay 时沿 policy attention graph 向前序步骤回溯，估计各步骤对最终响应的相关性。终局步骤相对 running baseline 的正负决定这些中间步骤被强化还是惩罚；所得 step reward 与原 PPO 目标结合。

## 关键实验结果

- Qwen2.5-7B-Instruct 在 ALFWorld held-out success 从 **91.2% 提升至 97.1%**。
- 在所有检查点均优于 PPO baseline。
- ScienceWorld 各检查点均改善，同时环境交互减少 **29.9%**。
- 消融显示收益来自中间奖励的分配方式，而非简单累加步骤奖励。

## 证据质量与局限

**论文原文结论**：覆盖两个长时程环境并有 credit-assignment 消融，代码公开。  
**局限**：注意力不等价于因果贡献；实验集中于单一 7B policy 和 PPO；未与强 PRM、反事实分叉 verifier 或 sealed evaluator 直接比较。

## 最接近的相关工作

最接近的是 process reward model、trajectory credit assignment、BATON、RLDS、RECAP、γOPD，以及 attention rollout / attribution 方法。

## 如何复用或推进 LLM-as-a-Verifier

把 attention relevance 仅作为**幅度先验**，把程序化/环境终局真值作为符号与总信用约束；再由 distributional verifier 输出步骤风险分布，而不是直接把 attention 当正确性证据。可将高 attention、低 verifier 一致性的步骤优先送入 critique 生成与局部重放。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 可把终局 teacher score 按 attention 分摊到步骤，但必须保持轨迹总信用守恒。
2. 对 pairwise A/B/T，应在共享前缀后比较 attention-attributed 关键步骤；若归因不稳定则标 T。
3. student-generated critique states 可优先取 attention 高且环境失败后的首个分歧步骤。
4. 高熵探索不能被 attention 权重单独压制；建议与策略熵、反事实边际贡献联合门控。
5. sealed eval 中加入 attention shuffle、causal intervention 与跨模型 attention transfer，检查是否只是架构特定相关性。