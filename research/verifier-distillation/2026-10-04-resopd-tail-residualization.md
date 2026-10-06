# ResOPD: Tail Residualization for Sparse On-Policy Distillation

- 作者：Penghui Yang、Long Xing、Xuanlang Dai、Ziyu Liu、Kai Chen、Yuhang Zang
- 首次公开日期：2026-10-04
- 当前版本日期：2026-10-04（v1）
- arXiv：2610.04882
- 原始论文：https://arxiv.org/abs/2610.04882
- Canonical URL：https://doi.org/10.48550/arXiv.2610.04882
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】ResOPD 在只传 sampled token 或 Top-k 的稀疏 teacher 接口下，将未观测词表聚合为可计算的 tail event，并采样尾部残差，以无偏估计 full-vocabulary reverse-KL 梯度且降低方差。

## 真正新增的内容

【论文原文】它解决稀疏 OPD 的核心两难：sampled-token 无偏但高方差，Top-k 低成本却系统有偏；tail residualization 在不增加 teacher 查询或 forward pass 的情况下恢复无偏性。

## 核心方法

【论文原文】对 Top-k 外词表先计算精确聚合梯度，再仅采样 tail 内细粒度残差；作为可插拔方差缩减模块用于 on-policy reverse KL。

## 关键实验结果

【论文原文】在论文所测设置中显著降低梯度方差、稳定在线训练并提升下游表现；摘要未给出统一提升数字。

## 证据质量与局限

【论文原文】方法目标清晰、具有无偏梯度性质，并覆盖多实验设置。局限是主要解决通信/估计问题，不直接处理 teacher 错误；尾部分布聚合在异构 tokenizer、极长动作 schema 或 score-level verifier 上仍需额外验证。

## 最接近的相关工作

最接近 RouteOPD、GVPO++、Low-Bit OPD，以及稀疏 token-level OPD 接口。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】对于只返回 Top-k ordinal score 或少量候选动作的 verifier，可增加“其余类别”聚合桶并采样桶内残差，避免把未返回候选默认为零概率。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：【分析推断】将未观测评分尾部作为显式 residual mass，避免 Top-k verifier 偏置。
- **A/B/T 与序数分布**：【分析推断】T/其他类别保留聚合概率，而非丢弃。
- **硬真值门控**：【分析推断】无偏估计不能修复错误 teacher，仍需硬门控。
- **critique states**：【分析推断】可稀疏传输高价值 critique token，同时保留尾部质量。
- **高熵探索**：【分析推断】tail mass 是探索信号，不能在 Top-k 截断中消失。
- **sealed eval**：【分析推断】比较稀疏估计与完整分布的校准误差、策略覆盖及最终成功率。
