# Verifiable On-Policy Distillation：以可验证奖励校正在线策略蒸馏

- **论文标题**：Verifiable On-Policy Distillation
- **作者**：Juntong Shi, Stefano Ermon, Jure Leskovec, Minkai Xu
- **首次公开日期**：2026-11-23
- **版本日期**：2026-11-23（v1）
- **原始论文**：https://arxiv.org/abs/2611.30325
- **DOI**：https://doi.org/10.48550/arXiv.2611.30325
- **代码/项目页**：https://github.com/juntongshi48/VOPD （论文页面注明代码将公开，当前可用性需复核）

## 一句话结论

VOPD 把稀疏的序列级可验证奖励投影到 teacher 的隐式奖励方向上，形成低方差、逐 token 的在线蒸馏目标，是“环境真值定方向、teacher 分布定幅度”的直接实现。

## 真正新增的内容

**论文原文结论**：作者指出标准 OPD 只模仿 teacher、未利用可验证结果；其方法用 verifier 奖励校正 teacher 信号，并通过 Rao–Blackwell 化得到全词表上的稠密目标。**分析推断**：这比事后把 pass/fail 乘到 KL loss 上更适合作为 score-level verifier distillation 基线，因为它显式处理序列奖励到 token 信用的投影，而不是把所有步骤等权归因。

## 核心方法

在 student 自生成轨迹上计算 teacher 隐式奖励方向，再把终局 verifier 回报投影到该方向；对采样动作的估计做全词表条件期望以降方差。目标外推幅度由 teacher–verifier 一致性自适应调节：teacher 与可验证结果一致时强化，冲突时限制迁移。

## 关键实验结果

**论文报告**：在 2 组 teacher/student 配置、8 个数学推理基准上，VOPD 相比 vanilla OPD 及多种 OPD 变体持续提高最终表现和学习效率。摘要未给出所有任务的逐项数值，结论仍需以正文表格和代码复现为准。

## 证据质量与局限

优点是监督来自可执行/可判定的终局奖励，并与 on-policy 状态分布对齐；跨模型配置和多基准提供一定外推证据。局限是实验集中在短到中程数学推理，尚未证明对含工具失败、部分可观测和长时延回报的 Agent 轨迹同样稳健；teacher 隐式奖励方向若系统性错误，投影仍可能遗漏替代策略。

## 最接近的相关工作

最接近 γOPD 的时间信用、UECR-GRPO 的 teacher 熵重分配、Low-Bit OPD 的执行奖励联合训练，以及 PACT 对 OPD teacher/critic 对齐的理论分析。VOPD 的差异在于直接把可验证序列奖励转成 teacher 方向上的稠密更新。

## 如何复用或推进 LLM-as-a-Verifier

可将二元 verifier 换成序数概率分布，并分别投影期望得分与不确定性；对 A/B/T 分支用环境真值先裁决可判定样本，T/证据不足样本保持分布而非硬压成负例。student-generated critique 只能在复执行通过后进入投影目标，避免语言自洽代替事实正确。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：把 VOPD 作为 score-level OPD 主基线，比较“纯 KL、终局奖励门控、VOPD 投影、序数分布投影”四组；在高熵分叉保留多条可恢复路径，而非只强化最高分分支。训练 verifier 与策略时共享在线数据，但最终指标必须由冻结环境、隐藏任务和独立 Judge 的 sealed eval 给出，以检测 evaluator 共适应与 reward hacking。
