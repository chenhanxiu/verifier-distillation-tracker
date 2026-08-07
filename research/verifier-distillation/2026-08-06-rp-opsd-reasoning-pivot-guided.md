# RP-OPSD：Reasoning-Pivot-Guided On-Policy Self-Distillation for Multilingual Reasoning Transfer

## 基本信息

- **作者**：Xinye Wang、Junxiao Liu、Shujian Huang
- **首次公开日期**：2026-08-06
- **当前版本日期**：2026-08-06（arXiv v1）
- **arXiv ID**：2608.06347
- **原始论文**：https://arxiv.org/abs/2608.06347
- **代码**：https://github.com/NJUNLP/RP-OPSD
- **记录类型**：新论文（2026-08-07 检出）

## 一句话结论

RP-OPSD 用同一模型在“有/无英语参考解”的两个 teacher view 之间的分布差异定位 reasoning-pivot token，只在高价值位置蒸馏、其余位置锚定原策略；这为 Agent verifier × OPD 提供了一个有用的选择性更新原型，但 pivot 仍是 privileged-context proxy，并非环境验证的因果关键状态。

## 真正新增的内容

**论文原文结论：**跨语言推理蒸馏不应在所有 token 上等强度进行。作者以 privileged 英语解答对 teacher 分布造成的变化作为“推理枢纽”信号，并使用 token-level gate：高 gate token 接收完整分布蒸馏，低 gate token 回到冻结 reference policy，从而同时传递推理知识并保护目标语言表面形式。

其新意主要是把“哪里值得蒸馏”内生化为两个 teacher view 的 KL 差异，而不再依赖外部 token 标注或对所有生成位置做均匀 KL。

**分析推断：**该 gate 可以迁移为 Agent 轨迹上的“teacher 信息价值”估计：比较 teacher 在加入环境真值、程序执行结果或 critique 前后的 verifier 分布变化，从而决定哪些分叉/时间步应更新。不过论文没有证明该差异等价于因果 credit，也没有直接训练 reward/verifier 模型。

## 核心方法

1. 学生模型从目标语言问题出发生成 on-policy rollout prefix。
2. 构造两个参数共享、stop-gradient 的 teacher view：
   - (q^+)：目标语言问题、英语翻译、当前 rollout prefix，加上英语参考解；
   - (q^-)：相同上下文，但不含英语参考解。
3. 以 (KL(q^+\|q^-)) 计算每个 token 的 Privileged Reasoning Score（PRS），再经归一化/门函数形成选择性权重。
4. 高 PRS 位置让 student 拟合 (q^+) 的完整词表分布；低 PRS 位置用冻结 reference policy 约束，减少语言漂移与无关行为变化。
5. teacher 与 student 仍来自同一基础模型，rollout 由当前策略生成，因此属于 on-policy self-distillation。

## 关键实验结果

**论文报告：**

- 在 17 种语言的 AfriMGSM 与 PolyMath 上，Qwen3-1.7B 的 RP-OPSD 平均分别达到 **19.07 / 17.97**，高于 COPSD 的 **16.70 / 15.99** 和 EGRSD 的 **16.40 / 16.31**。
- Qwen3-4B 上分别达到 **26.83 / 31.87**，对比 COPSD 的 **21.63 / 29.94** 与 EGRSD 的 **22.68 / 30.16**。
- 对 gate 的定向消融中，选择 PRS 最高 20% token 的结果（SWA **26.0**、FRA **74.8**）优于随机 20%（**20.8 / 74.0**）和最低 20%（**15.6 / 73.2**），说明差异信号确实富集了更有效的训练位置。
- 完整方法在对应消融设置中达到 **29.6 / 76.8**；移除 reference anchoring 后降至 **27.6 / 73.6**，支持“选择性学习 + 非关键位置保持”而非无约束全局蒸馏。

上述数字来自论文的特定模型与评测表，不能直接外推为一般 Agent 成功率。

## 证据质量与局限

- 优点：包含两种模型规模、两个多语言数学基准、多个蒸馏基线，以及 top/random/bottom gate 和 anchoring 消融；对 token 选择机制有较直接的证据。
- 局限：主要结论来自多语言数学推理，没有工具调用、长时程环境反馈或开放式 Agent 轨迹。
- PRS 衡量“加入英语参考解后预测分布改变多少”，不是环境真值、因果贡献或 verifier 校准；高差异也可能来自格式、翻译或措辞变化。
- 方法仍需要外部英语参考解，因而不属于完全无监督自蒸馏。
- 论文评估的是任务正确性与语言表现，没有报告 ordinal reward calibration、A/B/T 一致性、长轨迹 credit assignment 或 evaluator 共适应。
- 代码已公开，有利于复现；但新论文尚缺独立重复实验和跨模型家族验证。

## 最接近的相关工作

- **OPSD / context on-policy distillation**：都在 student 自己的状态上用 privileged context 形成 teacher 分布。
- **Selective knowledge distillation / token reweighting**：按 token 价值调节蒸馏强度；RP-OPSD 的区别是以 privileged-view KL 自动产生权重。
- **Privileged information distillation**：训练时 teacher 可见部署时 student 不可见的信息。
- **COPSD、EGRSD**：论文直接比较的多语言推理自蒸馏方法。
- **Process reward modeling / temporal credit assignment**：同样试图定位关键步骤，但通常学习显式过程分数或使用环境标签，证据来源不同。

## 如何复用或推进 LLM-as-a-Verifier

可把 (q^+) / (q^-) 从 policy-token 分布改成 verifier 的序数评分分布：

- (v^-)：只看 student 当前轨迹前缀；
- (v^+)：额外看程序执行结果、环境状态差分、隐藏测试或 teacher critique；
- 以 (KL(v^+\|v^-))、JSD 或 posterior entropy reduction 作为“verification pivot score”；
- 只在高 pivot 状态蒸馏完整评分分布或生成式 critique，在低 pivot 状态对原 verifier 加 trust-region anchoring。

这比直接复制论文 token gate 更贴合 LLM-as-a-Verifier，因为它定位的是新增可验证证据改变判断的位置。需要额外做校准，防止 judge 对文字风格敏感导致虚假高 pivot。

## 对 Agent verifier × OPD 实验路线的具体影响

1. **Score-level on-policy verifier distillation**：RP-OPSD 强化了“选择性 score distillation”方向。可在 student rollout 上比较有/无环境证据的 teacher ordinal distribution，仅对信息增益高的状态更新。
2. **Pairwise A/B/T 与序数评分分布**：把单 token PRS 扩展到分叉对。若新增证据显著改变 A/B 排序，标为高价值；若 posterior 重叠则保留 T，而不是硬造偏好。
3. **程序化/环境真值门控**：环境证据应取代英语参考解成为 (v^+) 的 privileged input。只有真值可审计且分布变化显著时，才把该 pivot 当可靠 teacher signal。
4. **Student-generated critique states**：让 student 先生成 critique，再比较 teacher 在加入 critique 前后的分布；但必须用环境结果区分“有说服力”与“真的纠错”。
5. **高熵分叉下保留探索**：reference anchoring 为此提供了可操作机制。低证据/低 pivot 分叉保持原策略概率，高置信被证伪分叉才压低；通过测试的多种策略应设为 tie 并保留熵。
6. **Sealed eval**：pivot teacher、训练 verifier 与最终 evaluator 需分离。尤其不能用同一 judge 的分布差异选训练点，再用它证明改进；应以隐藏环境 seed 和独立 judge 测成功率、校准与语言/策略漂移。

## 建议的最小验证实验

在含工具调用的长轨迹中，对每个时间步构造三种 verifier view：仅轨迹、轨迹 + student critique、轨迹 + 可执行环境证据。用 ordinal-distribution JSD 选择前 20% pivot 状态，比较全状态蒸馏、随机 20%、高 pivot 20%，并为其余状态加 frozen-verifier anchoring。sealed eval 同时报告终态成功率、pairwise A/B/T 准确率、ECE、有效策略分支数和 critic–environment 冲突率。
