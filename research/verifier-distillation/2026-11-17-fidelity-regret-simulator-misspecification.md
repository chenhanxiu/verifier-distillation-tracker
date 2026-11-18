# Fidelity Regret: Measuring Simulator Misspecification in Verifiable Design

- **作者**：Noah Flynn
- **首次公开日期**：2026-11-17
- **版本日期**：2026-11-17（v1）
- **原始论文**：https://arxiv.org/abs/2611.22263
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.22263；DOI: 10.48550/arXiv.2611.22263

## 一句话结论

【论文原文】通过便宜 simulator/verifier 优化出的“可验证最优”设计仍可能在真实参考目标上产生巨大 regret；部分预算用于高保真重评分，比 cheap-only 或 reference-only 更稳健。

## 真正新增的内容

【论文原文】定义 fidelity regret：便宜模拟器选中设计后，在参考物理目标上的 simple regret；并给出跨 21,362 个设计、5 个 gate library、3 种 organism 的系统测量及预算感知缓解方案。这把 specification gap 从定性警告转为可估计指标。

## 核心方法

1. 分离拓扑可行性 verifier、便宜性能 simulator 与高保真 reference objective。
2. 在设计空间内比较 cheap-selected 与 reference-optimal 的目标差。
3. 测试精确有序赋值、oracle whitelist、冻结 LLM 搜索和不同预算分配。
4. 固定规则将比例 `α=0.34` 的预算用于对 cheap top designs 做高保真重评分。

## 关键实验结果

【论文原文】72 个实验 cell 的平均 normalized regret 为 0.369，仅 6 个为零；同一 library 的 regret 随参考轴从 0.113（cytometry）到 0.801（growth burden）。保留至少 25% 空间的 oracle whitelist 在 52 个 cell 中仍有 30 个正 regret。α=0.34 的混合重评分 mean excess regret 0.016，cheap-only 为 0.305，reference-only 为 0.034，并在 360 个 cell 中 330 个优于 cheap-only。

## 证据质量与局限

【论文原文】设计空间规模大、跨 library/organism，并含 matched zero-regret control；但领域是遗传电路，结论能否迁移到语言 Agent 需验证。高保真 reference 仍可能不是现实终极目标；预算规则是 in-sample 固定，跨域最优性未证实。

## 最接近的相关工作

接近 sim-to-real、reward model misspecification、Goodhart/reward hacking、RLVF、digital-twin validation 与 reality settlement。差异是用 regret 量化 verifier 优化后的参考目标损失。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 cheap LLM verifier 与 sealed environment/human reference 视为两种 fidelity：定期在 verifier top-ranked、high-confidence 轨迹上抽样重评分，估计 fidelity regret；若 regret 上升，收紧蒸馏权重或扩大 reference audit，而不是继续优化同一 Judge。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：除训练 reward 外，新增“teacher-selected vs sealed-reference-optimal”的 regret 曲线。
- **pairwise A/B/T 与序数分布**：重点重审 teacher 高置信 A/B；若 reference 翻转则保留 teacher/reference 双分布。
- **程序化/环境真值门控**：硬 verifier 只证明其 specification，不能被描述为现实成功；终局 reference 需独立建模。
- **student-generated critique states**：critique 通过 cheap verifier 后仍抽样做高保真复核，防止语言一致性替代真实改进。
- **高熵分叉探索**：不仅抽样高熵区，也抽样 cheap verifier 极高分区，因为优化会把策略推向 misspecification 极值。
- **sealed eval**：预先冻结 reference objective、审计预算与重评分比例，训练过程不得查看 sealed 标签。
