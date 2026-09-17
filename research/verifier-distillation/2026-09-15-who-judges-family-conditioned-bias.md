# Who Judges Matters：Judge 家族条件偏置

## 元数据

- **论文标题**：Who Judges Matters: Measuring Family-Conditioned Preference in LLM-as-Judge Panels
- **作者**：David Ababio Awuni、Luke E. K. Achenie、Benjamin Tei Partey、Elvis Gyasi Owusu、Nii-Nai Derrick Sowah
- **首次公开日期**：2026-09-15
- **版本日期**：2026-09-15（v1）
- **原始论文**：https://arxiv.org/abs/2609.17857
- **代码链接**：论文称完整复现档案已准备公开；arXiv 页面未提供可核验代码 URL

## 一句话结论

Judge 面板并非可互换：同模型家族偏好与位置反转会系统性改变 pairwise 标签，因此 A/B/T 与序数分布蒸馏必须显式平衡 judge family 并保留分歧。

## 真正新增的内容

**论文原文结论**：在四个开源模型家族的全交叉设计中，作者提出固定候选家族后比较 Judge 的校正估计量，避免把候选质量误当成家族偏好；所有家族均存在正的同家族提升，且面板组成能改变相当比例的 pairwise 结果。

**分析推断**：对多 teacher verifier distillation，teacher identity 应成为标签生成过程的一部分。只聚合多数票会把结构性家族偏好压成虚假确定性。

## 核心方法

- Llama 3.1、Qwen 2.5、Gemma 2、Yi 1.5 四个家族的全交叉 pairwise Judge 设计。
- 固定候选家族，估计 judge-family conditioned preference。
- 使用家族平衡参考、人类共识锚点、panel 质量控制与 float16 复现实验。
- 分离同家族偏置与 AB/BA 位置反转。

## 关键实验结果

**论文报告**：共 9,312 次判断；常用家族统计量与 Bradley–Terry 能力高度混淆（r=0.95）。校正后四个家族的同家族提升为 3.4–8.4 个百分点，全局 FPS 为 0.067（95% CI [0.053, 0.084]，置换检验 p=0.0002）。55.4% 的 AB/BA 对发生反转；相对家族平衡参考，面板组成改变 18.5% 的 pairwise 结果。

## 证据质量与局限

- 优点：全交叉设计、独立人类锚点、精度复现和置信区间使偏置测量较扎实。
- 局限：只覆盖四个开源家族和 pairwise 协议；没有直接训练蒸馏后的 student verifier；judge-side likelihood 与偏置的关系仅为描述性衰减，不能解释为因果机制。

## 最接近的相关工作

JudgeStealer 关注跨 pointwise/pairwise/listwise 协议蒸馏，Robust Conformal Consensus 关注多 Judge 区间校准，多语言 Judge 排名反转工作关注语言—Judge 交互。本文补充的是模型家族条件偏置与位置反转。

## 如何复用或推进 LLM-as-a-Verifier

将每个 pair 同时交给家族平衡的 Judge 组，保存逐 Judge 概率而非仅多数结果；用层级 Bradley–Terry 或序数概率模型分解候选质量、家族偏置和位置效应。家族间分歧高时生成 T 标签或宽分布，并路由到环境真值/人类锚点。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏去偏后的潜在质量分布，不直接蒸馏单一 Judge logits。
- **A/B/T**：AB/BA 双向调用；位置反转或家族分歧时标 T。
- **真值门控**：可执行结果优先决定方向，Judge 只补充不可程序化维度。
- **critique states**：避免同家族 policy 与 Judge 形成“自家文本偏好”的闭环。
- **高熵探索**：家族分歧可作为保留分叉的信号。
- **sealed eval**：使用未参与训练、家族平衡且固定快照的 Judge 面板，并保留独立人类/环境锚点。