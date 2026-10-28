# GEPA-Curator：面向自改进 Agent 的经验筛选

- **论文标题**：GEPA-Curator: Curated Learning for Self Improving Agents
- **作者**：Zack Yu, Nicholas Lee, Minjae Lee, Lakshya Agarwal, Luca Manolache, Wonjun Kang, Matei Zaharia, Michael W. Mahoney, Kurt Keutzer, Sehoon Kim, Amir Gholami
- **首次公开日期**：2026-10-27
- **版本日期**：2026-10-27（v1）
- **原始论文**：https://arxiv.org/abs/2610.37651
- **代码链接**：未在论文首页给出独立实现；相关 GEPA 框架为 https://github.com/gepa-ai/gepa
- **标识**：arXiv:2610.37651；DOI: 10.48550/arXiv.2610.37651

## 一句话结论

失败 rollout 并不天然是好监督；先判断失败是否来自可学习的 prompt 缺陷，再让它进入反思优化，可比无差别吸收失败轨迹稳定得多。

## 真正新增的内容

**论文原文结论**：GEPA-Curator 在 GEPA 外加入任务筛选与历史成功轨迹检索，明确区分 prompt 弱点、harness 限制、随机执行和 noisy judge 导致的失败；在 GoBrowse、ALFWorld、AppWorld 与 τ-bench 上，平均表现不低于基线，最高相对 GEPA 提升 20.7%、相对 ACE 提升 21.2%。

**分析推断**：其核心价值不是新的 reward，而是“监督准入层”：在 critique 或 verifier 信号被蒸馏前，先估计该经验是否可归因、可复现、可学习。

## 核心方法

1. 任务筛选：过滤可能只提供噪声或不可学习失败的任务。
2. 历史成功检索：按当前任务选择相近成功轨迹，为反思器补充正向证据。
3. 由 Gemini 3.1 Pro 或 Claude Opus 5 作为优化器，在多轮 Agent 环境中更新 prompt。

## 关键实验结果

论文在四个多轮 Agent 基准上报告最高 20.7%（对 GEPA）和 21.2%（对 ACE）的增益；结论覆盖两种强闭源优化器。摘要未给出逐任务方差、筛选器误报/漏报和等预算消融，因此不能据此断言收益完全来自任务筛选。

## 证据质量与局限

证据优点是跨四个环境、两类优化器；局限是研究对象为 prompt 优化而非参数级 verifier distillation，且筛选器可能与同一 judge 共适应。论文没有证明被过滤经验在独立真值下确实无用。

## 最接近的相关工作

最接近 GEPA、ACE、GLARE 的 on-policy 失败样本更新，以及 SkillAA/RSIAgent 一类先验证再写入经验的工作。不同点在于本文把“是否让一次失败参与优化”作为一等决策。

## 如何复用或推进 LLM-as-a-Verifier

把 curator 改成三路输出：可学习失败、不可归因失败、证据不足（T）。只有第一类进入 generative critique；第二类送 harness/环境诊断；第三类触发重放或强 verifier。用 sealed oracle 回标 curator 的准入质量，而不是只看闭环策略分数。

## 对 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：在 token/score 蒸馏前乘以经验可学习性权重，避免 noisy judge 把错误方向放大。
- **A/B/T 与序数分布**：将“证据不足/不可归因”显式保留为 T，不强制压成负样本。
- **程序化/环境真值门控**：优先用可重放失败、确定性错误码和环境结算确认方向。
- **student-generated critique states**：只接纳能指向具体证据、且在重放中稳定的 critique。
- **高熵分叉与探索**：筛掉不可学失败不等于删掉罕见分支；应按失败原因分层保留探索样本。
- **sealed eval**：冻结独立评测器与隐藏重放集，分别报告 curator precision/recall 和策略收益，防止 curator、judge、optimizer 三者共适应。