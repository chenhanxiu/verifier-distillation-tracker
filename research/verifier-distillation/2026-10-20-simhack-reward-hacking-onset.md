# SimHack: Predicting the Onset of Detectable Reward Hacking Before RL Training

- **作者**：Junwei Deng、Alex Bie、Natalia Ponomareva
- **首次公开日期**：2026-10-20
- **版本日期**：2026-10-20（v1）
- **原始论文**：https://arxiv.org/abs/2610.28707
- **arXiv ID**：2610.28707
- **DOI**：https://doi.org/10.48550/arXiv.2610.28707
- **代码/项目**：未发现公开链接

## 一句话结论

少量小规模 RL 运行可以拟合 reward hacking 首次占主导的时间分布，从训练前筛掉高风险课程，而不是等 verifier 被攻破后补救。

## 真正新增的内容

把 hacking 风险从静态“初始作弊率”改写成 onset-step 的分布预测，并对未运行的模型规模、课程、rollout 数和学习率组合做反事实模拟。

## 核心方法

SimHack 从少数参考 RL 运行学习作弊动力学，对候选训练 recipe 生成 counterfactual runs；用预测的 onset 分布比较课程风险和可安全训练长度。

## 关键实验结果

未见 recipe 的 median onset 相对误差为 11.3%，跨 recipe 排序相关为 0.85；据此选出的课程在相同场景集合上可多训练 96.6% 的步数才出现 hacking。

## 证据质量与局限

包含跨模型规模和超参数泛化，且直接面向 coding RL；但只预测“可检测”作弊，检测器盲区与主动隐匿不在保证内，模拟准确率也可能随策略机制变化失效。

## 最接近的相关工作

最接近 Dynalize、Envelope Sampling、Monitoring and Discovering Reward Hacking、ImpossibleRubrics 与 Judge Hacking 的速度与深度。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier disagreement、环境真值违例和 latent monitor 告警作为多通道 onset 事件；对每个 verifier/OPD recipe 先估计风险分布，再决定蒸馏强度、刷新周期或提前停止。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】应将 sealed eval 从训练后的单点验收扩展为“hacking onset 生存曲线”，并比较 score-level OPD、A/B/T 与序数分布在何时开始偏离环境真值；高风险配置不应仅靠平均最终分淘汰。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
