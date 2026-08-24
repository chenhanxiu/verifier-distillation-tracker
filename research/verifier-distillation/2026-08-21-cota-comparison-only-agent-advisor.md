# COTA：同前缀反事实分支训练的轻量 Pairwise Agent Advisor

- **论文标题**：Don't Solve, Just Compare: Tiny Advisors for Runtime Intervention in LLM Agents
- **作者**：Yanze Jiang，Mingxuan Li，Yuhao Wang，Shengfang Zhai，Jiaheng Zhang
- **首次公开日期**：2026-08-21
- **版本日期**：2026-08-21（v1）
- **arXiv ID**：2608.21027
- **原始论文**：https://arxiv.org/abs/2608.21027
- **DOI**：https://doi.org/10.48550/arXiv.2608.21027
- **代码链接**：论文页面未提供公开代码

## 一句话结论

COTA 表明辅助模型无需能独立解决任务，只要能在同一 prefix 下比较候选分支的后续质量，就能对更强 Agent 提供有效、非强制的恢复建议。

## 真正新增的内容

**论文原文结论**：作者将运行时干预从“检测错误或生成完整修复”改写为 comparison-only：小 comparator 对同前缀反事实候选进行 pairwise 判断，多次比较决定是否介入，优选分支作为建议返回给原 actor 重新规划。

**分析推断**：这是现有 A/B/T verifier 路线最直接的新原型之一，因为监督单位正是同状态分叉，而且 advisor 弱于 actor 仍可有效，支持将 verifier 蒸馏为小模型。

## 核心方法

从相同历史 prefix 采样 actor 原动作和替代动作，展开反事实 continuation，构造成对偏好监督训练小 comparator。运行时重复比较候选，仅在证据足够时提供非绑定建议；最终动作仍由原 actor 决定。

## 关键实验结果

**论文原文**：在 WebShop、ALFWorld 与 tau3-Retail，搭配三个 actor 的九个设置全部得到改善，并优于所比较基线。摘要未公开逐任务绝对增益、advisor 参数规模和统计区间，因此不据此声称通用幅度。

## 证据质量与局限

覆盖三个 Agent 环境和多个 actor，方向证据较强；但仍为预印本，摘要缺少完整数值与代码。反事实 continuation 的偏好标签取决于 rollout 预算和终局 verifier，短展开可能误判“暂时变差但可恢复”的动作。

## 最接近的相关工作

最接近 SafeBranch、TRACE、Not Every Divergence Should Be Suppressed、SPOT 与 Robo-Dopamine 2.0。COTA 的区别是把 comparator 明确压缩为“只比较、不求解”，并把建议交回 actor，而不是直接替换动作。

## 如何复用或推进 LLM-as-a-Verifier

将下一步动作评估改为同一状态下的 A/B/T：A 为 actor 原动作，B 为采样替代，T 表示在有限 rollout 下不可区分。训练数据记录分支终局、成本、违规和可恢复性；小 verifier 学习 pairwise 分布，运行时只在置信度和价值差同时过阈值时介入。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：把 pairwise 胜率或序数效用蒸馏为小 advisor，而非蒸馏完整 teacher 解法。
- **pairwise A/B/T 与序数分布**：COTA 可直接扩展三分类 A/B/T，并通过多次 continuation 形成概率分布。
- **真值门控**：分支偏好先由环境终局、工具副作用和预算门控，再用 Judge 处理软质量。
- **student-generated critique states**：替代动作可由 student critique 生成，teacher/comparator 只判断其是否改善 continuation。
- **高熵探索**：建议是非绑定的；低置信或可恢复分支应保留，避免 comparator 过早收缩策略支持。
- **sealed eval**：用未参与分支生成和 comparator 训练的任务、actor 与终局 verifier 做独立验证，防止 actor 与 advisor 共适应。
