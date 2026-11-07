# How Do AI Agents Waste Your Money?

- **作者**：Huimin Zeng, Yuxuan Lu, Jesse Cai, Eric Hanchen Jiang, Di Wu, Po-Nien Kung, Wenbo Hu, Ziyi Wang, Dakuo Wang, Jiaxin Pei, Kai-Wei Chang
- **首次公开日期**：2026-11-04
- **版本日期**：2026-11-04（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.07238
- **DOI**：https://doi.org/10.48550/arXiv.2611.07238
- **代码**：论文页面未给出公开代码链接

## 一句话结论

论文让 LLM Judge 标记可删除轨迹片段，再通过“删除—恢复执行—比较结果”的直接干预验真；在线剪去 41%–46% 推理仍大致保持任务表现。

## 真正新增的内容

它把 Judge 对轨迹冗余的判断从相关性标签升级为可执行反事实测试，并区分 reasoning waste、visible execution waste、模型、任务与 harness 的系统级来源。

## 核心方法

统一记录完整 Agent 轨迹，LLM-as-a-Judge 标注 removable span并映射回原 token；删除片段后从相同状态继续执行，比较任务结果和后续动作。

## 关键实验结果

两个不同 Agent benchmark 上，在线 pruning 删除 **41%–46%** reasoning 而大致保持表现；浪费在任务和 Agent 设置间的差异大于模型间差异，同模型同任务的不同 harness 也会产生不同浪费结构。

## 证据质量与局限

直接干预显著强于静态 Judge 标签；但“结果不变”只在测试分布和有限重放中成立，删除片段可能影响罕见风险、可审计性或后续长程状态。

## 最接近的相关工作

最接近 ReplayRCA、minimal-edit verification、trajectory pruning、process reward 与 causal critique validation。

## 如何复用或推进 LLM-as-a-Verifier

把 critique 的准入测试改为可执行消融：删除或替换 critique 指向的步骤，若环境结果与风险指标按预测变化，才将其用于蒸馏。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. score-level OPD 可跳过经干预证明无贡献的片段。
2. 原片段/删除片段构成同状态 A/B/T；效果置信区间跨零时标 T。
3. critique state 记录干预和重放证据。
4. 高熵探索片段不能仅因短期 outcome 不变而删除。
5. sealed eval 同时测成功、风险、可审计性与未来状态差异，防止优化只压 token。