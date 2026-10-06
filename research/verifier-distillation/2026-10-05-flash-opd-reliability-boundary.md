# Flash-OPD: Fast On-Policy Distillation

- 作者：Wei Chen、Junle Chen、Yitong Yang、Zhaoyang Xu、Jiaxin Lin、Yuxuan Liang、Xiaofang Zhou、Kai Wang、Rui Chen
- 首次公开日期：2026-10-05
- 当前版本日期：2026-10-05（v1）
- arXiv：2610.06105
- 原始论文：https://arxiv.org/abs/2610.06105
- Canonical URL：https://doi.org/10.48550/arXiv.2610.06105
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】Flash-OPD 不预设统一 rollout 长度，而是在生成过程中按每条轨迹的 teacher–student 兼容事件精确判断可靠边界，获得 2.2×–7.5× 加速且不损失准确率。

## 真正新增的内容

【论文原文】可靠监督长度被建模为低兼容事件累计的 first-passage time；近期事件率只决定下次何时检查，真正停止仍由精确累计计数决定，从而把效率估计与正确停止解耦。

## 核心方法

【论文原文】缓存式生成与 teacher verification 交替进行，每条轨迹独立停止；短轨迹不会截断仍可靠的监督，长轨迹也不会继续支付越过可靠区的 teacher 成本。

## 关键实验结果

【论文原文】在多数据集和多 teacher–student 配置上，相对标准 OPD 实现 2.2×–7.5× 训练加速，同时保持或提高准确率。

## 证据质量与局限

【论文原文】跨数据集与模型设置的速度/准确率结果支持较强。局限是兼容事件仍是 teacher–student 一致性代理，不直接等价于环境正确性；阈值与缓存系统的工程敏感性可能影响复现；尚未证明对工具交互中的不可逆错误有效。

## 最接近的相关工作

最接近 AC-OPD 的自适应 continuation、STRIDE 的错误后缀提前停止，以及 Unified Per-Token OPD Gating。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把“低兼容事件”扩展为 verifier 分歧、环境违规和 critique 不一致的组合事件；长 Agent 轨迹可在首次累计风险越界处停止 teacher 查询并转入环境结算。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：【分析推断】按轨迹可靠边界截断 score 蒸馏，降低长后缀噪声与成本。
- **A/B/T 与序数分布**：【分析推断】越界后的状态不判负，标记 T/未观测。
- **硬真值门控**：【分析推断】硬违规应立即停止；软兼容事件仅控制检查频率。
- **critique states**：【分析推断】只在边界内生成/蒸馏 critique，越界后需重启或回放。
- **高熵探索**：【分析推断】不同分支独立停止，避免统一 horizon 抹去长尾有效路径。
- **sealed eval**：【分析推断】固定检查阈值并报告被截断轨迹的隐藏成功率，审计选择偏差。
