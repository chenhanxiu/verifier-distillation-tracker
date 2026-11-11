# Dependable Long-Horizon LLM Agents: A Trajectory-Centered Empirical Study of Where Errors Enter and Which Controls Reach Them

- **作者**：Shaohuang Wang、Jinghao Wen、Xulei Zhang、Xun Jiao
- **首次公开日期**：2026-11-11
- **版本日期**：2026-11-11（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.13254
- **代码/数据**：论文称包含 protocol、records 与 scripts；未找到可独立核验的公开仓库地址
- **标识符**：arXiv:2611.13254

## 一句话结论

【论文原文】长时程 Agent 失败常在很早进入轨迹，且轨迹本身往往已经包含反证，却没有任何 Agent 或控制器采取行动；只标“最后一步/责任 Agent”会错过真正可干预的状态。

## 真正新增的内容

【论文原文】作者提出 episode record，把错误起源、传播、检测、响应和后果映射到操作阶段与状态域，并进一步标注哪些控制拥有足够 observation 与 reach。它从症状分类转向“哪个控制能在何处真正移除错误状态”。

## 核心方法

- 制定 38 字段的失败轨迹标注协议。
- 全量阅读 Who&When 与 MAD 语料中的 95 条失败轨迹，覆盖六个多 Agent 系统。
- 区分错误首次进入、被标为 decisive 的步骤、已有反证、偏差告警、是否实际清除状态。
- 将独立 Judge、准入时任务契约、环境复核、状态恢复等控制映射到可覆盖的错误。

## 关键实验结果

【论文原文】错误进入位置中位数为轨迹进度 **0.18**；在 Who&When 的 88 条轨迹中有 **37 条**早于原人类标签的 decisive step。**72%** 的失败轨迹在失败前已含反证，其中 **88%** 没有 Agent 采取行动；**31%** 曾出现偏差告警，但没有响应清除错误状态。恢复 Agent 自身状态只足以修复 **35/95** 条。另有 **45%** 的手工 Who&When 失败以 provider content-filter crash 结束，随后 harness 输出了并非任何 Agent 产生的最终答案。

## 证据质量与局限

【论文原文】逐轨迹完整阅读与控制可达性分析提供了丰富诊断证据。但关键比例依赖单个自动 annotator 按协议标注，未报告人工 inter-annotator agreement；只分析失败轨迹，不能估计各控制的总体误报率或因果收益。

## 最接近的相关工作

最接近 Continual Search for Long-Horizon RCA、ReplayRCA、Knowing When to Intervene、BATON 与 Harness or Model?。本文突出“反证已存在但无人响应”和 harness 自身制造失败标签。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】generative verifier 应输出结构化五元组：错误起源、受污染状态、反证证据、可执行修复和未清义务；score student 再蒸馏每项的序数置信，而不是只学终局失败概率。若 verifier 仅 flag 却不能移除状态，应单独评价 response reach。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：按错误起源状态回传信用，而不是把分数压到最后一步。
- **A/B/T 与序数分布**：证据充分但无响应、已告警但未清除等状态应为不同序数类别。
- **程序化/环境真值**：准入契约与环境复核作为高优先级控制。
- **student-generated critique states**：只有包含反证指针和可执行清除动作的 critique 才准入。
- **高熵分叉**：在最早错误进入点分叉，而非症状出现后才重采样。
- **sealed eval**：把 harness crash、provider filter 和模型行为分账，禁止由 harness 伪造最终答案。