# RightDiff：让生成式奖励模型判断“真正重要的差异”

- **论文标题**：RightDiff: Learning Generative Reward Models to Judge by the Right Differences
- **作者**：Qiyuan Chen, Hongsen Huang, Jiahe Chen, Renjie Hua, Hongxia Xu, Chuan Ren, Jian Wu
- **首次公开日期**：2026-11-24
- **版本日期**：2026-11-24（v1）
- **原始论文**：https://arxiv.org/abs/2611.32166
- **DOI**：https://doi.org/10.48550/arXiv.2611.32166
- **代码链接**：未见公开代码

## 一句话结论

RightDiff 不让 Judge 套用固定总 rubric，而是先发现候选之间的差异、判断其是否实质相关，再形成 pair-specific rubric，可减少长度等表面线索主导 pairwise 奖励。

## 真正新增的内容

**论文原文结论**：方法用单次自回归生成完成差异发现、materiality 分类与 pair-specific rubric 归纳，并用差异对齐奖励、预算约束的一对一匹配和乘法门控训练。**分析推断**：它很适合把现有 A/B/T 的“T”从模糊平局改为“没有经证据支持的实质差异”，并为序数分布提供可解释的差异维度。

## 核心方法

对响应对生成 evidence-grounded evaluation trajectory：枚举差异，区分实质/非实质差异，再据此建立本对样本的评分准则。训练中加入 response-isolated demonstrations，减少直接从答案表面猜标签；差异对齐奖励和一对一匹配约束迫使评价覆盖关键差异，乘法门控抑制缺失关键证据时的高分。

## 关键实验结果

**论文报告**：在 RewardBench、RM-Bench 上达到领先表现，超过多种开放 reward models 和主流闭源 Judge；用于 DPO 时带来下游增益，并对长度捷径更稳健。摘要未披露全部任务数值和统计方差，Agent 长轨迹上的效果仍属未验证外推。

## 证据质量与局限

多基准与下游 DPO 结果支持方法有效性，且明确测试长度偏差。局限是差异发现仍由同一模型生成，可能漏掉不可见环境状态、时序义务或安全约束；pair-specific rubric 会提高可解释性，但也可能成为新的攻击面。没有独立 oracle 时，“重要差异”仍可能是模型共识而非真值。

## 最接近的相关工作

最接近多 Judge 分布恢复、Who Judges Matters 的家族偏差分析、MAWILE 的扰动审计，以及 RightDiff 同期的 STEP-GRM。与固定 rubric Judge 相比，它把比较监督的基本单位从“总偏好”移到“证据化实质差异”。

## 如何复用或推进 LLM-as-a-Verifier

把每个差异映射到序数贡献分布，并聚合为 A/B/T；环境可判定差异由程序 oracle 盖章，语义差异保留不确定性。对 student-generated critique，可要求每条 critique 指向一项差异、一个证据位置和一个可反驳条件，未满足则不进入蒸馏数据。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：在共享状态的高熵分叉上生成 A/B 候选，先用 RightDiff 风格发现“行动—后果”差异，再由环境真值门控；将 materiality 与 ordinal score 分开蒸馏，避免 student 仅学总分。sealed eval 应注入长度、语气和解释密度等无关变化，以及隐藏的时序/权限故障，验证 Judge 是否真正依据关键差异而非展示风格。
