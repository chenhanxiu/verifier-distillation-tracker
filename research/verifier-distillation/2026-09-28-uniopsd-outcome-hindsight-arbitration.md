# UniOPSD: Unifying Outcome and Hindsight Feedback for Agentic Reinforcement Learning

- **作者**：Zenghuang Fu, Zhaoyang Li, Qiuyuan Ai, Xiaofeng Han, Zelong Zheng, Haoyu Wu, Tianyu Fu, Chenxu Zhao, Minghui Wu, Guannan He, Changwei Wang
- **首次公开日期**：2026-09-28
- **版本日期**：2026-09-28（v1）
- **原始论文**：https://arxiv.org/abs/2609.34810
- **代码**：https://github.com/Zenghuang-Fu/Uniopsd

## 一句话结论

【论文原文】UniOPSD 在共享交互锚点上统一环境终局回报与成功同伴的 hindsight 信号，并按历史一致性、当前可用性和相对精度逐决策仲裁两者权重。

## 真正新增的内容

【论文原文】论文首先发现 outcome 与 hindsight 的平均一致为正，但局部冲突显著；它不是固定混合两类奖励，而是构造可比较的局部信用估计，再进行全局与局部两级自适应仲裁。

## 核心方法

1. 从环境回报构造 outcome credit。\n2. 在共享状态锚点处，以成功同伴轨迹构造 hindsight credit。\n3. 历史一致性控制全局混合，当前信号可用性和精度控制局部权重。\n4. 保留 episode-level outcome，再用有界 token modulation 细化策略更新。

## 关键实验结果

【论文原文】Qwen2.5-3B/7B 在 ALFWorld 达到 82.8%/83.6%，WebShop 达到 75.0%/82.0%，Search-QA 达到 45.3%/49.8%；3B WebShop 比 SDAR 高 7.0 个百分点。

## 证据质量与局限

【论文原文】覆盖三个 Agent 环境与两个模型规模，并公开代码，证据较强。局限是成功同伴 hindsight 仍依赖采样覆盖和状态可对齐性；实验环境有较强可验证终局，尚未证明开放式任务、异构 Judge 和真实工具副作用下成立。

## 最接近的相关工作

最接近 γOPD、BATON、RLDS、The Tasteful Agent 与 PACT；区别是显式估计两类信用的局部可靠性，而非固定加权或只做时间传播。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把环境回报视为硬方向，把 verifier 的 A/B/T 或序数分布视为 hindsight 幅度；当两者冲突时保留分布并降低蒸馏强度，而不是用软 Judge 覆盖环境真值。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：以逐状态可靠性仲裁硬 outcome 与软 score。\n- **A/B/T 与序数分布**：局部冲突时提高 T/不确定质量。\n- **真值门控**：终局环境回报保留不可覆盖的 episode-level 贡献。\n- **Critique states**：只从成功同伴提取可在共享状态验证的 critique。\n- **探索**：两信号冲突或精度低时保留多分支。\n- **Sealed eval**：仲裁器的精度估计不得使用最终评测轨迹。
