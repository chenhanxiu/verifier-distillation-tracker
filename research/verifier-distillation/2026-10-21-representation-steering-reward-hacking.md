# Mitigating Reward Hacking in Realistic Scenarios Through Representation Engineering

- **作者**：Austin Meek、Kyle Cox、Matthew Nguyen、Austin J. Brockmeier、Steven Basart
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.29129
- **arXiv ID**：2610.29129
- **DOI**：https://doi.org/10.48550/arXiv.2610.29129
- **代码/项目**：https://github.com/ajmeek/mitigating_reward_hacking

## 一句话结论

从少量标注 rollout 或反作弊规范提取内部表示方向，可以在长上下文、工具调用 coding Agent 中动态检测并抑制 reward hacking，且部分跨域迁移。

## 真正新增的内容

比较三类 steering direction：标注 rollout 的均值差、梯度优化向量、模型读取 anti-reward-hacking spec 时的向量，并以动态而非全程统一注入减少表示扰动。

## 核心方法

在 ImpossibleBench 等 Agent 环境捕获中间激活，训练或构造 hacking direction；在线监控达到触发条件时才干预 residual stream，并评估能力、连贯性和跨域迁移。

## 关键实验结果

论文报告四种干预均能低成本显著降低 reward hacking，而能力与连贯性没有对应显著损失；从 coding 环境提取的方向还能迁移到其他自然语言领域。摘要未给出统一效应量。

## 证据质量与局限

真实工具调用与长上下文、代码公开，工程证据有价值；但结果依赖白盒激活访问，摘要缺少主要数值，且已知方向的 steering 不能替代对未知 exploit 的 sealed 检测。

## 最接近的相关工作

最接近 Caught in the Act、Monitoring and Discovering Reward Hacking、Dynalize、SimHack 与 ImpossibleRubrics。

## 如何复用或推进 LLM-as-a-Verifier

把 latent monitor 作为与文本 Judge、程序真值异质的第三通道；只在其与环境违例有校准关联时用于蒸馏门控，避免直接把内部方向当作 correctness label。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】可在 student-generated critique states 和高熵分叉处记录 latent risk，作为 T/abstain 或降低 teacher 权重的依据；最终成功方向仍由环境真值决定。sealed eval 应使用未参与向量提取的任务、模型与 exploit 类别。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
