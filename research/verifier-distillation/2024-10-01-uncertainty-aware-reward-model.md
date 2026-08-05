# Uncertainty-aware Reward Model: Teaching Reward Models to Know What is Unknown

> 来源：历史研究计划核心条目（2026-07-27 整理）

## 论文信息

- **标题**：Uncertainty-aware Reward Model: Teaching Reward Models to Know What is Unknown
- **作者**：Xingzhou Lou, Dong Yan, Wei Shen, Yuzi Yan, Jian Xie, Junge Zhang
- **首次公开/版本**：2024-10-01（v2：2025-02-12）
- **arXiv**：[2410.00847](https://arxiv.org/abs/2410.00847)
- **HTML 全文**：[arxiv.org/html/2410.00847](https://arxiv.org/html/2410.00847)

## 一句话结论

URM/URME 把 aleatoric 与 epistemic uncertainty 分开，为 teacher 信号门控和主动学习提供了比单一置信度更清晰的依据。

## 真正新增的内容与核心方法

URM 用概率 value head 建模分解后的偏好属性分布以捕获数据噪声；URME 再通过多个 URM 的分歧估计模型认知不确定性，并据此识别不可靠 reward。

## 关键实验、证据质量与局限

在 RewardBench 及 BoN、迭代 DPO、PPO 中均报告收益，低不确定性 reward 更可靠。局限是 ensemble 成本高，且 uncertainty 的外部校准、跨域稳定性仍需独立检验。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

在 Agent verifier × OPD 中可用 aleatoric uncertainty 保留合理多解，用 epistemic uncertainty 决定是否调用更强 teacher/环境真值。应把 entropy、ensemble disagreement、实际错误率分别做 gating 消融，并纳入单位有效监督成本。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
