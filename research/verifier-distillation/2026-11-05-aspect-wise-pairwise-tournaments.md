# Aspect-wise Pairwise Tournaments for Test-Time Selection

## 基本信息

- **作者**：Hannah Guan；Yilun Du
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.08640
- **DOI**：https://doi.org/10.48550/arXiv.2611.08640
- **代码**：截至记录时未见论文页提供独立公开代码仓库

## 一句话结论

将复杂候选拆成多个自然语言维度，并让各维度 verifier 进行成对比较后通过淘汰赛聚合，比同预算的标量 reward model、二元多维审批和通用 pairwise Judge 更可靠，尤其适合开放式任务。

## 真正新增的内容

**论文原文结论**：APT 同时把“按维度评价”和“pairwise tournament”作为必要组成部分；去掉任一部分，在匹配预算下都不能复现完整收益。方法不训练新模型，只需改写评价维度即可迁移。

**分析推断**：它为现有 A/B/T 设计提供了一个比单一总分更直接的 teacher 协议，但论文输出仍以胜负投票为主，并未学习序数概率分布，也未验证蒸馏后的 student verifier。

## 核心方法

1. 为任务定义若干自然语言评价维度。
2. 对候选 A/B，分别调用维度专用 verifier 产生 pairwise 偏好。
3. 多个维度投票决定单场胜者。
4. 用单败淘汰赛把多候选压缩为最终选择；维度可按用户偏好重写。

## 关键实验结果

**论文报告**：在五个领域、三个生成模型上，APT 优于二元多维审批、自一致性和 reward-model verification；开放式任务收益最大。匹配预算的通用 pairwise Judge 也不及 APT。摘要未给出统一的绝对提升幅度。

## 证据质量与局限

- 多领域、多 generator 的比较提升了外部效度。
- 依赖作者自报实验；摘要未披露置信区间、完整成本曲线及维度间误差相关性。
- 单败赛对早期误判敏感；维度投票默认各 verifier 近似可交换，尚未处理相关错误、平票和校准。
- 没有环境真值门控，也没有 sealed eval 下的适应性攻击测试。

## 最接近的相关工作

最接近的是 LLM-as-a-Verifier 的 pairwise 选择、概率化评分 token、Judge panel 聚合，以及 Bradley–Terry / tournament 型偏好建模。与单一标量 RM 相比，APT 保留了“哪个维度导致偏好”的结构；与序数 probabilistic RM 相比，它没有显式建模评分分布。

## 如何复用或推进 LLM-as-a-Verifier

可把每个维度 verifier 的 A/B/T 输出保留为向量，而不是立即多数投票；用双顺序评测抵消位置偏差，并把多次采样的胜/负/平频率拟合为维度条件的 Bradley–Terry 或序数分布。环境或程序 oracle 可作为不可被软投票覆盖的硬维度。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：蒸馏目标应从单一总分扩展为维度条件的 pairwise log-odds，再由策略侧组合。
- **A/B/T 与序数分布**：APT 直接支持 A/B，但需显式加入 T，并报告各维度的概率与分歧。
- **真值门控**：程序化/环境失败应先硬拒绝；只有 oracle 不完备时才进入软维度 tournament。
- **student-generated critique states**：维度 verifier 可生成结构化 critique，但只有带证据指针且通过环境复核的 critique 才进入训练。
- **高熵分叉**：在维度间分歧最大或 A/B 接近时保留多分支，避免单败赛过早剪枝。
- **sealed eval**：冻结维度定义、对局顺序和独立 Judge；训练期 APT 不得兼任最终评估器。