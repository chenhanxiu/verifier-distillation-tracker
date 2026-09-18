# Agent Harness 的价值：规划信息与 Verifier Release Control

## 元数据
- **论文标题**：How Do Agent Harnesses Create Value? Planning Information and Release Control in Stateful LLM Agents
- **作者**：Yukun Zhang、Kemu Xu、Yishen Chen
- **首次公开日期**：2026-09-17
- **版本日期**：2026-09-17（v1）
- **原始论文**：https://arxiv.org/abs/2609.20474
- **代码链接**：未发现公开代码链接

## 一句话结论
规划提升成功率，terminal verifier 降低错误放行；二者价值应按 false-pass 成本分开测量，而非把整个 harness 的效果归给模型或统一总分。

## 真正新增的内容
**论文原文结论**：通过 Fixed plan 与等字数 shuffled Sham 对照，论文隔离规划内容的贡献；再单独测只读 terminal verifier 对 oracle-invalid 与正确 episode 的拦截，给出成本—责任损失下的组件价值。

**分析推断**：这与用户现有统一 scaffold 评测高度相关：应分别报告“模型能力、规划 scaffold 增益、verifier release-control 增益”，避免 harness 改进污染模型排名。

## 核心方法
- 在 τ²-bench 的两个 Retail 实验和 Airline pilot 中做状态型 Agent 对照。
- Fixed 与 Sham 保持长度一致，仅改变规划信息。
- 只读 terminal verifier 独立决定是否放行。
- 按错误接受的 liability 分析规划与 verifier 的相对价值。

## 关键实验结果
**论文报告**：265 个 matched cells 中，Fixed 使 oracle-verified success 提高 7.17 个百分点（90% task-cluster bootstrap CI 1.15–13.36），增益集中于复杂任务。terminal verifier 拒绝 61% 的 Retail oracle-invalid episode，同时扣留 17% 正确 episode，每例额外成本低于 1 美分。高 liability 下，独立 verifier 以较低成本获得完整 harness 几乎全部 false-pass 收益。

## 证据质量与局限
匹配对照与 oracle 验证较强，且报告误杀与成本。局限是主要结果集中 Retail，Airline 仅 pilot；90% 而非 95% 区间；固定规划与真实动态 planner 仍有差距。

## 最接近的相关工作
Harness or Model?、Harness-of-Harness、LLM-as-a-Judge Is Not an Oracle 与 AutoTuneBench 都强调 scaffold/evaluator 隔离。本文新增组件级因果对照和 liability-aware 价值分解。

## 如何复用或推进 LLM-as-a-Verifier
在评测结果中单列 base policy、plan-assisted policy、terminal release gate 三个读数；verifier 输出通过/拒绝/需复核的序数分布，并对误杀做成本敏感阈值校准。

## 对 Agent verifier × OPD 实验路线的具体影响
- **score-level OPD**：不要把 terminal gate 后的成功率直接当 student 原始能力。
- **A/B/T**：用 Fixed/Sham 配对分离信息贡献；不确定放行标 T。
- **真值门控**：oracle 判定用于校准 false pass/false reject。
- **critique states**：terminal verifier 只读，避免被 policy 改写。
- **高熵探索**：训练期允许探索，发布期按 liability 设置门槛。
- **sealed eval**：模型、planner、verifier 分别冻结版本并做组件消融。