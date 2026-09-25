# JEV vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places

## 基本信息

- **作者**：Delip Rao、Chris Callison-Burch
- **首次公开日期**：2026-09-24
- **版本日期**：2026-09-24（v1）
- **原始论文**：https://arxiv.org/abs/2609.29769
- **DOI**：https://doi.org/10.48550/arXiv.2609.29769
- **代码**：论文页面未给出公开仓库

## 一句话结论

小型 typed probabilistic judge 可比 LLM Judge 便宜 29–325 倍、快 30–220 倍，但二者错误高度相关，使“低置信再升级”的级联最多只增益约 2 点。

## 真正新增的内容

【论文原文】在七个基准的九个 panel 上，用相同 criterion 比较输出许可答案概率的 Jev 与三个 flash-tier LLM Judge；除成本/速度外，重点测量跨 Judge 的相关错误及 selective cascade 的真实上限。

【分析推断】对序数 probabilistic reward model 而言，关键不是更便宜的置信度，而是错误是否与昂贵 teacher 独立；若同源偏差高度相关，级联路由不能提供真正的 safety net。

## 核心方法

【论文原文】Jev 直接输出允许答案上的概率分布，不生成文本；对 binary 与 graded rubric 分别比较 accuracy、agreement、置信度排序和基于 cross-fitted/oracle threshold 的级联。

## 关键实验结果

【论文原文】27 个成对比较中仅 8 个准确率差异显著；Jev 多在 binary criterion 占优、graded criterion 落后。LLM Judge 成本为 Jev 的 29–325 倍、耗时 30–220 倍。由于 LLM 重复 Jev 的许多高置信错误，cross-fitted cascade 相对最佳单 Judge 最多提升 1.5 点，oracle threshold 最多 2.0 点。

## 证据质量与局限

45 页、九个 panel、统一 criterion、含 cross-fitting，测量设计较扎实；但作者指出 graded label 可能依赖 criterion 文本未包含的 scale convention，因此 Judge–label 分歧部分可能是规范缺失，而非纯模型错误。未直接覆盖长时程 Agent 环境结算。

## 最接近的相关工作

与 JEV-as-a-Judge、Judge panel 有效规模、Agreement Overstates Evidence、Robust Conformal Consensus 和 UniRRM 最接近。新增价值是同时量化 typed classifier 与 LLM rubric Judge 的成本、序数偏差和错误相关性。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 Jev 用作低成本 distributional verifier，但升级条件不能只看自身熵；应加入跨家族 verifier 分歧、环境可验证性和 OOD 检测。graded rubric 必须显式写出 scale anchors，并保留完整序数分布而非只取 argmax。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- A/B/T 蒸馏报告每类概率、校准和跨 Judge 错误相关矩阵。
- 级联实验比较“自身低置信”“跨模型分歧”“环境不可验证”三种路由。
- teacher 面板按有效独立信息量加权，避免多个同源 Judge 伪装成共识。
- sealed eval 使用独立人工/程序真值，防止 student 与 teacher 在同一盲区共同高置信。