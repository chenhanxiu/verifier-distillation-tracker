# TransHarness：从同任务成败对比演化可迁移的 Agent 干预策略

- **论文标题**：TransHarness: From Benchmark Overfitting to Transferable Harness Evolution
- **作者**：Tianze Xia, Zimo Wang, Heng Tong, Zhaoxiang Liu, Shiguo Lian, Fan Huang, Wenyu Liu, Yunchao Wei, Xinggang Wang
- **首次公开日期**：2026-11-25
- **版本日期**：2026-11-25（v1）
- **原始论文**：https://arxiv.org/abs/2611.33757
- **DOI**：https://doi.org/10.48550/arXiv.2611.33757
- **代码链接**：未见公开代码

## 一句话结论

TransHarness 从同任务成功—失败轨迹中学习“何时干预、如何诊断”，再经跨任务回放和独立语义选择过滤，降低 harness 对演化基准的过拟合。

## 真正新增的内容

**论文原文结论**：执行上下文触发器与诊断指导绑定后，可从 300 条分布外源轨迹迁移到新 benchmark。**分析推断**：其独立语义选择可作为 critique-state 的外部准入层，但仍需执行真值确认，不能只依赖另一个 Judge。

## 核心方法

从相同任务的成功/失败对比抽取干预政策；按当前任务证据触发检查和修正。通过 cross-task replay 排除源任务特定解，再由独立语义选择保留可泛化策略，并使用独立演化集和跨 benchmark 评测。

## 关键实验结果

使用测试分布外的 300 条源轨迹，DeepSWE v1.1 达到 76.4%，Terminal-Bench 2.1 达到 95.5%，分别超过最强基线模型 2.4 和 5.6 个百分点。

## 证据质量与局限

跨模型、跨 harness、跨 benchmark 验证优于仅在演化集报告结果。局限是提升可能仍受 benchmark grader 与 harness 实现影响；摘要未给出策略错误干预率和 sealed oracle 审计。

## 最接近的相关工作

与 Learning What vs. Learning How、Harness or Model?、SkillAA 和 Grounding Agent Memory 相关；区别是面向 harness intervention policy 的可迁移演化。

## 如何复用或推进 LLM-as-a-Verifier

把触发器分数、诊断类别和证据充分度分别蒸馏；程序测试决定是否允许干预，LLM verifier 只排序建议。A/B/T 对比应包含“无干预”分支以估计真实增量。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：将 student-generated critique 做成可回放 intervention policy，并以跨任务成功差作为 score-level OPD 目标；高熵分叉保留多个诊断。sealed eval 更换 benchmark、harness 和 grader，防止 evaluator 与干预策略共同过拟合。
