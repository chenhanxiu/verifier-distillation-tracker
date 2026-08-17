# Wrong but Useful：超越答案正确性的多 Agent 消息轨迹价值

## 基本信息

- **论文标题**：Wrong but Useful: Trajectory Value Beyond Answer Correctness in Multi-Agent Messages
- **作者**：Chih-Hsuan Yang, Anjir Ahmed Chowdhury, Cheng-Hau Yang, Weijian Zheng, Fernando Llorente, Xiaolong Ma, Xinyang Li, Eliu A. Huerta, Ian T. Foster, Rajeev Thakur
- **首次公开日期**：2026-08-14
- **版本日期**：2026-08-14（arXiv v1）
- **arXiv ID / DOI**：2608.14375 / 10.48550/arXiv.2608.14375
- **原始论文**：https://arxiv.org/abs/2608.14375
- **代码/复现材料**：论文未给独立 GitHub；arXiv ancillary files 附带完整代码、配置、测试与派生数据：https://arxiv.org/abs/2608.14375

## 一句话结论

一个局部答案可以是错的，却通过分解、约束或原理帮助下游 solver 得到正确结果；用“保留/隐藏消息后重放同一 integrator”的反事实差分，比局部正确性更接近长时程 Agent 中真正需要蒸馏的轨迹价值。

## 真正新增的内容

**论文原文结论：**

- 提出 Diverse Hypothesis Deliberation（DHD）：缓存五条独立消息，在其余条件匹配时，让同一 downstream integrator 分别看到完整消息池或隐藏其中一条。
- 把两种重放的最终正确性差定义为该消息在特定“消息池–integrator”上下文中的 trajectory value。
- 五个数学/科学基准、两个开放模型家族中都发现 wrong-but-helpful 消息；局部答案正确性不能决定轨迹价值。
- 完整消息的帮助最大；只保留 reasoning 比只保留 answer 更能维持成功，但完整消息优势的机制仍未完全解释。

**本文分析推断：**

这项工作可直接转成 Agent verifier teacher 信号：在同一环境快照上对某个 action/critique/工具结果做 keep、remove 或 replace 重放，以环境后果差作为训练标签。它尤其反对在高熵分叉中仅按“当前看起来错”剪枝。

## 核心方法

每题生成五条角色化、相互独立的候选消息，随后固定 integrator 条件，比较完整池与 leave-one-out 池的答案。为量化随机重放噪声，论文又在每个模型家族的 1,000 道题上做五个匹配 block；每题 35 次观察，包含重复 full-pool 和五种 one-removal 条件。

独立 evaluator 只判断答案等价，不看 agent reasoning；reasoning agent 不看真值或 evaluator 判断。论文还做 answer masking、reasoning masking、中性替换、重复效应和交叉拟合 keep/remove 诊断。

## 关键实验结果

**论文报告：**

- wrong-helpful 在 5 个基准 × 2 个模型的全部 10 个组合中出现。
- 在会改变最终正确性的 wrong-answer 消息中，两个模型都有超过 40% 的变化是有帮助的。
- 可重复消息效应的数量显著超过 block 内置换控制，`p=0.0002`。
- 10 个可重复 wrong-helpful anchor 上：完整消息成功率 82%；隐藏错误答案为 64%；隐藏 reasoning 为 44%；等长中性替换 46%；完全移除 26%。该小样本只用于机制诊断，不是总体发生率估计。
- 用四个重复 block 选择“全保留或删除一条”，第五个 block 测试，准确率对 gpt-oss-120b 提升 1.68 点、对 Gemma 提升 2.61 点；基于答案正确性的比较器仅提升 0.94 和 1.00 点。
- 标题摘要中的结论与附录敏感性分析一致：轨迹价值含有超出答案正确性的可重复信息。

## 证据质量与局限

证据强项包括大规模 leave-one-out 样本（91,740 条 OSS、83,020 条 Gemma eligible messages）、匹配重放、同输入噪声基线、置换检验、组件遮蔽、完整复现 artifact 和两个模型家族。

论文明确的局限：

- trajectory value 是“消息–消息池–integrator”上下文属性，不是文本固有属性；换 integrator 或池后符号可能改变；
- 重复只能降低、不能消除随机性；
- keep/remove 改进复用了同一问题，衡量的是 same-problem opportunity，不是未见问题上的泛化策略；
- leave-one-out 一次隐藏整条消息，固定提示顺序；reasoning/answer 分离仅做了较小诊断。

此外，任务仍是短程数学/科学 deliberation，不含真实工具调用、长环境反馈或成本约束。

## 最接近的相关工作

- multi-agent debate、self-consistency 与候选聚合
- leave-one-out / Shapley 式贡献估计
- process reward model 与 outcome reward model
- counterfactual credit assignment、difference rewards
- message selection / routing 与 learned communication
- 《Not Every Divergence Should Be Suppressed》中的反事实可恢复性评估

相较仅用 outcome correctness 或 judge score 的方法，DHD 用下游干预结果定义局部贡献；相较完整 Shapley 估计，它只做 one-removal，成本更低但交互归因不完整。

## 如何复用或推进 LLM-as-a-Verifier

- 用 DHD 产生高质量 teacher labels：从环境快照复制两条分支，分别 keep/remove 某个 critique 或 action，比较最终成功、成本和安全约束。
- 将二元差分扩展为 ordinal distribution：显著改善、轻微改善、Tie、轻微伤害、显著伤害，并保留重放置信区间。
- 对 A/B/T 训练，A/B 分别对应保留两个候选，T 由效应区间重叠或差异低于实用阈值定义，而非单次 judge 打平。
- 让 generative verifier 输出“为什么该错误消息仍有用”，但最终标签由反事实环境重放门控，避免解释自洽替代真实贡献。

## 对现有 Agent verifier × OPD 实验路线的具体影响

1. **score-level on-policy verifier distillation**：teacher target 应从局部正确率改成条件化 trajectory-value 分布；student 在自己生成的错误 critique/action 上学习最有价值。
2. **pairwise A/B/T 与序数评分分布**：采用成对重放的差值与 bootstrap 区间，显式建模 Tie 和不确定性，不把单次随机翻转当标签。
3. **程序化/环境真值门控**：最终成功、约束满足、工具状态和资源消耗应由程序/环境读取；LLM evaluator 仅用于真值不可得的语义等价部分。
4. **student-generated critique states**：优先采样 student 的错误但高潜力 critique；DHD 说明这类样本不是噪声，可能正是教 verifier 学会长期信用分配的关键。
5. **高熵分叉保留探索**：禁止按当前答案正确性或 teacher–student divergence 单点剪枝；先保留一部分 wrong/high-entropy 分支做 matched replay，再学习选择策略。
6. **sealed eval**：复用论文的角色隔离，并进一步冻结最终 evaluator、隐藏测试环境种子与任务；训练用 integrator 与 sealed integrator 分开，检测 evaluator/integrator 共适应。

## 结论边界

论文强力支持“局部正确性不等于条件化轨迹价值”，但不证明 DHD 标签能跨 integrator、跨任务或跨环境泛化。把它作为 verifier 蒸馏 teacher，需要报告重放成本、置信区间、上下文迁移与 sealed integrator 结果。
