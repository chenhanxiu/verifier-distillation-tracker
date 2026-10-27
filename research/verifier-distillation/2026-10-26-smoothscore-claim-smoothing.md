# SmoothScore：量化 Research Agent 的证据平滑

## 基本信息

- **论文标题**：Quantifying Claim Smoothing by LLM Research Agents
- **作者**：Tiasa Singha Roy, Manya Wadhwa, Greg Durrett
- **首次公开日期**：2026-10-26
- **版本日期**：2026-10-26（v1）
- **论文链接**：https://arxiv.org/abs/2610.35793
- **代码链接**：https://github.com/tiasa2/SmoothScore

## 一句话结论

长报告 Agent 会把相互冲突、边界不齐的证据“抹平”为过强结论；SmoothScore 在 claim 层面对证据检索、聚类和支持强度分账。

## 真正新增的内容

**论文原文结论**：先抽取报告中的关键结论性 claim，再检索相关证据、按高层 aspect 聚类，最后比较 claim 强度与证据可支持范围，量化 smoothing。

**分析推断**：长轨迹 verifier 不应只检查引用是否存在或最后答案是否流畅，还要保留证据分歧分布。把多源 evidence 压成一个总分，会丢掉恰好需要由 T/INCONCLUSIVE 表示的“锯齿”。

## 核心方法

1. 从研究报告抽取关键 claim。
2. 对每条 claim 找到相关源证据。
3. 将证据按 aspect 与立场组织。
4. 评分 claim 是否比证据更确定、更统一或覆盖范围更广。
5. 在多系统和多数据集上比较 smoothing。

## 关键实验结果

**论文报告**：在 7 个系统、4 个数据集上，Research Agents 持续生成强于底层证据所允许的结论。论文公开代码和数据；摘要未给出单一总体差值。

## 证据质量与局限

覆盖多个系统并提供 claim-level pipeline，证据具有可复用性。局限是抽取、检索、聚类和终判仍可能依赖模型组件，误差会级联；它测的是证据—结论关系，不等同于最终事实真伪。

## 最接近的相关工作

PaperDoctor、Evidence-First Agentic Verification、事实核验的证据—答案分账、Ground-truth-as-code。本文强调多源冲突被错误压平的问题。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 输出拆成 outcome score、evidence coverage、evidence conflict、claim strength 四个分布；要求 critique 附带源指针和反证。对证据冲突高的状态输出 T，而不是平均为中间分。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：只在证据覆盖充分时蒸馏 claim-level score。
- **A/B/T**：双方引用不同但可信证据时允许 T/INCONCLUSIVE。
- **硬真值门控**：可执行或原始源证据优先于报告自述。
- **critique states**：保存支持证据、反证和作用域，不保存单一“经验结论”。
- **高熵探索**：证据冲突应触发新的检索/分叉。
- **sealed eval**：隐藏冲突源与反证，测试 verifier 是否继续过度平滑。