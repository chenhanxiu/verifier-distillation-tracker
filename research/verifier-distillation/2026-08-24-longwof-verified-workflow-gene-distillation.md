# LongWoF-Bench: Evaluating EvoMap Genes for Verifiable Long-Workflow Tasks

## 基本信息

- 作者：Xiao Zhang、Qumeng Sun、Jihao Li、Yiming Ren、Xiang Liu、Haoyang Zhang、Junjie Wang
- 首次公开日期：2026-08-24
- 版本日期：2026-08-24（v1）
- arXiv：2608.23200
- 原始论文：https://arxiv.org/abs/2608.23200
- DOI：https://doi.org/10.48550/arXiv.2608.23200
- 代码：论文公开页未提供

## 一句话结论

将 verifier 确认的真实执行轨迹压缩为可复用 EvoMap Gene，比从参考答案蒸馏的 Gene 更有效：在 778 个机器可验证长流程任务中，对七个模型提升 8.7–15.5 个百分点。

## 真正新增的内容

**论文原文结论：** 构建包含 778 个机器可验证任务的 LongWoF-Bench，并显示“经验证执行经验的 provenance”而非单纯压缩表示，是 Gene 迁移有效性的关键。

**分析推断：** 这为 student-generated critique/skill state 提供了强约束：只有被环境 verifier 确认的学生轨迹才应进入经验蒸馏池，参考解法本身不一定是最优 teacher 状态。

## 核心方法

从完成长流程任务的执行轨迹中抽取结构化 Gene，记录策略、约束与失败模式，并让其他模型复用。任务覆盖代码生成、Agent 环境合成、数学推理和规则遵循，最终产物均可机器验证。

## 关键实验结果

- 778 个 machine-verifiable 任务；其中 252 个具备 verifier-confirmed Claude Opus 轨迹。
- Evolved Gene 相对 Skill 在全部七个模型上提升 8.7–15.5 个百分点，并跨模型家族迁移。
- 参考答案蒸馏的 Gene 没有同等优势。
- 对 Claude Opus，Gene 比 Skill 多完成 39 个任务，求解 token 减少 9.9%。

## 证据质量与局限

证据质量中高：任务规模较大、终态可验证、跨七个模型，并有 reference-distilled 对照。局限是只有 252 个任务有确认轨迹；Gene 抽取过程可能依赖特定强模型，公开页未提供代码或对污染、重复任务和 verifier 漏洞的完整审计。

## 最接近的相关工作

最接近 ReasoningBank、SKALD、MemGuard、MERA 和 verifier-gated experience distillation。不同点是直接比较“真实验证轨迹抽取”与“参考答案蒸馏”，凸显经验 provenance。

## 如何复用或推进 LLM-as-a-Verifier

将 verifier 从最终评分器提升为经验准入签名：保存终态检查、关键中间证据、版本和置信度。Gene/critique 的每个结论都可追溯到被验证的轨迹片段。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 优先蒸馏 verifier-confirmed student rollout，而非静态 reference trajectory。
- **A/B/T：** 对同任务的成功 Gene、失败 Gene 和参考 Gene 做三路比较，检验 provenance 效应。
- **真值门控：** 机器验证是 Gene 进入 teacher 池的硬门槛。
- **Student critique states：** 从学生真实失败与恢复轨迹提取 critique，保留证据链接。
- **高熵探索：** 多条通过 verifier 的异质轨迹都保留，避免压成唯一“标准路线”。
- **Sealed eval：** 隐藏 verifier 测试与最终任务，防止 Gene 针对公开检查器过拟合。
