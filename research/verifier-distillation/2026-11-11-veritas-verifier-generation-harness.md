# Veritas: A Verifier Generation Harness for Agent Tasks

- **作者**：Daoan Zhang、Qinbo Bai、Dehai Min、Xingyu Mu、Ziyi Chen、Jianing Yin
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.13336
- **代码**：未发现公开代码链接
- **标识符**：arXiv:2611.13336

## 一句话结论

【论文原文】Veritas 通过显式 evidence header、领域规则库和可迭代的 verifier authoring principles 自动生成 Agent verifier，在固定模型下比七种通用 harness 更一致地复现官方执行判定。

## 真正新增的内容

【论文原文】多数 Agent verifier 依赖人工编写，难以覆盖没有现成 scorer 的任务。Veritas 把“可观察证据边界”“任务未明说的领域规则”和“如何写 verifier 的原则”变成 verifier 生成 harness 的一等组件，并允许 authoring principles 通过自改进循环更新。

## 核心方法

- evidence header 明确 verifier 可以观察哪些状态与证据。
- domain-rule library 补充任务描述未显式写出的约束。
- authoring principles 约束 verifier 的生成与修订。
- 先认证四个执行型 benchmark 的官方 verifier，再以其 verdict 作为对齐参照；另评测两个 pairwise benchmark。
- 固定被评模型，只比较 harness 产生的 verifier，减少 model 变化混淆。

## 关键实验结果

【论文原文】在四个 execution-scored benchmark 上，Veritas 生成的 verifier 与官方 verdict 的一致性均优于七种其他 harness；两个 pairwise benchmark 上达到或接近最佳。对三种其他模型家族中的两种，它也超过供应商自带 harness；三个 harness × 四个执行 benchmark 的 12 个组合中，其机制改善了 9 个。

## 证据质量与局限

【论文原文】固定模型、先认证官方 verifier 并跨多 harness/模型家族比较，实验设计较强。但“与官方 verdict 一致”不等于规格真实正确；自改进 verifier 若持续看同一测试集，也会形成 evaluator 共适应。摘要未给出绝对一致率、置信区间及生成 verifier 的安全审计成本。

## 最接近的相关工作

最接近 AutoGym、Ground-truth-as-code、GCAC、M4Bench 和 Closed-Loop Agent Evaluation。Veritas 的新增点是自动生成 verifier，而不是只设计任务或人工规定 scorer。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把 Veritas 生成的多个 verifier 视为 teacher panel，蒸馏其 A/B/T 与序数分布；但只在它们与执行真值一致、且对等义 evidence header 扰动稳定时训练 student。领域规则与 evidence header 应作为版本化 provenance 写入每个标签。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：自动产生多 verifier teacher，但先按执行真值校准后再聚合。
- **A/B/T 与序数分布**：pairwise harness 可直接生成 A/B/T；跨 verifier 分歧保留为分布而非多数票。
- **程序化/环境真值**：官方执行 verifier 只作为已认证锚点，不把 agreement 当作最终真理。
- **student-generated critique states**：critique 必须声明证据可见范围与所用领域规则。
- **高熵分叉**：利用多个 verifier 的分歧定位值得保留和复查的分叉。
- **sealed eval**：冻结 verifier 生成器、规则库和 authoring principles；最终评测使用未参与自改进的任务与独立 scorer。