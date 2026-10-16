# Training-Free On-Policy Distillation：用 on-policy 二阶矩闭式融合专家

- **论文标题**：Training-Free On-Policy Distillation
- **作者**：Bangji Yang, Jiajun Fan, Zhaoyu Zhu, Hongbo Ma, Ge Liu
- **首次公开日期**：2026-10-15
- **版本日期**：2026-10-15（v1）
- **原始论文**：https://arxiv.org/abs/2610.22236
- **代码**：论文页面未提供公开代码链接

## 一句话结论

共享基座的多个 specialist 可以只用各自在自身答案上的前向 rollout 二阶矩，通过逐层最小二乘闭式融合，而无需梯度训练；但 rollout 中少量重复循环会因 token 占比过大严重污染结果。

## 真正新增的内容

**论文原文**：把多 specialist 的 on-policy consolidation 写成每个线性层的最小二乘问题，使融合模型在该 specialist 读取自己回答时的输入上复现其层输出；只需数百条 rollout 的二阶矩和前向计算。

**分析推断**：对 verifier 蒸馏而言，这给出“先融合多个专域 verifier，再做少量校准”的廉价基线，也揭示状态覆盖与轨迹 token 质量比求解器复杂度更重要。

## 核心方法

对每个 specialist 收集其自生成回答上的层输入，累计二阶统计量，逐层求解共享模型权重，使每个专家在自身 on-policy 状态上的输出被联合拟合；不进行反向传播。

## 关键实验结果

**论文原文**：Olmo 3 7B 上，每个 specialist 只需几 GPU 小时的前向计算，融合 generalist 在七个数学与代码基准中保留了各专家的大部分增益。去除数学 specialist rollout 中少量但 token 占比很高的重复截断样本后，融合模型 AIME25 表现从接近任务算术模型提升到匹配 specialist（相同精度）。

## 证据质量与局限

方法有解析结构且覆盖七个基准；但要求专家共享基座/层结构，摘要未展示异构 tokenizer 或生成式 verifier 的适用性。它融合的是行为表示，不自动解决错误专家、校准漂移或独立真值验证。

## 最接近的相关工作

与 One-Shot/Data-free OPD 的状态覆盖结论、Lightning Weave 的多专家能力位移组合、GVPO++ 的异构序列 OPD，以及 RM-OPD 的专域 reward-model consolidation 最接近。

## 如何复用或推进 LLM-as-a-Verifier

可把 pointwise、pairwise、critique 与安全 specialist 先按各自真实 on-policy 评价输入收集二阶矩，构造无训练融合 verifier；随后只对序数概率校准层做小规模真值监督。重复循环、空洞 critique 和无证据长回答应在统计量累计前过滤。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：加入“闭式层融合 + 小型校准头”作为低成本多 teacher 基线。
- **A/B/T 与序数分布**：分别收集各协议的 on-policy 状态，避免由长文本协议的 token 数量主导融合。
- **真值门控**：二阶矩按 sealed oracle 通过率或 teacher 不变性加权。
- **critique states**：过滤重复、无证据及解析失败的 critique，防止它们在 token 加权下过度影响。
- **高熵探索**：按状态而非 token 均衡采样，使稀有高熵分叉不会被长而低价值的轨迹淹没。
- **sealed eval**：融合求解、校准和最终评测三份数据严格隔离，并报告专家单体、闭式融合和再校准三层结果。
