# Beyond QASecClaw：Verifier 反馈不能替代确定性证据准入

- **论文标题**：Beyond QASecClaw: Agent Scaling, Verifier Feedback, and Evidence Reliability in Software Assurance
- **作者**：S M Abdulla Al Mamun, Akif Islam, Mohd. Ruhul Ameen
- **首次公开日期**：2026-10-27
- **版本日期**：2026-10-27（v1）
- **原始论文**：https://arxiv.org/abs/2610.36947
- **代码链接**：未在论文首页给出
- **标识**：arXiv:2610.36947；DOI: 10.48550/arXiv.2610.36947

## 一句话结论

增加 Agent 上下文或直接暴露 verifier 反馈，可能同时增加正确与错误 verdict；在可执行工具证据存在时，应由确定性 scope check 决定监督准入。

## 真正新增的内容

**论文原文结论**：五组软件保证实验、13,638 次模型请求显示，多上下文扩展未改善 unsafe clearance；原始 verifier 反馈虽提高正确判断，也显著增加错误判断；构造特定的确定性 scope check 在误导证据包上优于模型聚合。

**分析推断**：这直接反驳“更多 reviewer/反馈必然提高 teacher 信号质量”，并支持把环境证书放在软 Judge 之前。

## 核心方法

研究 Java warning、OWASP、Defects4J、SV-COMP 与故意误导证据包；比较 1–50 个 specialist context、原始 verifier 反馈、模型 verdict 聚合与 JBMC/JVM 或 construction-specific 检查。

## 关键实验结果

八个 warning 上，context 从 1 增至 50 导致 token 使用增加 49 倍但 unsafe clearance 无改善。32 个 SV-COMP 任务上，反馈令平均正确 verdict 从 12.7 增至 22.0，同时错误 verdict 从 1 增至 7；JBMC+JVM 得到 26 个正确和 6 个 unresolved。两组各 120 个证据包中，模型拒绝 70%–100% 的适用反例，而 scope check 全部正确分类。

## 证据质量与局限

优点是包含确定性工具对照、误导证据压力测试和较大请求量。局限是任务规模仍小、主要模型为 Qwen2.5-Coder-7B-Instruct，结果为描述性实验；Defects4J 三个 bug 未发现目标缺陷，其中一个还受 adapter 支持限制。

## 最接近的相关工作

最接近 GameLogicBench、Ground-truth-as-code、ContrAgent、AuditKIT 和 Checking the Checkers；与多 Judge 共识研究共同说明相关错误不能靠简单投票消除。

## 如何复用或推进 LLM-as-a-Verifier

采用两层 verifier：第一层确定性地验证证据适用范围与执行结果；第二层 LLM 解释未覆盖部分并允许 abstain。训练 generative verifier 时，把“证书不适用”与“程序失败”分成不同标签。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：硬证书决定梯度方向；LLM score 只在证书覆盖域内调节幅度。
- **A/B/T 与序数分布**：无法建立共同证据域时标 T，不以多数票伪造可比性。
- **程序化/环境真值门控**：优先采用测试、JVM/JBMC、schema/scope 检查。
- **student-generated critique states**：critique 必须携带可执行证据及适用性说明。
- **高熵分叉与探索**：聚合分歧大的状态应送确定性审计，而非直接剪枝。
- **sealed eval**：隐藏证据包构造与 scope check，防止 verifier 学会表面模式；同时报告 correct、incorrect、unresolved 三类。