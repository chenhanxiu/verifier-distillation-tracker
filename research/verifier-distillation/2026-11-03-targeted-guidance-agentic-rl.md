# Stabilizing On-Policy Targeted Guidance in Agentic Reinforcement Learning

## 基本信息

- **作者**：Kevin Frans, Alexander M. Rush, Sergey Levine, Pieter Abbeel, Ashvin Nair
- **首次公开日期**：2026-11-03
- **版本日期**：2026-11-03（v1）
- **原始论文**：https://arxiv.org/abs/2611.05266
- **DOI**：https://doi.org/10.48550/arXiv.2611.05266
- **代码**：未见公开代码链接

## 一句话结论

在多轮软件工程 Agent 中，把逐回合文本反馈作为 on-policy self-distillation 信号，并只在策略确实失败的回合触发，再与逐准则 RL 奖励结合，可在不牺牲基础 RL 的前提下稳定优化原本难学的行为。

## 真正新增的内容

**论文原文结论**：作者提出 targeted guidance 框架，重点不是简单加入 critique，而是研究如何在整个 Agent RL 训练过程中保持熵稳定、避免振荡，并发现“失败回合定向反馈 + per-criteria reward”最有效。

**分析推断**：这是目前最贴近“student-generated trajectory 上的 verifier/critique 蒸馏”的直接原型之一；它支持让硬奖励决定是否介入、文本 teacher 决定更新方向，而非对所有状态无差别蒸馏。

## 核心方法

- 由当前策略采样多轮 Agent 轨迹。
- 对每回合产生富文本、逐准则反馈。
- 将反馈转化为 on-policy self-distillation 目标。
- 仅在某项准则失败的回合注入针对性 guidance。
- 与逐准则 RL reward 联合训练，并审计训练熵和振荡。

## 关键实验结果

论文在多轮软件工程环境的多种设置中报告：targeted self-distillation 与 per-criteria RL reward 联合使用优于单独信号；只在失败回合提供反馈能够稳定训练熵并减少振荡。摘要未披露统一的绝对提升数值，因此此处不推断未报告数字。

## 证据质量与局限

优点是直接在 agentic、多轮、on-policy RL 场景验证，并关注训练动态。局限是公开摘要没有给出任务规模、绝对成功率和成本；环境集中于软件工程，文本反馈本身的正确性与独立性仍需检查。

## 最接近的相关工作

与 OPSD、process reward model、critique-guided RL、失败回合课程学习及 STRIDE 式首错定位最接近。区别是它将逐准则文本反馈直接纳入 on-policy 蒸馏，并显式研究稳定性。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier 输出拆为：可验证准则、失败证据指针、局部 critique 和置信分布。只有环境真值或独立检查确认失败后，才将相应 critique 蒸馏给 student；成功但高不确定性的状态保留为探索样本。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：新增“全状态蒸馏 vs 失败门控蒸馏 vs 置信门控蒸馏”主消融。
- **A/B/T 与序数分布**：按每项准则输出分布，失败证据不足时标 T，不把总回报强拆成伪标签。
- **程序/环境真值**：用测试、工具返回值或状态断言决定 guidance 是否可启用。
- **critique states**：只接受带证据定位与局部编辑范围的 critique。
- **高熵分叉**：控制蒸馏强度，避免 guidance 把策略熵压塌；持续记录熵与分叉覆盖率。
- **sealed eval**：冻结外部评测器与准则，防止训练中 feedback model 与策略共同适应。
