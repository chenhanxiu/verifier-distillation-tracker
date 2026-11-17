# Auditable Authorization for LLM Agents: Empirical Evidence Across Model, Harness, and Workflow Layers

- **作者**：Bangjie Deng、Xiaoxuan Lu、Wenjun Chen、Chengge Wen、Yulin Wang、Jiayue Meng、Yao Yu、Liying Liang、Weijia Han、Ziwei Hong、Zidong Yu
- **首次公开日期**：2026-11-14
- **版本日期**：2026-11-14（v1）
- **原始论文**：https://arxiv.org/abs/2611.19237
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.19237；DOI: 10.48550/arXiv.2611.19237

## 一句话结论

【论文原文】人类批准只有在“拒绝必停、批准必完成”同时成立时才是有效控制；模型、harness 与 workflow 三层都可能让授权意图与真实副作用分叉。

## 真正新增的内容

【论文原文】论文形式化 refusal safety 与 bounded authorization completeness，使用配对决策、精确 trace 和原生业务状态 witness 审计三个边界：模型选调用、harness 调度/恢复、workflow 把决定路由到受保护效果。方法定位 intent、生成调用、dispatch 与真实效果之间的首个可观测分叉。

【分析推断】这是长时程 Agent verifier 的硬真值接口：最终标签不能来自“模型说已拒绝/已执行”，必须来自 protected effect 的原生状态 witness。它也补充了只关注 unsafe false positive 而忽略 approved-action false negative 的评测偏差。

## 核心方法

1. 分别定义拒绝安全与有界授权完成性。
2. 跨 model、harness、workflow 收集配对决定和 exact trace。
3. 用 native business-state witness 验证真实副作用，并定位首个分叉层。

## 关键实验结果

【论文原文】覆盖 3 个模型、5 个 prompt arm、4 种运行时批准设计、2 个额外框架 replay 和 100 个公开 workflow 来源。300 次批准中 7 次未完成但无拒绝效果；并行确认每模型丢失 3 个已批准分支；CrewAI 恢复遗漏 336/672 个批准；59 个可比 n8n workflow 中 4 个在 Reject 后仍执行。

## 证据质量与局限

【论文原文】多层、配对、原生状态证据使错误归因比只读日志更可靠。

【分析推断】实验覆盖的工具与框架仍有限，bounded completeness 的时间窗选择会影响结论；人类授权本身可能错误。该方法验证控制边界，不等于验证任务目标或安全规范完整。

## 最接近的相关工作

最接近 Co-Sight Harness、GCAC、ContrAgent、MAGS 与 Ground-truth-as-code Agent Evaluation。本文独特点是同时测拒绝安全和授权完成，并把失败定位到模型/harness/workflow 的首个边界。

## 如何复用或推进 LLM-as-a-Verifier

让 verifier 同时输出 intent verdict、dispatch verdict 与 effect verdict；只有 native effect witness 可作为终局硬标签。生成式 critique 必须引用具体版本、调用 ID 与业务状态，不能依据自然语言确认。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：分别蒸馏 refusal safety 与 authorization completeness，禁止合成一个平均分。
- **pairwise A/B/T 与序数分布**：intent 相同但 effect 不同形成强 A/B；缺失 witness 标 T。
- **环境真值门控**：native business state 决定方向，trace Judge 只定位责任层。
- **student-generated critique states**：critique 必须绑定首个分叉和真实 effect 证据。
- **高熵探索**：授权完成路径可多样，但所有路径须满足相同 protected-effect 契约。
- **sealed eval**：隐藏恢复、并发和版本漂移案例，冻结 effect witness 与审批版本。

