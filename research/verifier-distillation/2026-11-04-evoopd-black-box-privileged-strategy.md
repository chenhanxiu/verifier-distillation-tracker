# EvoOPD：面向黑盒 On-Policy Distillation 的特权信息策略演化

## 基本信息

- **论文标题**：EvoOPD: Evolving Privileged Information Strategies for Black-Box On-Policy Distillation
- **作者**：Ximo Zhu, Ruiqi Liu, Yi Han, Zhengan Wu, Gengsheng Li, ZiAn Wang, Zhu Yuantian, Jin Jiang, Wenhao Wang
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（v1）
- **原始论文**：https://arxiv.org/abs/2611.06542
- **DOI**：https://doi.org/10.48550/arXiv.2611.06542
- **代码**：未见公开代码链接

## 一句话结论

EvoOPD 将“向黑盒 teacher 请求什么反馈”本身变成随 student 状态演化的优化问题，再通过 PI-conditioned privileged teacher 把文本反馈转成 student 自有轨迹上的密集监督。

## 真正新增的内容

**论文原文结论**：固定的 privileged-information（PI）请求策略无法在整个蒸馏过程中持续最优；最有效的关注位置、信息类型和粒度会随 student 能力变化。EvoOPD 用当前 student 上的 repair utility 更新 PI Strategy Bank。

**分析推断**：这把 verifier/critique teacher 从固定提示器升级为可学习的监督采集策略，直接适用于长轨迹中“何时问、问哪一步、要证据还是修复”的预算分配。

## 核心方法

- 黑盒模型只提供文本反馈，不需要 logits。
- 维护 PI Strategy Bank，策略控制反馈焦点、信息类型与细节粒度。
- 以 PI 对当前 student 输出的实际 repair utility 评价并演化策略。
- 由可访问 logits 的 PI-conditioned privileged teacher 将反馈映射为 student on-policy 轨迹上的密集蒸馏信号。

## 关键实验结果

- 覆盖数学推理、代码生成及 Qwen3-1.7B/4B/8B 六个 model-task 设置。
- 六个设置总体表现均最佳。
- 相对各设置最强基线，数学平均提高 **2.14 个百分点**，代码平均提高 **1.30 个百分点**。
- 分析显示 PI 策略的相对有效性确实随 student 状态改变。

## 证据质量与局限

优点是跨任务、跨规模，并把动态策略假设直接做了分析。局限是没有长时程 Agent 环境、工具副作用与独立 sealed eval；repair utility 若由同一评价链产生，仍可能与 student 共适应。文本 teacher 的成本和偏差传播也需单独审计。

## 最接近的相关工作

最接近黑盒知识蒸馏、OPD/OPSD、privileged-context distillation、主动教师查询和 adaptive teacher routing。相较固定 critique prompt，它优化的是“监督采集协议”。

## 如何复用或推进 LLM-as-a-Verifier

把 PI Strategy Bank 改为 verifier query bank：错误定位、证据请求、反事实后果、局部修复、置信分布。以环境重放后的净修复收益更新策略，而非用 Judge 自评分；输出同时保留 ordinal distribution 与 abstain。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：联合学习 teacher query 与蒸馏强度，比较固定 rubric、能力分段 rubric、在线演化 rubric。
- **A/B/T 与序数分布**：不同 PI 策略分别产生分布，策略间冲突标 T，不提前平均。
- **程序/环境真值**：repair utility 必须由测试、环境重放或外部 oracle 结算。
- **student-generated critique states**：用实际修复收益做准入，避免“看起来详细”的 critique 被偏好。
- **高熵分叉**：高分歧状态优先查询多种 PI，而非只调用单一 teacher。
- **sealed eval**：冻结独立任务与 query 模板，验证策略库没有过拟合训练 evaluator。
