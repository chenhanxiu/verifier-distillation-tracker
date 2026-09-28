# MOPD-Router: Rethinking Teacher Routing in Multi-Teacher On-Policy Distillation

- **作者**：Tianze Xu, Yanzhao Zheng, Zhentao Zhang, Yuanqiang Yu, Chao Ma, Jihuai Zhu, Lelun Wu, Lyumanshan Ye, Pengfei Liu, Baohua Dong, Hangcheng Zhu, Ruohui Huang, Gang Yu
- **首次公开日期**：2026-09-25
- **版本日期**：2026-09-25（v1）
- **原始论文**：https://arxiv.org/abs/2609.30837
- **代码**：https://github.com/TURLEing/MOPD-Router

## 一句话结论

【论文原文】MOPD-Router 在每个 student token 上评估完整 teacher 池，并以 ExpertAlign 衡量“teacher 修正是否体现其后训练获得的专长”，无需域标签或额外 router 即可优于整段硬路由。

## 真正新增的内容

【论文原文】它把多 teacher OPD 的路由粒度从 prompt/rollout 降到 token，并统一比较 Entropy、Novelty 与新提出的 ExpertAlign；后者通过 teacher 相对其共享 pre-RL base 的能力位移来识别真正的专长方向。

## 核心方法

1. 所有 teacher 对同一 student-generated token 给出 OPD 信号。
2. Entropy 路由偏向更自信的 teacher；Novelty 衡量共享 top-k 支持上的 teacher–student 差异。
3. ExpertAlign 比较 teacher 修正方向与其后训练专长位移的一致性，据此选择和加权。
4. 不训练单独 router，也不依赖训练样本的域标签。

## 关键实验结果

【论文原文】在无标签/有标签混合、strong-to-weak/same-size 共四种设置中，ExpertAlign 的总体表现均最佳。无标签数据上比 Mean aggregation 高 5.88 点（+12.3%）；即使有域标签，也在不使用标签的情况下比标准 MOPD 高 3.95 点（+7.8%）。

## 证据质量与局限

【论文原文】覆盖四个路由设置并公开训练代码，证据较强。局限是使用同一 Qwen3 系列与共享 base，ExpertAlign 是否能跨模型族、跨 tokenizer 或跨闭源 teacher 稳定工作仍未证实；最终分数也不能替代独立环境真值。

## 最接近的相关工作

最接近 VG-OPD、Lightning Weave、CompassOPD 与标准 MOPD。它比 prompt 级专家分配更细，比单纯 entropy routing 多利用 teacher 的后训练能力位移；与跨族校正方法互补。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把不同 verifier 视为专长 teacher：程序 oracle、轨迹 Judge、安全 Judge、证据 Judge 各自产生 score/ordinal 分布；ExpertAlign 可路由“当前状态该听谁”。但专长位移必须由 sealed calibration set 估计，不能用同一在线策略数据自证。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：建立 per-state/per-token 多 verifier 加权基线，而非先把 teacher 分数求均值。
- **A/B/T 与序数分布**：对每个 teacher 保留完整 A/B/T 或 ordinal 分布，再按可靠性混合；不要先硬化标签。
- **真值门控**：程序/环境 oracle 对更新方向拥有否决权，ExpertAlign 只决定软信号来源和幅度。
- **Critique states**：不同 specialist 可分别监督证据、错误定位与修复建议，路由器决定当前 critique 维度。
- **探索**：teacher 权重接近或总体熵高时保留多分支采样，而非强制选单一专家。
- **Sealed eval**：路由权重校准集、训练集与最终 evaluator 必须隔离，并报告跨模型族迁移。
