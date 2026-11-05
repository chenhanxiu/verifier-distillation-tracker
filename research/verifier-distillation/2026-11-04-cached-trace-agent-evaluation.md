# 使用缓存轨迹进行任务高效的 Agent 评测

## 基本信息

- **作者**：Ben Johnson, Hayden Helm
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（v1）
- **原始论文**：https://arxiv.org/abs/2611.06803
- **DOI**：https://doi.org/10.48550/arXiv.2611.06803
- **代码**：未见公开代码链接

## 一句话结论

将参考 Agent 轨迹压成去模型/去 harness 身份化的结构摘要并构建系统几何，可仅执行少量新任务就估计完整基准成绩，明显降低 SWE-bench Verified 与 Terminal-Bench 2.0 的评测误差。

## 真正新增的内容

**论文原文结论**：原始 trace embedding 易被模型家族、系统身份和 harness 特征支配；LLM 结构摘要再编码能保留正确性/任务信号并削弱这些混杂因素。

**分析推断**：缓存轨迹可降低 sealed eval 成本，但预测分数不能替代真实环境结算；若同一摘要器参与训练和评测，会形成新的 evaluator 共适应通道。

## 核心方法

- 对历史参考系统的每条执行轨迹抽取结构摘要并嵌入。
- 从任务级轨迹表示构造低维系统表示。
- 将新系统在少量执行任务上的位置与 item-response model 结合，预测完整 benchmark score。
- 对比 raw trace embeddings 与不使用轨迹几何的基线。

## 关键实验结果

仅提供 1 个随机执行任务时：
- SWE-bench Verified 的 MAE 从 **0.13 降至 0.08**（Wilcoxon p<10^-4）。
- Terminal-Bench 2.0 的 MAE 从 **0.14 降至 0.12**（p<10^-3）。
- 在可用完整参考系统集时，各执行任务预算下均优于基线。

## 证据质量与局限

覆盖两个真实 Agent benchmark，有统计检验和强预算对照。局限是评估目标仍是 benchmark 总分，可能继承基准缺陷；新型策略、全新 harness 或分布外失败可能不在参考几何中。预测不能提供单轨迹因果信用。

## 最接近的相关工作

与 item-response theory、低预算 Agent evaluation、trace representation、harness contamination audit 和 sealed benchmark sampling 最接近。

## 如何复用或推进 LLM-as-a-Verifier

把结构摘要器作为低成本 triage verifier：只用于选择最有信息量的真实执行任务；最终标签仍来自环境。摘要表示可辅助发现覆盖盲区，并为 ordinal risk distribution 提供先验。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：缓存轨迹只能决定采样预算，不能直接成为训练 reward。
- **A/B/T/序数分布**：预测区间重叠时输出 T，并触发更多真实执行。
- **程序真值门控**：所有预测需定期由真实测试和环境结算校准。
- **critique states**：结构摘要去除模型/家族身份，同时保留证据和失败阶段。
- **高熵分叉**：优先真实执行表示空间中稀疏或 OOD 的分支。
- **sealed eval**：摘要器、参考系统与最终评测任务分离，报告预测误差与真实成绩。
