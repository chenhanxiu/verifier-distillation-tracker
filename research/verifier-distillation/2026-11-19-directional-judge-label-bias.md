# Your Judge Inherits Your Prompt: In-Context Label Bias in an LLM-as-Judge Is Directional, Not Symmetric

- **作者**：Abdullah Ahmad、Ahmed J. O. Ahmed、Luca Citi
- **首次公开日期**：2026-11-19
- **当前版本日期**：2026-11-19（v1）
- **原始论文**：https://arxiv.org/abs/2611.26881
- **相关 DOI**：https://doi.org/10.18653/2026.blackboxnlp-1.40
- **代码**：截至本记录未发现作者公开代码链接
- **标识符**：arXiv:2611.26881

## 一句话结论

few-shot 示例的标签比例会单向抬高 LLM Judge 的接受率，且单次示例抽样可造成高达 18 个百分点波动；因此 verifier 蒸馏中的 A/B/T 先验与 sealed eval 示例集必须显式平衡和多抽样。

## 真正新增的内容

**论文原文**：作者固定生成器与答案，只改变 Judge few-shot 示例的 Yes/No 比例，并用双人共识真值验证，发现偏向接受的示例会显著抬高接受率，而偏向拒绝并不会产生对称下降。

**分析推断**：这不是普通位置偏差，而是 label prior 通过上下文直接污染 verdict 分布。若蒸馏的是 Judge logits 或 verbalized confidence，student 会把该偏差当成任务规律。

## 核心方法

- 冻结 generator–judge 流水线和被评分答案。
- 在四组 demonstration 中控制 Yes/No 比例。
- 每个数据集用 200 个样本、两位标注者共识作为参照。
- 另做五次 demonstration 抽样，估计单次提示选择造成的方差。

## 关键实验结果

**论文原文**：

- 平衡或偏拒绝示例时，Judge 接受率接近人类共识。
- 偏接受示例使 NExT-QA 接受率约升 30 点、MSVD-QA 约升 20 点，错误高度单向。
- 单次 demonstration 抽样之间最高相差 18 点，超过提示条件间差异。

## 证据质量与局限

控制变量清晰，且有人工共识基准，能支持“方向性偏差”而非一般相关性。局限是二元 Yes/No、多模态问答和每数据集 200 例；尚不能直接推出五级序数分布、长轨迹 Judge 或不同模型家族具有相同偏差。

## 最接近的相关工作

接近 LLM Judge 的位置偏差、自家族偏好、Judge 面板有效规模、Bradley–Terry 概率失真与 Numerical Scoring Topology。本文特别补充了 few-shot 标签先验的非对称性。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：训练和评测提示应固定 A/B/T 或序数桶的先验；对同一轨迹使用多组平衡 demonstration，聚合分布而非单次 verdict。可将示例抽样方差并入不确定性，在方差高时路由到环境 oracle 或人工审计。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：禁止直接蒸馏单一、偏接受提示产生的 logits；先做 prior correction 或重采样平均。
- **A/B/T 与序数分布**：训练批次按标签与位置双平衡，T 不能被当作负类填充。
- **真值门控**：用程序结果校准不同提示下的接受率，再决定 teacher 权重。
- **critique states**：同一 critique 在多提示下 verdict 不稳时，不进入记忆或训练。
- **高熵探索**：高提示方差代表 epistemic uncertainty，应保留分支而非过早剪枝。
- **sealed eval**：冻结平衡示例集、报告多抽样均值与区间，并与训练提示完全隔离。