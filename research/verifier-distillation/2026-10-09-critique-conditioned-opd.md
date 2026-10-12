# A Privileged Teacher That Only Scores Cannot Search: Critique-Conditioned On-Policy Self-Distillation for Reasoning

- **作者**：Mayug Maniparambil；Ayush Rai；Ekansh Verma；Noel E. O'Connor；Fergal Reid
- **首次公开日期**：2026-10-09
- **版本日期**：2026-10-09（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.13744
- **Canonical URL**：https://arxiv.org/abs/2610.13744
- **代码**：未发现公开代码链接

## 一句话结论

仅让 privileged teacher 给 student rollout 打分并不会自动产生纠错信用；先要求 teacher 搜索并生成 critique，再以 critique 条件化评分，才能定位错误、压低错误 token，并提高回溯 token 的概率。

## 真正新增的内容

【论文原文】作者使用 student rollout 的 gold error span，直接检验 self-distillation 常用的 full-distribution KL 与 token log-ratio 是否满足两项要求：定位错误、把概率从错误 token 移开。两类信号均失败，且不能可靠区分同题中的正确与错误 rollout。

【论文原文】同一个 teacher、同一份 privileged reference，在允许生成 critique 后显著改善错误定位；critique-conditioned scoring 随后产生真正纠错的 token 信号。

【分析推断】这为 student-generated critique states 提供了最直接的机制证据：critique 不是附加解释，而是把“全局评分”转化为“局部搜索后信用”的中间状态。

## 核心方法

1. 在带 gold error span 的 student rollout 上分析原始 teacher KL/log-ratio。
2. 分别评估错误定位能力和对错误 token 的梯度方向。
3. 让同一 privileged teacher 先生成针对当前 rollout 的 critique。
4. 将 critique 加入 teacher 条件，再计算分布差异并蒸馏回 student。
5. 在错误前缀续写和 cold-start GRPO 中检验 critique 是否提供可用的修复/优势信号。

## 关键实验结果

【论文原文】普通 scoring teacher 的 KL 与 token log-ratio既不能定位错误，也不能在错误 span 内可靠地把概率推离错误 token；critique-conditioned 信号则改善定位并提高 “Wait”“But”“Actually”等回溯起始 token 的概率。该 critique 在测试时能修复仅靠采样无法解决的数学题，也能在可验证奖励全为零的 cold-start prompt 上提供 advantage。

## 证据质量与局限

【论文原文】使用 gold error span 做机制级验证，比只报告最终准确率更能证明信用信号是否正确。  
【局限】实验集中于数学推理；gold error span 在开放式 Agent 轨迹中昂贵且可能不唯一。生成 critique 仍可能合理化错误，且摘要未证明 critique-conditioned teacher 在真实工具环境、长期副作用和分布外状态上保持校准。

## 最接近的相关工作

最接近 SELF、PaperDoctor、EnGRICH、FLARE、RC-OPD、Agent Error Dataset、TIPS 与 Caddie。区别在于本工作直接证明“只评分”的 privileged teacher 缺乏搜索能力，并把 critique 设为产生局部蒸馏信号的必要条件。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 分为两阶段：先输出带证据指针的错误搜索结果，再输出 A/B/T 或序数评分分布。critique 必须引用具体工具结果、状态差异或未完成义务；随后用环境重放验证其定位。只有通过验证的 critique 才用于 score-level OPD。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：加入“直接打分 teacher”与“critique-conditioned teacher”对照，分别测梯度定位率和实际修复率。
- **A/B/T 与序数分布**：critique 找不到可验证错误时输出 T，而非凭整体印象给中间分；评分分布保留证据覆盖度。
- **程序化/环境真值门控**：错误定位必须由重放、状态 diff 或确定性检查确认；语言 critique 只提出候选。
- **student-generated critique states**：将“错误位置—证据—修复建议—重放结果”作为新的训练状态，拒绝无证据自由反思。
- **高熵分叉**：在多种 critique 均可解释失败时保留多个修复分支，以环境结果决定方向。
- **sealed eval**：使用独立错误注入、隐藏环境真值和冻结 critic 评估定位与修复，防止 critique teacher 与 student 共适应。

总体判断：【分析推断】这篇论文直接验证了现有路线中 critique state 的必要性；下一步最值得做的是把 gold span 换成 Agent 环境中的可重放首错证据。