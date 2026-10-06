# Transfer-Stratified On-Policy Distillation for RL-Improved Reasoning Teachers

- 作者：Xiaoyu Chen、Bo Shao、Tiangang Zhu、Bintao Wu、Linjun Shou、Fengge Wu、Feng Sun、Wenbiao Ding
- 首次公开日期：2026-10-05
- 当前版本日期：2026-10-05（v1）
- arXiv：2610.05974
- 原始论文：https://arxiv.org/abs/2610.05974
- Canonical URL：https://doi.org/10.48550/arXiv.2610.05974
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】更强的 RL teacher 并不会自动带来更好的 dense distillation；TS-OPD 按 student/teacher 联合成功状态区分能力获得与巩固，分别路由 forward/reverse KL，并用 entropy brake 保留覆盖。

## 真正新增的内容

【论文原文】论文把 teacher 改进的“可迁移性”从单一能力差拆成结构化状态：acquisition problems 使用门控 forward KL，consolidation problems 使用门控 reverse KL，且明确保护 pass@K 覆盖。

## 核心方法

【论文原文】根据 student 与 teacher 的 sampled success 对训练题分层；不同层采用不同 KL 方向与 token gate，并添加熵制动。消融显示收益来自路由和 token gating，而不是简单跳过问题。

## 关键实验结果

【论文原文】在主要比较中，使用 GRPO 改进 teacher 时，TS-OPD 获得最高宏平均正确率；pass@K 结果更混合，说明平均性能与覆盖不能合并解读。

## 证据质量与局限

【论文原文】包含 teacher RL 前后谱系、多个 student 尺度、直接 GRPO 与多种 OPD 目标。局限是主要为数学推理；分层依赖有限采样成功率，可能误分类；宏平均最优不等于高熵探索或长轨迹成功最优。

## 最接近的相关工作

最接近 CompassOPD、TV-Regulated OPD、RetireOPD、Unified Per-Token Gating，以及 DCSD 的方向/幅度分离。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】Agent 状态也应按“student失败/teacher成功、双方成功、双方失败、teacher失败”分层；不同层决定蒸馏方向、强度或拒绝监督，而非统一使用 teacher 分数。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：【分析推断】把联合成功后验加入 score gate，并比较 FKL/RKL 路由。
- **A/B/T 与序数分布**：【分析推断】有限 rollout 形成成功后验；样本不足的层标 T。
- **硬真值门控**：【分析推断】联合成功必须由环境/程序结算，而非同源 Judge。
- **critique states**：【分析推断】teacher 仅在 student 失败而自身可验证成功的状态生成 critique。
- **高熵探索**：【分析推断】保留 entropy brake，并将 pass@K 与宏平均并列验收。
- **sealed eval**：【分析推断】用未见任务重新估计分层迁移矩阵，防止路由规则对训练集过拟合。
