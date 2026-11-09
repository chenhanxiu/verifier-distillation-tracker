# AutoRefine: Auto-Calibrating Code Judges from Workflow Outcomes

## 基本信息

- **作者**：Shervin Shahidi；James Poon；Hang Xie；Kenneth O. Xu；Robin Håkanson；Vikram Nair；Jens Pillgram-Larsen；Nachiappan Nagappan
- **首次公开日期**：2026-11-06
- **版本日期**：2026-11-06（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.09291
- **DOI**：https://doi.org/10.48550/arXiv.2611.09291
- **代码**：截至记录时未见独立公开仓库

## 一句话结论

用可见最终结果的 informed teacher 对工作流标签进行解释与弃权，再自动重写部署 Judge 的提示，可以在代码 Agent 分布变化时显著提高 Judge 与当前结果的一致性，但旧分布上的退化说明必须做版本化校准和独立评估。

## 真正新增的内容

**论文原文结论**：AutoRefine 不把 merge/abandon、测试通过等工作流结果直接当干净真值，而是让能看到结果的 teacher 判断该标签是否能从部署 Judge 的输入中解释；无法解释时弃权，再用保留样本自动校准 Judge prompt。

**分析推断**：这是 privileged teacher → deployable verifier 的轻量蒸馏原型，蒸馏对象是判定规则/提示而非模型参数或 score distribution。

## 核心方法

1. 收集代码变更的工作流结果标签。
2. informed teacher 同时看到 Judge 输入与结果，解释可保留标签并对不可解释样本弃权。
3. 以筛选后的标签迭代重写部署 Judge prompt。
4. 在当前和历史工作流切片上分别验证校准后的 Judge。

## 关键实验结果

**论文报告**：

- 在带执行 oracle 的 held-out 数据上，Scott's π 从 0.36 提升到 0.60。
- 人工随机翻转 25% 标签时，teacher 对翻转的 fail 标签弃权率超过真实 fail 的两倍，整体噪声降至 20%。
- 当前工作流的 17 个独立 held-out diff 上，π 从 0.16 提升到 0.51。
- 在 16 个旧工作流 diff 上，旧 Judge 反而更好，显示校准具有明显分布时效性。

## 证据质量与局限

- 同时包含执行 oracle 与真实部署结果，证据比只用 LLM 标签更强。
- 论文仅 5 页；当前/历史 held-out 集分别只有 17/16 个 diff，统计功效有限。
- 随机翻转噪声不等价于真实系统性偏差。
- 评价重点是一致性而非最终任务收益，也没有检验对抗性共适应或长期闭环漂移。

## 最接近的相关工作

接近 outcome-supervised Judge calibration、privileged-information distillation、selective prediction/abstention 和 continual reward-model calibration。与 HiSentinel 类 hindsight distillation 相似之处是 teacher 可见未来结果；区别是 AutoRefine 校准 Judge prompt，而非训练动作级 sentinel。

## 如何复用或推进 LLM-as-a-Verifier

可将 teacher 的三类输出扩展为“保留正例 / 保留负例 / 不可诊断 T”，并保存解释所引用的测试、执行日志和 diff 证据。随后蒸馏为小型 score-level verifier，同时保留弃权概率与时间/工作流版本特征。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：teacher 看到终局结果，student 只看在线状态；仅对 teacher 判定“输入足以解释结果”的样本蒸馏。
- **A/B/T 与序数分布**：T 应表示不可诊断，而不是折算成低分；可把 π 之外的校准概率作为分布目标。
- **真值门控**：执行测试、merge/abandon 只能作为候选真值，需先检查标签是否由 Judge 可见证据支持。
- **critique states**：只接纳包含可复核证据的解释；弃权样本反向驱动补充 observation。
- **高熵分叉**：新旧 Judge 分歧高的状态不应强制蒸馏，应保留探索并触发再采样。
- **sealed eval**：至少维护冻结的旧工作流切片与独立执行 oracle，防止持续重写 prompt 后只适配当前分布。