# Reward-Gated On-Policy Distillation

> 来源：历史研究计划 OPD 条目（2026-07-27 整理）

## 论文信息

- **标题**：Reward-Gated On-Policy Distillation
- **作者**：Mohammad Sadegh Akhondzadeh, Vijay Lingam, Atula Tejaswi, Chanakya Ekbote, Sujay Sanghavi, Aleksandar Bojchevski
- **首次公开/版本**：2026-07-04
- **arXiv**：[2607.04037](https://arxiv.org/abs/2607.04037)
- **HTML 全文**：[arxiv.org/html/2607.04037](https://arxiv.org/html/2607.04037)

## 一句话结论

RG-OPD 是“稀疏 verifier 真值决定何时信任 dense teacher logits”的最直接邻近工作。

## 真正新增的内容与核心方法

针对 teacher 可能偏好错误解或压制 student 的有效替代路径，用 verifier reward 对 teacher logits 做门控，在保留 token 级密集监督的同时过滤误导信号。

## 关键实验、证据质量与局限

在 reasoning/coding 上优于 vanilla reverse-KL 与 TSD-KD：1K 长度下分别高 2.9 和 4.9 分，长生成下比未调 student 高 8.2 分，并提供代码。仍需关注 verifier 假阴性及门控导致的覆盖偏差。

## 与 LLM-as-a-Verifier 及 Agent verifier × OPD 的关系

可直接作为 outcome-gated baseline。目标方案进一步比较二值 gate、reward weight、teacher confidence、序数分布 gate；Agent 任务需加入程序化环境真值与人工准则，并报告 gate precision/recall。

## 建议定位

这篇论文应作为当前研究路线的历史基线或邻近工作保存。以上“论文方法/结果”与“对现有方案的迁移判断”已分开表述；迁移建议属于研究分析，不代表原论文已在长时程 Agent verifier 场景完成验证。
