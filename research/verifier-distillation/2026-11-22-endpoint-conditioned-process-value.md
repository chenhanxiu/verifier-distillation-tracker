# Endpoint-Conditioned Process Value: What an Endpoint-Blind Process Score Adds Once Terminal Status and Cost Are Known

- **作者**：Chris D Yan, Ken Wang, MarkX Qian, Jin Jiang, Albus Wu, Wenhao Wang
- **首次公开日期**：2026-11-22
- **版本日期**：2026-11-22（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.29354
- **DOI**：https://doi.org/10.48550/arXiv.2611.29354
- **代码/数据**：论文称已发布 protocol、sealed-endpoint harness 与全部轨迹；arXiv 摘要页未给出可核实的独立 URL

## 一句话结论

过程分数是否提供终局状态与成本之外的信息高度依赖 Judge 规模和可见证据；小 Judge 的增益可能为零，而泄露终局 verdict 会人为抬高判别力。

## 真正新增的内容

**论文原文结论**：首次直接估计 endpoint-blind process score 在已知 terminal status 与 cost 后的增量价值，并操纵 Judge 规模与 evidence access。  
**分析推断**：这是现有 sealed eval 设计的强实证支持，也说明训练时“看全轨迹”与评估时“看终局”必须分账。

## 核心方法

构造 agent 与 Judge 都不可见、但需要额外 artifact 才能确定的 sealed consequence；以 terminal status + cost 为基线，在 7 个 Python 仓库的测试生成任务上比较不同 Judge 与证据视图。

## 关键实验结果

1,255 条轨迹、158 个任务。4B–14B 的四个 Judge（含一个先 reasoning）增量 AUC 的区间均未与零分离；Qwen3 32B 增加 0.050 AUC（95% CI [0.020, 0.081]），重拟合 bootstrap 为 [0.013, 0.095]。8 个行为计数器可恢复多数增益，加入计数器后 Judge 仅再增 0.020。披露 terminal verdict 使 standalone discrimination 虚增 0.103。

## 证据质量与局限

有 sealed artifact、明确估计量、置信区间和 bootstrap，证据较强。局限是仅测试生成任务，且结果依赖所选 Judge 与轨迹分布；过程分数对训练的因果收益未直接验证。

## 最接近的相关工作

最接近 AutoTuneBench 的冻结测量、Harness or Model? 的 harness 混淆、Beyond Accuracy 的 evidence-access 阈值，以及 Reward Score 残差化审计。

## 如何复用或推进 LLM-as-a-Verifier

所有 process verifier 都同时报告：相对 `terminal status + cost + behavioral counters` 的增量 AUC、Judge 规模、可见字段和消融；禁止把终局 verdict 放进 process-only 输入。

## 对 Agent verifier × OPD 实验路线的具体影响

独立 sealed eval 应成为主验收：teacher/student verifier 都不可见 sealed artifact；score-level OPD 只在训练闭环中使用，最终比较其对 sealed consequence 的增益。student-generated critique 可作为特征，但须证明超过行为计数器；否则不应增加复杂度或声称学到过程价值。