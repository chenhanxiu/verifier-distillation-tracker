# SAGE：以策略熵选择性调用并蒸馏不完美 VLM Teacher

## 基本信息

- **论文标题**：Selective Agent Guidance via Entropy: Learning Autonomous Policies from Imperfect VLM Teachers
- **作者**：Matteo Merler, Giovanni Bonetta, Davide Zago, Rossella Cancelliere, Bernardo Magnini
- **首次公开日期**：2026-09-01
- **当前版本日期**：2026-09-01（v1）
- **发表信息**：EMNLP 2026 Findings
- **arXiv**：[2609.01567](https://arxiv.org/abs/2609.01567)
- **DOI**：[10.48550/arXiv.2609.01567](https://doi.org/10.48550/arXiv.2609.01567)（DataCite 注册待完成）
- **代码**：截至 v1 未在 arXiv 页面提供公开代码链接

## 一句话结论

SAGE 只在 student 策略熵高时询问 VLM teacher，并用环境 advantage 判断建议是否值得蒸馏，为“高熵分叉保留探索、硬回报校验软教师”提供了直接的在线 Agent 基线。

## 真正新增的内容

**论文原文结论**：VLM 不必在每一步充当固定策略；它可作为临时且不完美的教师，仅在 learner 不确定时介入，建议的实际价值再由环境交互验证并内化。部署时轻量策略不再调用 VLM，并在部分环境中超过教师。

新增点在于把“何时求助”和“是否相信”拆开：熵决定查询位置，环境 advantage 决定 teacher-action 蒸馏权重。这比无条件行为克隆更能容忍 teacher 的系统性错误，也比始终查询显著降低教师成本。

## 核心方法

student 在环境中在线采样；当动作分布熵超过选择条件时调用 VLM，训练阶段执行其建议动作。RL 从实际结果更新策略，蒸馏项则由环境导出的 advantage 加权，避免把所有建议视为同等可靠。测试时仅运行 student。

## 关键实验结果

**论文报告**：在稀疏奖励视觉推理与导航任务中，SAGE 在多个环境优于无指导 RL；某些设置中 student 超过 VLM teacher。选择性调用只发生在部分训练步，部署调用数为零。收益主要出现在教师能帮助发现高回报轨迹时；若无指导探索已足够或教师动作不产生有信息量的经验，收益有限。v1 摘要未提供跨任务统一的具体提升值，因此这里不外推定量结论。

## 证据质量与局限

论文已被 EMNLP Findings 接收，正文含多表实验，证据中等偏强；但领域集中在视觉导航/推理，不等同于文本工具 Agent 的长轨迹。策略熵是 learner 不确定性的代理，不保证对应 teacher 有用性；advantage 也可能在稀疏回报和长信用链中高方差。尚未看到公开代码，复现实用性待确认。

## 最接近的相关工作

接近 DAgger、主动模仿学习、uncertainty-based teacher querying、OPDVR/RA-OPD 的环境奖励门控，以及 AED/SMOPD/SuRe 的熵选择性蒸馏。SAGE 的差异是教师建议被实际执行并由环境收益检验，而非只比较 logits。

## 如何复用或推进 LLM-as-a-Verifier

**分析推断**：将动作熵与 verifier 的序数评分熵、不同 verifier 的分歧联合用作查询触发；teacher 先输出 A/B/T 或评分分布，再由环境真值对建议分支作后验校准。对长轨迹，查询单位应从 token 改为状态/步骤分叉，并记录“高熵但 teacher 无信息”的负例训练路由器。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：用环境 advantage 作为 verifier 分布蒸馏权重，比较二值门、连续权重与无权重。
- **A/B/T/序数**：同前缀采样三个行动，只有执行结果支持排序时才蒸馏；不确定时保留 tie 概率。
- **真值门控**：环境结果负责校验教师，不让 VLM 自评分闭环决定自身可信度。
- **critique states**：在高熵状态让 student 先产 critique，再让 teacher 纠偏；只保留能提高后续回报的 critique。
- **探索**：熵用于决定求助，不应直接等价于“强制模仿”；高熵且 teacher 低价值时继续探索。
- **sealed eval**：评测不调用训练 teacher，并用独立环境种子、未见布局和固定程序 checker 检查真实迁移。