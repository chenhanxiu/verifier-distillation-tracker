# Hints, Critics, and Teachers: Prior Injection for Sparse-Reward RL in Vision-Language Math Reasoning

## 基本信息

- 作者：Qiqian Fu
- 首次公开日期：2026-08-22
- 版本日期：2026-08-22（v1）
- arXiv：2608.21811
- 原始论文：https://arxiv.org/abs/2608.21811
- DOI：https://doi.org/10.48550/arXiv.2608.21811
- 代码：论文公开页未提供

## 一句话结论

在 85%–97% rollout 组全错的极稀疏奖励区间，真正决定收益的是先验是否有效到达策略；分类式 HL-Gauss critic 比 MSE critic 高 14.4 点，而常用 in-domain 切片甚至与跨域迁移负相关。

## 真正新增的内容

**论文原文结论：** 在完全相同训练条件下比较文本 hint、7B teacher 的 on-policy distribution distillation 和 value critic 共 11 个方法，分离“先验类型”与“先验是否真正传递到 policy”的影响，并发现评测切片可能颠倒方法排序。

**分析推断：** 对现有路线最重要的不是再叠加一种 teacher，而是监测 teacher 信号经过 gate、loss 和优化后是否实际改变 student；同时分类/分布式 value target 比单点 MSE 更适合稀疏成功率。

## 核心方法

在 Qwen2-VL-2B 的同一稀疏奖励池中控制训练预算，对比 reference hint、OPD teacher distribution、MSE critic 与 HL-Gauss categorical critic，并用 in-domain 子集和 DynaMath 跨域集进行盲评与配对检验。

## 关键实验结果

- 20,830 道视觉数学题中基础模型仅 3.6% rollout 正确，85%–97% GRPO 组全错。
- 有效接收到先验的 6 个方法与先验被截断、门控掉或 critic 配置错误的 5 个方法在域内和跨域表现上完全分离。
- HL-Gauss critic 相对 MSE critic域内提升 14.4 点。
- 常用 general-distribution 切片与跨域迁移 Spearman ρ=-0.74（n=11，p=0.011），最难切片则为 ρ=+0.89（p<0.001）。

## 证据质量与局限

证据质量中等偏高：同条件 11-arm 对照、盲评和统计检验较强。局限是单作者、视觉数学领域且基础成功率极低；摘要未给出 OPD 各变体的完整绝对分数，不能据此宣称某一先验普遍最优。

## 最接近的相关工作

最接近 I-SDPO、Distill Where You Fail、RG-OPD、PAST，以及 distributional critic/HL-Gauss value learning。新增价值是统一比较 prior delivery 和暴露评测切片反转。

## 如何复用或推进 LLM-as-a-Verifier

为每批 teacher 信号增加“传递审计”：记录 gate 通过率、student 分布变化、梯度贡献与最终环境结果；将 value verifier 输出改为序数/分类分布，并保留熵而非只拟合均值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 必须报告 teacher 信号覆盖率和实际梯度贡献，防止 gate 形同虚设。
- **A/B/T 与序数分布：** 优先比较 categorical/ordinal critic 与 MSE 标量 critic。
- **真值门控：** 对全失败组注入先验，但用后续环境成功验证其方向。
- **Student critique states：** hint/critique 是否被 student 使用需通过行为变化验证。
- **高熵探索：** hint-guided exploration 的收益提示应保留多路径，而非直接复制 teacher。
- **Sealed eval：** 不以单一域内切片选模型；使用冻结的困难集和跨域集防止“未改变即得分”。
