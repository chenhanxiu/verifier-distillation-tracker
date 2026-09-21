# ArenaFlow：从轨迹排序传播到步骤信用与 Skill 记忆

- 论文标题：ArenaFlow: From Trajectory Ranking to Hierarchical Credit Propagation for Open-Ended Agent RL
- 作者：Qiang Zhang；Ruixue Ding；Fanrui Zhang；Xi Chen；Boli Chen；Shihang Wang；Yinfeng Huang；Yi Zheng；Pengjun Xie；Kaipeng Zhang；Jiawei Liu；Zheng-Jun Zha
- 首次公开日期：2026-09-18
- 当前版本日期：2026-09-18（v1）
- arXiv：https://arxiv.org/abs/2609.21378
- DOI：https://doi.org/10.48550/arXiv.2609.21378
- 代码：https://github.com/Alibaba-NLP/qqr

## 一句话结论

ArenaFlow 不把 pairwise/tournament 判断压成一个轨迹分数，而是把比较证据传播到关键步骤和可复用 skill；这是把 A/B/T 轨迹偏好转为长时程 score-level 监督的直接原型。

## 真正新增的内容

- 【论文原文】用 tournament relative ranking 解决开放任务 pointwise reward 区分度不足，并以淘汰深度形成轨迹级相对优势。
- 【论文原文】每次比较额外生成结构化反思，抽取 pivotal success steps、reusable strategy skills 和 retrieved-skill usage attribution。
- 【论文原文】把轨迹优势传播到高置信关键步骤，同时根据跨组使用归因维护、淘汰和检索全局 skill memory。
- 【分析推断】该框架把“偏好比较—步骤贡献—经验准入—后续探索”连成闭环，但关键标签仍来自 LLM Judge，尚缺不可覆盖的环境真值层。

## 核心方法

同题生成 16 条轨迹，通过 tournament 比较获得相对排名和 survival depth。Judge 对比较结果生成结构化反思，定位决定胜负的步骤；step advantage 结合轨迹偏好和深度权重用于 PPO 式更新。skill 层累计被检索 skill 的使用效用，低效 skill 被裁剪，高效 skill 作为未来生成的策略先验。

## 关键实验结果

- 【论文原文】Qwen3-8B 上，Open-Travel 平均从 ArenaRL 的 35.9 提升到 55.4；Open-DeepResearch 从 54.7 提升到 69.1。
- 【论文原文】迁移到 DeepResearch Bench 得分 43.2，高于 ArenaRL 的 37.6、Pref-GRPO 的 34.1，也略高于 Perplexity Deep Research 的 42.3。
- 【论文原文】移除 step credit，Open-Travel 从 55.4 降到 48.6；移除整个 skill memory 降到 41.2。
- 【论文原文】使用 Qwen3-Max、GPT-5、Claude-4.5-Sonnet 作为 reward model 时，Open-Travel 均保持提升；训练 judge 越强，结果越高。
- 【论文原文】检索 skill 数从 1 增到 3 时由 49.8 升至 55.4，增到 6 则降至 43.6，显示记忆过载会干扰策略。

## 证据质量与局限

- 【论文原文】覆盖旅行规划、开放深度研究和跨 benchmark 迁移，包含主要 RL baseline、组件消融和跨 Judge 替换。
- 【论文原文】核心训练只用 Qwen3-8B，120 个训练 step；结构化反思主要由强 LLM Judge 产生。
- 【分析推断】跨 Judge 都有效只能说明机制不完全依赖单一模型家族，不能排除多个 Judge 共享偏差；论文未展示人工/程序真值对关键步骤标签的精确率。
- 【分析推断】skill memory 同时影响后续探索和训练分布，存在 evaluator–policy–memory 共适应；需要冻结的外部任务与隐藏验收才能确认收益不是评分偏好迁移。

## 最接近的相关工作

最接近 ArenaRL、Pref-GRPO、Writing-Zero、Turn-PPO、process reward credit assignment 和 Graph of Skills。相较 BATON，ArenaFlow把轨迹间排序进一步传播到 skill memory；相较 DDO，它依赖 tournament 排名而非只保留多个成功策略。

## 如何复用或推进 LLM-as-a-Verifier

现有三 Judge 可先输出 pairwise A/B/T 与置信度，再聚合成 tournament；只有跨 Judge 稳定且有证据指针的“关键步骤”才获得强 step score。skill 准入应保存来源轨迹、使用次数、下游增益和失效场景；检索后的贡献要通过 usage attribution 回写，而不是按生成质量主观评分。

## 对现有 Agent verifier × OPD 路线的具体影响

- score-level OPD：用 tournament depth × pivotal-step confidence 形成步骤权重，避免全轨迹统一 advantage。
- pairwise A/B/T：原生采用相对比较；应显式增加 Tie/不确定边，防止弱差异被淘汰赛放大。
- 真值门控：可执行任务先由环境结果决定胜负方向，Judge 只负责解释关键步骤和信用幅度。
- student-generated critique states：将 pivotal-step critique 与 skill candidate 一并保存，必须经跨轨迹使用归因后才能晋升为长期记忆。
- 高熵探索：高效 skill 只作为 prior，不应强制动作；对高熵或多路径状态保留未胜出的可恢复分支。
- sealed eval：冻结 skill memory、Judge 版本与检索器，在从未参与 tournament 的任务上独立评估，报告成功率、误报步骤率和策略多样性。
