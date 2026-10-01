# Agent Error Dataset: Scaling 50,000 Error–Diagnosis Pairs for Failure Analysis and Error-Aware Post-Training

- **作者**：Kunlun Zhu, Xuyan Ye, Yibo Li, Cheng Qian, Beibin Li, Heng Ji
- **首次公开日期**：2026-09-30
- **版本日期**：2026-09-30（v1）
- **原始论文**：https://arxiv.org/abs/2609.40111
- **代码/数据**：未发现公开链接

## 一句话结论

AED 将失败轨迹转为 50,228 组带证据诊断，并通过同 checkpoint 匹配重放验证修正；首个修正的 verifier 通过率从 18.4% 升到 51.1%。

## 真正新增的内容

【论文原文】数据覆盖 9,961 个任务、33 个环境、19 个 harness family 和 23 个 policy model，保留原始 trace 与执行元数据。AET 流水线分别构造诊断训练视图与 actor recovery 视图，并在可重放环境中比较修正动作和原动作重试。

【分析推断】这是 student-generated critique state 的大规模“证据—修正—重放”模板，比只让 LLM 解释失败更接近可验证因果归因。

## 核心方法

收集自然失败，生成诊断和候选修正，对照记录证据；支持时从同一 checkpoint 做 matched replay，再分离训练 diagnosis model 与 recovery actor。

## 关键实验结果

【论文原文】3,062 个 matched replay pair 中，first-proposal correction 的 verifier pass rate 从 18.4% 到 51.1%。冻结诊断发布上，1,656 个源任务微调使 Qwen3-8B 在 943-case holdout 的 exact-step teacher agreement 从 47.2% 到 63.6%（三种子），强提示基线为 54.7%。WebShop-lite 单种子中 action-only repair 比 success-only 高 6.67 点。

## 证据质量与局限

覆盖面和 matched replay 强，但部分关键指标仍是 teacher agreement 或 verifier pass，而非独立人类/环境真值；actor 对照有单种子限制。

## 最接近的相关工作

DENSE、PaperDoctor、SkillAA、FLARE、LLM-as-an-Improver。

## 如何复用或推进 LLM-as-a-Verifier

采用其双视图数据结构：诊断 verifier 学“错在哪里”，actor 学“怎么恢复”；每条 critique 附 checkpoint、证据指针和重放 outcome。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- **score-level OPD**：以 matched replay 的 outcome delta 作为 critique/修正权重。
- **A/B/T 与序数分布**：原动作与修正动作构成 A/B；不可重放或差异不显著为 T。
- **硬真值门控**：优先使用环境重放，不把 teacher agreement 当最终真值。
- **student-generated critique states**：直接提供准入流水线，失败 critique 不自动入库。
- **高熵分叉**：同 checkpoint 测多个修正，保留多条成功恢复。
- **sealed eval**：冻结诊断发布、policy family 和环境划分，防止数据回流污染。
