# Generated Evaluation Suites as Diversity-Driven Search for Real Agent Regressions

- **作者**：Pulkit Yadav
- **首次公开日期**：2026-11-13
- **版本日期**：2026-11-13（v1）
- **原始论文**：https://arxiv.org/abs/2611.17632
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.17632；DOI: 10.48550/arXiv.2611.17632

## 一句话结论

【论文原文】生成式 Agent 评测若只汇总平均通过率，会把覆盖率上限与真实回归抵消掉；应把评测套件视为多样性搜索档案，按 descriptor cell 评分并公开覆盖。

## 真正新增的内容

【论文原文】论文把“根据 Agent 规范生成测试”形式化为在 `requirements × personas × scenario kinds` descriptor 空间中的搜索，并指出每个缺陷可影响的 trace footprint 决定其可检测上限。它用 7 个受控缺陷测试 suite-level mean、按 cell 评分与行为型覆盖的差异。

【分析推断】这直接影响 sealed eval：即使 evaluator 完全正确，测试生成器没覆盖缺陷 footprint，整体均值仍无法发现回归。OPD 实验因此不能只报告均值，应报告分叉/状态 cell 的覆盖与缺陷检出率。

## 核心方法

1. 将生成器输出保留为 descriptor-space archive，而非只保留均值。
2. 给受控缺陷追踪静态或行为 footprint，并计算其对大小为 N 的套件的最大可能贡献 `b/N`。
3. 比较 happy-path-only 与 scenario-kind-diverse 套件，按 cell 检测回归及反常改善。

## 关键实验结果

【论文原文】在两个领域的 tau²-bench Agent 中注入 7 个缺陷。5 个可追踪缺陷中有 4 个的覆盖上限不高于 0.10 检测阈值；工具移除缺陷破坏所有已覆盖场景时，suite-level pass rate 反而朝相反方向移动。固定套件规模下，纯 happy-path 套件未检出任何缺陷，而 scenario-kind-diverse 套件在 20 次抽样中有 5 次检出 orchestration defect。

## 证据质量与局限

【论文原文】受控缺陷和 footprint 上限给出清晰的因果诊断，且展示均值聚合的结构性盲点。

【分析推断】证据来自一个 Agent、两个领域和 7 个缺陷；descriptor 由生成器定义，仍可能遗漏未知失败轴。5/20 的检出率也说明多样性本身不足，需结合真实事故和隐藏任务持续扩充 sealed archive。

## 最接近的相关工作

最接近 AutoGym 的可验证任务生成、AutoTuneBench 的冻结测量、GameLogicBench 的确定性 oracle，以及 Harness or Model? 对 scaffold 混淆的控制。本文新增的是覆盖上限分析与 cell-level regression scoring。

## 如何复用或推进 LLM-as-a-Verifier

用 verifier 对每个 descriptor cell 输出独立分布和证据，而非对整个 suite 求一个分数；用真实受控缺陷校准各 cell 的灵敏度。生成式 verifier 只有在说明覆盖到哪个行为 footprint 时，其 critique 才进入训练集。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：按状态/缺陷 cell 分层归一化 score，避免大 cell 淹没稀有失败。
- **pairwise A/B/T 与序数分布**：在同一 cell 内构造 A/B；跨 cell 不可比或未覆盖时标 T。
- **环境真值门控**：用受控 defect injection 与可执行回归测试确定分数方向。
- **student-generated critique states**：critique 必须映射到 footprint 与 descriptor cell，无法定位者不作硬监督。
- **高熵探索**：用 archive coverage 分配分叉预算，优先补齐空 cell 而非重复高频路径。
- **sealed eval**：隐藏 defect、descriptor 映射和真实事故样本；报告 cell 覆盖、缺陷检出率及均值，防止 evaluator 共适应。

