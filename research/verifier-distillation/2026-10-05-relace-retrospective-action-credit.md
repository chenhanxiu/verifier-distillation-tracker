# RELACE: retrospective likelihood-based action credit estimation for long-horizon language agents

- 作者：Sayak Chakrabarti、Sathish Reddy Indurthi
- 首次公开日期：2026-10-05
- 版本日期：2026-10-05（v1）
- 原始论文：https://arxiv.org/abs/2610.07349
- Canonical URL：https://arxiv.org/abs/2610.07349
- 代码：https://github.com/sayaksc/RELACE

## 一句话结论

【论文原文】RELACE 用结果可见前后同一已执行动作的 teacher-forced likelihood 变化构造回顾因子，再结合真实任务回报做同状态局部比较，无需额外 critic、reward model 或生成 rollout 即可细化长轨迹信用。

## 真正新增的内容

【论文原文】它区分“看到结局后动作变得更像什么”与单纯 hindsight plausibility：回顾似然差必须和实际 reward 相乘，并在等价状态动作间形成局部 advantage；另以时间平滑和成功保护 mask 稳定训练。

## 核心方法

【论文原文】分别在原始上下文和追加 outcome 的上下文中 teacher-force 评分已执行动作；差值形成轨迹归一化回顾因子，重加权折扣回报，再对同任务等价状态下的动作比较构造局部优势。

## 关键实验结果

【论文原文】Qwen2.5-1.5B-Instruct 在 ALFWorld 达 96.35%、WebShop 达 79.43%，分别比 GiGPO 高 5.47 与 5.60 个百分点；1.5B 和 7B 实验均优于 GRPO、GiGPO、HCAPO。

## 证据质量与局限

【论文原文】覆盖两个交互环境、两个模型规模和多个强基线，且不引入额外生成成本。【分析推断】似然变化仍是模型内生信号，可能把 outcome 泄漏后的合理化当因果信用；“等价状态”定义及环境扩展性需要进一步验证。

## 最接近的相关工作

【分析推断】最接近 BATON、RLDS、RECAP、DRACO 与 GiGPO/HCAPO；本文用 outcome-conditioned likelihood 而非显式 critic 定位动作信用。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】可把 terminal 环境结算追加给 verifier，比较动作或 critique 在结算前后的序数分布变化；但方向必须由真实 reward 锚定，似然差只用于幅度和定位。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：用 outcome 前后 score shift 分配逐步蒸馏权重。
- 【分析推断】A/B/T：同状态动作按结算加权形成 A/B；差异小或状态不等价则 T。
- 【分析推断】真值门控：任务回报决定正负，回顾似然不得翻转硬真值。
- 【分析推断】critique states：比较 critique 在未知/已知结局下的稳定性，过滤事后合理化。
- 【分析推断】高熵分叉：在高回顾差异且等价状态处追加分叉，保留多个成功动作。
- 【分析推断】sealed eval：隐藏结局生成规则，独立测试对伪相关 outcome 的敏感性。