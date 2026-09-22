# AC-OPD：用自适应 Teacher Continuation 修复不可靠的 On-Policy 蒸馏状态

- 论文标题：Teacher Should Think Ahead: Adaptive Continuations for Reliable On-Policy Distillation
- 作者：Jingang Zhou；Yuyi Zhou；Haiyang Guo；Xukai Wang；Shuai Feng；Sirui Gao；Jian Xu；Qingpei Guo；Xu-Yao Zhang
- 首次公开日期：2026-09-06
- 当前版本日期：2026-09-06（v1）
- arXiv：https://arxiv.org/abs/2609.22254
- DOI：https://doi.org/10.48550/arXiv.2609.22254
- 代码：论文称将在发表后公开；截至 v1 未提供有效仓库 URL

## 一句话结论

AC-OPD 不只让 teacher 在 student 当前前缀上给逐 token 分布，而是在高分歧状态向前生成有限长度 continuation，并按“方差下降—路径偏差上升”的权衡自适应截断，为高熵分叉处的 score-level OPD 提供了直接机制。

## 真正新增的内容

- 【论文原文】识别 Teacher Uncertainty Contraction（TUC）：teacher 从不完整或低质量 student 前缀继续生成时，预测不确定性会随 continuation 加深而下降。
- 【论文原文】给出 teacher-branch 梯度的方差—偏差分解：更长 continuation 降低监督方差，但 teacher 路径逐渐偏离 student on-policy 分布而增加偏差，因此最优监督深度应有限且依上下文变化。
- 【论文原文】提出 AC-OPD：用 teacher–student sampled-token log-ratio 的平方选择 anchor，并为每个 anchor 自适应决定有效 continuation horizon。

## 核心方法

1. student 生成完整 on-policy rollout，保留标准 reverse-log-ratio OPD 目标。
2. 以每个位置的 teacher–student log-ratio 平方衡量分歧，选择信息量最高的 K 个状态。
3. teacher 从这些 student 状态生成分支；只有当边际不确定性收缩收益仍能覆盖累积路径失配时才继续蒸馏。
4. 将原轨迹 token loss 与分支 continuation loss联合训练；分支采样和 anchor 选择不反向求导。

## 关键实验结果

- 【论文原文】Qwen3-4B→1.7B 时，数学平均分从标准 OPD 的 33.65 提升到 38.03，代码平均分从 57.70 提升到 61.20。
- 【论文原文】Qwen3-32B→4B 时，数学平均分从 47.78 提升到 50.38，代码平均分从 75.60 提升到 76.65。
- 【论文原文】固定 continuation 深度呈非单调关系，代码任务在 h=8 达峰；自适应方案平均深度 5.74，仍比最优固定 h=8 高 0.35 分，并比打乱上下文配对的同预算控制高 1.10 分。
- 【论文原文】结果均报告五次独立训练均值与标准差，并做了监督 token 数匹配对照。

## 证据质量与局限

- 证据较强：包含理论分解、两种 teacher/student 尺度、五随机种子、固定深度与 matched-budget 控制。
- 局限：只覆盖 Qwen3 系列的数学和代码生成，没有 Agent 长轨迹、环境奖励或 verifier 蒸馏实验；anchor 指标依赖 teacher–student token 概率，未验证黑盒 teacher；公开代码尚不可用。
- 【分析推断】TUC 下降不等于 teacher 判断更正确，因此不能把较低熵直接当作可靠性；必须以程序或环境真值校验分支方向。

## 最接近的相关工作

最接近的是标准 token-level OPD、ExOPD/EOPD，以及“Are Full Rollouts Necessary for On-Policy Distillation?”；与仓库中的 Unified Per-Token OPD Gating、SuRe、Belief-Shift Branching 和 TV-Regulated OPD 共同构成“在哪些状态、沿多长 horizon、以何种方向蒸馏”的设计空间。

## 如何复用或推进 LLM-as-a-Verifier

- 把 Agent 轨迹中的高分歧/高熵状态作为 anchor，让强 verifier 不只给当前动作分数，还生成有限的“预期后果—风险—修复”continuation。
- 将 continuation 转换成逐步序数分布或 A/B/T 分支比较；环境重放决定方向，teacher 分布与 TUC 只决定监督幅度和长度。
- 对 student-generated critique state 使用同一截断原则：只保留能降低不确定性且尚未与真实轨迹明显偏离的后续 critique。

## 对现有 Agent verifier × OPD 路线的具体影响

- 【分析推断】score-level OPD 可从“每步一个 teacher 分数”升级为“关键状态 + 有界未来窗口”的蒸馏单元，重点比较固定 1/4/8 步与自适应 horizon。
- 【分析推断】高熵分叉不应直接全程跟随 teacher；只在 log-ratio、策略熵或 A/B/T 分歧高的状态启动分支，并由环境真值否决方向错误的 continuation。
- 【分析推断】sealed eval 必须单独测量分支监督是否改善最终任务成功率，而非仅看 teacher 熵下降或 student–teacher 一致性，防止把 teacher 自信收缩误判为能力提升。
