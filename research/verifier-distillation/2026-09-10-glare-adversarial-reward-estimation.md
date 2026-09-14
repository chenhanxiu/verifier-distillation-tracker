# GLARE：面向长会议续写的对抗式 On-Policy Reward Estimation

## 基本信息

- **论文标题**：GLARE: Generative Learning via Adversarial Reward Estimation For Social Dynamics Forecasting
- **作者**：Tenghao Huang, Zhaoxuan Tan, Muhao Chen, Jonathan May, Mengting Wan, Longqi Yang, Pei Zhou, Sihao Chen
- **首次公开日期**：2026-09-10
- **版本日期**：2026-09-10（v1）
- **原始论文**：https://arxiv.org/abs/2609.12165
- **DOI**：https://doi.org/10.48550/arXiv.2609.12165
- **代码**：未在 arXiv 摘要页发现可核验链接

## 一句话结论

【论文原文】让 discriminator 持续区分真实会议未来与当前 actor 样本，并把其分数作为 KL 正则奖励，能在长多方对话续写上优于 SFT 与 SPIN。

## 真正新增的内容

【论文原文】提出 MDFB：2,207 场真实会议、24,794 个面向未来的问题；任务要求从 transcript prefix 一次生成多轮延续。GLARE 将对抗模仿学习迁移到条件语言生成，并用 current-policy negatives 重训 reward estimator，使奖励面随 actor 分布更新。

## 核心方法

Actor 生成候选多轮未来；discriminator 对“观测到的真实延续 > 当前 actor 样本”做排序；判别分数与 KL 约束共同形成策略奖励；迭代加入 on-policy negatives。评价分为问题推进效用和对话/角色一致性，不要求复现唯一未来。

## 关键实验结果

【论文原文】相对 SFT 与 SPIN，GLARE 的人工评测平均胜率为效用 0.66、人类相似度 0.70，但仍低于真实人类延续。MDFB 也用于通过参考辅助判断比较通用闭源模型。

## 证据质量与局限

【论文原文】数据规模和人工评测增强可信度，并直接覆盖长多方上下文。局限是 reward estimator 与 actor 共演化，摘要未给出独立 sealed evaluator、校准误差或 reward-hacking 压力测试；真实未来也只是多种合理未来之一。

## 最接近的相关工作

Adversarial imitation learning、SPIN、reward model co-training、STAR-OPD、ARISE-RL、Proof-Carrying Cognition，以及长时程 Agent trajectory judging。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把 discriminator 从单标量扩展为序数分布：进展、角色一致性、承诺兑现、分歧处理分别评分；共享前缀的候选续写天然产生 pairwise A/B/T。真实后续或环境事件只作为方向门控，生成式 critique 提供幅度和原因。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】GLARE 是长轨迹 on-policy reward-model 更新的直接基线，但必须增加冻结 shadow verifier 与 sealed human/environment eval。对高熵分叉，保留多个获得相近分布分数的策略，而非让动态 discriminator 过早坍缩；周期性测试旧分支和变换样例以监控 evaluator 共适应。