# ClaimReceipt：Agent 评测证据充分性与覆盖率的可验证回执

## 基本信息

- **论文标题**：ClaimReceipt: Verifying Evidence Sufficiency and Coverage in Agent Evaluations
- **作者**：Peiying Zhu, Sidi Chang
- **首次公开日期**：2026-09-02
- **当前版本日期**：2026-09-02（v1）
- **发表信息**：投稿至 NeurIPS 2026 Workshop “Who Verifies the Agents?”
- **arXiv**：[2609.01992](https://arxiv.org/abs/2609.01992)
- **DOI**：[10.48550/arXiv.2609.01992](https://doi.org/10.48550/arXiv.2609.01992)（DataCite 注册待完成）
- **代码**：截至 v1 未在 arXiv 页面提供公开代码链接

## 一句话结论

ClaimReceipt 把“某结论能否由留存证据重算”和“证据是否覆盖事先承诺的全部实验”分开验证，并输出 PASS／INVALID／INCONCLUSIVE，为 sealed eval 防止挑选性遗漏提供了低成本协议层。

## 真正新增的内容

**论文原文结论**：普通日志和 hash 链不能保证某个报告 claim 有足够证据，也不能证明没有漏掉失败实验。ClaimReceipt 将 typed transaction evidence 绑定到签名 experiment manifest，为每项 claim 单独验证 sufficiency 与 coverage；缺少关键证据时输出 INCONCLUSIVE，而不是错误地 PASS/FAIL。

新增之处是引入“事先承诺的实验全集”，使遗漏本身可见；同时允许隐私证据不公开但交给 auditor 解密。

## 核心方法

冻结 claim-relative receipt specification；在执行前签名任务 manifest，运行中保存类型化证据，终局 receipt 签名并串联。selective verifier 只读取验证某 claim 必需的字段，区分协议完整、覆盖完整和经济/质量结论可重算。另做字段消融和语义故障注入。

## 关键实验结果

**论文报告**：在 1,392 条历史 buyer–seller 记录上，CR-2 重现全部 5 个手工审计 verdict，精确重放 600 条确定性与 792 条 post-generation 记录；13 个字段组在测试消融中均非冗余；11/11 语义故障返回预期结果且 0/8 false positive。独立前瞻 CR-3 epoch 预先承诺 30 个 assignment：证据完整时 coverage/accounting PASS；少一个终局 receipt 时返回 INCONCLUSIVE_COVERAGE。开销为推理时间的 0.021%，每交易 9.9 KB。

## 证据质量与局限

证据设计较严谨：规格先冻结、有历史回放与前瞻验证、故障注入和预注册预测。局限是手工 verdict 只有 5 个、前瞻任务 30 个；作者自己的 specification-legibility probe 表明独立读者仍认为规格存在歧义。它验证的是证据和协议，不直接保证 rubric 本身正确或模型结论语义可靠。

## 最接近的相关工作

接近 sealed evaluation、不可篡改日志、实验预注册、Parsing the Stream、ExecRubrics、S3Gym 与 omission-blindness 研究。其独特贡献是让“遗漏了哪些运行”成为可验证命题，而非只保证现有日志未被改写。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：每个 verifier 分数都生成 receipt：绑定 case ID、轨迹版本、工具观察、rubric 版本、Judge 模型/提示及硬门结果。只有证据充分且 manifest 覆盖完整，分数才进入训练；否则标 T/INCONCLUSIVE。这样可避免只保留高分 rollout 或只审计 Judge 拒绝样本造成的选择偏差。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏样本必须携带可重算 receipt；缺字段样本不进入 loss。
- **A/B/T 与序数分布**：A/B 两条分支证据不对称时直接 T，而非比较不完整分数。
- **真值门控**：manifest、工具结果、终态与程序 checker 输出签名绑定。
- **critique states**：critique 必须引用 receipt 中具体证据；无引用或缺覆盖仅作候选。
- **高熵探索**：预先承诺分支全集，防止训练后只上报有利探索。
- **sealed eval**：隐藏证据可加密给独立 auditor；评测先检查覆盖，再报告性能。