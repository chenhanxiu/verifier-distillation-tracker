# 生成式奖励模型的 Scaling Laws：静态 Judge 更准不等于在线 Rewarder 更好

- **论文标题**：Scaling Laws for Generative Reward Models
- **作者**：Angel Raychev, Nathan Lile, Rafael Rafailov
- **首次公开日期**：2026-10-22
- **版本日期**：2026-10-22（v1）
- **原始论文**：https://arxiv.org/abs/2610.30765
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.30765
- **代码与研究材料**：https://github.com/RaychevAngel/generative-reward-models （arXiv 声明的链接；本次检查时公开页面暂未解析）

## 一句话结论

在在线 DPO 中，静态 Gold-label 准确率更高的 Thinking judge 经常不如 Answer-Only rewarder，说明 verifier 选型必须以“优化后的策略表现”而非离线判分准确率为主指标。

## 真正新增的内容

**论文原文结论**：作者系统扫描 0.6B–14B 的 Qwen3 reward model、policy 规模、训练时长与 DPO 正则；发现 Thinking/GRPO judge 的静态判分更准，但 Answer-Only/SFT rewarder 在 8 个配对设置中的 7 个获得更高 peak 和 top-five-average policy Elo，中间 checkpoint 也可能优于更晚、更准的 checkpoint。

**分析推断**：这是 evaluator–rewarder gap 的直接量化：能测量偏好的模型不一定适合作为被策略优化的奖励面，且“更强 verifier”可能更易被共适应。

## 核心方法

1. 训练不同规模、不同输出形式和目标的生成式奖励模型。
2. 先测固定分布上的 Gold-label accuracy。
3. 再让同一 rewarder 在线提供偏好，驱动 policy 的 DPO 更新。
4. 用固定 32B learned Gold evaluator 建 Elo arena，比较峰值和训练期表现。
5. 扫描 rewarder/policy 规模、训练时长、正则与 checkpoint。

## 关键实验结果

**论文原文结论**：Answer-Only rewarder 在 7/8 个匹配设置中产生更高的 peak 与 top-five-average policy Elo；更大的 rewarder，包括大于 policy 的 rewarder，通常有益；静态更准确的后期 Thinking checkpoint 不保证带来更好的 policy。

## 证据质量与局限

规模扫描和在线优化结果丰富，证据强于只做静态 RM benchmark。作者明确承认：比较同时改变了 judge 训练目标与响应格式；主要排名依赖一个 learned 32B evaluator，换另一个 learned judge 的有限复现实验整体无定论；领域集中于创意写作，不能外推为普遍 scaling law。

## 最接近的相关工作

最接近 GLARE、Proof-Carrying Cognition、PROSE、ImpossibleRubrics，以及 reward model overoptimization / Goodhart 研究。与 UniRRM 等生成式 RM 的区别是，本工作重点评估 rewarder 驱动在线学习后的结果。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 的验收拆成三层：静态判分准确率、在线优化效用、独立 sealed evaluator 下的抗利用性。部署时保留 checkpoint ensemble 或回退机制，不把单一离线最优 checkpoint 视为最佳 teacher。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：teacher/verifier checkpoint 必须按 downstream student 改善选择，而非按离线 AUC 选择。
- **A/B/T 与序数分布**：保留 rewarder 的分布输出，并单独校准“区分能力”和“被优化后稳定性”。
- **硬真值门控**：在可执行任务中用环境结果锁定方向，生成式 RM 只提供幅度、解释和候选排序。
- **critique states**：比较 Thinking critique 与 Answer-Only 分数是否带来真实修复，而非更高自洽性。
- **高熵探索**：监测 rewarder checkpoint 是否过早压低多样性；中间 checkpoint 可能是更好的探索 teacher。
- **sealed eval**：必须使用不参与 rewarder 训练和 policy 更新的 evaluator，并报告多个 evaluator 下的排序稳定性。
