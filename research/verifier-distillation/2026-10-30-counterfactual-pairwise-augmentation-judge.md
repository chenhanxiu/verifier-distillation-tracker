# CPA：用反事实成对增强训练小型 Pointwise LLM Judge

- **论文标题**：Counterfactual Pairwise Augmentation Improves Small Pointwise LLM Judges
- **作者**：Mohammad Zangooei, Peyvand Teymoori, Mohammad Robati Shirzad, Soroosh Shahtalebi
- **首次公开日期**：2026-10-30
- **版本日期**：2026-10-30（v1）
- **原始论文**：https://arxiv.org/abs/2610.41149
- **DOI**：https://doi.org/10.48550/arXiv.2610.41149
- **代码链接**：论文页面未列出

## 一句话结论

CPA 为每个 pointwise 样本合成并审计一个最小反事实负例，联合训练 pointwise 与 pairwise 任务，使 8B Judge 在六个二元标准上显著优于 pointwise-only 和模型合并。

## 真正新增的内容

**论文原文结论**：跨 query 的 pointwise 标签沿许多维度同时变化，无法清晰标定决策边界；同 query、反标签的最小反事实 pair 能把“决定性差异”显式化。联合训练可在 pairwise loss 平坦方向保持 pointwise 最优点，在高曲率方向吸收 pairwise 信息。

**分析推断**：这为现有 A/B/T 与序数评分分布提供直接数据构造方案：先以 pointwise outcome 为锚，再围绕同一 Agent 状态生成最小动作/critique 反事实，学习局部边界而非全局文风差异。

## 核心方法

1. 对每个 pointwise item 合成一个预期携带相反标签的 counterfactual response。
2. 审计反事实是否确实跨过目标 criterion 的边界。
3. 将原响应与反事实组成 pairwise 选择题。
4. 同一 Judge 联合微调 pointwise 和 pairwise 数据，部署时仍仅使用 pointwise 模式。

## 关键实验结果

**论文原文报告**：

- 在 Qwen3-8B 的六个二元标准 LoRA adapter 上，criterion-averaged pointwise macro-F1 比 pointwise-only 提升 2.5 点。
- 在全部六个标准、所有测试 merge weight 上均优于分别训练后做模型合并。
- 比所评估的最强 zero-shot frontier Judge（Gemini 3.6 Flash）高 11.8 点。

## 证据质量与局限

有六标准、多个 merge weight 和二阶理论解释，能支持 CPA 的局部边界价值。但实验限于二元 criterion、单一 8B backbone 与 pointwise 部署；反事实由何种模型生成、审计错误率和跨域泛化仍决定可靠性。结果不能直接证明序数分布已校准，也未在长轨迹终局真值上验证。

## 最接近的相关工作

包括 pointwise/pairwise Judge 训练、counterfactual data augmentation、model merging、TwinCheck 的 negative twin，以及 MAWILE 的受控扰动审计。CPA 的区别是以同源最小 pair 联合塑造 pointwise 边界。

## 如何复用或推进 LLM-as-a-Verifier

- 从共享 Agent 状态生成 A（原动作）、B（最小反事实）、T（未跨界或证据不足）。
- 先用 executor/环境断言审计 pair，再让 teacher 提供局部排序或序数间隔。
- 训练多头 verifier：pointwise outcome、pairwise preference、ordinal bucket；用一致性约束但不强行抹平 T。
- 对 critique states 只改变一个可定位主张、工具参数或步骤依赖，避免多因素混淆。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析推断**：将 CPA 作为 score-level OPD 的数据层：在 student on-policy 状态上围绕高熵动作合成最小反事实，以环境真值判定是否真正翻转，再联合蒸馏 pointwise score 与 A/B/T。高熵分叉如果多个动作都成功，应保留 T 或多峰序数分布，不能伪造唯一赢家。sealed eval 使用未见反事实生成器和隐藏 executor，并报告边界敏感性、语义保持不变性与真实任务成功，防止只学会合成器痕迹。