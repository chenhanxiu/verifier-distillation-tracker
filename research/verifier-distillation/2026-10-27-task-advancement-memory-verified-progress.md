# Task Advancement Memory：把可验证进展变成长轨迹状态与监督

- **论文标题**：From Interaction to Capability: Task Advancement as State and Supervision for GUI Agents
- **作者**：Ziyang Chen, Qian Li, Chengwei Qin
- **首次公开日期**：2026-10-27
- **版本日期**：2026-10-27（v1）
- **原始论文**：https://arxiv.org/abs/2610.37482
- **代码链接**：未在论文首页给出
- **标识**：arXiv:2610.37482；DOI: 10.48550/arXiv.2610.37482

## 一句话结论

长轨迹监督不应只看整题成败；把“已由环境验证的局部进展”抽成状态与可复用操作，能从失败任务中保留正确片段。

## 真正新增的内容

**论文原文结论**：Task Advancement Memory（TAM）用 Task Advancement State 表示已验证进展如何改变剩余目标，并在任务后提取产生局部可验证结果的交互，保留输入、预期输出和验证条件之间的关系。

**分析推断**：这为 Agent verifier 提供了比逐步分数更稳健的监督粒度：以“进展事件”而不是单动作或终局 outcome 作为信用单元。

## 核心方法

执行时维护已完成且已验证的局部目标及剩余义务；任务结束后，从成功或失败轨迹中抽取产生局部成功的操作，并将验证条件随技能一起保存，供后续跨应用任务复用。

## 关键实验结果

在 MobileWorld GUI-only 上，仅 Advancement State 就把成功率从 12.0% 提升到 28.2%；完整 TAM 相对最强基线任务成功率提高 17.6%，每个已解决任务的生命周期 token 降低 38.7%；在 SPA-Bench 单应用英文 Level 3 达到 SOTA。

## 证据质量与局限

优点是同时覆盖持续执行与任务后学习，并报告效率指标。局限是摘要没有给出验证器错误率、局部进展的人工一致性或对错误验证条件的压力测试；GUI 域结果也不能直接外推到代码、网页或开放世界 Agent。

## 最接近的相关工作

最接近 DynSTEER 的阶段级评估、DENSE 的带证据轨迹压缩、SkillAA/RSIAgent 的验证后记忆写入，以及 BATON/RLDS 的分层信用分配。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier 输出从单一轨迹分改为事件账本：每项包含 claim、环境证据、验证条件、适用范围、剩余义务与置信分布。Generative verifier 只解释事件间因果，硬 verifier 负责确认局部结果。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：在进展事件边界蒸馏 score，而非把终局回报均匀传播到全部 token。
- **A/B/T 与序数分布**：比较两个分支新增的“已验证进展集合”；证据不可比时输出 T。
- **程序化/环境真值门控**：将验证条件与技能绑定，缺少可执行确认时不得把局部成功写成硬标签。
- **student-generated critique states**：critique 必须引用具体进展事件与未完成义务，验真后才进入 memory。
- **高熵分叉与探索**：保留产生不同合法局部进展的分支，避免只保留单一路径。
- **sealed eval**：冻结隐藏任务及独立事件检查器，分别测局部进展 precision、终局成功与生命周期成本。