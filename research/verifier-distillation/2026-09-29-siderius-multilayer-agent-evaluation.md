# SIDERIUS：面向长时程 Agent 的多层科学有效性评估

- **论文标题**：Beyond a Better Score: Long-Horizon Agentic ML Development and Evaluation Protocol for Physics Time Series
- **作者**：Yue Ma, Lucas Venetoulias, Akbota Assan, Aobo Li
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2610.14024
- **代码**：论文摘要未给出公开链接
- **标识符**：arXiv:2610.14024；DOI: https://doi.org/10.48550/arXiv.2610.14024

## 一句话结论

SIDERIUS 把单分数优化替换为契约化能力、多层科学有效性检查和资源约束探索，显示“得分高”与“产出可被信任”必须分开评价。

## 真正新增的内容

**论文原文结论**：面向物理时间序列的 LLM Agent 可能通过捷径、模式坍缩或评价投机取得高分但无效。SIDERIUS 用契约定义可组合能力、多层评价协议和资源感知探索过滤不健康/博弈模型；在 TIDMAD 上，GPT 编排器的有效模型提案率为 63.8%，有效去噪分数 2.744，而同一 GPT 配通用 Codex Agent 为 1.6% 与 -0.647。

**分析推断**：这为 sealed eval 提供了领域化模板：最终分数之外，还要验证约束、失败模式、探索过程和模型有效性。

## 核心方法

1. 用契约定义 Agent 可调用的能力和有效输出条件。
2. 多层协议分别检查表面分数、科学有效性、异常/博弈模式。
3. 在昂贵实验中按资源预算进行探索，并保留人工介入。

## 关键实验结果

- TIDMAD 有效模型提案率：63.8% 对 1.6%。
- 有效去噪分数：2.744 对 -0.647。
- 另在三个物理时间序列数据集上验证复用性。

## 证据质量与局限

**论文原文**使用同一底座模型对比不同 harness，较好地区分模型与评估/编排贡献；跨四个科学数据集增强外部有效性。局限是领域集中于物理时间序列，人工介入和领域契约成本可能较高，尚未直接检验 reward model 蒸馏。

## 最接近的相关工作

与 AutoTuneBench 的冻结协议和证据账本、Harness or Model? 的因果拆分、Ground-truth-as-code 以及 MAGS/ContrAgent 的形式化门控相近。

## 如何复用或推进 LLM-as-a-Verifier

- 将 verifier 输出拆成性能、约束满足、异常模式、证据完整性和资源合规等序数维度。
- 环境/程序 checker 决定不可覆盖的硬失败；LLM verifier 只对未决维度给概率分布。
- 把“有效但较弱”和“高分但无效”作为关键 A/B 对，训练抗捷径 reward model。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：sealed eval 应冻结任务契约、隐藏有效性测试和资源预算，并同时报告原始分数、有效提案率与博弈率。score-level OPD 不应直接追逐单一总分，而应蒸馏多维序数分布；硬契约定方向，soft verifier 定幅度。高熵探索只在契约允许的可行域内保留，student critique 必须引用被触发的契约或环境证据。