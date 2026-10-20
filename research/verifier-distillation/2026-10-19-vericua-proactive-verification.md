# VeriCUA: Learning Proactive Verification for Reliable GUI Agent Rewards

- **作者**：Zhizhou Wang、Yaxi Lu、Zhong Zhang、Zikun Hu、Xin Cong、Yankai Lin、Fangming Liu
- **首次公开日期**：2026-10-19
- **版本日期**：2026-10-19（v1）
- **原始论文**：https://arxiv.org/abs/2610.26469
- **arXiv ID**：2610.26469
- **DOI**：https://doi.org/10.48550/arXiv.2610.26469
- **代码/项目**：未公开

## 一句话结论

主动 verifier 的瓶颈不是模型规模，而是学会在真实终态中检查什么、何时停止；VeriCUA 用一次性环境交互训练该策略。

## 真正新增的内容

把 GUI reward agent 拆成可训练 Judge 与冻结 Probe，并针对每个不可重放终态只有一次验证机会的约束设计在线 RL。

## 核心方法

Judge 决定下一项环境检查或停止，Probe 在现场执行；以 verdict 正确性和 Probe 成本联合优化，并跨 OSWorld、MobileWorld、WebArena-Verified 测试。

## 关键实验结果

prompted 4B 到 GPT-5.4 均停在 68%–70% macro agreement；VeriCUA 比 few-shot GPT-5.4 高 5.36 点且少用 47.6%–59.8% Probe token，1B 模型也超过全部 prompted Judge；作为 Actor RL 奖励时总体任务成功率 +3.21 点、held-out 多应用任务 +5.40 点。

## 证据质量与局限

跨三个 GUI benchmark、跨规模与下游 RL 的证据完整；但终态单次验证使方差估计困难，冻结 Probe 的盲区仍可能系统性遗漏证据。

## 最接近的相关工作

与 FailBench、Ground-truth-as-code、CoVer、Speculative Uncertainty 和工具调用 verifier 最接近。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier 建模为信息采集 policy：先输出待检查证据动作，再输出 A/B/T 或序数分布；Probe 返回只读环境证据，Judge 不直接操作环境。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】现有 Agent verifier × OPD 应比较“静态读轨迹”与“主动探测后评分”，并将探测成本纳入 score；sealed eval 使用独立 Probe/任务快照，避免检查策略与训练环境共适应。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论均来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
