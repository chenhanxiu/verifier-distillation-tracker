# AtomSD: Procedural Atom-Guided Self-Distillation for LLM Agents

- **作者**：Bohan Yu、Pengfei Cao、Kai Tian、Chen Han、Shi-Yang Li、Chenxi Zhou、Junlin Liu、Cao Liu、Ke Zeng、Jun Zhao、Kang Liu
- **首次公开日期**：2026-10-17
- **版本日期**：2026-10-17（v1）
- **原始论文**：https://arxiv.org/abs/2610.26926
- **arXiv ID**：2610.26926
- **DOI**：https://doi.org/10.48550/arXiv.2610.26926
- **代码/项目**：未公开

## 一句话结论

把成功轨迹压缩成 Intent/When/Do/Avoid 四字段的独立程序原子，再通过条件监督和任务奖励持续蒸馏进 Agent。

## 真正新增的内容

相较整条轨迹或大颗粒 skill，Procedural Atom 强调可跨不同交互历史独立适用，并明确适用与禁用条件。

## 核心方法

从 student 成功轨迹持续抽取原子，作为 privileged guidance 条件化监督，同时联合任务 reward 优化策略，使经验库和策略共同演化。

## 关键实验结果

论文报告在综合实验中稳定超过 reward-based 与 distillation 基线，相对最强基线平均表现最高提升 9.31 点。

## 证据质量与局限

表示形式清晰且直接面向 Agent 复用；但公开摘要未披露原子抽取错误率、跨任务污染与失败轨迹覆盖，证据强度中等。

## 最接近的相关工作

与 SkillAA、RoboRSI、BELIEFWEAVER、DENSE 与 RSD 最接近。

## 如何复用或推进 LLM-as-a-Verifier

把每个 atom 作为可审计 critique/memory 单元，要求附源轨迹、环境结果、作用域和反例；Avoid 字段可映射为 verifier 的硬/软禁用门。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】适合替代无结构自由文本 critique state，但只有成功轨迹来源仍可能遗漏失败模式；建议加入反事实失败分支和 sealed applicability 测试。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
