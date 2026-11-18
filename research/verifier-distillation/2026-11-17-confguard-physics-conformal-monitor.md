# ConfGuard: a physics-grounded reference monitor for predictive-maintenance large-language-model agents

- **作者**：Arunkumar V、Gangadharan G. R.、S. Senthilkumar
- **首次公开日期**：2026-11-17
- **版本日期**：2026-11-17（v1）
- **原始论文**：https://arxiv.org/abs/2611.22288
- **代码链接**：未发现公开代码
- **标识符**：arXiv:2611.22288；DOI: 10.48550/arXiv.2611.22288

## 一句话结论

【论文原文】把轨迹级 conformal monitor、退化物理约束和确定性策略 validator 放在 LLM Agent 外部，可同时抑制文本注入与传感器攻击，并给出可控的清洁轨迹升级率。

## 真正新增的内容

【论文原文】ConfGuard 不只检查数据来源或工具权限，而验证预测量是否符合资产历史和退化物理：剩余寿命上限不应上升、每周期下降幅度受限；再用相同区间驱动确定性维护紧急度策略，形成独立 reference monitor。

## 核心方法

1. 对整条资产轨迹校准 conformal threshold，而非把 window 当独立样本。
2. 物理投影检查 capped remaining life 的单调性与步长约束。
3. policy validator 比较 Agent 决策与由预测区间导出的确定性策略。
4. 评估文档 prompt injection、通用 sensor attack 与 adaptive attacker。

## 关键实验结果

【论文原文】在 10,196 个 C-MAPSS test windows 上，健康资产 covert attack reach 从 0.529 降到 0.046，故障资产 suppression 从 0.151 降到 0；clean escalation 0.027，目标 0.05。接在 Qwen3-14B planner 后，紧急度注入成功率为 0，sensor attack 为 0.12，而 defended prompt 为 0.29/0.54。自适应攻击可击败 Mahalanobis detector（0.504）和 adversarial training（0.485）。

## 证据质量与局限

【论文原文】覆盖组合攻击、适应性攻击和清洁误报，且校准单位与时间依赖一致；但领域与物理规律高度特定，预测区间及 deterministic policy 本身可能错。论文也报告物理投影未覆盖的一类攻击，不能视为完整安全证明。

## 最接近的相关工作

接近 conformal risk control、runtime assurance/reference monitor、physics-informed anomaly detection、Agent guardrail 与 ContrAgent/MAGS 的外部硬门控。差异是将轨迹物理规律与 Agent 决策策略联结。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】在长时程 Agent 中把不可学习的单调性、预算、权限与时间义务写成外部 monitor；LLM verifier 只解释 violation、预测软风险与路由补证。可将 conformal p-value/区间蒸馏给 student，但最终 release gate 保持独立。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：软 verifier score 之外增加 conformal/physics channel，分别蒸馏并保留硬门优先级。
- **pairwise A/B/T 与序数分布**：任一分支触发不可覆盖物理冲突即判劣；两者均在区间内时保留概率排序或 T。
- **程序化/环境真值门控**：reference monitor 作为不可由 LLM teacher 覆盖的 release gate，并按完整轨迹校准。
- **student-generated critique states**：critique 必须指向具体物理/策略 violation，修复后重新跑 monitor。
- **高熵分叉探索**：在 conformal boundary 附近保留分叉，同时专门生成 adaptive attack 轨迹，避免只训练平均样本。
- **sealed eval**：隐藏攻击族、资产轨迹与物理参数；监控器与被训练 Agent/LLM Judge 独立版本化。
