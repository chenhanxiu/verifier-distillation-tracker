# VerifierBench: Benchmarking the Generation of Executable Verifiers for LLM Agents

- **作者**：Jianing Yin、Ziyi Chen、Hao Wang、Yiyou Sun、Zijian Jin、Dawn Song、Daoan Zhang
- **首次公开日期**：2026-10-19
- **版本日期**：2026-10-19（v1）
- **原始论文**：https://arxiv.org/abs/2610.28679
- **arXiv ID**：2610.28679
- **DOI**：https://doi.org/10.48550/arXiv.2610.28679
- **代码/项目**：论文称项目页与数据集已公开，但 arXiv 摘要未给出可核验直链

## 一句话结论

自动生成的 executable verifier 往往善于拒绝坏解、却会把所有合法解一起拒绝，因此 verifier 训练与评测必须同时覆盖正例、等价合法解和攻击样本。

## 真正新增的内容

提出面向 Agent verifier 生成的 VerifierBench：222 个任务、六类 Agent benchmark、4,993 个隐藏测试，并用六项检查的 Verifier4Verifier 审计源 verifier 与测试套件。

## 核心方法

模型仅从任务指令与可用环境生成可执行 verifier；隐藏集同时包含标准正确解、不同形式的合法解和对抗性无效解，以 normalized balanced accuracy 衡量双向判别，而非只看拒绝率。

## 关键实验结果

19 个模型的 normalized balanced accuracy 仅为 10.6–62.1；生成 verifier 对无效解的拒绝明显强于对合法解的接受，且多数已分析假阴性来自“所有测试解都拒绝”的过严 verifier。

## 证据质量与局限

任务与隐藏案例规模较大、覆盖工具调用、状态和代码验证；但摘要未披露各环境分层结果，且 benchmark 本身仍依赖 V4V 对源测试的正确性。

## 最接近的相关工作

最接近 AutoGym、Ground-truth-as-code Agent Evaluation、GameLogicBench、MAWILE 与 Beyond Aggregate Scores。

## 如何复用或推进 LLM-as-a-Verifier

把 V4V 的六项审计接入 verifier teacher 准入：至少要求一条已知正确轨迹、多个语义等价合法轨迹和攻击轨迹同时通过，再允许生成 A/B/T 或序数监督。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】程序真值不能只作为“拒绝错误”的硬门；应拆成 false-accept 与 false-reject 两个方向。高熵分叉中若 verifier 对合法多样性过严，score-level OPD 会系统性压掉探索，因此需用合法替代解估计 support coverage，并在 sealed eval 中冻结隐藏变体。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
