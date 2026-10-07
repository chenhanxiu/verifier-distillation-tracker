# Evaluate the Stack, Not the Layer: Do Deterministic and LLM Gates for Agent Actions Fail Independently?

- 作者：Chenglin Yang
- 首次公开日期：2026-10-05
- 版本日期：2026-10-05（v1）
- 原始论文：https://arxiv.org/abs/2610.07359
- Canonical URL：https://arxiv.org/abs/2610.07359
- 代码：未发现公开代码链接

## 一句话结论

【论文原文】多个 LLM gate 的错误强相关，两层 judge 仅相当于约 1.2–1.4 个独立乘法层；确定性规则加一个 judge 更接近独立，因此 verifier 栈应按联合覆盖而非单层准确率设计。

## 真正新增的内容

【论文原文】论文以 multiplication-equivalent layers 衡量组合防线，并同时报告不同 escalation 计分规则、相关系数、理论耦合下限和服务模型漂移对结论的影响。

## 核心方法

【论文原文】在三个语料的 1,119 个标注 Agent 动作上比较一个确定性规则层和四个 LLM judges；分别以 STRICT（升级人工算未拦截）与 PRIMARY（升级算捕获）定义 miss，估计两层栈的有效独立层数。

## 关键实验结果

【论文原文】STRICT 下任意两 judge 仅约 1.2–1.4 层，φ 中位数 +0.430，6/6 配对显著；规则+judge 为 1.86–2.09 层，φ 中位数 +0.014，0/4 显著。PRIMARY 下分别为 1.21–1.57 与 1.80–2.13。某 judge 112 批中 50 批被错误模型版本服务，且 review verdict 计分变化反转五项结论。

## 证据质量与局限

【论文原文】有预声明规则、双重计分和服务版本审计，并公开报告结论反转。【分析推断】样本量尚可但仅三个语料、无自适应攻击；有效层数依赖 miss 定义，不能外推为普遍安全保证。

## 最接近的相关工作

【分析推断】与 Agreement Overstates Evidence、多 Judge 有效规模、Calibration Is Not Verification 和 Black-Box Judge 测量不稳定性直接相连。

## 如何复用或推进 LLM-as-a-Verifier

【分析推断】选择 verifier 组合时优化边际联合覆盖和错误互信息，而不是平均准确率；至少保留一个机制异质的确定性/环境通道，并记录实际服务模型版本。

## 对 Agent verifier × OPD 实验路线的具体影响

- 【分析推断】score-level OPD：teacher panel 权重按条件错误相关校正。
- 【分析推断】A/B/T：judge 高一致但错误相关时提高 T，而非增强 A/B 置信度。
- 【分析推断】真值门控：确定性层独立保留，不被 LLM 多数票覆盖。
- 【分析推断】critique states：同源 judges 的重复 critique 不算独立证据。
- 【分析推断】高熵分叉：预算优先给机制异质 verifier。
- 【分析推断】sealed eval：锁定 endpoint/model 版本，同时预注册 escalation 计分规则。