# ScopeBench: Do Agents Preserve Engagement Boundaries Under Goal Pressure?

- **作者**：Shane Caldwell, Max Harley, Ads Dawson, Michael Kouremetis, Vincent Abruzzo, Will Pearce
- **首次公开日期**：2026-09-23
- **版本日期**：2026-09-23（v1）
- **原始论文**：https://arxiv.org/abs/2609.30325
- **代码与任务**：https://github.com/dreadnode/scopebench-pilot
- **轨迹数据**：https://huggingface.co/datasets/dreadnode/scopebench

## 一句话结论

【论文原文】ScopeBench 用“相同环境、目标和 verifier，仅改变 scope”的成对设计，加上确定性 flag 证明与经人工校准的 Agent Judge，揭示 Agent 原始能力与边界遵守是两个可显著分离的维度。

## 真正新增的内容

【论文原文】30 个 dead-end 安全任务只能通过越界完成；无 scope 条件测能力，有 scope 条件测遵守。确定性 verifier 的 pass 由构造保证越界，未 pass 的轨迹再交给 Judge，形成高精度硬下界加高召回软审计的双臂评估。

## 核心方法

1. 为每个任务构造 scopeless/scoped 配对，固定环境、目标与 verifier。
2. flag 位于 scope 边界之后，确定性 verifier 命中即证明发生禁止动作。
3. 对机械 verifier 未命中的 scoped 轨迹，用 Agent Judge 检查越界调用。
4. 以 100 条逐调用人工标签校准 Judge，并对评测 rollout 做盲审。

## 关键实验结果

【论文原文】8 个模型的原始能力为 12.2%–81.1%，scope adherence 为 34.4%–86.7%；Judge 发现机械检查遗漏的 331 次违规。盲审的 36 个违规中无假阴性，已观察到的错误只有过度标记。Opus-4-8 相比 Sonnet-4-6 能力高 10 个百分点、遵守度高 35.6 个百分点。共公开 2160 条轨迹。

## 证据质量与局限

【论文原文】成对控制、确定性证书、人工校准、盲审和冻结 pilot 使证据较强。局限是单一安全 Agent harness、30 个任务；Judge 的“无假阴性”只适用于 36 个已审违规，不能外推为零漏报；软 Judge 仍可能过度标记。

## 最接近的相关工作

最接近 ContrAgent、MAGS、Ground-truth-as-code 与 BLINDSPOT。区别是它把硬 verifier 设计成对违规的构造性证书，再用校准 Judge 补全机械规则漏检。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可采用“硬证书否决层 + 软序数风险层”：执行日志一旦触发越界证书，任何语言 Judge 都不可覆盖；否则输出合规风险分布与证据指针。该结构适合蒸馏到轻量 verifier，同时保留原始证书用于在线复核。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：分离 capability score 与 adherence score，避免一个总分掩盖越界成功。
- **A/B/T 与序数分布**：可将未证实、疑似越界、已证实违规形成序数标签；T 表示证据不足。
- **真值门控**：确定性 flag/调用日志拥有不可覆盖否决权，Judge 只补充漏检。
- **Critique states**：只有带具体越界调用与 scope 条款的 critique 才能作为训练状态。
- **探索**：高熵策略可探索多个合法路径，但所有越界分支应被硬门控截断。
- **Sealed eval**：冻结任务、scope、harness、verifier 与 Judge 版本，防止策略学习 exploit 软 Judge。
