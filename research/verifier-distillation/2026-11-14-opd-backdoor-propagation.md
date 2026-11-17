# On-policy Distillation as a Backdoor Propagation Channel

- **作者**：Zane Fu、Yanzhao Zheng、Ziting Qin、Qianshan Wei、Yi Yu、Gongli Xi、Jihuai Zhu、Baohua Dong、Hangcheng Zhu、Ruohui Huang、Gang Yu
- **首次公开日期**：2026-11-14
- **版本日期**：2026-11-14（v1）
- **原始论文**：https://arxiv.org/abs/2611.19207
- **代码**：未发现公开代码
- **标识符**：arXiv:2611.19207；DOI: 10.48550/arXiv.2611.19207

## 一句话结论

【论文原文】OPD 会通过 triggered 与 clean 输入上的异常条件概率差，把 teacher 后门高效传入 student，且传播强于传统蒸馏，即使 trigger 暴露比例极小。

## 真正新增的内容

【论文原文】作者先用 SFT 给 teacher 植入条件后门，再比较 OPD 与传统蒸馏的传播。机制分析把传播定位到 teacher 条件概率异常及其在 student 内部表示中的逐步内化，并提出从蒸馏监督源头抑制异常概率信号的训练方法。

【分析推断】这直接否定“只要 student rollout 是 on-policy，teacher logits 就天然安全”的假设。verifier × OPD 路线必须把 teacher 可靠性门控扩展到输入条件差分和稀有 trigger 分支。

## 核心方法

1. 在 teacher 中植入条件触发后门，控制 trigger 暴露比例。
2. 比较 OPD 与常规蒸馏的 student 后门继承，并分析 logits 与内部表示。
3. 识别异常 conditional-probability signal，并在源头过滤或抑制。

## 关键实验结果

【论文原文】极少 trigger prompt 暴露即可通过 OPD 传播后门，且强度显著高于传统蒸馏；异常概率差是主要传输通道。摘要未提供具体攻击成功率、模型规模和缓解后残余风险数字。

## 证据质量与局限

【论文原文】包含受控植入、跨蒸馏范式比较、机制分析和针对性缓解。

【分析推断】人工后门未必覆盖自然产生的 verifier 偏差或复杂 Agent trigger；没有摘要级绝对数值，难判断缓解成本。防御若只压平异常概率，也可能误伤高熵但有价值的少数分支。

## 最接近的相关工作

最接近 IWD 的 teacher 稳定性加权、RoboDrop 的梯度相容门控、OPRD 的方向筛选与 Reward Hacking monitor。本文新增的是 OPD 作为安全风险传播通道的直接证据。

## 如何复用或推进 LLM-as-a-Verifier

用独立 verifier 比较 clean/perturbed/triggered 条件下的 teacher score 与 logits 差异；若方向只在稀有表面模式上突变，则隔离样本并要求环境真值复核。保留审计日志，不让同一 teacher 同时生成监督和批准异常。

## 对现有 Agent verifier × OPD 实验路线的具体影响

- **score-level OPD**：加入条件差分异常分数和 teacher trust gate。
- **pairwise A/B/T 与序数分布**：触发扰动前后 verdict 翻转但环境不变时标 T/可疑，不生成 A/B。
- **环境真值门控**：只有独立执行结果能覆盖异常 teacher 方向。
- **student-generated critique states**：对稀有短语、格式和工具参数做反事实触发审计。
- **高熵探索**：防御需区分恶意突变与真实多模态，避免一律削平尾部。
- **sealed eval**：隐藏 trigger、teacher 来源和攻击族，单独报告后门成功率与正常能力损失。

