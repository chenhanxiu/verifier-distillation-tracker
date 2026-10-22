# SANE: Automated Scorer-Specific Metamorphic Testing for LLM Judges

- **作者**：Ethan Ludwick、Yu-Chung Hsiao
- **首次公开日期**：2026-10-20
- **版本日期**：2026-10-20（v1）
- **原始论文**：https://arxiv.org/abs/2610.28886
- **arXiv ID**：2610.28886
- **DOI**：https://doi.org/10.48550/arXiv.2610.28886
- **代码/项目**：未发现公开链接

## 一句话结论

SANE 自动为每个 Judge 生成“应保持不变”或“应定向变化”的变形测试，可把 sealed eval 从固定通用扰动扩展为 scorer-specific 审计。

## 真正新增的内容

不再依赖人工预设扰动清单，而是从 scorer 规范、实现和代表性输入自动识别能力，生成特定扰动 recipe、预期分数关系，并独立验证测试是否忠实于 scorer 意图。

## 核心方法

Agent pipeline 先抽取 scorer-specific capability，再合成 metamorphic relation 与实例；独立验证器检查 recipe 合法性、变换是否真实发生及期望关系能否成立，最后以通过率评价 Judge。

## 关键实验结果

五个领域中，SANE 生成的有效测试族数量为 Judge Reliability Harness 的 3.7 倍，并在所有领域发现缺陷；其 faithfulness 测试对 11 个 Judge 的排序与 FaithBench 人标排序 Spearman 相关为 0.852，JRH 为 0.100。

## 证据质量与局限

跨五领域且有人类标注外部锚点，证据较强；但测试生成与测试验证仍可能共享模型偏差，且论文只证明审计相关性，不证明经修复后的训练收益。

## 最接近的相关工作

最接近 MAWILE、Beyond Aggregate Scores、AutoTuneBench、All Verdicts Are Not Equal 与 TRACE。

## 如何复用或推进 LLM-as-a-Verifier

为 pointwise、pairwise A/B/T、序数分布各自生成不变性和敏感性测试；将失败模式作为 teacher reliability feature，而不是直接把 Judge 的单次置信度当蒸馏权重。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】每轮更新 verifier 前应先在冻结的 SANE-style 测试集上验收，且测试生成器与最终 scorer 分离。sealed eval 应同时报告不变性误差、方向性误差和环境真值误差，避免 evaluator 共适应被平均分掩盖。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
