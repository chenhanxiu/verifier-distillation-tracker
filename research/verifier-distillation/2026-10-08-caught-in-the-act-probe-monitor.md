# Caught in the Act: Probes Effectively Detect Sabotage and Catch Unverbalized Deception

- **作者**：Oskar J. Hollinsworth；Alex F. Spies；Tigist Diriba；Adam Gleave；Chris Cundy
- **首次公开日期**：2026-10-08
- **版本日期**：2026-10-08（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2610.12445
- **Canonical URL**：https://arxiv.org/abs/2610.12445
- **代码与数据**：https://github.com/AlignmentResearch/caught-in-the-act-probes

## 一句话结论

跨层、跨 token 聚合的白盒表示探针在 Agent sabotage 轨迹上达到 98.8% AUC，并能识别未口头表达的隐藏目标，说明长轨迹 verifier 不应只读可见文本，还应保留一个机制异质的内部状态监控通道。

## 真正新增的内容

【论文原文】作者构建迄今规模最大的 deception probe 训练集，并提出可聚合多个网络层和多个 token 信息的新探针架构；评测不仅包括从文本上下文可判断的 sabotage，还包括只能通过模型内部目标或训练信息确定的“introspective deception”。

【分析推断】这为 Agent verifier × OPD 路线增加了第三类 teacher 信号：除环境真值和语言 Judge 外，还可使用内部表示风险分布，但它只能承担筛查或路由，不能未经因果验证直接充当最终正确性标签。

## 核心方法

1. 从 Agent sabotage、隐藏目标和受压陈述等场景收集带真值的表示—行为样本。
2. 从多个 transformer 层、多个轨迹 token 读取激活，而非只取单层末 token。
3. 用聚合探针预测 deception/sabotage 风险，并与强文本监控器比较。
4. 在上下文本身不足以确定答案的 introspective deception 上测试探针是否读取到了未语言化信号。

## 关键实验结果

【论文原文】探针在 SHADE-Arena 上达到 98.8% AUC，超过 Opus 5.5 文本监控基线；在包含模型真实隐藏目标的 transcript 识别任务上，最高达到 99.7% AUC。作者还报告，底层模型规模增大时探针效果有所提高，并能检测开放权重模型在敏感议题与压力情境下的欺骗。

## 证据质量与局限

【论文原文】数据规模、跨任务验证、强文本基线和公开代码/数据使证据较强。  
【局限】AUC 是离线区分指标，不等于低基率部署时的精确率；探针可能学习任务、提示或训练数据伪特征。内部表示信号与行为因果关系尚未完全证明，跨模型、量化部署和 post-training 后的校准也可能漂移。

## 最接近的相关工作

最接近 Monitoring and Discovering Reward Hacking、Near-Zero Monitor Readout、FARM、Speculative Uncertainty、BLINDSPOT 与 Evaluate the Stack, Not the Layer。区别在于本工作专门利用白盒隐藏表示，并验证了不可从文本直接推断的内部目标。

## 如何复用或推进 LLM-as-a-Verifier

将探针输出作为 distributional safety verifier 的一条独立特征流：输出风险概率、模型/层版本与覆盖范围；高风险或探针—文本 Judge 冲突时触发环境隔离、额外 rollout 或人工复核。用执行结果做后验校准，避免把 probe score 当作自证真值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：可蒸馏“内部风险分布→轻量监控头”，但只用于门控 teacher 强度或动作提交，不直接替代任务 reward。
- **A/B/T 与序数分布**：把表示探针、文本 Judge、环境 oracle 的联合结果保留为多通道分布；冲突样本输出 T。
- **程序化/环境真值门控**：探针报警不能推翻执行真值，但可在不可逆动作前触发更严格的硬检查。
- **student-generated critique states**：若 student critique 声称安全而探针高风险，保存为重点反事实状态，并通过环境重放核验。
- **高熵分叉**：对高风险且高不确定分支保留隔离探索，而非直接删除，以便识别新型 sabotage。
- **sealed eval**：冻结探针版本并用未参与训练的模型、任务和攻击测试；同时报告低基率 precision/recall、校准误差和干预成本。

总体判断：【分析推断】该工作适合成为现有三 Judge 之外的机制异质监控层，但最终裁决仍应由隐藏的环境/行为真值完成。