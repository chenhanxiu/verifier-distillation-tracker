# Can We Trust the Teacher? Decoupled Credit Direction-Magnitude for Self-Distillation

- **作者**：Yugu Li, Zehong Cao, Peizhen Li, Yang Zhang, Siyi Hu, Jianglin Qiao
- **首次公开日期**：2026-09-28
- **版本日期**：2026-09-28（v1）
- **原始论文**：https://arxiv.org/abs/2609.34848
- **代码**：未在 arXiv 页面提供

## 一句话结论

【论文原文】DCSD 将 step/token 信用的方向与幅度拆开：belief-margin probing 决定方向，marginal information gain 决定贡献大小，再用两者校准 privileged teacher。

## 真正新增的内容

【论文原文】论文从理论上指出直接让 teacher 同时决定信用正负与大小，会把判断错误和偏好方差耦合进更新；新增的是两条独立信号及 step-to-token 信用映射。

## 核心方法

1. 用 belief-margin probing 判断一步应被奖励还是惩罚。\n2. 用 marginal information gain 衡量该步对结果的贡献幅度。\n3. 两者分别校准 teacher 信号，再映射到 token credit。\n4. 与 RLVR 的可靠轨迹级信用联合做策略优化。

## 关键实验结果

【论文原文】跨 11 个 benchmark 总体优于 GRPO、OPSD、RLSD、RLCSD；相对 base，数学推理总分提高 8.45 点、多模态推理提高 7.01 点；修正 6% token 的信用方向，并把 token 信用幅度压缩 1.5 倍。

## 证据质量与局限

【论文原文】含理论分析与广泛 benchmark，能直接检验方向修正。局限是摘要未显示长时程工具 Agent 证据；belief margin 与 information gain 是否受同一 teacher 偏差污染需要独立审计。

## 最接近的相关工作

最接近 TV-Regulated OPD、UECR-GRPO、SIGNBALANCE 与 RoboDrop；共同支持“可靠信号定方向、软信号定幅度”。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把程序/环境真值用于方向 head，把 ordinal verifier 的分布宽度、证据增量和反事实差用于 magnitude head；两头分别校准并分别做 sealed audit。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：拆分 sign 与 scale 两个学习目标。\n- **A/B/T 与序数分布**：A/B 决定方向，T 或高熵压低幅度。\n- **真值门控**：硬 oracle 对方向拥有否决权。\n- **Critique states**：critique 仅提高信息增量时才获得幅度。\n- **探索**：高熵状态可保留方向不确定性而非强推。\n- **Sealed eval**：分别报告方向错误率与幅度校准误差。
