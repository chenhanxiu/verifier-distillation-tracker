# Aligning Crowd Feedback via Distributional Preference Reward Modeling

> 来源：历史研究计划核心条目（2026-07-27 整理）

## 论文信息

- **标题**：Aligning Crowd Feedback via Distributional Preference Reward Modeling
- **作者**：Dexun Li, Cong Zhang, Kuicai Dong, Derrick Goh Xin Deik, Ruiming Tang, Yong Liu
- **首次公开/版本**：2024-02-15（v3：2024-05-30）
- **arXiv**：[2402.09764](https://arxiv.org/abs/2402.09764)
- **HTML 全文**：[arxiv.org/html/2402.09764](https://arxiv.org/html/2402.09764)

## 一句话结论

DPRM 提醒我们：评分分布不一定只是模型不确定性，也可能是真实的人群偏好异质性。

## 真正新增的内容与核心方法

用 categorical distribution 表达多群体偏好，借助 Bayesian updater 适应偏好变化，并以 optimal-transport loss 校准预测分布；策略优化使用分布期望作为 reward。

## 关键实验、证据质量与局限

论文报告在多样化人群偏好下比标量 reward 更准确、公平且贴合上下文。证据来自偏好对齐场景，对 Agent 成败这种含较强环境真值的任务不应直接把所有分歧解释为合理多样性。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

可把人工/多 verifier 的分歧保留为目标分布，而非多数票压平；但程序可验证错误应作为 hard constraint。建议把“主观准则分布”和“客观正确性门控”分层建模。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
