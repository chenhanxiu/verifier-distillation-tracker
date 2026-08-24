# ProofJudge：工具真值锚定的形式化证明质量 Judge

- **论文标题**：ProofJudge: Tool-Grounded LLM Evaluation of Formal Proof Quality in Mathlib
- **作者**：Shane Caldwell
- **首次公开日期**：2026-08-20
- **版本日期**：2026-08-20（v1）
- **arXiv ID**：2608.20432
- **原始论文**：https://arxiv.org/abs/2608.20432
- **DOI**：https://doi.org/10.48550/arXiv.2608.20432
- **代码链接**：https://github.com/SJCaldwell/ProofJudge
- **数据与轨迹**：https://huggingface.co/datasets/SJCaldwell/proofjudge ，https://huggingface.co/datasets/SJCaldwell/proofjudge-eval-traces

## 一句话结论

在 Lean kernel 已保证正确性的前提下，ProofJudge 用工具访问真实 Mathlib 状态评价更软的工程质量，并以“被 reviewer 接受的最终版本优于初稿”构造 pairwise 人类偏好锚点。

## 真正新增的内容

**论文原文结论**：作者把硬正确性与软质量分离：kernel 负责可执行真值，agentic Judge 用搜索工具评价库复用、自动化适配、结构清晰度、statement 质量和 Mathlib 规范。

**分析推断**：这正是 Agent verifier 的理想分层：环境/程序 verifier 决定“动作是否有效”，LLM Judge 决定“是否是可维护、清晰、低成本的好动作”，两者不应混为单一标量。

## 核心方法

Judge 可在目标 commit 上搜索 Mathlib，并对五个维度独立打 1–10 分后汇总。测试集包含 218 对来自不同 PR 的初稿与最终接受版本；Judge 不知道它们成对，也不看到另一版本得分，每次最多使用 20 次工具调用。

## 关键实验结果

**论文原文**：六个 Judge 的人类偏好一致率为 63.5%–80.8%，均显著高于随机；Claude Sonnet 5 为 80.8%（95% CI 73.6–88.2），两个开放权重 Judge 约 70%，成本约为最佳 Judge 的十分之一。重复运行会翻转约五分之一到接近一半 verdict，作者强调单次运行不足以支持细微差异。

## 证据质量与局限

优点是硬真值、真实 PR、人类审查结果、开放 harness/数据/完整轨迹和重复实验。局限是论文仅 4 页、单一 Mathlib 域，开发集曾用于调 rubric；“最终合并版本更好”是合理但不完美的人类偏好代理。高运行方差说明不能直接将单次分数用于 RL。

## 最接近的相关工作

最接近 Agent-as-a-Judge、程序化证明 verifier、DashJudge、WebGrader 与 SARA。区别在于 ProofJudge 把编译正确性留给 kernel，而让工具化 Judge 评价超出正确性的工程品质。

## 如何复用或推进 LLM-as-a-Verifier

为每个工具动作建立“硬合法性 + 软工程质量”双通道：前者来自执行、schema 和环境状态，后者来自可检索真实系统状态的 Judge。训练 verifier 时保留五维输出和运行间方差；对高方差样本使用多次采样或升级更强模型。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：分别蒸馏硬 pass 与软质量分布，不让软 Judge 覆盖环境真值。
- **pairwise A/B/T 与序数分布**：直接复用“初稿/修订稿”pairwise 协议；差异落入重复运行置信区间时标 Tie。
- **真值门控**：工具调用必须先通过执行或状态校验，随后才进入 LLM 质量评分。
- **student-generated critique states**：student 生成检索计划和质量 critique，Judge 通过工具验证其中引用。
- **高熵探索**：多个均通过硬 verifier 的方案可按软质量分布排序，而非只保留唯一实现。
- **sealed eval**：冻结未参与 rubric 调优的 PR 与 commit，并分离训练 Judge、调参 Judge 和最终 sealed Judge。
