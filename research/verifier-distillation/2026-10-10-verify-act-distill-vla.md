# Verify, Act, Distill：把测试时 verifier 收益内化进 VLA

- **论文标题**：Verify, Act, Distill: Turning Test-Time Compute into Test-Time Adaptation for Vision-Language-Action Models
- **作者**：Kaneyoshi Hiratsuka, Satoshi Yamamori, Jun Morimoto
- **首次公开日期**：2026-10-10
- **版本日期**：2026-10-10（v1）
- **原始论文**：https://arxiv.org/abs/2610.14885
- **代码**：论文摘要未给出公开链接
- **标识符**：arXiv:2610.14885；DOI: https://doi.org/10.48550/arXiv.2610.14885

## 一句话结论

固定 verifier 在执行时聚合多候选动作，再把成功 episode 的聚合动作蒸馏进 LoRA，使单候选策略保留约 74% 的测试时计算收益。

## 真正新增的内容

**论文原文结论**：候选由 flow-matching VLA 生成，固定 verifier 评分并执行加权聚合；成功适应 episode 的观察与聚合 action chunk 用标准 flow-matching loss 蒸馏，无需额外 RL 或专门 teacher rollout。40 个 LIBERO 任务、每任务仅 10 episode 后，单候选成功率 54.1% → 70.6%。

**分析推断**：这是“执行期 verifier → on-policy 数据 → 策略蒸馏”的干净原型，但其蒸馏对象是动作而非 verifier 分布。

## 核心方法

1. 每状态采样多个动作候选。
2. 固定 verifier 评分，按权重聚合并在环境中执行。
3. 仅从成功适应 episode 提取监督，以 LoRA 内化聚合动作。
4. 可在蒸馏后再次使用同一 TTC 聚合。

## 关键实验结果

- 单候选：54.1% → 70.6%，保留约 74% 的八候选聚合增益。
- 蒸馏后再聚合：76.4% → 82.3%。
- LIBERO-Long：44.0% → 57.8%；LIBERO-plus 分布偏移上也提升。

## 证据质量与局限

覆盖 40 个任务并含长时程与分布偏移，结果直接。局限是仅成功 episode 的选择偏差、固定 verifier 可能被共适应、摘要未报告校准或失败候选保留；机器人仿真外推有限。

## 最接近的相关工作

与 VG-OPD、OnPoKD、Persistent Teacher Anchoring、Low-Bit OPD 以及 DDO 的多候选探索最接近。

## 如何复用或推进 LLM-as-a-Verifier

- 同时保存候选集合、verifier 分布、执行 outcome，而不只保存聚合动作。
- 将候选构成 pairwise A/B/T，并以环境成功率校准 verifier 分数。
- 把失败但可恢复候选保留为 critique-state 反例。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：加入“执行时多候选 verifier 聚合 → 成功轨迹蒸馏 → verifier-free 单候选评估”基线。score-level OPD 可蒸馏完整候选评分分布；环境真值门控方向，verifier 只定聚合幅度。高熵处保留多个候选，低熵处降采样。最终必须用冻结、独立 verifier 与隐藏环境种子做 sealed eval，验证内化收益而非 evaluator 共适应。