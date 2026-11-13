# Safety as a Budget: Calibrating the Control Channel of Constrained GRPO for Vision-Language Models

- **作者**：Bo Han
- **首次公开日期**：2026-11-12
- **版本日期**：2026-11-12（v1）
- **原始论文**：https://arxiv.org/abs/2611.16628
- **代码**：未见公开代码仓库
- **标识符**：arXiv:2611.16628；DOI: 10.48550/arXiv.2611.16628

## 一句话结论

【论文原文】用于排序的安全 scorer 若直接当作绝对 cost，会因均值偏差和 GRPO 组内标准化失效；经 Judge 标签单调校准并保留双通道 advantage 后，held-out harm 从 8.9% 降至 4.8%。

## 真正新增的内容

【论文原文】论文识别两个机制性失败：排名 scorer 的均值不代表真实风险预算，且标准 GRPO 会在组内标准化中消去拉格朗日乘子。Two-channel constrained GRPO 保留原 reward 的组内排序，同时将 penalty 与约束估计经单调映射校准，并让乘子真正进入梯度。

【分析推断】这对 ordinal probabilistic reward model 很关键：序数/排名能力不自动赋予可当绝对期望值使用的标尺。现有 score-level verifier distillation 若直接匹配 raw score，可能蒸馏的是排序而非风险概率。

## 核心方法

1. 用离线 scorer 生成原始安全分数。
2. 用 Judge 标注训练单调校准映射，将排序分数转成约束可解释的 cost。
3. reward 通道保留原始组内比较；constraint 通道保留绝对尺度与拉格朗日乘子。
4. 用可控的 order-preserving distortion 验证固定点理论。

## 关键实验结果

【论文原文】Qwen3-VL-2B 上，1,037 个对抗 prompt 的 harm 从标准 GRPO 的 8.9% 降至 4.8%，未校准预算为 7.6%；400 个 benign query 的 over-refusal 不超过 2%，MMBench 不变。HADES 从 28.9% 降至 12.8%；换 Judge 标签、图像 Judge 和人工审计时趋势保持。

## 证据质量与局限

【论文原文】有理论固定点分析、可控分数扭曲、跨 Judge 与人工审计；但实验集中在一个 2B VLM 与安全任务。

【分析推断】单调校准只能修绝对尺度，不能修构念错误、隐藏混杂或分布外失真；Judge 标签仍可能偏。对长轨迹还需处理逐步 cost 的时间信用与相关误差。

## 最接近的相关工作

最接近 ordinal reward model、constrained GRPO、Coupled Calibration and Learning、Rethinking Verbalized Confidence、PROSE 与 reward score 残差化审计。本文特别强调“保序不等于校准”和优化器会消去控制信号。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 输出分成 ordinal preference 分布与经真值校准的绝对风险分布；前者用于 A/B 排序，后者用于预算和门控。校准集应来自程序化/环境真值或独立人工 reference，并随策略更新做小规模 fresh recalibration。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：不要直接蒸馏 raw Judge score；先做单调或等距校准，并分离排序与绝对 cost 通道。
- **A/B/T 与序数分布**：A/B 可依保序分数，T 由校准不确定性或区间跨阈值触发。
- **环境真值门控**：硬真值决定安全方向，soft verifier 只调幅度。
- **critique states**：critique 的风险分数须通过独立标签校准，避免高置信措辞影响绝对尺度。
- **高熵探索**：在预算内保留高熵合法分支，避免单一惩罚权重导致全面拒绝。
- **sealed eval**：冻结校准映射、预算和独立 harm/over-refusal 集，避免训练中重新拟合评价标尺。
