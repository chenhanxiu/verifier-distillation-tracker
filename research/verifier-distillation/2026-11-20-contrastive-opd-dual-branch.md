# Contrastive On-Policy Distillation via Dual-Branch Supervision

- **作者**：Zhibo Hou, Fan Zhao, Yiping Li, Zhiyu An, Wan Du
- **首次公开日期**：2026-11-20
- **版本日期**：2026-11-20（arXiv v1）
- **原始论文**：https://arxiv.org/abs/2611.28359
- **DOI**：https://doi.org/10.48550/arXiv.2611.28359
- **代码**：未见作者在 arXiv 摘要页给出独立代码链接

## 一句话结论

弱 teacher 不只是不够好的 teacher；把强 teacher、弱 teacher 与 student 在 student-generated prefix 上做三方对比，可形成方向性 token 监督，并在提高数学 Pass@16 的同时抑制坏模式、保留探索。

## 真正新增的内容

**论文原文结论**：提出 cOPD，用 dual-branch supervision 对比 strong teacher、weak teacher 和 student；受控 token intervention 显示，能力弱于 student 的模型仍可充当有信息量的反例参考。  
**分析推断**：这比单 teacher score-level OPD 更接近 A/B/T：强分支提供 A，弱分支提供 B，三方差异小或相互矛盾时可显式映射为 T/不确定，而不是强迫单点标签。

## 核心方法

在 student 自生成前缀上同时查询强、弱 teacher，利用三方预测差异挑选与好/坏推理结果相关的 token；理论分析在理想化模型下解释这种对比如何产生方向性监督。实验覆盖不同训练阶段、规模和模型族。

## 关键实验结果

在数学推理、指令遵循和带 abstention 的问答上均达到最佳或第一梯队；数学推理总体 Pass@16 相对最强基线最高提升 7.51%。附加分析显示坏响应模式被压制，并提示探索能力改善。

## 证据质量与局限

优点是 teacher–student 配置多样，且包含 token intervention 与跨任务实验。局限是“促进探索”主要来自行为分析，尚未在长时程 Agent 环境用真实分叉成功率、恢复性或 sealed endpoint 证明；强弱 teacher 的错误相关性也未被完全消除。

## 最接近的相关工作

最接近 VG-OPD 的多专家门控、CompassOPD 的跨模型族位移、IWD 的 teacher 可靠性加权，以及对比式自蒸馏的正负 privileged teacher log-ratio。

## 如何复用或推进 LLM-as-a-Verifier

把 verifier 输出从单分数扩展为 `(strong, weak, student)` 三元组，蒸馏 score difference、pairwise A/B/T 与序数分布；仅当强弱 teacher 的方向与程序/环境真值一致时更新，冲突样本保留为 T 并送入高熵分叉复核。

## 对 Agent verifier × OPD 实验路线的具体影响

优先新增“强 verifier − 弱 verifier”的对比分支：在 student-generated critique state 上计算三方差异，差异大且有 oracle 支持时做 score-level OPD；差异小或方向冲突时保留探索，不做硬收缩。独立 sealed eval 必须使用未参与三方训练的 verifier/环境，以检测三者共同偏差。