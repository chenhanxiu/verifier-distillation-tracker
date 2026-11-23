# Reward Integrity in Adversarial Reinforcement Learning for LLM Guardrail Red-Teaming

- **作者**：Chengming Liu、Leon Viti、Hongxu Chen、Erdem Kemik、Mary-Anne Williams、Ruth Oliver
- **首次公开日期**：2026-11-20
- **当前版本日期**：2026-11-20（v1）
- **原始论文**：https://arxiv.org/abs/2611.26998
- **代码**：截至本记录未发现作者公开代码链接
- **标识符**：arXiv:2611.26998；DOI: 10.48550/arXiv.2611.26998

## 一句话结论

在对抗式 RL 红队闭环中，Judge 可把缺少指定 PII 或未攻击目标策略的样本误判为成功；必须把输入完整性、目标命中与响应越权拆成独立 verifier，并用作者审查的 off-target 集做 sealed audit。

## 真正新增的内容

**论文原文**：研究将 reward fidelity 拆成两层：TypeSafe Jev 检查攻击输入是否包含规定 PII，决策模型再判断目标响应是否违反指定策略；作者另外构造人工审查的 off-target 集，证明强 Judge 也会奖励假胜利。

**分析推断**：这直接说明单一标量 reward 会把“任务构造错误”和“目标真正被攻破”混在一起。若用于 verifier 蒸馏，应分别学习输入有效性与结果正确性，而非蒸馏一个总分。

## 核心方法

- 在攻击生成阶段用专门 verifier 检查规定 PII 是否出现。
- 用 TypeSafe Jev、Laya（预训练/后训练）和 CLM-8B 对目标响应评分。
- 与 replay corpus 中记录的 Opus 4.8 判断比较。
- 以独立作者审查的 off-target 集审计 Judge 的假阳性胜利。

## 关键实验结果

**论文原文**：Laya 后训练显著提高了与记录 Judge 的一致性；但独立 off-target 集显示 Opus 仍会给并未命中目标政策的响应奖励。论文因此主张使用专门 decision-model judges 分别检查输入和目标结果。摘要未给出完整数值表。

## 证据质量与局限

优点是主动寻找 reward 假阳性，并引入独立人工审查集；场景为金融服务 guardrail 红队，且以另一 Judge 的记录作为主要参照，一致性不等于真值。缺少公开代码与摘要级详细统计，不能据此证明所提 decision model 在所有安全领域可靠。

## 最接近的相关工作

最接近 ImpossibleRubrics、Monitoring and Discovering Reward Hacking、AutoTuneBench 的 sealed measurement、Proof-Carrying Cognition 的现实结算，以及将 evidence 与 answer 分账的事实核验研究。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：将 verifier 输出拆成至少三轴分布：输入有效性、目标命中、响应政策违规；只有前两轴通过，第三轴才产生可训练 reward。生成式 critique 必须引用触发政策和证据片段，并由独立规则或审计集复核。

## 对 Agent verifier × OPD 路线的具体影响

**分析推断**：

- **score-level OPD**：蒸馏多轴 score，而非将所有条件压成一个 reward。
- **A/B/T 与序数分布**：攻击输入无效应标为 T/INVALID，不应当作失败 B；有效但未命中与真正成功必须分离。
- **真值门控**：输入 schema/PII 检查先于 learned teacher。
- **critique states**：只接纳能指出具体目标政策和证据的 critique。
- **高熵探索**：对输入有效但目标命中不确定的分支保留探索；无效输入直接剪枝。
- **sealed eval**：使用不参与训练的 off-target 集和人工审计，专门估计 reward 假阳性。