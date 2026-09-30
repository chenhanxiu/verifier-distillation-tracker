# Graph-Conditioned On-Policy Agent Distillation from Off-the-Shelf Teachers

- **作者**：Xiaohan Yi, Wen Luo, Yani Huang, Junfeng Zhan, Asher Qin, Peilin Zhao, Xi Xiao
- **首次公开日期**：2026-09-29
- **版本日期**：2026-09-29（v1）
- **原始论文**：https://arxiv.org/abs/2609.37522
- **代码**：未发现公开代码链接

## 一句话结论

GC-OPD 用成功/失败执行历史图为现成 teacher 补充状态证据，使 ScienceWorld 4B student 的平均成功率由 vanilla OPD 的 24.70% 提升到 48.78%。

## 真正新增的内容

【论文原文】多轮 student 的累积错误会把状态带出 teacher 熟悉范围；GC-OPD 将重复 teacher 执行按共享状态建图，保留完整成功与失败历史，再为每条 student 轨迹检索当前状态参考或历史替代路径，结合 hindsight 评分原始 thought-action token。

【分析推断】这是“执行证据条件化 verifier teacher”的直接实现：teacher 不再只看文本轨迹，而由可重放的状态邻域约束其判断。

## 核心方法

离线收集 teacher 多次执行并构造共享状态图；student 完成 episode 后检索同状态或相邻历史，拼接 hindsight，由原 teacher 对 student token 产生 OPD 分数，无需针对任务再训练 teacher。

## 关键实验结果

【论文原文】相对 vanilla OPD，ScienceWorld 4B 从 24.70% 到 48.78%，ALFWorld Unseen 从 53.36% 到 85.26%，WebShop 从 29.10% 到 37.65%；在 ScienceWorld 与 ALFWorld 还超过使用 GRPO 训练 teacher 的 OPD 基线。

## 证据质量与局限

【论文原文】结果横跨三个多轮环境且提升大，但摘要未说明状态图规模、数据成本、图检索错误和环境版本漂移。【分析推断】图中历史若由同一 teacher 生成，会继承覆盖盲区；成功轨迹也不等于最优或安全。

## 最接近的相关工作

DENSE、Terminal-Universe、STRIDE、ArenaFlow、DRACO，以及 student-state 上直接查询 teacher 的标准 OPD。

## 如何复用或推进 LLM-as-a-Verifier

把执行图作为 verifier 的证据层，要求每个 step score 同时返回命中的状态节点、成功/失败先例与不确定性；无证据时输出 T/INCONCLUSIVE。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：以图证据覆盖度和成功/失败邻域差异校准 token/step 分数。
- **A/B/T 与序数分布**：同状态的多条替代历史天然构成 A/B/T；相互矛盾时保留完整序数分布。
- **硬真值门控**：只让环境可重放且状态一致的节点改变更新方向。
- **critique states**：student critique 必须引用图中证据节点，执行复现后才写入记忆。
- **高熵探索**：共享状态下保留多个成功分支，不把图压成单一最佳路径。
- **sealed eval**：训练图与 sealed 任务/状态种子隔离，避免检索式泄漏。
