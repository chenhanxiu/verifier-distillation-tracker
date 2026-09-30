# Dr. OPD: Learning What to Follow for Optimal On-Policy Distillation of Large Language Models

- **作者**：Zhenyu Wang, Tianze Wang, Linjun Zhang, Yifan Hu
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2609.38025
- **代码**：未发现公开代码链接

## 一句话结论

Dr. OPD 把“哪些 teacher token 值得跟随”写成以最终期望奖励为外层目标的双层优化，并在强到弱蒸馏中比等权 OPD 平均提高 9.7 个数学性能点。

## 真正新增的内容

【论文原文】标准 OPD 等权使用所有 token 级 teacher 信号；本文学习 token 权重，使一次加权蒸馏更新直接服务于学生的期望奖励。作者给出交替更新权重与策略的高效求解器，并在正则条件下证明加权更新优于 vanilla OPD 更新。

【分析推断】它把 score-level verifier 从“给整条轨迹一个系数”推进到“估计每个 teacher 位移对真实回报的边际价值”，是现有 verifier × OPD 路线中最直接的权重学习基线。

## 核心方法

外层选择 token 权重以最大化更新后学生的期望奖励，内层按这些权重最小化 teacher–student 蒸馏损失；每轮先闭式更新权重，再执行一步学生梯度更新。

## 关键实验结果

【论文原文】在数学和代码、强到弱与同尺寸蒸馏设置中均优于所有评测基线；强到弱设置平均数学成绩比 vanilla OPD 高 9.7 点，小模型学生可超过大模型 teacher。

## 证据质量与局限

【论文原文】有理论局部改进保证和跨两类任务的实证，但摘要未报告 Agent 长轨迹、不同 verifier 噪声或 sealed evaluator 下的结果。【分析推断】权重若由同一个可被优化的 reward 产生，仍可能学习 reward hacking；需要独立硬真值和冻结评测验证。

## 最接近的相关工作

TV-Regulated OPD、UECR-GRPO、BATON、RetireOPD，以及按不变性门控 teacher 信号的 IWD。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 输出的序数分布、置信区间或环境结算信号进入外层奖励，而不是直接把 Judge 分数当真值；比较等权、轨迹级权重、token 级权重三种方案的校准与收益。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：直接实现“verifier 分数决定蒸馏强度”的可学习版本。
- **A/B/T 与序数分布**：可将 A/B/T 的后验胜率或序数期望作为外层收益，但 T 应对应低权或不更新。
- **硬真值门控**：建议由程序/环境真值决定更新方向，学习权重只决定幅度。
- **student-generated critique states**：可把 critique token 的权重单独学习，并要求其改善后续执行回报。
- **高熵探索**：对高熵分叉设置权重上限，避免单一 teacher 位移压平多种可行策略。
- **sealed eval**：权重训练器与最终 evaluator 必须隔离；冻结任务、种子和 grader 后再报告增益。
