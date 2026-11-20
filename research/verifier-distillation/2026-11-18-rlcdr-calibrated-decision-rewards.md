# Calibrated Decision Rewards: Training Language Models with a Judge That Knows How Sure It Is

- **作者**：Rudransh Agnihotri, Manasvi Kapoor
- **首次公开日期**：2026-11-18
- **版本日期**：2026-11-18（v1）
- **原始论文**：[arXiv:2611.25135](https://arxiv.org/abs/2611.25135)
- **DOI**：[10.48550/arXiv.2611.25135](https://doi.org/10.48550/arXiv.2611.25135)
- **代码**：论文页面未提供公开代码链接

## 一句话结论

【论文原文】把 LLM Judge 改造成经少量标签校准、直接输出选项概率分布的 decision model，可在 on-policy 样本上提供接近答案键效果的 reference-free RL 奖励；【分析推断】这是现有 score-level verifier distillation 从“未校准标量”升级为“可审计序数/类别分布”的强直接基线。

## 真正新增的内容

【论文原文】RLCDR 不把 Judge 的任意分数当概率，而是让模型回答类型化判定问题（如“最终答案是否正确”“第一处错误在哪一步”），一次前向读取完整选项分布；再通过选项顺序去偏与约百个标签做校准。作者同时在不断变化的当前策略样本上检查校准，而不只报告静态 held-out 准确率。

【分析推断】关键新增不是“再用一次 LLM-as-a-Judge”，而是把 reward 的语义、概率空间和校准协议绑定起来，使 reward 可进入分布蒸馏、拒答/平局决策及动态路由。

## 核心方法

【论文原文】

1. 把评价任务写成带明确选项的 decision question，读取选项概率分布；
2. 交换选项顺序并聚合，降低位置偏差；
3. 用小规模标注做后校准；
4. 将校准后的正确概率用于 GRPO 奖励，并在 policy 分布变化后复测 ECE；
5. 同一模型还可输出第一处错误位置的分布，而无需专门的 step-level 训练。

## 关键实验结果

【论文原文】

- Qwen3-1.7B 在 MATH 上经 GRPO 训练后，MATH500 从 72.2% 提升至 76.8%，与答案键奖励 76.9% 接近；随机奖励仅提升 0.65 点。
- 最难等级从 44.8% 提升至 51.7%。
- 在策略自身不断变化的样本上，ECE 为 0.074，而同一 27B backbone 的 softmax Judge 为 0.141。
- 未做 step training 时，第一错步定位在 ProcessBench 上 F1 0.772，高于专用 7B PRM 的 0.722。
- 在主要由 base model 失败样本构成的分布上仍提升 1.9 点，但落后答案键，且出现过度自信。

## 证据质量与局限

【论文原文】优点是预先陈述六个假设并为每个设计可证伪控制，同时报告显著性、随机奖励、答案键奖励、校准误差和困难分布失效边界。局限是主要证据集中在数学推理、单一小模型和判定式选项空间；“无 reward hacking 迹象”不等于已证明在更长训练或 Agent 环境中安全。

【分析推断】迁移到长轨迹前仍需验证：选项集合不完备时的概率含义、同一 Judge 对自身 critique 的共适应，以及环境变化后的再校准成本。

## 最接近的相关工作

- RLAIF / LLM-as-a-Judge reward：同样用模型反馈训练策略，但通常把打分直接当奖励。
- Process reward model 与 ProcessBench：提供步骤级监督或首错定位。
- ordinal probabilistic reward model：共同目标是保留完整评分分布而非压成单点。
- Calibration Is Not Verification、Rethinking Verbalized Confidence：分别强调一致性不等于真值，以及不同置信信号需实测校准。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 Agent verifier 的输出改为联合分布：任务完成等级、首错阶段、证据充分性与可恢复性；用程序/环境真值抽取少量锚点做在线温度或等距校准。训练时蒸馏分布本身，并保留熵作为路由到昂贵 teacher、生成 critique 或触发环境重放的信号。

## 对现有 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level on-policy verifier distillation**：以校准后的类别概率或期望序数分替代未校准标量，并在每轮 policy 更新后复测 ECE。
- **pairwise A/B/T 与序数评分分布**：直接输出 A/B/T 或多级质量的完整分布；T 应同时覆盖平局与证据不足，但需拆分记录。
- **程序化/环境真值门控**：硬真值用于校准与越界否决，软 Judge 分布用于幅度和信用分配。
- **student-generated critique states**：先预测“首错位置”分布，再只在高后验步骤生成 critique，减少无关自我修订。
- **高熵分叉保留探索**：高熵不应立刻压成单一偏好；保留多个分支或升级 teacher。
- **独立 sealed eval**：冻结独立 Judge、校准集和环境结算器，报告 on-policy ECE 与 sealed 成功率，避免训练 Judge 与策略共同变得自洽而非正确。
