# DashArena：基于交互轨迹证据的 Pairwise Judge 蒸馏

## 基本信息

- **论文标题**：DashArena: Benchmarking LLMs on Interactive Analytic Dashboard Generation
- **作者**：Xiaotong Wang, Dazhen Deng
- **首次公开日期**：2026-08-11
- **当前版本日期**：2026-08-11（v1）
- **arXiv ID**：2608.10567
- **原始论文**：https://arxiv.org/abs/2608.10567
- **代码**：截至记录时未发现公开代码仓库

## 一句话结论

DashArena 将可重放交互轨迹和浏览器执行报告加入 pairwise VLM Judge，并把 proprietary teacher 蒸馏成 DashJudge-8B；交互证据使人类一致率提高 8.1 点，但 45 对 held-out judge test 仍很小。

## 真正新增的内容

**论文原文结论：** 对开放式交互 dashboard，仅看静态截图或能否执行不足以评价分析价值。候选模型同时生成 dashboard 与可重放交互轨迹，浏览器执行器提供视觉/执行证据，VLM Judge 做 A/B 比较，Bradley–Terry 聚合成系统排名；最终 Judge 再蒸馏到 Qwen3-VL-8B-Instruct。

**分析推断：** 这为长时程 Agent verifier 提供了一个完整模板：candidate-authored trajectory 负责声明意图，环境 executor 验证实际变化，generative teacher 产出 pairwise 标签，再蒸馏为开放权重 verifier。

## 核心方法

1. 模型先生成完整 dashboard HTML，再在保留代码上下文的第二轮生成交互 action chain。
2. 浏览器执行器重放轨迹，记录截图、交互是否执行及分析变化；候选只声明预期，不能控制最终判定。
3. proprietary VLM teacher 根据任务、A/B 截图、轨迹和执行报告做整体 pairwise 判断。
4. teacher 标注 300 对；255 对、114 个任务用于训练，45 对、20 个不重叠任务用于 Judge test。
5. 训练加入 A/B swap 并反转标签，得到 510 个 SFT 样本；使用 LoRA 微调 Qwen3-VL-8B。
6. 系统级结果用 Bradley–Terry 聚合。

## 关键实验结果

**论文报告：**

- DashJudge-8B 在 45 个 held-out teacher-test pairs 上复现 proprietary teacher 标签的准确率为 88.9%。
- 在 100 个人工标注 pairs 上，相对 base model，人类一致率提高 9.1 点，Cohen’s κ 从 0.419 升至 0.600；与 proprietary teacher 的人类一致性相近。
- 移除 trajectory 与 execution report、只保留任务和截图时，一致率为 71.7%、κ=0.441；加入完整交互证据后为 79.8%、κ=0.600，即 +8.1 点、κ +0.159。
- 100 对人工比较中 99 对有多数偏好，52 对全体一致。
- 排名稳健性分析中，100/120 个任务的重采样排名平均 Kendall τ=0.945；300 次采样均恢复 top model 与 top-three set。

## 证据质量与局限

**证据较强处：** 有 disjoint-task Judge test、人类对照、A/B swap、交互证据消融及 leaderboard 重采样。

**论文明确或可见的局限：**

- Judge test 仅 45 对、20 个任务，无法充分覆盖开放式错误模式。
- 使用单一整体 pairwise 标签，没有建模人群偏好分布；作者明确把 distributional modeling 留作未来工作。
- model-authored trajectory 可能选择性展示自身强项；执行器虽验证行为，但轨迹覆盖度仍主要由 Judge 解释。
- benchmark 专注 dashboard，结论不能直接外推到任意 Agent。
- proprietary teacher、student Judge 与 leaderboard protocol 仍可能共享偏差；当前 human set 较小。
- 截至记录时没有公开代码链接。

## 最接近的相关工作

Arena-style pairwise judging、Bradley–Terry 排名、interactive artifact evaluation、generative reward/judge distillation，以及 Agent-as-a-Judge。它区别于静态 Judge 的关键是把可重放行为证据纳入比较。

## 如何复用或推进 LLM-as-a-Verifier

**分析建议：**

- 将下一步 Agent 动作的候选 A/B 各自做短程反事实续跑，向 Judge 提供状态变化、工具回执和候选自述的预期贡献。
- 在 A/B 之外加入 tie，并让 teacher 输出失败/无贡献/部分推进/高贡献的序数分布。
- 采用 A/B swap、位置偏差审计和人类锚点校准蒸馏 student verifier。
- 将“model-authored trajectory”改造成“student-generated critique + expected state transition”，由环境执行器验证，而非直接相信文字。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：把 teacher 的 pairwise 判断转换为序数 latent score 分布，再在 student 访问状态上蒸馏。
- **A/B/T**：DashArena 只做 A/B；你的路线应显式加入 tie，避免强制排序近似等价动作。
- **真值门控**：执行报告是强证据层，LLM Judge 只负责解释开放式价值。
- **Critique states**：候选动作自述预期效果相当于 critique/proposal，但必须由重放验证。
- **高熵探索**：保留能够展示不同有效工作流的候选，不以单一路径为 reference。
- **Sealed eval**：训练 pairs、Judge test 与最终 Agent leaderboard 应任务隔离；最终 evaluator 不参与生成 teacher labels。

DashArena 是目前最接近“交互证据 + pairwise verifier distillation”的可复用实验设计，但下一步应补 tie、序数概率和更大规模独立人类校准。
