# Beyond Single-Turn Confidence：Agent 轨迹级不确定性量化

## 基本信息

- **标题**：Beyond Single-Turn Confidence: Trajectory-Adapted Uncertainty Quantification for LLM Agents
- **作者**：Dylan Bouchard, Mohit Singh Chauhan
- **首次公开/版本日期**：2026-08-12（v1）
- **arXiv**：https://arxiv.org/abs/2608.11552
- **代码**：截至记录时未发现公开仓库

## 一句话结论

单步 token confidence 不能稳定代表整条 Agent 轨迹成功概率；轨迹重采样的一致性通常更强，低成本 self-reflexive score 也优于多数白盒聚合，为 distributional verifier 提供了直接基线。

## 真正新增的内容

**论文结论：** 在 BFCL-v4 与 τ²-bench 的四类多轮工具任务上，比较白盒 action-token probability、黑盒重采样一致性和模型自评三类 UQ；方法迁移有效但强烈依赖跨 turn 聚合器、等价定义与成本。

**分析推断：** 这些 uncertainty scores 可以成为 score-level OPD 的 teacher targets，但论文只预测完整轨迹成功，尚未解决用户当前关心的“下一步动作对最终目标贡献”。

## 核心方法

- 五个 LLM、四个 multi-turn tool-use datasets。
- 白盒：对 action token probabilities 跨 turn 聚合。
- 黑盒：额外采样 3 条轨迹，比较 trajectory/action/message equivalence。
- Reflexive：模型对最后动作前缀做一次自评。
- 以 greedy trajectory 的最终成功标签计算 AUROC，并用 task-clustered bootstrap。

## 关键实验结果

**论文报告：** scorer family 的平均/峰值 AUROC：白盒 0.628/0.725，reflexive 0.691/0.885，action consistency 0.705/0.849，judged consistency 0.686/0.868；message consistency 平均较弱（0.603）。作者提示部分列 minority class 少于 20，不能视为确定排名。

## 证据质量与局限

- 多模型、多工具域、成本分析和 clustered bootstrap，适合作为轨迹 verifier 基线。
- 数据集 label noise、user simulator、action interface 范围和统计功效均有限。
- 黑盒一致性混合 agent 与 simulated-user 变化；论文仅做一个 targeted prefix ablation。
- 预测的是轨迹最终成功，不是因果贡献或可恢复性；部分 grading 依赖 Judge。
- 未训练/蒸馏 verifier，也未检验用这些分数在线决策是否提高结果。

## 最接近的相关工作

Semantic/self-consistency、token-probability uncertainty、self-evaluation、trajectory reward/verifier、AgentRewardBench。

## 如何复用或推进 LLM-as-a-Verifier

把三类 UQ 作为 teacher features，输出失败/低贡献/可恢复/高贡献的序数概率；对当前下一步动作做短程 counterfactual resampling，而非等待完整轨迹。将环境执行标签用于校准，Judge 只补开放语义。

## 对 Agent verifier × OPD 路线的影响

- **Score-level OPD**：蒸馏 trajectory/action consistency 与 reflexive teacher 的组合分布。
- **A/B/T**：两个动作的短续跑成功区间重叠时标 tie，不强制排序。
- **真值门控**：BFCL/τ² 的环境结果应优先于 self-confidence。
- **Critique states**：比较 critique 前后 action-consistency，评估 critique 是否真正减少不确定性。
- **高熵探索**：高 uncertainty 应触发额外 rollout，而不是立即剪枝。
- **Sealed eval**：用不参与 UQ 校准的任务和 grader 检查 AUROC、ECE 及实际决策收益。
