# Rethinking Verbalized Confidence for LLM-as-a-Judge: A Compatibility Shift on Post-2025 Proprietary Models

- **作者**：Yu-Chung Hsiao
- **首次公开日期**：2026-09-10
- **当前版本日期**：2026-09-10（v1）
- **原始论文**：https://arxiv.org/abs/2609.10996
- **DOI**：https://doi.org/10.48550/arXiv.2609.10996
- **代码**：截至记录时未发现公开代码

## 一句话结论

在较新的顶级闭源模型上，经“过度自信提醒 + self-debate”处理的 verbalized confidence 可能比 logprob 更适合作为 Judge 软分数，但这种代际效应高度依赖模型快照。

## 真正新增的内容

**论文原文结论**：跨 SummEval、AggreFact、HelpSteer2 及最多 18 个模型，发现 post-2025 proprietary models 上 verbalized confidence 相对 logprob soft scoring 出现兼容性反转；准确率指标单独看不到这一变化。  
**分析推断**：这为 ordinal probabilistic reward model 提供廉价 teacher 信号，但只能当作待校准观测，不能当作认识论真值。

## 核心方法

在标准 verbalized-confidence Judge 上加入过度自信 advisory 与 self-debate，比较校准、分数分布展开、balanced accuracy 和对任务主观性的稳健性，并按模型年代分析 generation effect。

## 关键实验结果

论文报告在 AggreFact 的 90 个 model×task 比较中，Brier score 有 67 个支持新方法，且无比较显著支持 rubric 基线；post-era 模型中 Brier 为 37 个改善、8 个变差。post-2025 模型总体保持预测准确率，pre-2025 模型则出现可测的 balanced-accuracy 代价。

## 证据质量与局限

跨模型与多数据集比较有价值，且同时检查校准而非只报 accuracy；但闭源 endpoint 会随时间变化，年代分组与架构机制混杂，单作者研究需要复验。任务主要是响应级评价，不是长时程 Agent；self-debate 增加成本，也未证明在优化压力或 evaluator 共适应下保持校准。

## 最接近的相关工作

G-Eval/logprob soft scoring、verbalized confidence calibration、self-consistency/self-debate、distributional reward models、Robust Conformal Consensus、黑盒 Judge 测量不稳定性研究。

## 如何复用或推进 LLM-as-a-Verifier

让 Judge 输出完整序数概率及证据，而非硬分；用独立执行结果对 verbalized confidence 做 isotonic/conformal 校准。线上记录模型版本、提示词与日期，检测兼容性漂移。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：可用经校准的 verbalized distribution 控制梯度幅度，硬环境结果仍控制方向。
- **A/B/T**：由两分支置信区间重叠定义 T，避免强迫微小分差成为 A/B。
- **critique states**：self-debate 可产出候选 critique，但须由证据覆盖和环境回放筛选。
- **高熵探索**：高熵/高区间重叠应保留探索或升级强 verifier。
- **sealed eval**：必须锁定 endpoint 快照或持续做锚点审计；训练期 Judge 与 sealed Judge 不应共享同一可漂移服务。