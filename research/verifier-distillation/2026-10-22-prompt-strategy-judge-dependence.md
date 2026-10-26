# 多语言 Judge：Prompt 策略效果依赖具体 Judge

- **论文标题**：Prompting Strategy Effects Depend on the Judge: A Multilingual Study of LLM-as-a-Judge Robustness
- **作者**：Asal Mehrabi、Mohammad Aliannejadi、Clemencia Siro
- **首次公开日期**：2026-10-22
- **版本日期**：2026-10-22（v1）
- **原始论文**：https://arxiv.org/abs/2610.31172
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.31172
- **代码**：未发现公开代码链接

## 一句话结论

超过一百万次打分显示，CoT、角色设定等 Judge prompting 策略并不跨 Judge 或语言迁移，效果甚至会反向；prompt 必须作为 evaluator 版本的一部分冻结和单独校准。

## 真正新增的内容

**论文原文结论**：系统比较 9 种 prompting 策略、4 个开源 Judge、27 种语言、4 类任务与 13 个数据集，并用人工判断验证 pointwise score。

**分析推断**：这说明“换一个更复杂 Judge prompt”不是稳健提升；在 verifier distillation 中，prompt 变化相当于 teacher 分布切换，应像模型 checkpoint 一样纳入版本控制。

## 核心方法

1. 同一 gold-reference 输出上改变 Judge prompting 策略。
2. 横跨多 Judge、任务与资源水平语言。
3. 分析 judge × strategy × task × language 的交互。
4. 对照人工判断，避免只看模型间一致性。

## 关键实验结果

**论文原文结论**：Judge 模型选择的影响大于 prompting 策略；策略效果会在不同 Judge 间反向；低资源语言稳定性更差，而聚合指标会掩盖这些差异。总计产生超过 100 万个 pointwise score。

## 证据质量与局限

实验覆盖广且有人类锚定；但只含 4 个开源 Judge，主要是 pointwise 静态输出，不含长轨迹、pairwise 顺序和 on-policy 共适应。摘要未给出每种语言的绝对提升区间。

## 最接近的相关工作

接近 Who Judges Matters、Rethinking Verbalized Confidence、Multilingual P(True)、MAWILE、Agreement Overstates Evidence 与 CAP。

## 如何复用或推进 LLM-as-a-Verifier

将 evaluator 指纹扩展为 model + checkpoint + prompt + rubric language + decoding + parser；每个组合单独做人工/硬真值校准，禁止跨版本混合 score。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：prompt 版本变化后重新校准蒸馏幅度。
- **A/B/T**：不同 prompt verdict 冲突时保留 T，而不是置信度加权成伪确定。
- **真值门控**：prompt 优化只能在硬真值不退化时上线。
- **critique states**：保存生成 critique 的完整 evaluator 指纹。
- **探索保留**：对 prompt 敏感的状态维持多分支。
- **sealed eval**：评测 prompt 与训练/选择 prompt 隔离，并报告跨 prompt 最差性能。
