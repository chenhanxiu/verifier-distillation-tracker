# SimpleOPD：面向长上下文推理的简单、分词器无关 On-Policy Distillation

## 基本信息

- **论文标题**：SimpleOPD: Simple Tokenizer-Agnostic On-Policy Distillation for Long-Context Reasoning
- **作者**：Haonan He, Haodi Lei, Yun Luo, Haoran Zhang, Shunkai Zhang, Yizhuo Li, Shengji Tang, Zhilin Wang, Runzhe Zhan, Lei Bai, Ganqu Cui, Fangchen Yu, Yafu Li, Peng Ye, Ning Ding, Yu Cheng
- **首次公开日期**：2026-08-14
- **版本日期**：2026-08-14（arXiv v1）
- **arXiv ID / DOI**：2608.14277 / 10.48550/arXiv.2608.14277
- **原始论文**：https://arxiv.org/abs/2608.14277
- **项目页**：https://hhnqqq.github.io/SimpleOPD-project-page/
- **代码**：https://github.com/hhnqqq/SimpleOPD

## 一句话结论

SimpleOPD 证明跨分词器、长教师到短学生的 OPD 可以只在共享文本跨度上对齐，再用 student-reference KL 与终止 token 掩码抑制长度爆炸；它为异构 Agent verifier 的 score/logit 级蒸馏提供了直接的工程模板，但尚未在 Agent 轨迹或 verifier 任务上验证。

## 真正新增的内容

**论文原文结论：**

1. 不要求 teacher 与 student 共享词表，而是在字符/文本空间定位两边完全相同的跨度，只对这些可比位置构造 teacher 分数。
2. 直接 OPD 在长序列上会出现输出持续变长、终止 token 缢失和截断；论文用 student-reference KL 保留学生原分布，并将 `</think>`、`<|im_end|>` 等终止 token 的优势置零。
3. 方案不依赖先生成 teacher 轨迹做 SFT，可直接沿 student rollout 做 PPO 式更新。

**本文分析推断：**

这里最值得复用的不是“数学能力迁移”本身，而是“异构表示下只在可信公共支撑集蒸馏”的原则。对 verifier，可把共享文本跨度换成共享事件、工具调用或状态边界，避免对 tokenizer/轨迹切分不一致的位置强行逐 token 对齐。

## 核心方法

学生从自己的策略生成 rollout；教师在同一前缀上评分。跨 tokenizer 时，将 token 映射到文本区间，只保留 teacher 与 student 边界一致的区间，构造可比较的 log-prob 差作为优势，再用 PPO clipping 更新学生。

稳定化包含两项：

- student-reference KL：约束训练后策略不要远离原 student，缓解 teacher–student 分布不匹配；
- termination-token advantage masking：终止 token 不参与优势驱动，避免“为了匹配教师”而不断延长输出。

## 关键实验结果

**论文报告：**

- SU-01 蒸馏到 Qwen3、Qwen3.5、Intern-S2、GLM-4.7 与 Gemma-4 等多种学生，覆盖同 tokenizer、跨 tokenizer 和跨模型家族。
- Intern-S2-Preview 在 Gemini-2.5-Pro judge 下的 ProofBench 从 34.0 升至 55.2（+21.2）；在论文主表的另一评测设置中从 21.70 升至 44.50。
- Qwen3.5-35B-A3B 的 ProofBench 从 26.78 升至 42.39；GLM-4.7-Flash 从 30.8 升至 39.7。
- Gemma-4-26B-A4B 的 ProofBench 从 25.5 升至 34.2，但 AnswerBench 从 68.8 降至 67.5，说明较大的 tokenizer 差异仍会损伤部分能力。
- 加入 reference KL 后，ProofBench@4 从 21.70 升至 38.50，并改善 AnswerBench/AIME25；论文还展示了朴素 OPD 产生 160k token 循环输出的失败案例。

## 证据质量与局限

证据强项是学生家族多、含同/跨 tokenizer 对照、消融和退化案例，并同时覆盖可验证与 judge-based 基准。代码与模型已公开。

局限包括：

- 训练与主结论集中在数学证明/问答，不是 verifier 蒸馏或长时程工具 Agent；
- ProofBench 部分结果依赖模型 judge，虽做四次重复取均值，仍可能受 judge 偏差影响；
- 不同表格使用不同 judge/协议，55.2 与 44.5 不应直接混为同一测量；
- 跨 tokenizer 只利用边界完全一致的跨度，可能系统性丢失高信息但切分不一致的位置；
- 未报告独立 sealed evaluator，也未研究 teacher 与 evaluator 共适应。

## 最接近的相关工作

- On-Policy Distillation（Agarwal et al., 2024）
- EOPD：在 teacher 高熵位置补充 forward KL，强调覆盖支撑集
- G-OPD：引入灵活 reference model 与 reward scaling
- LOPD：长上下文 OPD 的长度与稳定性问题
- Draft-OPD：以 verification-error replay 训练 speculative draft model

与这些工作相比，SimpleOPD 的差异点是跨 tokenizer 文本跨度对齐，以及对终止行为与 student reference 的极简稳定化。

## 如何复用或推进 LLM-as-a-Verifier

- **score-level 蒸馏**：在共享“事件跨度”而非 token 上蒸馏 teacher 的标量分数、分位点或 ordinal logits；不匹配区间应标为缺失，而不是插值成伪标签。
- **pairwise A/B/T 与序数分布**：先把两条轨迹对齐到相同环境状态/工具返回，再蒸馏 A 胜、B 胜、Tie 的分布；reference KL 可防止学生把全部概率压到单一类别。
- **critique states**：让 student 生成 critique，再由 teacher 在同一 critique 前缀上打分；跨 tokenizer 只对可比的句子/事件边界更新。
- **长轨迹终止**：把“终止 token 掩码”改成对 STOP/提交动作单独校准，避免蒸馏目标诱发无意义延长。

## 对现有 Agent verifier × OPD 实验路线的具体影响

1. **score-level on-policy verifier distillation**：可直接采用“公共支撑集 + reference KL”，优先验证异构 teacher/student tokenizer 时的校准误差、排序一致性和 OOD 稳定性。
2. **A/B/T 与序数评分分布**：将 loss 限制在共享状态锚点；Tie 应保留为分布质量，不应因 token 对齐缺失而被硬拆成 A/B。
3. **程序化/环境真值门控**：仅当共享锚点前后的环境状态一致时接受 teacher 信号；工具返回不一致的跨度不进入蒸馏。
4. **student-generated critique states**：沿学生自己的错误/批评轨迹查询 teacher，符合 on-policy 原则；同时保存未对齐率作为数据质量指标。
5. **高熵分叉保留探索**：reference KL 有助于保留原策略支撑，但 SimpleOPD 的 reverse-KL/PPO 仍可能压缩多样性；建议在高熵节点加入 EOPD 风格 forward-KL 或最低熵约束。
6. **sealed eval**：训练 teacher、在线 verifier 与最终评估器必须隔离；至少以冻结的程序检查器和未参与训练的 judge 双轨评估，防止“更会迎合 teacher”被误判为轨迹质量提升。

## 结论边界

论文足以支持“跨 tokenizer OPD 可行且长序列稳定化重要”，但不能支持“该方案已改善 Agent verifier、序数奖励分布或长时程决策”。后者是基于方法结构提出的实验迁移建议。
