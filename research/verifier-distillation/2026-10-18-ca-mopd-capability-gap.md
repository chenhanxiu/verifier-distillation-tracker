# Beyond Policy Discrepancy: Capability-Aware Multi-Teacher On-Policy Distillation

- **作者**：Xuanfeng Yang、Le Gui、Jiaming Wang、Xuan Zhang
- **首次公开日期**：2026-10-18
- **版本日期**：2026-10-18（v1）
- **原始论文**：https://arxiv.org/abs/2610.26950
- **arXiv ID**：2610.26950
- **DOI**：https://doi.org/10.48550/arXiv.2610.26950
- **代码/项目**：未公开

## 一句话结论

CA-MOPD 用 verifier 估计的能力差而非 teacher–student 策略分歧分配多 teacher 蒸馏强度，避免 student 已追平甚至超过 teacher 后仍被强制模仿。

## 真正新增的内容

论文明确区分行为分布不一致与真实能力缺口，并把能力回退作为重新增强监督的触发条件。

## 核心方法

先合并多个 RL specialist 得到较强初始化，再由 verifier 估计各域 teacher–student capability gap；差距缩小时降低该域蒸馏权重，student 回退时重新提高，同时保留 teacher 的稠密 token 监督。

## 关键实验结果

六个数学、代码和指令遵循 benchmark 的平均分为 32.22，分别比 naive MOPD、Open-MOPD 和仅合并初始化高 0.86、0.83、0.74 点。

## 证据质量与局限

包含匹配预算的受控对照和六项 benchmark，但绝对增益较小；结果依赖 capability verifier 的校准质量，尚未展示 verifier 被 student 策略利用时的稳健性。

## 最接近的相关工作

最接近 Nash-MOPD、VG-OPD、RetireOPD、SPOD 与 verifier-gated multi-teacher routing；区别是直接以能力差而非 KL/训练进展决定域级权重。

## 如何复用或推进 LLM-as-a-Verifier

把环境成功率、程序化断言和 sealed benchmark 组合成 capability gap，作为 score-level OPD 的上层域门控；token 级 teacher 分布只决定门内更新。

## 对 Agent verifier × OPD 实验路线的具体影响

【分析推断】现有 Agent verifier × OPD 应新增“策略分歧高但能力差≤0”的冻结/保护状态；A/B/T 中这类样本应偏向 T，而不是自动判 teacher 为 A。

## 结论边界

除明确标注“分析推断”的段落外，上述方法与实验结论来自论文原文或公开摘要；推断部分是面向现有研究路线的可检验假设，不应视为论文作者已经证明的结论。
