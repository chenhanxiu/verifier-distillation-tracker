# Legibility is Not Interpretability: Comparing Judged and Actual Importance in Chain-Of-Thought Reasoning

## 基本信息

- **作者**：Kevin Du, Alexander Hoyle, Laura Ruis, Acyr Locatelli
- **首次公开日期**：2026-09-03
- **版本日期**：2026-09-03（v1）
- **原始论文**：https://arxiv.org/abs/2609.04194
- **代码**：公开页未提供
- **arXiv**：2609.04194
- **DOI**：https://doi.org/10.48550/arXiv.2609.04194
- **状态**：COLM 2026 论文

## 一句话结论

LLM Judge 能从 CoT 文本识别部分高贡献步骤，但显著低于基于 Monte Carlo rollout advantage 的噪声上限；“看起来关键”不能替代“对最终奖励有因果贡献”。

## 真正新增的内容

**论文原文结论**：把步骤重要性操作化为包含该步骤对期望奖励造成的变化，用 Monte Carlo rollouts 估计 advantage，再直接比较 Judge 判断、微调 critic 与该基准。

**分析推断**：长时程 Agent 的 critique/步骤评分应由反事实环境 rollout 锚定。纯文本 teacher critique 可作为候选解释，但不应直接成为 step-level 真值或 OPD 权重。

## 核心方法

- 对 reasoning step 做干预并多次 rollout，估计其对最终正确奖励的 advantage。
- 用估计结果构造高重要性步骤标签和 noise ceiling。
- 评估通用 LLM Judge 是否能从轨迹文本找出高 advantage 步骤。
- 微调 step-level critic，并分别分析正确与错误回答。

## 关键实验结果

- 足够强的 Judge 超过 prevalence baseline，但明显低于 noise ceiling。
- 微调 step critic 在错误回答上提升显著，在正确回答上仍远离上限。
- 论文由此认为步骤功能角色只能从可读文本中部分恢复。
- 摘要未公开统一的具体百分比；本记录不从图表之外补造数值。

## 证据质量与局限

- **质量：中高。** 使用反事实 rollout advantage 而非人工“看起来重要”标签，并有已发表会议状态。
- Monte Carlo advantage 本身有方差，且依赖 rollout policy、干预方式与最终奖励定义。
- 研究对象主要是推理 CoT，不是带外部状态和工具副作用的 Agent；在 Agent 中因果识别可能更难。
- 不能据此断言所有自然语言 critique 无效，只能说明其不足以作为无条件因果标签。

## 最接近的相关工作

与 Coding Agent 过程评估三层测量、Wrong but Useful、EDGE、PGPO 和 Key-Step Supervision 最接近；这些工作共同把语义相关性、局部错误与因果贡献区分开来。

## 如何复用或推进 LLM-as-a-Verifier

- 将 generative verifier 的“关键步骤”声明视为 proposal，再用环境 replay 估计 removal/replacement advantage。
- 蒸馏目标同时包含 Judge 的序数置信分布与 rollout 得到的因果区间。
- 对正确轨迹专门构造微小但关键的步骤干预，解决 critic 在正确样本上的弱监督。
- 允许 verifier 返回“文本不可判定”，把计算预算路由给工具或反事实 rollout。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：只有经反事实验证的 step score 才决定梯度方向；文本 Judge 只调幅度或提供先验。
- **A/B/T 与序数分布**：同前缀替换一步并重放，基于奖励差的置信区间标 A/B/T；区间重叠标 Tie。
- **真值门控**：环境终态和副作用为 advantage 提供硬锚点。
- **critique states**：要求 critique 预测“替换此步后哪些可观测结果改变”，以可证伪性筛选。
- **高熵探索**：高 Judge 不确定且潜在 advantage 大的步骤保留多个分支，不做强制模仿。
- **sealed eval**：使用独立 rollout seeds、环境实例和 evaluator，避免 critic 与生成干预共同适应。