# LastOPD: Taming Collapse in Latent On-Policy Distillation

## 基本信息

- **作者**：Jie Yang、Zhengyu Fang、Zelin Xu、Jiarui Sun、Xiran Fan、Junpeng Wang、Liang Wang、Qinghua Liu、Yiwei Cai、Yan Zheng
- **首次公开日期**：2026-09-23
- **版本日期**：2026-09-23（v1）
- **原始论文**：https://arxiv.org/abs/2609.28845
- **DOI**：https://doi.org/10.48550/arXiv.2609.28845
- **代码**：https://github.com/Muyiiiii/LastOPD （论文声称公开；本次检查时链接尚不可访问）

## 一句话结论

跨层 latent alignment 可以在对齐指标持续变好时让行为崩溃；LastOPD 只短暂对齐最后层并渐变回 token OPD，说明“表示更像 teacher”不能替代行为与环境验收。

## 真正新增的内容

【论文原文】在 Qwen3-4B/8B → Qwen3-1.7B-Base 的 latent OPD 中发现“早期提升、后期坍缩”和“对齐更好、行为更差”；提出只对齐双方 LM head 共同读取的最后层，并在 10 步内 crossfade 到 token-level OPD。

【分析推断】真正重要的负结果是 alignment metric 与任务效用反向变化，这直接要求 verifier 蒸馏把表征损失视为辅助项，而非停止条件或成功证据。

## 核心方法

【论文原文】避免按深度配对异构模型层，只对齐最后层状态；latent signal 仅用于最初 10 步，并逐步移交给 token-level OPD，防止 student 被拉向其无法解释的 teacher 内部状态。

## 关键实验结果

【论文原文】latent-only 在 10 步把 MATH-500 从 25 提到 46，随后跌至 11；LastOPD 相对 token-only OPD 在 4B/8B teacher 下分别提高 5.55/4.02 点，在多数 held-out 数据集领先，并约用一半步数达到 token-only 最终分数。

## 证据质量与局限

包含明确崩溃曲线、双 teacher 和 held-out 结果，证据较强；但只覆盖同一模型家族与数学推理，小 student 的失败未必外推到 Agent 工具轨迹。代码仓库当前不可访问，细节与复现仍待核验。

## 最接近的相关工作

最接近 OPRD、SCOPE-OPSD 和传统 token-level OPD。与 SCOPE-OPSD 的“特权子空间”相比，LastOPD 更保守：限制层位与持续时间，并最终回到行为分布监督。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可短暂对齐 teacher verifier 的最后层 score representation，但必须同时监控环境真值、校准误差和 A/B/T 分布；若 latent loss 下降而 sealed utility 下降，应立即停止该通道。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】

- 新增 latent-only、token-only、last-layer crossfade 三组基线。
- 以程序/环境真值而非 representation similarity 选择 checkpoint。
- critique state 的 latent 蒸馏限于短 warm-up，之后由可解释 score/critique 接管。
- 高熵状态不能因 latent 对齐而被强制收窄；保留 teacher–student 分歧。
- sealed eval 独立冻结，专门检测“对齐更好但行为更差”的指标替代失效。