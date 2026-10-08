# Correct Answers, Unsupported Findings: Evidence Binding in Forensic Reconstruction of LLM Agent Logs

- 作者：Taehyeon Yun、Dongho Kim、Geonwoo Kim、Juyoung Seo、Minseok Hur、Moohong Min
- 首次公开日期：2026-10-07
- 版本日期：2026-10-07（v1）
- 原始论文：https://arxiv.org/abs/2610.09581
- Canonical URL：https://arxiv.org/abs/2610.09581
- 代码：https://anonymous.4open.science/r/2027_DFRWS_EU-624C

## 一句话结论

【论文原文】Agent 日志重建中“答案碰巧正确”不等于“证据支持”：没有 identifier-to-record 绑定表时，模型虽常答对，却会虚构 citation 与来源记录的关系。

## 真正新增的内容

【论文原文】将 complete-record agreement、evidence-grounded finding、justified abstention 与 unsupported assertion 分开计量，并用机械可检案例证明局部引用 ID 本身不构成来源证据。

## 核心方法

【论文原文】在 64 个 AgentDojo Banking 保存执行案例上，控制可见记录和 ID 绑定；两种 LLM reader 重建来源关系，与确定性 same-packet comparator 比较。

## 关键实验结果

【论文原文】原始 ID 可见但无绑定表时，Sonnet 找到所有字面位置，却在 28 个需要缺失关系的案例中有 26 个做出无支持的 citation-source 断言，其中 22 个仍与完整参考答案一致；加入显式绑定后两模型 grounding 均改善，确定性比较器始终正确解出或拒答。

## 证据质量与局限

【论文原文】任务机械可检、控制变量清晰，并有确定性基线。【分析推断】样本仅 64 个且聚焦取证重建；无法直接覆盖开放式语义证据，但足以否定“正确答案即可靠证据”的评分规则。

## 最接近的相关工作

【分析推断】与 Evidence Ledger、Transect、PaperDoctor、事实核验的证据—答案分账最接近；本文聚焦 citation ID 到原始记录的绑定完整性。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】verifier 输出需把 outcome score 与 evidence-binding score 分头；任何 critique 或完成声明必须携带不可伪造的 event/record ID 绑定，缺失时应 T/ABSTAIN。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：分别蒸馏答案正确性和证据绑定可靠性。
- 【分析推断】A/B/T：答案相同但证据缺失的候选不可判 A，应标 T 或降可信度。
- 【分析推断】真值门控：确定性 record binding 优先于 LLM 引用解释。
- 【分析推断】critique states：无有效绑定的 critique 禁止写回。
- 【分析推断】高熵分叉：对证据来源不确定的分支保留探索而非强裁决。
- 【分析推断】sealed eval：隐藏绑定表并审计 unsupported assertion 率。