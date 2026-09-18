# LLM-as-an-Improver：Verify–Repair–Reselect

## 元数据
- **论文标题**：LLM-as-an-Improver: Turning Verification into Better Candidates
- **作者**：Akiyoshi Tomihari、Yuma Ichikawa
- **首次公开日期**：2026-09-17
- **版本日期**：2026-09-17（v1）
- **原始论文**：https://arxiv.org/abs/2609.19515
- **代码链接**：未发现公开代码链接

## 一句话结论
Verifier 反馈不应在排序后丢弃；它可以条件生成修复 winner、修复 runner-up 和全新路径，再用原评价标准重选，甚至救回初始候选全部错误的案例。

## 真正新增的内容
**论文原文结论**：Verify–Repair–Reselect（VRR）保留初始 winner，并按需生成三种互补候选；推理时过滤无效与重复候选，再用原 verifier 重选。

**分析推断**：这是 generative verifier 与 student-generated critique states 的直接闭环，但也提高 evaluator 共适应风险，必须让修复生成器和最终 sealed evaluator 分离。

## 核心方法
1. 验证固定候选池并保留 winner。
2. 基于反馈修复 winner、修复 runner-up、生成新方法候选。
3. 仅用推理时信息去除无效/重复项。
4. 在同一原始评价标准下重新选择。

## 关键实验结果
**论文报告**：跨多模型、代码生成和推理基准，VRR 在许多设置中优于固定池 verifier selection，并能在初始候选全部错误时恢复正确解。摘要未提供统一数值提升。

## 证据质量与局限
覆盖多模型和两类任务，并检查 all-wrong 初始池。局限是 verifier 反馈若错误会被放大；同一 verifier 同时指导修复与重选会产生闭环偏置；尚未覆盖有外部副作用的长轨迹 Agent。

## 最接近的相关工作
EquiReview-R、PaperDoctor 与 Draft-Verify-Revise 关注 critique 修订；ParallelWorld 关注未来分支搜索。VRR 的核心区别是把 verifier 反馈显式用于扩张候选集。

## 如何复用或推进 LLM-as-a-Verifier
将 VRR 扩展到 Agent 分叉：修复当前最佳动作、修复次优动作、探索新策略；critique 必须绑定环境证据。训练时可蒸馏“原候选→反馈→修复候选→真值变化”的完整 transition。

## 对 Agent verifier × OPD 实验路线的具体影响
- **score-level OPD**：只蒸馏经执行验证确实改善的修复。
- **A/B/T**：原候选与修复候选形成局部 A/B；无法执行则保留 T。
- **真值门控**：环境结果决定修复是否进入训练。
- **critique states**：直接形成 student-generated critique transition。
- **高熵探索**：新方法候选防止只在 winner 邻域坍缩。
- **sealed eval**：最终评测必须使用未参与修复的 Judge/隐藏测试，审计 reward hacking。