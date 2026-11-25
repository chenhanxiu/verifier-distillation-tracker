# Branch and Consolidate：多 Teacher 在线策略蒸馏的统一配方

- **论文标题**：Branch and Consolidate: A Unified Recipe for Multi-Teacher On-Policy Distillation
- **作者**：Zihan Liang, Zikun Qu, Ben Chen, Fan Yang, Wenwu Ou, Min Zhang, Zhongxiang Dai, Xinchao Wang
- **首次公开日期**：2026-11-24
- **版本日期**：2026-11-24（v1）
- **原始论文**：https://arxiv.org/abs/2611.32515
- **DOI**：https://doi.org/10.48550/arXiv.2611.32515
- **代码链接**：论文注明将公开，当前未见可用仓库

## 一句话结论

当多个 specialist teacher 已远离共同初始化时，MOPD 不能只做简单平均；初始化、数据选择、监督平衡、能力保持和定向 refinement 必须联合设计。

## 真正新增的内容

**论文原文结论**：作者给出覆盖多 teacher 合并全流程的统一 recipe，解决 specialist 分支漂移、教师强弱不均与能力遗忘。**分析推断**：对 verifier distillation 而言，多 Judge/多 oracle 也应“分支后再整合”，保留各自可靠域和分歧，而不是把 logits 或总分无条件平均。

## 核心方法

从共同或经选择的 student 初始化出发，按领域/能力选择数据并平衡 teacher 监督；训练中加入能力保持机制，避免合并时覆盖通用能力；在 consolidation 后再对薄弱领域定向 refinement，使同一 student 吸收多个已分化 specialist。

## 关键实验结果

**论文报告**：工业设置中合并 6 个 specialist，恢复其平均增益的 97.0%，对比 IM-MOPD 的 79.8%；开放设置中用 Qwen3-4B 合并 5 个领域，consolidation 为 95.7%，refinement 后为 97.5%，高于 IM-MOPD 的 94.1%。

## 证据质量与局限

同时覆盖工业和开放模型、多个 specialist，数值差距具有实用意义。局限是“恢复增益”依赖作者定义的归一化指标；尚未专门研究 verifier、序数奖励分布或 evaluator 共适应。代码未公开时，数据配比和 refinement 细节难以独立复核。

## 最接近的相关工作

与 VG-OPD 的 verifier-gated multi-expert、CompassOPD 的跨模型族位移、Lightning Weave 的 specialist 能力组合、KMed MOPD² 的中位 teacher 选择，以及 RetireOPD 的 teacher 退出机制最接近。

## 如何复用或推进 LLM-as-a-Verifier

将不同 Judge、程序 oracle、规则检查器视为 specialist teachers；为每个样本保存 teacher 身份、可靠域和完整序数分布。只在经 sealed calibration 证明可靠的域内蒸馏其分数，冲突样本进入 A/B/T 分歧池，而非用均值掩盖。

## 对现有 Agent verifier × OPD 实验路线的具体影响

**分析建议**：构建“分支 verifier → 可靠性校准 → score-level consolidation → 薄弱域 refinement”流水线；程序/环境真值作为锚点 teacher，不被多数 LLM Judge 覆盖。高熵状态按 teacher 分歧与环境可恢复性分配分叉预算。最终用未参与合并的 Judge、隐藏环境和新 harness 做 sealed eval，检查多 teacher consolidation 是否只是共同偏差压缩。
