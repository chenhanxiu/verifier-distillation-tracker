# Code Owns the Simulation, Jev Owns the Evaluation

- **作者**：Yaodong Yang, Hongyao Tang, Yi Ma, Xingyu Fan, Weixun Wang, Jinpeng Li, Tianpei Yang
- **首次公开日期**：2026-10-01
- **版本日期**：2026-10-01（v1）
- **原始论文**：https://arxiv.org/abs/2610.01834
- **代码**：未发现公开代码链接

## 一句话结论

Jev 擅长评价输入中已经描述的候选，却不擅长在同一次调用里先模拟隐藏后果再评价；用代码提供 lookahead 后，它可成为强动作选择器。

## 真正新增的内容

【论文原文】作者在反思测试、矩阵博弈、ALFWorld 和机器人控制中识别出 evaluation/simulation 边界。Jev 能独立预测对手行动，也能在得到该行动后正确评价，但把两步放进一次调用就失败。

【分析推断】序数概率 verifier 不应承担世界模型职责；现有 Agent evaluator 应明确拆成“环境/代码生成后果”和“概率模型评价后果”。

## 核心方法

跨四类任务比较纯 Jev 选择、单独模拟问答和代码/物理模拟提供后果后的 Jev 评价，检查概率式快速 Judge 的能力边界。

## 关键实验结果

【论文原文】Jev 在反直觉 Cognitive Reflection Test 上达到 99%；ALFWorld 中会因任务词面直接选择 drawer 而跳过洗刀。加入 ALFWorld lookahead 或机器人物理模拟后，其一般评价能力可形成专家控制器。

## 证据质量与局限

覆盖离散推理、博弈、文本 Agent 和机器人，边界一致；但研究针对一个商业模型版本，摘要未提供全部任务的绝对对照和校准误差。

## 最接近的相关工作

JEV-as-a-Judge、JEV Agent Trace Security、FARM、HaWMPO、Reality Is the Final Verifier。

## 如何复用或推进 LLM-as-a-Verifier

构建两阶段架构：程序/世界模型枚举候选后果，Jev 或 ordinal verifier 只对已显式化后果打分；同时单独校准 simulation error 与 evaluation error。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：只在后果已由环境/代码生成后使用 Jev score。
- **A/B/T 与序数分布**：对相同显式后果做 A/B/T；缺失关键后果时必须 T。
- **硬真值门控**：simulation 由程序、环境或可审计 world model负责。
- **student-generated critique states**：critique 可解释评价，但不得臆造未观察状态。
- **高熵分叉**：高熵时增加真实 lookahead，而不是让 Judge 自行想象。
- **sealed eval**：分别冻结 simulator 与 evaluator，并做交叉组合测试以识别共适应。
