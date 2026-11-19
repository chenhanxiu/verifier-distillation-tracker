# VESPA: Verifiable Symbolic Policy Adaptation for Safe Reinforcement Learning

- **作者**：Paul König、Sascha Marton、Stefan Lüdtke、Christian Bartelt
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：https://arxiv.org/abs/2611.24083
- **代码链接**：https://anonymous.4open.science/r/VESPA-Submission/
- **标识符**：arXiv:2611.24083；DOI: 10.48550/arXiv.2611.24083

## 一句话结论

【论文原文】正式 verifier 不只给 pass/fail，还能把反例变成定向训练数据；VESPA 用验证反例局部微调决策树策略，比反复从头训练更快获得可证明安全的 policy。

## 真正新增的内容

【论文原文】提出 verification→counterexample→targeted fine-tuning 的闭环：当策略违反安全约束时，形式验证器返回导致违例的状态/路径，训练只针对这些脆弱区域调整现有决策树，而非丢弃整个 policy。

## 核心方法

1. 对策略与安全约束做形式验证。
2. 收集验证器产生的 counterexample traces。
3. 在反例状态上做定向 policy adaptation，并再次验证。
4. 与不使用反例的重复训练/验证循环比较收敛速度。

## 关键实验结果

【论文原文】CartPole 上 verified safe steps 均值从 63.8 提至至少 92.7，两轮达到无反例循环十轮的水平；MountainCarContinuous 上 60 次运行中有 53 次把 unsafe policy 转为 safe policy。

## 证据质量与局限

【论文原文】验证器给出硬安全证据，并有迭代效率对照；但实验是小型控制任务和可解释决策树，未验证 LLM/长文本 Agent。形式安全只覆盖声明约束，specification gap 仍在。

## 最接近的相关工作

接近 counterexample-guided inductive synthesis、CEGAR、RL from verifier feedback、formal runtime monitor、MAGS/ContrAgent。其价值在于把 verifier 反例直接作为训练信号。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把程序化/环境 verifier 失败转成最小反例轨迹和局部 obligation，作为 verifier student 的 hard-negative 与 Agent OPD 的脆弱状态；生成式 verifier 负责解释和扩展邻域，但不能修改硬标签。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：对反例邻域提高硬真值权重，普通状态保持低权或不更新。
- **pairwise A/B/T 与序数分布**：反例路径与最小修复路径构成 A/B；多种安全修复可标 T。
- **程序化/环境真值门控**：形式反例决定更新方向，是不可由 LLM teacher 覆盖的硬门。
- **student-generated critique states**：critique 必须能映射到反例中的具体违例条件，并由重新验证闭环确认。
- **高熵分叉探索**：在反例状态周围展开多个安全修复分支，而非全局压低熵。
- **sealed eval**：使用隐藏安全约束与未见 counterexample family，防止仅记忆公开反例。
