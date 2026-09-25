# Back to the Definition: Estimating Step-Level Advantages via Trajectory Graphs for Agentic Reinforcement Learning

## 基本信息

- **方法简称**：GRAFT
- **作者**：Xincheng Yao、Haobo Fu、Weiming Liu、Chongyang Zhang
- **首次公开日期**：2026-09-24
- **版本日期**：2026-09-24（v1）
- **原始论文**：https://arxiv.org/abs/2609.28963
- **DOI**：https://doi.org/10.48550/arXiv.2609.28963
- **代码**：https://github.com/xcyao00/GRAFT （论文声称公开；本次检查时链接尚不可访问）

## 一句话结论

GRAFT 把共享前缀的多条 Agent rollout 合并成轨迹图，以节点价值差给步骤分配信用，可避免把失败轨迹中的有效步骤统一判负。

## 真正新增的内容

【论文原文】指出 group-normalized response advantage 在步骤级系统性有偏；把所有 rollout graft 成图，用 Bellman iteration 恢复节点状态价值，再以相邻节点价值差定义 edge advantage，并用 Graph GAE 降低价值估计偏差。

【分析推断】这为 score-level verifier distillation 提供了比“整轨迹分数复制到每步”更接近反事实贡献的 target，但可靠性仍取决于图覆盖和终局奖励质量。

## 核心方法

【论文原文】共享或可合并的中间状态成为图节点，动作/步骤成为边；终局回报向图内反向传播，边的优势由后继与当前节点价值之差得到。Graph GAE 在图上扩展 GAE 以平衡偏差和方差。

## 关键实验结果

【论文原文】作者报告在一系列多轮 Agent 基准上一致优于 GRPO，并超过近期 agentic RL 方法。摘要未给出逐基准数值、置信区间或失败类型分解。

## 证据质量与局限

方法有清晰的 RL 定义与图上估计结构，但公开摘要中的实证细节有限；状态合并准则可能把表面相似而隐藏状态不同的节点错误聚合，稀疏图也无法真正替代每状态反事实采样。代码链接暂不可访问，复现性待确认。

## 最接近的相关工作

与 BATON 的轨迹内/间双轴信用、PGPO 的状态势能、RLDS 的子任务分解、RECAP 的步骤增量贡献和 EDGE 的反事实依赖图最接近。GRAFT 的差异是直接从多 rollout 共享状态图估计 Bellman advantage。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】将 verifier 的序数节点价值分布蒸馏为 `P(V=k|s)`，再从相邻节点分布推导 A/B/T：置信区间显著上升为 A，显著下降为 B，重叠或覆盖不足为 T。程序化终局回报作为不可覆盖锚点。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- score-level OPD target 改为图边 advantage，而不是广播轨迹分数。
- student-generated critique 只在对应边有环境证据、且跨分支价值一致时准入。
- 优先扩展价值区间宽或图覆盖稀疏的高熵节点，保留探索。
- sealed eval 使用未参与构图的新任务，并审计状态合并错误与 evaluator 共适应。