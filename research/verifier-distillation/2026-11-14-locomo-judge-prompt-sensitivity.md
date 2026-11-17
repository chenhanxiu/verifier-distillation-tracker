# What Moves a LoCoMo Score? Memory Context, Answer Prompts and Judges

- **作者**：Nikhil Kumar Jha、Amitoj Cheema
- **首次公开日期**：2026-11-14
- **版本日期**：2026-11-14（v1）
- **原始论文**：https://arxiv.org/abs/2611.19199
- **代码与完整结果**：https://github.com/becos-ai/locomo-results
- **标识符**：arXiv:2611.19199；DOI: 10.48550/arXiv.2611.19199

## 一句话结论

【论文原文】LoCoMo 分数仅因更换 Judge 就可移动 7.2 分、更换回答 prompt 可移动 9.3 分；记忆系统结论还会随 answer model 改变。

## 真正新增的内容

【论文原文】论文在相同条件下联合控制 memory context、answer model、answer prompt、Judge 和 baseline layout，评估 Becos 与完整对话基线，并对 Judge 分歧样本做盲人审；同时公开全部答案、verdict 和评分脚本。

【分析推断】这直接说明 Agent verifier 评测中“模型进步”可能只是 prompt/Judge 配置漂移。独立 sealed eval 不仅要冻结题目，还必须冻结 answer prompt、Judge 版本和 baseline layout，并报告跨 Judge 方差。

## 核心方法

1. 在 10 段对话、1,540 个问题上全因子变化两种 answer model、两种 prompt 和三种 LLM Judge。
2. 与相同设置下重跑的 whole-conversation baseline 配对比较。
3. 对 150 个答案做盲人检查，区分 Judge 一致与分歧区域。

## 关键实验结果

【论文原文】只换 Judge 最高移动 7.2 分，只换 prompt 最高移动 9.3 分。Becos 使用少 90% 字符的 context；在 gpt-4o-mini 下为 79.7 vs 73.0（短 prompt，差值 95% 区间 +3.8 至 +9.5）及 88.8 vs 77.5（step-by-step）。在 gpt-4.1-mini 下几乎持平：83.2 vs 83.1、92.5 vs 92.1。系统在 LoCoMo 上开发，无 held-out set。

## 证据质量与局限

【论文原文】全设置配对、盲人审、置信区间和完整结果公开提高可复核性；作者明确披露没有 held-out set。

【分析推断】仅 10 段对话和 150 条人工检查限制精度；Judge 一致时较可靠不代表共同偏差消失。开发集污染使 Becos 的绝对优势不能视为无偏泛化结果。

## 最接近的相关工作

最接近 Who Judges Matters、Agreement Overstates Evidence、Reward Score 残差化审计、Harness or Model? 与 Verification Transport。本文新增的是把 prompt、answer model 与 Judge 对长期记忆分数的移动量同时量化。

## 如何复用或推进 LLM-as-a-Verifier

对同一轨迹保留多 Judge 的序数分布并标记分歧；校准时使用人工或环境证据只检查分歧区域。任何 verifier 蒸馏结果都应跨固定 prompt/Judge panel 重算，避免把单一 Judge 偏好蒸馏成能力提升。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：训练与评估分别冻结 prompt 和 Judge，报告跨 Judge score variance。
- **pairwise A/B/T 与序数分布**：Judge 一致才形成强 A/B；分歧区域标 T 并保留面板分布。
- **环境真值门控**：可重放的记忆事实和时间状态优先于 LLM Judge。
- **student-generated critique states**：critique 需对 prompt 改写稳定，避免格式诱发虚假改善。
- **高熵探索**：Judge 分歧视为认知不确定性，不用单一 verdict 裁剪分支。
- **sealed eval**：冻结 answer model、prompt、Judge 快照和 baseline layout，并保留完全独立 held-out 对话。
