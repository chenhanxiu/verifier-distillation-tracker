# Swapping the Judge Changes the Ranking：跨 Provider Judge 复现研究

## 基本信息

- **作者**：Sangdo Han, Moonsoo Kim
- **首次公开日期**：2026-11-03
- **版本日期**：2026-11-03（v1）
- **原始论文**：https://arxiv.org/abs/2611.04090
- **DOI**：https://doi.org/10.48550/arXiv.2611.04090
- **代码与裁决数据**：论文 ancillary files（arXiv 页面提供）

## 一句话结论

在 4,000 场带人类投票的 Arena 对战上，替换 Judge 会显著改变系统排名；跨 provider 复现只能在筛掉失配 Judge 时改善精度，不能被当作独立证据的简单叠加。

## 真正新增的内容

**论文原文结论**：预注册实验直接测量跨 provider Judge 对系统比较结论的复现性，并显示 Judge 错误高度相关、排名稳定性不足。

**分析推断**：现有 A/B/T 蒸馏若把多个 Judge 当独立样本，会严重高估有效样本量；应显式建模 judge-conditioned bias 与 error dependence。

## 核心方法

- 5 个 Judge、3 个 provider，重新评价 4,000 场 Chatbot Arena battles。
- 覆盖 9 个系统、33 个系统对，每场采用两个响应顺序。
- 以人类票为参考，比较 verdict-level agreement、系统排名、跨 provider replication 与收敛性。

## 关键实验结果

- 与人类票的 verdict-level 中位 Cohen's κ 仅 **0.22**。
- Judge 排名与人类排名的 Kendall's τ 范围 **0.17–0.89**，中位 0.67；预注册“排名稳定”假设未获支持。
- 两个跨 provider 低成本 Judge 共同复现的结论比单 Judge 精度高 **0.10**，但收益来自过滤一个失配 Judge。
- 涉及该失配 Judge 时，仅 35% 比较留下结论。
- 部分 Judge 在每对最多 100 个 verdict 下仍有 **26%–70%** 系统对不收敛；错误共现远高于独立性预期。

## 证据质量与局限

优点是预注册、大样本、多 provider、双顺序且有人类参考。局限是每场只有一票人类标签，无法完全区分共享 Judge 偏差和 voter noise；Judge 集合在注册后有披露的缩减。

## 最接近的相关工作

与 Who Judges Matters、Judge panel 有效规模、Agreement Overstates Evidence、position bias 和 Arena 评测最接近。本工作进一步将相关错误连接到系统排名是否可复现。

## 如何复用或推进 LLM-as-a-Verifier

用层级模型估计每个 Judge 的校准、位置偏差和相关错误，不把 provider 数量等同独立信息量。蒸馏目标应是条件化于 Judge identity 的 verdict distribution，并由人类/环境真值校准。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher ensemble 采用有效样本量和相关性校正，不做简单平均。
- **A/B/T/序数分布**：双顺序 A/B；不收敛或跨 Judge 冲突标 T，并保留完整分布。
- **程序真值门控**：环境真值用于筛除系统性失配 Judge。
- **critique states**：跨 Judge 一致 critique 仍需证据指针，不能把一致性当真值。
- **高熵分叉**：相关 Judge 共识不应过早截断候选。
- **sealed eval**：至少保留一个未参与训练/路由的独立 evaluator，并与人类或程序 oracle 对齐。
