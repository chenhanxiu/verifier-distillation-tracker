# UP-MOPD: Update Projection in Multi-Teacher On-Policy Distillation

- 作者：Taojie Zhu、Jing Jin、Yuan Xia、Chenyang Ding、Qunshan He、Wanke Xia、Tao Sun、Yan Chen、Jian Wang、Jinjie Gu、Tao Feng
- 首次公开日期：2026-10-06
- 版本日期：2026-10-06（v1）
- 原始论文：https://arxiv.org/abs/2610.08398
- Canonical URL：https://arxiv.org/abs/2610.08398
- 代码：https://anonymous.4open.science/r/UP-MOPD/

## 一句话结论

【论文原文】多 teacher OPD 的冲突应约束 AdamW 实际候选位移而非原始梯度；UP-MOPD 在提交参数前投影违规更新，优于梯度投影和更新拒绝。

## 真正新增的内容

【论文原文】论文指出经梯度修正后的方向，仍会被 momentum、自适应缩放与 weight decay 转成一阶增加某域损失的实际更新；因此把可行性检查移动到 optimizer 产生候选 displacement 之后。

## 核心方法

【论文原文】混合梯度照常更新 optimizer state 并生成候选位移；若候选对任一 teacher/domain 的一阶损失约束违规，只投影候选位移，取欧氏距离下最接近候选的唯一可行更新，再提交参数。

## 关键实验结果

【论文原文】医疗+通用域实验后期 IFEval-loose 比 vanilla M-OPD 高 2.96 点；八项平均 60.03，对比梯度投影 59.00、更新拒绝 59.15。数学、代码、指令遵循六任务公开基准平均 32.67，LiveCodeBench v5 最优，IFEval 并列最优。

## 证据质量与局限

【论文原文】有跨域与公开多任务比较，并直接对照两类冲突处理。【分析推断】约束依赖局部一阶近似，欧氏投影未考虑参数尺度/Fisher 几何；尚未证明多个 verifier teacher 的偏差相关或环境真值冲突时仍安全。

## 最接近的相关工作

【分析推断】最接近 VG-OPD、Lightning Weave、SCOPE-OPSD 与一般多任务 PCGrad 类方法；本文独特处是投影 optimizer displacement。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将不同 verifier（执行真值、pairwise judge、序数分布、风险模型）视作独立约束：允许共享 optimizer state，但提交前禁止任何高可信信号的一阶退化。可按可信度给硬约束与软约束分级。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：新增 gradient projection、update rejection、update projection 三臂消融。
- 【分析推断】A/B/T：分别追踪每类标签损失，避免多数 A/B 更新损害稀有 T。
- 【分析推断】真值门控：程序/环境真值作为不可违反硬约束，LLM teacher 作为软约束。
- 【分析推断】critique states：只有不恶化证据一致性的 critique 更新才提交。
- 【分析推断】高熵分叉：以“不得损害探索域”约束阻止单 teacher 吞并多策略。
- 【分析推断】sealed eval：冻结约束定义，在独立任务上报告各域损失变化而非只报平均分。