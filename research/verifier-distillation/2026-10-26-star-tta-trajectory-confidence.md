# StaR-TTA：RL 轨迹漂移下的测试时置信度适配

## 基本信息

- **论文标题**：Test-Time Confidence Adaptation under RL-Induced Trajectory Shift
- **作者**：Zhenzhen Ren, Xiaoqing Zhang, GuoBiao Li, Bowen Fang, Yanxi Wang, Xinpeng Zhang, Ke Han
- **首次公开日期**：2026-10-26
- **版本日期**：2026-10-26（v1）
- **论文链接**：https://arxiv.org/abs/2610.35500
- **代码链接**：未发现公开代码

## 一句话结论

Agentic RL 会让轨迹式置信度估计器失准，但“更稳定的轨迹更可能正确”这一排序关系仍可用于无标签测试时重校准。

## 真正新增的内容

**论文原文结论**：Base 与 RL 模型之间轨迹分布显著变化，已有 confidence estimator 会退化；StaR-TTA 在有标签 Base 轨迹上联合学习正确性和稳定性监督，再用无标签 RL 轨迹的稳定性排序做测试时适配。

**分析推断**：distributional verifier 在 policy 更新后不能沿用旧校准曲线。可以把轨迹稳定性当作迁移锚点，但它只能校准概率排序，不能替代执行真值或证明因果正确性。

## 核心方法

- 从多条推理轨迹提取稳定性信号。
- 在 Base 数据上联合优化 correctness supervision 与 stability-derived ranking。
- 在目标 RL policy 上不使用正确标签，仅利用稳定性排名适配 confidence。
- 跨数据集、模型家族、规模和 Agentic RL 算法测试。

## 关键实验结果

**论文报告**：四个 QA benchmark 平均 AUROC 为 0.721，并在未见数据集、模型家族与规模、不同 Agentic RL 方法上持续改善。

## 证据质量与局限

跨设置泛化是优点。局限是 AUROC 只评价排序，不代表概率校准或决策阈值正确；QA 推理轨迹短于工具 Agent，稳定轨迹也可能是稳定地使用错误策略。

## 最接近的相关工作

The Mirage of Calibrated Confidence、FARM、Speculative Uncertainty、Policy-Aligned Predictive Verification。本文专门处理 policy 训练导致的 confidence distribution shift。

## 如何复用或推进 LLM-as-a-Verifier

每次 policy/OPD checkpoint 更新后，保存同题多 rollout 的 score、轨迹 embedding 与执行结果；若无即时标签，可暂用稳定性排序重校准，但在后续有环境结算时回填并检验 ECE/Brier/coverage。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：蒸馏权重需随 policy checkpoint 重新校准。
- **A/B/T**：低稳定性或适配后后验重叠的状态标 T。
- **硬真值门控**：稳定性仅决定幅度，环境结果决定方向。
- **critique states**：跨 rollout 不稳定的 critique 暂不写入长期记忆。
- **高熵探索**：不稳定状态应增加分叉，而非强行压低熵。
- **sealed eval**：冻结跨 checkpoint 的校准集，报告 AUROC 外还需 ECE、Brier 和 selective risk。