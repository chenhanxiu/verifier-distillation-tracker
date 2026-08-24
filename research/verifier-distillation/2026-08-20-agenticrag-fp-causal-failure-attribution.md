# AgenticRAG-FP：带已知干预真值的 Agent 轨迹因果失败归因

- **论文标题**：When Failures Propagate: Causal Failure Attribution in Agentic Retrieval-Augmented Generation
- **作者**：Lauren Pothuru
- **首次公开日期**：2026-08-20
- **版本日期**：2026-08-20（v1）
- **arXiv ID**：2608.20627
- **原始论文**：https://arxiv.org/abs/2608.20627
- **DOI**：https://doi.org/10.48550/arXiv.2608.20627
- **代码链接**：论文页面未提供公开代码

## 一句话结论

后验轨迹证据会随错误向后传播而消失；通过在已知 hop 注入故障并重跑 suffix，AgenticRAG-FP 为“哪一步真正导致失败”提供了比 trace 观察更可信的因果真值。

## 真正新增的内容

**论文原文结论**：该基准在指定检索 hop 注入认证故障、重执行后续轨迹，并以已知干预位置评价诊断器；同时比较普通覆盖诊断与冻结 hop 的反事实探针。

**分析推断**：它给 score-level verifier distillation 提供了关键标签源：不是把最终失败均匀回传到每一步，而是用可重复干预判断某一步是否真正改变终局，尤其适合构造 A/B/T 与可恢复性标签。

## 核心方法

在多跳 Agentic RAG 中注入检索缺失或内容腐败，保留故障位置作为程序化真值，重新生成下游轨迹；诊断器需从改变后的 trace 找回根因。冻结 hop 反事实探针用受控替换隔离该步骤的因果作用。

## 关键实验结果

**论文原文**：在 80 个三跳 MuSiQue 问题的严格 Claude Haiku 4.5 sweep 中，coverage-based diagnosis 在 hop 1 为 0.91，但在 hop 2 和 3 均为 0。较小的内容腐败实验中，depth 2 的 18 个失败样本上覆盖诊断为 0，冻结 hop 反事实探针为 0.67；depth 3 仅 3 个失败样本，只能作描述性结果。

## 证据质量与局限

优点是有明确干预真值、重放和严格区分确认性与探索性结果。局限是单一作者、80 个问题、单一主要模型，深层样本极少；人工注入故障不代表自然错误分布，且 RAG 三跳仍短于许多 GUI/工作流 Agent。

## 最接近的相关工作

最接近 LongRCA Bench、TRACE、Not Every Divergence Should Be Suppressed、Wrong but Useful 和 DART-SD。区别在于 AgenticRAG-FP 直接持有故障注入位置，能区分相关轨迹信号与因果根因。

## 如何复用或推进 LLM-as-a-Verifier

建立可控错误注入库：替换工具结果、删去前置事实、修改参数或延迟副作用，并从同一 prefix 重放。用这些 sealed interventions 校准 Judge 的步骤贡献分数，训练 verifier 输出“致因、可恢复、无影响”三类概率，而不是仅预测最终成功。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：以干预造成的终局差值作为步骤分数教师，避免 outcome confounding。
- **pairwise A/B/T 与序数分布**：原始/故障/修复三个分支天然形成 A/B/T 与序数效用标签。
- **真值门控**：干预位置、执行日志和终态差异构成 teacher 的硬真值门控。
- **student-generated critique states**：student 可提出根因假设，再由冻结 hop 重放验证，而不是让 teacher 自证。
- **高熵探索**：若错误分支可被后续步骤修复，应标为可恢复并保留，不把局部异常等同于必败。
- **sealed eval**：将故障模板、注入位置和重放 seed 完全冻结并对训练不可见，专门审计 evaluator 的因果归因能力。
