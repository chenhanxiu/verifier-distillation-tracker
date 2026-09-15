# Who Teaches Which Token? Verifier-Gated Multi-Expert On-Policy Distillation for Scientific Reasoning

## 基本信息

- **简称**：VG-OPD
- **作者**：Xun Xu；Zaixi Zhang
- **首次公开日期**：2026-09-14
- **版本日期**：2026-09-14（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2609.15404
- **代码**：未发现公开代码链接

## 一句话结论

【论文原文】VG-OPD 不再让所有 teacher 在所有 token 上平均施教，而是先由 verifier 判断“哪个专家对哪个评价维度确有反事实增益”，再把这种许可、teacher–student 分歧和维度重要性组合成 token 级蒸馏优势。

## 真正新增的内容

【论文原文】论文把多专家 OPD 拆成三个此前常被混合的问题：专家是否值得信任、监督应落在哪些 token、该评价维度对当前样本有多重要。其核心新意是 verifier-gated expert licensing：只有去掉某专家后会降低对应维度得分时，该专家才获得监督许可；随后以 teacher–student token 分歧定位监督，以维度权重控制强度。

【分析推断】这比“选一个总分最高 teacher”更接近 score-level on-policy verifier distillation：verifier 不直接替代策略梯度，而是决定蒸馏方向和支持域。

## 核心方法

1. 在 student 的 on-policy 输出上计算各科学推理维度的 verifier 分数。
2. 对每个专家做反事实消融，估计其对相应维度的边际增益，据此生成专家许可门。
3. 以 teacher–student token 分布差异定位需要教学的 token。
4. 将许可、分歧和维度重要性相乘，形成 token-level gated KL，并作为额外优势项并入 GRPO。

## 关键实验结果

【论文原文】在 7 个科学推理基准上，4B 与 8B 设置均取得最佳总体结果，并分别在 5 个基准上排名第一。消融显示，把同样的监督预算放错位置造成的损害最大；不加选择地蒸馏会把 RL 表现拖到其原有下限以下。

【证据边界】目前主要证据来自科学推理和论文选定的专家/评价维度；摘要未证明该门控在长时程工具 Agent、非平稳环境或弱 verifier 下同样成立。

## 证据质量与局限

- **质量**：多模型规模、7 个基准及针对监督位置的消融，使“选择谁、教哪里”具有较直接的实证支持。
- **局限**：没有公开代码；反事实许可仍依赖 verifier 的可识别性与校准。若 verifier 与训练策略共适应，许可门可能稳定地放大系统性偏差。
- **未被证明**：论文没有证明 verifier 的分数分布是校准概率，也没有验证 sealed evaluator 下的长期泛化。

## 最接近的相关工作

最接近的是多 teacher OPD、Uncertainty-Calibrated MOPD、Unified Per-Token OPD Gating、JudgeStealer，以及用硬奖励筛选 teacher 信号的 OPDVR/RA-OPD。VG-OPD 的差异在于把 verifier 的反事实维度增益直接用于专家许可，而非仅依赖 entropy、总分或 teacher–student gap。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把单一标量 verifier 改为“完成度、事实性、工具安全、可恢复性”等序数分布头；只有某专家使对应头的期望分数上升且置信区间不跨零时才许可。pairwise A/B/T 可由同一 state 下“启用/移除专家”的反事实分支产生，Tie 用于保留无法可靠区分的探索分支。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：优先实现“硬真值决定许可符号、序数分布决定权重”的门控，而不是全量 KL。
- **A/B/T 与序数分布**：对每个高熵 state 比较专家分支与原 student 分支；将不显著差异标为 Tie。
- **程序/环境真值**：副作用、任务终态和约束违反应拥有不可覆盖的 veto；LLM verifier 只细化软维度。
- **critique states**：只有能通过反事实重放提升相应维度的 student-generated critique 才进入蒸馏。
- **探索**：在 verifier 许可不确定或多个专家均有效时保留多分支，不强制坍缩到单专家。
- **sealed eval**：训练许可 verifier 与最终 evaluator 必须模型、提示、数据切片和版本隔离，并报告优化压力下的许可准确率。