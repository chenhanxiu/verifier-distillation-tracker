# Detection Is Not Enough：把推理轨迹当作可测试的程序假设

- **论文标题**：Detection Is Not Enough: Reasoning Traces as Testable Program Hypotheses
- **作者**：Vaidehi Hegde
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.30200
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.30200
- **代码与结果**：https://github.com/S2V3/Detection-is-not-enough

## 一句话结论

无参考 verifier 能找到一部分可疑轨迹，但若 repair policy 不能稳定修复，提升检测率不会转化为最终准确率；critique-state 路线必须把“检测—修复—再验证”作为整体评估。

## 真正新增的内容

**论文原文结论**：作者不使用参考解、外部 judge 或权重更新，把单条 reasoning trace 抽象为关于题目数量的程序，扰动输入量、执行该程序并让同一模型回答改写问题，从而让每条轨迹产生自己的 metamorphic test；并推导 detect-then-retry 的 break-even 条件。

**分析推断**：相比传统 self-check，它把 critique 的可测试性放在结构化变换上；更重要的是证明 verifier AUC 不是闭环效用，repair-induced damage 必须进入目标。

## 核心方法

1. 对冻结 LLaMA-2-7B-chat 的 GSM8K 轨迹做静态自检。
2. 将轨迹解析为题目数量上的程序假设。
3. 改变一个数量并执行程序，生成候选自带的 metamorphic probe。
4. 用一次改写问题回答检查轨迹支持/反驳。
5. 以修复率 R 与损害率 D 推导 detector precision 需超过 D/(R+D) 才值得重试。

## 关键实验结果

**论文原文结论**：静态自检 AUROC 为 0.741；约三分之二错误轨迹没有错误方程，而是“错误计划被正确执行”。1,319 题中 937 题（71.0%）可构造有效扰动；在 847 条可解析首轨迹中，probe 支持的轨迹正确率 60.6%，基线 31.6%，但同时反驳 45.5% 的正确轨迹。没有测试策略显著提高最终准确率；即使完美 detector，在同等 retry 预算下估计也只恢复 66/1,319 题。

## 证据质量与局限

有公开代码、存储结果、机制分析和显式决策阈值，负结果报告完整。局限是单一旧模型、GSM8K 和单次改写；probe 的 45.5% 正确轨迹误拒率很高，解析失败与扰动有效性限制覆盖率；结论不能直接推广到工具 Agent。

## 最接近的相关工作

最接近 LLM-as-an-Improver、PaperDoctor、Beyond Aggregate Scores 的 metamorphic audit、Ground-truth-as-code，以及过程 verifier / self-consistency。不同点是候选轨迹本身生成可执行测试，而非依赖参考答案。

## 如何复用或推进 LLM-as-a-Verifier

让 generative verifier 不只输出 critique，还输出可执行 counterfactual test、预期结果和修复动作；随后真实执行并记录修复是否改善。训练目标同时惩罚漏检、误拒与 repair damage。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：优化目标应从 detector accuracy 改为验证后闭环净收益，包含 retry 成本与修复伤害。
- **A/B/T**：probe 支持/反驳可形成 A/B，解析失败或测试无效必须为 T。
- **硬真值门控**：counterfactual 必须由程序或环境执行，LLM 只提出测试。
- **critique states**：保存“轨迹程序—扰动—预测—实际结果—修复后结果”的完整状态。
- **高熵探索**：误拒高时保留原轨迹与修复轨迹双分支，而不是直接替换。
- **sealed eval**：用隐藏扰动生成器和独立执行器，分别报告检测 AUC、修复率、损害率和最终任务增益。
