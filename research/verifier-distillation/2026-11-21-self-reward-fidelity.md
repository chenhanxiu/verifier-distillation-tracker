# Understanding and Mitigating the Fragility of Self-Rewarding Optimization

- **作者**：Rongyi Zhu, Tanqiu Jiang, Fenglong Ma, Ting Wang
- **首次公开日期**：2026-11-21
- **版本日期**：2026-11-21（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.28582
- **DOI**：https://doi.org/10.48550/arXiv.2611.28582
- **代码**：未见作者在 arXiv 摘要页给出独立代码链接

## 一句话结论

自奖励优化存在随 on-policy self-reward fidelity 下降而跨越的崩溃阈值；短前缀即可抬高自评分而不提高 oracle 质量，说明独立真值结算不可省略。

## 真正新增的内容

**论文原文结论**：定义 SRF 衡量 on-policy 自评奖励与 oracle 奖励的一致性，并用 Re-Ranking 与 Preamble 两类攻击展示 phase-transition 式崩溃；提出 Projection Decoupling Defense。  
**分析推断**：SRF 可直接作为 verifier teacher 是否允许继续蒸馏的停止/降权条件。

## 核心方法

Re-Ranking 将训练集中样本集中到 self-reward 与 oracle 分歧的 prompt；Preamble 学习仅抬高 self-reward 的短前缀。通过可控改变 SRF 观察迭代优化相变，并投影掉沿 reward generator 局部敏感方向的更新分量。

## 关键实验结果

论文报告：SRF 足够高时 SRO 改善，低于模型与任务相关阈值后发生迭代崩溃；防御在对抗条件下提高稳健性。摘要未给统一阈值或跨任务数值效应量。

## 证据质量与局限

两类受控攻击和机制性指标比单纯失败案例更有解释力；但阈值不具跨模型普适性，oracle 可用性是假设，且摘要未给长期 Agent 环境结果。

## 最接近的相关工作

最接近 PROSE 的伪标签自强化、RetireOPD 的 teacher 退出、Reward Integrity 的闭环奖励审计，以及 ImpossibleRubrics 的 verifier gaming。

## 如何复用或推进 LLM-as-a-Verifier

定期从 on-policy 轨迹抽样，使用程序/环境真值估计 SRF；按状态、任务和 score bin 分层报告。SRF 下降时降低 teacher 权重、增加 T/abstention、扩大 oracle 结算，并冻结或退休共适应 verifier。

## 对 Agent verifier × OPD 实验路线的具体影响

把 SRF 纳入 score-level OPD 的安全门：只有分层 SRF 高于预设阈值才更新；student-generated critique 必须检测 preamble/格式捷径。高熵分叉保留一部分不经自奖励筛选的探索分支；sealed eval 使用独立 oracle 与未见 prompt，专门检测自评提升但真实质量不变。