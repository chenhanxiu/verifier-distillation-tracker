# Learning Ordinal Probabilistic Reward from Preferences

> 来源：历史研究计划核心条目（2026-07-27 整理）

## 论文信息

- **标题**：Learning Ordinal Probabilistic Reward from Preferences
- **作者**：Longze Chen, Lu Wang, Renke Shan, Ze Gong, Run Luo, Jiaming Li, Jing Luo, Qiyao Wang, Min Yang
- **首次公开/版本**：2026-02-13（v2：2026-03-02；ICLR 2026）
- **arXiv**：[2602.12660](https://arxiv.org/abs/2602.12660)
- **HTML 全文**：[arxiv.org/html/2602.12660](https://arxiv.org/html/2602.12660)

## 一句话结论

OPRM 为 A/B/T 或多档序数评分提供了可解释的完整概率分布，是 score-level verifier distillation 的关键目标形式。

## 真正新增的内容与核心方法

把 reward 建模为随机变量，并用有限个有序档位形成 Ordinal Probabilistic Reward Model；Region Flooding Tuning 用少量绝对质量标注约束概率质量落在对应评分区间。

## 关键实验、证据质量与局限

论文在多项 reward-model benchmark 上相对既有方法提升 2.9%–7.4%，并展示分布能同时表达相对排序和绝对质量。已被 ICLR 2026 接收；但验证重点仍是通用回答偏好，而非长轨迹或在线 student states。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

可把 OPRM 作为 student verifier 输出头：先用 pairwise 偏好学排序，再用少量绝对标注校准档位。实验应比较 hard label、期望分数、完整序数分布，并报告 NLL/Brier/ECE、pairwise accuracy 与跨任务校准。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
