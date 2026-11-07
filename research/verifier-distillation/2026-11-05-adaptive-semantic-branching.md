# Adaptive Semantic Branching: Disagreement-Localized Cross-Trajectory Regeneration for Reasoning Candidate Expansion

- **作者**：Jeong-Yoon Kim, Tae-Yoon Lee
- **首次公开日期**：2026-11-05
- **版本日期**：2026-11-05（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.07918
- **DOI**：https://doi.org/10.48550/arXiv.2611.07918
- **代码**：论文页面未给出公开代码链接

## 一句话结论

ASB 对不同答案轨迹做步骤对齐，在持续分歧点把竞争轨迹的局部窗口移植到原前缀，仅用少量额外生成把 MATH oracle coverage 从 89% 提至 91%。

## 真正新增的内容

它不是随机增加 self-consistency 样本，而是把答案簇间的语义分歧定位成 branch point，并按现有答案多样性分配最多三个额外 generation。

## 核心方法

按最终答案聚类并选代表轨迹；用单调动态规划对齐步骤；persistent-divergence objective 定位分歧；保留 source 前缀并注入 donor 的短 reasoning window，再生成新后缀。

## 关键实验结果

Qwen2.5-7B-Instruct、500 个 MATH 问题：七个初始样本覆盖 445/500（89%），ASB 提升至 455/500（91%），找回原 55 个未覆盖问题中的 10 个；额外生成 576 次，平均每题 8.152 次总调用。

## 证据质量与局限

分支算子、对齐目标与预算披露清楚；但仅单模型、单 benchmark，评价是 oracle coverage 而非可部署选择准确率，且局部 donor window 可能制造不可执行状态。

## 最接近的相关工作

最接近 Belief-Shift Branching、EPIG-Tree、StepBack、TSBPO 与 turn-level best-of-N。

## 如何复用或推进 LLM-as-a-Verifier

让 distributional verifier 输出分歧点后各后缀的序数分布；在 Agent 环境中只从可回滚 snapshot 移植动作/critique，并用环境 oracle 检查状态一致性。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

1. 用跨轨迹持续分歧定位 score-level OPD 的高价值状态。
2. answer cluster 可转为 A/B/T，未被 oracle 区分的簇保留 T。
3. donor critique 需通过环境重放后准入。
4. 分支预算按答案簇与 verifier 熵分配，直接保留探索。
5. sealed eval 报告 candidate coverage 与 selector accuracy，避免把 oracle 上限误写为实际收益。