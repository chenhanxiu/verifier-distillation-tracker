# OPMD：超越输出监督的 On-Policy Mechanism Distillation

- **论文标题**：OPMD: On-Policy Mechanism Distillation Beyond Output Supervision
- **作者**：Yingdong Shi, Zhihong Li, Changming Li, Jingyi Yu, Quan Li, Kan Ren
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2610.14022
- **代码**：论文摘要未给出公开链接
- **标识符**：arXiv:2610.14022；DOI: https://doi.org/10.48550/arXiv.2610.14022

## 一句话结论

OPMD 不只蒸馏 teacher 的 next-token 分布，而是先把 teacher 中间计算映射成 student 下游网络真正可用的状态，再在 student 自生成轨迹上内化这些机制。

## 真正新增的内容

**论文原文结论**：直接表示匹配会受 teacher/student 几何差异和“对齐但不可用”问题限制；OPMD 构造 student-compatible teacher，将 teacher 表示变换为 student 后续计算可消费的中间状态，并在 on-policy 轨迹中蒸馏。三组 teacher–student 设置中平均准确率均优于所评估蒸馏基线，并扩展到多 teacher 与跨家族 SFT。

**分析推断**：这是对纯 score-level OPD 的重要补充，但尚不能证明机制表示本身等价于可靠 verifier 信号；它更适合作为“受硬真值门控的辅助通道”。

## 核心方法

1. 从 student 自身策略采样前缀，保持 on-policy 状态分布。
2. 学习 student-compatible teacher，将 teacher 中间表示变换到 student 后续层可利用的状态。
3. 同时进行输出/机制层监督，使 student 内化可执行的中间计算而非仅模仿答案概率。

## 关键实验结果

- 三个 teacher–student 设置中，OPMD 的平均准确率均为所比较蒸馏方法最高。
- 支持多 teacher 蒸馏与跨模型家族 SFT。
- 表示与解题策略分析显示 student 的中间计算发生实质变化。

## 证据质量与局限

**论文原文**包含多设置与机制分析，证据强于单一 benchmark；但摘要未给出具体绝对分数、计算开销与长时程 Agent 环境结果。中间状态“可用”不等于“正确”，teacher 机制偏差仍可能被更深地固化。

## 最接近的相关工作

最接近 SCOPE-OPSD 的特权子空间蒸馏、GVPO++ 的序列级 OPD、Lightning Weave/TrustMOPD 的跨 teacher 组合，以及 CompassOPD 的跨家族位移校正。

## 如何复用或推进 LLM-as-a-Verifier

- 将 verifier 的“证据定位—错误类型—修复方向”隐状态映射成 student-verifier 可消费状态。
- 把机制损失仅施加在环境真值明确、teacher 校准通过的样本上。
- 对 A/B/T 或序数分布，机制通道用于解释排序依据，输出头仍负责校准概率。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：新增一个三臂消融：仅 score-level OPD、仅机制蒸馏、两者联合。机制通道应由程序/环境真值硬门控，teacher 信号只调节幅度；在高熵分叉上保留多种成功机制，避免状态塌缩。student-generated critique states 可作为机制蒸馏载体，但须通过证据可追溯与执行复现准入。sealed eval 应跨模型家族并冻结环境与 evaluator，验证机制迁移是否提升真实成功率而非只提高同源 probe 可读性。