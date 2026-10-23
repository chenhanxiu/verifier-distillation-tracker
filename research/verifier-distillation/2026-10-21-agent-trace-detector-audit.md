# Agent 轨迹里“看见的行为”与“记录的标签”并不相同

- **论文标题**：What the Trace Shows and What the Label Says: Auditing Behavioral Detectors in Agent Evaluation
- **作者**：Idunnuoluwa A. Adeniji, Shilpika, Michael E. Papka
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.30491
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.30491
- **代码/轨迹查看器**：论文摘要提及 trace viewer，但 arXiv 元数据未给出独立公开链接

## 一句话结论

Agent 评测中的“验证过”“故障传播”等标签会被检测器定义和执行预算扭曲，训练 verifier 时必须保存可检查证据、适用性与截断状态，而不能只蒸馏最终标签。

## 真正新增的内容

**论文原文结论**：作者在带可控计算器故障的 GSM8K 工具场景中，审计 final correctness、visible re-verification 和 fault propagation 三类 trace-level detector，发现这些量会系统性分离，并识别 silent tool-output override。

**分析推断**：这不是一般的 parser bug；它表明“行为标签”本身是 measurement model 的输出。若直接用作 OPD teacher 信号，student 会学会检测器的操作性定义，而非真实因果行为。

## 核心方法

1. 随机让计算器返回错误值，保留工具返回、模型后续使用值和 detector 输出的可核对真值。
2. 在 6 个生产模型、每个 30 道题上运行 3 类检测器。
3. 人工复核 90 条轨迹并分类自动标签分歧。
4. 改变 step/token budget，测量截断对结论的影响。
5. 用 trace viewer 并列呈现证据与标签。

## 关键实验结果

**论文原文结论**：人工对 final correctness、fault impact、fault relevance 的核对分别为 67/67、19/19、18/18 一致，但 verification 标签仅 67/81 一致，14 个分歧落入 4 类重复模式。执行预算消融中，一个模型的正确数在 21/30–27/30 间变化，另一个在 27/30–29/30。

## 证据质量与局限

有可控故障、逐轨迹人工审计和预算消融，因果可解释性较好。局限是总问题量小、领域限于 GSM8K + calculator，生产模型与 detector 的选择可能影响分歧比例；结果证明标签脆弱，不直接给出统一修复器。

## 最接近的相关工作

最接近 Interface-Induced Trajectory Censoring、Harness or Model、Agent 轨迹可诊断性、DynSTEER，以及 evaluator measurement audit。与只检查最终正确率的工作不同，它把 detector 的适用性和证据一起审计。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 样本结构改为：verdict、evidence span、问题是否适用、轨迹是否截断、人工/程序化更正。对“未观察到显式 re-check”与“没有验证”分开建模，并让 generative verifier解释模型实际使用了哪个 observation。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：蒸馏 evidence-conditioned score，而不是裸标签；截断轨迹要单独建模。
- **A/B/T**：检测器问题不适用或证据不足时必须给 T，不能记为 B/失败。
- **硬真值门控**：工具返回、后续使用值与终局结果分别记录，避免 outcome 覆盖过程错误。
- **critique states**：critique 需指向具体 observation 和后续使用位置，经重放确认。
- **高熵探索**：执行预算作为显式状态变量，防止长分支因截断被误判。
- **sealed eval**：使用独立 detector 与人工抽检，并报告标签—证据一致率和预算敏感性。
