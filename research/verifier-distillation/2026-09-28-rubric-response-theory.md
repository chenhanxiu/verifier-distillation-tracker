# Rubric Rewards from Item Response Theory

- **作者**：Milad Yazdani, Yaser Souri, Xiren Zhou, Pranit Chawla, Dena Shahriari, Subhojit Som, Xia Song
- **首次公开日期**：2026-09-28
- **版本日期**：2026-09-28（v1）
- **原始论文**：https://arxiv.org/abs/2609.35646
- **代码**：未在 arXiv 页面提供

## 一句话结论

【论文原文】Rubric Response Theory 用两参数 IRT 将多个 criterion verdict 解释为对潜在质量的概率证据，并在线估计 criterion 难度与区分度，优于简单加权求和。

## 真正新增的内容

【论文原文】不同 rubric 命中模式可能得到相同总分，固定权重也不反映当前 rollout 上的判别力；RRT 新增 Response Parameter Network、在线 EM，以及按 Fisher 信息自适应选择少量 criterion。

## 核心方法

1. 假设 rubric criterion 是同一潜在质量的单调指标。\n2. 两参数 IRT 建模 criterion difficulty 与 discrimination。\n3. RPN 从 prompt 和 criterion 文本预测参数。\n4. 随 policy 分布变化，用当前 rollout verdict 在线 EM 更新；推理时按 Fisher 信息选 criterion。

## 关键实验结果

【论文原文】Qwen3.5-4B 在四个数据集的 macro criterion score 比 GRPO 高 1.7 点；Medical/Science 的 hard 与 very hard criterion 高 2.8–5.6 点。只用一半 criterion 预算、冻结 RPN 时，四集宏观分数距离 full-judging GRPO 仅 0.1 点。

## 证据质量与局限

【论文原文】方法直接解决 rubric 聚合和成本，且报告困难 criterion 与预算消融。局限是共同单一潜在质量和单调性可能不适用于安全、正确性、效率等相互冲突维度；在线 EM 也会与策略共适应。

## 最接近的相关工作

最接近 ordinal probabilistic reward model、Rubrics as Rewards、多 Judge 分布恢复与 MAWILE；其独特价值是显式估计 rubric 项目的难度和区分度。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将你现有五维 rubric 先保持多维潜变量，而非强行单轴；每个子能力 criterion 输出 likelihood，再生成序数质量分布及不确定性。硬门槛维度应独立保留，不能被 IRT 总质量抵消。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：蒸馏 latent-quality likelihood 而非 rubric 点数和。\n- **A/B/T 与序数分布**：由 posterior 差生成 A/B/T 与等级概率。\n- **真值门控**：安全/目标完成等硬项不参与可抵消聚合。\n- **Critique states**：criterion 的证据支持度可独立建模。\n- **探索**：posterior 高熵状态优先补评 criterion。\n- **Sealed eval**：冻结 RPN 或在隔离集重校准，报告策略版本漂移。
