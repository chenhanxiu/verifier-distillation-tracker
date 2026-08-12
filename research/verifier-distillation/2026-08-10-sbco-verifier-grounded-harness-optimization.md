# SBCO：面向规划 Agent 的 Self-Supervised Verifier-Grounded Harness Optimization

## 基本信息

- **论文标题**：SBCO: Self-Supervised, Verifier-Grounded Harness Optimization For Planning Agents
- **作者**：Vivek Kulkarni, Sudipta Paul, Aounon Kumar, Nicholas Tzou, Srinivas Chappidi
- **首次公开日期**：2026-08-10
- **当前版本日期**：2026-08-10（v1）
- **arXiv ID**：2608.10157
- **原始论文**：https://arxiv.org/abs/2608.10157
- **代码**：截至记录时未发现公开代码仓库

## 一句话结论

SBCO 将复杂规划约束拆成可学习的 verifier bank，并交替优化 verifier 与检查—修复 harness；它以较低计算量达到自修改基线水平，但没有独立 held-out test，证据存在明显 evaluator 共适应风险。

## 真正新增的内容

**论文原文结论：** 对不适合自改代码的规划任务，SBCO 用固定 meta-agent 进行近似 block coordinate ascent：逐约束学习 verifier signature/implementation，再学习在可靠 verifier 触发后检查和修复输出的 harness policy，无需人工标签。

**分析推断：** 其价值不在 OPD 本身，而在“把单一总分 evaluator 分解成约束 verifier bank，并对 verifier 设置 acceptance gate”。这可成为 generative verifier 蒸馏前的 teacher 构建层。

## 核心方法

1. 将任务要求分解为约束 (c)，每项学习一个 verifier 的函数签名与实现。
2. 从 baseline run 构造该约束的正负样本，以 precision/recall/F1 衡量 verifier。
3. 只有通过质量检查的 verifier 才进入 verifier set。
4. 固定 meta-agent 根据 graded feedback 交替改进 verifier bank 与 harness policy；policy 在 verifier 触发时执行程序化修复或重新规划。
5. 在 Travel Planning 与 Shopping 两个显式约束任务上比较 Huxley Gödel Machine 等自修改基线。

## 关键实验结果

**论文报告：**

- task agent 使用 GPT-5.4-mini，critic/strategist 使用 GPT-5.4-medium。
- customized HGM 在 Travel/Shopping 从 76/83 提高到 83/91，但使用 4,000 次 plan-generation budget。
- SBCO 在 4–5.5 倍更低预算下，Travel composite 84（HGM-C 83），Shopping 比 HGM-C 高 3 分，case accuracy 高 9 分。
- Shopping 总分从 0.828 提至 0.940；L1/L2 分别提高 0.096/0.154，L3 仅提高 0.045，因为未学到可靠的 coupon-stacking verifier。
- 所有数值仅为两次 policy run 的均值。

## 证据质量与局限

**论文明确局限：**

- 只评估两个具有显式可检查约束的规划域；验证接近求解难度时是否有效未知。
- 提升受 base LLM 能力限制；固定 meta-agent 不具开放式元认知自改能力。

**重要证据边界：**

- 最终性能在完整 task set（training + validation）上报告，没有独立 held-out test；作者称这与基线协议一致，但不足以排除 harness/verifier 对 benchmark 共适应。
- 仅两次运行，方差证据较弱。
- verifier 训练正负样本来自 baseline evaluations，不等同于外部 sealed truth。
- 论文优化的是 harness 而非 student 模型参数，不属于严格的 verifier distillation。

## 最接近的相关工作

Process reward/verifier feedback、plan–execute–verify–replan、自动 criterion/verifier induction、DGM/HGM、Trace2Skill。SBCO 的差异是联合学习分解 verifier bank 与 repair workflow。

## 如何复用或推进 LLM-as-a-Verifier

**分析建议：**

- 先把下一步动作贡献拆成硬约束、安全约束、进度增量、可恢复性等 verifier heads。
- 对程序可判的 heads 使用函数 verifier；开放语义 heads 使用 LLM teacher，并统一输出序数概率。
- 用 held-out failure cases 为每个 verifier 设置 precision/recall acceptance gate，再蒸馏到共享 student verifier。
- 让 generative verifier 输出具体违反的约束和修复建议，形成 student-generated critique states。

## 对 Agent verifier × OPD 实验路线的具体影响

- **Score-level OPD**：不要直接蒸馏一个 composite score；先蒸馏各约束的 score distribution，再做可审计聚合。
- **A/B/T**：按约束逐项比较两个动作；优势冲突或差异不足时保留 tie。
- **真值门控**：硬约束 verifier 优先使用程序化检查，并对 LLM verifier 设置 admission gate。
- **Critique states**：约束级失败原因可作为 teacher privileged critique。
- **高熵探索**：只修复已被高精度 verifier 证实的违规，避免低召回/低精度 head 过早剪枝。
- **Sealed eval**：必须修正本文最关键弱点——训练/验收 verifier 的样本与最终任务完全隔离，并冻结 evaluator。

SBCO 适合用来设计 verifier bank 和门控协议，但不能把其非独立评测结果视为 verifier 泛化证据。
