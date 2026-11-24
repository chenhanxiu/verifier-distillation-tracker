# From Rewarding What Models Say to How They Think: Attention Process Reward Model for LLM Reinforcement Learning

- **作者**：Kairong Han, Nuanqiao Shan, Ziyu Zhao, Xinpeng Dong, Zijing Hu, Dian Jin, Leyan Deng, Junjian Ye, Lujia Pan, Fei Wu, Kun Kuang
- **首次公开日期**：2026-11-24
- **版本日期**：2026-11-24（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.30627
- **DOI**：https://doi.org/10.48550/arXiv.2611.30627
- **代码**：未见作者在 arXiv 摘要页给出独立代码链接

## 一句话结论

一个约 46M 参数、读取 hidden state 与 attention map 的过程奖励模型，可用 ranking 与 counterfactual 目标学习内部推理质量，并通过周期更新适应 RL 分布漂移。

## 真正新增的内容

**论文原文结论**：指出 textual reward aliasing，提出 APRM 对“内部如何思考”而非仅文本轨迹评分，并在 RL 中周期更新。  
**分析推断**：内部信号可作为独立 verifier 通道，但若与 policy 联合更新，仍可能产生隐式共适应，因此不能替代 sealed outcome。

## 核心方法

从 hidden states 与 attention maps 提取过程特征；以排序和反事实目标训练轻量 APRM；将其奖励接入代表性 RL 方法，并周期性刷新以应对 on-policy distribution shift。

## 关键实验结果

APRM 约 46M 参数；接入多种 RL 方法后，平均 pass@8 提升 2.88%。摘要未给逐任务结果、置信区间或内部信号可解释性审计。

## 证据质量与局限

轻量、跨 RL 方法且包含反事实目标是优点。局限是内部状态仅对同/兼容架构可用，attention 不等于因果解释；周期更新可能让 reward model 与 policy 共漂移，且未报告长时程 Agent 轨迹。

## 最接近的相关工作

最接近 representation monitor reward hacking、FARM 的冻结状态读取、DM-PRM 的分布式过程奖励，以及 GLARE 的 on-policy reward estimator 更新。

## 如何复用或推进 LLM-as-a-Verifier

把 APRM 当作第三通道：环境真值负责 hard gate，外部 LLM verifier 负责语义 critique，内部 APRM 负责早期风险与相对排序；三者分开校准，不把内部分数直接解释为真值概率。

## 对 Agent verifier × OPD 实验路线的具体影响

可在长轨迹每个决策点蒸馏 internal process score，并与 pairwise A/B/T 联合训练；高熵分叉时优先保留内部 verifier 与外部 verifier 分歧的分支。训练中可周期更新 APRM，但 sealed eval 固定其快照，并另用环境终局和未见任务检测 evaluator 共适应。