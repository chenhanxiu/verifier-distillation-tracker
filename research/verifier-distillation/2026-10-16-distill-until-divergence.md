# Distill Until Divergence: Error-Truncated Hindsight Distillation for Agentic RL

## 基本信息

- 作者：Yibin Huang, Conghui Zhu
- 首次公开日期：2026-10-16
- 版本日期：2026-10-16（v1）
- arXiv：2610.23048
- 原始论文：https://arxiv.org/abs/2610.23048
- DOI：https://doi.org/10.48550/arXiv.2610.23048
- 代码：未发现公开代码链接

## 一句话结论

把 hindsight-conditioned OPD 限制在“仍与当前状态匹配”的首错之前，并让首错之后回到环境结果驱动的 GRPO，可避免将事后技能错误地蒸馏到已经分叉的长轨迹状态。

## 真正新增的内容

**论文原文结论：** 长时程 Agent 中，完成轨迹蒸馏得到的技能位移不必然等于 reward-aligned credit；一旦错误动作改变后续状态，继续沿后缀施加 hindsight 蒸馏会产生状态错配。论文提出误差截断的 hindsight distillation：成功轨迹使用正向技能，失败轨迹使用针对首错的负向修正，错误后的后缀只接受 GRPO。

**分析推断：** 这比“整条轨迹都加 teacher KL”更接近 Agent verifier × OPD 所需的因果边界：verifier 不仅决定分数，还决定蒸馏信号可传播到哪里。

## 核心方法

1. 从完成轨迹中提取正向工作流技能或失败特定的负向修正技能。
2. 根据终局结果和错误边界路由技能。
3. 在成功轨迹及失败轨迹首错之前施加 hindsight-conditioned dense supervision。
4. 首错之后停止技能蒸馏，仅保留基于终局结果的 GRPO，避免用反事实上已失配的 teacher 信号监督真实后缀。

## 关键实验结果

**论文原文：** 摘要报告在长时程 Agentic RL 设置中取得有竞争力的任务表现，并通过实验支持更有效的细粒度信用分配；公开摘要未给出可独立核对的具体数值、任务规模或置信区间。

**分析推断：** 当前最有价值的证据是方法消融应能检验“首错后截断”是否优于全轨迹 OPD；在取得全文表格或代码前，不应把“competitive”解释为跨环境稳定领先。

## 证据质量与局限

- 优点：问题定义直接针对长轨迹状态错配，方法边界清晰且可证伪。
- 局限：公开摘要缺少具体数据集、数值和统计不确定性；错误边界本身如何标注或估计是关键依赖。
- 失败风险：若首错识别器与训练 verifier 同源，截断位置会与 student 共适应；失败轨迹也可能在首错后包含可复用的恢复动作，被一刀切丢弃。

## 最接近的相关工作

- hindsight-conditioned OPD 与 completed-trajectory skill distillation；
- STRIDE 的首错定位和 OOD 后缀早停；
- BATON/RLDS 的层级轨迹信用分配；
- γOPD 的终局奖励与 token/sequence 蒸馏混合；
- student-generated critique state 的环境验真与准入。

## 如何复用或推进 LLM-as-a-Verifier

让生成式 verifier 输出结构化的 `first_error_step`、`error_type`、`recoverable` 与证据指针；环境重放或程序 oracle 只负责确认边界和方向，语言 verifier 负责生成负向修正技能。这样可把 critique 从“整段评论”变成带传播范围的监督对象。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD：** 将权重改成“分数 × 边界掩码”，而不是把终局分数广播到全部 token。
- **A/B/T 与序数分布：** 对首错位置不确定时输出 T，并保留边界位置后验，而非强行二分。
- **真值门控：** 用执行日志、单元测试或环境重放确认首错；软 Judge 只调幅度。
- **critique states：** 仅接纳带证据且作用域落在首错附近的 critique。
- **高熵探索：** 首错后不施加模式收缩型 KL，保留恢复探索；可另设 recoverability 分支。
- **sealed eval：** 冻结首错检测器，在未参与技能抽取的环境与轨迹上评估边界准确率、最终成功率和恢复覆盖率。
