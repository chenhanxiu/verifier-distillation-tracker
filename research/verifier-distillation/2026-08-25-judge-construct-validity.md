# A Judge Should Know What Changed: Construct Validity for LLM-as-a-Judge Evaluation

## 基本信息

- 作者：Jianlin Chen、Wenhui Chen、Ziyao Lin、Chi Man Vong
- 首次公开日期：2026-08-25
- 版本日期：2026-08-25（v1）
- arXiv：2608.24419
- 原始论文：https://arxiv.org/abs/2608.24419
- DOI：https://doi.org/10.48550/arXiv.2608.24419
- 代码：论文公开页未提供

## 一句话结论

Judge 对表面改写保持稳定并不代表能识别真正质量变化：七个 Judge 在 invariance 约 0.945 时，construct sensitivity 仅 0.319，因此评估校准必须同时测“不该变时不变”和“该变时能变”。

## 真正新增的内容

**论文原文结论：** 将 construct validity 表示为二维 profile：对 construct-preserving 编辑的不变性 S，以及对最小 construct-changing 编辑的敏感性 R；证明两者独立，无法由单一标量无损概括。

**分析推断：** 这正好补足常规 Judge 一致率/Kappa 的盲区。新 Agent Judge 即使与人工总体一致，也可能对“目标推进、安全、可恢复性”真正变化不敏感。

## 核心方法

跨七个 Judge、四个领域，构造七类改变目标 construct 的最小干预和五类仅改变 register 的控制编辑；干预方向由人工确定，生成、验证和 judging 使用互不重叠的模型家族，降低自评共适应。

## 关键实验结果

在 S≥0.90 的匹配条件下，平均 S=0.945、R=0.319；范围变化敏感性 R_scope=0.383，高于强度变化的 R_strength=0.262。五个公开标签集中的 paired label 有 55%–67% 可被仅看表面的预测器复现，MT-Bench 人类投票达到 67.4%。

## 证据质量与局限

证据质量高：跨七 Judge、四领域、多种干预，且人工确定方向并隔离模型家族。局限是构造干预本身仍依赖研究者对 construct 的定义；尚未直接覆盖长时程 Agent 工具轨迹，也不能把 S/R 简单聚合为唯一上线阈值。

## 最接近的相关工作

最接近 Rubric Dropout、JuryProbe、Competence Not Accuracy、Jagged Judges 与 metamorphic testing。本文把“稳健性”与“对真实变化的敏感性”明确分离。

## 如何复用或推进 LLM-as-a-Verifier

为五维 Agent rubric 各自建立成对干预集：无关措辞、格式变化应保持分数；目标推进、工具可行性、安全副作用和可恢复性发生最小变化时应改变分数。分别报告 S、R 和方向正确率。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 只蒸馏在高 S 且高 R 维度上通过校准的 teacher score。
- **A/B/T：** 用最小 construct-changing 分支验证 Judge 是否能把 A/B 排对，并识别真正 tie。
- **真值门控：** 程序化干预给出变化方向，避免由 Judge 自己定义 gold。
- **Student critique states：** critique 必须指出被改变的具体 construct，而非响应表面差异。
- **高熵探索：** Judge 对强度变化不敏感时，不应用低分差强行剪枝。
- **Sealed eval：** 生成、验证、Judge 使用独立模型家族；隐藏最终干预集，防止 evaluator 记住模板。
