# Beyond Reward Scoring: Online Multi-Agent Preference Learning for Multimodal Response Generation

## 基本信息

- 方法名：PrefMind
- 作者：Ziyun Zou, Jiwoo Hong, Yifan Lu, Shao Tang, Weiyi Wu, Aman Gupta, Jin Tian, Imran Razzak
- 首次公开日期：2026-10-16
- 版本日期：2026-10-16（v1）
- arXiv：2610.23256
- 原始论文：https://arxiv.org/abs/2610.23256
- DOI：https://doi.org/10.48550/arXiv.2610.23256
- 代码：未发现公开代码链接

## 一句话结论

PrefMind 不把人类偏好压成固定 reward scalar，而是让 generator 与 preference critic 在当前策略样本上共同判断、纠错和生成改进答案，为在线 generative reward learning 提供直接原型。

## 真正新增的内容

**论文原文结论：** 传统多模态 RLHF 先训练 reward model，再用单分优化生成器，模型不一定学会偏好的理由。PrefMind 让 response Generator 和 preference Critic 都可训练；两者围绕候选 A/B 讨论偏好，接受人类标签纠错，并在双方正确判断时生成改进答案，由 Critic 将其与原偏好答案比较产生奖励。

**分析推断：** 其核心不是“多 Agent”本身，而是把 preference understanding 内化为可生成、可纠错的能力；这与 generative verifier distillation 和 student-generated critique state 高度一致。

## 核心方法

1. 从当前 Generator 策略采样成对候选。
2. Generator 与 Critic 分别分析哪一项更符合人类偏好，并进行交互式修订。
3. 用人类偏好标签监督判断与纠错。
4. 仅在双方正确识别偏好时生成改进答案。
5. Critic 比较改进答案与原 preferred answer，形成 generation reward；两侧均用在线交互更新。

## 关键实验结果

**论文原文：** 摘要报告在三个模型规模上同时改善独立偏好判断与下游回答生成，但未在公开摘要中给出具体数值、数据集规模或统计区间。

**分析推断：** 在获得完整消融前，尚不能区分收益来自在线数据、双 Agent 讨论、人类标签还是 Critic 生成奖励；也不能据此认定 critic 在策略优化压力下保持可靠。

## 证据质量与局限

- 直接覆盖在线、当前策略数据和生成式偏好解释，概念相关性高。
- 公开摘要缺少数值与 sealed evaluator 细节。
- Generator 与 Critic 共训练会产生 evaluator 共适应；双方一致并不等于正确。
- 依赖人类标签的规模与一致性，尚不清楚如何迁移到程序化真值稀疏的长轨迹。

## 最接近的相关工作

- generative reward models 与 Critique-Conditioned OPD；
- UniRRM 的多协议生成式 reward；
- Caddie 的 outcome-trained critic；
- GLARE 的 on-policy reward estimator；
- Who Judges Matters 与 Agreement Overstates Evidence 的相关错误警告。

## 如何复用或推进 LLM-as-a-Verifier

将 Critic 输出拆为：A/B/T verdict、序数评分分布、证据/理由、可执行验证请求。训练时只在硬真值或独立人类标签确认方向后蒸馏 critique 与分数幅度；对双方高置信但无外部证据的样本进入 abstain 队列。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD：** 可把 Critic 的在线 score 作为幅度，但偏好方向由环境真值或独立标签门控。
- **A/B/T 与序数分布：** 方法天然从 pairwise 起步；应显式加入 T 并保留不确定性。
- **真值门控：** 双方一致不是门控，必须使用外部执行、人工或程序 oracle。
- **critique states：** Generator—Critic 纠错对话可直接形成 student-generated critique states。
- **高熵探索：** 不应只保留 Critic 首选候选；保留高分歧、多个可验证改进答案。
- **sealed eval：** 使用冻结、不同家族的 Judge 与程序指标评估，阻断联合训练产生的共适应。
