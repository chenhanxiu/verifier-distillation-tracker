# IQuest-Q1：面向 Agentic CLI 的多 Harness、多版本 MOPD

- **论文标题**：IQuest-Q1: Advancing Foundation Capabilities for Agentic CLI Systems
- **作者**：A. Jian Yang 等（IQuest Research，共 177 位作者）
- **首次公开日期**：2026-10-22
- **版本日期**：2026-10-22（v1）
- **原始论文**：https://arxiv.org/abs/2610.30949
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.30949
- **模型与代码仓库**：https://github.com/IQuestLab/IQuest-Q1

## 一句话结论

IQuest-Q1 将四类冻结 Agent 专家通过按域路由的 token-level MOPD 合并到单一 student，并把 harness 版本、独立 verifier、故障归因和 rollout–training 一致性纳入同一训练系统，是目前最接近“长时程 Agent verifier × OPD”完整工程闭环的公开技术报告之一。

## 真正新增的内容

**论文原文结论**：报告公开了一个 320B 总参数、每 token 激活约 15B 的 MoE Agent 模型及其 CLI 中心化训练流水线。后训练先在不同 harness 与环境上进行 SFT 和 environment-centered RL，再从四类冻结专家实施 MOPD：终端交互/工具使用专家、多 harness 专家、长时程 coding 与 cybersecurity 专家、通用 Agent 专家。student 在自己的轨迹上生成 token，按任务域选择 teacher，使用裁剪后的 teacher–student log-prob ratio 作为 distillation advantage。

**分析推断**：相比只在静态问答中合并能力的 MOPD，本报告真正有价值的是把工具调用 token、不同 scaffold 版本、环境故障屏蔽、独立终局 verifier 和异步 teacher 执行放进同一 on-policy 数据路径；它提供了可直接复用的系统边界，但并未以受控消融证明每个组件或 MOPD 本身分别贡献多少。

## 核心方法

1. **多 Harness、多版本 rollout**：在 Claude Code、Codex、OpenCode 等不同 scaffold/版本上采集轨迹；每个 episode 固定任务域、harness、版本、环境与 evaluator。
2. **环境中心 RL**：独立 verifier 决定终局正确性；长轨迹的 segment reward 只用于可测量进展，另设无效计算、约束违反和 reward hacking 惩罚。
3. **故障归因门控**：policy 错误进入训练；环境或 harness 故障被 mask；evaluator 故障阻止样本消费。模型生成的诊断必须有执行记录证据。
4. **四 Teacher MOPD**：student 从 SFT Stage 2 初始化，在自身轨迹上按 domain 选择冻结专家。对生成 token 计算
   `clip(log q_teacher(y_t|h_t) - log p_student(y_t|h_t), -c, c)`，
   并优化长度归一化的 reverse-KL 风格 surrogate。
5. **损失掩码**：只对模型生成 token（含 tool-call token）计算损失；指令和工具 observation 仅作为上下文；重复 rollout 的样本权重置零。
6. **TITO 一致性与异步执行**：服务边界记录 token prefix、分支、reward 和 mask；teacher 在 student 在线轨迹上异步前向，并显式控制样本陈旧度。
7. **模型合并**：将 expert、MOPD 与不同阶段 checkpoint 的参数增量做指定权重与全局 L2 范数校准后合并。

## 关键实验结果

**论文原文结论**：IQuest-Q1 在公开报告的 Agent/coding 评测中取得：DeepSWE v1.1 64.6、SWE-bench Multilingual 80.3、SWE-Bench Pro 57.5、NL2Repo-Bench 63.0、CyberGym 84.5、Terminal-Bench 4.0 22.7、Toolathlon-Verified 75.0、MCP-Atlas 78.4、AutomationBench 52.7、Agents’ Last Exam 29.6、τ³-Banking 51.8。内部 IQuest-CLIBench 结合脚本化用户模拟、执行轨迹与环境状态不变量，得分 53.7。

**论文原文未证明的部分**：这些最终模型结果不能单独归因于 MOPD，因为训练同时包含大规模预训练、中期训练、SFT、RL、模型合并和多阶段 checkpoint 组合；报告未提供“无 MOPD”或逐 teacher 的严格消融。

## 证据质量与局限

优点是方法公式、训练基础设施、reward hacking 防护、harness 配置和大量公开 benchmark 均有披露，且开放模型仓库。局限包括：

- 最终能力没有受控隔离 MOPD 的边际贡献；
- IQuest-CLIBench 为私有 benchmark，无法独立复核；
- 部分对照分数来自公开报告、部分为作者自测，harness 与预算并非完全统一；
- 按 domain 硬路由 teacher，未报告跨 teacher 分歧、能力反制或校准误差；
- 重复 rollout 直接置零，但没有分析其是否包含罕见而有价值的探索路径；
- evaluator 与策略虽有隔离设计，仍缺少长期在线共适应的 sealed holdout 结果。

## 最接近的相关工作

最接近 MOPD、Kimi K3 的多 teacher 能力合并、DeepSeek-V4 的 domain-specialized RL、ToolOPD 的长轨迹信用、Nash-MOPD/CA-MOPD 的 teacher 权衡，以及 Harness or Model、AuditKIT、AutoTuneBench 对 scaffold 与 evaluator 隔离的研究。与这些方法相比，IQuest-Q1 的主要贡献更偏向大规模系统集成，而非新的 MOPD 优化目标。

## 如何复用或推进 LLM-as-a-Verifier

可把报告的训练实例 schema 直接迁移为 verifier 数据协议：`task × harness × version × environment snapshot × evaluator version × trajectory × terminal truth × fault attribution × token mask`。独立 verifier 先判定样本是否可消费，再由生成式 verifier 输出局部 critique 或分数；只有能指向执行证据的诊断才能进入 segment reward 或 critique-state 训练。TITO 路径可用于精确对齐工具 observation 后的 student token 与 teacher log-prob，减少多轮轨迹在服务端重分词或上下文拼接导致的训练偏差。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level on-policy verifier distillation**：将当前单一 teacher 扩展为“终端交互、长时程、通用任务、特定 harness”四类 teacher；先复现按域硬路由作为基线，再与 verifier-gated soft routing 比较。
- **pairwise A/B/T 与序数评分分布**：论文只使用单 teacher 的裁剪 log-ratio，未显式保存多 teacher 分歧。实验应同时查询相邻专家，在分歧或后验重叠时生成 T，而不是强制选定一个域 teacher。
- **程序化/环境真值门控**：直接采用其三类故障归因：policy fault 才训练，environment/harness fault mask，evaluator fault block；终局执行真值决定更新方向，teacher log-ratio只控制 token 幅度。
- **student-generated critique states**：要求 critique 附执行记录、失败归因和对应 observation；只有重放后仍成立的诊断进入状态，避免语言上合理但环境上错误的自评。
- **高熵分叉与探索保留**：不能照搬“重复 rollout 权重为零”；应区分近重复无信息轨迹与共享前缀后的高价值分叉，并用 verifier 不确定性、结果差和 lineage coverage 决定保留。
- **独立 sealed eval**：冻结一组未用于 teacher 路由、RL 和模型合并选择的任务、harness 版本与 evaluator；分别报告 model、scaffold、environment 和 verifier 的版本指纹，避免最终成绩吸收多轮 evaluator 共适应。
- **首个建议实验**：在现有接口 harness 上选择 2 个模型 × 3 个 scaffold 版本 × 4 类任务，比较单 teacher OPD、按域 MOPD、verifier-gated MOPD；所有方案共享环境真值和 sealed holdout，并报告任务成功率、跨版本最差性能、A/B/T 分布、teacher 分歧率与探索分支覆盖。
