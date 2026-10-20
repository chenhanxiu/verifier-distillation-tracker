# ToolOPD: Credit-Aware On-Policy Distillation for Tool-Use Agents

- **作者**：Chu Zhao、Lei Tang、Yanming Wang、Jianzhe Zhao、Guibing Guo、Zhengzong Chen、Yuanyuan Zhao、Fei Huang
- **首次公开日期**：2026-10-19
- **版本日期**：2026-10-19（v1）
- **原始论文**：https://arxiv.org/abs/2610.25693
- **arXiv ID**：2610.25693
- **DOI**：https://doi.org/10.48550/arXiv.2610.25693
- **代码/项目**：未公开

## 一句话结论

用完整轨迹结果生成 hindsight skill，再测该 skill 对每个动作 token 的 teacher 概率影响，为长时程工具 Agent 提供结果感知的逐动作 OPD 信用。

## 真正新增的内容

反事实实验显示只反转终局结果就会改变多个交互轮次的信用，否定标准 OPD 的均匀信用假设。

## 核心方法

先将轨迹与结果总结为可复用 hindsight skill；再计算带/不带该 skill 时 teacher 对 student 动作 token 的概率差，将其转成 outcome-aware credit，重加权蒸馏损失并联合 RL。

## 关键实验结果

论文报告在多个长时程工具交互 benchmark 上显著超过 RL 和自蒸馏基线；公开摘要未列具体数值。

## 证据质量与局限

机制与长轨迹因果信用高度对齐；但 skill 由模型总结，可能混入事后合理化，且缺少摘要级精确效应量。

## 最接近的相关工作

最接近 BATON、γOPD、RLDS、RECAP 与 DRACO，区别在于以 teacher 概率对 hindsight skill 的敏感性估计动作信用。

## 如何复用或推进 LLM-as-a-Verifier

可把环境终局、错误码和程序断言先编码为不可修改的事实层，再让 generative verifier 生成 skill/critique，并仅在事实层一致时用于 score-level OPD。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】当前实验应新增“环境结果→hindsight critique→teacher 概率差”的逐动作权重，并与均匀 OPD、轨迹级 reward、反事实重放三种基线比较；sealed eval 不读取训练期 skill。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
