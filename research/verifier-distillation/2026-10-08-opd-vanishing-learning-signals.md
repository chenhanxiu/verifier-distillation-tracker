# Why On-Policy Distillation Sometimes Fails: Vanishing Learning Signals

- **作者**：Lei Zhao；Qichao Zhao；Bowen Zuo；Qishi Zhan
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.11247
- **Canonical URL**：https://arxiv.org/abs/2610.11247
- **代码**：https://github.com/leizhao7/opd-learning-signals

## 一句话结论

OPD 失败未必是 teacher 不够强，而可能是 student 在自身轨迹上几乎收不到可积累的梯度信号；持续观察 loss 远远不够，必须监控有效梯度与表示变化。

## 真正新增的内容

【论文原文】作者识别出“大 teacher 反而早期 loss plateau”的现象，并用连续时间动力学分析代理梯度信号为何在损失仍高时衰减；同时给出 teacher 足够接近 student 时的局部恢复保证。

【分析推断】对 verifier 蒸馏而言，应把“判决分歧”与“可学习信号”分开：高分歧样本可能只有噪声或梯度抵消，不能仅凭 teacher–student gap 加权。

## 核心方法

1. 对不同来源与能力差距的 teacher 执行 on-policy distillation。
2. 跟踪训练损失、代理梯度信号、参数位移和表示相似度。
3. 用连续时间模型解释 student 访问分布与蒸馏梯度共同演化时的信号消失。
4. 分析近邻 teacher 条件下的局部恢复，并提出需要用“可学习性”筛选 teacher/状态。

## 关键实验结果

【论文原文】训练 200 步后，大 teacher 设置的平均最终 loss 仅下降 25.1%，而 self-RL teacher 设置下降 96.2%。失败设置中的参数相对变化仅 0.025%–0.098%，linear CKA 仍高于 0.98，显示模型几乎没有发生有效表征更新。

## 证据质量与局限

【论文原文】机制分析、训练诊断与理论结果相互印证，并公开代码。  
【局限】局部保证依赖 teacher 接近性假设；代理梯度指标是否能泛化到生成式 verifier、序数分布和非平稳 Agent 轨迹尚未验证。CKA 高也不能单独证明所有能力都未变化。

## 最接近的相关工作

最接近 OPD、PACT 的 critic–policy 对齐、RetireOPD、CompassOPD、TV-Regulated OPD 与 Unified Per-Token OPD Gating。它把焦点从 KL 方向或 teacher 质量转向“训练信号是否真正进入 student”。

## 如何复用或推进 LLM-as-a-Verifier

在 verifier 蒸馏仪表板中加入：每状态梯度范数、梯度方向一致性、有效样本率、参数/表示位移、判决分布熵。若 teacher 分歧大但有效梯度持续消失，应切换到中间 teacher、缩短 continuation、加入硬真值方向信号或暂时退役 teacher。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：除分数校准外，记录 score loss 对共享表示的实际梯度；把“信号存活率”列为核心指标。
- **A/B/T 与序数分布**：检查各等级质量是否产生抵消梯度；T 应作为拒绝/路由，而非被强压成中间分。
- **程序化/环境真值门控**：当软 teacher 梯度消失时，以可验证终局奖励决定方向，但限制其幅度以避免稀疏奖励震荡。
- **student-generated critique states**：优先保留既能通过证据门控、又产生非退化梯度的 critique 状态。
- **高熵分叉**：高熵状态应按信息增益与梯度有效性联合采样，而不是只按熵。
- **sealed eval**：独立评测需同时报告最终性能与训练动力学，防止仅用在线 verifier loss 掩盖“无学习”。

总体判断：【分析推断】这篇论文要求现有路线新增“梯度可用性审计”；否则任何 gating 或 teacher 组合都可能在表面有分歧、实际无更新。