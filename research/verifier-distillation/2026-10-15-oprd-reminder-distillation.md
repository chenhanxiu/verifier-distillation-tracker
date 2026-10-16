# OPRD：面向长时程 Coding Agent 的 On-Policy Reminder Distillation

- **论文标题**：OPRD: On-Policy Reminder Distillation for Long-Horizon Coding Agents
- **作者**：Yuechen Luo, Zhiyi Lai, Miao Ziqi, Zihang Xu, Jingxuan Xu, Songwei Yu, Wenqiang Zhu, Weihao Li, Junhao Fan, Haoyang Huang, Yanan Wu, Ken Deng
- **首次公开日期**：2026-10-15
- **版本日期**：2026-10-15（v1）
- **原始论文**：https://arxiv.org/abs/2610.21496
- **代码**：论文页面未提供公开代码链接

## 一句话结论

OPRD 在不改变部署时输入的前提下，把终局测试诊断和局部环境观察转成仅供 teacher 使用的 reminder，并在 student 自己生成的失败前缀上做 reverse-KL，是目前最贴近“环境真值门控的长轨迹 score-level OPD”的直接实现。

## 真正新增的内容

**论文原文**：作者不是把 reminder 永久加入 Agent 上下文，而是只在训练时让 teacher 看见；成功的 reminder-free student rollout 用自回归自模仿，失败 rollout 才接收 reminder-conditioned teacher 的 reverse-KL。Global Reminder 来自最终测试诊断，Turn-local Reminder 仅作用于对应环境观察之后的下一次决策。

**分析推断**：这把“硬真值决定是否纠偏、privileged critique 决定如何纠偏”落实成了 outcome-routed OPD，可直接替换现有统一强制蒸馏的做法。

## 核心方法

1. student 在无 reminder 条件下生成完整仓库级 coding 轨迹。
2. 依据可执行测试结果路由：成功轨迹做 self-imitation；失败轨迹由带 Global/Turn-local Reminder 的 teacher 重评分同一 student prefix。
3. 在失败状态用 reverse-KL 迁移 teacher 的条件化动作分布；推理时完全移除 reminder。
4. teacher 与 student 都从 Coding SFT + Instruction-Following SFT 的两阶段初始化出发。

## 关键实验结果

**论文原文**：在 SWE-bench Verified、SWE-bench Pro 与 SWE-bench Multilingual 上，相比开源 Qwen3.5-4B 基座，三项平均任务解决率提高 11.3 个百分点；同一诊断协议下，聚合错误事件从 446 降到 222，减少 50.2%。

## 证据质量与局限

优点是使用真实仓库级执行测试、三个 SWE-bench 变体并报告过程错误；局限是摘要未给出多 seed 置信区间，也未证明 reminder teacher 在非 coding Agent、不同模型族或不可完全测试任务上同样可靠。成功轨迹的自模仿还可能复制偶然成功的冗余行为。

## 最接近的相关工作

与 STRIDE 的“首错定位后从正确前缀重启”、Persistent Teacher Anchoring 的执行前 teacher 承诺、γOPD 的终局奖励混合，以及 FLARE 的环境结算因果错误链最接近；区别在于 OPRD 直接在原始 student prefix 上做 reminder-conditioned reverse-KL。

## 如何复用或推进 LLM-as-a-Verifier

可把 Global/Turn-local Reminder 生成器视为可审计的 generative verifier：先由测试、lint、类型检查或环境状态产生不可伪造证据，再让 teacher 输出 A/B/T 或序数评分分布。对无足够证据的状态应输出 T/abstain，而不是强制负向蒸馏。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：新增“成功自模仿 / 失败 privileged-teacher”双路由基线，并比较固定 KL 与按 verifier 置信度加权。
- **A/B/T 与序数分布**：把测试诊断映射为 A=改进、B=保留、T=证据不足；保留完整概率而非硬标签。
- **真值门控**：方向必须由 sealed tests 或环境回放决定，teacher 只决定幅度和局部动作。
- **critique states**：只接纳能指向具体测试失败或环境观察的 reminder。
- **高熵探索**：在失败但 verifier 分歧高的分叉降低 reverse-KL，避免把尚未证伪的策略压平。
- **sealed eval**：训练 reminder 生成器、路由器与最终评测测试集必须隔离，另设隐藏仓库与隐藏诊断格式以防 evaluator 共适应。
