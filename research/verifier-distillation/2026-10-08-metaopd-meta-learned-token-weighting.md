# MetaOPD: Meta-Learned Token Weighting for On-Policy Distillation

- **作者**：Zipeng Wang；Xinpeng Dong；Yuefan Wang；Pingchen Lu；Xian Wei；Kun Kuang；Fei Wu；Zhongxiang Dai；Min Zhang
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.11989
- **Canonical URL**：https://arxiv.org/abs/2610.11989
- **代码**：未发现公开代码链接

## 一句话结论

MetaOPD 用双层优化从验证目标中学习逐 token 的蒸馏权重，说明 OPD 的关键不只是“是否跟 teacher”，而是“哪些 student-generated token 值得接受多强的 teacher 信号”。

## 真正新增的内容

【论文原文】作者不再以人工启发式规则按熵、置信度或 teacher–student gap 设权，而是训练一个 token-weighting network：内层执行加权 OPD 虚拟更新，外层以参考解上的验证损失反向优化权重网络。

【分析推断】这把 score-level verifier distillation 的“监督强度函数”变成可学习组件，可用于学习从序数评分分布、环境真值和策略熵到蒸馏权重的映射。

## 核心方法

1. 在 student 的 on-policy rollout 上计算 teacher–student 蒸馏损失与 token 特征。
2. 权重网络为每个 token 产生非负权重，内层据此做一次虚拟 student 更新。
3. 用虚拟更新后的 student 在参考答案上的损失作为外层目标，反向更新权重网络。
4. 再用更新后的权重完成真实 student 更新，形成 bilevel training。

## 关键实验结果

【论文原文】实验覆盖 6 个数学基准、3 个 OOD 基准、2 个 student 尺度与 7 个基线。相对普通 OPD，0.6B student 的 Avg@8 / Pass@8 平均提高 1.99 / 5.97 个百分点，1.7B student 提高 2.25 / 6.41 个百分点。

## 证据质量与局限

【论文原文】多基准、双尺度和较完整的基线比较提高了证据可信度。  
【局限】外层目标依赖参考解，尚未证明在长时程 Agent、稀疏终局奖励或 verifier 本身会漂移的闭环中仍稳定；权重网络也可能过拟合验证分布。论文未直接评估 A/B/T、序数分布或 sealed eval。

## 最接近的相关工作

最接近普通 OPD、Unified Per-Token OPD Gating、TV-Regulated OPD、UECR-GRPO 与 RoboDrop。区别在于 MetaOPD 由验证损失学习 token 权重，而不是固定地使用熵、总变差、teacher gap 或梯度相容性。

## 如何复用或推进 LLM-as-a-Verifier

可把权重网络输入扩展为：student/teacher score 分布、A/B/T 概率、环境 oracle 是否可用、critique 是否通过证据检查、以及多 Judge 分歧。外层目标应优先使用冻结的程序化真值或独立人工/环境标签，避免权重网络只学会迎合在线 verifier。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：新增“可学习权重”臂，与 uniform、entropy gate、teacher–student gap gate 对照。
- **A/B/T 与序数分布**：将类别熵、期望分、相邻等级质量与 T 概率作为权重输入，而不是先压成单一标量。
- **程序化/环境真值门控**：外层元目标使用执行真值；无真值样本只提供软幅度，不决定更新方向。
- **student-generated critique states**：仅对经证据指针与环境重放验真的 critique 开启高权重。
- **高熵分叉**：高熵不应自动降权；若外层显示其能改善 sealed validation，应保留并加权这些探索状态。
- **sealed eval**：元训练验证集与最终 sealed eval 必须隔离，冻结 evaluator、任务和 harness，防止权重网络共适应。

总体判断：【分析推断】这是现有 score-level verifier × OPD 路线最直接的可学习门控基线之一，但必须把外层监督从“参考答案损失”升级为环境真值锚定的独立目标。