# 事实核验分数的证据—答案分账

## 基本信息

- 论文标题：What Changes When Fact-Verification Scores Improve? Evidence and Answer Accounting Across Trained Verifiers and LLMs
- 作者：Han Chen；Yingrui Li
- 首次公开日期：2026-09-22
- 版本日期：2026-09-22（v1）
- arXiv：2609.27064
- DOI：https://doi.org/10.48550/arXiv.2609.27064
- 原始论文：https://arxiv.org/abs/2609.27064
- 代码：截至 2026-09-24，论文页面未提供作者代码链接

## 一句话结论

联合 verifier 分数的提升可能主要来自证据提交方式而非答案更正确，因此必须对答案质量和证据质量做反事实分账。

## 真正新增的内容

【论文原文】论文固定答案、替换证据，或固定证据生成条件、比较答案，通过四种答案—证据组合拆解 strict fact-verification score 的来源；同时考察模型、数据集、答案格式和上下文预算对“证据收益”的影响。

【分析推断】这直接警示 score-level verifier distillation：若 student 学会提供更讨好 scorer 的证据格式，联合分数会提高，但任务能力可能几乎未变。

## 核心方法

1. 在 FEVEROUS 上比较 DCUF 与 UnifEE 的答案和证据。
2. 用固定答案/替换证据的反事实组合估计证据贡献。
3. 对两个 8B LLM、三个数据集、两种答案格式和两种上下文预算生成 470,400 个响应。
4. 同时报告答案准确率、证据覆盖和联合 strict score 的 claim-level 变化。

## 关键实验结果

【论文原文】四个 DeBERTa checkpoint、7,890 个 claim 中，替换为 UnifEE 证据使 strict score 提升 9.61 个百分点，而答案准确率仅提升 1.96 个百分点；固定答案时，证据替换仍解释 7.92 或 9.08 个百分点。把上下文从 256 增至 2,048 token，在 FEVEROUS 上令固定答案的证据收益增加 3.84 和 3.10 个百分点，但跨数据集预注册判据未满足。

## 证据质量与局限

【论文原文】包含配对 95% 区间、大规模响应生成，并明确报告预注册跨数据集判据失败。

【分析推断】任务限于事实核验，不能自动外推到通用 Agent；严格分数依赖人工证据组定义。结论说明“需要分账”，但没有提出完整的防投机训练算法。

## 最接近的相关工作

与 ClaimReceipt、Ground-truth-as-code Agent Evaluation、PaperDoctor、AutoSciRub 和遗漏盲区研究最接近；共同主题是把整体判断拆成证据充分性、义务覆盖和最终答案，而非依赖一个总分。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 输出二维或多维序数分布：答案正确性、证据充分性、证据真实性和覆盖率；用固定答案替换证据、固定证据替换答案的反事实测试校准每个维度。总分只能作为展示，不应作为唯一蒸馏目标。

## 对现有 Agent verifier × OPD 路线的具体影响

【分析推断】

- score-level OPD：分别蒸馏 outcome score 与 evidence score，禁止用后者替代前者。
- A/B/T：只有答案和环境结果一致改善时判 A；仅证据包装改善应标 T 或单独的 evidence-A。
- 真值门控：证据指针必须通过环境查询或程序复算，联合 Judge 不得覆盖硬真值。
- critique states：critique 需包含可验证证据，但“证据更多”不能自动获得更高策略奖励。
- 高熵探索：保留答案相近但证据路径不同的分支，用于识别 scorer 偏好而非过早合并。
- sealed eval：报告固定答案和固定证据的反事实矩阵，检查优化是否只抬高可操纵的证据维度。