# 可复现 Eval 驱动的安全 Prompt 压缩

- **论文标题**：Reproducible Evaluation as the Substrate for Safe Prompt Compression in Production Agents
- **作者**：Prabal Vashisht、Zheng Hu、Ying Yang
- **首次公开日期**：2026-10-22
- **版本日期**：2026-10-22（v1）
- **原始论文**：https://arxiv.org/abs/2610.31972
- **DOI / canonical URL**：https://doi.org/10.48550/arXiv.2610.31972
- **代码**：未发现公开代码链接

## 一句话结论

该报告先把易漂移的生产后端冻结成可再生离线评测，再用 correctness gate 约束 GEPA prompt 优化，证明任何 evaluator 驱动的自改进都应先有可复现环境和不可突破的正确性门槛。

## 真正新增的内容

**论文原文结论**：构建可在 live enterprise data 变化后重新生成的离线 harness，并将其作为 GEPA prompt compression 的 fitness；优化只有通过 correctness gate 才能接受。

**分析推断**：虽然目标是 prompt 压缩而非 verifier distillation，但其“先冻结测量底座、再允许优化”的顺序正是防止 policy–evaluator 共适应所需的工程原则。

## 核心方法

1. 从生产会话与可变后端构造离线可复现快照。
2. 检测 benchmark 过期并按需再生，而非静默继续使用。
3. 用 GEPA 搜索更短 prompt。
4. correctness gate 阻止以牺牲任务正确性换取表面 fitness。
5. 在 held-out 任务上检验压缩候选。

## 关键实验结果

**论文原文结论**：在一个生产 merchant-facing Agent 上，三类独立 subject model 的完整 prompt surface 缩短 3.5%–7.6%，held-out task correctness 未下降；其中一个模型正确性显著提升。

## 证据质量与局限

来自生产系统且有三模型复现，但仅一个业务 Agent、8 页短报告、优化目标较窄；未公开代码和数据，外部难以复核。正确性 gate 的覆盖范围决定能否真正防 reward hacking，未证明对未建模行为安全。

## 最接近的相关工作

接近 AutoTuneBench、AuditKIT、Harness or Model、MC-EvoBench、VeriEvolve 与 ground-truth-as-code。区别是把可复现评测直接用作 prompt 优化约束。

## 如何复用或推进 LLM-as-a-Verifier

把环境快照、工具版本、用户模拟、evaluator 指纹和数据生成时间写入 eval artifact；任何 verifier/prompt/OPD 更新先过 frozen correctness gate，再进入可解释的软指标比较。

## 对 Agent verifier × OPD 实验路线的具体影响

**分析推断**：

- **score-level OPD**：软 score 只在硬正确率不退化的候选间排序。
- **A/B/T**：快照不一致或数据已过期时标 T，不产生偏好标签。
- **真值门控**：correctness gate 必须独立于训练 Judge。
- **critique states**：只允许可在冻结后端重放的 critique 进入训练。
- **探索保留**：压缩/蒸馏候选先在 sandbox 多分支试验，不直接替换主策略。
- **sealed eval**：冻结 held-out 快照和 evaluator；数据过期时整体再生并启用新版本，禁止混用分数。
