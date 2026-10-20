# Write Once, Check Many: Reusable Ledgers for Post-Hoc Policy Compliance Auditing of Agent Trajectories

- **作者**：Ashwin Nagarajan、Gursimran Panesar、Alicia Yang、Mona T. Diab、Virginia Smith、Aashiq Muhamed
- **首次公开日期**：2026-10-18
- **版本日期**：2026-10-18（v1）
- **原始论文**：https://arxiv.org/abs/2610.24483
- **arXiv ID**：2610.24483
- **DOI**：https://doi.org/10.48550/arXiv.2610.24483
- **代码/项目**：未公开

## 一句话结论

先把长 Agent 轨迹写成与政策无关的证据 ledger，再让不同 verifier 重复审计，降低长上下文成本并支持事后新增规则。

## 真正新增的内容

将一次性的 trace interpretation 与多次 policy checking 解耦；ledger 保存动作、结果与证据，而不是针对某一 rubric 的结论。

## 核心方法

writer 将完整轨迹压缩为可复用叙事/结构化 ledger，reader 针对新政策读取 ledger 判定；在多 Agent benchmark 上与直接读全轨迹比较。

## 关键实验结果

900 条 SHADE-Arena、τ-bench/τ2-bench 轨迹中，12B reader 的 narrative ledger 匹配或超过全轨迹；SHADE 组合政策 AUC 0.777，高于 31B full-trace 的 0.713，输入 token 约减少 5 倍。

## 证据质量与局限

跨三个 benchmark、模型规模和成本对照充分；局限是长工具输出或消息中的细粒度证据可能在 ledger 中丢失，writer 也会成为新的单点故障。

## 最接近的相关工作

与 DENSE、PaperDoctor、Evidence accounting、trajectory censoring 和审计日志体系最接近。

## 如何复用或推进 LLM-as-a-Verifier

把 ledger 作为 verifier 的可缓存 evidence state，要求每条事实带原始事件指针；序数评分与 A/B/T 均从同一 ledger 读取，但 sealed eval 抽样回看原始轨迹。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】可显著降低长轨迹多 Judge 成本，但训练期 ledger writer 必须冻结版本并做遗漏率审计；不能用 ledger 成功替代环境真值。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
