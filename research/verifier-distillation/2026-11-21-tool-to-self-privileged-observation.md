# Tool-to-Self: Internalizing Visual Tool Capabilities via Scaffolded Reinforcement Learning

- **作者**：Jin Cui, Hao Dong, Xinyue Long, Boran Zhao, Pengju Ren
- **首次公开日期**：2026-11-21
- **版本日期**：2026-11-21（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.28564
- **DOI**：https://doi.org/10.48550/arXiv.2611.28564
- **代码**：未见作者在 arXiv 摘要页给出独立代码链接

## 一句话结论

把真实工具观察作为 privileged on-policy teacher，再逐工具退火工具调用，可把外部视觉工具能力内化到 student，并在无工具推理时保留收益。

## 真正新增的内容

**论文原文结论**：T2S 先从 tool-repairable 样本冷启动工具使用与观察预测，再在 RL 中按工具逐步 anneal 执行，并联合答案正确性、观察一致性和 privileged on-policy self-distillation。  
**分析推断**：它是“程序/环境真值门控 teacher 信号”到 student-generated internal state 的直接原型。

## 核心方法

实际工具输出只在训练期作为 privileged observation；student 学习复现观察并据其推理。随着能力提升，逐工具降低真实调用比例，使策略迁移到 tool-free inference。

## 关键实验结果

跨多种视觉感知和推理 benchmark，持续优于显式工具使用与隐式 zooming 基线，并降低无工具推理延迟；摘要未给统一数值效应量。

## 证据质量与局限

有多 benchmark 与明确的工具退火机制，但摘要未给统计区间；领域限于视觉工具，student 预测的观察可能在 OOD 状态产生自洽幻觉。

## 最接近的相关工作

最接近 Grounding Agent Memory 的环境探针门控、OPD-Aha 的真实视觉证据差分、CoVer 的 ground-truth 测试锚定，以及 RSIAgent 的验证后记忆写入。

## 如何复用或推进 LLM-as-a-Verifier

把执行器、数据库查询或模拟器结果作为 privileged teacher observation，训练 student verifier 预测 `P(outcome | state, action)` 与 critique；随校准改善退火 oracle 调用，但持续抽样现实结算以估计漂移。

## 对 Agent verifier × OPD 实验路线的具体影响

可直接实现“工具真值 → critique state”的 OPD：先只接受与工具观察一致的 student critique，再蒸馏 ordinal score distribution。高熵分叉与低置信状态保持较高 oracle 调用率，不能统一退火；sealed eval 中重新启用真实工具，禁止使用 student 预测观察作为裁判。