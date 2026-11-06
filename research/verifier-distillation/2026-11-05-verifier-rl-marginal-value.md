# Measuring the Marginal Value of Verifier-Based RL Beyond Supervised Fine-Tuning

- **作者**：Amit Sagtani, Saloni Garg
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.07639
- **DOI**：https://doi.org/10.48550/arXiv.2611.07639
- **代码/配置**：论文声称归档了可复现实验配置，但论文页所指公开仓库在本次检查时无法确认可访问

## 一句话结论

在一个确定性、程序化 partial-credit verifier 的 GPU 调试 benchmark 上，SFT 已吸收大部分可学信号，后续 verifier-RL 对 IID 无可检测增益，仅对 OOD 有小幅但可测改善。

## 真正新增的内容

论文不再把 RLVR 与 SFT 当替代方案，而是直接测量“完成 SFT 后，RLVR 还增加多少”；并在 pilot 结果出现后书面修订、预注册完整实验问题与尺度。

## 核心方法

构建 gpu-train-debug：1,877 个合成 GPU/LLM 训练故障诊断任务、30 类 archetype，由确定性程序 verifier 给 partial credit。比较 base、1,200 gold demonstrations 的 SFT，以及固定步数和学习率的 GRPO，并分别报告 IID/OOD 差值与置信区间。

## 关键实验结果

- hard split 上 SFT 达 **0.785**。
- pilot 中 base 为 **0.311**，15-step cold GRPO 为 **0.314**，几乎无变化。
- 预注册完整实验中，SFT 后 GRPO 的 IID 增益为 **+0.22 个百分点**，95% CI **[-0.06, +0.51]**。
- OOD 增益为 **+0.33 个百分点**，95% CI **[+0.02, +0.68]**。

## 证据质量与局限

**论文原文结论**：确定性 verifier、预注册修改、置信区间与完整对照使“边际价值”估计较可信。  
**局限**：单一合成调试域、有限 GRPO 配置与规模；小效应不能推出 RLVR 普遍无效。公开代码链接当前不可确认，也削弱即时复现性。

## 最接近的相关工作

最接近的是 RLVR/GRPO、SFT→RL 两阶段训练、Ground-truth-as-code、AutoGym，以及研究 OPD 是否应在 RL 前后使用的工作。

## 如何复用或推进 LLM-as-a-Verifier

将“verifier 能给多少 SFT 之外的新信息”设为核心指标：先用同一 oracle 生成 demonstrations，再测试 on-policy 分支是否产生训练集未覆盖的错误模式。可把 ordinal partial credit 分解为独立子项，并报告每项的 OOD 边际收益。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD/RL 必须对比强 SFT，并报告增量而非只报相对 base 的总提升。
2. pairwise A/B/T 数据应优先来自 SFT 后仍高熵、且环境真值能区分的 on-policy 分叉。
3. critique states 若只是复述 gold demonstrations，价值有限；应覆盖 OOD failure archetype。
4. sealed eval 要保留完全未用于 verifier、SFT 或课程构造的 OOD split，并给置信区间。
5. 若 IID 边际收益接近零，应把预算转向新状态覆盖、verifier 校准和 OOD 分叉，而非继续增加同分布 RL 步数。