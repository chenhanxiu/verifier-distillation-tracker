# OmniVerifier-C1：面向规则世界模型的分解式分级生成 Verifier

- **论文标题**：OmniVerifier-C1: Decomposed Graded Verifier for Rule-Governed Generative World Modeling
- **作者**：Bowei Liu, Xinchen Zhang, Xuhuan Li, Tianlin Zhang, Kaian Jiang, Jingwei Liu, Congyang Zhao, Yifei Qian, Junhong Liu, Zhiheng Li, Yujiu Yang, Yang Cai, Ling Yang
- **首次公开日期**：2026-10-15
- **版本日期**：2026-10-15（v1）
- **原始论文**：https://arxiv.org/abs/2610.22355
- **项目/代码**：https://github.com/Cominclip/OmniVerifier

## 一句话结论

把复杂规则自动拆成子问题并输出连续 pointwise 分数，比二值 verifier 更有信息；有 ground-truth 图像时，pairwise 分级验证又优于 pointwise，直接支持“分解评分 + A/B/T + 序数分布”的组合设计。

## 真正新增的内容

**论文原文**：提出自动分解复杂 prompt/环境规则、对子项判定并形成全局连续分数的生成式视觉 verifier；Decoupled RL 同时优化子问题二值判断和全局 alignment score，并把方法扩展到 Maze、Sudoku 等规则控制的生成式世界建模。

**分析推断**：这可迁移为长轨迹 Agent verifier：将任务契约、环境义务和步骤证据拆开评价，再把局部分布聚合成轨迹级序数分布，而不是只给一个不可诊断的总分。

## 核心方法

规则自动分解 → 子问题局部判断 → 连续全局评分；训练时将精确局部反馈与全局对齐目标解耦联合优化。存在 ground-truth reference 时改用 pairwise graded verification。

## 关键实验结果

**论文原文**：分级 pointwise verifier 在传统文本到图像任务上显著优于二值 verifier；结构化输出改善 OOD multimodal critic 泛化；Maze、Sudoku 等任务验证了 pairwise graded verifier 在有真值图像时产生更准确 critique。摘要未披露具体数值。

## 证据质量与局限

论文为 NeurIPS 2026 工作且有跨任务实验与理论讨论；但当前摘要没有样本量、置信区间或详细绝对增益。视觉规则世界与文本/工具 Agent 的状态分布不同，不能直接把结论外推到长轨迹软件 Agent。

## 最接近的相关工作

与 UniRRM 的多协议生成式 reward、DRACO 的动态 rubric 信用分配、Beyond Solver Verdicts 的形式 oracle→生成 verifier，以及 ordinal probabilistic reward model 最接近。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 先产生机器可检查的 rule decomposition，再对每个义务输出 {A,B,T} 概率、证据指针和连续严重度；全局分数只作为聚合视图。若有可执行 reference，则优先比较两个候选分支，而不是绝对打分。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：teacher 输出子规则分数向量与全局分布，student 同时蒸馏局部与全局。
- **A/B/T 与序数分布**：以 pairwise A/B/T 为主、pointwise ordinal 为辅，并保留规则级协方差。
- **真值门控**：Maze/Sudoku 式可执行规则只决定合法性和方向；生成 verifier 负责解释与幅度。
- **critique states**：只有携带具体规则编号和环境证据的 critique 才写回 student 状态。
- **高熵探索**：对子规则冲突或高熵分布保留多个候选，不用平均总分提前剪枝。
- **sealed eval**：冻结规则解析器、隐藏规则实例和 reference，防止 verifier 与生成器围绕公开分解模板共适应。
