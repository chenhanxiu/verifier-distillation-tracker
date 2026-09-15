# Lightning Weave: Improving the Accuracy-Efficiency Frontier of Reasoning Models through Capability Composition

## 基本信息

- **作者**：Yecheng Wu；Song Han；Han Cai
- **首次公开日期**：2026-09-13
- **版本日期**：2026-09-13（arXiv v1）
- **状态**：work in progress
- **原始论文**：https://arxiv.org/abs/2609.14708
- **代码**：论文称将于后续公开，当前未发现可用链接

## 一句话结论

【论文原文】Lightning Weave 把 specialist 从预训练到后训练的 log-ratio 位移视为可组合能力，在 student 自己访问的 token state 上对齐这些位移，并用稳定目标和缓存 anchor 轨迹实现多能力 OPD。

## 真正新增的内容

【论文原文】论文不是直接混合多个 teacher 的绝对分布，而是提取各 specialist 相对其起点的能力位移；在 student token states 上进行能力对齐，再以 Tilted-Target DOPD 稳定组合目标。anchor pairs 允许轨迹只评分一次并缓存，降低反复 verifier 调用。

【分析推断】这种“迁移相对能力位移而非绝对偏好”的思路与 CompassOPD 接近，但更强调多能力合成及准确率—推理成本前沿。

## 核心方法

1. 用 specialist 后训练策略与其基线策略的 log-ratio 表示能力位移。
2. 将多项能力位移映射并组合到 student 的 on-policy token states。
3. 通过 Tilted-Target DOPD 构造稳定的蒸馏目标。
4. 用 anchor pairs 对轨迹评分并缓存，避免训练中重复评价。
5. 在准确率和生成 token 成本上共同优化组合结果。

## 关键实验结果

【论文原文】Qwen3.5-4B 在 HMMT 上从 59.2 提升到 64.0，同时生成 token 减少 10.7%；LiveCodeBench v5 从 41.7 提升到 54.2，同时生成 token 减少 9.6%。

【证据边界】论文仍标记为 work in progress，代码尚未公开；摘要结果集中在推理/代码任务，尚无长时程工具 Agent 或 evaluator 压力测试。

## 证据质量与局限

- **质量**：同时报告能力提升和推理成本下降，且方法对多 specialist 组合具有清晰机制解释。
- **局限**：能力 log-ratio 是否可跨模型族、词表和任务稳定迁移仍需更多消融；缓存评分会在策略分布变化后变陈旧。
- **风险**：若 anchor verifier 有偏，缓存会长期固化偏差；多能力相加也可能掩盖冲突约束。

## 最接近的相关工作

CompassOPD 的跨族能力位移、RouteOPD 的概率运输、Open-MOPD/Uncertainty-Calibrated MOPD 的多 teacher 组合，以及 OPRD 的 teacher 位移方向约束。Lightning Weave 更关注能力位移的可组合性和成本前沿。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】把 verifier 的后训练位移也建模为相对 score shift：从通用 Judge 到领域 Judge 的序数 log-odds 变化，而不是直接蒸馏领域 Judge 的绝对分数。anchor pair 应包含环境真值和 Judge 证据，缓存时记录模型/提示/环境版本。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- score-level OPD 可组合“安全、完成度、效率”三个 verifier 位移，但硬约束冲突时禁止线性抵消。
- anchor pair 可直接作为 A/B/T 数据；序数分布比单一差值更能表达能力冲突。
- 环境 oracle 决定成功与副作用的符号，领域 verifier 位移只调节软幅度。
- student critique state 可作为新能力通道，但只有在下游重放收益为正时合入。
- 高熵分叉保留多个非支配能力组合，而非只选加权总分最高者。
- sealed eval 必须禁用训练缓存并使用新 anchor、冻结 evaluator 与独立成本计量。