# M4Bench：程序规格与严格检查驱动的 Agent 评测

- **论文标题**：M4Bench: Evaluating Procedural Specification for Clinical EHR Derivation Agents
- **作者**：Hannes Ill, Rafi Al Attrach, Rajna Fani, Ahram Han, Ryohei Yamamoto, Marlene Louisa Moerig, Dukyong Yoon, Leo Anthony Celi
- **首次公开日期**：2026-10-27
- **版本日期**：2026-10-27（v1）
- **原始论文**：https://arxiv.org/abs/2610.37459
- **代码链接**：https://github.com/hannesill/m4/tree/m4bench-neurips2026-camera-ready/benchmark
- **标识**：arXiv:2610.37459；DOI: 10.48550/arXiv.2610.37459

## 一句话结论

严格程序检查显示“部分 reward 提升”与真正完成任务相差很远；规格完整性比技能包装本身更关键。

## 真正新增的内容

**论文原文结论**：M4Bench 用 28 个临床 EHR 派生任务分解 specification completeness、delivery format 与 schema familiarity 的贡献，并发布版本化技能、评测代码和逐次运行证据。

**分析推断**：该设计可作为 sealed Agent verifier 模板：把动态数据、时间窗、缺失规则和输出粒度编译为冻结检查器，避免 LLM Judge 将“看起来合理”误当完成。

## 核心方法

在 MIMIC-IV 与 eICU 上构建 15 个任务族；用 Docker 隔离执行 coding Agent；通过 operational spec、targeted skill、decoy skill、raw SQL、schema 混淆/重构等对照拆分监督来源。

## 关键实验结果

Codex campaign 中技能相对无技能 reward +0.136，28 个任务中 26 个改善；八任务控制集上 operational spec 单独 +0.162，技能在其上仅 +0.024，统计上不可区分于零。schema 混淆与重构分别保留 86% 与 70% 的技能增益。严格全通过仅为有技能 25/280、无技能 13/280；key F1 仅 +0.003。Claude Code 复现实验方向一致（+0.120，21/28 改善）。

## 证据质量与局限

优点是多模型复现、严格执行检查、decoy 和 schema 对照，并公开证据。局限是临床任务专门化强，reward 为与 reference 的部分一致而非真实临床效用；部分结果为描述性，不能证明技能在其他 Agent 域无效。

## 最接近的相关工作

最接近 Ground-truth-as-code、AutoTuneBench、GameLogicBench、AuditKIT 与 Harness or Model；共同强调执行环境、规格和 harness 必须从模型能力中拆开。

## 如何复用或推进 LLM-as-a-Verifier

将任务规格编译为多维检查：数据来源、时间窗、缺失处理、行粒度、schema 约束与最终值。LLM verifier 只负责解释失败与生成 critique，最终得分由隔离执行器重算。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：使用各检查维度的部分通过向量，而不是单一总 reward；硬检查决定方向。
- **A/B/T 与序数分布**：依据通过维度与严重度生成序数分布；不同维度互有胜负时保留 T。
- **程序化/环境真值门控**：Docker、冻结数据快照和严格检查器作为 teacher anchor。
- **student-generated critique states**：critique 必须定位失败规格并提出可执行修复，修复后重新运行才能准入。
- **高熵分叉与探索**：保留能满足不同规格子集的候选，用分维度证据而非总分过早裁剪。
- **sealed eval**：隐藏 schema 扰动、decoy 技能与 reference-validity audit；分别报告部分 reward、全通过率和 key F1，防止 evaluator 共适应。