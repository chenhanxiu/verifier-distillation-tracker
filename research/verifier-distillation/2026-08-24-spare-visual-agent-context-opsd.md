# Buried in Textual Debt: Context Pruning with Visual Evidence Preservation for MLLM Agents

## 基本信息

- 作者：Yuchen Huang、Sijia Li、Jun Zhang、Yi R. Fung
- 首次公开日期：2026-08-24
- 版本日期：2026-08-24（v1）
- arXiv：2608.22963
- 原始论文：https://arxiv.org/abs/2608.22963
- DOI：https://doi.org/10.48550/arXiv.2608.22963
- 代码：论文公开页未提供

## 一句话结论

SPARE 用特权任务状态摘要和同模型 replay 的 reverse-KL 判断哪些历史推理可安全删除，在多步视觉工具 Agent 中删除 37.89%–64.58% 推理 token 的同时保持最佳平均准确率。

## 真正新增的内容

**论文原文结论：** 将 on-policy self-distillation 的分布差异用作上下文覆盖度测试：若摘要条件下的未来分布未被显著扰动，则对应历史文本可被裁剪。

**分析推断：** 这是“student-generated state + privileged teacher context”在长轨迹压缩中的直接实例；其 KL 信号也可以迁移为 verifier 蒸馏的状态充分性评分。

## 核心方法

先生成紧凑任务状态摘要作为 privileged diagnostic context；对每个候选历史片段，用同一模型分别在原上下文和摘要上下文重放，计算 reverse-KL；根据分布扰动决定是否裁剪，并用 SFT 进一步训练摘要器。

## 关键实验结果

在多步视觉工具使用 benchmark 上，SPARE 在上下文裁剪方法中取得最高平均准确率，同时删除 37.89%–64.58% 的 reasoning tokens；论文归因于减少自生成文本的过度条件化并恢复对视觉证据的依赖。

## 证据质量与局限

证据质量中等：有多 benchmark 与明确效率—准确率结果，但公开摘要未列出逐数据集效应、统计显著性或跨模型泛化。reverse-KL 只衡量模型分布变化，不等同于环境真值；原模型若共同犯错，会把错误摘要判为充分。

## 最接近的相关工作

最接近 Latent OPSD、SMOPD 的 dirty history 处理、SimpleOPD 的长上下文对齐，以及 privileged-context distillation。区别是把 OPSD 当作裁剪诊断器而非单纯能力迁移目标。

## 如何复用或推进 LLM-as-a-Verifier

可训练一个“状态充分性 verifier”，输入原轨迹、摘要和后续候选分布，输出保留/删除概率及不确定性；再用环境回放校准 KL 阈值，避免模型自洽替代真实正确。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD：** 将原上下文—摘要上下文的分布差异蒸馏成低成本状态充分性分数。
- **A/B/T：** 比较保留原片段、摘要替换、删除片段三种续跑，形成天然 A/B/T。
- **真值门控：** 只有终态成功或程序化检查不下降时，KL 一致才可作为正 teacher 信号。
- **Student critique states：** 摘要与 critique 可共用结构，但需分别建模事实状态和错误解释。
- **高熵探索：** 对高 KL/高熵片段默认保留，避免删除尚未解决的分叉证据。
- **Sealed eval：** 用独立未参与摘要器训练的视觉任务评估，防止摘要器与 verifier 形成自洽闭环。
