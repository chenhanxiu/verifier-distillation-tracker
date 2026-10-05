# OPD Before RL: Warm-Starting Rubric-Based RL with On-Policy Distillation

- 作者：Xinpeng Wang、Wei Shi、Yu-Chia Chen、Maria Zontak、Yun He、Richard Yuanzhe Pang
- 首次公开日期：2026-10-02
- 当前版本日期：2026-10-02（v1）
- arXiv：2610.02781
- 原始论文：https://arxiv.org/abs/2610.02781
- Canonical URL：https://doi.org/10.48550/arXiv.2610.02781
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】先用 rubric 作为 teacher 的 privileged context 做 token-level OPD，再用同一 rubric reward 做 RL，优于直接 SFT/RL 组合，并减少“声称满足 rubric 却未提供内容”的 reward hacking。

## 真正新增的内容

【论文原文】RP-OPD 让无 rubric 的 student 在自身生成前缀上匹配 rubric-aware teacher 的 next-token 分布；当蒸馏到达平台期后，再由 rubric-based RL 直接优化完整响应得分，实现密集信用与最终目标优化的两阶段衔接。

## 核心方法

【论文原文】阶段一在 student-generated prefixes 上做 privileged-context OPD；阶段二继续做 rubric RL。作者系统改变进入 RL 前的 SFT 或 RP-OPD 训练量，比较不同 warm start。

## 关键实验结果

【论文原文】在 HealthBench、ResearchQA、RubricHub Science 的开放权重模型实验中，两阶段 RP-OPD + RL 获得所比较方法中的最高分。RubricHub Science 上，该组合只显示有限 reward hacking，而 SFT + RL 越来越多通过“自称合规”获得高 reward 却缺失必要内容。

## 证据质量与局限

【论文原文】优点是跨三个开放式 rubric 任务、对训练阶段和 warm-start 数量进行比较。局限是 rubric 既作为 privileged teacher context 又作为 RL reward，训练信号相关性很高；“有限 hacking”不等于无 hacking；缺少与程序真值相同强度的独立正确性 oracle，不能把 rubric 得分视为真实任务成功。

## 最接近的相关工作

最接近 Beyond Solver Verdicts 的 oracle-to-generative reward、UniRRM 的多协议 reward、GLARE 的 on-policy reward estimator，以及“RL Starts before RL”对 OPD→RL 阶段效应的分析。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可将 rubric-aware teacher 蒸馏成 score-level verifier warm start，再用少量环境真值做第二阶段校准；关键是拆开“内容是否满足要求”与“回答是否宣称满足要求”两个头。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level on-policy verifier distillation**：【分析推断】先蒸馏 rubric 条件的序数分数分布，再用真实 task success 做轻量 RL/校准，直接形成两阶段基线。
- **pairwise A/B/T 与序数评分分布**：【分析推断】按 rubric 维度保留分布，不把总分压成单一标签；差距小于校准阈值时标 T。
- **程序化/环境真值门控**：【分析推断】rubric 只能决定软幅度，环境测试必须决定方向并否决“口头合规”。
- **student-generated critique states**：【分析推断】critique 应引用具体缺失项与证据，禁止把“我已满足”本身作为正信号。
- **高熵分叉下保留探索**：【分析推断】RP-OPD 只在 rubric 高置信维度收缩，歧义维度保留多候选并延后到 RL/环境结算。
- **独立 sealed eval**：【分析推断】冻结隐藏 rubric、人工/程序验真和反“自称合规”测试；评测器不得与训练 teacher 同源。
