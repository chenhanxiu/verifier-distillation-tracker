# SWE-VERIFIER：面向 Coding Agent 的选择性验证

- **论文标题**：SWE-VERIFIER: Selective Verification for Cost-Efficient Coding Agents
- **作者**：Kaijian Zou, Vaibhav Chennareddy, Yunxiang Zhang, Naihao Deng, Longju Bai, Jiaxin Pei, Rada Mihalcea, Lu Wang
- **首次公开日期**：2026-10-21
- **版本日期**：2026-10-21（v1）
- **原始论文**：https://arxiv.org/abs/2610.30284
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.30284
- **代码与数据**：https://github.com/zkjzou/SWE-Verifier （arXiv 声明的链接；本次检查时公开页面暂未解析）

## 一句话结论

轻量 generative verifier 只在少于 4% 的关键步骤触发候选分叉与排序，就能以约 1.1 倍成本提升 coding-agent 解题率，给“高熵状态才调用 verifier”的路线提供了直接实证。

## 真正新增的内容

**论文原文结论**：SWE-Verifier 同时学习两件事：判断当前动作是否值得额外采样，以及在触发后对多个候选动作排序。训练数据把对比动作、后续环境 observation 和 rubric-guided teacher score 绑定起来。

**分析推断**：相较全轨迹或每步验证，该工作把 verifier 变成稀疏预算分配器；这比单纯提高 judge 准确率更接近长时程 Agent 的实际成本约束。

## 核心方法

1. 从 Qwen3.5-4B 训练轻量生成式 verifier。
2. 对 proposed action 输出触发分数；高风险状态才生成额外候选。
3. 利用动作之后的环境 observation 与 rubric teacher 分数构造偏好组。
4. 对触发后的候选排序，选定动作后再执行。
5. 在未见过其动作分布的另一 coding model 上测试迁移。

## 关键实验结果

**论文原文结论**：在 mini-swe-agent harness 中，MiniMax-M2.7 的 resolution 从 75.47% 提升到 77.20%，成本为 1.09 倍；对训练时未见动作的 DeepSeek-V4-Flash，从 72.60% 提升到 74.27%，成本为 1.13 倍。两者验证步骤均少于 4%，效果不低于全轨迹或每步验证基线。

## 证据质量与局限

有跨被验证模型的迁移实验、成本与成功率联合报告，证据较强。局限是改进幅度约 1.7 个百分点、领域限于 coding，训练标签仍含 rubric-guided teacher score；摘要不足以判断 verifier 是否会与 harness 的特定错误分布共适应。

## 最接近的相关工作

最接近 EPIG-Tree、Belief-Shift Branching、Speculative Uncertainty、FARM，以及 action-level process reward model；与 VG-OPD 的共同点是按状态选择监督源，但本工作选择的是“是否验证/分叉”。

## 如何复用或推进 LLM-as-a-Verifier

可将 verifier 的输出扩展为联合分布：不触发、触发但保留探索、触发并强制替换；训练标签由环境重放结果、后继 observation 与 teacher critique 共同构造。生成式输出应附带证据指针和预期后继状态，便于程序化验真。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：只在 verifier 触发的状态做 teacher score 蒸馏，其他状态保持 student on-policy 分布。
- **A/B/T**：候选排序天然产生 A/B；无显著差异或证据不足输出 T，避免强行排序。
- **硬真值门控**：teacher 分数必须由编译、测试、环境 observation 验证方向。
- **critique states**：把“为何触发 + 候选预期后果”作为 student-generated critique state，再经执行结果筛选。
- **高熵探索**：验证预算分配应同时参考策略熵、候选价值差和可恢复性，而非单一置信度。
- **sealed eval**：冻结触发器阈值，在隔离仓库、未见项目和独立 harness 上评估触发召回、误触发成本与最终成功率。
