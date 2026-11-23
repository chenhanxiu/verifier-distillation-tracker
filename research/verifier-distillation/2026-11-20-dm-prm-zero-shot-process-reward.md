# Decision Models Are General-Purpose Process Reward Models

- **作者**：Jiajun Fan、Qinglong Zheng、Ziwen Wang、Bangji Yang、Neil He、Ruihan Guo、Chaoran Cheng、Ge Liu
- **首次公开日期**：2026-11-20
- **当前版本日期**：2026-11-20（v1）
- **原始论文**：https://arxiv.org/abs/2611.27068
- **代码**：截至本记录未发现作者公开代码链接
- **标识符**：arXiv:2611.27068；DOI: 10.48550/arXiv.2611.27068

## 一句话结论

DM-PRM 无需步骤标签或微调，只把通用 decision model 对每一步的 Yes/No 概率标准化后加入优势，即能显著改善 ALFWorld 与 WebShop 的长轨迹信用分配；它是低成本 distributional process verifier 的直接基线。

## 真正新增的内容

**论文原文**：作者把通用概率式 decision model 直接用作零样本 PRM，每个环境只需一条问题文本；其逐步分数可为全失败 rollout 提供信号，并兼容 GRPO、GiGPO 和 GraphGPO。

**分析推断**：真正新意是“问出信用”而非训练 critic。输出概率天然适合保留序数/不确定性，但是否校准仍需独立真值审计，不能把概率大小当作可靠度证明。

## 核心方法

- 对轨迹每一步询问一个环境相关的 Yes/No 决策问题。
- 读取 decision model 的概率并在轨迹/组内标准化。
- 将该逐步信号加到原优势估计中，不改变底层策略梯度算法。
- 同一 decision model 跨 household、web shopping 和多种 RL 算法复用。

## 关键实验结果

**论文原文**：

- Qwen2.5-1.5B 上，GRPO 在 ALFWorld 提升超过 20 点，在 WebShop 提升超过 10 点。
- 在 ALFWorld 超过 GiGPO，并以更少迭代学到有效策略。
- 还能改善 GiGPO 与 GraphGPO，在两项基准取得对比方法中的最高成功率。
- 分数能定位失败 rollout 中的有用步骤；训练后空转动作减少、探索增加。

## 证据质量与局限

跨两个长轨迹环境和三种 RL 框架的结果较有说服力，并包含行为变化观察。局限是模型与环境范围仍窄，摘要未报告概率校准、反事实正确率、对抗性提示或 sealed set；Yes/No 问法可能把 rubric 设计偏差带入所有步骤。

## 最接近的相关工作

最接近 PRM、critic-based PPO、GiGPO/HGPO/GraphGPO、FARM 的失败概率读出与 RLC-DR 的 calibrated decision rewards。与训练型 PRM 不同，DM-PRM 直接复用通用 decision model。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：将 Yes/No 概率扩展为 A/B/T 或五级序数分布，并对同一步使用反向问题、证据隐藏和环境回放校准。可把 decision model 作为廉价第一层，只有高熵或与环境真值冲突的状态才升级到生成式 verifier。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：直接蒸馏逐状态概率分布，而非只蒸馏采样 token 的 teacher logit。
- **A/B/T 与序数分布**：保留 Yes/No 之外的 T；用熵而非单一阈值决定权重。
- **真值门控**：环境成功、非法动作和状态断言为硬层，decision model 仅补充稠密信用。
- **critique states**：要求 decision 问题及证据指针随 critique 一起存储，便于重放审计。
- **高熵探索**：高熵且价值斜率大的步骤应增加分叉，低熵才允许剪枝。
- **sealed eval**：冻结独立问题模板、模型快照和环境集，防止 policy 学会迎合同一 decision model。