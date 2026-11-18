# Contract-Explicit Evaluation: From Auditing Learned Readers to Scoped Certificates

- **作者**：Hao Lu、Weixing Zhu、Ruiyang Li
- **首次公开日期**：2026-11-17
- **版本日期**：2026-11-17（v1）
- **原始论文**：https://arxiv.org/abs/2611.22665
- **代码链接**：https://github.com/lutttw/contract-explicit-evaluation
- **标识符**：arXiv:2611.22665；DOI: 10.48550/arXiv.2611.22665

## 一句话结论

【论文原文】评估结论必须绑定 gold、scoring 和 threshold 契约；Declare–Measure–Scope–Certify–Hedge 可指出哪些排行榜比较可证明稳健，哪些必须保留不确定性。

## 真正新增的内容

【论文原文】提出 preregistered contract-explicit protocol，以 Kendall concordance decomposition 和 distribution-free census certificates 把“换 Judge/阈值会不会翻转”转为带范围的证书，并在 DocRE 与 49,938 场 LLM-judge battle 上验证。

## 核心方法

1. **Declare** 冻结 gold version、score、threshold 与比较口径。
2. **Measure/Scope** 测量契约维度并圈定可证区域。
3. **Certify** 用分布无关的 census bound 给出错误上界。
4. **Hedge** 对无法稳定支持的比较明确不下结论，并保留 per-instance ledger。

## 关键实验结果

【论文原文】DocRE 审计覆盖同一架构族 44 次训练运行，scoring 维度得到三条 flagged instance、Clopper–Pearson 上界 0.146。LLM-judge census 含 17 个 Judge、49,938 场 battle；12.25% 排行榜比较按预注册条件必须 hedge，panel-robust bound 为 0.143。探索性 two-tier reading 可对 69% 比较给出不高于 0.072 的界；争议 battle 中 65% 是 Judge error 而非本身歧义。

## 证据质量与局限

【论文原文】有预注册、全量 ledger、负结果和开源 artifact，方法透明；但 certificate 只对声明契约与样本 census 有效，不自动外推新分布。cross-model certificate 在真实 confidence score 上被撤回，说明软分数校准仍是薄弱点。

## 最接近的相关工作

接近 Judge panel calibration、conformal evaluation、rank robustness、contract-aware benchmarking、MAWILE 与 evaluator dependence 审计。其新增点是把“可报告范围”正式化为证书和 hedge 规则。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】为 verifier 蒸馏建立版本化 evaluation contract：teacher snapshot、rubric、聚合、A/B/T 阈值、环境版本和置信区间全部入 ledger；只有跨契约稳定的改善才能进入 sealed report，其余标注为条件性结果。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：训练前声明 score mapping 与阈值，报告不同契约下是否翻转，而非只报一个均值。
- **pairwise A/B/T 与序数分布**：把 A/B/T threshold 作为契约维度；争议样本保留 per-judge 分布与 hedge 标签。
- **程序化/环境真值门控**：gold/environment 版本必须锁定并记账，动态真值变化不能静默混入。
- **student-generated critique states**：只有在预声明证据契约下可验证的 critique 才计为改进。
- **高熵分叉探索**：优先审计跨契约翻转的分叉，但不得把 exploratory two-tier 证书当 confirmatory 结论。
- **sealed eval**：直接采用 Declare–Measure–Scope–Certify–Hedge，且 evaluator panel 与训练 teacher 隔离。
