# CrossEnv: Synthesizing Verifiable Cross-Environment Tasks for Long-Horizon Agent Training

- **作者**：Zhengfeng Yu、Tian Lan、Zhijing Wu、Enbo Zhao、Xuannan Liu、Feihu Jiang、Qianghuai Jia、Longyue Wang、Zhao Xu、Weihua Luo、Xian-Ling Mao
- **首次公开日期**：2026-11-17
- **版本日期**：2026-11-17（v1）
- **原始论文**：https://arxiv.org/abs/2611.22777
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.22777；DOI: 10.48550/arXiv.2611.22777

## 一句话结论

【论文原文】通过 entity-tool graph 对齐多个可执行环境的数据，CrossEnv 能合成长时程、跨服务且可验证的训练任务，并以课程学习改善对新环境组合和更长 workflow 的迁移。

## 真正新增的内容

【论文原文】把环境合成从“单服务内部”提升为跨服务组合：用实体—工具图识别依赖、对齐数据以保证跨环境操作一致，再按单环境→多环境→跨业务域→用户交互构造课程。附录报告 100 个环境产生 51,566 个候选任务，并对部分 L5 任务做重放、遗漏操作和等价查询检查。

## 核心方法

1. 用 entity-tool graph 连接服务间共享实体和动作依赖。
2. 对齐各环境数据，使参考 workflow 可执行、结果约束可程序化检查。
3. 任务得分采用所有必要结果与约束的合取，而非原子检查平均值。
4. CrossEnv-Curriculum 逐步增加环境数、业务域和交互复杂度。

## 关键实验结果

【论文原文】跨四个外部基准，跨环境数据加课程以更少训练样本获得有竞争力结果；分析显示向未见环境组合、与训练较不相似的外部任务及更长 workflow 迁移。随机抽取的 100 个 L5 任务中参考 workflow 全部执行并满分，遗漏必要操作会阻止满分，等价查询重排保持满分。

## 证据质量与局限

【论文原文】覆盖多环境组合与外部迁移，并检查 verifier 的基本变异性质；但 100 任务质量审计有限，合成任务候选不等于最终高质量训练样本，结果约束仍可能漏掉现实要求。摘要未给出统一幅度，代码也未见公开，复现性暂受限。

## 最接近的相关工作

接近 AgentWorld、EnvScaler、AutoGym、ToolBench 环境合成、长时程工具 Agent 课程学习与 ground-truth-as-code 评测。差异是显式跨环境实体一致性和全约束合取评分。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】CrossEnv 可作为 Agent verifier × OPD 的 on-policy 数据工厂：每个跨服务 workflow 产生可执行终局真值、阶段义务和可恢复分叉；LLM verifier 学习预测这些检查的分布与因果解释，而不是直接替代环境执行。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：在真实 student rollout 上蒸馏“各约束成功概率 + 合取成功概率”，避免仅用平均原子分数。
- **pairwise A/B/T 与序数分布**：从共享状态生成跨环境分叉；满足不同子集的轨迹应保留不可比/T 标签。
- **程序化/环境真值门控**：以重放、必要操作遗漏和等价改写作为 verifier metamorphic tests。
- **student-generated critique states**：critique 指明未完成义务及对应环境证据，修复后必须跨服务重放。
- **高熵分叉探索**：新环境组合与更长 workflow 是优先保留探索的区域；课程不能过早淘汰多种合法顺序。
- **sealed eval**：冻结未见实体映射、环境组合和隐藏约束；生成器、训练 verifier 与最终执行 checker 分离。
