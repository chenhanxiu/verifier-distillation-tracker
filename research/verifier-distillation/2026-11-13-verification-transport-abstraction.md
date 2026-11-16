# Do Verifier Judgments Survive Abstraction? Measuring Verification Transport for LLM Agent Evaluation

- **作者**：Disha Sheshanarayana、Sai Linisha Reddy Goli
- **首次公开日期**：2026-11-13
- **版本日期**：2026-11-13（v1）
- **原始论文**：https://arxiv.org/abs/2611.18471
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.18471；DOI: 10.48550/arXiv.2611.18471

## 一句话结论

【论文原文】同一条冻结 Agent 执行轨迹只因工具组合、委托或历史压缩而改变可观测表示，就可能产生最高约 31% 的 verifier 迁移失败；恢复执行溯源可挽回 85.5% 的失败。

## 真正新增的内容

【论文原文】论文提出 **Verification Transport**：在任务、真实执行、结果、ground truth、评价准则与 verifier 全部固定时，构造 native、abstracted、restored 三种匹配视图，单独测量“执行证据跨抽象边界后，判断是否仍成立”。它还区分错误 verdict 与 abstention，避免把“少做判断”误解为更可靠。

【分析推断】这补上了现有 Agent verifier × OPD 路线中的一个隐藏变量：蒸馏目标可能不是因行为质量改变而漂移，而是因训练/部署所见轨迹表示不同而漂移。它应被视为独立于常规准确率的 verifier 验收轴。

## 核心方法

1. 冻结同一批执行及其真值，生成原生、宏观抽象、委托和恢复视图。
2. 在 7 个 verifier backbone、4 种验证协议上比较判断迁移，包括 direct、evidence-grounded 与 deliberative 等协议。
3. 将 transport failure 分解为错误判断与弃权，并测试完整或有损 provenance 恢复后的可逆性。

## 关键实验结果

【论文原文】实验覆盖 4 个 Agent 评测基准、7 个 verifier、4 种协议和 3 类抽象边界；宏观抽象与委托下迁移失败最高约 31%。直接验证更常产生错误 verdict，证据化与审议式协议在可观测性不足时更倾向 abstain。恢复对应执行溯源可挽回 85.5% 的迁移失败，有损或缺失 provenance 时恢复率下降。

## 证据质量与局限

【论文原文】控制变量设计很强：真实轨迹、结果、真值和 verifier 均保持不变，因而可把差异较干净地归因于可观测表示。论文被 NeurIPS 2026 “Who Verifies the Agents?” workshop 接收。

【分析推断】研究测量的是判断稳定性而非 verifier 蒸馏后的下游策略收益；摘要未说明全部任务分布、置信区间及长期在线共适应。稳定也不等于正确，因此 transport 指标必须与 ground-truth accuracy、abstention cost 和 sealed outcome eval 联合报告。

## 最接近的相关工作

最接近的是 DENSE 的证据化轨迹压缩、Grounding Agent Memory 的证据准入、Agent 轨迹可诊断性的 abstention 规则，以及 Agreement Overstates Evidence 与 MAWILE 对 Judge 可靠性的审计。本文区别在于保持执行与真值不变，只改变轨迹抽象层，直接测量 verifier judgment 的跨表示迁移。

## 如何复用或推进 LLM-as-a-Verifier

把 native/abstracted/restored 三联视图加入 verifier 训练与回归测试；要求 generative verifier 输出 verdict、证据指针、可观测性缺口和 abstention。对序数评分同时蒸馏分布与“证据是否足够”的门控，不将抽象视图上的低分直接解释为行为失败。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：同一状态在多种轨迹表示下的 score 应保持可校准；不稳定样本降低蒸馏权重。
- **pairwise A/B/T 与序数分布**：原生与抽象视图发生翻转时标为 T/不可判，而非伪造 A/B；保留 abstention 概率。
- **环境真值门控**：更新方向由冻结执行和环境结算决定，verifier 只在可观测证据充分时调节幅度。
- **student-generated critique states**：critique 必须携带可恢复的事件、工具与委托 provenance；压缩前后做 transport test。
- **高熵探索**：表示不稳定不能被误当作策略不确定性；两者分开估计，避免压制合理分叉。
- **sealed eval**：加入模型未见过的抽象边界和有损 provenance 条件，并冻结 verifier 与轨迹渲染器。

